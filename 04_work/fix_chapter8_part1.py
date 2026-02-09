from pathlib import Path

FILE_PATH = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\12_第2部 第8章 単一責任原則 (SRP) 変更の軸を明確にする設計指針_01.md")

def main():
    text = FILE_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    # (line_number_1_based, insertion_text)
    # qualiry_check reports line of "#### ..."
    insertions = [
        (110, "**現状のコード:** 以下は、SRPに違反している典型的な構造体定義です。すべてのフィールドがフラットに並べられています。\n"),
        (478, "**実行結果:** プログラムは動作しますが、コード内部では責任が混在しています。\n"),
        (486, "**ログ内容:** 出力されたログファイルの内容です。整形ロジックと出力ロジックが密結合しているため、どちらかの変更が他方に影響します。\n")
    ]

    insertions.sort(key=lambda x: x[0], reverse=True)

    for line_num, text_to_insert in insertions:
        index = line_num - 1
        # Safety check
        # verification is harder because line content varies, checking rough match
        line_content = lines[index]
        if "####" not in line_content:
             print(f"Warning: Line {line_num} does not look like a header. Found: '{line_content}'")
        
        lines.insert(index, text_to_insert)
        print(f"Inserted at line {line_num}")

    new_text = "\n".join(lines)
    FILE_PATH.write_text(new_text, encoding="utf-8")
    print("Done.")

if __name__ == "__main__":
    main()
