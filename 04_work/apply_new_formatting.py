import os
import re

def apply_formatting(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    
    # Track Last Header Level (None, 1, 2, 3, 4, 5, 6)
    last_header_level = None

    # Patterns
    re_header = re.compile(r'^(#+)\s+(.*)$')
    re_code_fence = re.compile(r'^\s*```')
    in_code_block = False

    # Match: (indent) [- ] **Title**[:]? (content)
    re_promote_candidate = re.compile(r'^(\s*(?:-\s+)?)\*\*([^\*]+)\*\*[:：]?\s*(.*)$')
    
    # Specific H5 Labels Mapping
    SPECIAL_H5_MAP = {
        "処理の内容": "処理の内容",
        "設計的意図": "設計的意図",
        "評価": "評価",
        "この図が示すもの": "この図が示すもの",
        "注目ポイント": "注目ポイント",
        "読み方のガイド": "読み方のガイド"
    }

    # Buffer for "ファイルの役割" content
    file_role_content = ""

    while i < len(lines):
        line = lines[i]
        
        # Toggle code block status
        if re_code_fence.match(line):
            in_code_block = not in_code_block
            new_lines.append(line)
            i += 1
            continue
            
        if in_code_block:
            new_lines.append(line)
            i += 1
            continue

        # Check for Header
        match_header = re_header.match(line)
        if match_header:
            level = len(match_header.group(1))
            title = match_header.group(2).strip()
            clean_title = title.rstrip(" :：")
            
            # --- Handle "ファイルの役割" header ---
            if clean_title == "このファイルの役割":
                # Collect next lines until next header as role content
                file_role_content = ""
                i += 1
                while i < len(lines):
                    if re_header.match(lines[i]):
                        break
                    file_role_content += lines[i].strip() + " "
                    i += 1
                file_role_content = file_role_content.strip()
                continue # Skip this header line

            # --- Specific H5 Labels Mapping for existing headers ---
            if clean_title in SPECIAL_H5_MAP:
                target_level = 5
                final_title = SPECIAL_H5_MAP[clean_title]
                
                # Prepend role content if this is "処理の内容"
                collected_content = ""
                if clean_title == "処理の内容" and file_role_content:
                    collected_content = file_role_content + " "
                    file_role_content = ""
                
                # Collect next lines until next header as content for this H5
                i += 1
                while i < len(lines):
                    if re_header.match(lines[i]):
                        break
                    # Skip bolded list versions if they match the same title
                    if re_promote_candidate.match(lines[i]):
                        cand_title = re_promote_candidate.match(lines[i]).group(2).strip().rstrip(" :：")
                        if cand_title == clean_title:
                            collected_content += re_promote_candidate.match(lines[i]).group(3).strip() + " "
                            i += 1
                            continue
                    collected_content += lines[i].strip() + " "
                    i += 1
                
                # Write back the new H5 header and content
                if new_lines and new_lines[-1].strip() != "":
                    new_lines.append("\n")
                new_lines.append(f"{'#' * target_level} {final_title}\n")
                if collected_content.strip():
                    new_lines.append(f"{collected_content.strip()}\n")
                
                last_header_level = target_level
                continue

            last_header_level = level
            new_lines.append(line)
            i += 1
            continue

        # Check for Promotion Candidate (Bolded list items)
        match_cand = re_promote_candidate.match(line)
        if match_cand:
            raw_title = match_cand.group(2).strip()
            clean_title = raw_title.rstrip(" :：")
            content = match_cand.group(3).strip()
            
            if clean_title in SPECIAL_H5_MAP:
                target_level = 5
                final_title = SPECIAL_H5_MAP[clean_title]
                
                # Prepend role content if this is "処理の内容"
                if clean_title == "処理の内容" and file_role_content:
                    content = file_role_content + " " + content
                    file_role_content = ""
                
                if new_lines and new_lines[-1].strip() != "":
                    new_lines.append("\n")
                new_lines.append(f"{'#' * target_level} {final_title}\n")
                if content.strip():
                    new_lines.append(f"{content.strip()}\n")
                print(f"  [Force H5 for Label] {clean_title}")
                i += 1
                continue
            
            elif last_header_level == 3:
                target_level = 4
                if new_lines and new_lines[-1].strip() != "":
                    new_lines.append("\n")
                new_lines.append(f"#### {raw_title}\n")
                if content: new_lines.append(f"{content}\n")
                last_header_level = target_level
                i += 1
                continue
            elif last_header_level == 4:
                target_level = 5
                if new_lines and new_lines[-1].strip() != "":
                    new_lines.append("\n")
                new_lines.append(f"##### {raw_title}\n")
                if content: new_lines.append(f"{content}\n")
                last_header_level = target_level
                i += 1
                continue
        
        # Default
        new_lines.append(line)
        i += 1    
    output_content = "".join(new_lines)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(output_content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                print(f"Processing: {full_path}")
                apply_formatting(full_path)

if __name__ == "__main__":
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02_章別"))
    print(f"Target Directory: {target_dir}")
    if os.path.exists(target_dir):
        process_directory(target_dir)
        print("Formatting complete.")
    else:
        print(f"Error: Directory not found: {target_dir}")
