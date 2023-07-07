# 输入：爬虫程序将交易所新的公告链接
# 调用gpt总结，分析，返回结构化的结果
# 参考 https://liaokong.gitbook.io/llm-kai-fa-jiao-cheng/#pa-qu-wang-ye-bing-shu-chu-json-shu-ju
def Request():
    print("")



# 输入： 文本类型数据
# 输出： 调用gpt总结，分析，返回结构化的结果
# 用于测试展示时使用，可能交易所公告没有那么及时更新

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMRequestsChain, LLMChain
from prompt.template import URLTemplate
import os

os.environ.update(HTTPS_PROXY="http://127.0.0.1:7890")

llm = OpenAI(model_name="gpt-3.5-turbo", temperature=1)

prompt = PromptTemplate(
    input_variables=["requests_result"],
    template=URLTemplate
)

chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=prompt))
inputs = {
  "url": "https://www.binance.com/zh-CN/support/announcement/api%E6%9C%8D%E5%8A%A1%E6%9B%B4%E6%96%B0%E5%85%AC%E5%91%8A-654c092a2a2347bdb5ccd6faa0c6c039"
}

response = chain(inputs)
print(response['output'])