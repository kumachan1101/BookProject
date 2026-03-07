import os
import re
import glob

def fix_self_context():
    md_files = glob.glob('c:/Users/kumac/OneDrive/デスクトップ/antigravity/BookProject/02_章別/*.md')
    
    # 1. replace void* self with void* context
    # 2. replace (void)self with (void)context
    # 3. replace ->self with ->context (e.g. tax->self)
    # 4. replace (Type*)self with (Type*)context inside type casts
    # 5. replace self ? with context ? (for ternary)
    
    replacements = [
        (r'void\*\s+self', 'void* context'),
        (r'void\s+\*self', 'void *context'),
        (r'\(void\)self', '(void)context'),
        (r'->self\b', '->context'),
        (r'\b\.self\b', '.context'),
        (r'\(([\w\s\*]+)\)self\b', r'(\1)context'),
        (r'\bself\s*\?', 'context ?'),
        (r'free\(self\)', 'free(context)')
    ]
    
    for fpath in md_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        for pattern, repl in replacements:
            new_content = re.sub(pattern, repl, new_content)
            
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated: {os.path.basename(fpath)}')

if __name__ == "__main__":
    fix_self_context()
