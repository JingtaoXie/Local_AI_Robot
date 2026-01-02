import time
from langchain_ollama import ChatOllama   ##langchain ollama package
import VOICE_INPUT_OUTPUT as vio
from functools import lru_cache


llm = ChatOllama(
    model="phi3",
    temperature=0,
)
@lru_cache(maxsize=30)
def questionAndResponse():
    print("I am listening your question ")
    clientCommand = vio.startListening()
    vio.sd.wait()
    clientCommandinText = vio.identfyingCommand(clientCommand)

    if clientCommandinText == "":
        vio.readingAnswer("Sorry I didn't follow your questions")
    else:
        time.sleep(0.5)
        messages = [
            ("system", "Answer all questions in Chinese."),
            ("human", clientCommandinText),
        ]
        ai_msg = llm.invoke(messages)

        # invoke can return lots of elements and content is the answer itself
        print(ai_msg.content)
        vio.readingAnswer(ai_msg.content)


if __name__ == "__main__":
    print("===== Program Starting =====", flush=True)
    questionAndResponse()






