from pathlib import Path

FILE_PATH = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\18_第2部 第14章 統合実践（応用）_02.md")

def main():
    text = FILE_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    insertions = [
        # Before #### Image_Pipeline.c
        (159, "**設定の記述:** `main` 関数などで、それぞれのパイプライン構成を定義するコードです。順序や組み合わせを一目で理解できます。\n\n"),
        
        # Before #### Data_Analysis_Pipeline.c
        (179, "**別の例:** データ分析の分野でも、前処理（正規化、外れ値除去など）の順序を実験的に変える際、この設計が威力を発揮します。\n\n"),
        
        # Before #### test_failure.c
        (442, "**テスト失敗の例:** 以下のコードは、本物の暗号化ロジックが強制的に動いてしまうため、単体テストとして機能しません。\n\n"),
        
        # Before #### usage_confusion.c
        (461, "**使用時の混乱:** 生成関数のシグネチャ `customer_module_create(void)` だけを見ても、内部で何が必要かわからず、隠れた依存に悩まされます。\n\n")
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
