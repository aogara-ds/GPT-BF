import os
import dotenv
import openai

dotenv.load_dotenv()
openai.api_key = os.getenv('OpenAI_API_Key')

def conversation(username, partnername, prompt, stopword,
                 endpoint, max_tokens=50, temperature=0.7):

    # AI makes the first statement
    completion = openai.Completion.create(
        model=endpoint,
        prompt=prompt,
        max_tokens=max_tokens,
        stop='&&&',
        temperature=temperature
    )['choices'][0]['text']

    print(prompt)

    # initialize user reply
    user_reply = ""

    # end the conversation with a specified string
    while(user_reply != stopword):

        # get user input
        user_reply = input(f"{username}: ")
        prompt += completion + f"\n{username}: " + user_reply + f"\n{partnername}:"

        # get AI response
        completion = openai.Completion.create(
            model=endpoint,
            prompt=prompt,
            max_tokens=max_tokens,
            stop='&&&',
            temperature=temperature
        )['choices'][0]['text']

        # print AI response
        print(f"{partnername}: {completion}")

if __name__ == "__main__":

    prompt = "You are AI-Dan, my loving and caring boyfriend. I am Regan, your girlfriend who you adore. Let's have a conversation!"
    endpoint = "curie:ft-personal-2022-12-05-19-41-02"

    conversation(
        username="Regan",
        partnername="Aidan",
        prompt=prompt,
        stopword="ok byee",
        endpoint=endpoint
    )