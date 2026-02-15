
import re
from pathlib import Path

TARGET_DIR = Path("../02_章別")

# Generic texts for fallback
GENERIC_DESC = {
    "h": {
        "content": "モジュールの公開インターフェース定義を行います。",
        "intent": "実装詳細を隠蔽し、外部には必要な契約（API）のみを公開することで、結合度を下げます。",
        "eval": "インターフェースと実装が分離され、高い保守性が確保されています。"
    },
    "c": {
        "content": "ヘッダで定義されたインターフェースの具体的な実装を行います。",
        "intent": "内部データや詳細ロジックをこのファイル内に閉じ込め（カプセル化）、外部からの直接アクセスを防ぎます。",
        "eval": "変更が発生しても、このファイル内のみに影響を留めることができます。"
    },
    "main": {
        "content": "モジュールのクライアントコードとして、APIを利用した処理の流れを示します。",
        "intent": "具体的な実装構造には依存せず、抽象化されたインターフェース（API）のみを通じて操作を行います。",
        "eval": "実装の変更に影響を受けない、疎結合な利用コードとなっています。"
    },
    "default": {
        "content": "コードの処理内容を示します。",
        "intent": "責任を明確にし、適切な責務の分離を行っています。",
        "eval": "可読性と保守性に優れた実装です。"
    }
}

def get_file_type(filename):
    if not filename: return "default"
    if "main" in filename.lower(): return "main"
    if filename.endswith(".h"): return "h"
    if filename.endswith(".c"): return "c"
    return "default"

def fix_file(md_path):
    print(f"Processing: {md_path.name}")
    text = md_path.read_text(encoding="utf-8")
    original_text = text
    
    # Pattern: 3 backticks + c (or C) ... 3 backticks
    code_pattern = re.compile(r'```c(.*?)```', re.DOTALL | re.IGNORECASE)
    
    new_text_parts = []
    last_end = 0
    modified = False
    
    for match in code_pattern.finditer(text):
        start, end = match.span()
        code_content = match.group(1)
        
        # Text before this code block
        pre_text = text[last_end:start]
        
        # 1. Identify if there is already a Header/Caption (#### Filename) right before the code
        # We look backwards from the end of pre_text.
        # Allow some whitespace/newlines.
        
        # Check for existing "Explanation" sections
        # We look at the ~20 lines before the code block to see if they contain the keywords.
        # This is a heuristic.
        
        scan_window_size = 1500 # chars
        scan_text = pre_text[-scan_window_size:] if len(pre_text) > scan_window_size else pre_text
        
        has_content = "**処理の内容:**" in scan_text
        has_intent = "**設計的意図:**" in scan_text
        has_eval = "**評価:**" in scan_text
        
        # Try to find the Caption line: #### Something
        # It should be close to the end of scan_text
        caption_match = re.search(r'(####\s+.*?)(\n|\r)+$', scan_text, re.MULTILINE)
        
        caption_text = ""
        filename_guess = "Source Code"
        
        if caption_match:
            caption_text = caption_match.group(1).strip()
            # Extract filename from caption for type guessing
            # Remove "#### "
            filename_guess = re.sub(r'^####\s+', '', caption_text).strip()
        else:
            # No caption found immediately before code. 
            # We might need to insert one.
            # Try to find a filename in previous lines? 
            # Or just use a default specific to the guessed file type from content?
            if "#include" in code_content and "main" in code_content: filename_guess = "main.c"
            elif "#ifndef" in code_content: filename_guess = "header.h"
            elif "#include" in code_content: filename_guess = "implementation.c"
            
            caption_text = f"#### {filename_guess}"
        
        # Determine if we need to insert explanation
        needs_fix = not (has_content and has_intent and has_eval)
        
        if needs_fix or not caption_match:
            # We need to rewrite the section before the code.
            
            # Identify where the "Explanation Section" starts. 
            # If there was a caption, we replace from the caption onwards.
            # If no caption, we just append to pre_text.
            
            insertion_point = len(pre_text)
            existing_explanation = ""
            
            if caption_match:
                # The caption is at the very end of pre_text (ignoring whitespace)
                # We want to keep the text BEFORE the caption, and insert/fix the explanation+caption.
                # However, the explanation usually comes BEFORE the caption in the desired format?
                # SKILL says:
                # 1. #### Filename (Header)
                # 2. Explanation
                # 3. #### Filename (Caption)
                # 4. Code
                
                # So if we found a caption, the explanation should be BEFORE it.
                # If the explanation is missing, we insert it before the caption.
                
                # Let's see if we can find the "Header" (Case A step 1).
                # It might be the same as the caption or different.
                # Finding the start of the explanation is hard.
                
                # Strategy: Just append the missing sections RIGHT BEFORE the caption line.
                
                # Remove the caption line from pre_text temporarily
                match_len = len(caption_match.group(0))
                pre_text_no_caption = pre_text[:-match_len].rstrip()
                caption_line = caption_match.group(1) # The #### line without trailing newlines
                
                # Now append missing sections to pre_text_no_caption
                ftype = get_file_type(filename_guess)
                defaults = GENERIC_DESC[ftype]
                
                addition = "\n\n"
                
                # If we have some sections but not others, it's messy. 
                # But commonly either all are there or none/partial.
                # We append what is missing.
                
                if not has_content:
                    addition += f"**処理の内容:** {defaults['content']}\n\n"
                if not has_intent:
                    addition += f"**設計的意図:** {defaults['intent']}\n\n"
                if not has_eval:
                    addition += f"**評価:** {defaults['eval']}\n\n"
                
                new_pre_text = pre_text_no_caption + addition + caption_line + "\n"
                
                new_text_parts.append(text[last_end:start - len(pre_text)]) # Parts before this pre_text segment? No.
                # Wait, structure is: text[last_end : start] is pre_text.
                # We replace pre_text with new_pre_text.
                new_text_parts.append(new_pre_text)
                new_text_parts.append(match.group(0))
                
                last_end = end
                modified = True
                
            else:
                # No caption found. 
                # We should add explanation AND caption.
                
                ftype = get_file_type(filename_guess)
                defaults = GENERIC_DESC[ftype]
                
                addition = "\n\n"
                if not has_content: addition += f"**処理の内容:** {defaults['content']}\n\n"
                if not has_intent: addition += f"**設計的意図:** {defaults['intent']}\n\n"
                if not has_eval: addition += f"**評価:** {defaults['eval']}\n\n"
                
                addition += f"#### {filename_guess}\n"
                
                new_text_parts.append(pre_text.rstrip() + addition)
                new_text_parts.append(match.group(0))
                last_end = end
                modified = True
                
        else:
            # All good
            new_text_parts.append(text[last_end:end])
            last_end = end
            
    new_text_parts.append(text[last_end:])
    
    if modified:
        final_text = "".join(new_text_parts)
        if final_text != original_text:
            md_path.write_text(final_text, encoding="utf-8")
            print(f"  -> Fixed.")
        else:
            print("  -> Content identical.")
    else:
        print("  -> No changes.")

def main():
    if not TARGET_DIR.exists():
        print("Target directory not found.")
        return

    for md_file in sorted(TARGET_DIR.glob("*.md")):
        try:
            fix_file(md_file)
        except Exception as e:
            print(f"Error processing {md_file}: {e}")

if __name__ == "__main__":
    main()
