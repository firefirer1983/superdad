from datetime import datetime as DateTime
from ..model import DayKline, Favourite, DayTrend
from sqlalchemy.exc import IntegrityError


class Trendy:
    def __init__(self):
        pass

    @staticmethod
    def process():
        for fav in Favourite.list_stock():
            histories = DayKline.list_history(market_code=fav.market_code)
            break_point = DayTrend.last_time_key(fav.market_code)
            for i, dat in enumerate(histories):

                if i == 0:
                    continue

                if break_point and dat.time_key <= break_point:
                    continue
                    
                trend = DayTrend()
                trend.market_code = dat.market_code
                trend.time_key = dat.time_key
                trend.price_up = dat.close > histories[i - 1].close
                trend.volume_up = dat.volume > histories[i - 1].volume
                print("save %s %r" % (trend.market_code, trend.time_key))
                trend.save()
