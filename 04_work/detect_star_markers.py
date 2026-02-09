# -*- coding: utf-8 -*-
"""
包括的な★マーカー処理スクリプト
全ファイルの★マーカーを検出し、パターン別に自動修正
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

# ★マーカーのパターンと対応
STAR_PATTERNS = {
    "設計ポイント不足": r"★.*設計ポイント.*",
    "システム概要欠如": r"★.*システム.*例.*記載.*",
    "コードブロック分割": r"★.*コードブロック分割.*",
    "Mermaid図エラー": r"★.*mermaid.*エラー.*",
    "Mermaid図修正": r"★.*mermaid.*修正.*",
    "説明不明瞭": r"★.*説明.*おかしい.*",
    "実行結果説明不足": r"★.*実行結果.*説明.*",
    "用語説明不足": r"★.*用語.*説明.*",
    "その他": r"★.*"
}

def find_all_star_markers():
    """全★マーカーを検出"""
    results = []
    for md_file in sorted(CHAPTER_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if '★' in line:
                # パターン分類
                pattern_type = "その他"
                for ptype, pattern in STAR_PATTERNS.items():
                    if re.search(pattern, line, re.IGNORECASE):
                        pattern_type = ptype
                        break
                
                results.append({
                    "file": md_file.name,
                    "line": i,
                    "content": line.strip(),
                    "type": pattern_type
                })
    
    return results

def main():
    print("★マーカー検出開始...")
    markers = find_all_star_markers()
    
    # パターン別に集計
    by_type = {}
    for m in markers:
        ptype = m["type"]
        if ptype not in by_type:
            by_type[ptype] = []
        by_type[ptype].append(m)
    
    print(f"\n合計: {len(markers)}箇所\n")
    
    for ptype, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
        print(f"## {ptype}: {len(items)}箇所")
        for item in items[:5]:  # 最初の5件のみ表示
            print(f"  - {item['file']}:L{item['line']}: {item['content'][:60]}...")
        if len(items) > 5:
            print(f"  ... 他{len(items)-5}件")
        print()
    
    # 詳細レポート出力
    report_path = Path("04_work/star_markers_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("★マーカー詳細レポート\n")
        f.write("=" * 80 + "\n\n")
        for ptype, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
            f.write(f"## {ptype}: {len(items)}箇所\n\n")
            for item in items:
                f.write(f"{item['file']}:L{item['line']}\n")
                f.write(f"  {item['content']}\n\n")
            f.write("\n")
    
    print(f"詳細レポート: {report_path}")

if __name__ == "__main__":
    main()
