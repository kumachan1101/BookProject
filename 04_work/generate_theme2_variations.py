import imgkit
from pygments import highlight
from pygments.lexers import CLexer
from pygments.formatters import HtmlFormatter
from pathlib import Path

IMGKIT_OPTIONS = {
    "format": "png",
    "encoding": "UTF-8",
    "quiet": "",
    "width": "1400",
    "minimum-font-size": "1",
    "quality": "95",
    "disable-smart-width": "",
}

sample_code = """#include <stdio.h>
#include "data_sorter.h"

// 抽象モジュールの戦略を利用
static int ascending_compare_impl(const void* a, const void* b) {
    const int val_a = *(const int*)a; // Aの値を取得
    const int val_b = *(const int*)b;
    if (val_a < val_b) return -1;
    if (val_a > val_b) return 1;
    return 0; // 成功
}

int main(void) {
    printf("ソート処理の開始\\n");
    return 0;
}
"""

themes = [
    {
        "name": "【2-A】元々のTheme 2",
        "title_bg": "#1E293B",
        "title_color": "#F8FAFC",
        "title_border": "#3B82F6",
        "bg": "#0F172A",
        "text": "#E2E8F0",      # 変数・一般テキスト: 明るいグレー
        "comment": "#94A3B8",   # コメント: 中間グレー (似ている)
        "prefix": "#C4B5FD",
        "string": "#A3E635",
        "keyword": "#38BDF8",
        "type": "#818CF8",
        "number": "#FBBF24",
        "function": "#A78BFA",
    },
    {
        "name": "【2-B】コメントを緑/暗めに",
        "title_bg": "#1E293B",
        "title_color": "#F8FAFC",
        "title_border": "#3B82F6",
        "bg": "#0F172A",
        "text": "#E2E8F0",      # 変数: そのまま
        "comment": "#4ADE80",   # コメント: グリーン系 (VS Code風)
        "prefix": "#C4B5FD",
        "string": "#FDE047",    # 文字列を緑から黄色に変更（コメントと被らないように）
        "keyword": "#38BDF8",
        "type": "#818CF8",
        "number": "#FBBF24",
        "function": "#A78BFA",
    },
    {
        "name": "【2-C】変数を白く、コメントを青暗く",
        "title_bg": "#1E293B",
        "title_color": "#F8FAFC",
        "title_border": "#3B82F6",
        "bg": "#0F172A",
        "text": "#FFFFFF",      # 変数: 純白
        "comment": "#64748B",   # コメント: もっと暗いスレートブルー
        "prefix": "#C4B5FD",
        "string": "#A3E635",
        "keyword": "#38BDF8",
        "type": "#818CF8",
        "number": "#FBBF24",
        "function": "#A78BFA",
    },
    {
        "name": "【2-D】コメントを落ち着いた茶色/オレンジに",
        "title_bg": "#1E293B",
        "title_color": "#F8FAFC",
        "title_border": "#3B82F6",
        "bg": "#0F172A",
        "text": "#F1F5F9",      # 変数: 少し明るく
        "comment": "#D97757",   # コメント: 落ち着いたテラコッタ（赤茶）
        "prefix": "#C4B5FD",
        "string": "#A3E635",
        "keyword": "#38BDF8",
        "type": "#818CF8",
        "number": "#FBBF24",
        "function": "#A78BFA",
    },
]

def generate_sample(theme, index):
    css = f'''
    <style>
    body {{ margin: 0; padding: 0; background: {theme["bg"]}; width: 1400px !important; box-sizing: border-box; overflow: hidden; }}
    .highlight {{ background: {theme["bg"]} !important; font-size: 38px !important; line-height: 1.85 !important; font-family: 'JetBrains Mono', monospace !important; font-weight: 500 !important; padding: 0 40px !important; }}
    .highlight pre {{ background: {theme["bg"]} !important; color: {theme["text"]} !important; padding: 10px 0 !important; margin: 0 !important; font-size: 38px !important; line-height: 1.85 !important; font-weight: 500 !important; white-space: pre-wrap; word-break: break-all; overflow-wrap: break-word; word-wrap: break-word; }}
    .highlight .c1, .highlight .cm, .highlight .c, .highlight .cp {{ color: {theme["comment"]} !important; font-weight: 600 !important; font-style: italic !important; }}
    .highlight .cp {{ color: {theme["prefix"]} !important; font-weight: bold !important; font-style: normal !important; }}
    .highlight .cpf, .highlight .s, .highlight .s1, .highlight .s2 {{ color: {theme["string"]} !important; font-weight: 600 !important; }}
    .highlight .k, .highlight .kn, .highlight .kr, .highlight .kd {{ color: {theme["keyword"]} !important; font-weight: bold !important; }}
    .highlight .kt, .highlight .nc {{ color: {theme["type"]} !important; font-weight: 600 !important; }}
    .highlight .mi, .highlight .mf, .highlight .mh {{ color: {theme["number"]} !important; font-weight: 600 !important; }}
    .highlight .nf, .highlight .nb {{ color: {theme["function"]} !important; font-weight: bold !important; }}
    .highlight .n, .highlight .p, .highlight .o {{ color: {theme["text"]} !important; }}
    .highlight .go {{ color: {theme["text"]} !important; opacity: 0.8 !important; font-weight: 600 !important; }}
    </style>
    '''
    
    formatter = HtmlFormatter(full=False, linenos=False, noclasses=False)
    # Using CLexer
    full_highlighted = highlight(sample_code, CLexer(), formatter)
    
    import re
    pre_match = re.search(r'<pre[^>]*>(.*?)</pre>', full_highlighted, re.DOTALL)
    chunk_html = pre_match.group(1) if pre_match else full_highlighted
    
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8">{css}</head>
<body style="width: 1400px; margin: 0; padding: 0;">
<div style="background: {theme["title_bg"]}; color: {theme["title_color"]}; padding: 25px 40px; font-family: 'JetBrains Mono', monospace; font-size: 34px; font-weight: 800; border-bottom: 2px solid {theme["title_border"]}; margin-bottom: 0; width: 1400px; box-sizing: border-box; display: block;">
sample_code.c ({theme["name"]})
</div>
<div class="highlight" style="width: 1400px; box-sizing: border-box; display: block;">
<pre style="width: 1400px; box-sizing: border-box; display: block; margin: 0;">{chunk_html}</pre>
</div>
</body>
</html>"""
    
    out_path = Path(f"sample_theme2_variant_{index}.png")
    imgkit.from_string(html, str(out_path), options=IMGKIT_OPTIONS)

if __name__ == "__main__":
    for i, theme in enumerate(themes, 1):
        generate_sample(theme, i)
        print(f"Generated sample_theme2_variant_{i}.png")
