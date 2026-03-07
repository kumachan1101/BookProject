import os
import re
from pathlib import Path
import imgkit
from pygments import highlight
from pygments.lexers import CLexer
from pygments.formatters import HtmlFormatter

CODE_CSS = """
<style>
/* 全体の背景 */
html, body {
  margin: 0; padding: 0; 
  background: #0F172A !important; 
  width: 2000px !important;
  max-width: 2000px !important;
  box-sizing: border-box; 
  overflow: hidden;
}

/* Pygmentsハイライトコンテナ */
.highlight {
  background: #0F172A !important;
  font-size: 38px !important;
  line-height: 1.85 !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-weight: 500 !important;
  box-sizing: border-box;
  width: 2000px !important;
  padding: 0 40px !important; /* 両端の余白 */
  display: block !important;
}

/* コード表示領域 */
.highlight pre {
  background: #0F172A !important;
  color: #FFFFFF !important;
  padding: 10px 0 !important;
  margin: 0 !important;
  font-size: 38px !important;
  line-height: 1.85 !important;
  font-weight: 500 !important;
  white-space: pre-wrap !important;
  word-wrap: break-word !important;
  word-break: break-all !important;
  display: block !important;
  box-sizing: border-box;
}

/* 一部ハイライト色だけ残す */
.highlight .c1, .highlight .cm, .highlight .c, .highlight .cp { color: #64748B !important; font-weight: 600 !important; font-style: italic !important; }
</style>
"""

def generate_test_image(options, out_name):
    code = """#include <stdio.h>
// -------------------------------------------------------------------------------------------------------------------------------------------------------------
// これは非常に長い行のコメントです。もしCSSでの幅計算が甘ければ、文字が折り返すか突き抜けた右側の背景がこの行のように暗く塗りつぶされず、黒い隙間ができてしまいます。さらにここの文字列は1400pxを確実に超える長さになっています！！！！！
// -------------------------------------------------------------------------------------------------------------------------------------------------------------
int main() {
    printf("Test rendering to check background issues.\\n");
    return 0;
}
"""
    formatter = HtmlFormatter(full=False, linenos=False, noclasses=False)
    full_highlighted = highlight(code, CLexer(), formatter)
    
    pre_match = re.search(r'<pre[^>]*>(.*?)</pre>', full_highlighted, re.DOTALL)
    if not pre_match: return
    
    chunk_html = pre_match.group(1)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{CODE_CSS}
</head>
<body style="margin: 0; padding: 0; background-color: #0F172A; width: 2000px;">
<div style="background: #1E293B; color: #F8FAFC; padding: 25px 40px; 
    border-bottom: 2px solid #334155;
    font-size: 38px; font-weight: bold; font-family: 'JetBrains Mono', monospace;
    display: flex; align-items: center; gap: 15px; width: 2000px; box-sizing: border-box;">
    test_file_very_long_name_to_test.c
</div>
<div style="background: #0F172A; padding-top: 20px; padding-bottom: 20px; width: 2000px; box-sizing: border-box;">
<div class="highlight"><pre>{chunk_html}</pre></div>
</div>
</body>
</html>
"""
    out_path = Path(out_name)
    imgkit.from_string(html, str(out_path), options=options)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    opts1 = {
        "format": "png",
        "encoding": "UTF-8",
        "quiet": "",
        "width": "2000",
        "minimum-font-size": "1",
        "quality": "95"
    }
    opts2 = {
        "format": "png",
        "encoding": "UTF-8",
        "quiet": "",
        "width": "0", # tries to let it auto-scale?
        "minimum-font-size": "1",
        "quality": "95"
    }
    
    generate_test_image(opts1, "test_auto.png")
    generate_test_image(opts2, "test_width0.png")
