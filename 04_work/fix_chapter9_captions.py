import re

# ファイルを読み込む
filepath = r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\13_第2部 第9章 開放閉鎖原則（OCP）：拡張のために開き、修正に対して閉じる_01.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# パターン: **ファイル名**: `filename.h` または `filename.c` の後に続く ```c
# これを見つけて、```c の直前に #### filename を挿入

# まず、**ファイル名**: `xxx.h` または `xxx.c` のパターンを探す
pattern = r'\*\*ファイル名\*\*:\s*`([a-z_]+\.[ch])`'

lines = content.split('\n')
result_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    result_lines.append(line)
    
    # **ファイル名**: `xxx.h` のパターンにマッチするか確認
    match = re.search(pattern, line)
    if match:
        filename = match.group(1)  # idevice.h, serial_device.c など
        
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

print(f"完了: Chapter 9にコードキャプションを追加しました")
