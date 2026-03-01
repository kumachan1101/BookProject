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

# The code from the user's screenshot that wraps awkwardly
sample_code = """#include <stdio.h>
#include <string.h>
// 選択ロジックと計算ロジックの2つの責任が混在

int compress_data(const char* data, int size, char* output, int output_size) {
    // 責任1: 選択基準の決定(ポリシー担当の領域)
    if (size < 1024) {
        // 責任2: LZ4の具体的な計算処理(圧縮担当の領域)
        printf("Executing LZ4 compression for size %d\\n", size);
        
        // LZ4固有の処理...
        int compressed_size = size / 2; // 簡略化
        memcpy(output, data, compressed_size);
        
        return compressed_size;
    } else {
        // 責任2: Gzipの具体的な計算処理(圧縮担当の領域)
        printf("Executing Gzip compression for size %d\\n", size);
        
        // Gzip固有の処理...
        int compressed_size = size / 3; // 簡略化
    }
}
"""

# Theme 2C (White Variables / Blue-Gray Comments)
theme = {
    "name": "Theme 2C Base",
    "title_bg": "#1E293B",
    "title_color": "#F8FAFC",
    "title_border": "#3B82F6",
    "bg": "#0F172A",
    "text": "#FFFFFF",
    "comment": "#64748B",
    "prefix": "#C4B5FD",
    "string": "#A3E635",
    "keyword": "#38BDF8",
    "type": "#818CF8",
    "number": "#FBBF24",
    "function": "#A78BFA",
}

configurations = [
    {
        "id": "F",
        "name": "【F】フォント32px + 文字間隔-0.5px + 行間1.6",
        "font_size": "32px",
        "letter_spacing": "-0.5px",
        "line_height": "1.6"
    },
    {
        "id": "G",
        "name": "【G】フォント32px + 文字間隔-1.0px + 行間1.5",
        "font_size": "32px",
        "letter_spacing": "-1.0px",
        "line_height": "1.5"
    },
    {
        "id": "H",
        "name": "【H】フォント30px + 文字間隔-0.5px + 行間1.4",
        "font_size": "30px",
        "letter_spacing": "-0.5px",
        "line_height": "1.4"
    },
    {
        "id": "I",
        "name": "【I】限界圧縮: フォント28px + 文字間隔-0.5px + 行間1.4",
        "font_size": "28px",
        "letter_spacing": "-0.5px",
        "line_height": "1.4"
    }
]

def generate_sample(config):
    css = f'''
    <style>
    body {{ margin: 0; padding: 0; background: {theme["bg"]}; width: 1400px !important; box-sizing: border-box; overflow: hidden; }}
    .highlight {{ background: {theme["bg"]} !important; font-size: {config["font_size"]} !important; letter-spacing: {config["letter_spacing"]} !important; line-height: {config["line_height"]} !important; font-family: 'JetBrains Mono', monospace !important; font-weight: 500 !important; padding: 0 40px !important; }}
    .highlight pre {{ background: {theme["bg"]} !important; color: {theme["text"]} !important; padding: 10px 0 !important; margin: 0 !important; font-size: {config["font_size"]} !important; letter-spacing: {config["letter_spacing"]} !important; line-height: {config["line_height"]} !important; font-weight: 500 !important; white-space: pre-wrap; word-break: break-all; overflow-wrap: break-word; word-wrap: break-word; }}
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
    full_highlighted = highlight(sample_code, CLexer(), formatter)
    
    import re
    pre_match = re.search(r'<pre[^>]*>(.*?)</pre>', full_highlighted, re.DOTALL)
    chunk_html = pre_match.group(1) if pre_match else full_highlighted
    
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8">{css}</head>
<body style="width: 1400px; margin: 0; padding: 0;">
<div style="background: {theme["title_bg"]}; color: {theme["title_color"]}; padding: 25px 40px; font-family: 'JetBrains Mono', monospace; font-size: 34px; font-weight: 800; border-bottom: 2px solid {theme["title_border"]}; margin-bottom: 0; width: 1400px; box-sizing: border-box; display: block;">
compression_bad.c ({config["name"]})
</div>
<div class="highlight" style="width: 1400px; box-sizing: border-box; display: block;">
<pre style="width: 1400px; box-sizing: border-box; display: block; margin: 0;">{chunk_html}</pre>
</div>
</body>
</html>"""
    
    out_path = Path(f"sample_spacing_{config['id']}.png")
    imgkit.from_string(html, str(out_path), options=IMGKIT_OPTIONS)

if __name__ == "__main__":
    for config in configurations:
        generate_sample(config)
        print(f"Generated sample_spacing_{config['id']}.png")
