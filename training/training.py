# 程序启动从文件读取训练样本和对应的prompt
# 将embeddings结果写入到chroma

# 如果chroma中有数据直接读取，不重复训练
# 参考https://liaokong.gitbook.io/llm-kai-fa-jiao-cheng/#gou-jian-ben-di-zhi-shi-ku-wen-da-ji-qi-ren
# https://liaokong.gitbook.io/llm-kai-fa-jiao-cheng/#gou-jian-xiang-liang-suo-yin-shu-ju-ku


def RunTraining():
    print("here run training")