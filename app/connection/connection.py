from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from tables.book_reader_tables import Book_Reader_Tables 
from crud.repository import Model_meta_data_repository, Data_set_meta_data_repository
import json

class Init_db:
    def __init__(self,path):
        with open(path,"r") as file:
            config = json.load(file)
            self.user = config["user"]
            self.pwd = config["pwd"]
            self.host = config["host"]
            self.database = config["database"]
            self.url = f"mysql+pymysql://{self.user}:{self.pwd}@{self.host}"
            self.engine = create_engine(self.url,echo=True)
            with self.engine.begin() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.database}"))
                conn.commit() 
                
            self.base = declarative_base()
            self.tables = Book_Reader_Tables(self.base,self.database)
            self.base.metadata.create_all(self.engine)

    def get_connection(self):
        return self.engine
    
    def get_repository(self):
        self.rvc_model_repository = Model_meta_data_repository(self.engine,self.tables.rvc_model)
        self.tts_model_repository = Model_meta_data_repository(self.engine,self.tables.tts_model)
        self.rvc_data_set_repository = Data_set_meta_data_repository(self.engine,self.tables.rvc_data_set)
        self.tts_data_set_repository = Data_set_meta_data_repository(self.engine,self.tables.tts_data_set)
        return self.rvc_model_repository, self.tts_model_repository, self.rvc_data_set_repository, self.tts_data_set_repository
    