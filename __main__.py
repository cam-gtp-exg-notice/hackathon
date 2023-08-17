import os

from rest import rest
from gpt import demo


if __name__ == "__main__":
    #training.RunTraining()
    # 后台执行cmd命令
    os.system('nohup python3 spider/announcement_monitoring.py &')
    os.system('nohup python3 spider/gemini_monitoring.py &')
    demo.RunLangChain()
    #notify.RunNotify()
    rest.RunRest()
