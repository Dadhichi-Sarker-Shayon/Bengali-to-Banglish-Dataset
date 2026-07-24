import pandas as pd

df = pd.read_csv("D:/BN-BE-EN/bengali_dataset.csv")
res = df[df['Bangla_Word'].str.contains('দ্বিখণ্ডিত', na=False)]

with open("D:/BN-BE-EN/debug.txt", "w", encoding="utf-8") as f:
    for _, row in res.iterrows():
        f.write(f"{row['Bangla_Word']} | {row['English_Meaning']} | {row['Banglish']}\n")
