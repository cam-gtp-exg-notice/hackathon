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
  "url": "https://www.binance.com/zh-CN/support/announcement/%E5%B8%81%E5%AE%89%E4%B8%8A%E7%BA%BF%E7%AC%AC35%E6%9C%9F%E6%96%B0%E5%B8%81%E6%8C%96%E7%9F%BF-%E4%BD%BF%E7%94%A8bnb-tusd%E6%8C%96%E7%9F%BFpendle-pendle-8baee8ca20d64074ba503aa3963e952e"
}

response = chain(inputs)
print(response['output'])