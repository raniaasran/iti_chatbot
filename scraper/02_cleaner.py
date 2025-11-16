# stage 2: Cleaning
import pandas as pd
import re

df = pd.read_csv("data/iti_full_website_data.csv")
df.dropna(subset=["content"], inplace=True)

def clean_text(text):
    if not isinstance(text, str):
        return ""

    t = text

    t = re.sub(r".*@iti\.gov\.eg.*(Home|About|Services|News)", " ", t, flags=re.IGNORECASE)    # 1) delete links 
    t = re.sub(r"http\S+|www\.\S+", " ", t)

    # 2) delete HTML if exists
    t = re.sub(r"<[^>]+>", " ", t)

    # 3) delete noise (not information!)
    nav_patterns = [
        r"Home\b", r"About ITI\b", r"Services\b", r"Branches\b", r"News\b",
        r"Programs\b", r"Post Graduates\b", r"Under Graduates\b",
        r"Tech-Business\b", r"Tech Ambassadors\b", r"Juniors\b",
        r"KEEP IN TOUCH", r"QUICK LINKS", r"Follow us",
        r"Terms of Use", r"Privacy Policy",
        r"Subscribe", r"Read more",
        r"Previous News", r"Next News",
        r"All rights reserved", r"©.*?\d{4}"
    ]
    for pat in nav_patterns:
        t = re.sub(pat, " ", t, flags=re.IGNORECASE)

    # 4) remove weird symbols 
    t = re.sub(r"[•\u2022\u25CF\u25A0]", " ", t)

    # 5) remove spaces repetitions 
    t = re.sub(r"\s{2,}", " ", t).strip()

    return t

df["clean"] = df["content"].apply(clean_text)

# 6) remove empty rows
df = df[df["clean"].str.len() > 10]

# 7) remove repetitions
df.drop_duplicates(subset=["clean"], inplace=True)

df.to_csv("data/iti_sample_clean.csv", index=False)
print("after clean:", len(df))
df.sample(10)
