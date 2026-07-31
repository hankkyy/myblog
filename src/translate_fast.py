#!/usr/bin/env python3
"""Fast concurrent batch translator — 5 parallel workers, no sleep between posts."""
import os, sys, json, urllib.request, time, re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "src/content/posts"

# Load API key
api_key = None
env_file = ROOT / ".env.local"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if line.startswith("DEEPSEEK_API_KEY="):
            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"

SYSTEM_PROMPT = """You are a professional translator. Translate this Chinese blog post into natural, fluent English.

Rules:
1. Translate the title, description, and all content to English
2. Keep ALL markdown formatting intact (headers, code blocks, links, images)
3. Keep ALL code blocks unchanged — never translate code
4. Keep technical terms accurate (API, SDK, HTTP, JSON, etc.)
5. Change `lang: zh` to `lang: en` in the frontmatter
6. Translate Chinese categories to English
7. Keep the `date` field unchanged
8. Output the COMPLETE translated markdown file, including frontmatter
9. Output ONLY the translated markdown — no explanations"""

def translate_one(f: Path) -> tuple[str, bool]:
    """Translate a single post. Returns (stem, success)."""
    try:
        content = f.read_text(encoding="utf-8")
        if len(content) < 50:
            return (f.stem, False)

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content},
            ],
            "temperature": 0.3,
            "max_tokens": 8192,
        }

        req = urllib.request.Request(
            DEEPSEEK_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )

        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            translated = result["choices"][0]["message"]["content"]

        translated = translated.strip()
        # Clean up code fences the model might add
        for prefix in ["```markdown\n", "```\n"]:
            if translated.startswith(prefix):
                translated = translated[len(prefix):]
        if translated.endswith("\n```"):
            translated = translated[:-4]

        # Ensure lang is en
        translated = re.sub(r"^lang:\s*zh", "lang: en", translated, flags=re.MULTILINE)

        en_file = f.with_name(f"{f.stem}.en.md")
        en_file.write_text(translated, encoding="utf-8")
        return (f.stem, True)

    except Exception as e:
        return (f.stem, False)


def main():
    md_files = sorted(CONTENT_DIR.glob("*.md"))
    to_translate = []
    for f in md_files:
        if f.stem.endswith(".en"):
            continue
        en_file = f.with_name(f"{f.stem}.en.md")
        if en_file.exists():
            continue
        content = f.read_text(encoding="utf-8")
        if "lang: zh" not in content[:200]:
            continue
        to_translate.append(f)

    total = len(to_translate)
    if total == 0:
        print("✅ All done!")
        return

    print(f"📝 {total} posts to translate (5 concurrent workers)\n")
    done = 0
    start = time.time()

    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(translate_one, f): f for f in to_translate}
        for future in as_completed(futures):
            stem, ok = future.result()
            done += 1
            elapsed = time.time() - start
            rate = done / elapsed * 60 if elapsed > 0 else 0
            status = "✅" if ok else "❌"
            print(f"[{done}/{total}] {status} {stem}  ({rate:.0f}/min)")

    elapsed = time.time() - start
    print(f"\n✅ Done! {done} posts in {elapsed:.0f}s ({done/elapsed*60:.0f}/min)")


if __name__ == "__main__":
    main()
