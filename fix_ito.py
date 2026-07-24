import pandas as pd
import re

df = pd.read_csv("D:/BN-BE-EN/bengali_dataset.csv")

def generate_ito_variants(bangla, banglish_str):
    if not isinstance(banglish_str, str) or not isinstance(bangla, str):
        return banglish_str
    
    variants = [v.strip() for v in banglish_str.split(',')]
    new_variants = set(variants)
    
    # Check if 'িত' is in the Bengali word
    if 'িত' in bangla:
        for v in variants:
            # We want to replace 'it' with 'ito' at word boundaries, 
            # e.g. "dwikhondit" -> "dwikhondito", "dwikhondit kora" -> "dwikhondito kora"
            # But we must be careful not to replace inside a word like 'with'. 
            # But 'it' is usually the suffix we are targeting.
            new_v = re.sub(r'it\b', 'ito', v)
            if new_v != v:
                new_variants.add(new_v)
                
    final_variants = variants.copy()
    for nv in sorted(list(new_variants)):
        if nv not in final_variants:
            final_variants.append(nv)
            
    return ", ".join(final_variants)

print("Fixing 'ito' variants...")
df['Banglish'] = df.apply(lambda row: generate_ito_variants(row['Bangla_Word'], row['Banglish']), axis=1)

df.to_csv("D:/BN-BE-EN/bengali_dataset.csv", index=False)
print("Added 'ito' variants successfully!")
