import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

default_connection_string = ""

class StockDbConnection:
    def __init__(self, connection_string):
        self.logger = logging.getLogger(__name__ + ".StockDbConnection")
#        self.engine = create_engine('sqlite:///%s' % filename)
        self.engine = create_engine(
            connection_string,
            pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)
        self.conn = None
        return
    
    def get_engine(self):
        return self.engine
    
    def get_sessionmake(self):
        return self.Session

    def create_session(self):
        '''
            create_session
        '''
        session = self.Session()
        return session

DB_CONN = None

def get_default_db_connection():
    global DB_CONN
    if (DB_CONN is None):
        DB_CONN = StockDbConnection(default_connection_string)
    #edit from droidedit
    return DB_CONN

