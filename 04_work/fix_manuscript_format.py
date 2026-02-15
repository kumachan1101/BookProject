
import re
from pathlib import Path
import shutil

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
    if "main" in filename.lower(): return "main"
    if filename.endswith(".h"): return "h"
    if filename.endswith(".c"): return "c"
    return "default"

def fix_file(md_path):
    print(f"Processing: {md_path.name}")
    text = md_path.read_text(encoding="utf-8")
    original_text = text
    
    # Pattern to find code blocks and their preceding context
    # We look for a line that starts with #### Filename, followed by content, followed by ```c
    # But often the Caption #### Filename is missing.
    
    # Strategy:
    # 1. Split by code blocks.
    # 2. For each block, check preceding lines for #### Filename.
    # 3. Analyze the text between Header and Code.
    
    # Split text into segments based on code blocks
    # Using splitting might represent challenges with capturing the delimiter.
    # Let's use re.finditer to locate code blocks.
    
    code_pattern = re.compile(r'```c(.*?)```', re.DOTALL)
    
    # We will build a new text string
    new_text_parts = []
    last_end = 0
    
    modified = False
    
    for match in code_pattern.finditer(text):
        start, end = match.span()
        code_content = match.group(1)
        
        pre_text = text[last_end:start]
        
        # Look for the last header `#### ...` in pre_text
        # We need to be careful not to grab a header that belongs to a previous section if there's a lot of text.
        # Limit search to last 30 lines? No, user might write long explanation.
        # Look for the NEAREST #### header.
        
        headers = list(re.finditer(r'^####\s+(.+?)\s*$', pre_text, re.MULTILINE))
        
        if headers:
            last_header_match = headers[-1]
            header_title = last_header_match.group(1).strip()
            header_end_pos = last_header_match.end()
            
            # Text between Header and Code
            explanation = pre_text[header_end_pos:]
            
            # Check if this header is "Execution Result" - skip if so
            if "実行結果" in header_title or "出力" in header_title:
                 new_text_parts.append(text[last_end:end])
                 last_end = end
                 continue
            
            # Check if this header is actually for this code.
            # If there's another # header in between, then this #### belongs to that.
            # But we searched for ####. What if there is ###?
            # User rule says use #### for filenames.
            
            # Check if explanation already has specific sections
            has_content = "**処理の内容:**" in explanation
            has_intent = "**設計的意図:**" in explanation
            has_eval = "**評価:**" in explanation
            
            # Check if there is a duplicate header (Caption) right before code
            # We look at the lines immediately preceding `start`
            # pre_text.strip().endswith(f"#### {header_title}") check is tricky due to whitespace.
            
            explanation_stripped = explanation.strip()
            # If explanation ends with the header title (caption), identifying it.
            
            has_caption = False
            caption_regex = re.compile(rf'####\s+{re.escape(header_title)}\s*$', re.MULTILINE)
            if caption_regex.search(explanation):
                has_caption = True
                # Remove caption from explanation for processing
                explanation = caption_regex.sub('', explanation)
            
            # Refine explanation text (remove whitespace)
            content_text = explanation.strip()
            
            # Construct new explanation
            new_explanation = "\n\n"
            
            ftype = get_file_type(header_title)
            defaults = GENERIC_DESC[ftype]
            
            if not has_content:
                if content_text:
                    new_explanation += f"**処理の内容:** {content_text}\n\n"
                else:
                    new_explanation += f"**処理の内容:** {defaults['content']}\n\n"
            else:
                 new_explanation += f"{content_text}\n\n"
            
            if not has_intent:
                new_explanation += f"**設計的意図:** {defaults['intent']}\n\n"
            
            if not has_eval:
                new_explanation += f"**評価:** {defaults['eval']}\n\n"
                
            # Add Caption
            new_explanation += f"#### {header_title}\n"
            
            # Reconstruct part
            # pre_text is up to header_end_pos + explanation + (caption was removed) + code
            # We replace [header_end_pos : start] with new_explanation
            
            part_before_header = pre_text[:header_end_pos]
            new_text_parts.append(part_before_header)
            new_text_parts.append(new_explanation)
            new_text_parts.append(match.group(0)) # The code block
            
            last_end = end
            modified = True
            
        else:
            # No header found nearby. Text might describe code but no filename header?
            # Or maybe it follows "実行結果"?
            # Leave as is to avoid breaking structure
            new_text_parts.append(text[last_end:end])
            last_end = end

    new_text_parts.append(text[last_end:])
    
    if modified:
        final_text = "".join(new_text_parts)
        if final_text != original_text:
            md_path.write_text(final_text, encoding="utf-8")
            print(f"  -> Fixed.")
        else:
            print("  -> No changes needed (content match).")
    else:
        print("  -> No changes needed.")

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
