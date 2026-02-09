import re

def add_code_captions(filepath):
    """指定されたファイルにコードキャプションを追加"""
    # ファイルを読み込む
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
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
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(modified_content)
    
    return filepath

# Chapter 7とChapter 9を処理
base_path = r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別'

files = [
    r'09_第1部 第7章 メモリ管理パターン - 責任の明確化_01.md',
    r'13_第2部 第9章 開放閉鎖原則（OCP）：拡張のために開き、修正に対して閉じる_01.md'
]

for filename in files:
    filepath = f'{base_path}\\{filename}'
    add_code_captions(filepath)
    print(f'完了: {filename}')

print('\nすべてのファイルにコードキャプションを追加しました')
