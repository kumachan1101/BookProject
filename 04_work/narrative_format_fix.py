import os
import re

def narrativize_text(text):
    if not text.strip(): return ""
    
    # Common labels to strip specifically
    known_labels = [
        "処理の内容", "設計的意図", "評価", "設計的視点", "目的", "機能", 
        "概要", "システム概要", "注目ポイント", "読み方のガイド", 
        "この図が示すもの", "達成される設計上のメリット", "状態保持の仕組み",
        "依存関係と隠蔽の構造", "構成図", "アーキテクチャ", "入出力", "解決する設計課題",
        "制御する範囲", "役割", "原則パート", "統合実践パート", "解決に使う道具", 
        "実現する設計原則", "効果", "技術（道具）", "原則（指針）", "目的（価値）", 
        "現状（アンチパターン）", "解決策", "問題点", "課題の概要", "はじめに", "次章への橋渡し"
    ]
    
    lines = text.split('\n')
    buffer = []
    
    for line in lines:
        s = line.strip()
        if not s: continue
        
        # 1. Strip leading colons, bullets, and spaces
        s = re.sub(r'^[:：\-\*\s]+', '', s)
        
        # 2. Aggressively strip any leading bold labels: **Label**: or **Label** followed by colon/space
        # This covers things like **制御する範囲**: or **役割**:
        s = re.sub(r'^\*?\*?.*?\*?\*?[:：\s]*', '', s, count=1) if re.match(r'^\*?\*?.*?\*?\*?[:：\s]', s) else s
        
        # 3. Specifically strip known labels if they were missed (without bold)
        for lbl in known_labels:
            pat = r'^' + re.escape(lbl) + r'[:：\s]*'
            if re.match(pat, s):
                s = re.sub(pat, '', s).strip()
                break
        
        # 4. Cleanup residual symbols at start
        s = re.sub(r'^[:：\-\*\s]+', '', s).strip()
        
        if s: buffer.append(s)
            
    if not buffer: return ""
    
    # Join into flow
    raw_text = " ".join(buffer).strip()
    raw_text = raw_text.replace("。。", "。")
    
    # Split into sentences to re-group
    sentences = re.split(r'(?<=[。！？])\s*', raw_text)
    proc_s = []
    for s in sentences:
        s = s.strip()
        if not s: continue
        if not s.endswith(('。', '！', '？')): s += "。"
        proc_s.append(s)
    
    if not proc_s: return ""

    # Grouping for Kindle (2-3 sentences per paragraph) 
    paragraphs = []
    for i in range(0, len(proc_s), 2):
        para = "".join(proc_s[i:i+2])
        paragraphs.append(para)
        
    return "\n\n" + "\n\n".join(paragraphs).strip() + "\n\n"

def fix_content(filename, content):
    content = content.replace('\r\n', '\n')
    
    # 1. Protect Blocks and Tables
    protected_blocks = []
    placeholder_base = "___STRICT_PROTECT_"
    
    def repl_block(m):
        idx = len(protected_blocks)
        protected_blocks.append(m.group(0))
        return f"\n\n{placeholder_base}_B_{idx}___\n\n"
    
    def repl_table(m):
        idx = len(protected_blocks)
        protected_blocks.append(m.group(0).strip())
        return f"\n\n{placeholder_base}_T_{idx}___\n\n"

    # Protect code/mermaid
    content = re.sub(r'```[\s\S]*?```', repl_block, content)
    # Protect Tables
    content = re.sub(r'(?:^|\n)(\|.*\|[ \t]*\n(?:\|[:\-\s|]*\|[ \t]*\n)?(?:\|.*\|[ \t]*\n)+)', repl_table, content)

    # 2. YAML and H1 (preserve original YAML if exists)
    yaml_fm = ""
    if content.startswith('---'):
        end_fm = content.find('---', 3)
        if end_fm != -1:
            yaml_content = content[:end_fm+3]
            content = content[end_fm+3:].strip()
            # Clean up the YAML if it already has our tags
            yaml_fm = yaml_content + "\n\n"
    
    h1_match = re.search(r'^# (.*)', content, re.MULTILINE)
    title = h1_match.group(1).strip() if h1_match else os.path.basename(filename)
    
    if not yaml_fm:
        tags = ["C言語", "設計原則", "Kindle", "Obsidian"]
        yaml_fm = f"---\ntags: {tags}\naliases: [\"{title}\"]\n---\n\n"
    
    chapter_num_match = re.search(r'第(\d+)章', filename)
    chapter_num = chapter_num_match.group(1).zfill(2) if chapter_num_match else "01"
    pdf_tag = f"![PDF](chapter{chapter_num}.pdf)\n\n"
    
    content = re.sub(r'!\[PDF\].*?\n', '', content)
    if h1_match:
        content = content.replace(h1_match.group(0), f"{h1_match.group(0)}\n\n{pdf_tag}")

    # 3. Header Segmenting
    segments = re.split(r'(\n#+ .*\n)', content)
    processed_segments = []
    
    for seg in segments:
        if not seg: continue
        if re.match(r'\n#+ ', seg):
            processed_segments.append(seg)
        else:
            parts = re.split(rf'({placeholder_base}_[BT]_\d+___)', seg)
            new_parts = []
            for p in parts:
                if placeholder_base in p:
                    new_parts.append(p)
                else:
                    new_parts.append(narrativize_text(p))
            processed_segments.append("".join(new_parts))
            
    content = "".join(processed_segments)

    # 4. Strict Reordering: #### Header -> Overview -> Code -> Explanation
    reorder_pattern = r'(#### (?!実行結果)[^\n]+)\n+(.*?)(___STRICT_PROTECT_[BT]_\d+___)\s*(.*?)(?=\n####|\n###|\n##|\n#|$)'
    
    def repl_order(match):
        header = match.group(1).strip()
        ov = match.group(2).strip()
        code_placeholder = match.group(3).strip()
        ex = match.group(4).strip()
        
        ov_text = ov if ov else "実装例とその設計ポイントを解説します。"
        ex_text = ex if ex else ""
        
        return f"{header}\n\n{ov_text}\n\n{code_placeholder}\n\n{ex_text}"

    content = re.sub(reorder_pattern, repl_order, content, flags=re.DOTALL)

    # 5. Final Restoration
    for i, block in enumerate(protected_blocks):
        if block.startswith("```") and "```mermaid" not in block:
            lines = block.split('\n')
            cleaned_code = [l for l in lines[1:-1] if l.strip()]
            block = f"{lines[0]}\n" + "\n".join(cleaned_code) + f"\n{lines[-1]}"
            
        content = content.replace(f"{placeholder_base}_B_{i}___", block)
        content = content.replace(f"{placeholder_base}_T_{i}___", block)
        
    content = content.replace("。。", "。")
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return yaml_fm + content.strip() + "\n"

def run():
    orig_dir = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\01_原稿"
    target_dir = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
    
    files = sorted([f for f in os.listdir(orig_dir) if f.endswith('.md')])
    for filename in files:
        orig_path = os.path.join(orig_dir, filename)
        target_path = os.path.join(target_dir, filename)
        with open(orig_path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = fix_content(filename, content)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Processed: {filename}")

if __name__ == "__main__":
    run()
