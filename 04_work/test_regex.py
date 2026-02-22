import re

text = """
ABI (Application Binary Interface) 互換性の維持

*   **判断**
    ライブラリをアップデートした際、利用側のバイナリを再コンパイルせずにそのまま動かしたい場合、構造体のサイズが変わることは許されません。
*   **対策**
    不完全型を使用すれば、外部から見えるサイズは「ポインタのサイズ」で固定されます。

別の段落。

*   **所有ポインタ**
    *   親Entityが`malloc`で生成し、破棄するまでの全責任を持つ（ **Composition** ）
    *   `device_destroy`内で確実に解放する
"""

def list_to_dl_repl(match):
    block = match.group(0)
    lines = block.split('\n')
    
    html = '<dl style="margin: 1.2em 0; padding-left: 0.5em;">\n'
    in_dd = False
    
    for line in lines:
        if not line.strip():
            continue
            
        # Matches: * **Title** or - **Title**
        m_dt = re.match(r'^[\-\*]\s+\*\*(.*?)\*\*\s*$', line)
        if m_dt:
            if in_dd:
                html += '</dd>\n'
                in_dd = False
            html += f'<dt style="font-weight: bold; margin-top: 1.0em; margin-bottom: 0.3em; color: #222; border-left: 4px solid #78909c; padding-left: 0.5em;">{m_dt.group(1)}</dt>\n'
            continue
            
        # Description lines (indented)
        if line.startswith('    ') or line.startswith('\t'):
            if not in_dd:
                html += '<dd style="margin-left: 1.5em; margin-bottom: 0.8em; color: #333; line-height: 1.5;">\n'
                in_dd = True
            
            content = line.strip()
            # If the description itself contains a list item, format it with a bullet
            if content.startswith('* ') or content.startswith('- '):
                content = '• ' + content[2:]
                
            html += content + '<br/>\n'
        else:
            # Maybe text that wasn't properly indented but is part of the block
            if in_dd:
                 html += line.strip() + '<br/>\n'
            
    if in_dd:
        html += '</dd>\n'
    html += '</dl>\n\n'
    
    return html

# Match blocks of items starting with * **BOLD** and indented lines following them
pattern = re.compile(r'(?:^[\-\*]\s+\*\*(.*?)\*\*.*\n(?:(?: {4}|\t).*\n|^\s*$\n)*)+', re.MULTILINE)

res = pattern.sub(list_to_dl_repl, text)
print("=== ORIGINAL ===")
print(text)
print("=== REPLACED ===")
print(res)
