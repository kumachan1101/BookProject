import os
import re

def extract_blocks(content):
    return re.findall(r'```[\s\S]*?```', content)

def check_diff():
    orig_dir = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\01_原稿"
    processed_dir = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
    
    files = [f for f in os.listdir(orig_dir) if f.endswith('.md')]
    
    for filename in files:
        orig_path = os.path.join(orig_dir, filename)
        proc_path = os.path.join(processed_dir, filename)
        
        if not os.path.exists(proc_path):
            print(f"Missing in processed: {filename}")
            continue
            
        with open(orig_path, 'r', encoding='utf-8') as f:
            orig_content = f.read()
        with open(proc_path, 'r', encoding='utf-8') as f:
            proc_content = f.read()
            
        orig_blocks = extract_blocks(orig_content)
        proc_blocks = extract_blocks(proc_content)
        
        if len(orig_blocks) != len(proc_blocks):
            print(f"Mismatch in block count for {filename}: Orig={len(orig_blocks)}, Proc={len(proc_blocks)}")
            continue
            
        for i, (ob, pb) in enumerate(zip(orig_blocks, proc_blocks)):
            if ob.strip() != pb.strip():
                print(f"Block {i} in {filename} differs!")
                # Show a bit of diff for debugging
                if "mermaid" in ob:
                    print(f"  Orig: {ob[:50]}...")
                    print(f"  Proc: {pb[:50]}...")
                
    print("Check finished.")

if __name__ == "__main__":
    check_diff()
