# -*- coding: utf-8 -*-
"""
SKILL準拠の設計ポイント自動追加スクリプト
★マーカーがある箇所に、SKILL.md 3.3の要件に基づいた設計ポイントを追加
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

# 設計ポイントテンプレート (SKILL.md 3.3準拠)
DESIGN_POINT_TEMPLATE = """
**設計ポイント**:

1. **処理内容**: {processing}
2. **設計意図**: {design_intent}
3. **評価**: {evaluation}
"""

# ファイル別の設計ポイント定義
DESIGN_POINTS = {
    "08_第1部 第6章": {
        "L99": {
            "processing": "Userモジュールの公開エラーコードを-1000番台で定義",
            "design_intent": "モジュール間でエラーコードの名前空間を分離し、エラーの発生源を即座に特定可能にする。これは**単一責任原則(SRP)**に基づき、各モジュールが自身のエラー範囲に責任を持つ設計",
            "evaluation": "**Good Pattern** - エラーコードの衝突を防ぎ、デバッグ時にエラー発生元を即座に特定できる。保守性が向上"
        },
        "L124": {
            "processing": "Storageモジュールの公開エラーコードを-2000番台で定義",
            "design_intent": "下位層モジュールとして独立したエラー範囲を確保し、上位層(User)との依存を最小化。**依存性逆転原則(DIP)**の実践",
            "evaluation": "**Good Pattern** - モジュール間の結合度を下げ、Storageモジュールの独立性を保つ"
        },
        "L147": {
            "processing": "エラーコードのマッピング処理",
            "design_intent": "下位層のエラーを上位層の抽象エラーにマッピングすることで、実装詳細を隠蔽。**契約の安定性**を確保",
            "evaluation": "**Good Pattern** - 下位層の変更が上位層に波及しない。変更容易性が向上"
        },
        "L279": {
            "processing": "エラーハンドリングの実装例",
            "design_intent": "エラーの伝播経路を明示し、各層での責任を明確化。**責任の明確化**",
            "evaluation": "**Good Pattern** - エラー処理の流れが追跡可能で、デバッグが容易"
        },
        "L451": {
            "processing": "エラーリカバリー処理",
            "design_intent": "エラー発生時の回復戦略を実装し、システムの堅牢性を向上。**堅牢な契約**の実現",
            "evaluation": "**Good Pattern** - 異常系でもシステムが安全に動作する"
        },
        "L490": {
            "processing": "エラーログ出力",
            "design_intent": "エラー情報を記録し、事後分析を可能にする。**可観測性**の向上",
            "evaluation": "**Good Pattern** - 本番環境での問題追跡が容易になる"
        },
        "L858": {
            "processing": "実行結果の出力",
            "design_intent": "エラーハンドリングの動作を実証し、設計の正しさを検証",
            "evaluation": "この実行結果から、エラーコードが正しくマッピングされ、各層で適切に処理されていることが確認できる"
        }
    }
}

def add_design_points_to_file(file_path: Path, markers: list):
    """ファイルに設計ポイントを追加"""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    # ★マーカーを含む行を特定して設計ポイントを追加
    modified = False
    for marker in markers:
        line_num = marker["line"] - 1  # 0-indexed
        if line_num < len(lines) and '★' in lines[line_num]:
            # ★マーカー行を削除
            star_line = lines[line_num]
            
            # 設計ポイントを取得
            file_key = file_path.stem[:20]  # ファイル名の最初の20文字
            line_key = f"L{marker['line']}"
            
            if file_key in DESIGN_POINTS and line_key in DESIGN_POINTS[file_key]:
                dp = DESIGN_POINTS[file_key][line_key]
                design_point = DESIGN_POINT_TEMPLATE.format(**dp)
                
                # ★マーカー行を設計ポイントに置換
                lines[line_num] = design_point
                modified = True
                print(f"  追加: {file_path.name}:L{marker['line']}")
    
    if modified:
        # ファイルを更新
        new_content = '\n'.join(lines)
        file_path.write_text(new_content, encoding="utf-8")
        return True
    return False

def main():
    print("設計ポイント自動追加開始...\n")
    
    # Chapter 6のみ処理 (テスト)
    target_file = CHAPTER_DIR / "08_第1部 第6章 エラーハンドリングパターン - 堅牢な契約_01.md"
    
    if target_file.exists():
        # ★マーカーを検出
        content = target_file.read_text(encoding="utf-8")
        lines = content.split('\n')
        markers = []
        for i, line in enumerate(lines, 1):
            if '★' in line:
                markers.append({"line": i, "content": line.strip()})
        
        print(f"{target_file.name}: {len(markers)}箇所の★マーカー")
        
        if add_design_points_to_file(target_file, markers):
            print(f"\n✓ {target_file.name} 更新完了")
        else:
            print(f"\n- {target_file.name} 変更なし")
    else:
        print(f"ファイルが見つかりません: {target_file}")

if __name__ == "__main__":
    main()
