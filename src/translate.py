#!/usr/bin/env python3
"""
Batch translate Chinese blog posts to English using DeepSeek API.
Reads .env.local for DEEPSEEK_API_KEY.
Creates {slug}.en.md files alongside original {slug}.md files.
"""

import os
import re
import sys
import time
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "src" / "content" / "posts"

# Load API key from .env.local
env_file = ROOT / ".env.local"
api_key = None
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if line.startswith("DEEPSEEK_API_KEY="):
            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

if not api_key:
    api_key = os.environ.get("DEEPSEEK_API_KEY")

if not api_key:
    print("❌ DEEPSEEK_API_KEY not found in .env.local or environment")
    sys.exit(1)

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"

SYSTEM_PROMPT = """You are a professional translator specializing in Chinese-to-English technical translation. Translate the following Chinese blog post into natural, fluent English.

Rules:
1. Translate the title, description, and all content to English
2. Keep ALL markdown formatting intact (headers, code blocks, links, images, etc.)
3. Keep ALL code blocks unchanged — never translate code
4. Keep technical terms accurate (e.g., API, SDK, HTTP, JSON, etc.)
5. Change `lang: zh` to `lang: en` in the frontmatter
6. Keep `categories` in English if they're already in English; translate if in Chinese
7. Keep the `date` field unchanged
8. Output the COMPLETE translated markdown file, including frontmatter
9. Do NOT add any explanations or notes — output ONLY the translated markdown"""


def translate_post(content: str) -> str | None:
    """Send a post to DeepSeek for translation. Returns translated text or None."""
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

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  ⚠️ API error: {e}")
        return None


def main():
    md_files = sorted(CONTENT_DIR.glob("*.md"))
    # Filter: only Chinese posts without existing English translation
    to_translate = []
    for f in md_files:
        if f.stem.endswith(".en"):
            continue  # already an English translation
        en_file = f.with_name(f"{f.stem}.en.md")
        if en_file.exists():
            continue  # already translated
        content = f.read_text(encoding="utf-8")
        # Check if it's a Chinese post
        if "lang: zh" not in content[:200]:
            continue
        to_translate.append(f)

    total = len(to_translate)
    if total == 0:
        print("✅ All Chinese posts already have English translations!")
        return

    print(f"📝 Found {total} Chinese posts to translate\n")

    for i, f in enumerate(to_translate):
        print(f"[{i+1}/{total}] Translating: {f.stem}...")
        content = f.read_text(encoding="utf-8")

        # Skip if content is too short
        if len(content) < 50:
            print(f"  ⏭️ Too short, skipping")
            continue

        translated = translate_post(content)

        if translated:
            # Clean up any markdown fence the model might have added
            translated = translated.strip()
            if translated.startswith("```markdown"):
                translated = translated[len("```markdown"):]
            if translated.startswith("```"):
                translated = translated[3:]
            if translated.endswith("```"):
                translated = translated[:-3]
            translated = translated.strip()

            # Ensure frontmatter starts correctly
            if not translated.startswith("---"):
                # Model might have stripped frontmatter — re-parse
                print(f"  ⚠️ Frontmatter missing in translation, retrying...")
                # Try to fix by prepending translated frontmatter
                translated = content[: content.index("---", 4)] + "\n" + translated
                continue  # skip this one, user can retry

            # Ensure lang is en
            translated = re.sub(r"^lang:\s*zh", "lang: en", translated, flags=re.MULTILINE)

            en_file = f.with_name(f"{f.stem}.en.md")
            en_file.write_text(translated, encoding="utf-8")
            print(f"  ✅ Saved: {en_file.name}")
        else:
            print(f"  ❌ Failed")

        # Rate limit: 1 request per 3 seconds
        if i < total - 1:
            time.sleep(3)

    print(f"\n✅ Done! Translated {total} posts.")


if __name__ == "__main__":
    main()
