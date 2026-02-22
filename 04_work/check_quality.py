"""EPUBの品質チェックスクリプト"""
import re
from pathlib import Path
import os

os.chdir(Path(__file__).parent)

dist = Path("../05_生成/dist")
img = dist / "images"

# 画像数確認
for subdir in ["mermaid", "code", "pdf"]:
    d = img / subdir
    count = len(list(d.glob("*.png"))) if d.exists() else 0
    print(f"{subdir}: {count} images")

# images直下
for f in sorted(img.glob("*.*")):
    if f.is_file():
        print(f"  images/{f.name} ({f.stat().st_size}B)")

# 表紙確認
for p in ["../cover.png", "../cover.jpg", "../05_生成/cover.png"]:
    print(f"cover: {p} -> {Path(p).exists()}")

# book.html内の問題確認
html_path = dist / "book.html"
if html_path.exists():
    html = html_path.read_text(encoding="utf-8")
    fail_count = html.count("[図生成失敗]")
    print(f"\n[図生成失敗]の箇所: {fail_count}")
    
    img_tags = re.findall(r'<img[^>]+src="([^"]+)"', html)
    print(f"imgタグ総数: {len(img_tags)}")
    
    mermaid_imgs = [i for i in img_tags if "mermaid" in i]
    code_imgs = [i for i in img_tags if "code/" in i]
    pdf_imgs = [i for i in img_tags if "pdf/" in i]
    print(f"  mermaid参照: {len(mermaid_imgs)}")
    print(f"  code参照: {len(code_imgs)}")
    print(f"  pdf参照: {len(pdf_imgs)}")
    
    # 欠落画像
    missing = 0
    for src in img_tags:
        p = dist / src
        if not p.exists():
            print(f"  MISSING: {src}")
            missing += 1
    print(f"\n欠落画像: {missing}")
    
    # mermaidコードブロックの残存(変換されなかったもの)
    raw_mermaid = html.count("```mermaid")
    print(f"未変換mermaidブロック: {raw_mermaid}")
    
    # cコードブロックの残存
    raw_c = len(re.findall(r'```c\b', html))
    print(f"未変換cコードブロック: {raw_c}")
