import re

txt_path = "kno_sys_AB_shuf.txt"

with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
    abstracts = [line.strip() for line in f if line.strip()]

# regex: capture preceding word + the keyword (all lowercase now)
pattern = re.compile(r"(\b\w+\b)\s+(knowledge system\w*)")

stopwords = {"the", "and", "of", "a"}

for i, abs_text in enumerate(abstracts, start=1):
    text = abs_text.lower()   # lowercase once here
    matches = pattern.findall(text)
    if matches:
        #print(f"\nAbstract {i}:")
        for prev, kw in matches:
            if prev not in stopwords:
                #print(f"... {prev} {kw} ...")
                print(f"{prev} knowledge system")


