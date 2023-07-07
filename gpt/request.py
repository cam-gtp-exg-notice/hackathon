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

llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)

template = """在 >>> 和 <<< 之间是网页的返回的HTML内容。
网页是币安发布的公告。
请抽取参数请求的信息。

>>> {requests_result} <<<
请使用如下的JSON格式返回数据
{{
  ""announcement": "Exchange announcement text",
}}
Extracted:"""

prompt = PromptTemplate(
    input_variables=["requests_result"],
    template=template
)

chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=prompt))
inputs = {
  "url": "https://www.binance.com/zh-CN/support/announcement/%E5%B8%81%E5%AE%89%E9%80%90%E4%BB%93%E6%9D%A0%E6%9D%86%E6%96%B0%E5%A2%9Exvg%E8%B5%84%E4%BA%A7-580de383967f459ba1306d67886d5978"
}

response = chain(inputs)
print(response['output'])