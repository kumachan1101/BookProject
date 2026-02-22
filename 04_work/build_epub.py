from pathlib import Path
import re
import subprocess
import shutil
import os
import sys
from pygments import highlight
from pygments.lexers import CLexer
from pygments.formatters import HtmlFormatter
import imgkit

# ========= 設定 =========
CHAPTER_DIR = Path("../02_章別")  # 修正: 02_章別を対象にする
DIST_DIR = Path("../05_生成/dist")
IMG_DIR = DIST_DIR / "images"
MERMAID_DIR = IMG_DIR / "mermaid"
CODE_IMG_DIR = IMG_DIR / "code"
PDF_IMG_DIR = IMG_DIR / "pdf"

# PDF資料のパス（04_workから見た相対パス）
RESOURCE_PDF_PATH = Path("../03_資料/SOLID_C_Architecture.pdf")

# PDFページ → MDファイルインデックスのマッピング（20ページ分）
# インデックスは sorted(02_章別/*.md) の順番に対応
# PDFスライドは章順に作成されているため、順番に各章の先頭ファイルへ対応付け
PAGE_TO_MD_INDEX = {
    0:  0,   # PDF p1  → 01_序論
    1:  1,   # PDF p2  → 02_第1部 学習ガイドマップ
    2:  2,   # PDF p3  → 03_第1部 第1章 static
    3:  3,   # PDF p4  → 04_第1部 第2章 関数ポインタ_01
    4:  5,   # PDF p5  → 05_第1部 第3章 構造体_01
    5:  7,   # PDF p6  → 06_第1部 第4章 不完全型
    6:  8,   # PDF p7  → 07_第1部 第5章 モジュール_01
    7:  10,  # PDF p8  → 08_第1部 第6章 エラーハンドリング_01
    8:  12,  # PDF p9  → 09_第1部 第7章 メモリ管理_01
    9:  14,  # PDF p10 → 10_第1部 まとめ
    10: 15,  # PDF p11 → 11_第2部 学習ガイドマップ
    11: 16,  # PDF p12 → 12_第2部 第8章 SRP_01
    12: 18,  # PDF p13 → 13_第2部 第9章 OCP_01
    13: 20,  # PDF p14 → 14_第2部 第10章 LSP_01
    14: 22,  # PDF p15 → 15_第2部 第11章 ISP_01
    15: 24,  # PDF p16 → 16_第2部 第12章 DIP_01
    16: 27,  # PDF p17 → 17_第2部 第13章 統合（基本）_01
    17: 29,  # PDF p18 → 18_第2部 第14章 統合（応用）_01
    18: 31,  # PDF p19 → 19_第2部 第15章 SOLID統合
    19: 32,  # PDF p20 → 20_結論
}

BOOK_HTML = DIST_DIR / "book.html"
BOOK_EPUB = DIST_DIR / "book.epub"
BOOK_MOBI = DIST_DIR / "book.mobi"

COVER_IMAGE = Path("../05_生成/cover.png")

# Kindle互換性設定
MAX_IMAGE_WIDTH = 1400
MAX_IMAGE_HEIGHT = 1600

# 【重要】ご自身の環境に合わせてパスを変更してください
MMDC = r"C:\Users\kumac\AppData\Roaming\npm\mmdc.cmd"

TARGET_CODE_IMAGE_HEIGHT = 1400  # コード画像の目標高さ
LINE_HEIGHT_PX = 55              # 1行あたりの推定高さ (line-height 1.45 * font-size 38px)

IMGKIT_OPTIONS = {
    "format": "png",
    "encoding": "UTF-8",
    "quiet": "",
    "width": str(MAX_IMAGE_WIDTH),
    "minimum-font-size": "1",    # フォントサイズ縮小を防止
    "quality": "95",
    "disable-smart-width": "",   # 指定幅を厳守
}

# 視認性を最大化したCSS設定（ファイル名見出し・色分け強化版）
CODE_CSS = """
<style>
/* 全体の背景 */
body { margin: 0; padding: 0; background: #1a1a1a; width: 1400px; min-width: 1400px; max-width: 1400px; box-sizing: border-box; overflow: hidden; }

/* Pygmentsハイライトコンテナ */
.highlight {
  background: #1a1a1a !important;
  font-size: 38px !important; /* 文字サイズ大 */
  line-height: 1.45 !important; /* 行間を広めに */
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
  font-weight: 600 !important;
}

/* コード表示領域 */
.highlight pre {
  background: #1a1a1a !important;
  color: #f8f8f2 !important; /* 文字色を白に近づける */
  padding: 35px !important;
  margin: 0 !important;
  font-size: 38px !important;
  line-height: 1.45 !important;
  font-weight: 600 !important;
  border: 2px solid #44475a; /* 枠線を少し明るく */
  white-space: pre-wrap;
  word-break: break-all;
  overflow-wrap: break-word;
  word-wrap: break-word;
}

/* --- シンタックスハイライト（色分けの明確化） --- */

/* 1. コメント: 暗めのグレー（背景に沈ませる） */
.highlight .c1, .highlight .cm, .highlight .c {
  color: #6272a4 !important; /* 青みがかったグレー */
  font-weight: normal !important; /* コメントは太字にしない */
  font-style: italic !important;
}

/* 2. プリプロセッサ (#include, #define): 鮮やかなピンク */
.highlight .cp { 
  color: #ff79c6 !important; 
  font-weight: 700 !important; 
}

/* 3. インクルードファイル名 (<stdio.h>): 明るい水色（コメントと完全に区別） */
.highlight .cpf { 
  color: #8be9fd !important; 
  font-weight: 700 !important; 
}

/* キーワード (if, return, int, void) - ピンク/紫系 */
.highlight .k, .highlight .kt { color: #ff79c6 !important; font-weight: 700 !important; }

/* 関数名 - 緑色 */
.highlight .nf, .highlight .nb { color: #50fa7b !important; font-weight: 700 !important; }

/* 変数名 - 白 */
.highlight .n { color: #f8f8f2 !important; }

/* 数値 - 紫 */
.highlight .mi, .highlight .mf { color: #bd93f9 !important; font-weight: 700 !important; }

/* 文字列 - 黄色 */
.highlight .s { color: #f1fa8c !important; font-weight: 700 !important; }

/* 演算子 - ピンク */
.highlight .o { color: #ff79c6 !important; font-weight: 700 !important; }

/* 括弧・カンマ - 白 */
.highlight .p { color: #f8f8f2 !important; }
</style>
"""

# MAX_LINES_PER_IMAGE は動的計算に置き換え（TARGET_CODE_IMAGE_HEIGHT / LINE_HEIGHT_PX ベース）


# ========= 初期化 =========
def force_remove_dist():
    """distフォルダを確実に削除して再作成する"""
    if DIST_DIR.exists():
        print(f"[INIT] {DIST_DIR} をクリーンアップ中...")
        def handle_remove_readonly(func, path, excinfo):
            import stat
            os.chmod(path, stat.S_IWRITE)
            func(path)
        try:
            shutil.rmtree(DIST_DIR, onerror=handle_remove_readonly)
        except Exception as e:
            print(f"[WARN] distの削除失敗: {e}")

    MERMAID_DIR.mkdir(parents=True, exist_ok=True)
    CODE_IMG_DIR.mkdir(parents=True, exist_ok=True)
    PDF_IMG_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[INIT] ディレクトリ準備完了")

force_remove_dist()


def optimize_image(img_path: Path):
    """画像をKindle互換サイズに最適化"""
    try:
        from PIL import Image
        img = Image.open(img_path)
        width, height = img.size
        if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
            ratio = min(MAX_IMAGE_WIDTH / width, MAX_IMAGE_HEIGHT / height)
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            img.save(img_path, "PNG", optimize=True)
            print(f"    画像最適化: {width}x{height} -> {new_size[0]}x{new_size[1]}")
        else:
            img.save(img_path, "PNG", optimize=True)
    except ImportError:
        pass
    except Exception as e:
        print(f"    [WARN] 画像最適化失敗: {e}")

# 表紙画像をコピー
cover_dest = None
if COVER_IMAGE.exists():
    cover_dest = IMG_DIR / COVER_IMAGE.name
    shutil.copy(COVER_IMAGE, cover_dest)
    print(f"[COVER] 表紙画像をコピー: {COVER_IMAGE.name}")
    optimize_image(cover_dest)
elif Path("cover.jpg").exists():
    COVER_IMAGE = Path("cover.jpg")
    cover_dest = IMG_DIR / COVER_IMAGE.name
    shutil.copy(COVER_IMAGE, cover_dest)
    print(f"[COVER] 表紙画像をコピー: {COVER_IMAGE.name}")
    optimize_image(cover_dest)
else:
    print("[INFO] 表紙画像が見つかりません")


# ========= PDF処理 =========
def split_pdf_by_pages() -> dict:
    """PDFを各ページ画像に変換し、MDファイルインデックスに対応付ける"""
    if not RESOURCE_PDF_PATH.exists():
        print(f"[WARN] PDFが見つかりません: {RESOURCE_PDF_PATH}")
        return {}

    print(f"[PDF] {RESOURCE_PDF_PATH.name} を各章に配分中...")
    chapter_images = {}  # {md_index: [image_rel_paths]}

    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(RESOURCE_PDF_PATH))
        total_pages = len(doc)
        print(f"[PDF] 総ページ数: {total_pages}")

        for page_num in range(total_pages):
            chapter_index = PAGE_TO_MD_INDEX.get(page_num)
            if chapter_index is None:
                print(f"[WARN] ページ{page_num}はマッピングなし")
                continue

            page = doc[page_num]
            zoom = 150 / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            out_path = PDF_IMG_DIR / f"chapter{chapter_index:02d}_page{page_num+1:02d}.png"
            pix.save(str(out_path))
            optimize_image(out_path)

            if chapter_index not in chapter_images:
                chapter_images[chapter_index] = []
            chapter_images[chapter_index].append(f"images/pdf/{out_path.name}")
            print(f"  -> 章{chapter_index} にPDFページ{page_num+1}を配分")

        doc.close()
        print(f"[PDF] {len(chapter_images)}章に配分完了")
        return chapter_images

    except ImportError:
        print("[ERROR] PyMuPDFがインストールされていません: pip install PyMuPDF")
    except Exception as e:
        print(f"[ERROR] PDF処理失敗: {e}")
    return {}


# PDFを各章に配分
chapter_pdf_images = split_pdf_by_pages()


# ========= Mermaid =========
def sanitize_mermaid(code: str) -> str:
    lines = code.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    code = "\n".join(cleaned_lines)
    code = code.replace('　', '  ')
    code = re.sub(r'graph\s+LR\b', 'graph TB', code, flags=re.I)
    code = re.sub(r'flowchart\s+LR\b', 'flowchart TB', code, flags=re.I)
    code = re.sub(r'^(graph|flowchart|classDiagram|mindmap|sequenceDiagram)(.*)$', r'\1\2', code, flags=re.M)
    return code.strip()

def mermaid_to_image(code: str, out_png: Path, img_index:int) -> bool:
    cleaned_code = sanitize_mermaid(code)
    tmp_mmd = out_png.parent / f"temp_diag_{img_index}.mmd"
    with open(tmp_mmd, "w", encoding="utf-8", newline="\n") as f:
        f.write(cleaned_code)
    
    try:
        cmd = [
            MMDC, "-i", str(tmp_mmd), "-o", str(out_png),
            "--backgroundColor", "white", "--scale", "3",
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        if res.returncode != 0:
            print(f"[ERROR] mmdc stderr: {res.stderr}")
            return False
        print(f"  -> Mermaid画像 {img_index} 作成成功")
        optimize_image(out_png)
        return True
    except Exception as e:
        print(f"[ERROR] Mermaid例外: {e}")
        return False
    finally:
        if tmp_mmd.exists(): tmp_mmd.unlink()

# ========= ソースコード画像化（ファイル名ヘッダー改善版） =========
def code_to_images_with_title(code: str, md_stem: str, code_index: int, title: str = None) -> list:
    lines = code.splitlines()
    images = []
    
    print(f"  コード全体: {len(lines)}行")
    
    formatter = HtmlFormatter(full=False, style="dracula", linenos=False, noclasses=True)
    full_highlighted = highlight(code, CLexer(), formatter)
    
    pre_match = re.search(r'<pre[^>]*>(.*?)</pre>', full_highlighted, re.DOTALL)
    if not pre_match: return []
    
    highlighted_lines = pre_match.group(1).split('\n')
    start_line = 0
    part_num = 0
    
    # 固定行数で統一（サイズの安定化）
    MAX_LINES = 28
    # タイトル付き最初の画像は少し減らす
    MAX_LINES_WITH_TITLE = 25
    # オーファン防止：残りがこの行数以下なら前のチャンクに含める
    ORPHAN_THRESHOLD = 6
    
    while start_line < len(highlighted_lines):
        is_first = (part_num == 0 and title)
        max_lines_for_chunk = MAX_LINES_WITH_TITLE if is_first else MAX_LINES
        remaining = len(highlighted_lines) - start_line
        chunk_size = min(remaining, max_lines_for_chunk)
        
        # オーファン防止：次のチャンクが少なすぎる場合、今のチャンクに含める
        next_remaining = remaining - chunk_size
        if 0 < next_remaining <= ORPHAN_THRESHOLD:
            chunk_size = remaining  # 全部含める
        
        end_line = start_line + chunk_size
        chunk_html = '\n'.join(highlighted_lines[start_line:end_line])
        
        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{CODE_CSS}
</head>
<body>
"""
        # ファイル名（タイトル）の見やすさを改善
        # 背景色を明るいパープルグレーに変更し、黒いコード部分と明確に区別
        if title and part_num == 0:
            html += f"""<div style="background: #FFFFFF; color: #000000; padding: 25px 40px; 
            font-family: 'Consolas', 'Monaco', monospace; font-size: 34px; 
            font-weight: 800; border-bottom: 4px solid #999999; margin-bottom: 0;">
{title}
</div>
"""
        
        html += f"""<div class="highlight"><pre>{chunk_html}</pre></div>
</body>
</html>"""
        
        img_name = f"{md_stem}_code{code_index}_part{part_num}.png"
        out_path = CODE_IMG_DIR / img_name
        
        try:
            imgkit.from_string(html, str(out_path), options=IMGKIT_OPTIONS)
            print(f"  -> 画像作成: {img_name}")
            optimize_image(out_path)
            images.append(img_name)
        except Exception as e:
            print(f"[ERROR] 画像生成失敗 {img_name}: {e}")
        
        start_line = end_line
        part_num += 1
    
    return images


# ========= Markdown要素処理 =========
def md_links_to_html(text: str) -> str:
    return re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', r'<a href="\2">\1</a>', text)

def inline_code_to_html(text: str) -> str:
    return re.sub(r'`([^`\n]+)`', r"<code style='font-family: monospace; font-size: 0.95em; background-color: #f5f5f5; padding: 0.15em 0.4em; border: 1px solid #e0e0e0; font-weight: 600;'>\1</code>", text)

def emphasize_code_symbols(text: str) -> str:
    def safe_sub(pattern, repl, text):
        parts = re.split(r'(<a\s+[^>]+>.*?</a>)', text, flags=re.S)
        for i in range(len(parts)):
            if not parts[i].startswith('<a '):
                parts[i] = re.sub(pattern, repl, parts[i])
        return ''.join(parts)

    protected = []
    def protect_include(m):
        protected.append(m.group(0))
        return f"@@INCLUDE_{len(protected)-1}@@"
    
    text = re.sub(r'#include\s*<[^>]+>', protect_include, text)

    text = safe_sub(
        r'\b([a-zA-Z_][a-zA-Z0-9_]*\.(?:c|h))\b',
        r"<code style='font-family: monospace; font-weight: 600; background-color: #f5f5f5; padding: 0.1em 0.3em; border: 1px solid #e0e0e0;'>\1</code>",
        text
    )
    text = safe_sub(
        r'\b([a-zA-Z_][a-zA-Z0-9_]*)\(\)',
        r"<code style='font-family: monospace; font-weight: 600; background-color: #e3f2fd; padding: 0.1em 0.3em; border: 1px solid #bbdefb;'>\1()</code>",
        text
    )

    for i, inc in enumerate(protected):
        text = text.replace(f"@@INCLUDE_{i}@@", inc)
    return text

def md_images_to_html(md_text: str) -> str:
    code_blocks = []
    def _cb(m):
        code_blocks.append(m.group(0))
        return f"@@CODEBLOCK_{len(code_blocks)-1}@@"
    md_text = re.sub(r"```[\s\S]*?```", _cb, md_text)

    inline_codes = []
    def _ic(m):
        inline_codes.append(m.group(0))
        return f"@@INLINECODE_{len(inline_codes)-1}@@"
    md_text = re.sub(r"`[^`]*`", _ic, md_text)

    def _img(m):
        alt = m.group(1); path = m.group(2).strip()
        if not path.startswith("images/"): path = f"images/{Path(path).name}"
        return f'<img src="{path}" alt="{alt}" style="max-width:100%; height:auto;" />'
    md_text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', _img, md_text)

    for i, c in enumerate(inline_codes): md_text = md_text.replace(f"@@INLINECODE_{i}@@", c)
    for i, c in enumerate(code_blocks): md_text = md_text.replace(f"@@CODEBLOCK_{i}@@", c)
    return md_text


# ========= Markdown処理 =========
def process_md(md_path: Path, chapter_index: int = -1):
    print(f"\n[MD] {md_path.name}")
    text = md_path.read_text(encoding="utf-8")
    
    # 章タイトル抽出
    h1_match = re.search(r"^# (.+)$", text, flags=re.M)
    chapter_title = h1_match.group(1) if h1_match else md_path.stem

    code_counter = 0
    code_placeholders = {}

    def extract_code_common(code, heading=None):
        nonlocal code_counter
        code_counter += 1
        title = heading.split('\n')[0].strip() if heading else None
        if title: 
            title = re.sub(r'<[^>]+>', '', title)
            title = re.sub(r'\*\*', '', title)
        
        imgs = code_to_images_with_title(code, md_path.stem, code_counter, title)
        
        result = []
        for i, img in enumerate(imgs):
            # ページ区切りを削除し、マージンを最小限に
            result.append(f'<div style="margin: 0.3em 0; text-align: center; background-color: #fafafa; padding: 0.5em; border: 1px solid #ddd;"><img src="images/code/{img}" alt="Code {code_counter} Part {i+1}" style="max-width: 100%; height: auto;"/></div>')
        
        placeholder = f"@@CODE_BLOCK_{code_counter}@@"
        code_placeholders[placeholder] = "".join(result)
        return placeholder

    text = re.sub(r'####\s+([^\n]+)\n+```c\s*(.*?)```', lambda m: extract_code_common(m.group(2), m.group(1)), text, flags=re.S)
    text = re.sub(r'\*\*([^\*]+)\*\*\s*[：:]*\s*\n+```c\s*(.*?)```', lambda m: extract_code_common(m.group(2), m.group(1)), text, flags=re.S)
    for keyword in ["実行結果", "出力例", "実行例"]:
        text = re.sub(rf'^({keyword}[^\n]*)$\s*\n+```c\s*(.*?)```', lambda m: extract_code_common(m.group(2), m.group(1)), text, flags=re.S | re.M)
    text = re.sub(r"```c\s*(.*?)```", lambda m: extract_code_common(m.group(1)), text, flags=re.S)

    # Mermaidもプレースホルダ化してinline_code変換から保護
    img_counter = 0
    mermaid_placeholders = {}
    def mermaid_repl(match):
        nonlocal img_counter; img_counter += 1
        img_name = f"{md_path.stem}_mermaid{img_counter}.png"
        if mermaid_to_image(match.group(1), MERMAID_DIR / img_name, img_counter):
            html_result = f'<div style="margin: 1.5em 0; page-break-inside: avoid; text-align: center; background-color: #fafafa; padding: 1em; border: 1px solid #ddd;"><img src="images/mermaid/{img_name}" alt="Diagram" style="max-width: 100%; height: auto;"/></div>'
        else:
            html_result = "<p>[図生成失敗]</p>"
        placeholder = f"@@MERMAID_BLOCK_{img_counter}@@"
        mermaid_placeholders[placeholder] = html_result
        return placeholder
    text = re.sub(r"```mermaid\s*(.*?)```", mermaid_repl, text, flags=re.S)

    # ![PDF](chapterXX.pdf) を除去
    text = re.sub(r'!\[PDF\]\([^)]+\.pdf\)', '', text)

    text = md_images_to_html(text)
    text = md_links_to_html(text)
    text = inline_code_to_html(text)
    text = emphasize_code_symbols(text)
    # プレースホルダを復元（コード画像、Mermaid画像）
    for k, v in code_placeholders.items(): text = text.replace(k, v)
    for k, v in mermaid_placeholders.items(): text = text.replace(k, v)

    # テーブル処理（簡潔かつ堅牢に）
    def table_repl(match):
        lines = match.group(0).strip().split('\n')
        if len(lines) < 3: return match.group(0)
        headers = [c.strip() for c in lines[0].split('|') if c.strip()]
        rows = []
        for line in lines[2:]:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if cells: rows.append(cells)
        html = '<table style="width: 100%; border-collapse: collapse; margin: 1.2em 0; font-size: 0.9em; page-break-inside: avoid;">\n<thead>\n<tr>\n'
        for h in headers: html += f'<th style="border: 1px solid #666; padding: 0.7em; text-align: left; background: #f5f5f5;">{h}</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'
        for i, row in enumerate(rows):
            bg = '#fafafa' if i % 2 == 1 else '#fff'
            html += '<tr>\n'
            for c in row: html += f'<td style="border: 1px solid #999; padding: 0.6em; background: {bg};">{c}</td>\n'
            html += '</tr>\n'
        html += '</tbody>\n</table>\n'
        return html
    text = re.sub(r'(?:^\|.+\|$\n?){3,}', table_repl, text, flags=re.M)

    # ---- Obsidian Callout 変換 ----
    # > [!NOTE] タイトル
    # > 本文行1
    # > 本文行2
    # → 水色/黄色/緑色の装飾ボックスに変換

    callout_styles = {
        'NOTE':      ('✏', '#e3f2fd', '#1565c0', '#bbdefb'),
        'INFO':      ('ℹ', '#e3f2fd', '#1565c0', '#bbdefb'),
        'TIP':       ('💡', '#e8f5e9', '#2e7d32', '#c8e6c9'),
        'IMPORTANT': ('⚠', '#fff8e1', '#e65100', '#ffe082'),
        'WARNING':   ('⚠', '#fff3e0', '#bf360c', '#ffcc80'),
        'CAUTION':   ('❌', '#ffebee', '#b71c1c', '#ffcdd2'),
        'SUCCESS':   ('✓', '#e8f5e9', '#2e7d32', '#c8e6c9'),
    }

    def convert_callout(text):
        lines = text.split('\n')
        result = []
        i = 0
        while i < len(lines):
            # コールアウト開始行を探す: > [!TYPE] タイトル
            m = re.match(r'^>\s*\[!(NOTE|INFO|TIP|IMPORTANT|WARNING|CAUTION|SUCCESS)\]\s*(.*)', lines[i], re.I)
            if m:
                ctype = m.group(1).upper()
                ctitle = m.group(2).strip()
                icon, bg, border_color, header_bg = callout_styles.get(ctype, ('ℹ', '#e3f2fd', '#1565c0', '#bbdefb'))
                # 本文行を収集（> で始まる連続行）
                body_lines = []
                i += 1
                while i < len(lines) and re.match(r'^>\s?', lines[i]):
                    body_line = re.sub(r'^>\s?', '', lines[i]).strip()
                    if body_line:
                        body_lines.append(body_line)
                    i += 1
                # タイトルがない場合はctype自体をタイトルにする
                display_title = ctitle if ctitle else ctype.capitalize()
                body_html = ' '.join(body_lines)
                # HTMLを生成
                html = (
                    f'<div style="background-color:{bg}; border-left:4px solid {border_color}; '
                    f'border-radius:4px; margin:1.2em 0; padding:0.8em 1em; page-break-inside:avoid;">'
                    f'<div style="color:{border_color}; font-weight:bold; margin-bottom:0.4em;">'
                    f'{icon} {display_title}</div>'
                    f'<div style="color:#333; line-height:1.8;">{body_html}</div>'
                    f'</div>'
                )
                result.append(html)
            elif re.match(r'^>\s?', lines[i]):
                # コールアウト以外の > 行（通常blockquoteや孤立した >）
                # 連続する > 行をまとめてHTMLのblockquoteに変換
                bq_lines = []
                while i < len(lines) and re.match(r'^>\s?', lines[i]):
                    bq_line = re.sub(r'^>\s?', '', lines[i]).strip()
                    if bq_line:
                        bq_lines.append(bq_line)
                    i += 1
                if bq_lines:
                    bq_html = (
                        '<blockquote style="border-left:3px solid #ccc; '
                        'margin:0.8em 0 0.8em 1em; padding:0.4em 1em; '
                        'color:#555; font-style:italic;">'
                        + ' '.join(bq_lines)
                        + '</blockquote>'
                    )
                    result.append(bq_html)
            else:
                result.append(lines[i])
                i += 1
        return '\n'.join(result)

    text = convert_callout(text)

    # 装飾

    text = re.sub(r'【重要】', r'<b style="background-color: #fff9c4; padding: 0.2em 0.5em; border-left: 3px solid #ffa726;">【重要】</b>', text)
    text = re.sub(r'【注意】', r'<b style="background-color: #ffcdd2; padding: 0.2em 0.5em; border-left: 3px solid #ef5350;">【注意】</b>', text)
    text = re.sub(r'【ポイント】', r'<b style="background-color: #e1f5fe; padding: 0.2em 0.5em; border-left: 3px solid #42a5f5;">【ポイント】</b>', text)
    text = re.sub(r'❌', r'<span style="color: #ef5350; font-weight: bold;">✕</span>', text)
    text = re.sub(r'✅', r'<span style="color: #66bb6a; font-weight: bold;">✓</span>', text)
    text = re.sub(r'[⚠⚠️]', r'<span style="color: #ffa726; font-weight: bold;">⚠</span>', text)
    text = re.sub(r'\[[xX]\]', r'<span style="color: #66bb6a; font-weight: bold;">✓</span>', text)
    text = re.sub(r'\[ \]', r'<span style="border: 1px solid #666; width: 1em; display: inline-block;">&nbsp;</span>', text)
    
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)

    # 見出し（Kindle用にスタイル強化）
    text = re.sub(r"^# (.+)$", lambda m: f'<h1 id="chapter-{md_path.stem}" style="font-size: 2em; margin: 2em 0 1.2em 0; font-weight: bold; line-height: 1.4; background-color: #e0e0e0; padding: 0.5em 0.8em; border-bottom: 4px solid #333; page-break-before: always;">{m.group(1)}</h1>', text, flags=re.M)
    text = re.sub(r"^## (.+)$", r'<h2 style="font-size: 1.5em; margin: 2em 0 1em 0; font-weight: bold; background-color: #e3f2fd; padding: 0.6em 0.8em; border-left: 5px solid #1976d2;">\1</h2>', text, flags=re.M)
    text = re.sub(r"^### (.+)$", r'<h3 style="font-size: 1.3em; margin: 1.5em 0 0.8em 0; font-weight: bold; background-color: #e8f5e9; padding: 0.5em 0.7em; border-left: 4px solid #388e3c;">\1</h3>', text, flags=re.M)
    text = re.sub(r"^#### (.+)$", r'<h4 style="font-size: 1.15em; margin: 1.2em 0 0.6em 0; font-weight: bold; background-color: #fff3e0; padding: 0.4em 0.6em; border-left: 3px solid #ff9800;">\1</h4>', text, flags=re.M)
    text = re.sub(r"^##### (.+)$", r'<h5 style="font-size: 1.05em; margin: 1em 0 0.5em 0; font-weight: bold;">\1</h5>', text, flags=re.M)
    text = re.sub(r"^###### (.+)$", r'<h6 style="font-size: 1em; margin: 0.8em 0 0.4em 0; font-weight: bold;">\1</h6>', text, flags=re.M)

    # リストと段落
    text = re.sub(r"^[\-\*]\s+(.+)$", r"<li>\1</li>", text, flags=re.M)
    text = re.sub(r"(<li>.*?</li>\n?)+", lambda m: f"<ul style='margin: 1.2em 0; padding-left: 2em; line-height: 1.9;'>\n{m.group(0)}</ul>\n", text, flags=re.S)

    lines = []
    for line in text.splitlines():
        if line.strip() and not line.strip().startswith("<"): lines.append(f"<p>{line}</p>")
        else: lines.append(line)
    html_content = "\n".join(lines)

    # 章ごとのPDF画像をH1タグの直後に挿入
    if chapter_index in chapter_pdf_images:
        pdf_html = '<div style="margin: 2em 0; page-break-inside: avoid;">\n'
        for pdf_img_path in chapter_pdf_images[chapter_index]:
            pdf_html += f'<div style="margin: 0.5em 0; text-align: center;"><img src="{pdf_img_path}" alt="Slide" style="max-width: 100%; height: auto; border: 1px solid #ddd;"/></div>\n'
        pdf_html += '</div>\n'
        h1_pattern = r'(<h1[^>]*>.*?</h1>)'
        html_content = re.sub(h1_pattern, r'\1\n' + pdf_html, html_content, count=1)

    return html_content, chapter_title

# ========= メイン =========
def main():
    print("EPUB生成開始...")
    CHAPTER_DIR.mkdir(exist_ok=True)
    md_files = sorted(CHAPTER_DIR.glob("*.md"))
    if not md_files:
        (CHAPTER_DIR / "01_test.md").write_text("# テスト\n```c\n#include <stdio.h>\n// コメント\nint main(){}\n```", encoding="utf-8")
        md_files = sorted(CHAPTER_DIR.glob("*.md"))

    body = []
    chapters = []
    for chapter_index, md in enumerate(md_files):
        try:
            html, title = process_md(md, chapter_index)
            body.append(html)
            chapters.append({'id': md.stem, 'title': title})
        except Exception as e:
            print(f"[ERROR] {md.name} 処理中にエラー: {e}")
            import traceback
            traceback.print_exc()

    toc = ""
    if cover_dest: toc += f'<div style="text-align:center; page-break-after:always;"><img src="images/{cover_dest.name}" /></div>'
    toc += '<div style="page-break-before:always; page-break-after:always;"><h2>目次</h2>'
    for i, c in enumerate(chapters, 1): toc += f'<p><a href="#chapter-{c["id"]}">{i}. {c["title"]}</a></p>'
    toc += '</div>'

    BOOK_HTML.write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Book</title>
<style>
body{{font-family:"Hiragino Mincho ProN",serif; line-height:1.8; margin:0; padding:1em; text-align:justify; color:#111;}} 
img{{max-width:100%; height:auto;}}
</style>
</head><body>{toc}{''.join(body)}</body></html>""", encoding="utf-8")

    print(f"[HTML] {BOOK_HTML} 生成完了")

    # EPUB生成オプション（Kindle向け最適化設定 - h1のみを章として認識）
    epub_options = [
        "ebook-convert", str(BOOK_HTML), str(BOOK_EPUB),
        "--language", "ja", 
        "--epub-version", "2",
        "--chapter", "//*[name()='h1']",  # h1のみを章として認識
        "--level1-toc", "//h:h1",
        "--chapter-mark", "pagebreak",
        "--disable-font-rescaling",
        "--margin-top", "0", "--margin-bottom", "0",
        "--margin-left", "0", "--margin-right", "0",
        "--pretty-print"
    ]
    if cover_dest:
        epub_options.extend(["--cover", str(cover_dest)])

    try:
        print("[EPUB変換開始...]")
        result = subprocess.run(epub_options, capture_output=True)
        if result.returncode == 0:
            print("[OK] EPUB完了:", BOOK_EPUB)
        else:
            stderr = result.stderr.decode('utf-8', errors='replace')
            print(f"[ERROR] EPUB変換失敗: {stderr}")
            return
        
        # Kindle(MOBI)変換
        if Path(BOOK_EPUB).exists():
            print("[MOBI変換開始...]")
            result2 = subprocess.run([
                "ebook-convert", str(BOOK_EPUB), str(BOOK_MOBI),
                "--output-profile", "kindle",
                "--mobi-file-type", "both"
            ], capture_output=True)
            if result2.returncode == 0:
                print("[OK] MOBI完了:", BOOK_MOBI)
            else:
                stderr2 = result2.stderr.decode('utf-8', errors='replace')
                print(f"[ERROR] MOBI変換失敗: {stderr2}")

        # PDF変換
        if Path(BOOK_EPUB).exists():
            print("[PDF変換開始...]")
            book_pdf = DIST_DIR / "book.pdf"
            result3 = subprocess.run([
                "ebook-convert", str(BOOK_EPUB), str(book_pdf),
                "--pdf-page-numbers",
                "--paper-size", "a5",
                "--pdf-default-font-size", "12",
                "--pdf-mono-font-size", "12"
            ], capture_output=True)
            if result3.returncode == 0:
                print("[OK] PDF完了:", book_pdf)
            else:
                stderr3 = result3.stderr.decode('utf-8', errors='replace')
                print(f"[ERROR] PDF変換失敗: {stderr3}")
    except Exception as e:
        print(f"[ERROR] 変換失敗: {e}")
        print("Calibreがインストールされているか確認してください。")

if __name__ == "__main__":
    main()