import os
import re
import glob

def heal_content(content):
    # Mermaidブロックを保護
    parts = re.split(r'(```mermaid[\s\S]*?```)', content)
    
    # 接続の不自然な行の開始パターン
    broken_starters = [
        'は', 'が', 'を', 'に', 'と', 'で', 'や', 
        'を用いる', 'によって', 'により', 'を学び', 'を習得', 
        'の採用は', 'などの', '属性（'
    ]
    
    fixed_parts = []
    for i, part in enumerate(parts):
        if part.startswith('```mermaid'):
            fixed_parts.append(part)
        else:
            lines = part.split('\n')
            new_lines = []
            skip_next = False
            
            for j in range(len(lines)):
                if skip_next:
                    skip_next = False
                    continue
                
                line = lines[j]
                
                # 見出し行 (### または ####) を探す
                match = re.match(r'^(#{2,4})\s+(.+)$', line)
                if match:
                    level_hashes = match.group(1)
                    title = match.group(2)
                    
                    # 次の非空行をチェック
                    found_target = False
                    target_line_idx = -1
                    
                    for k in range(j + 1, min(j + 4, len(lines))):
                        if lines[k].strip():
                            if any(lines[k].strip().startswith(s) for s in broken_starters):
                                found_target = True
                                target_line_idx = k
                            break
                    
                    if found_target:
                        # 結合する
                        # 見出しを太字に戻す
                        new_text = f"**{title}**" + lines[target_line_idx].strip()
                        new_lines.append(new_text)
                        
                        # jからtarget_line_idxまでの行（空行含む）をスキップ
                        # ただし、j番目の行を今appendしたので、j+1番目からをスキップ対象にするフラグ管理が必要
                        # ここでは直接jを調整するのが難しいので、後続のループでスキップさせる
                        # 間に空行がある場合も消す
                        
                        # 修正: target_line_idx までを処理したことにする
                        # この場所で skip_next のようなフラグを適切に設定する
                        # 簡易的に、jを更新する
                        # (Pythonのfor rangeはjを更新しても次に戻るので、whileを使うのがよい)
                        pass
                
                # whileループで書き直す
    
    # 書き直し...
    return heal_content_v2(content)

def heal_content_v2(content):
    parts = re.split(r'(```mermaid[\s\S]*?```)', content)
    broken_starters = [
        'は', 'が', 'を', 'に', 'と', 'で', 'や', 
        'を用いる', 'によって', 'により', 'を学び', 'を習得', 
        'の採用は', 'などの', '属性（'
    ]
    
    fixed_parts = []
    for part in parts:
        if part.startswith('```mermaid'):
            fixed_parts.append(part)
            continue
            
        lines = part.split('\n')
        new_lines = []
        j = 0
        while j < len(lines):
            line = lines[j]
            match = re.match(r'^(#{2,4})\s+(.+)$', line)
            
            if match:
                title = match.group(2)
                found_target = False
                target_idx = -1
                
                # 次の非空行を探す（2行先まで）
                for k in range(j + 1, min(j + 3, len(lines))):
                    if lines[k].strip():
                        if any(lines[k].strip().startswith(s) for s in broken_starters):
                            found_target = True
                            target_idx = k
                        break
                
                if found_target:
                    # 結合
                    healed_line = f"**{title}**" + lines[target_idx].strip()
                    new_lines.append(healed_line)
                    j = target_idx + 1
                    continue
            
            new_lines.append(line)
            j += 1
            
        fixed_parts.append('\n'.join(new_lines))
        
    return "".join(fixed_parts)

def main():
    target_dir = r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
    files = glob.glob(os.path.join(target_dir, "*.md"))
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = heal_content_v2(content)
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Healed: {os.path.basename(file_path)}")

if __name__ == "__main__":
    main()
