import datetime
from ..model import DayKline, Favourite
from ..utils.strs import datetime_to_day_str
from ..gateway import gateway


class KLiner:
    def __init__(self):
        pass
    
    def update(self):
        today = datetime.datetime.now()
        last = DayKline.last_time_key()
        if last < today and last.day != today.day:
            for fav in Favourite.list_stock():
                gateway.get_daily_history(fav.market_code, start_date=last)
        
