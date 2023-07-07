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
  "url": "https://www.binance.com/zh-CN/support/announcement/%E5%B8%81%E5%AE%89%E5%90%88%E7%BA%A6%E5%B0%86%E8%B0%83%E6%95%B4storjusdt-u%E6%9C%AC%E4%BD%8D%E6%B0%B8%E7%BB%AD%E5%90%88%E7%BA%A6%E6%9D%A0%E6%9D%86%E5%92%8C%E4%BF%9D%E8%AF%81%E9%87%91%E9%98%B6%E6%A2%AF%E5%8F%8A%E8%B5%84%E9%87%91%E8%B4%B9%E7%8E%87%E4%B8%8A%E9%99%90-50eb47de435f4313b09615c3c2c68bb8"
}

response = chain(inputs)
print(response['output'])