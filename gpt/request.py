# 示例：
# 输入：爬虫程序将交易所新的公告链接
# 调用gpt总结，分析，返回结构化的结果
# 参考 https://liaokong.gitbook.io/llm-kai-fa-jiao-cheng/#pa-qu-wang-ye-bing-shu-chu-json-shu-ju

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMRequestsChain, LLMChain
from prompt.template import URLTemplate
import os

os.environ.update(HTTPS_PROXY="http://127.0.0.1:7890")

llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.618)

prompt = PromptTemplate(
    input_variables=["requests_result"],
    template=URLTemplate
)

chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=prompt))
inputs = {
  "url": "https://www.binance.com/zh-CN/support/announcement/arkham-arkm-%E9%A1%B9%E7%9B%AE%E4%B8%8A%E7%BA%BF%E5%B8%81%E5%AE%89launchpad-%E5%9F%BA%E4%BA%8E%E6%8A%95%E5%85%A5%E6%A8%A1%E5%BC%8F-6ad1921b56fb4b369f9cf3e4449e62e2"
}

response = chain(inputs)
print(response['output'])