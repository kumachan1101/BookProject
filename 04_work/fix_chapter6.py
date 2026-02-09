from pathlib import Path

FILE_PATH = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\08_第1部 第6章 エラーハンドリングパターン - 堅牢な契約_01.md")

def main():
    text = FILE_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    # (line_number_1_based, insertion_text)
    # quality_check.py reports line number of "#### ..."
    # We want to insert BEFORE that line.
    insertions = [
        (234, "**実行結果:** 異なるエラーコードが返された場合でも、その範囲（-1000番台か-2000番台か）によって、どのモジュールで障害が発生したかを正しく判別できています。\n"),
        (423, "**実行結果:** 入力エラーの場合は詳細メッセージが出力されますが、ハンドル自体はNULLであることが保証されています。これにより、呼び出し側での誤用を防げます。\n"),
        (676, "**実行結果:** file_open 失敗時に、サイドチャネル（file_get_last_error）を通じて的確なエラー理由（ファイル不在、権限不足など）が伝わっていることがわかります。\n"),
        (901, "**実行結果:** 下位のストレージ層で発生したI/Oエラー（-2001）が、ユーザー層によって抽象的な保存失敗エラー（-1021）に変換され、アプリケーション層に通知されています。\n")
    ]

    # Sort in descending order to avoid index shift
    insertions.sort(key=lambda x: x[0], reverse=True)

    for line_num, text_to_insert in insertions:
        index = line_num - 1 # Convert to 0-based
        # Check if the line is indeed what we expect (safety check)
        if "#### 実行結果" not in lines[index]:
             print(f"Warning: Line {line_num} does not contain '#### 実行結果'. Found: '{lines[index]}'")
             # continue # or proceed anyway if strictness is not required, but strict is better
        
        lines.insert(index, text_to_insert)
        print(f"Inserted at line {line_num}")

    new_text = "\n".join(lines)
    FILE_PATH.write_text(new_text, encoding="utf-8")
    print("Done.")

if __name__ == "__main__":
    main()
