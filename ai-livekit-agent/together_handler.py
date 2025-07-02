from together import Together

client = Together(api_key="fcc488af99db8e9cec36934fb3a0743ca99c49b589ff986a66046f2923183d19")

def get_llm_response(user_input):
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content.strip()
