from rest import rest
from langchain import langchain
from training import training
from notify import notify

if __name__ == "__main__":
    training.RunTraining()
    langchain.RunLangChain()
    notify.RunNotify()
    rest.RunRest()
