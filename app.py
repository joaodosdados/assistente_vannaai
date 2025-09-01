from vanna.ollama import Ollama
from vanna.base import VannaBase

class MyCustomVectorDB(VannaBase):
  def add_ddl(self, ddl: str, **kwargs) -> str:
     # Implement here

  def add_documentation(self, doc: str, **kwargs) -> str:
     # Implement here

  def add_question_sql(self, question: str, sql: str, **kwargs) -> str:
     # Implement here

  def get_related_ddl(self, question: str, **kwargs) -> list:
     # Implement here

  def get_related_documentation(self, question: str, **kwargs) -> list:
     # Implement here

  def get_similar_question_sql(self, question: str, **kwargs) -> list:
     # Implement here

  def get_training_data(self, **kwargs) -> pd.DataFrame:
     # Implement here

  def remove_training_data(id: str, **kwargs) -> bool:
     # Implement here


class MyVanna(MyCustomVectorDB, Ollama):
    def __init__(self, config=None):
        MyCustomVectorDB.__init__(self, config=config)
        Ollama.__init__(self, config=config)

vn = MyVanna(config={'model': 'llama3:8b'})

vn.connect_to_postgres(host='my-host', dbname='my-dbname', user='my-user', password='my-password', port='my-port')