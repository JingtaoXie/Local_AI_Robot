import time
from langchain_ollama import ChatOllama   ##langchain ollama package
import VOICE_INPUT_OUTPUT as vio
import vosk ##voice recognizer model
import sqlite3
from difflib import SequenceMatcher

model_path="vosk-model-small-cn-0.22"
languageModel = vosk.Model(model_path)

llm = ChatOllama(
    model="phi3",
    temperature=0,
)

memoryDatebase = sqlite3.connect("memory.db")
cursor = memoryDatebase.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS MEMORY_TABLE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

def gettingSimilarQuestion(question1,question2)-> float:
    return SequenceMatcher(None, question1, question2).ratio()



def writingDatabase(question: str, answer: str):
    cursor.execute(
        """
        INSERT INTO MEMORY_TABLE (question, answer)
        VALUES (?, ?)
        """,
        (question, answer)
    )
    memoryDatebase.commit()

def readingDatabase(newQuestion: str):
    cursor.execute("""SELECT question,anwser FROM MEMORY_TABLE""")
    questionsList = cursor.fetchall()

    if questionsList == []:
        return None
    else:
        theBiggestSimilarity = 0
        mostSimilarQuestion = None
        mostUsefulAnswer = None
        for question,answer in questionsList:
            similarity = gettingSimilarQuestion(question,newQuestion)
            if similarity > theBiggestSimilarity:
                mostSimilarQuestion = question
                mostUsefulAnswer = answer
                return mostUsefulAnswer


def questionAndResponse():
    print("I am listening your question ")
    clientCommand = vio.startListening()
    vio.sd.wait()
    clientCommandinText = vio.identfyingCommand(languageModel,clientCommand)

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

        ## save the question and answer to the memory database
        writingDatabase(clientCommandinText,ai_msg.content)


if __name__ == "__main__":
    print("===== Program Starting =====", flush=True)
    questionAndResponse()





