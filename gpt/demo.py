from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
#from langchain.llms import OpenAI
from langchain.chains import LLMRequestsChain, LLMChain
import nltk,os

def RunLangChain():
    print("here run langchain")
    os.environ["OPENAI_API_KEY"] = "sb-29b8d019e623a4b6e4dbbbd0dff3d9b78cc8dffd7fab6248"
    os.environ.update(HTTP_PROXY="http://127.0.0.1:10807", HTTPS_PROXY="http://127.0.0.1:10807")
    #os.environ["OPENAI_PROXY"] = "http://127.0.0.1:10807"
    #nltk.set_proxy('http://127.0.0.1:10807')
    #nltk.download('punkt')
    #nltk.download('averaged_perceptron_tagger')
    #RunTxtReader()
    GetJsonFromURL()

def RunTxtReader():
    # 导入文本
    loader = UnstructuredFileLoader("/Users/e/workspace/hackathon/gpt/1token.txt")
    # 将文本转成 Document 对象
    document = loader.load()
    print(f'documents:{len(document)}')

    # 初始化文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 0
    )

    # 切分文本
    split_documents = text_splitter.split_documents(document)
    print(f'documents:{len(split_documents)}')

    # 加载 llm 模型
    llm = OpenAI(model_name="text-davinci-003", max_tokens=1500)

    # 创建总结链
    chain = load_summarize_chain(llm, chain_type="refine", verbose=True)

    # 执行总结链，（为了快速演示，只总结前5段）
    chain.run(split_documents[:5])


def GetJsonFromURL():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    template = """在 >>> 和 <<< 之间是网页的返回的HTML内容。
    请抽取参数请求的信息。

    >>> {requests_result} <<<
    请使用如下的JSON格式返回数据
    {{
      "时间":"a",
      "调整内容":"b",
      "接口":"c"
    }}
    Extracted:"""

    prompt = PromptTemplate(
        input_variables=["requests_result"],
        template=template
    )

    chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=prompt))
    inputs = {
      "url": "https://www.binance.com/zh-CN/support/announcement/%E5%85%B3%E4%BA%8E%E8%B0%83%E6%95%B4rest-api%E6%8E%A5%E5%8F%A3%E8%AF%B7%E6%B1%82%E6%9D%83%E9%87%8D%E7%9A%84%E5%85%AC%E5%91%8A-f3d75a44fc7b4610b080b9c3499ed075"
    }

    response = chain(inputs)
    print(response['output'])
