import datetime
from contextlib import contextmanager
from datetime import datetime as DateTime
from typing import List

from futu import *

from .base import ExGateway
from ..limiter import limit
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
    
    @limit(count=1, period=60 * 1000)
    def _request_history_kline(self, c, code, start: DateTime, end: DateTime,
                               page_req_key):
        return c.request_history_kline(
            code,
            start=datetime_to_day_str(start),
            end=datetime_to_day_str(end),
            page_req_key=page_req_key,
        )
    
    def get_kline_daily_history(
        self, code, start_date: datetime, end_date: datetime
    ):
        histories = []
        print("get kline:%s from %r to %r" % (code, start_date, end_date))
        page_req_key = None
        with connection() as c:
            curr_month = start_date.month
            while True:
                ret, data, page_req_key = self._request_history_kline(
                    c,
                    code,
                    start=start_date,
                    end=end_date,
                    page_req_key=page_req_key
                )
                assert ret == RET_OK, "%r, %r" % (ret, data)
                for i, row in data.iterrows():
                    date = datetime.strptime(row["time_key"], DATETIME_FORMAT)
                    if curr_month != date.month:
                        yield histories
                        histories.clear()
                        curr_month = date.month
                    else:
                        row["time_key"] = date
                        histories.append(row)
                
                if not page_req_key:
                    break
    
    def get_daily_history(
        self, market_code, start_date: datetime, end_date: datetime
    ):
        return self.get_kline_daily_history(market_code, start_date, end_date)
    
    @staticmethod
    def get_stock_basic_info(market, security_type):
        with connection() as c:
            ret, data = c.get_stock_basicinfo(market, security_type, None)
            if ret == RET_OK:
                print(data)
                print(data["name"][0])  # 取第一条的股票名称
                print(data["name"].values.tolist())  # 转为list
                return data
            else:
                return []
    
    def get_sz_basic_info(self):
        return self.get_stock_basic_info(Market.SH, SecurityType.STOCK)
    
    def get_sh_basic_info(self):
        return self.get_stock_basic_info(Market.SZ, SecurityType.STOCK)
    
    @staticmethod
    def get_global_state():
        with connection() as c:
            gs = c.get_global_state()
            return gs
    
    def get_state(self):
        return self.get_global_state()
    
    @staticmethod
    def get_kline_history_quota():
        with connection() as c:
            ret, quota = c.get_history_kl_quota(get_detail=True)
            if ret == RET_OK:
                print(quota)
            return quota
    
    def get_kline_quota(self):
        return self.get_kline_history_quota()
    
    @staticmethod
    def get_plate_stock(code):
        with connection() as c:
            ret, stocks = c.get_plate_stock(code)
            if ret == RET_OK:
                return stocks
            return []
    
    def list_stock_by_plate(self, code):
        return self.get_plate_stock(code)
    
    @staticmethod
    def get_market_snap_shot(stocks: List[str]):
        with connection() as c:
            ret, data = c.get_market_snapshot(stocks)
            if ret == RET_OK:
                return data
            return []
    
    def get_snap_shot(self, stocks: List[str]):
        if not stocks:
            return None
        return self.get_market_snap_shot(stocks)
