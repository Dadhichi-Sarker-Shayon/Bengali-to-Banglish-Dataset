import pandas as pd
import re

df = pd.read_csv("D:/BN-BE-EN/bengali_dataset.csv")

with open("D:/BN-BE-EN/audit.txt", "w", encoding="utf-8") as f:
    # 1. Words with ড় — should be 'r' not 'd'
    rra = df[df['Bangla_Word'].str.contains('ড়', na=False)]
    f.write(f"=== Words with ড় (should use 'r' not 'd'): {len(rra)} rows ===\n")
    for _, row in rra.head(5).iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])[:80]}\n")

    # 2. Words with ঢ় — should be 'rh' not 'dh'
    rha = df[df['Bangla_Word'].str.contains('ঢ়', na=False)]
    f.write(f"\n=== Words with ঢ় (should use 'rh' not 'dh'): {len(rha)} rows ===\n")
    for _, row in rha.head(5).iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])[:80]}\n")

    # 3. Words with দ্ব — 'dw' but should also have 'd' variant, NOT 'dob'
    dwa = df[df['Bangla_Word'].str.contains('দ্ব', na=False)]
    f.write(f"\n=== Words with দ্ব (dw/d variants): {len(dwa)} rows ===\n")
    for _, row in dwa.head(5).iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])[:80]}\n")

    # 4. Words with স্ব — should be 'sw' or 'sh', not 'sob'
    swa = df[df['Bangla_Word'].str.contains('স্ব', na=False)]
    f.write(f"\n=== Words with স্ব (sw/sh variants): {len(swa)} rows ===\n")
    for _, row in swa.head(5).iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])[:80]}\n")

    # 5. Words with জ্ঞ — should be 'ggo' not 'gya'
    gya = df[df['Bangla_Word'].str.contains('জ্ঞ', na=False)]
    f.write(f"\n=== Words with জ্ঞ (should be 'gg'): {len(gya)} rows ===\n")
    for _, row in gya.head(5).iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])[:80]}\n")

    # 6. Words with ক্ষ — should be 'kkho' 
    ksha = df[df['Bangla_Word'].str.contains('ক্ষ', na=False)]
    f.write(f"\n=== Words with ক্ষ (should be 'kkh'): {len(ksha)} rows ===\n")
    for _, row in ksha.head(5).iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])[:80]}\n")

    # 7. Words with ত্ব — should be 'tw'/'tt'
    twa = df[df['Bangla_Word'].str.contains('ত্ব', na=False)]
    f.write(f"\n=== Words with ত্ব: {len(twa)} rows ===\n")
    for _, row in twa.head(5).iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])[:80]}\n")

    # 8. Random sample of 20 rows
    f.write(f"\n=== RANDOM SAMPLE (20 rows) ===\n")
    sample = df.sample(20, random_state=42)
    for _, row in sample.iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])[:100]}\n")

    f.write(f"\n=== TOTAL ROWS: {len(df)} ===\n")

print("Audit complete!")
