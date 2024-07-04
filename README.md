# Evaluating the Multilingual Rhyming capabilities of Open-Source LLMs

In this project, we investigate the phonological capabilities of LLMs by testing whether they are able to discern rhyming and non-rhyming word-pairs in two Germanic languages (Dutch and English). We mine English (CMU-Dict) and Dutch (Celex2) pronunciation dictionaries and construct rhyming datasets for five types of rhymes [Single perfect/Double Perfect/Assonance/Consonance/Alliteration]. We test three open-source LLMs: **Llama2-7b-chat-hf**, **Llama3-8B-Instruct** and **CrystalChat-7b** on the English and Dutch datasets.  Additionally, we test out prompt variation (title/description-level prompts) with the models.

This project was completed under the guidance of Prof. David Mortensen, at LTI, CMU. For more details refer to the [report](https://github.com/Aadit3003/llm-rhyme/blob/85faec464d38443517b90497e032cf2f9bb28e9a/report.pdf) and the slides from my [talk](https://github.com/Aadit3003/llm-rhyme/blob/85faec464d38443517b90497e032cf2f9bb28e9a/talk_slides.pdf)!

## **Results**
English Results (F1 scores) (Title Prompts):
|      Model     | Single Perfect | Double Perfect | Assonance | Consonance | Alliteration |
|:--------------:|:--------------:|:--------------:|:---------:|:----------:|:------------:|
|   Llama-2-7b   |          38.87 |          66.52 |     66.84 |      66.80 |        66.76 |
|    Llama3-8b   |          73.60 |          68.41 |     65.24 |      67.16 |        69.12 |
| CrystalChat-7b |          55.45 |          60.60 |     63.32 |      64.17 |        63.40 |

Dutch Results (F1 scores) (Title Prompts):
|      Model     | Single Perfect | Double Perfect | Assonance | Consonance | Alliteration |
|:--------------:|:--------------:|:--------------:|:---------:|:----------:|:------------:|
|   Llama-2-7b   |          28.78 |          50.33 |     45.19 |      52.37 |        62.58 |
|    Llama3-8b   |          65.00 |          66.90 |     67.08 |      59.56 |        67.61 |
| CrystalChat-7b |          55.39 |          56.48 |     64.69 |      57.53 |        63.59 |

Based on the F1 scores, the overall performance order seems to be Llama3-8B > Llama2-7b > CrystalChat-7b. Perfect rhymes seem to be difficult for both languages, whereas assonance, consonance, and alliteration are nearly identical in English and Dutch. Description-level prompts benefit models like Llama2 or CrystalChat, but Llama3 is virtually unaffected.

_For a more detailed results and discussion section refer to the [report](https://github.com/Aadit3003/llm-rhyme/blob/85faec464d38443517b90497e032cf2f9bb28e9a/report.pdf)_

## **Main Contributions**
* [Dutch Pronunciation dictionary](https://github.com/Aadit3003/llm-rhyme/blob/85faec464d38443517b90497e032cf2f9bb28e9a/aadit's-dutch-dict) in CMU-Dict format with 349k words.
* [English](https://github.com/Aadit3003/llm-rhyme/tree/85faec464d38443517b90497e032cf2f9bb28e9a/data/english) and [Dutch](https://github.com/Aadit3003/llm-rhyme/tree/85faec464d38443517b90497e032cf2f9bb28e9a/data/dutch) Rhyming datasets, both with 5k word pairs corresponding to five types of rhymes (1k each) (including orthographic and phonemic representation), and 5k non-rhyming word pairs.
* Inference [Outputs](https://github.com/Aadit3003/llm-rhyme/tree/85faec464d38443517b90497e032cf2f9bb28e9a/output) on both rhyme datasets using three open-source LLMs (Llama2-7b, Llama3-8B, and CrystalChat).


## Directory Structure
* bash_scripts - Bash scripts to run evaluate_rhyme.py in different configurations.
* **data** - The English and Dutch datasets organized by <language>/<model_family>/<prompt_type>/<rhyme_type>/. The 'solutions' directory contains the words with orthographic and phonemic representation both, whereas the 'test' directory contains only the word pairs. Each txt file contains 1k word pairs and the non.txt file contains 5k non-rhyming word pairs.
* **data_preparation**
    * _create_aadit's_dutch_dict.py_ - The script to convert Celex2 data into aadit's-dutch-dict, following the CMU-Dict format.
    * _scrape_cmu_dict.py_ - The script to extract the five types of rhyming words from CMU-Dict (cmudict-0.7b).
    * _scrape_dutch_dict.py_ - The script to extract the five types of rhyming word pairs from aadit's-dutch-dict.
    * _utils.py_ - utilities for file read/write, string operations
* logs - Logs from the various evaluation runs.
* **output** - The LLM inference outputs organized by <language>/<model_family>/<prompt_type>/<rhyme_type>/

**aadit's-dutch-dict** - The file containing Celex2 data (in the CMU-Dict format) (349k words and their orthographic-phonemic representation).\
**cmudict-0.7b** - The file containing CMU-Dict data (134k words and their orthographic-phonemic representation).

**_evaluate_rhyme.py_** - The script to evaluate an LLM for a particular rhyming dataset. Returns the F1 score and stores the inference outputs. \
**_prompts.py_** - The script to generate the prompts used by evaluate_rhyme.py for different LLM families.


report.pdf - The report containing details about experimental design and results. \
talk_slides.pdf - The slides to my presentation on this study.

## Reproduce the Results

* (Optional) To recreate the Dutch pronunciation dictionary:
    * Download the Celex2 dictionary and place it in the root folder
    * ``` python create_aadit's_dutch_dict.py```
    * Otherwise, simply use:- [Aadit's Dutch Pronunciation dictionary](https://github.com/Aadit3003/llm-rhyme/blob/85faec464d38443517b90497e032cf2f9bb28e9a/aadit's-dutch-dict)
* (Optional) To recreate the dataset:
    *  ``` python scrape_cmu_dict.py```
    *  ``` python scrape_dutch_dict.py```
    *  Otherwise, simply use the relevant rhyming dataset for your use case:- [English](https://github.com/Aadit3003/llm-rhyme/tree/85faec464d38443517b90497e032cf2f9bb28e9a/data/english) and [Dutch](https://github.com/Aadit3003/llm-rhyme/tree/85faec464d38443517b90497e032cf2f9bb28e9a/data/dutch)
* To inference the LLMs:
    * ``` python evaluate_rhyme.py <language> <model_family> <rhyme_type> <prompt_type> ```
    *  language = _"english" / "dutch"_
    *  model_family = _"llama2" / "llama3" / "crystal" / "olmo"_
    *  rhyme_type = _"alliterative" / "assonance" / "consonance" / "singlePerfect" / "doublePerfect"_
    *  prompt_type = _"title" / "description"_
    * Refer to [bash_scripts](https://github.com/Aadit3003/llm-rhyme/tree/51dde68e3a068d624a5f32fa3477ee26e8aad44d/bash_scripts).
    * The final F1 score is printed to the console, while the outputs for each rhyme pair are written to:- output/<language>/<model_family>/<prompt_type>/<rhyme_type>/



