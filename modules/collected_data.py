class collected_data:
    def __init__(self, user_name: str, movie_name: str, date: str, vas_list:list):
        self._user_name = user_name
        self._movie_name = movie_name
        self._date = date
        self._vas_list = vas_list
        
    def get_user_name(self) :
        return self._user_name
    
    def get_movie_name(self) :
        return self._movie_name
    
    def get_date(self) :
        return self._date
        
    def get_vas_list(self) :
        return self._vas_list
    