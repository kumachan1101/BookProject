import os
import glob
import re

def verify_code_execution():
    ms_dir = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
    files = glob.glob(os.path.join(ms_dir, "*.md"))
    
    with open("verify_exec_output.txt", "w", encoding="utf-8") as out:
        for fpath in files:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
                
            exec_blocks = list(re.finditer(r'(#+\s*[^#\n]*実行結果[^#\n]*\n(?:[^#]*?\n)?```(?:[a-zA-Z]*)\n(.*?)```)', content, re.DOTALL))
            
            if not exec_blocks:
                continue
                
            out.write(f"=== File: {os.path.basename(fpath)} ===\n")
            
            for i, match in enumerate(exec_blocks):
                exec_output = match.group(2).strip()
                start_index = match.start()
                
                code_search_area = content[:start_index]
                preceding_code_blocks = list(re.finditer(r'```[cC]\n(.*?)```', code_search_area, re.DOTALL))
                
                if preceding_code_blocks:
                    last_code = preceding_code_blocks[-1].group(1)
                    
                    out.write(f"  --- Exec Block {i+1} ---\n")
                    out.write("  [Execution Output]:\n")
                    for line in exec_output.split('\n')[:5]:
                        out.write(f"    > {line}\n")
                    if exec_output.count('\n') >= 5:
                        out.write("    > ...\n")
                        
                    out.write("  [Preceding Code (approx last 10 lines)]:\n")
                    for line in last_code.split('\n')[-10:]:
                        out.write(f"    | {line}\n")
                    out.write("\n")

if __name__ == "__main__":
    verify_code_execution()
