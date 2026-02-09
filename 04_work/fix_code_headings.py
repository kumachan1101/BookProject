# -*- coding: utf-8 -*-
"""
SKILL.md 3.2準拠修正スクリプト: コードブロック直前に#### ファイル名を追加
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def fix_code_block_headings(file_path: Path):
    """コードブロック直前に#### ファイル名を追加"""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    modified = False
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # ```cを検出
        if line.strip().startswith('```c'):
            # 実行結果セクションかチェック
            context_start = max(0, i - 10)
            context = '\n'.join(lines[context_start:i])
            if '実行結果' in context or '出力例' in context or '実行例' in context:
                i += 1
                continue
            
            # 直前の行をチェック
            prev_idx = len(new_lines) - 2
            while prev_idx >= 0 and not new_lines[prev_idx].strip():
                prev_idx -= 1
            
            if prev_idx >= 0:
                prev_line = new_lines[prev_idx].strip()
                
                # #### で始まっていない場合
                if not prev_line.startswith('####'):
                    # ファイル名を推測
                    # 前方の#### 行を探す
                    filename = None
                    for j in range(prev_idx, max(0, prev_idx - 20), -1):
                        if new_lines[j].strip().startswith('####'):
                            # #### の後のファイル名部分を抽出
                            match = re.search(r'####\s+([^\n]+)', new_lines[j])
                            if match:
                                filename = match.group(1).strip()
                                break
                    
                    if filename:
                        # 空行の直前に#### ファイル名を挿入
                        insert_idx = len(new_lines) - 1
                        while insert_idx > 0 and not new_lines[insert_idx - 1].strip():
                            insert_idx -= 1
                        
                        new_lines.insert(insert_idx, f"\n#### {filename}\n")
                        modified = True
                        print(f"  L{i+1}: #### {filename} を追加")
        
        i += 1
    
    if modified:
        new_content = '\n'.join(new_lines)
        file_path.write_text(new_content, encoding="utf-8")
    
    return modified

def main():
    print("コードブロック直前見出し自動修正開始...\n")
    
    fixed_count = 0
    
    # 問題のあるファイルのみ処理
    problem_files = [
        "04_第1部 第2章 関数ポインタと間接呼び出し - 動的結合の実現_01.md",
        "05_第1部 第3章 構造体設計とコンポジション - データと責任の統合_01.md",
        "06_第1部 第4章 不完全型と不透明ポインタ - 型情報の隠蔽による契約のカプセル化.md",
        "07_第1部 第5章 モジュール構成とヘッダ設計 - 最小限の契約公開と依存の最小化_01.md",
        "08_第1部 第6章 エラーハンドリングパターン - 堅牢な契約_01.md",
        "09_第1部 第7章 メモリ管理パターン - 責任の明確化_01.md",
        "12_第2部 第8章 単一責任原則 (SRP) 変更の軸を明確にする設計指針_01.md",
        "12_第2部 第8章 単一責任原則 (SRP) 変更の軸を明確にする設計指針_02.md",
        "13_第2部 第9章 開放閉鎖原則（OCP）：拡張のために開き、修正に対して閉じる_02.md",
        "14_第2部 第10章 リスコフ置換原則 (LSP) 多態性の安全性と契約の保証_02.md",
    ]
    
    for filename in problem_files:
        file_path = CHAPTER_DIR / filename
        if file_path.exists():
            print(f"\n処理中: {filename}")
            if fix_code_block_headings(file_path):
                print(f"  ✓ 修正完了")
                fixed_count += 1
            else:
                print(f"  - 変更なし")
    
    print(f"\n完了: {fixed_count}ファイルを修正しました")

if __name__ == "__main__":
    main()
