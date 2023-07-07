from threading import Thread
import telegram
import feishu


def RunNotify(text):
    tg = telegram.TelegramMessagePusher()
    fs = feishu.FeiShuMessagePusher()
    t1 = Thread(target=tg.send_text, args=(text, ))
    t2 = Thread(target=fs.send_text, args=(text, ))
    t1.start()
    t2.start()
    print("here run notify")


if __name__ == '__main__':
    RunNotify("text example")
