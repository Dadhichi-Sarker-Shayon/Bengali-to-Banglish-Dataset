import pandas as pd

df = pd.read_csv("D:/BN-BE-EN/bengali_dataset.csv")

with open("D:/BN-BE-EN/audit2.txt", "w", encoding="utf-8") as f:
    # Check weird "dob" variants for দ্ব  
    dob = df[df['Banglish'].str.contains('dob', na=False)].head(10)
    f.write("=== Rows with 'dob' in Banglish (bad দ্ব variants) ===\n")
    for _, row in dob.iterrows():
        f.write(f"  {row['Bangla_Word'][:40]} -> {str(row['Banglish'])[:120]}\n")
    
    # Check "sob" for স্ব
    sob = df[df['Banglish'].str.contains('sob', na=False)].head(10)
    f.write(f"\n=== Rows with 'sob' in Banglish (bad স্ব variants): ===\n")
    for _, row in sob.iterrows():
        f.write(f"  {row['Bangla_Word'][:40]} -> {str(row['Banglish'])[:120]}\n")

    # Check ভ্যানকা → vjanka (should be bh/v handled better)
    f.write(f"\n=== ভ্যানকা row ===\n")
    r = df[df['Bangla_Word'].str.contains('ভ্যানকা', na=False)]
    for _, row in r.iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])}\n")

    # Check শরীয়া → shriya (missing 'o' in middle?)
    f.write(f"\n=== শরীয়া row ===\n")
    r = df[df['Bangla_Word'] == 'শরীয়া']
    for _, row in r.iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])}\n")

    # Check ইস্যুকে → isjuke (য in conjunct handled wrong?)
    f.write(f"\n=== ইস্যুকে row ===\n")
    r = df[df['Bangla_Word'] == 'ইস্যুকে']
    for _, row in r.iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])}\n")

    # Check বিস্ফোরণের → bisforner (missing some sounds)
    f.write(f"\n=== বিস্ফোরণের row ===\n")
    r = df[df['Bangla_Word'] == 'বিস্ফোরণের']
    for _, row in r.iterrows():
        f.write(f"  {row['Bangla_Word']} -> {str(row['Banglish'])}\n")

    # Check words with ড় that still have 'd' in Banglish  
    f.write(f"\n=== ড় words that still have wrong 'd' transliteration ===\n")
    rra = df[df['Bangla_Word'].str.contains('ড়', na=False)]
    # Check গাড়ি
    g = df[df['Bangla_Word'] == 'গাড়ি']
    for _, row in g.iterrows():
        f.write(f"  গাড়ি -> {str(row['Banglish'])}\n")
    # Check বাড়ি 
    g = df[df['Bangla_Word'] == 'বাড়ি']
    for _, row in g.iterrows():
        f.write(f"  বাড়ি -> {str(row['Banglish'])}\n")
    # Check তাড়া
    g = df[df['Bangla_Word'] == 'তাড়া']
    for _, row in g.iterrows():
        f.write(f"  তাড়া -> {str(row['Banglish'])}\n")
    # Check পাড়ি
    g = df[df['Bangla_Word'] == 'পাড়ি']
    for _, row in g.iterrows():
        f.write(f"  পাড়ি -> {str(row['Banglish'])}\n")

print("Audit 2 complete!")
