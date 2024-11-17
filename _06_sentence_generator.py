import openai
from _05_prompt import prompt_openai
from dotenv import load_dotenv

def openai_generator():
    load_dotenv()
    client = openai.OpenAI()
    last_number_file = 'last_number.txt'  # File to store the last used number

    # gpt_model = "gpt-3.5-turbo"
    gpt_model = "gpt-4o"


    def get_completion(prompt, model=gpt_model, temperature=0.9):
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,  # this is the degree of randomness of the model's output
        )
        return response.choices[0].message.content

    # load last number from db
    def load_last_number():
        try:
            with open(last_number_file, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return '1'  # Default to the first number if file doesn't exist


    response = get_completion(prompt_openai(seq=load_last_number()))
    print(response)


    # save the response to a text file named ‘sentences_{last_number}.txt’
    with open(f'sentences/sentences_{load_last_number()}.txt', 'w', encoding='utf-8') as f:
        f.write(response)
