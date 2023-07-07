from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

llm = OpenAI(model_name="text-davinci-003")

# 告诉他我们生成的内容需要哪些字段，每个字段类型式啥
response_schemas = [
    ResponseSchema(name="summary", description="Summary of the announcement"),
    ResponseSchema(name="score", description="A score between 0 to 100")
]

# 初始化解析器
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 生成的格式提示符
format_instructions = output_parser.get_format_instructions()

template = """
As a blockchain developer and trader, you need to stay up-to-date with exchange announcement changes and rate them based on their importance, on a scale of 0 to 100, with higher scores indicating higher importance. Generate an announcement summary and corresponding score based on the input exchange announcement.

% USER INPUT:
{user_input}

Output format: {format_instructions}

YOUR RESPONSE:
"""

# 将我们的格式描述嵌入到 prompt 中去，告诉 llm 我们需要他输出什么样格式的内容
prompt = PromptTemplate(
    input_variables=["user_input"],
    partial_variables={"format_instructions": format_instructions},
    template=template
)

promptValue = prompt.format(user_input="币安将于2023年07月07日16:00（东八区时间）上线MAV/TRY、OCEAN/TRY、TUSD/TRY交易对，邀您体验！")
llm_output = llm(promptValue)

# 使用解析器进行解析生成的内容
print(output_parser.parse(llm_output))