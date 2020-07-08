import datetime
import threading
import os
from ..gateway import gateway
from ..model import DayKline, Favourite
from ..utils.strs import first_day_of_year


class KLiner:
    def __init__(self):
        pass
    
    @staticmethod
    def update():
        print("pid:%r tid:%r" %(os.getpid(), threading.get_ident()))
        end = datetime.datetime.today()
        # 如果数据库为空,则用今年第一天为开始
        begin = first_day_of_year(end.year)

        for fav in Favourite.list_stock():
            last = DayKline.last_time_key(fav.market_code)
            if last is None:
                pass
            elif last < end and last.day != end.day:
                begin = last + datetime.timedelta(days=1)
            else:
                continue
            for lines in gateway.get_daily_history(
                fav.market_code,
                start_date=begin,
                end_date=end
            ):
                for kline in lines:
                    kline["market_code"] = kline["code"]
                    DayKline(**kline).save()
