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
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

CHAPTER_DIR = PROJECT_ROOT / "02_章別"
DIST_DIR = SCRIPT_DIR / "dist"  # 05_生成/dist に変更
IMG_DIR = DIST_DIR / "images"
MERMAID_DIR = IMG_DIR / "mermaid"
CODE_IMG_DIR = IMG_DIR / "code"
PDF_IMG_DIR = IMG_DIR / "pdf"

# PDF資料のパス
RESOURCE_PDF_DIR = PROJECT_ROOT / "03_資料"
RESOURCE_PDF_NAME = "C_Language_Architectural_Design_Patterns.pdf"

BOOK_HTML = DIST_DIR / "book.html"
BOOK_EPUB = DIST_DIR / "book.epub"
BOOK_MOBI = DIST_DIR / "book.mobi"

COVER_IMAGE = Path("cover.png")

# Kindle互換性設定
MAX_IMAGE_WIDTH = 1400
MAX_IMAGE_HEIGHT = 1600
MAX_LINES_PER_IMAGE = 50  # 非推奨: 代わりにTARGET_CODE_IMAGE_HEIGHTを使用
TARGET_CODE_IMAGE_HEIGHT = 1400  # コード画像の目標高さ(余裕を持たせる)
LINE_HEIGHT_PX = 55  # 1行あたりの推定高さ(line-height 1.45 * font-size 38px)

# Mermaidパス
MMDC = r"C:\Users\kumac\AppData\Roaming\npm\mmdc.cmd"

IMGKIT_OPTIONS = {
    "format": "png",
    "encoding": "UTF-8",
    "quiet": "",
    "width": str(MAX_IMAGE_WIDTH),
    "minimum-font-size": "1",  # フォントサイズ縮小を防止
    "quality": "95",
    "disable-smart-width": "",
}

# コードブロック用CSS（ファイル名見出し付き）
CODE_CSS = """
<style>
body { margin: 0; padding: 0; background: #1a1a1a; width: 1400px; min-width: 1400px; box-sizing: border-box; }

.highlight {
  background: #1a1a1a !important;
  font-size: 38px !important;
  line-height: 1.45 !important;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
  font-weight: 600 !important;
  width: 100%;
  box-sizing: border-box;
}

.highlight pre {
  background: #1a1a1a !important;
  color: #f8f8f2 !important;
  padding: 35px !important;
  margin: 0 !important;
  font-size: 38px !important;
  line-height: 1.45 !important;
  font-weight: 600 !important;
  border: 2px solid #44475a;
  width: 100%;
  box-sizing: border-box;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.highlight .c1, .highlight .cm, .highlight .c {
  color: #6272a4 !important;
  font-weight: normal !important;
  font-style: italic !important;
}

.highlight .cp { 
  color: #ff79c6 !important; 
  font-weight: 700 !important; 
}

.highlight .cpf { 
  color: #8be9fd !important; 
  font-weight: 700 !important; 
}

.highlight .k, .highlight .kt { color: #ff79c6 !important; font-weight: 700 !important; }
.highlight .nf, .highlight .nb { color: #50fa7b !important; font-weight: 700 !important; }
.highlight .s, .highlight .s1, .highlight .s2 { color: #f1fa8c !important; font-weight: 600 !important; }
.highlight .n { color: #f8f8f2 !important; }
.highlight .o { color: #ff79c6 !important; font-weight: 700 !important; }
.highlight .mi, .highlight .mf { color: #bd93f9 !important; font-weight: 700 !important; }
</style>
"""

# ========= 初期化 =========
print("ディレクトリ初期化...")
if DIST_DIR.exists():
    shutil.rmtree(DIST_DIR)
DIST_DIR.mkdir(parents=True)
IMG_DIR.mkdir(parents=True)
MERMAID_DIR.mkdir(parents=True)
CODE_IMG_DIR.mkdir(parents=True)
PDF_IMG_DIR.mkdir(parents=True)

def optimize_image(img_path: Path):
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


# ========= PDF処理（1ページずつ各章に配分） =========
def split_pdf_by_pages(pdf_path: Path) -> dict:
    """PDFを各章に1ページずつ配分"""
    if not pdf_path.exists():
        print(f"[WARN] PDFが見つかりません: {pdf_path}")
        return {}
    
    print(f"[PDF] {pdf_path.name} を各章に配分中...")
    chapter_images = {}  # {chapter_index: [image_paths]}
    
    try:
        import fitz  # PyMuPDF
        print("[PDF] PyMuPDF (fitz)を使用します...")
        
        doc = fitz.open(str(pdf_path))
        total_pages = len(doc)
        print(f"[PDF] 総ページ数: {total_pages}")
        
        # 各ページを各章に1ページずつ配分
        for page_num in range(total_pages):
            chapter_index = page_num  # ページ0→章0, ページ1→章1, ...
            
            if chapter_index not in chapter_images:
                chapter_images[chapter_index] = []
            
            page = doc[page_num]
            zoom = 150 / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            output_path = PDF_IMG_DIR / f"chapter{chapter_index:02d}_page01.png"
            pix.save(str(output_path))
            optimize_image(output_path)
            chapter_images[chapter_index].append(f"images/pdf/{output_path.name}")
            print(f"  -> 章{chapter_index} にページ{page_num + 1}を配分")
        
        doc.close()
        print(f"[PDF] {len(chapter_images)}章に配分しました")
        return chapter_images
        
    except ImportError:
        print("[ERROR] PyMuPDFがインストールされていません")
        print("pip install PyMuPDF を実行してください")
    except Exception as e:
        print(f"[ERROR] PDF分割失敗: {e}")
    
    return {}


# PDFを各章に配分
resource_pdf_path = RESOURCE_PDF_DIR / RESOURCE_PDF_NAME
chapter_pdf_images = split_pdf_by_pages(resource_pdf_path)


# ========= Mermaid =========
def sanitize_mermaid(code: str) -> str:
    """Mermaidコードをクリーンアップ"""
    lines = code.splitlines()
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # コメント行を除外
        if stripped.startswith('%%'):
            continue
        cleaned_lines.append(stripped)
    
    code = "\n".join(cleaned_lines)
    code = code.replace('　', '  ')
    
    # LR -> TB 変換
    code = re.sub(r'graph\s+LR\b', 'graph TB', code, flags=re.I)
    code = re.sub(r'flowchart\s+LR\b', 'flowchart TB', code, flags=re.I)
    
    return code.strip()

def mermaid_to_image(code: str, out_png: Path, img_index: int) -> bool:
    """Mermaid図を画像化（エラーハンドリング強化版）"""
    cleaned_code = sanitize_mermaid(code)
    
    # 空のコードをチェック
    if not cleaned_code or len(cleaned_code) < 10:
        print(f"[WARN] Mermaid {img_index}: コードが空または短すぎます")
        return False
    
    tmp_mmd = out_png.parent / f"temp_diag_{img_index}.mmd"
    
    try:
        with open(tmp_mmd, "w", encoding="utf-8", newline="\n") as f:
            f.write(cleaned_code)
        
        cmd = [
            MMDC, "-i", str(tmp_mmd), "-o", str(out_png),
            "--backgroundColor", "white", 
            "--scale", "3",
            "--width", "1400",
            "--height", "1600"
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=30)
        
        if res.returncode != 0:
            print(f"[ERROR] Mermaid {img_index} 失敗:")
            print(f"  stderr: {res.stderr[:200]}")
            print(f"  コード先頭: {cleaned_code[:100]}")
            return False
        
        if not out_png.exists() or out_png.stat().st_size < 100:
            print(f"[ERROR] Mermaid {img_index}: 出力ファイルが生成されませんでした")
            return False
        
        print(f"  -> Mermaid画像 {img_index} 作成成功")
        optimize_image(out_png)
        return True
        
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Mermaid {img_index}: タイムアウト")
        return False
    except Exception as e:
        print(f"[ERROR] Mermaid {img_index} 例外: {e}")
        return False
    finally:
        if tmp_mmd.exists():
            tmp_mmd.unlink()


# ========= コードブロック画像化（####ファイル名対応） =========
def code_to_images_with_title(code: str, md_stem: str, code_index: int, title: str = None) -> list:
    """コードを画像化（ファイル名見出し付き）"""
    lines = code.splitlines()
    images = []
    
    print(f"  コード全体: {len(lines)}行, タイトル: {title}")
    
    formatter = HtmlFormatter(full=False, style="dracula", linenos=False, noclasses=True)
    full_highlighted = highlight(code, CLexer(), formatter)
    
    pre_match = re.search(r'<pre[^>]*>(.*?)</pre>', full_highlighted, re.DOTALL)
    if not pre_match:
        return []
    
    highlighted_lines = pre_match.group(1).split('\n')
    start_line = 0
    part_num = 0
    
    while start_line < len(highlighted_lines):
        # タイトル部分の高さを考慮して動的に行数を計算
        title_height = 120 if (title and part_num == 0) else 0
        available_height = TARGET_CODE_IMAGE_HEIGHT - title_height - 100  # パディング分を引く
        max_lines_for_chunk = max(10, int(available_height / LINE_HEIGHT_PX))  # 最低10行は確保
        
        remaining = len(highlighted_lines) - start_line
        chunk_size = min(remaining, max_lines_for_chunk)
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
        # ####ファイル名を画像の最上部に埋め込む
        if title and part_num == 0:
            html += f"""<div style="background: #FFFFFF; color: #000000; padding: 25px 40px; 
            font-family: 'Consolas', 'Monaco', monospace; font-size: 34px; 
            font-weight: 800; border-bottom: 4px solid #6272a4; margin-bottom: 0;">
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
        r"<code style='font-family: monospace; font-weight: 600; background-color: #fff8e1; padding: 0.1em 0.3em; border: 1px solid #ffe082;'>\1</code>",
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
def process_md(md_path: Path, chapter_index: int):
    """Markdownファイルを処理（章ごとのPDF画像挿入対応）"""
    print(f"\n[MD] {md_path.name} (章{chapter_index})")
    text = md_path.read_text(encoding="utf-8")
    
    # 段落間空行処理は削除(テーブル変換を壊すため)
    
    # ファイル名から安全なIDを生成（バッククォートなどを除去）
    safe_stem = re.sub(r'[\\/:*?"<>|`]', '_', md_path.stem)
    
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
        
        # safe_stem を使用
        imgs = code_to_images_with_title(code, safe_stem, code_counter, title)
        
        result = []
        for i, img in enumerate(imgs):
            result.append(f'<div style="margin: 1.2em 0; text-align: center; background-color: #fafafa; padding: 0.5em; border: 1px solid #ddd;"><img src="images/code/{img}" alt="Code {code_counter} Part {i+1}" style="max-width: 100%; height: auto;"/></div>')
        
        placeholder = f"@@CODE_BLOCK_{code_counter}@@"
        code_placeholders[placeholder] = "".join(result)
        return placeholder

    # ####ファイル名 + ```c のパターンを優先的に処理
    text = re.sub(r'####\s+([^\n]+)\n+```c\s*(.*?)```', lambda m: extract_code_common(m.group(2), m.group(1)), text, flags=re.S)
    text = re.sub(r'\*\*([^\*]+)\*\*\s*[：:]*\s*\n+```c\s*(.*?)```', lambda m: extract_code_common(m.group(2), m.group(1)), text, flags=re.S)
    for keyword in ["実行結果", "出力例", "実行例"]:
        text = re.sub(rf'^({keyword}[^\n]*)$\s*\n+```c\s*(.*?)```', lambda m: extract_code_common(m.group(2), m.group(1)), text, flags=re.S | re.M)
    text = re.sub(r"```c\s*(.*?)```", lambda m: extract_code_common(m.group(1)), text, flags=re.S)

    # Mermaid処理
    img_counter = 0
    def mermaid_repl(match):
        nonlocal img_counter; img_counter += 1
        # safe_stem を使用
        img_name = f"{safe_stem}_mermaid{img_counter}.png"
        if mermaid_to_image(match.group(1), MERMAID_DIR / img_name, img_counter):
            return f'<div style="margin: 1.2em 0; page-break-inside: avoid; text-align: center; background-color: #fafafa; padding: 1em; border: 1px solid #ddd;"><img src="images/mermaid/{img_name}" alt="Diagram" style="max-width: 100%; height: auto;"/></div>'
        return "<p>[図生成失敗]</p>"
    text = re.sub(r"```mermaid\s*(.*?)```", mermaid_repl, text, flags=re.S)

    text = md_images_to_html(text)
    text = md_links_to_html(text)
    text = inline_code_to_html(text)
    text = emphasize_code_symbols(text)
    for k, v in code_placeholders.items(): text = text.replace(k, v)

    # テーブル処理(Kindle互換性向上)
    def table_repl(match):
        lines = match.group(0).strip().split('\n')
        if len(lines) < 3: return match.group(0)
        headers = [c.strip() for c in lines[0].split('|') if c.strip()]
        rows = []
        for line in lines[2:]:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if cells: rows.append(cells)
        
        # Kindle互換性のためにシンプルなスタイルを使用
        html = '<table style="width: 100%; border-collapse: collapse; margin: 1.2em 0; font-size: 0.85em;">\n<thead>\n<tr>\n'
        for h in headers: 
            html += f'<th style="border: 2px solid #333; padding: 0.8em; text-align: left; background-color: #e0e0e0; font-weight: bold;">{h}</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'
        for i, row in enumerate(rows):
            bg = '#f5f5f5' if i % 2 == 1 else '#ffffff'
            html += '<tr>\n'
            for c in row: 
                html += f'<td style="border: 1px solid #666; padding: 0.7em; background-color: {bg};">{c}</td>\n'
            html += '</tr>\n'
        html += '</tbody>\n</table>\n'
        return html
    text = re.sub(r'(?:^\|.+\|$\n?){3,}', table_repl, text, flags=re.M)

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

    # 見出し (マージンを縮小して行間を詰める、配色の刷新)
    text = re.sub(r"^# (.+)$", lambda m: f'<h1 id="chapter-{md_path.stem}" style="font-size: 2em; margin: 1.2em 0 1em 0; font-weight: bold; line-height: 1.3; background-color: #f0f0f0; padding: 0.5em 0.8em; border-bottom: 4px solid #444; page-break-before: always;">{m.group(1)}</h1>', text, flags=re.M)
    text = re.sub(r"^## (.+)$", r'<h2 style="font-size: 1.5em; margin: 1.2em 0 0.6em 0; font-weight: bold; background-color: #e8eaf6; padding: 0.5em 0.8em; border-left: 5px solid #3f51b5;">\1</h2>', text, flags=re.M)
    text = re.sub(r"^### (.+)$", r'<h3 style="font-size: 1.3em; margin: 1.0em 0 0.5em 0; font-weight: bold; background-color: #f3e5f5; padding: 0.4em 0.7em; border-left: 4px solid #8e24aa;">\1</h3>', text, flags=re.M)
    text = re.sub(r"^#### (.+)$", r'<h4 style="font-size: 1.15em; margin: 0.8em 0 0.4em 0; font-weight: bold; background-color: #ffebee; padding: 0.3em 0.6em; border-left: 3px solid #e53935;">\1</h4>', text, flags=re.M)
    text = re.sub(r"^##### (.+)$", r'<h5 style="font-size: 1.05em; margin: 0.6em 0 0.3em 0; font-weight: bold;">\1</h5>', text, flags=re.M)
    text = re.sub(r"^###### (.+)$", r'<h6 style="font-size: 1em; margin: 0.5em 0 0.2em 0; font-weight: bold;">\1</h6>', text, flags=re.M)

    # リストと段落 (インラインスタイル除去しCSSに委譲)
    text = re.sub(r"^[\-\*] (.+)$", r"<li>\1</li>", text, flags=re.M)
    text = re.sub(r"(<li>.*?</li>\n?)+", lambda m: f"<ul>\n{m.group(0)}</ul>\n", text, flags=re.S)

    # 引用 (blockquote) 処理
    lines_q = []
    in_quote = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("> "):
            if not in_quote:
                lines_q.append("<blockquote>")
                in_quote = True
            lines_q.append(f"<p>{stripped[2:]}</p>")
        else:
            if in_quote:
                lines_q.append("</blockquote>")
                in_quote = False
            lines_q.append(line)
    if in_quote: lines_q.append("</blockquote>")
    text = "\n".join(lines_q)

    # 段落処理: 空行を<br/>に変換し、非HTMLタグ行を<p>で囲む
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        # 空行の場合は無視(pタグのマージンで十分)
        if not stripped:
            continue
        # HTMLタグで始まる行はそのまま
        elif stripped.startswith("<"):
            lines.append(line)
        # それ以外は<p>で囲む
        else:
            lines.append(f"<p>{line}</p>")
    
    html_content = "\n".join(lines)
    
    # 章ごとのPDF画像を挿入 (章の直後、H1タグのすぐ後ろ)
    if chapter_index in chapter_pdf_images:
        pdf_html = '<div style="margin: 2em 0; page-break-after: always;">\n'
        # 「参考資料」という項目名は不要とのことで削除
        # pdf_html += '<h2 style="... >参考資料</h2>\n'
        for pdf_img_path in chapter_pdf_images[chapter_index]:
            pdf_html += f'<div style="margin: 0.5em 0; text-align: center;"><img src="{pdf_img_path}" alt="Reference Material" style="max-width: 100%; height: auto;"/></div>\n'
        pdf_html += '</div>\n'
        
        # h1タグの直後にPDF画像を挿入
        h1_pattern = r'(<h1[^>]*>.*?</h1>)'
        html_content = re.sub(h1_pattern, r'\1' + pdf_html, html_content, count=1)
    
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
body{{font-family:"Hiragino Mincho ProN",serif; line-height:1.6; margin:0; padding:0.5em; text-align:justify; color:#111;}} 
p{{margin: 0.5em 0; text-indent: 1em;}}
h1{{margin: 1.5em 0 1em 0; line-height: 1.3;}}
h2{{margin: 1.5em 0 0.8em 0; line-height: 1.3;}}
h3, h4, h5, h6 {{margin: 1.2em 0 0.6em 0; line-height: 1.3;}}
ul, ol {{margin: 1.0em 0; padding-left: 2em;}}
li {{margin: 0.4em 0;}}
img{{max-width:100%; height:auto;}}
blockquote {{margin: 1.2em 0; padding: 0.8em 1.2em; border-left: 5px solid #ccc; background-color: #f9f9f9; color: #555; font-style: italic;}}
</style>
</head><body>{toc}{''.join(body)}</body></html>""", encoding="utf-8")

    print(f"[HTML] {BOOK_HTML} 生成完了")

    # EPUB生成
    epub_options = [
        "ebook-convert", str(BOOK_HTML), str(BOOK_EPUB),
        "--language", "ja", 
        "--epub-version", "2",
        "--chapter", "//*[name()='h1']",
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
        subprocess.run(epub_options, check=True)
        print(f"✓ EPUB完了: {BOOK_EPUB}")
        
        # MOBI変換
        if Path(BOOK_EPUB).exists():
            print("[MOBI変換開始...]")
            subprocess.run(["ebook-convert", str(BOOK_EPUB), str(BOOK_MOBI), 
                            "--output-profile", "kindle", 
                            "--mobi-file-type", "both"], check=True)
            print(f"✓ MOBI完了: {BOOK_MOBI}")
            
            # PDF変換
            print("[PDF変換開始...]")
            book_pdf = DIST_DIR / "book.pdf"
            subprocess.run(["ebook-convert", str(BOOK_EPUB), str(book_pdf),
                            "--pdf-page-numbers",
                            "--paper-size", "a5",
                            "--pdf-default-font-size", "12",
                            "--pdf-mono-font-size", "12"], check=True)
            print(f"✓ PDF完了: {book_pdf}")
    except Exception as e:
        print(f"[ERROR] 変換失敗: {e}")
        print("※Calibreがインストールされているか確認してください。")

if __name__ == "__main__":
    main()