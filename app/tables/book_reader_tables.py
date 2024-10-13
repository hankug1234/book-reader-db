from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String,Text
from sqlalchemy.orm import relationship

class Book_Reader_Tables:
    def __init__(self,base,database):
        self.base = base 
        self.database = database
        self.rvc_data_set, self.tts_data_set, self.rvc_model,self.tts_model  = self._make_meta_data_table()
    
    def _make_meta_data_table(self):
        
        class Rvc_data_set_meta_data(self.base):
            
            __tablename__ = "rvc_data_set_meta_data"
            __table_args__ = {'schema': self.database} 
            
            data_set_name = Column(String(200))
            description = Column(Text)
            data_set = Column(String(200))
            data_set_id = Column(String(200),primary_key=True)
            
            model = relationship("Rvc_model_meta_data",back_populates="data_set")
            
            def asJson(self):
                return {c.name: getattr(self, c.name) for c in self.__table__.columns}
            def asDict(self):
                return self.__dict__
            def __repr__(self):
                return f"{self.__tablename__}({','.join([f'{c.name}={getattr(self, c.name)}' for c in self.__table__.columns])})"
        
        class Tts_data_set_meta_data(self.base):
            
            __tablename__ = "tts_data_set_meta_data"
            __table_args__ = {'schema': self.database} 
            
            data_set_name = Column(String(200))
            description = Column(Text)
            data_set = Column(String(200))
            file_list = Column(String(200))
            config  = Column(String(200))
            data_set_id = Column(String(200),primary_key=True)
            
            model = relationship("Tts_model_meta_data",back_populates="data_set")
            
            def asJson(self):
                return {c.name: getattr(self, c.name) for c in self.__table__.columns}
            def asDict(self):
                return self.__dict__
            def __repr__(self):
                return f"{self.__tablename__}({','.join([f'{c.name}={getattr(self, c.name)}' for c in self.__table__.columns])})"
        
        class Rvc_model_meta_data(self.base):
            
            __tablename__ = "rvc_model_meta_data"
            __table_args__ = {'schema': self.database} 
            
            id = Column(String(200),primary_key=True)
            name = Column(String(200))
            batch_size = Column(Integer)
            save_epoch = Column(Integer)
            total_epoch = Column(Integer)
            image = Column(Text)
            image_name = Column(String(200))
            data_set_id = Column(String(200),ForeignKey("book_reader.rvc_data_set_meta_data.data_set_id"))
            test_script = Column(String(200))
            
            data_set = relationship("Rvc_data_set_meta_data",back_populates="model")
            
            def asJson(self):
                return {c.name: getattr(self, c.name) for c in self.__table__.columns}
            def asDict(self):
                return self.__dict__
            def __repr__(self):
                return f"{self.__tablename__}({','.join([f'{c.name}={getattr(self, c.name)}' for c in self.__table__.columns])})"
            
            
        class Tts_model_meta_data(self.base):
            
            __tablename__ = "tts_model_meta_data"
            __table_args__ = {'schema': self.database} 
            
            id = Column(String(200),primary_key=True)
            name = Column(String(200))
            batch_size = Column(Integer)
            save_epoch = Column(Integer)
            total_epoch = Column(Integer)
            image = Column(Text)
            image_name = Column(String(200))
            data_set_id = Column(String(200),ForeignKey("book_reader.tts_data_set_meta_data.data_set_id"))
            language = Column(String(200))
            test_script = Column(String(200))
            
            data_set = relationship("Tts_data_set_meta_data",back_populates="model")
            
            def asJson(self):
                return {c.name: getattr(self, c.name) for c in self.__table__.columns}
            def asDict(self):
                return self.__dict__
            def __repr__(self):
                return f"{self.__tablename__}({','.join([f'{c.name}={getattr(self, c.name)}' for c in self.__table__.columns])})"
            
            
        return Rvc_data_set_meta_data,Tts_data_set_meta_data, Rvc_model_meta_data,Tts_model_meta_data    
            