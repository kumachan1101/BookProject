import os
import re

directory = 'c:/Users/kumac/OneDrive/デスクトップ/antigravity/BookProject/02_章別'
md_files = [f for f in os.listdir(directory) if f.endswith('.md')]

with open(os.path.join(directory, 'analysis_result.txt'), 'w', encoding='utf-8') as out:
    for f in md_files:
        content = open(os.path.join(directory, f), encoding='utf-8').read()
        code_blocks = re.findall(r'```c\n(.*?)\n```', content, re.DOTALL)
        
        mallocs = []
        frees = []
        static_vars = []
        
        for i, code in enumerate(code_blocks):
            lines = code.split('\n')
            for j, line in enumerate(lines):
                sline = line.strip()
                # Find static variables (not functions, not constants)
                if sline.startswith('static ') and '(' not in sline and 'const ' not in sline:
                    static_vars.append(f"Line {j+1}: {sline}")
                
                # Memory allocation
                if 'malloc(' in sline or 'calloc(' in sline or 'strdup(' in sline:
                    mallocs.append(f"Line {j+1}: {sline}")
                if 'free(' in sline:
                    frees.append(f"Line {j+1}: {sline}")
                    
        if static_vars or mallocs or frees:
            out.write(f"\n--- {f} ---\n")
            if static_vars:
                out.write("Static Variables (Check for Thread Safety):\n")
                for v in static_vars: out.write("  " + v + "\n")
            if mallocs:
                out.write("Allocations:\n")
                for m in mallocs: out.write("  " + m + "\n")
            if frees:
                out.write("Frees:\n")
                for fr in frees: out.write("  " + fr + "\n")
