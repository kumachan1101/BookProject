import re

# ファイルを読み込む
with open(r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\08_第1部 第6章 エラーハンドリングパターン - 堅牢な契約_01.md', 'r', encoding='utf-8') as f:
    content = f.read()

# パターン: #### で始まる行でファイル名を含むもの (拡張子 .h, .c を持つもの)
# その後に続く説明文と ```c の間に #### ファイル名 を挿入

# ファイル名パターン: .h または .c で終わる
filename_pattern = r'#### ([a-z_]+\.[ch])(?: \(.*?\))?'

# 全ての #### ファイル名 セクションを見つけて、コードブロックの直前にキャプションを追加
lines = content.split('\n')
result_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    result_lines.append(line)
    
    # #### ファイル名 のパターンにマッチするか確認
    match = re.match(filename_pattern, line)
    if match:
        filename = match.group(1)  # user.h, storage.c など
        
        # 次の ```c を探す
        j = i + 1
        while j < len(lines) and not lines[j].strip().startswith('```c'):
            result_lines.append(lines[j])
            j += 1
        
        # ```c の直前に #### ファイル名 を挿入
        if j < len(lines) and lines[j].strip().startswith('```c'):
            result_lines.append('')  # 空行
            result_lines.append(f'#### {filename}')  # コードキャプション
            # ```c 行は次のイテレーションで追加される
            i = j - 1  # 次のループで ```c 行を処理
    
    i += 1

# 結果を書き込む
modified_content = '\n'.join(result_lines)
with open(r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\08_第1部 第6章 エラーハンドリングパターン - 堅牢な契約_01.md', 'w', encoding='utf-8', newline='') as f:
    f.write(modified_content)

print("完了: コードキャプションを正しく追加しました")
