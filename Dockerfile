FROM python:3.10
WORKDIR /gpt
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENV OPENAI_API_BASE=https://api.openai-sb.com/v1
ENV OPENAI_API_KEY=sb-29b8d019e623a4b6e4dbbbd0dff3d9b78cc8dffd7fab6248

CMD [ "python3", "."]
