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
                
            exec_blocks = list(re.finditer(r'(#[^\n]*?(?:実行結果|出力結果|出力例)[^\n]*\n)(.*?)(```[a-zA-Z]*\n)(.*?)(```)', content, re.DOTALL))
            
            written_header = False
            for i, match in enumerate(exec_blocks):
                between_text = match.group(2)
                # If there's another heading between "実行結果" and the code block, skip
                if re.search(r'\n#+\s', between_text):
                    continue
                
                exec_output = match.group(4).strip()
                start_index = match.start()
                
                code_search_area = content[:start_index]
                preceding_code_blocks = list(re.finditer(r'```[cC]\n(.*?)```', code_search_area, re.DOTALL))
                
                if preceding_code_blocks:
                    if not written_header:
                        out.write(f"=== File: {os.path.basename(fpath)} ===\n")
                        written_header = True
                        
                    last_code = preceding_code_blocks[-1].group(1)
                    
                    out.write(f"  --- Exec Block {i+1} ---\n")
                    out.write("  [Execution Output]:\n")
                    for line in exec_output.split('\n')[:5]:
                        out.write(f"    > {line}\n")
                    if exec_output.count('\n') >= 5:
                        out.write("    > ...\n")
                        
                    out.write("  [Preceding Code (approx last 15 lines)]:\n")
                    for line in last_code.split('\n')[-15:]:
                        out.write(f"    | {line}\n")
                    out.write("\n")

if __name__ == "__main__":
    verify_code_execution()
