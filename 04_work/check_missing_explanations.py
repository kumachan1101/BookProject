import os
import re

TARGET_DIR = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    issues = []
    
    # Simple state machine
    # We look for #### Filename (not Execution Result)
    # Then we check the text until the next #### or code block or end
    
    # Better approach might be regex iterating over headers
    # But headers might be split (Header ... Caption).
    
    # Let's verify each "Unit" which is effectively:
    # Header -> [Explanation] -> Caption -> [Code] 
    # OR just Header/Caption -> [Explanation] -> [Code] (if malformed)
    
    # We will look for code blocks first, then scan backwards for the explanation.
    
    code_block_indices = [i for i, line in enumerate(lines) if line.strip().startswith('```') and not line.strip().startswith('```mermaid')]
    
    # We only care about opening ``` (usually ```c or ```cpp or just ```)
    # Filter to opening blocks. Simple heuristic: if previous was not code, this is start.
    # Actually, getting all ``` lines and taking every 2nd one (0, 2, 4...) is risky if nested.
    # Assuming standard markdown code blocks.
    
    block_starts = []
    in_block = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```') and not line.strip().startswith('```mermaid'):
            if not in_block:
                block_starts.append(i)
                in_block = True
            else:
                in_block = False
                
    for start_line_idx in block_starts:
        # Check preceding lines for Caption/Header
        # Scan backwards from start_line_idx
        
        caption_found = False
        header_found = False
        caption_line = -1
        
        # Look for immediate caption (#### filename)
        # Expected format: 
        # ...
        # #### filename (Caption)
        # ```
        
        scan_idx = start_line_idx - 1
        while scan_idx >= 0 and lines[scan_idx].strip() == "":
            scan_idx -= 1
            
        if scan_idx >= 0 and lines[scan_idx].strip().startswith("####"):
            header_text = lines[scan_idx].strip()[4:].strip()
            if "実行結果" in header_text or "Execution Result" in header_text:
                continue # Skip Execution Results
            
            caption_found = True
            caption_line = scan_idx
        else:
            # If no immediate caption, maybe it's missing or we have a structural issue.
            # But let's check further back for the explanation anyway.
            pass

        # Now we define the "Explanation Region".
        # It sits between the PREVIOUS section header (or end of previous code block) and THIS code block/caption.
        
        # We need to find the start of the explanation.
        # It typically starts after the "Section Header" (#### filename) which might be some lines above the Caption.
        
        # Let's search backwards from scan_idx (or caption_line if found) for the "Section Header" 
        # OR just check the distinct text blob preceding this code.
        
        # Heuristic: Scan back until we hit:
        # 1. Another code block closing (```)
        # 2. A higher level header (###, ##, #) -- Wait, #### is usually the level.
        # 3. The file start.
        
        explanation_end = scan_idx if not caption_found else caption_line - 1
        explanation_start = explanation_end
        
        found_higher_header = False
        
        for k in range(explanation_end, -1, -1):
            line = lines[k].strip()
            if line.startswith('```'):
                explanation_start = k + 1
                break
            if line.startswith('#'):
                # If it's #### and matches the caption (if caption exists), it's the Section Header.
                # If it's #### and different, it might be the previous file's caption?
                # If it's ###, it's a chapter, so stop.
                
                if line.startswith('##') and not line.startswith('####'): # ## or ###
                    explanation_start = k + 1
                    found_higher_header = True
                    break
                
                # If it is ####, includes start line
                explanation_start = k
                # If this header is the Section Header, we should include it or stop at it?
                # The prompt implies Header -> Explanation. 
                # So the explanation is AFTER this header.
                if caption_found and lines[k].strip() == lines[caption_line].strip():
                     # This is likely the Section Header for the same file
                     explanation_start = k + 1
                     break
                else: 
                     # A different #### header. Could be start of this section (if caption didn't match exactly?)
                     # or end of previous. 
                     # Let's assume explanation goes up to here.
                     pass 
            
            explanation_start = k
            
        # Extract explanation text
        ex_lines = lines[explanation_start : explanation_end+1]
        ex_text = "\n".join(ex_lines)
        
        # Check for keywords
        # Loose matching to account for bolding variations
        has_proc = "処理" in ex_text and "内容" in ex_text
        has_design = "設計" in ex_text and "意図" in ex_text
        has_eval = "評価" in ex_text
        
        if not (has_proc and has_design and has_eval):
            # Print issue
            # Get nearby filename for context
            fname = "Unknown"
            if caption_found:
                fname = lines[caption_line].strip()
            
            issues.append({
                "line": start_line_idx + 1,
                "file": os.path.basename(filepath),
                "header": fname,
                "missing": [k for k, v in [("処理内容", has_proc), ("設計意図", has_design), ("評価", has_eval)] if not v]
            })

    return issues

def main():
    all_issues = []
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    isues = analyze_file(path)
                    all_issues.extend(isues)
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    for issue in all_issues:
        print(f"{issue['file']}:{issue['line']} ({issue['header']}) missing {issue['missing']}")

if __name__ == "__main__":
    main()
