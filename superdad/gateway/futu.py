import datetime
from contextlib import contextmanager

from futu import *

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


class FutuGateway:
    
    @staticmethod
    def get_kline_by_month(code, from_date: datetime, to_date: datetime):
        histories = []
        print("get kline:%s from %r to %r" % (code, from_date, to_date))
        page_req_key = None
        with connection() as c:
            curr_month = from_date.month
            while True:
                ret, data, page_req_key = c.request_history_kline(
                    code,
                    start=datetime_to_day_str(from_date),
                    end=datetime_to_day_str(to_date),
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
