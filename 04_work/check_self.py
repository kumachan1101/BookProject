import glob, re
import sys

def check():
    md_files = glob.glob('c:/Users/kumac/OneDrive/デスクトップ/antigravity/BookProject/02_章別/*.md')
    for f in md_files:
        content = open(f, encoding='utf-8').read()
        funcs = re.findall(r'(\w+)\s*\([^)]*void\*\s+self[^)]*\)\s*\{(.*?)\}', content, re.DOTALL)
        for name, body in funcs:
            if re.search(r'\bself\b', body):
                print(f"File: {f.split('/')[-1]} | Func: {name}")
                for line in body.split('\n'):
                    if 'self' in line:
                        print('  ', line.strip())

if __name__ == '__main__':
    check()
