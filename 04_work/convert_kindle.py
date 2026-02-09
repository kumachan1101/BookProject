import os
import re
import sys

# Define source and destination directories
base_dir = r"C:\Users\kumac\OneDrive\デスクトップ\desktop\Obsidian\BookProject"
src_dir = os.path.join(base_dir, "01_原稿")
dst_dir = os.path.join(base_dir, "02_章別")

# Ensure destination directory exists
os.makedirs(dst_dir, exist_ok=True)

def process_content(content):
    # 1. Remove YAML Frontmatter
    # Matches --- at start of file, content, then --- followed by newline
    content = re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL)
    
    # 2. Convert WikiLinks with alias: [[Link|Text]] -> Text
    content = re.sub(r'\[\[(?:[^|\]]*)\|([^\]]*)\]\]', r'\1', content)
    
    # 3. Convert simple WikiLinks: [[Link]] -> Link
    content = re.sub(r'\[\[([^\]]*)\]\]', r'\1', content)
    
    # 4. Convert Callouts: > [!INFO] Title -> > **INFO: Title**
    # Matches > [!ANYTHING] Title
    def replace_callout(match):
        type_upper = match.group(1).upper()
        title = match.group(2)
        return f'> **{type_upper}: {title}**'
    
    content = re.sub(r'>\s*\[!(\w+)\]\s*(.*)', replace_callout, content)
    
    return content

processed_count = 0
try:
    files = os.listdir(src_dir)
    print(f"Found {len(files)} files in {src_dir}")
    
    for filename in files:
        if not filename.endswith(".md"):
            continue
            
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)
        
        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = process_content(content)
            
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print(f"Processed: {filename}")
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print(f"Total processed files: {processed_count}")

except Exception as e:
    print(f"Critical Error: {e}")
