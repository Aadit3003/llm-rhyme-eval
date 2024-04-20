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
from scrape import file_read_strings, file_write_strings

few_shot_prompt = """<s>[INST] Observe these examples of rhymes.
        perchance-enhance (yes)
        mean-bean (yes)
        cat-bot (no)
        Now, do these words rhyme? 
        """

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

def evaluate(input_file, model, tokenizer, title, output_file):
    lines = file_read_strings(input_file)
    pairs = [tuple(line.split()) for line in lines]
    
    answers = []
    answer_strings = []
    print(pairs)
    for word1, word2 in pairs:
        
        word1 = ''.join(filter(str.isalpha, word1)) # Gets rid of those abbreviation(1) markers!
        word2 = ''.join(filter(str.isalpha, word2))

        prompt = few_shot_prompt + \
            f"""{word1}-{word2} ( [/INST]
            """
        ans = llama_generate(prompt, model, tokenizer, temperature = 0.8, max_blog_length=300)

        answers.append(ans)
        answer_strings.append(f"{word1}, {word2} {ans.removeprefix(prompt)}")

    file_write_strings(output_file, answer_strings)

    count = 0
    for a in answers:
        if "yes" in a.lower():
            count += 1
    

    accuracy = count / len(answers)
    print(f"RHYME TYPE: {title} | ACCURACY: {accuracy}")

    return accuracy


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str, help='testing file')
    parser.add_argument("output_path", type=str, help='output write file')
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path


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

    evaluate(input_file= input_path,
             model=generator_model,
             tokenizer=generator_tokenizer,
             title = input_path.split("/")[-1].split(".txt")[0],
             output_file= output_path)
    
    print("DONE GURL!!")
