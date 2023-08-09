from opencc import OpenCC


# 初始化转换器，s2t表示简体转繁体，t2s表示繁体转简体
cc = OpenCC('t2s')


def convert(s: str) -> str:
    return cc.convert(s)
