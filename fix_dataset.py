import pandas as pd
import re

df = pd.read_csv("D:/BN-BE-EN/bengali_dataset.csv")

def generate_variants(bangla, banglish_str):
    if not isinstance(banglish_str, str):
        return banglish_str
    
    variants = [v.strip() for v in banglish_str.split(',')]
    new_variants = set(variants)
    
    for variant in variants:
        v = variant
        
        # Word-level specific fixes just in case
        v_specific = re.sub(r'\bdwara\b', 'dara', v)
        v_specific = re.sub(r'\bpadi\b', 'pari', v_specific)
        v_specific = re.sub(r'\bbadi\b', 'bari', v_specific)
        v_specific = re.sub(r'\bgadi\b', 'gari', v_specific)
        if v_specific != v:
            new_variants.add(v_specific)

        # ড়/ঢ় fixes based on Bangla_Word
        if isinstance(bangla, str):
            if 'ড়' in bangla:
                # Replace 'd' with 'r' safely? 
                # Since 'd' could be actual 'd' (দ/ড), we just blindly create a variant replacing 'd' with 'r'
                # but only if 'd' exists. Better is to replace all 'd' with 'r' as a variant.
                new_v = v.replace('d', 'r')
                if new_v != v:
                    new_variants.add(new_v)
            if 'ঢ়' in bangla:
                new_v = v.replace('dh', 'rh').replace('d', 'r')
                if new_v != v:
                    new_variants.add(new_v)
            
            # W-phala fixes (ব-ফলা)
            if 'দ্ব' in bangla:
                new_v = v.replace('dw', 'd')
                if new_v != v:
                    new_variants.add(new_v)
            if 'স্ব' in bangla:
                new_v = v.replace('sw', 's')
                if new_v != v:
                    new_variants.add(new_v)
            if 'ত্ব' in bangla:
                new_v = v.replace('tw', 't')
                if new_v != v:
                    new_variants.add(new_v)
            if 'ম্ব' in bangla or 'ম্ব' in bangla: # mw -> m, actually mbo is m, but let's check
                new_v = v.replace('mw', 'm')
                if new_v != v:
                    new_variants.add(new_v)
            if 'hw' in v:
                new_v = v.replace('hw', 'h')
                if new_v != v:
                    new_variants.add(new_v)
    
    # Preserve original order and append new ones
    final_variants = variants.copy()
    for nv in sorted(list(new_variants)):
        if nv not in final_variants:
            final_variants.append(nv)
            
    return ", ".join(final_variants)

print("Fixing dataset...")
df['Banglish'] = df.apply(lambda row: generate_variants(row['Bangla_Word'], row['Banglish']), axis=1)

output_file = "D:/BN-BE-EN/bengali_dataset.csv"
df.to_csv(output_file, index=False)
print("Dataset successfully saved with new variants!")
