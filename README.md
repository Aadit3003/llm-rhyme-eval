# Evaluating the Multilingual Rhyming capabilities of Open-Source LLMs

Intro About the purpose
    Types of Rhymes
    Models
    Evaluation metrics

    Results Tables

For more details refer to the [report]([url](https://github.com/Aadit3003/llm-rhyme/blob/85faec464d38443517b90497e032cf2f9bb28e9a/report.pdf)) and slides from my [talk](https://github.com/Aadit3003/llm-rhyme/blob/85faec464d38443517b90497e032cf2f9bb28e9a/talk_slides.pdf)! \

Main Contributions:
* [Dutch Pronunciation dictionary](https://github.com/Aadit3003/llm-rhyme/blob/85faec464d38443517b90497e032cf2f9bb28e9a/aadit's-dutch-dict) in CMU-Dict format with 349k words.
* [English]([url](https://github.com/Aadit3003/llm-rhyme/tree/85faec464d38443517b90497e032cf2f9bb28e9a/data/english)) and [Dutch]([url](https://github.com/Aadit3003/llm-rhyme/tree/85faec464d38443517b90497e032cf2f9bb28e9a/data/dutch)) Rhyming datasets with five types of rhymes, along with orthographic and phonemic representation.
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

## Reproduce
Environment
Steps to recreate dictionary
Steps to recreate dataset
Steps to inference models





# TO DO
1. Reorganize files, rename files, paths consistently!
2. Module Docstrings, Function Docstrings clean-up code
3. Finish off Readme!
