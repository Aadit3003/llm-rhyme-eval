import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import pandas as pd
from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig
import argparse
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)
from clean import file_read_strings, file_write_strings
from sklearn.metrics import f1_score
import random

DATA_PATH = "data/english/test"
OUTPUT_PATH = "output/english/llama2"
NON_RHYME_PATH = "data/english/test/non.txt"

prompt_set_1 = { # Title
    "singlePerfect": "[INST] Do these words rhyme form a perfect rhyme? ",
    "doublePerfect": "[INST] Do these words form a perfect rhyme? ",
    "assonance": "[INST] Do these words show assonance? ",
    "consonance": "[INST] Do these words show consonance? ",
    "alliterative": "[INST] Do these words show alliteration?"
}

prompt_set_2 = { # Description
    "singlePerfect": "[INST] Do these words rhyme i.e. have different consonants followed by identical vowel and consonant sounds?",
    "doublePerfect": "[INST] Do these words rhyme i.e. have different consonants followed by identical vowel and consonant sounds?",
    "assonance": "[INST] Do these words have identical vowel sounds but different consonant sounds? ",
    "consonance": "[INST] Do these words have identical consonant sounds but different vowel sounds? ",
    "alliterative": "[INST] Do these words begin with the same consonant sound?"
}

few_shot_prompt = "[INST] Do these words rhyme? "

def llama_generate(prompt, model, tokenizer, temperature = 0.8, max_blog_length=300):
    DEV = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(DEV)

    generate_kwargs = dict(
        input_ids=inputs,
        temperature=temperature, 
        top_p=1.0, 
        top_k=40,
        max_new_tokens=100,
        repetition_penalty=1.3
    )
    outputs = model.generate(**generate_kwargs)
    text =  str(tokenizer.decode(outputs[0]))

    return text

def evaluate(model, tokenizer, rhyme_type, prompt_type):
    if prompt_type == "title":
        prompt_prefix = prompt_set_1[rhyme_type]
    elif prompt_type == "description":
        prompt_prefix = prompt_set_2[rhyme_type]

    input_file = f"{DATA_PATH}/{rhyme_type}.txt"
    output_file = f"{OUTPUT_PATH}/{prompt_type}/{rhyme_type}.txt"

    old_lines = file_read_strings(input_file)[0:500]
    non_rhymes = file_read_strings(NON_RHYME_PATH)
    random.shuffle(non_rhymes)
    non_rhymes = non_rhymes[0:500]
    lines = old_lines + non_rhymes

    golds = [1 for _ in range(len(old_lines))] + [0 for _ in range(len(non_rhymes))]
    print(golds)
    ziploc = list(zip(lines, golds))
    random.shuffle(ziploc)
    lines, golds = zip(*ziploc)

    preds = []
    answer_strings = []

    pairs = [tuple(line.split()) for line in lines]
    print(pairs)
    
    i = 0
    for word1, word2 in pairs:

        prompt = prompt_prefix + f"{word1}-{word2} [/INST]"
        ans = llama_generate(prompt, model, tokenizer, temperature = 0.8, max_blog_length=300)

        if "yes" in ans.lower():
            pred = 1
        else:
            pred = 0

        preds.append(pred)
        answer_strings.append(f"{word1}, {word2}, Gold: {golds[i]}, Pred: {pred} || {ans.removeprefix(prompt)}")
        i += 1

    file_write_strings(output_file, answer_strings)

    F1 = f1_score(golds, preds)


    print(f"RHYME TYPE: {rhyme_type} | PROMPT TYPE: {prompt_type} | F-1 Score: {F1}")

    return F1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("rhyme_type", type=str, help='Type of Rhyme')
    parser.add_argument("prompt_type", type=str, help='Type of Prompt')
    args = parser.parse_args()

    rhyme_type = args.rhyme_type
    prompt_type = args.prompt_type


    # Loading the Generator Model
    torch.backends.cuda.enable_mem_efficient_sdp(False)
    torch.backends.cuda.enable_flash_sdp(False)
    cache_path = "/data/shire/data/aaditd/trial/"

    DEV = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    generator_model_name = "meta-llama/Llama-2-7b-chat-hf"
    login("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")
        
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    generator_model = AutoModelForCausalLM.from_pretrained(generator_model_name, 
                                                torch_dtype=torch.bfloat16,
                                                quantization_config=bnb_config,
                                                cache_dir=cache_path)
    generator_tokenizer = AutoTokenizer.from_pretrained(generator_model_name, cache_dir=cache_path)

    evaluate(
             model=generator_model,
             tokenizer=generator_tokenizer,
             rhyme_type = rhyme_type,
             prompt_type= prompt_type
             )
    
    print("DONE GURL!!")
