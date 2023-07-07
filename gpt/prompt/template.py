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

# URLTemplate = """在 >>> 和 <<< 之间是网页的返回的HTML内容的总结和评分。
# 作为区块链开发者和交易员，我们根据以下标准对公告进行评分：API更新中资产、账户相关接口变动公告大于90分，API更新中其他接口变动、交易对上新和下架公告大于70分，费率调整公告大于60分，理财公告大于40分，交易所活动公告大于20分。如果是交易所API变动，我们会提取受影响的API列表。
# 根据这些标准，请给出了公告的评分和总结。

# >>> {requests_result} <<<
# 请使用如下的JSON格式返回数据
# {{
#   "title": "公告标题",
#   "summary": "公告内容简述总结",
#   "API": "受影响的API列表",
#   "score": 评分结果（0-100分）,
#   "time": "公告发布时间",
# }}
# Extracted:"""

URLTemplate="""Between >>> and <<< is the HTML content returned by a webpage.
As a blockchain developer and trader, we evaluate announcements based on the following criteria:

API updates related to assets and accounts: score 90-100.
API updates related to other interfaces, new trading pairs, and delisting announcements: score 70-90.
fee adjustment announcements: score 60-70.
financial management announcements: score 40-60.
exchange activity announcements: score 20-40.
others: 0~20.

If it is an exchange API update, we will extract the affected API list.
Based on these criteria, please provide the score and summary of the announcement.

>>> {requests_result} <<<
Please use the following JSON format to return the data:
{{
  "title": "announcement title",
  "summary": "Exchange announcement text summary, use concise descriptions",
  "API": "affected API list, empty if no affected",
  "score": A score between 0 to 100,
  "time": "announcement time",
}}
Extracted:"""