import os
import glob
import re

def fix_missing_headers():
    md_files = glob.glob(r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\*.md")
    
    for filepath in md_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        new_lines = []
        in_code_block = False
        
        for i, line in enumerate(lines):
            if line.startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    lang = line.strip().replace('```', '').lower()
                    
                    if lang != 'mermaid':
                        # Look back to find the previous non-empty line
                        prev_idx = len(new_lines) - 1
                        while prev_idx >= 0 and new_lines[prev_idx].strip() == '':
                            prev_idx -= 1
                        
                        if prev_idx >= 0:
                            prev_line = new_lines[prev_idx].strip()
                            # Check if the previous line looks like a header or other block element
                            if not any(prev_line.startswith(c) for c in ['#', '<', '>', '-', '*']):
                                # Determine header text
                                if lang in ['txt', 'text'] or '出力' in prev_line or '結果' in prev_line:
                                    header = '#### 実行結果\n'
                                else:
                                    header = '#### コード例\n'
                                
                                # Add empty line before header if necessary
                                if new_lines and new_lines[-1].strip() != '':
                                    new_lines.append('\n')
                                
                                new_lines.append(header)
                                new_lines.append('\n')
                else:
                    in_code_block = False
                    
            new_lines.append(line)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            
    print("Code block headers have been successfully fixed.")

if __name__ == '__main__':
    fix_missing_headers()
