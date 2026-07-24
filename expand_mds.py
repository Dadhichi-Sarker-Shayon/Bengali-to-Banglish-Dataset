import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

readme_content = """# 📚 Massive Bengali-English-Banglish Dictionary Dataset

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
"""

hf_content = """---
language:
- bn
- en
license: mit
size_categories:
- 100K<n<1M
task_categories:
- translation
- text-generation
- token-classification
tags:
- bengali
- banglish
- dictionary
- transliteration
dataset_info:
  features:
  - name: Bangla_Word
    dtype: string
  - name: English_Meaning
    dtype: string
  - name: Banglish
    dtype: string
  splits:
  - name: train
    num_bytes: ~25000000
    num_examples: 206926
---

# Dataset Card for Massive Bengali-English-Banglish Dictionary

## Dataset Description

This is a comprehensive, massive-scale dictionary dataset containing **206,926 unique Bengali words**, their corresponding English meanings, and up to 15 conversational Banglish (Latin script) transliteration variants per word.

## Intended Uses & Out of Scope Use

### Intended Use Cases
- **Machine Translation:** Training neural machine translation (NMT) models to translate informal Banglish text into English.
- **Transliteration Engines:** Building highly accurate seq2seq models that convert Romanized Bengali back into proper Eastern Nagari script for display or further processing.
- **Spell Correction & Normalization:** Using the combinatorial variants to train autocorrect models that standardize messy Banglish typing.
- **Cross-Lingual Information Retrieval:** Building search engines that allow users to search for Bengali content using English queries or Banglish phonetic spellings.

### Out of Scope Uses
- **Grammar Checking:** This is a dictionary of lexical terms and phrases, not a corpus of full grammatical sentences. It should not be used to train grammar parsers.
- **Sentiment Analysis:** The dataset lacks sentiment labels.

## Dataset Distribution and Structure

The dataset contains exactly 206,926 instances structured identically across three columns. The words range from high-frequency conversational vocabulary to deep, formal morphological derivatives. 

```json
{
  "Bangla_Word": "বিকারগ্রস্ত",
  "English_Meaning": "diseased, deranged, insane",
  "Banglish": "bikargrosto, bikargrosta, vikargrosto, vikargrosta"
}
```

## Detailed Preprocessing & Curation

### Curation Rationale
While standard Bengali-English dictionaries exist, there is a gaping void in resources that map proper Bengali to everyday, conversational Banglish variations. This dataset bridges that gap by applying rigorous linguistic algorithms to generate accurate, human-like transliterations.

### Linguistic Processing & Schwa Deletion
The preprocessing pipeline resolves the notoriously difficult issue of Bengali schwa deletion. It intelligently drops the inherent 'o' vowel when it closes a syllable (e.g., transliterating `বিকারগ্রস্ত` as `bikargrosto` rather than the robotic `bikarogrosto`).

### Phonetic Variance Mapping
The pipeline also simulates common human typing errors and phonetic substitutions:
- Exchanging `bh` and `v`.
- Exchanging `sh`, `s`, and `ss`.
- Exchanging `i` and `ee`.

## Ethical Considerations & Biases

### Biases
The English meanings provided are sourced from historical dictionary data and may occasionally reflect archaic or culturally situated definitions. Furthermore, the Banglish variants generated prioritize standard Bangladeshi typing conventions; regional dialects (such as those specific to rural West Bengal or Assam) may have slightly different phonetic transliteration rules not fully captured here.

### Ethical Considerations
This dataset contains open-source dictionary data. While aggressive filtering was performed, it is possible that offensive or derogatory terms exist within the 206k rows, as is common in any comprehensive language dictionary. Researchers building user-facing systems should apply standard safety filtering.

## Benchmark Potentials
This dataset is positioned to become the gold-standard benchmark for the **Banglish-to-Bengali Transliteration Task**. Researchers are encouraged to split the dataset and test seq2seq models on their ability to predict the exact `Bangla_Word` given any of the variants in the `Banglish` column.
"""

kaggle_content = """# Massive Bengali-English-Banglish Dictionary

## Detailed Context & The Banglish Phenomenon
With over 230 million native speakers, Bengali is one of the most spoken languages in the world. However, on the internet, in text messaging, and across social media, native speakers frequently use **Banglish**—Bengali written using the English alphabet. 

Building modern NLP models for the Bengali language requires understanding not just the native Eastern Nagari script, but how it is colloquially and messily typed in Latin characters. Because there is no central authority on how to spell Bengali words with English letters, native speakers exhibit wild orthographic variance.

This dataset bridges that gap by providing a massive, high-quality mapping of over **206,926 Bengali words** to both their English meanings and their myriad Banglish transliterations.

## Exhaustive Column Deep Dive

### 1. `Bangla_Word`
The original, clean word in Bengali script. 
- **Scale:** 206,926 perfectly unique rows.
- **Sorting:** The entire dataset is sorted strictly according to proper Bengali dictionary sorting rules (Vowels first, then Consonants), not mechanical Unicode points.

### 2. `English_Meaning`
The English translation or definition of the word. Contains multiple definitions separated by commas.

### 3. `Banglish`
A comma-separated string containing up to 15 different ways native speakers might spell the word in Latin script.
- **Algorithmic Schwa Deletion:** We applied advanced morphological heuristics to delete the inherent 'o' (schwa) from closed syllables, guaranteeing the transliterations sound like actual humans speaking, rather than robotic Unicode parsers.
- **Phonetic Combinations:** Includes permutations for common key swaps (e.g., `v` vs `bh`, `s` vs `sh`).

## Starter Ideas & Exploratory Data Analysis (EDA)

Here are several ways you can jumpstart your work on Kaggle using this massive dataset:

### 1. The Banglish Autocorrect Engine
**Task:** Build a model that takes a messy, misspelled Banglish word and standardizes it, or predicts the correct original Bengali word.
**Approach:** Flatten the dataset so every Banglish variant is a feature predicting the `Bangla_Word` label. Train a character-level sequence-to-sequence model (like a Transformer or BiLSTM).

### 2. EDA: Phonetic Variance Clustering
**Task:** Analyze which Bengali characters generate the highest number of Banglish variants. 
**Approach:** Count the number of commas in the `Banglish` column for each row. Use NLP tokenization to identify which Bengali syllables (e.g., `ভ`, `শ`) are most responsible for generating multiple spelling variants. Plot the variance distribution!

### 3. Cross-Lingual Semantic Search
**Task:** Build a search engine that understands Banglish queries.
**Approach:** Use TF-IDF or Word2Vec embeddings on the `English_Meaning` column, and map the user's Banglish input to retrieve the English definition or the native Bengali word.

## Acknowledgements
This dataset was meticulously crafted by merging and heavily processing data from incredible open-source projects:
- [MinhasKamal / BengaliDictionary](https://github.com/MinhasKamal/BengaliDictionary)
- SKNahin's Datasets
- ProjectShobdo
- Custom Proprietary Gold Mappings

Enjoy exploring the complexities of the Bengali language!
"""

print("Writing massively expanded README.md...")
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("Writing massively expanded HF_Dataset_Card.md...")
with open("HF_Dataset_Card.md", "w", encoding="utf-8") as f:
    f.write(hf_content)

print("Writing massively expanded Kaggle_Dataset_Card.md...")
with open("Kaggle_Dataset_Card.md", "w", encoding="utf-8") as f:
    f.write(kaggle_content)

print("Expanded Markdown files generated successfully!")
