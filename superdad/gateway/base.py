import abc


class ExGateway(abc.ABC):
    
    @abc.abstractmethod
    def get_daily_history(self, market, code, start_date, end_date):
        pass
    
    @abc.abstractmethod
    def get_sz_basic_info(self):
        pass
    
    @abc.abstractmethod
    def get_sh_basic_info(self):
        pass
