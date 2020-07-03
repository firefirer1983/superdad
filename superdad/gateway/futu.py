import datetime
from contextlib import contextmanager

from futu import *

from .base import ExGateway
from ..utils.strs import datetime_to_day_str

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
FUTU_OPEND_HOST = "127.0.0.1"
FUTU_OPEND_PORT = 11111
MAX_DAY_PER_MONTH = 31


@contextmanager
def connection():
    conn = OpenQuoteContext(host=FUTU_OPEND_HOST, port=FUTU_OPEND_PORT)
    yield conn
    conn.close()


class FutuGateway(ExGateway):
    
    @staticmethod
    def get_kline_daily_history(code, start_date: datetime,
                                end_date: datetime):
        histories = []
        print("get kline:%s from %r to %r" % (code, start_date, end_date))
        page_req_key = None
        with connection() as c:
            curr_month = start_date.month
            while True:
                ret, data, page_req_key = c.request_history_kline(
                    code,
                    start=datetime_to_day_str(start_date),
                    end=datetime_to_day_str(end_date),
                    max_count=MAX_DAY_PER_MONTH,
                    page_req_key=page_req_key
                )
                assert ret == RET_OK, "%r, %r" % (ret, data)
                for i, date in enumerate(data["time_key"].values.tolist()):
                    date = datetime.strptime(date, DATETIME_FORMAT)
                    if curr_month != date.month:
                        yield curr_month, histories
                        histories.clear()
                        curr_month = date.month
                    else:
                        histories.append(
                            [date, data["open"][i], data["close"][i]])
                
                if not page_req_key:
                    break
    
    def get_daily_history(self, market, code, start_date: datetime,
                          end_date: datetime):
        code = "%s.%s" % (market, code)
        return self.get_kline_daily_history(code, start_date, end_date)
    
    @staticmethod
    def get_stock_basic_info(market, security_type):
        with connection() as c:
            ret, data = c.get_stock_basicinfo(market, security_type, None)
            if ret == RET_OK:
                print(data)
                print(data['name'][0])  # 取第一条的股票名称
                print(data['name'].values.tolist())  # 转为list
                return data
            else:
                return []
    
    def get_sz_basic_info(self):
        return self.get_stock_basic_info(Market.SH, SecurityType.STOCK)
    
    def get_sh_basic_info(self):
        return self.get_stock_basic_info(Market.SZ, SecurityType.STOCK)
