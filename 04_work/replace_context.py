import glob, re

def process_file(filepath):
    lines = open(filepath, encoding='utf-8').read().split('\n')
    out_lines = []
    
    in_void_func = False
    brace_count = 0
    has_seen_open_brace = False
    
    for orig_line in lines:
        line = orig_line
        
        # Determine if we are starting a void* context function block or macro
        # Typical signature: char* func(void* self) {
        # or macro: #define DEFINE(name) void func(void* self) {
        if not in_void_func:
            if '(' in orig_line and re.search(r'void\s*\*\s*self\b', orig_line) and not orig_line.strip().endswith(';'):
                in_void_func = True
                brace_count = 0
                has_seen_open_brace = False
                
        # Global replacements
        # Field declarations and parameters
        line = re.sub(r'void\*\s+self\b', 'void* context', line)
        line = re.sub(r'void\s+\*self\b', 'void *context', line)
        # Struct member accesses
        line = re.sub(r'->self\b', '->context', line)
        line = re.sub(r'\.self\b', '.context', line)
        
        # Local replacements inside the identified functions
        if in_void_func:
            # We replace 'self' with 'context' safely
            line = re.sub(r'\bself\b', 'context', line)
            
        out_lines.append(line)
        
        # Determine if we are ending the function block
        if in_void_func:
            brace_count += orig_line.count('{') - orig_line.count('}')
            if '{' in orig_line:
                has_seen_open_brace = True
            
            # If we've seen an open brace and now count is 0, the function is done
            if has_seen_open_brace and brace_count == 0:
                in_void_func = False
            # Check for one liner without braces (like a macro or strange formatting)
            # Actually macro usually has a \ at the end, if it's not a macro and has no brace on the first line, 
            # brace_count stays 0 and has_seen_open_brace is false until the next line. This is handled.
                
    new_content = '\n'.join(out_lines)
    if open(filepath, encoding='utf-8').read() != new_content:
        open(filepath, 'w', encoding='utf-8').write(new_content)
        print(f"Updated {filepath.split('/')[-1]}")

if __name__ == '__main__':
    md_files = glob.glob('c:/Users/kumac/OneDrive/デスクトップ/antigravity/BookProject/02_章別/*.md')
    for f in md_files:
        process_file(f)
