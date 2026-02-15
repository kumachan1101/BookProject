
import glob
import os

def fix_files():
    files = glob.glob(r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\*.md')
    print(f"Fixing {len(files)} files...")
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        new_lines = []
        modified = False
        
        for i in range(len(lines)):
            curr_line = lines[i].rstrip('\n')
            
            # Use original line with newline for appending unless we modify
            original_line_with_newline = lines[i]
            
            if i > 0:
                prev_line_content = lines[i-1].rstrip('\n')
                
                # Check condition:
                # 1. Current line starts with ** (ignoring leading whitespace for detection, but checking structure)
                # 2. Previous line was not empty
                # 3. Previous line did not end with 2 spaces
                # 4. Not a list item
                
                # Logic: If current line starts with **, and previous line has text and no forced break,
                # we likely need a blank line.
                
                if curr_line.strip().startswith("**") and not (curr_line.strip().startswith("-") or curr_line.strip().startswith("* ")):
                    if prev_line_content.strip() != "" and not prev_line_content.endswith("  "):
                         # Check indentation to be safe? 
                         # If prev line is list item "- ...", and this line is indented?
                         # If prev line starts with "-", and this line starts with "**" with same indent?
                         
                         # For now, blindly inserting \n is safer than having merged text.
                         # Exception: If inside a code block?
                         # We should probably track code blocks.
                         pass
            
            new_lines.append(original_line_with_newline)

        # Re-processing with index access to look ahead/behind is easier if I rewrite logic.
        # Let's iterate and build a new list.
        
        final_lines = []
        in_code_block = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Track code blocks
            if stripped.startswith("```"):
                in_code_block = not in_code_block
            
            if i > 0 and not in_code_block:
                prev_line = lines[i-1].rstrip('\n')
                curr_line_stripped = line.strip()
                
                # Check target condition
                if curr_line_stripped.startswith("**") and \
                   not curr_line_stripped.startswith("-") and \
                   not curr_line_stripped.startswith("* "):
                    
                    if prev_line.strip() != "" and not prev_line.endswith("  "):
                        # Insert blank line before this line
                        final_lines.append("\n")
                        modified = True
            
            final_lines.append(line)
            
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(final_lines)
            print(f"Fixed {os.path.basename(file_path)}")

if __name__ == "__main__":
    fix_files()
