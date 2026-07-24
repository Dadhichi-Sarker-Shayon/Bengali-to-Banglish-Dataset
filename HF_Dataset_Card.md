---
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
