import openai

openai.api_key = "********"

def ask_agent(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    return response['choices'][0]['message']['content']

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    reply = ask_agent(user_input)
    print("Agent:", reply)
