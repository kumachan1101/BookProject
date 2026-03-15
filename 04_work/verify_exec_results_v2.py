import os
import glob
import re

def verify_code_execution():
    ms_dir = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
    files = glob.glob(os.path.join(ms_dir, "*.md"))
    
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 実行結果 blocks
        # Pattern: look for a header mentioning 実行結果, followed by an optional descriptive text, then a code block.
        # Then, we want to look at the code blocks BEFORE this execution result to see if they match.
        exec_blocks = list(re.finditer(r'(#+\s*[^#\n]*実行結果[^#\n]*\n(?:[^#]*?\n)?```(?:[a-zA-Z]*)\n(.*?)```)', content, re.DOTALL))
        
        if not exec_blocks:
            continue
            
        print(f"=== File: {os.path.basename(fpath)} ===")
        
        for i, match in enumerate(exec_blocks):
            full_match = match.group(1)
            exec_output = match.group(2).strip()
            start_index = match.start()
            
            # Find the closest preceding code block before this start_index
            # Specifically look for 'main' function or 'printf'
            code_search_area = content[:start_index]
            preceding_code_blocks = list(re.finditer(r'```[cC]\n(.*?)```', code_search_area, re.DOTALL))
            
            if preceding_code_blocks:
                last_code = preceding_code_blocks[-1].group(1)
                
                # Try to extract the target string it's supposedly printing, to do a basic manual check
                print(f"  --- Exec Block {i+1} ---")
                print("  [Execution Output]:")
                for line in exec_output.split('\n')[:5]:
                    print(f"    > {line}")
                if exec_output.count('\n') >= 5:
                    print("    > ...")
                    
                print("  [Preceding Code (approx last 10 lines)]:")
                for line in last_code.split('\n')[-10:]:
                    print(f"    | {line}")
                print()

if __name__ == "__main__":
    verify_code_execution()
