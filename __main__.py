from rest import rest
from gpt import demo
from training import training
from notify import notify


if __name__ == "__main__":
    #training.RunTraining()
    demo.RunLangChain()
    #notify.RunNotify()
    rest.RunRest()
