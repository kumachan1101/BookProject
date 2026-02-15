import os
import re

def process_c_code(code):
    lines = code.split('\n')
    new_lines = []
    
    in_function = False
    in_declaration_block = False
    
    for i in range(len(lines)):
        line = lines[i]
        stripped = line.strip()
        
        # Rule: Include/Macro group end
        if i > 0:
            prev_line = lines[i-1].strip()
            if (prev_line.startswith('#include') or prev_line.startswith('#define')) and \
               not (stripped.startswith('#include') or stripped.startswith('#define')) and \
               stripped and not stripped.startswith('//'):
                if new_lines and new_lines[-1].strip():
                    new_lines.append('')

        # Rule: Function start detection (rudimentary)
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_* ]+\([a-zA-Z0-9_* ,]*\)$', stripped) or \
           (stripped.endswith('{') and '(' in stripped and not stripped.startswith('if') and not stripped.startswith('for')):
            if not in_function and i > 0 and new_lines and new_lines[-1].strip():
                new_lines.append('')
            in_function = True
            in_declaration_block = True
        
        # Rule: Variable declaration end (inside function)
        if in_function and in_declaration_block:
            # Check if current line is NO LONGER a declaration
            is_decl = re.match(r'^(int|char|float|double|uint\d+_t|bool|unsigned|struct|static|const|[\w\d_]+\s*\*+)[\s\w\d_\[\],=]+;', stripped)
            if not is_decl and stripped and not stripped.startswith('//') and not stripped.startswith('{'):
                if new_lines and new_lines[-1].strip() and ';' in new_lines[-1]:
                    # Previous line was likely a declaration
                    new_lines.append('')
                in_declaration_block = False

        # Rule: Control structures (if, for, while, switch)
        if any(stripped.startswith(kw) for kw in ['if', 'for', 'while', 'switch']):
            if i > 0 and new_lines and new_lines[-1].strip() and not new_lines[-1].strip().endswith('{') and not new_lines[-1].strip().startswith('//'):
                new_lines.append('')

        # Rule: return
        if stripped.startswith('return'):
            if i > 0 and new_lines and new_lines[-1].strip() and not new_lines[-1].strip().endswith('{'):
                new_lines.append('')

        new_lines.append(line)
        
        if stripped == '}':
            in_function = False

    return '\n'.join(new_lines)

def fix_markdown_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            filepath = os.path.join(directory, filename)
            print(f"Processing {filename}...")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Regex to find C code blocks
            pattern = re.compile(r'(```c\n)(.*?)(```)', re.DOTALL)
            
            def replacer(match):
                header = match.group(1)
                code = match.group(2)
                footer = match.group(3)
                processed_code = process_c_code(code)
                return f"{header}{processed_code}{footer}"
            
            new_content = pattern.sub(replacer, content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed {filename}")
            else:
                print(f"No changes needed for {filename}")

if __name__ == "__main__":
    target_dir = r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別'
    fix_markdown_files(target_dir)
