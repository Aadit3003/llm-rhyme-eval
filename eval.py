import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from huggingface_hub import login
import argparse
from clean import file_read_strings, file_write_strings
from sklearn.metrics import f1_score
from prompts import MODEL_NAMES, get_prompt, clean_answer
from string import punctuation
import re
import random

DATA_PATH = "data/english/test"
OUTPUT_PATH = "output/english"
NON_RHYME_PATH = "data/english/test/non.txt"

# TEXT GENERATION FUNCTIONS

def llama2_generate(prompt, model, tokenizer):
    DEV = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(DEV)

    generate_kwargs = dict(
        input_ids=inputs,
        temperature=0.6, 
        top_p=0.9, 
        do_sample=True,
        max_new_tokens=100,
        repetition_penalty=1.3
    )
    outputs = model.generate(**generate_kwargs)
    text =  str(tokenizer.decode(outputs[0]))

    return text

def llama3_generate(prompt, model, tokenizer):
    DEV = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    messages = [
    {"role": "system", "content": "You are an AI assistant. You will be given a task. You must generate a Yes/No answer and justify it."},
    {"role": "user", "content": prompt},
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize = False,
        add_generation_prompt = True
    )
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(DEV)

    generate_kwargs = dict(
        input_ids=inputs,
        temperature=0.6, 
        top_p=0.9, 
        do_sample=True,
        eos_token_id = [tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")],
        max_new_tokens=100,
        repetition_penalty=1.3
    )
    outputs = model.generate(**generate_kwargs)
    text =  str(tokenizer.decode(outputs[0]))

    return text

def crystal_generate(prompt, model, tokenizer):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    gen_tokens = model.generate(input_ids, do_sample=True, max_length=400)

    
    return tokenizer.batch_decode(gen_tokens)[0]

def olmo_generate(prompt, model, tokenizer):
    
    chat = [
        { "role": "user", "content": prompt},
    ]
    prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    # optional verifying cuda
    # inputs = {k: v.to('cuda') for k,v in inputs.items()}
    response = model.generate(input_ids=inputs.to(model.device), max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
    
    return tokenizer.batch_decode(response, skip_special_tokens=True)[0]


def text_generate(model_family, prompt, model, tokenizer):
    if model_family == "llama2":
        return llama2_generate(prompt, model, tokenizer)
    elif model_family == "llama3":
        return llama3_generate(prompt, model, tokenizer)
    elif model_family == "crystal":
        return crystal_generate(prompt, model, tokenizer)
    elif model_family == "olmo":
        return olmo_generate(prompt, model, tokenizer)
    
    raise Exception("No such model supported!!!")

# EVALUATION CODE

def evaluate(model, tokenizer, rhyme_type, prompt_type, model_family):

    first_n = 500

    input_file = f"{DATA_PATH}/{rhyme_type}.txt"
    output_file = f"{OUTPUT_PATH}/{model_family}/{prompt_type}/{rhyme_type}.txt"

    old_lines = file_read_strings(input_file)[0:first_n]
    non_rhymes = file_read_strings(NON_RHYME_PATH)
    random.shuffle(non_rhymes)
    non_rhymes = non_rhymes[0:first_n]
    lines = old_lines + non_rhymes

    golds = [1 for _ in range(len(old_lines))] + [0 for _ in range(len(non_rhymes))]
    
    ziploc = list(zip(lines, golds))
    random.shuffle(ziploc)
    lines, golds = zip(*ziploc)

    preds = []
    answer_strings = []

    pairs = [tuple(line.split()) for line in lines]
    print(golds)
    print(pairs)
    
    i = 0
    count = 0
    for word1, word2 in pairs:

        prompt = get_prompt(model_family, prompt_type, rhyme_type, word1, word2)

        ans = text_generate(model_family, prompt, model, tokenizer)

        answer = clean_answer(model_family, ans, prompt)

        r = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))
        answer_tokens = r.split(answer.strip().lower())[0:15]
        # print()
        # print(answer_tokens)
        # print()

        if "yes" in answer_tokens:
            pred = 1
        elif "no" in answer_tokens or "not" in answer_tokens:
            pred = 0
        else:
            print("     Came Here")
            count += 1
            pred = 0

        preds.append(pred)
        # print("PROMPT: ")
        # print(prompt)
        # print()
        # print("ANSWER: ")
        # print(ans)
        # print()
        # print("_______________________________________________________")
        answer_strings.append(f"{word1}, {word2}, Gold: {golds[i]}, Pred: {pred} || {answer}")

        if i % 100 == 0:
            print(f"        {i} DONE!")
        i += 1

    file_write_strings(output_file, answer_strings)

    F1 = f1_score(golds, preds)


    print(f"Non yes/no happened {count} times!")
    print(f"RHYME TYPE: {rhyme_type} | PROMPT TYPE: {prompt_type} | F-1 Score: {F1}")

    return F1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model_family", type=str, help='LLM family')
    parser.add_argument("rhyme_type", type=str, help='Type of Rhyme')
    parser.add_argument("prompt_type", type=str, help='Type of Prompt')
    args = parser.parse_args()

    model_family = args.model_family
    rhyme_type = args.rhyme_type
    prompt_type = args.prompt_type


    # Loading the Generator Model
    torch.backends.cuda.enable_mem_efficient_sdp(False)
    torch.backends.cuda.enable_flash_sdp(False)
    cache_path = "/data/shire/data/aaditd/trial/"

    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    generator_model_name = MODEL_NAMES[model_family]
    login("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")
        


    if model_family in ["llama2", "llama3"]:
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
    
    elif model_family in "crystal":
        generator_tokenizer = AutoTokenizer.from_pretrained(generator_model_name, 
                                          trust_remote_code=True,
                                          cache_dir = cache_path)
        generator_model = AutoModelForCausalLM.from_pretrained(generator_model_name, 
                                             trust_remote_code=True,
                                             cache_dir = cache_path).to(device)
    
    elif model_family in "olmo":
        generator_model = AutoModelForCausalLM.from_pretrained(generator_model_name, 
                                                          cache_dir = cache_path,
                                                          trust_remote_code=True)
        generator_tokenizer = AutoTokenizer.from_pretrained(generator_model_name, 
                                                       cache_dir = cache_path,
                                                       trust_remote_code=True)

    evaluate(
             model=generator_model,
             tokenizer=generator_tokenizer,
             rhyme_type= rhyme_type,
             prompt_type= prompt_type,
             model_family= model_family
             )
    
    print("DONE GURL!!")


