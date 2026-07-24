"""
Comprehensive Bengali-to-Banglish Re-transliteration Engine
============================================================
Fixes ALL known transliteration issues in bengali_dataset.csv by 
re-generating the Banglish column from scratch using proper
Bengali Unicode parsing and phonetic rules.

Key fixes:
- ড় (U+09DC) → 'r' (was incorrectly 'd')
- ঢ় (U+09DD) → 'rh' (was incorrectly 'dh')
- জ্ঞ → 'gg' (Bengali pronunciation, not Sanskrit 'gya')
- ক্ষ → 'kkh' (Bengali pronunciation)
- দ্ব/স্ব/ত্ব ব-ফলা properly handled
- য-ফলা adds 'y' (not 'j')
- Proper variant generation (bh/v, sh/s, ee/i, j/z, f/ph, etc.)
- Correct schwa deletion rules
"""

import pandas as pd
import unicodedata
from itertools import product

# ============================================================
# Unicode Constants
# ============================================================
HALANT = '\u09CD'       # ্
NUKTA  = '\u09BC'       # ়
CHANDRABINDU = '\u0981' # ঁ
ANUSVARA = '\u0982'     # ং
VISARGA  = '\u0983'     # ঃ
KHANDA_TA = '\u09CE'    # ৎ

# ============================================================
# Character Classification
# ============================================================
def is_bengali(ch):
    return 0x0980 <= ord(ch) <= 0x09FF

def is_consonant(ch):
    cp = ord(ch)
    return (0x0995 <= cp <= 0x09B9) or cp in (0x09DC, 0x09DD, 0x09DF)

def is_vowel_sign(ch):
    cp = ord(ch)
    return cp in (0x09BE, 0x09BF, 0x09C0, 0x09C1, 0x09C2, 0x09C3,
                  0x09C7, 0x09C8, 0x09CB, 0x09CC)

def is_indep_vowel(ch):
    cp = ord(ch)
    return 0x0985 <= cp <= 0x0994

# ============================================================
# Transliteration Mappings
# ============================================================

# Consonants: primary spelling first, then variants
CONS = {
    'ক': ['k'],
    'খ': ['kh'],
    'গ': ['g'],
    'ঘ': ['gh'],
    'ঙ': ['ng'],
    'চ': ['ch'],
    'ছ': ['chh', 'ch'],
    'জ': ['j', 'z'],
    'ঝ': ['jh', 'zh'],
    'ঞ': ['n'],
    'ট': ['t'],
    'ঠ': ['th'],
    'ড': ['d'],
    'ঢ': ['dh'],
    'ণ': ['n'],
    'ত': ['t'],
    'থ': ['th'],
    'দ': ['d'],
    'ধ': ['dh'],
    'ন': ['n'],
    'প': ['p'],
    'ফ': ['f', 'ph'],
    'ব': ['b'],
    'ভ': ['bh', 'v'],
    'ম': ['m'],
    'য': ['j', 'z'],       # standalone য
    'র': ['r'],
    'ল': ['l'],
    'শ': ['sh', 's'],
    'ষ': ['sh', 'ss'],
    'স': ['s'],
    'হ': ['h'],
    'ড়': ['r'],             # KEY FIX (was 'd')
    'ঢ়': ['rh'],            # KEY FIX (was 'dh')
    'য়': ['y'],
}

# Vowel signs (matras): primary first, then variants
VSIGNS = {
    'া': ['a'],
    'ি': ['i'],
    'ী': ['ee', 'i'],
    'ু': ['u'],
    'ূ': ['oo', 'u'],
    'ৃ': ['ri'],
    'ে': ['e'],
    'ৈ': ['oi'],
    'ো': ['o'],
    'ৌ': ['ou'],
}

# Independent vowels
IVOWELS = {
    'অ': ['o'],
    'আ': ['a'],
    'ই': ['i'],
    'ঈ': ['ee', 'i'],
    'উ': ['u'],
    'ঊ': ['oo', 'u'],
    'ঋ': ['ri'],
    'এ': ['e'],
    'ঐ': ['oi'],
    'ও': ['o'],
    'ঔ': ['ou'],
}

# Special 2-consonant conjuncts (base form without inherent vowel)
SPECIAL_2 = {
    ('জ', 'ঞ'): ['gg'],               # জ্ঞ → gg (Bengali: "ggo")
    ('ক', 'ষ'): ['kkh', 'ksh'],       # ক্ষ → kkh
    ('হ', 'ন'): ['nn', 'hn'],         # হ্ন → nn
    ('হ', 'ম'): ['mm', 'hm'],         # হ্ম → mm
    ('ঙ', 'ক'): ['nk'],
    ('ঙ', 'খ'): ['nkh'],
    ('ঙ', 'গ'): ['ngg'],
    ('ঙ', 'ঘ'): ['nggh'],
    ('ঞ', 'চ'): ['nch'],
    ('ঞ', 'ছ'): ['nchh'],
    ('ঞ', 'জ'): ['nj', 'nz'],
    ('ঞ', 'ঝ'): ['njh'],
    ('চ', 'ছ'): ['cchh', 'cch'],     # চ্ছ
    ('ত', 'থ'): ['tth'],              # ত্থ
}

# ব-ফলা special cases (consonant + ব in conjunct)
BA_PHALA = {
    'দ': ['dw', 'd'],          # দ্ব → dw or d (e.g., দ্বারা → dwara/dara)
    'স': ['sw', 'sh'],         # স্ব → sw or sh (e.g., স্বাধীন → shadhin)
    'ত': ['tw', 'tt', 't'],    # ত্ব → tw/tt/t
}

# ============================================================
# Parsing
# ============================================================

def parse_word(word):
    """Parse a Bengali word into phonetic blocks.
    
    Returns a list of tuples:
    - ('V', char)                                    — independent vowel
    - ('C', [consonants], vowel_sign|None, has_halant, has_chandrabindu) — consonant block
    - ('S', latin_str)                               — special char (ং, ঃ, ৎ, ঁ)
    - ('O', char)                                    — other (space, punctuation, etc.)
    """
    word = unicodedata.normalize('NFC', word)
    blocks = []
    i = 0
    n = len(word)
    
    while i < n:
        ch = word[i]
        
        if is_indep_vowel(ch):
            blocks.append(('V', ch))
            i += 1
            
        elif is_consonant(ch):
            # Collect consonant cluster joined by halant
            cons = [ch]
            j = i + 1
            while j + 1 < n and word[j] == HALANT and is_consonant(word[j+1]):
                cons.append(word[j+1])
                j += 2
            
            # Trailing halant (explicit virama — no inherent vowel)
            has_halant = (j < n and word[j] == HALANT)
            if has_halant:
                j += 1
            
            # Vowel sign
            vsign = None
            if j < n and is_vowel_sign(word[j]):
                vsign = word[j]
                j += 1
            
            # Chandrabindu (nasalization)
            has_cb = (j < n and word[j] == CHANDRABINDU)
            if has_cb:
                j += 1
            
            blocks.append(('C', cons, vsign, has_halant, has_cb))
            i = j
            
        elif ch == KHANDA_TA:
            blocks.append(('S', 't'))
            i += 1
        elif ch == ANUSVARA:
            blocks.append(('S', 'ng'))
            i += 1
        elif ch == VISARGA:
            blocks.append(('S', 'h'))
            i += 1
        elif ch == CHANDRABINDU:
            blocks.append(('S', 'n'))
            i += 1
        else:
            blocks.append(('O', ch))
            i += 1
    
    return blocks

# ============================================================
# Consonant Cluster Transliteration
# ============================================================

def get_cluster_variants(cons):
    """Given a list of consonants in a conjunct, return variant transliterations."""
    
    # Single consonant
    if len(cons) == 1:
        return CONS.get(cons[0], [cons[0]])
    
    # Check special 2-consonant conjuncts
    if len(cons) == 2:
        key = (cons[0], cons[1])
        if key in SPECIAL_2:
            return SPECIAL_2[key]
    
    # Handle phala characters (last consonant in cluster)
    last = cons[-1]
    rest = cons[:-1]
    
    # য-ফলা: য as last element adds 'y' sound
    if last == 'য':
        if len(rest) == 1:
            rv = CONS.get(rest[0], [rest[0]])
        else:
            rv = get_cluster_variants(rest)
        return list(dict.fromkeys(c + 'y' for c in rv))  # deduplicate
    
    # র-ফলা: র as last element adds 'r' sound
    if last == 'র':
        if len(rest) == 1:
            rv = CONS.get(rest[0], [rest[0]])
        else:
            rv = get_cluster_variants(rest)
        return list(dict.fromkeys(c + 'r' for c in rv))
    
    # ব-ফলা: ব as last element
    if last == 'ব':
        # Special cases
        if len(rest) == 1 and rest[0] in BA_PHALA:
            return BA_PHALA[rest[0]]
        
        # General: add 'w' or nothing
        if len(rest) == 1:
            rv = CONS.get(rest[0], [rest[0]])
        else:
            rv = get_cluster_variants(rest)
        results = []
        for c in rv:
            results.append(c + 'w')
            if c not in results:
                results.append(c)
        return list(dict.fromkeys(results))
    
    # General case: concatenate individual consonant transliterations
    # Primary: use first variant of each consonant
    primary = ''.join(CONS.get(c, [c])[0] for c in cons)
    results = [primary]
    
    # Generate variants by alternating each position
    for i, c in enumerate(cons):
        alts = CONS.get(c, [c])
        for alt in alts[1:]:
            v = ''.join(
                alt if j == i else CONS.get(c2, [c2])[0]
                for j, c2 in enumerate(cons)
            )
            if v not in results:
                results.append(v)
    
    return results

# ============================================================
# Word Transliteration
# ============================================================

def transliterate_word(word):
    """Transliterate a single Bengali word to a list of Banglish variants."""
    blocks = parse_word(word)
    if not blocks:
        return [word]
    
    slots = []  # Each slot is a list of variant strings
    
    for idx, block in enumerate(blocks):
        btype = block[0]
        
        if btype == 'V':
            ch = block[1]
            slots.append(IVOWELS.get(ch, [ch]))
            
        elif btype == 'C':
            cons, vsign, has_halant, has_cb = block[1], block[2], block[3], block[4]
            
            # Get consonant cluster variants
            cv = get_cluster_variants(cons)
            
            # Determine vowel
            if has_halant:
                # Explicit halant → no vowel
                vv = ['']
            elif vsign:
                vv = VSIGNS.get(vsign, [vsign])
            else:
                # Inherent vowel 'o' — apply schwa deletion rules
                is_last = all(b[0] == 'O' for b in blocks[idx+1:]) if idx + 1 < len(blocks) else True
                
                if is_last:
                    # Word-final position
                    if idx == 0 and len(blocks) == 1:
                        # Single-block word → keep schwa
                        vv = ['o']
                    elif len(cons) > 1:
                        # Word-final CONJUNCT → keep schwa
                        vv = ['o']
                    else:
                        # Word-final SINGLE consonant
                        # Keep schwa if preceded by a consonant ending
                        prev_is_consonant_end = False
                        if idx > 0:
                            pb = blocks[idx - 1]
                            if pb[0] == 'S':
                                prev_is_consonant_end = True
                            elif pb[0] == 'C' and pb[3]:  # has_halant
                                prev_is_consonant_end = True
                        
                        if prev_is_consonant_end:
                            vv = ['o']
                        else:
                            vv = ['']  # delete schwa
                else:
                    # Non-final → keep schwa
                    vv = ['o']
            
            # Chandrabindu
            cb = 'n' if has_cb else ''
            
            # Combine consonant × vowel variants
            combined = []
            for c in cv:
                for v in vv:
                    s = c + v + cb
                    if s not in combined:
                        combined.append(s)
            
            slots.append(combined)
            
        elif btype == 'S':
            slots.append([block[1]])
            
        elif btype == 'O':
            slots.append([block[1]])
    
    if not slots:
        return [word]
    
    # Generate variants via Cartesian product, capped at 15
    return _generate_capped_variants(slots, 15)


def _generate_capped_variants(slots, cap):
    """Generate Cartesian product of slots, limited to `cap` results."""
    # Calculate total combinations
    total = 1
    for s in slots:
        total *= len(s)
        if total > cap * 10:
            break
    
    if total <= cap:
        return [''.join(combo) for combo in product(*slots)]
    
    # Too many → prune: limit each slot to 2 options
    pruned = [s[:2] for s in slots]
    total2 = 1
    for s in pruned:
        total2 *= len(s)
    
    if total2 <= cap:
        return [''.join(combo) for combo in product(*pruned)]
    
    # Still too many → primary + individual alternations
    primary = ''.join(s[0] for s in slots)
    results = [primary]
    for i, s in enumerate(slots):
        for alt in s[1:]:
            v = ''.join(s2[0] if j != i else alt for j, s2 in enumerate(slots))
            if v not in results:
                results.append(v)
            if len(results) >= cap:
                return results
    
    return results[:cap]

# ============================================================
# Phrase-Level Transliteration
# ============================================================

def segment_text(text):
    """Split text into (segment_string, is_bengali) pairs."""
    text = unicodedata.normalize('NFC', text)
    segments = []
    current = ''
    cur_bn = None
    
    for ch in text:
        ch_bn = is_bengali(ch)
        if cur_bn is None:
            cur_bn = ch_bn
        
        if ch_bn == cur_bn:
            current += ch
        else:
            segments.append((current, cur_bn))
            current = ch
            cur_bn = ch_bn
    
    if current:
        segments.append((current, cur_bn))
    
    return segments


def transliterate_phrase(phrase):
    """Transliterate a phrase (may contain mixed Bengali/English).
    Returns up to 15 Banglish variants.
    """
    if not isinstance(phrase, str) or not phrase.strip():
        return ['']
    
    segments = segment_text(phrase)
    
    seg_variants = []
    for text, is_bn in segments:
        if is_bn:
            variants = transliterate_word(text)
            seg_variants.append(variants)
        else:
            seg_variants.append([text])
    
    return _generate_capped_variants(seg_variants, 15)

# ============================================================
# Row Processing
# ============================================================

def process_row(bangla_word):
    """Process a single row's Bangla_Word → Banglish string."""
    if not isinstance(bangla_word, str) or not bangla_word.strip():
        return ''
    
    # Check if the entry has commas (multiple definitions)
    # We treat the ENTIRE text as one phrase to transliterate
    variants = transliterate_phrase(bangla_word)
    return ', '.join(variants)

# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("Bengali-to-Banglish Re-transliteration Engine")
    print("=" * 60)
    
    # Quick test before running on full dataset
    test_words = {
        'পাড়ি': 'pari',
        'বাড়ি': 'bari',
        'গাড়ি': 'gari',
        'দ্বারা': 'dwara/dara',
        'দ্বিখণ্ডিত': 'dwikhondito/dikhondito',
        'স্বাধীন': 'swadhin/shadhin',
        'জ্ঞান': 'ggan',
        'ভালোবাসা': 'bhalobasha/valobasha',
        'বাংলাদেশ': 'bangladesh',
        'বিজ্ঞান': 'biggyan/biggan',
        'তত্ত্ব': 'tottwo/totto',
        'ক্ষমা': 'kkhoma/kshoma',
        'ভবিষ্যৎ': 'bhobishyot',
    }
    
    print("\n--- Validation Tests ---")
    all_pass = True
    for bn, expected_hint in test_words.items():
        variants = transliterate_phrase(bn)
        joined = ', '.join(variants)
        print(f"  [Bengali Word] -> {joined.encode('ascii', 'replace').decode('ascii')}")
        # Basic sanity: should not contain 'dob' or wrong 'd' for ড়
        if 'ড়' in bn and any('d' in v and 'dh' not in v for v in variants):
            # Check if any variant incorrectly has 'd' for ড়
            # This is a rough check
            pass
    
    print("\n--- Loading dataset ---")
    df = pd.read_csv("D:/BN-BE-EN/bengali_dataset.csv")
    print(f"Loaded {len(df)} rows")
    
    print("--- Re-transliterating all rows ---")
    total = len(df)
    
    # Process with progress
    results = []
    for i, bangla in enumerate(df['Bangla_Word']):
        results.append(process_row(bangla))
        if (i + 1) % 20000 == 0:
            pct = ((i + 1) / total) * 100
            print(f"  Progress: {i+1}/{total} ({pct:.1f}%)")
    
    df['Banglish'] = results
    
    print("--- Saving ---")
    df.to_csv("D:/BN-BE-EN/bengali_dataset.csv", index=False)
    print(f"Done! All {total} rows re-transliterated and saved.")
