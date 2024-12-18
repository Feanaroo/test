from sqlalchemy import Column, DateTime, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

config = {
    'user': 'root',
    'password': 'qwerty',
    'host': '172.17.0.2',
    'database': 'python_service',
}

Base = declarative_base()


class Result(Base):
    """
    Result class represents a record in the 'results' table.
    """
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    text = Column(String(512), nullable=False)
    ins_date = Column(DateTime, default=func.now())

    @staticmethod
    def upload(results):
        """
        Upload the given results to the database.

        :param results: A list of dictionaries containing 'number' and 'text' keys.
        """
        current_time = datetime.datetime.now().strftime('%y-%m-%d')
        delete_query = Result.__table__.delete().where(Result.ins_date > current_time)
        engine.execute(delete_query)
        objects = [Result(number=item['number'], text=item['text']) for item in results]
        session.add_all(objects)
        session.commit()

    @staticmethod
    def get_closest(number, days_ago, numbers_count):
        """
        Get the closest numbers to the given number from the database.

        :param number: The reference number.
        :param days_ago: The number of days ago to consider.
        :param numbers_count: The number of closest numbers to retrieve.
        :return: A list of Result objects.
        """
        date_from = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%y-%m-%d')
        rows = session.query(Result).filter(Result.ins_date > date_from).order_by(func.abs(Result.number - number)).limit((days_ago+1)*numbers_count*2).all()
        return rows    

class ResultViewer:
    """
    ResultViewer class to format the results for output.
    """
    def __init__(self, rows=None):
        self.rows = rows if rows is not None else []

    def output_json(self, numbers_count):
        """
        Format the results as a JSON-compatible dictionary.

        :param numbers_count: The number of results to include for each date.
        :return: A dictionary with dates as keys and dictionaries of number-text pairs as values.
        """
        output = {}
        for item in self.rows:
            key = item.ins_date.strftime('%y%m%d')
            if key not in output:
                output[key] = {}
            if len(output[key]) < numbers_count:
                output[key].update({item.number: item.text})

        return output    

def setup():
    Base.metadata.create_all(engine)

connection_str = 'mysql+pymysql://{user}:{password}@{host}/mysql'.format(**config)
engine = create_engine(connection_str)
conn = engine.connect()
conn.execute("COMMIT")
conn.execute("CREATE DATABASE IF NOT EXISTS python_service")
conn.close()
    
engine = create_engine('mysql+pymysql://{user}:{password}@{host}/{database}'.format(**config))
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
