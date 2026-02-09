# -*- coding: utf-8 -*-
"""
包括的SKILL準拠チェッカー - 全ファイル対応
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def check_file_compliance(file_path: Path):
    """ファイルのSKILL準拠を包括的にチェック"""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    issues = []
    
    # 1. コードブロック直前に#### があるかチェック (実行結果を除く)
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```c'):
            # 実行結果セクションかチェック
            context_start = max(0, i - 10)
            context = '\n'.join(lines[context_start:i])
            if '実行結果' in context or '出力例' in context or '実行例' in context:
                continue  # 実行結果はスキップ
            
            # 直前の行をチェック
            prev_line_idx = i - 2
            if prev_line_idx >= 0:
                prev_line = lines[prev_line_idx].strip()
                # 空行を遡る
                while prev_line_idx >= 0 and not prev_line:
                    prev_line_idx -= 1
                    prev_line = lines[prev_line_idx].strip() if prev_line_idx >= 0 else ""
                
                if prev_line and not prev_line.startswith('####'):
                    issues.append({
                        'type': 'code_format',
                        'line': i,
                        'message': f'コードブロック直前に#### ファイル名がありません (直前: {prev_line[:50]})'
                    })
    
    # 2. ★マーカーチェック
    for i, line in enumerate(lines, 1):
        if '★' in line:
            issues.append({
                'type': 'star_marker',
                'line': i,
                'message': f'★マーカーが残っています: {line.strip()[:50]}'
            })
    
    # 3. 見出し階層チェック
    heading_stack = []
    for i, line in enumerate(lines, 1):
        if line.startswith('#'):
            level = len(re.match(r'^#+', line).group())
            
            if level > 1 and not heading_stack:
                issues.append({
                    'type': 'heading',
                    'line': i,
                    'message': f'H1なしでH{level}が使用されています'
                })
            
            if heading_stack and level > heading_stack[-1] + 1:
                issues.append({
                    'type': 'heading',
                    'line': i,
                    'message': f'見出し階層が飛んでいます (H{heading_stack[-1]} → H{level})'
                })
            
            while heading_stack and heading_stack[-1] >= level:
                heading_stack.pop()
            heading_stack.append(level)
    
    # 4. Mermaid LR/LRチェック
    in_mermaid = False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```mermaid'):
            in_mermaid = True
        elif in_mermaid and line.strip() == '```':
            in_mermaid = False
        elif in_mermaid:
            if re.search(r'\b(graph|flowchart)\s+LR\b', line, re.I):
                issues.append({
                    'type': 'mermaid',
                    'line': i,
                    'message': 'Mermaid図がLRレイアウトです (TBに変更推奨)'
                })
    
    return issues

def main():
    print("全ファイルSKILL準拠チェック開始...\n")
    
    all_issues = {}
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        issues = check_file_compliance(file_path)
        if issues:
            all_issues[file_path.name] = issues
    
    if all_issues:
        print(f"❌ {len(all_issues)}ファイルで問題を検出:\n")
        for filename, issues in all_issues.items():
            print(f"【{filename}】 ({len(issues)}件)")
            for issue in issues[:5]:  # 最初の5件のみ表示
                print(f"  L{issue['line']}: [{issue['type']}] {issue['message']}")
            if len(issues) > 5:
                print(f"  ... 他{len(issues)-5}件")
            print()
    else:
        print("✅ 全ファイルがSKILL準拠です!")

if __name__ == "__main__":
    main()
