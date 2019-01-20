# coding=utf-8
import logging

import requests

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

f_handler = logging.FileHandler('stock.log')
f_handler.setLevel(logging.INFO)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

s_handler = logging.StreamHandler()
s_handler.setLevel(logging.DEBUG)
s_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(f_handler)
logger.addHandler(s_handler)


class stock(object):
    def __init__(self, stock_zone, stock_code, lower_price, higher_price):
        self.stock_zone = stock_zone
        self.stock_code = stock_code
        self.lower_price = lower_price
        self.higher_price = higher_price


class dint_msg(object):
    def __init__(self, text, msgtype='text', at={}):
        self.text = text
        self.msgtype = msgtype
        self.at = at


DING_URL = "https://oapi.dingtalk.com/robot/send?access_token=5c2d9902a29b263176e1d6935b300019bf94b256570c5328fa1719da6c77b44a"


def send_ding_message(msg):
    # 第一种方式 通过json指定，直接传能转json对象即可
    response = requests.post(DING_URL, json=dint_msg({'content': msg}).__dict__)
    logger.info(response)

    # 第二种 ，设置header，data传json字符串
    # headers = {'Content-Type': 'application/json; charset=utf-8'}
    # response2 = requests.post(DING_URL, data=json.dumps(dint_msg({'content': msg}).__dict__), headers = headers)
    # print response2


def analysis_stock(stock):
    url = 'http://hq.sinajs.cn/list=' + stock.stock_zone + stock.stock_code
    response = requests.get(url)
    logger.info("sina返回信息：" + str(response))
    if response.status_code == 200:
        data = response.text.split("=")[1].split(',')
        name = data[0].encode("utf-8")[1:]
        current_price = float(data[3])
        if current_price < stock.lower_price:
            send_ding_message('跌了！！！ %s当前价格:%f' % (name, current_price))
        elif current_price >= stock.higher_price:
            send_ding_message('涨了！！！ %s当前价格:%f' % (name, current_price))


if __name__ == '__main__':
    logger.info("开始了")
    stock_tuowei = stock('sz', '002261', 4.5, 5.0)
    stock_360 = stock('sh', '601360', 20.0, 22.0)

    analysis_stock(stock_tuowei)
    analysis_stock(stock_360)
    logger.info("结束了")
