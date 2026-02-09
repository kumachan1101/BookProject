from pathlib import Path

FILE_PATH = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\12_第2部 第8章 単一責任原則 (SRP) 変更の軸を明確にする設計指針_02.md")

def main():
    text = FILE_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    insertions = [
        # Before #### 実行結果（適用前）
        (80, "**実行結果:** 以下のように、想定通りの動作をすることを確認します。\n\n"),
        
        # Before #### compression_strategy.h
        (145, "**抽象の定義:** 圧縮アルゴリズムの共通インターフェースを定義します。クライアントはこのインターフェースにのみ依存します。\n\n"),
        
        # Before #### 実行結果（適用後）
        (378, "**実行結果:** Strategyパターン適用後も、外部からの振る舞いは変わらず、正しく動作していることが確認できます。\n\n"),
        
        # Before #### ui.c
        (755, "### ui.c\n\n**表示ロジックの実装:** 抽象化された `Library` からデータを取得し、整形して出力します。内部データ構造への直接依存はありません。\n\n"),
        
        # Before #### main.c
        (789, "**メイン関数:** データの `Library` と表示の `UI` を組み合わせて動作させます。各モジュールが独立しているため、組み合わせが容易です。\n\n")
    ]

    insertions.sort(key=lambda x: x[0], reverse=True)

    for line_num, text_to_insert in insertions:
        index = line_num - 1
        line_content = lines[index]
        print(f"Checking line {line_num}: {line_content}")
        
        lines.insert(index, text_to_insert)
        print(f"Inserted at line {line_num}")

    new_text = "\n".join(lines)
    FILE_PATH.write_text(new_text, encoding="utf-8")
    print("Done.")

if __name__ == "__main__":
    main()
