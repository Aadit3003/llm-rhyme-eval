MODEL_NAMES = {
    "llama2": "meta-llama/Llama-2-7b-chat-hf",
    "llama3": "meta-llama/Meta-Llama-3-8B",
    "crystal": "LLM360/CrystalChat",
    "olmo": "allenai/OLMo-7B"
}


SYSTEM_START_PROMPTS = {
    "llama2": "<s>[INST] <<SYS>> You are a helpful assistant. Always give a Yes/No answer and justify it. <</SYS>> ",
    "llama3": "<s>[INST] <<SYS>> You are a helpful assistant. Always give a Yes/No answer and justify it. <</SYS>> ",
    "crystal": "<s> <|sys_start|> You are an AI assistant. You will be given a task. You must generate a Yes/No answer and justify it. <|sys_end|> <|im_start|> ",
    "olmo": "banana"
}

SYSTEM_PROMPT_ENDINGS = {
    "llama2": " [/INST]",
    "llama3": " [/INST]",
    "crystal": " <|im_end|>",
    "olmo": "banana"

}

RHYME_PROMPTS = {
        "title":{ # Title
            "singlePerfect": "Do these words rhyme form a perfect rhyme? ",
            "doublePerfect": "Do these words form a perfect rhyme? ",
            "assonance": "Do these words show assonance? ",
            "consonance": "Do these words show consonance? ",
            "alliterative": "Do these words show alliteration? "
        },
        "description":{ # Description
            "singlePerfect": "Do these words rhyme i.e. have different consonants followed by identical vowel and consonant sounds? ",
            "doublePerfect": "Do these words rhyme i.e. have different consonants followed by identical vowel and consonant sounds? ",
            "assonance": "Do these words have identical vowel sounds but different consonant sounds? ",
            "consonance": "Do these words have identical consonant sounds but different vowel sounds? ",
            "alliterative": "Do these words begin with the same consonant sound? "
        }
}

model_family = "llama2"
prompt_type = "title"
rhyme_type = "assonance"
word1 = "bean"
word2 = "whale"

def get_prompt(model_family, prompt_type, rhyme_type, word1, word2):
    prompt_prefix = SYSTEM_START_PROMPTS[model_family]
    prompt_suffix = SYSTEM_PROMPT_ENDINGS[model_family]


    prompt = prompt_prefix + RHYME_PROMPTS[prompt_type][rhyme_type] + f"{word1}-{word2}" + prompt_suffix

    return prompt

def clean_answer(answer, prompt):
    answer = answer.replace("  ", " ")
    answer = answer.replace("  ", " ")
    answer = answer.removeprefix(prompt)

    return answer

# print(get_prompt(model_family, prompt_type, rhyme_type, word1, word2))
