import pandas as pd
df = pd.read_csv("D:/BN-BE-EN/bengali_dataset.csv")

padi = df[df['Banglish'].str.contains('padi', na=False)].head(15)

with open("D:/BN-BE-EN/output3.txt", "w", encoding="utf-8") as f:
    f.write("Rows with padi:\n")
    for i, row in padi.iterrows():
        f.write(f"{row['Bangla_Word']} -> {row['Banglish'][:70]}\n")
