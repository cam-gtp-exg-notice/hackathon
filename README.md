# hackathon

- 安装依赖
  - 尽量使用pip3 23.1.2, pyhton3.11
```command
    pip3 install flask
    pip3 install openai
    pip3 install langchain
    pip3 install unstructured
     pip3 install bs4
```

- rest端口: 9999
- 运行环境: mac m1 + python3
```command
    python3 .
```

## Docker 部署

```bash
# 停止容器
docker stop hackathon
# 删除容器
docker rm hackathon

# 创建镜像
docker build -t hackathon .
# 运行镜像
docker run -it -d --name hackathon hackathon
# 进入容器
docker exec -it hackathon bash
```
