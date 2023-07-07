from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from .prompt import template
from langchain.chains import LLMRequestsChain, LLMChain
import nltk,os,json

APIKEY="sb-29b8d019e623a4b6e4dbbbd0dff3d9b78cc8dffd7fab6248"
PROXY="http://127.0.0.1:10807"

def RunLangChain():
    print("here run langchain")
    os.environ["OPENAI_API_KEY"] = APIKEY
    os.environ.update(HTTP_PROXY=PROXY, HTTPS_PROXY=PROXY)
    #os.environ["OPENAI_PROXY"] = "http://127.0.0.1:10807"
    #nltk.set_proxy('http://127.0.0.1:10807')
    #nltk.download('punkt')
    #nltk.download('averaged_perceptron_tagger')
    #RunTxtReader()
    print(GetJsonFromURL(url="https://www.binance.com/zh-CN/support/announcement/api%E6%9C%8D%E5%8A%A1%E6%9B%B4%E6%96%B0%E5%85%AC%E5%91%8A-654c092a2a2347bdb5ccd6faa0c6c039"))

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


def GetJsonFromURL(url):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


    prompt = PromptTemplate(
        input_variables=["requests_result"],
        template=template.URLTemplate
    )

    chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=prompt))
    inputs = {
        # "url": "https://www.binance.com/en/support/announcement/notice-on-adjusting-the-request-weight-of-rest-api-endpoints-f3d75a44fc7b4610b080b9c3499ed075"
        # "url": "https://www.binance.com/zh-CN/support/announcement/%E5%B8%81%E5%AE%89%E9%80%90%E4%BB%93%E6%9D%A0%E6%9D%86%E6%96%B0%E5%A2%9Exvg%E8%B5%84%E4%BA%A7-580de383967f459ba1306d67886d5978"
        # "url": "https://www.binance.com/en/support/announcement/updates-to-api-services-654c092a2a2347bdb5ccd6faa0c6c039"
        #"url":"https://www.binance.com/zh-CN/support/announcement/api%E6%9C%8D%E5%8A%A1%E6%9B%B4%E6%96%B0%E5%85%AC%E5%91%8A-654c092a2a2347bdb5ccd6faa0c6c039"
        "url":url
    }

    response = chain(inputs)
    out = response['output']
    if is_json_string(out):
        return out
    return  out

def is_json_string(s):
    try:
        json_object = json.loads(s)
    except ValueError as e:
        return False
    return True