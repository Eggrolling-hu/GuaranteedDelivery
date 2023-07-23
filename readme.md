# NOTE

1. 新开一个虚拟环境 python=3.10, 最好是 conda ，包我没有统计，辛苦各位看看，自行安装一下
2. 主要看看工程结构是否需要优化
3. 代码比赛结束前别去开源了，比赛结束再决定是否开源

# 简单运行

1. 启动向量数据库

启动 docker

```shell
cd database/pure
docker compose up
```

安装完成后, 注入数据

```shell
python insert.py
```

2. 启动 ChatGLM2

```shell
cd core/models/chatglm2
python jina_server.py
```

3. 运行 main.py

```shell
python main.py
```
