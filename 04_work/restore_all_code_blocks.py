import os
import re
import glob

def extract_blocks(content):
    # ``` で始まるブロックをすべて抽出
    return re.findall(r'(```[\s\S]*?```)', content)

def restore_file(source_path, target_path):
    with open(source_path, 'r', encoding='utf-8') as f:
        source_content = f.read()
    with open(target_path, 'r', encoding='utf-8') as f:
        target_content = f.read()
        
    source_blocks = extract_blocks(source_content)
    # ターゲット側のコードブロックをユニークなプレースホルダーに置換
    # 既存の平坦化されたブロックも含む
    
    # ターゲットの分割（コードブロックで分割）
    target_parts = re.split(r'(```[\s\S]*?```)', target_content)
    
    target_blocks_count = 0
    new_parts = []
    
    s_idx = 0
    for part in target_parts:
        if part.startswith('```'):
            if s_idx < len(source_blocks):
                # 原稿のブロックを採用
                new_parts.append(source_blocks[s_idx])
                s_idx += 1
                target_blocks_count += 1
            else:
                # 原稿より多い場合はそのまま（あるいは警告）
                print(f"Warning: Extra block in target {os.path.basename(target_path)} at block index {s_idx}")
                new_parts.append(part)
        else:
            new_parts.append(part)
            
    if s_idx != len(source_blocks):
        print(f"Warning: Source has {len(source_blocks)} blocks, but target has {target_blocks_count} blocks in {os.path.basename(target_path)}")

    return "".join(new_parts)

def main():
    source_dir = r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\01_原稿"
    target_dir = r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
    
    target_files = glob.glob(os.path.join(target_dir, "*.md"))
    
    fixed_count = 0
    for t_path in target_files:
        filename = os.path.basename(t_path)
        s_path = os.path.join(source_dir, filename)
        
        if not os.path.exists(s_path):
            print(f"Source not found for: {filename}")
            continue
            
        new_content = restore_file(s_path, t_path)
        
        with open(t_path, 'r', encoding='utf-8') as f:
            old_content = f.read()
            
        if old_content != new_content:
            with open(t_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Restored blocks in: {filename}")
            fixed_count += 1
            
    print(f"\nTotal files restored: {fixed_count}")

if __name__ == "__main__":
    main()
