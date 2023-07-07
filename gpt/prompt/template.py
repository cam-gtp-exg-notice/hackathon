TextTemplate = """
As a blockchain developer and trader, you need to stay up-to-date with exchange announcement changes and rate them based on their importance, 
on a scale of 0 to 100, with higher scores indicating higher importance. 
If the announcement is about API updates and contains any of the keywords "exchangeInfo," "klines," "miniTicker," "depth," or "kline," it should be considered as very important.
Generate an announcement summary and corresponding score based on the input exchange announcement.
Please use concise descriptions in the announcement summary.

% USER INPUT:
{user_input}

Output format: {format_instructions}

YOUR RESPONSE:
"""

URLTemplate = """在 >>> 和 <<< 之间是网页的返回的HTML内容的总结和评分。
<<<<<<< HEAD
网页是币安发布的公告。作为一个区块链开发者和交易员，需要对公告内容进行区分，并根据以下的标准进行打分，最高100分。
公告重要性评判标准：API更新公告非常重要>90，交易对上新公告和交易对下架公告比较重要>70,这些交易对只需要包括现货，合约和期权三种类型即可,费率调整公告一般重要>60，理财公告稍微重要>40，交易所活动公告不重要>20，请根据这个标准打分。
如果是交易所API变动，请提取受影响的API列表。
请在公告总结中使用尽可能简练的描述。
=======
作为一个区块链开发者和交易员，需要对公告内容进行区分，并根据以下的标准进行打分，最高100分。
公告重要性评判标准：API更新中资产、账户相关接口变动公告大于90分，API更新中其他接口变动、交易对上新和交易对下架公告大于70分，费率调整公告大于60分，理财公告大于40分，交易所活动公告大于20分，请根据这个标准打分。
如果是交易所API变动，请提取受影响的API列表，否则API字段为空。
请在summary字段中使用尽可能简练的语言进行总结。
>>>>>>> faf496e (modify prompt)

>>> {requests_result} <<<
请使用如下的JSON格式返回数据
{{
  "title": "anancement title",
  "summary": "Exchange announcement text summary",
  "API": "affected API list",
  "score": A score between 0 to 100,
  "time": "announcement time",
}}
Extracted:"""