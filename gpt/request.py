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

llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.9)

prompt = PromptTemplate(
    input_variables=["requests_result"],
    template=URLTemplate
)

chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=prompt))
inputs = {
  "url": "https://www.binance.com/zh-CN/support/announcement/%E5%B8%81%E5%AE%89vip%E5%92%8C%E6%B4%BB%E6%9C%9F%E5%80%9F%E5%B8%81%E5%B9%B3%E5%8F%B0%E6%96%B0%E5%A2%9E%E5%8F%AF%E5%80%9F%E8%B5%84%E4%BA%A7%E4%BB%A5%E5%8F%8A%E5%8F%AF%E8%B4%A8%E6%8A%BC%E8%B5%84%E4%BA%A7-2023-06-28-381724453dcb409fbd86a97323cb2a7f"
}

response = chain(inputs)
print(response['output'])