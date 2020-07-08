import abc


class ExGateway(abc.ABC):
    
    def __init__(self):
        self._app = None
    
    def init_app(self, app):
        self._app = app
    
    @abc.abstractmethod
    def get_daily_history(self, market_code, start_date, end_date):
        pass
    
    @abc.abstractmethod
    def get_sz_basic_info(self):
        pass
    
    @abc.abstractmethod
    def get_sh_basic_info(self):
        pass
