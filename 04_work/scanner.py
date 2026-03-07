import os
import re

TARGET_DIR = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
OUTPUT_FILE = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\04_work\scan_report2.md"

first_appearance_terms = [
    "SDP", "バッファのフラッシュ", "DRY原則", "valgrind", "包含", "ガベージコレクション", "Brotli", "Zstd"
]
bad_terms = ["螺旋", "らせん", "悪臭", "コードの臭い", "Code Smell", "コードの不吉な臭い"]
pointer_terms = ["self", "context"]
ng_patterns = ["（悪い例）", "（良い例）", "（対策）", "（代替手段）", "（解決策）", "対策：", "理由：", "の例を示します。", "以下のコードを見てください。"]

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"Dir not found: {TARGET_DIR}")
        return

    files = sorted([f for f in os.listdir(TARGET_DIR) if f.endswith('.md')])
    
    first_found = set()
    report = []
    
    for filename in files:
        filepath = os.path.join(TARGET_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        file_report = {"first_terms": [], "bad_terms": [], "pointers": [], "ng_patterns": []}
        
        for i, line in enumerate(lines):
            for term in first_appearance_terms:
                if term not in first_found and term in line:
                    first_found.add(term)
                    file_report["first_terms"].append(f"Line {i+1}: {term}")
            
            for term in bad_terms:
                if term in line:
                    file_report["bad_terms"].append(f"Line {i+1}: {term} -> {line.strip()}")
            
            for term in pointer_terms:
                if re.search(r'\b' + term + r'\b', line):
                    file_report["pointers"].append(f"Line {i+1}: {term}")
                    
            for term in ng_patterns:
                if term in line:
                    file_report["ng_patterns"].append(f"Line {i+1}: {term} -> {line.strip()}")
                    
        if any(file_report.values()):
            report.append(f"## {filename}")
            for k, v in file_report.items():
                if v:
                    report.append(f"### {k}")
                    report.extend(v)
            report.append("")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print("Scan 2 complete.")

if __name__ == "__main__":
    main()
