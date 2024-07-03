import hf_olmo
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

olmo_model_name = "allenai/OLMo-7B-Instruct"

cache_path = "/data/shire/data/aaditd/trial/"
olmo_model = AutoModelForCausalLM.from_pretrained(olmo_model_name, cache_dir = cache_path).to('cuda')
olmo_tokenizer = AutoTokenizer.from_pretrained(olmo_model_name, cache_dir = cache_path)
word1 = "bot"
word2 = "caught"
prompt = f"Do these words form a perfect rhyme {word1}-{word2}?"

def olmo_generate(prompt, model, tokenizer):
    
    chat = [
        { "role": "user", "content": prompt},
    ]
    prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    # optional verifying cuda
    # inputs = {k: v.to('cuda') for k,v in inputs.items()}
    # olmo = olmo.to('cuda')
    response = model.generate(input_ids=inputs.to(model.device), max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
    
    return tokenizer.batch_decode(response, skip_special_tokens=True)[0]
    # >> '<|user|>\nWhat is language modeling?\n<|assistant|>\nLanguage modeling is a type of natural language processing (NLP) task or machine learning task that...'

print("OLMO:")

print(olmo_generate(prompt, olmo_model, olmo_tokenizer))

print("______________________________________________")


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

generator_model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
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
 
print("LLAMA3")
print(llama3_generate(prompt = prompt,
                model = generator_model, 
                tokenizer= generator_tokenizer))

print("______________________________________________")
