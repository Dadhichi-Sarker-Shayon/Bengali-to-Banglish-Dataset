# 📚 Massive Bengali-English-Banglish Dictionary Dataset

![Dataset Size](https://img.shields.io/badge/Size-206%2C926%20Words-brightgreen)
![Language](https://img.shields.io/badge/Language-Bengali%20%7C%20English%20%7C%20Banglish-blue)
![Format](https://img.shields.io/badge/Format-CSV-orange)

A comprehensive, meticulously curated, and linguistically accurate dictionary dataset containing **206,926 unique Bengali words**, their English meanings, and up to 15 conversational Banglish (Bengali written in Latin script) variants per word. 

This dataset is perfect for NLP tasks, machine translation, transliteration models, and language learning applications involving Bengali.

## 📑 Table of Contents
1. [Dataset Overview](#dataset-overview)
2. [Historical Context of Bengali and Banglish](#historical-context-of-bengali-and-banglish)
3. [The Linguistic Rules of Schwa Deletion](#the-linguistic-rules-of-schwa-deletion)
4. [Computational Challenges in Transliteration](#computational-challenges-in-transliteration)
5. [Dataset Architecture & Deep Dive](#dataset-architecture--deep-dive)
6. [Exhaustive Usage Examples](#exhaustive-usage-examples)
7. [FAQ](#faq)
8. [Sources & Citations](#sources--citations)
9. [License](#license)

---

## 1. Dataset Overview

- **Total Rows (Unique Bangla Words):** 206,926
- **Columns:** 3 (`Bangla_Word`, `English_Meaning`, `Banglish`)
- **Rich Banglish Variations:** Generates up to 15 comma-separated conversational spelling variations for the Banglish representation of each word.

---

## 2. Historical Context of Bengali and Banglish

### The Bengali Language
Bengali (or Bangla) is an Indo-Aryan language spoken predominantly in South Asia. With over 230 million native speakers, it is the seventh most spoken language in the world by total number of native speakers. It is the national and official language of Bangladesh and one of the 22 scheduled languages of India, predominantly spoken in the states of West Bengal, Tripura, and Assam. 

### The Rise of Banglish
With the explosion of internet penetration and smartphone usage in the early 2000s, typing in native Bengali script was notoriously difficult due to a lack of standardized, user-friendly mobile keyboards. As a result, users adapted by typing Bengali phonetically using the standard English QWERTY keyboard. This phenomenon, known as **Banglish** (a portmanteau of Bangla and English), became the de facto standard for SMS texting, social media messaging, and informal digital communication.

Even though sophisticated Bengali keyboards (like Avro and Ridmik) exist today, millions of users still prefer typing in Banglish due to typing speed and habit. Consequently, a massive, undocumented parallel corpus of Banglish exists online, posing severe challenges for modern NLP models that are exclusively trained on standard Bengali script.

---

## 3. The Linguistic Rules of Schwa Deletion

One of the most complex aspects of Bengali phonology is the **inherent vowel** (or schwa). In the Bengali abugida script, every consonant letter inherently carries a vowel sound, typically pronounced as an "o" (ɔ/o). For instance, the letter `ক` is pronounced `kɔ`. 

### The Phenomenon
When native speakers speak Bengali, they frequently drop this inherent vowel at the end of syllables and words. This is known as **schwa deletion**. 
However, because standard transliteration libraries parse Unicode mechanically, they often retain these dropped vowels, leading to robotic, unnatural Romanization.

**Example of the Problem:**
- Word: `বিকারগ্রস্ত` (deranged)
- Mechanical Transliteration: `bikarogrosto`
- Actual Pronunciation & Banglish: `bikargrosto`

### Our Solution
To solve this, our dataset curation pipeline features a state-of-the-art Schwa Deletion Algorithm. The algorithm looks for specific linguistic triggers:
1. **Suffix Matching:** It scans for over 30 compound suffixes (e.g., `grosto`, `jukto`, `potro`, `shil`, `kari`).
2. **Syllable Boundaries:** It uses regex heuristics to identify consonant-vowel-consonant (CVC) closures, surgically removing the 'o' when it naturally closes a syllable (e.g., changing `torokari` to `torkari`).

---

## 4. Computational Challenges in Transliteration

Beyond schwa deletion, building this dataset required solving several deep computational challenges:

### 4.1 Conjunct Consonants (Juktakkhor)
Bengali features complex conjuncts where two or more consonants merge into a single typographic ligature (e.g., `ষ` + `ট` = `ষ্ট`). In Unicode, these are joined by a invisible character called a Halant (0x09CD). Our engine meticulously parses the Unicode sequence, groups these blocks, and ensures that the inherent vowel is suppressed for all but the final consonant in the block.

### 4.2 Orthographic Variance
Banglish is wildly unstandardized. Depending on dialect and typing speed, users interchange letters constantly:
- `ভ` is typed as `bh` or `v` (e.g., `bhalo` vs `valo`).
- `শ`, `ষ`, and `স` are interchangeably typed as `sh` or `s`.
- Long and short vowels (`ঈ` vs `ই`) are collapsed to `i` or `ee`.

Our engine intelligently generates a combinatorial matrix of up to 15 valid conversational spelling variations for every single word in the dataset, capturing this messy reality beautifully.

---

## 5. Dataset Architecture & Deep Dive

### Data Structure

| Column Name | Description | Example |
| :--- | :--- | :--- |
| `Bangla_Word` | The word in Bengali script (properly sorted). | বিকারগ্রস্ত |
| `English_Meaning` | The meaning of the word in English. | deranged, insane |
| `Banglish` | Up to 15 comma-separated transliterations. | bikargrosto, bikargrosta, vikargrosto |

### Deep Dive: The 'v' vs 'bh' Mapping Matrix

| Original | Standard Transliteration | Generated Conversational Variants |
| :--- | :--- | :--- |
| ভালোবাসা | bhalobasha | valobasha, bhalobasa, valobasa |
| অভাব | obhab | ovab |
| ভবিষ্যৎ | bhobishyot | vobishyot, bhobisyot, vobisyot |

---

## 6. Exhaustive Usage Examples

### Python (Pandas)
```python
import pandas as pd

# Load the massive dataset
df = pd.read_csv('bengali_dataset.csv')

# Search for a word
search_term = "আকাশ"
result = df[df['Bangla_Word'] == search_term]
print(f"Variants for {search_term}: {result['Banglish'].values[0]}")
```

### HuggingFace Datasets
```python
from datasets import load_dataset

dataset = load_dataset('csv', data_files='bengali_dataset.csv')
print(dataset['train'][0])
```

### PyTorch Dataloader
```python
import pandas as pd
from torch.utils.data import Dataset, DataLoader

class BanglishDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        return {
            'bengali': row['Bangla_Word'],
            'english': row['English_Meaning'],
            'banglish': row['Banglish'].split(', ')
        }

loader = DataLoader(BanglishDataset('bengali_dataset.csv'), batch_size=32)
```

---

## 7. FAQ

**Q: Why are there multiple Banglish variants for a single word?**
A: Because Banglish is unstandardized, real users type the same word in different ways. Providing variants helps ML models generalize better to real-world messy text.

**Q: Is the dataset sorted?**
A: Yes! Unlike naive Unicode sorts, this dataset is sorted strictly according to the actual Bengali linguistic dictionary order (Vowels first, Consonants second).

**Q: Can I use this for commercial purposes?**
A: Yes, it is licensed under the MIT License.

---

## 8. Sources & Citations
- **MinhasKamal's BengaliDictionary:** A foundational source of Bengali-English word pairs.
- **SKNahin's Datasets:** Contributions for extended vocabulary.
- **ProjectShobdo:** For deep morphological roots and lexical structures.
- **Gold Mapping CSV:** A proprietary mapping algorithm used to refine the phonetic rules.

## 9. License
Distributed under the MIT License.
