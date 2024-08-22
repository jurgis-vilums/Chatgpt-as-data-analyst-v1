import os
from openai import OpenAI
from groq import Groq



def get_openai_result(system_role, question, max_tokens):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=max_tokens,
        temperature=0,
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content

def get_groq_result(system_role, question, max_tokens):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        max_tokens=max_tokens,
        temperature=0,
        messages=[    
            {"role": "system", "content": system_role},
            {"role": "user", "content": question},
        ],
    )
    return chat_completion.choices[0].message.content

def get_ai_result(provider, system_role, question, max_tokens):
    if provider == "openai":
        return get_openai_result(system_role, question, max_tokens)
    elif provider == "groq":
        return get_groq_result(system_role, question, max_tokens)
    else:
        raise ValueError(f"Unknown AI provider: {provider}")