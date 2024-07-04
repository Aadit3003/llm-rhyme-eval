# Evaluating the Multilingual Rhyming capabilities of Open-Source LLMs

Intro About the purpose
    Types of Rhymes
    Models
    Evaluation metrics

**Results:**
English Results (Title Prompts):
|      Model     | Single Perfect | Double Perfect | Assonance | Consonance | Alliteration |
|:--------------:|:--------------:|:--------------:|:---------:|:----------:|:------------:|
|   Llama-2-7b   |          38.87 |          66.52 |     66.84 |      66.80 |        66.76 |
|    Llama3-8b   |          73.60 |          68.41 |     65.24 |      67.16 |        69.12 |
| CrystalChat-7b |          55.45 |          60.60 |     63.32 |      64.17 |        63.40 |

Dutch Results (Title Prompts):
|      Model     | Single Perfect | Double Perfect | Assonance | Consonance | Alliteration |
|:--------------:|:--------------:|:--------------:|:---------:|:----------:|:------------:|
|   Llama-2-7b   |          28.78 |          50.33 |     45.19 |      52.37 |        62.58 |
|    Llama3-8b   |          65.00 |          66.90 |     67.08 |      59.56 |        67.61 |
| CrystalChat-7b |          55.39 |          56.48 |     64.69 |      57.53 |        63.59 |

For more details refer to the [report](https://github.com/Aadit3003/llm-rhyme/blob/85faec464d38443517b90497e032cf2f9bb28e9a/report.pdf) and the slides from my [talk](https://github.com/Aadit3003/llm-rhyme/blob/85faec464d38443517b90497e032cf2f9bb28e9a/talk_slides.pdf)!

**Main Contributions**:
* [Dutch Pronunciation dictionary](https://github.com/Aadit3003/llm-rhyme/blob/85faec464d38443517b90497e032cf2f9bb28e9a/aadit's-dutch-dict) in CMU-Dict format with 349k words.
* [English](https://github.com/Aadit3003/llm-rhyme/tree/85faec464d38443517b90497e032cf2f9bb28e9a/data/english) and [Dutch](https://github.com/Aadit3003/llm-rhyme/tree/85faec464d38443517b90497e032cf2f9bb28e9a/data/dutch) Rhyming datasets with five types of rhymes, along with orthographic and phonemic representation.
* Inference [Outputs](https://github.com/Aadit3003/llm-rhyme/tree/85faec464d38443517b90497e032cf2f9bb28e9a/output) on both rhyme datasets using three open-source LLMs (Llama2-7b, Llama3-8B, and CrystalChat).


## Directory Structure
* bash_scripts
* data
* data_preparation
    * _create_aadit's_dutch_dict.py_
    * _scrape_cmu_dict.py_
    * _scrape_dutch_dict.py_
    * _utils.py_
* logs
* output

**aadit's-dutch-dict** \
**cmudict-0.7b**

_evaluate_rhyme.py_ \
_prompts.py_ 

README.md \
report.pdf \
talk_slides.pdf 

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



