from pathlib import Path

FILE_PATH = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\12_第2部 第8章 単一責任原則 (SRP) 変更の軸を明確にする設計指針_01.md")

def main():
    text = FILE_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    # (line_number_1_based, insertion_text)
    # Note: These line numbers are based on the file content observed in previous view_file steps.
    # Inserting text will shift subsequent lines, so we must sort descending.
    
    insertions = [
        # Before #### logger.h
        (634, "### logger.h\n\n**責務の委譲:** フォーマッターとライターを調整し、ログ出力プロセス全体を制御します。\n\n"), 
        
        # Before #### main.c
        (667, "### main.c\n\n**クライアントコード:** 詳細なロジックを知ることなく、高レベルなAPIを利用します。\n\n"),
        
        # Before #### 実行結果
        (686, "**実行結果:** 内部構造は大きく変わりましたが、外部からの振る舞い（ログ出力）は以前と同じであり、機能が維持されていることがわかります。\n\n"),
        
        # Before #### app.log
        (694, "**ログ内容:** 出力結果も以前と完全に同一です。これがリファクタリング（振る舞いを変えずに内部構造を改善する）の成功証拠です。\n\n")
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
