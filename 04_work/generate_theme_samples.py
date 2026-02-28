import os

THEMES = {
    "onedark": {
        "name": "One Dark (Atom/VSCode 標準ダーク)",
        "bg": "#282C34",
        "title_bg": "#3e4451",  # より明るいグレーで区別
        "title_color": "#ABB2BF", # 文字色は白に近いグレー
        "title_border": "#5c6370",
        "fg": "#ABB2BF",
        "comment": "#5c6370",
        "keyword": "#c678dd",  # パープル
        "string": "#98c379",   # グリーン
        "function": "#61afef", # ブルー
        "number": "#d19a66",   # オレンジ
        "operator": "#56b6c2", # シアン
    },
    "dracula": {
        "name": "Dracula (鮮やかなダーク)",
        "bg": "#282a36",
        "title_bg": "#44475a",  # より明るいパープルグレー
        "title_color": "#f8f8f2",
        "title_border": "#6272a4",
        "fg": "#f8f8f2",
        "comment": "#6272a4",
        "keyword": "#ff79c6",  # ピンク
        "string": "#f1fa8c",   # イエロー
        "function": "#50fa7b", # グリーン
        "number": "#bd93f9",   # パープル
        "operator": "#ffb86c", # オレンジ
    },
    "nord": {
        "name": "Nord (北欧風クールダーク)",
        "bg": "#2E3440",
        "title_bg": "#4C566A",  # より明るいグレー
        "title_color": "#ECEFF4",
        "title_border": "#81A1C1",
        "fg": "#D8DEE9",
        "comment": "#616E88",  # Kindleでも見えるように少し明るめ
        "keyword": "#81A1C1",  # ブルー
        "string": "#A3BE8C",   # グリーン
        "function": "#88C0D0", # ライトブルー
        "number": "#B48EAD",   # パープル
        "operator": "#EBCB8B", # イエロー
    },
    "vscode_light": {
        "name": "VS Code Light (定番ライト色)",
        "bg": "#FFFFFF",
        "title_bg": "#F3F3F3",  # 薄いグレー
        "title_color": "#000000",
        "title_border": "#CCCCCC",
        "fg": "#000000",
        "comment": "#008000",  # グリーン
        "keyword": "#0000FF",  # ブルー
        "string": "#A31515",   # ダークレッド
        "function": "#795E26", # ブラウン
        "number": "#098658",   # ダークグリーン
        "operator": "#000000",
    },
    "github_light": {
        "name": "GitHub Light (明るくクリアな色)",
        "bg": "#FFFFFF",
        "title_bg": "#F6F8FA",  # ほんのりブルーがかった極薄グレー
        "title_color": "#24292F",
        "title_border": "#D0D7DE",
        "fg": "#24292F",
        "comment": "#6E7781",  # グレー
        "keyword": "#CF222E",  # レッド
        "string": "#0A3069",   # ネイビー
        "function": "#8250DF", # パープル
        "number": "#0550AE",   # ブルー
        "operator": "#000000",
    }
}

SAMPLE_CODE = """#include <stdio.h>

// サンプルコメント
void sample_function(int value) {
    if (value > 0) {
        printf("Value is %d\\n", value);
    } else {
        return;
    }
}
"""

def generate_html(theme_id, theme):
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{theme['name']} - Sample</title>
<style>
body {{ margin: 0; padding: 20px; background: #e0e0e0; font-family: sans-serif; }}
.container {{ margin: 0 auto; width: 1400px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}

/* タイトル帯 */
.title-bar {{
    background: {theme['title_bg']};
    color: {theme['title_color']};
    padding: 25px 40px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 34px;
    font-weight: 800;
    border-bottom: 2px solid {theme['title_border']};
    box-sizing: border-box;
}}

/* Pygmentsコンテナ */
.highlight {{
    background: {theme['bg']} !important;
    font-size: 38px !important;
    line-height: 1.45 !important;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
    font-weight: 600 !important;
    padding: 0 40px !important;
    box-sizing: border-box;
}}

.highlight pre {{
    background: {theme['bg']} !important;
    color: {theme['fg']} !important;
    padding: 10px 0 !important;
    margin: 0 !important;
    font-size: 38px !important;
    line-height: 1.45 !important;
    font-weight: 600 !important;
    white-space: pre-wrap;
}}

/* 各要素の色 */
.highlight .c1, .highlight .cm, .highlight .c {{ color: {theme['comment']} !important; font-weight: 600 !important; }}
.highlight .cp {{ color: {theme['keyword']} !important; font-weight: 700 !important; }}
.highlight .cpf {{ color: {theme['string']} !important; font-weight: 700 !important; }}
.highlight .k, .highlight .kt {{ color: {theme['keyword']} !important; font-weight: 700 !important; }}
.highlight .nf, .highlight .nb {{ color: {theme['function']} !important; font-weight: 700 !important; }}
.highlight .n {{ color: {theme['fg']} !important; }}
.highlight .mi, .highlight .mf {{ color: {theme['number']} !important; font-weight: 700 !important; }}
.highlight .s {{ color: {theme['string']} !important; font-weight: 700 !important; }}
.highlight .o {{ color: {theme['operator']} !important; font-weight: 700 !important; }}
.highlight .p {{ color: {theme['fg']} !important; }}

h1 {{ text-align: center; color: #333; }}
</style>
</head>
<body>
    <h1>{theme['name']}</h1>
    <div class="container">
        <div class="title-bar">sample.c</div>
        <div class="highlight">
<pre>
<span class="cp">#include</span> <span class="cpf">&lt;stdio.h&gt;</span>

<span class="c1">// サンプルコメント</span>
<span class="kt">void</span> <span class="nf">sample_function</span>(<span class="kt">int</span> <span class="n">value</span>) {{
    <span class="k">if</span> (<span class="n">value</span> <span class="o">&gt;</span> <span class="mi">0</span>) {{
        <span class="nf">printf</span>(<span class="s">"Value is %d\\n"</span>, <span class="n">value</span>);
    }} <span class="k">else</span> {{
        <span class="k">return</span>;
    }}
}}
</pre>
        </div>
    </div>
</body>
</html>
"""
    filename = f"theme_sample_{theme_id}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {filename}")

def main():
    for theme_id, theme in THEMES.items():
        generate_html(theme_id, theme)
    print("All theme samples generated successfully.")

if __name__ == "__main__":
    main()
