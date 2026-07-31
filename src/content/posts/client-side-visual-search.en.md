---
lang: en
title: "How I Built a Browser-Based Reverse Image Search Engine for an Antique Auction Platform"
date: 2026-07-30T12:00:00+08:00
categories: ["Technology", "AI"]
description: "No GPU server needed — pack an entire visual search engine into the browser with multi-dimensional feature signatures, weighted similarity scoring, and confidence gating"
---

I independently developed an antique auction platform called Eastwood Auction. When users browse antiques like porcelain, jade, calligraphy, and bronze ware, they often have a reference photo in hand but don't know what the item is called, which category it belongs to, or which era it's from.

Keyword search is essentially useless in this scenario — an average buyer wouldn't type "Qing Qianlong blue-and-white interlocking lotus pattern appreciation vase." They'd just pull out a photo.

So I needed reverse image search. But here's the problem: I'm a solo developer with no GPU server; users might upload photos of antiques worth hundreds of thousands of dollars, making privacy highly sensitive; and auction browsing is fast-paced exploration that can't wait for the hundreds of milliseconds of server latency.

My final solution: **pack the entire visual search engine into the browser**.

## Overall Architecture

```
User Uploads Image
    │
    ▼
┌─────────────────────────────┐
│  Browser-Side Feature       │
│  Extraction                 │
│  • 48×48 pixel analysis     │
│    canvas                   │
│  • 8-dim color feature      │
│    vector                   │
│  • 14-dim extended          │
│    signature                │
└──────────────┬──────────────┘
               │
    ┌──────────┴──────────┐
    │                      │
    ▼                      ▼
┌──────────────┐   ┌──────────────────┐
│ Client-Side  │   │ Server-Side      │
│ Matching     │   │ Matching (Optional)│
│ • Signature  │   │ • HuggingFace API │
│   similarity │   │ • pgvector vector │
│ • Confidence │   │   search          │
│   gating     │   │ • 512-dim         │
│ • Instant    │   │   embedding       │
│   results    │   │                   │
└──────────────┘   └──────────────────┘
```

The default path is client-side: zero server cost, zero latency, and privacy-preserving. The server-side path serves as a fallback as the knowledge base grows.

## Core One: Image Signature Design

### Layer 1: 8-Dimensional Color Feature Vector

```typescript
type ArtworkFeatureVector = [
  red: number,        // Average red channel intensity
  green: number,      // Average green channel intensity
  blue: number,       // Average blue channel intensity
  brightness: number, // Overall brightness
  saturation: number, // Color saturation
  warmth: number,     // Warm tone tendency (red + gold)
  coolness: number,   // Cool tone tendency (blue + green)
  contrast: number    // Light-dark contrast
];
```

This 8-dimensional vector serves as a "coarse filter." For instance, a piece of blue-and-white porcelain (blue-white tones) and a bronze piece (warm brown tones) can be distinguished by this vector alone. But color alone isn't enough — when two pieces are both blue-and-white porcelain, their colors are nearly identical, requiring deeper features to differentiate them.

### Layer 2: 14-Dimensional Extended Signature

This includes a 48-bin RGB color histogram, 16-bin edge intensity spatial distribution, two perceptual hashes (aHash + dHash), 8×8 luminance spatial distribution, 8-bin edge orientation distribution, horizontal and vertical projections of foreground pixels, foreground ratio and centroid position — 14 dimensions in total.

Key design decisions:

1. **Two hashes instead of one**: aHash (average hash) is sensitive to luminance distribution, making it good for distinguishing "white porcelain" from "bronze"; dHash (gradient hash) is sensitive to edges, making it good for distinguishing "plain surface" from "carved patterns." They complement each other, and the computational cost is nearly zero.

2. **rowProfile/columnProfile capture object silhouettes**: Project foreground pixels onto horizontal and vertical axes to get a 16-dimensional "shape signature." This lets the system distinguish a "slender vase" from a "flat plate," even when colors are identical.

3. **Foreground segmentation without deep learning**: Sample border pixels as background color estimates, then compute the color distance of each pixel against the background. For antique auctions, which typically feature solid-color photography backdrops, this performs well enough.

### Why 48×48?

| Resolution | Pixels | Edge Detection Quality | Processing Time |
|------------|--------|------------------------|-----------------|
| 32×32 | 1,024 | Blurry edges | ~2ms |
| **48×48** | **2,304** | **Sufficiently clear** | **~5ms** |
| 64×64 | 4,096 | Slightly better | ~18ms |

48×48 is the sweet spot: 2,304 pixels provide enough data for edge detection and spatial distribution analysis, while processing time stays at just ~5ms.

## Core Two: Weighted Similarity Scoring

### Vector Similarity (8-dim)

The RGB channels carry a weight of 0.3 because color information is already expressed more finely in the lower-level signatures and shouldn't dominate repeatedly at the vector layer.

### Signature Similarity (14-dim, Weighted Combination)

| Feature | Weight | What It Captures |
|---------|--------|------------------|
| rowProfile | 18% | Horizontal object silhouette |
| columnProfile | 18% | Vertical object silhouette |
| edgeOrientation | 14% | Texture direction |
| edgeHistogram | 12% | Edge spatial distribution |
| luminanceGrid | 10% | Light-dark distribution |
| differenceHash | 8% | Gradient structure |
| averageHash | 8% | Luminance structure |
| aspectRatio | 5% | Object proportions |
| centroid | 5% | Object position |
| foregroundRatio | 4% | Object size |
| texture | 3% | Texture complexity |
| colorHistogram | 3% | Color distribution |

rowProfile and columnProfile carry the highest weights (18% each) because for antiques, **form** is the most critical classification feature — a plum vase and a brush pot may share similar colors and textures, but their silhouettes are completely different.

### Shape Gate

This is the most important false-positive prevention mechanism in the entire system. It computes "shape consistency" — the average similarity of row + column + aspectRatio — then applies a shape gate factor to correct the final score. If shape consistency falls below 0.38, the score is hard-capped at 42 points (out of 100).

This means: **even if colors are identical, a shape mismatch will significantly suppress the score**. It prevents the system from incorrectly matching a "red vase" to a "red plate."

### Final Score Composition

When both signature and vector are available: `finalScore = 0.94 × signatureScore + 0.06 × vectorScore`. When only the vector exists (legacy data), the weight drops to 0.58 because matching without signatures is less trustworthy.

## Core Three: Confidence Gating — Proactively Saying "I Don't Know"

Most search systems return Top-K results regardless of whether they match. We chose a different strategy:

- Minimum total score ≥72
- Minimum signature score ≥0.64
- Minimum shape consistency ≥0.58
- Minimum vector score ≥0.52
- Higher threshold without signature ≥92
- Minimum score gap between #1 and #2 ≥6

All six thresholds must pass before results are returned. If none pass, the system explicitly states: *"This image differs significantly from items in the current knowledge base. The system has proactively rejected low-confidence results."*

This is especially critical in antique trading scenarios — buyers may make purchase decisions based on match results, and a misleading match is worse than no match at all.

## Core Four: Hybrid Architecture — Client + Server

The server-side path handles backend indexing and retrieval as the knowledge base scales:

```
Image → HuggingFace Embedding API → 512-dim vector → L2 normalization → pgvector similarity search
```

Implemented via Supabase's `match_artworks_by_image` RPC function, supporting both `index-artwork` and `match-image` operations.

## Performance Data

Measured on an M2 MacBook Pro (Chrome):

| Operation | Time |
|-----------|------|
| Image loading + resizing | ~2ms |
| Feature vector extraction | ~0.01ms |
| Signature construction | ~5ms |
| Search (100 items) | ~3ms |
| **Total (first run)** | **~10ms** |

For 1,000 artworks, estimated search time is ~30ms — still far below the human perception threshold. Memory footprint: ~2KB of feature data per artwork, ~2MB for 1,000 items.

## Engineering Highlights

**Type safety**: All feature vectors and signatures are strongly typed in TypeScript, with the compiler checking dimension lengths and order.

**Blob URL memory management**: Blob URLs created from uploaded images are manually released after search completes, preventing memory leaks during extended browsing of auction catalogs.

**Progressive image encoding**: Images uploaded to the knowledge base automatically try different JPEG quality levels (0.82→0.72→0.6→0.5) to find the optimal encoding at ≤1.6MB.

**CDN proxy**: All external images pass through the `/api/proxy-image` proxy, solving the issue of inaccessible image sources like Unsplash from mainland China.

## Future Directions

- **WASM acceleration**: Compile signature extraction to WebAssembly for an estimated 2-3× speedup
- **Service Worker caching**: Store signatures in IndexedDB for instant availability on page load
- **Hybrid ranking**: Combine client-side signature scores with server-side embedding scores for learned ranking
- **3D search**: The platform already supports LiDAR 3D models (USDZ/GLB); extend to 3D shape matching

## Summary

This project proves that: **you don't need a GPU server or a deep learning framework to build a practical reverse image search feature right in the browser**.

Key takeaways:
- **Multi-dimensional feature signatures** > single features (14 dimensions, weighted combination)
- **Shape gating** prevents color from misleading (the most important line of defense)
- **Confidence gating** proactively rejects unreliable results
- **Client-first** reduces cost and latency, with server as fallback

The code is open-sourced at [github.com/hankkyy/EastWood-Auction](https://github.com/hankkyy/EastWood-Auction).