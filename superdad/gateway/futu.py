from contextlib import contextmanager
from ..utils.strs import str_to_datetime, datetime_to_day_str, tomorrow_in_str
from futu import *

FUTU_OPEND_HOST = "127.0.0.1"
FUTU_OPEND_PORT = 11111


@contextmanager
def connection():
    conn = OpenQuoteContext(host=FUTU_OPEND_HOST, port=FUTU_OPEND_PORT)
    yield conn
    conn.close()


class FutuGateway:
    
    @staticmethod
    def get_kline_by_days(code, from_date: str, to_date: str):
        histories = []
        print("get kline:%s from %r to %r" % (code, from_date, to_date))
        with connection() as c:
            ret, data, page_req_key = c.request_history_kline(
                code, start=from_date, end=to_date, max_count=5)  # 每页5个，请求第一页
            print(data)
            if ret == RET_OK:
                histories.append(data)
                from_date = tomorrow_in_str(from_date)
                if from_date >= to_date:
                    return histories
            
            while page_req_key:  # 请求后面的所有结果
                ret, data, page_req_key = c.request_history_kline(
                    code,
                    start=from_date,
                    end=to_date,
                    max_count=31,
                    page_req_key=page_req_key
                )
                if ret == RET_OK:
                    histories.append(data)
                else:
                    return []
            return histories
