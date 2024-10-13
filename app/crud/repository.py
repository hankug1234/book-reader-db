from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete


class Base_repository:
    def __init__(self,connection):
        self.connection = connection
    
    def insert(self,datas):
        with Session(self.connection) as session:
            session.add_all(datas)
            session.commit()
    
    def delete(self,stmt):
        with Session(self.connection) as session:
            session.execute(stmt)
            session.commit()
            
    def select(self,stmt):
        with Session(self.connection) as session:
            return [client[0] for client in session.execute(stmt)]
        
    def update(self,stmt):
        with Session(self.connection) as session:
            session.execute(stmt)
            session.commit()

class Model_meta_data_repository:
    def __init__(self,connection,table):
        self.table = table
        self.base_repository = Base_repository(connection)
        
    def select_by_page(self,start,offset):
        stmt = select(self.table).limit(offset).offset(start)
        return self.base_repository.select(stmt)
    
    def select_by_id(self,id):
        stmt = select(self.table).where(self.table.model_id == id)
        return self.base_repository.select(stmt)
    
    def select_all(self):
        stmt = select(self.table)
        return self.base_repository.select(stmt)
    
    def delete_by_id(self,id):
        stmt = delete(self.table).where(self.table.model_id == id)
        self.base_repository.delete(stmt)
    
    def delete_all(self):
        stmt = delete(self.table)
        self.base_repository.delete(stmt)
    
    def insert(self,datas):
        self.base_repository.insert(datas)
    
    def update(self,data):
        values = data.asDict()
        del values['_sa_instance_state']
        stmt = insert(self.table).values(**values)
        stmt = stmt.on_conflict_do_update(index_elements=['model_id'],set_=data)
        self.base_repository.update(stmt)

class Data_set_meta_data_repository:
    def __init__(self,connection,table):
        self.table = table
        self.base_repository = Base_repository(connection)
        
    def select_by_page(self,start,offset):
        stmt = select(self.table).limit(offset).offset(start)
        return self.base_repository.select(stmt)
    
    def select_by_id(self,id):
        stmt = select(self.table).where(self.table.data_set_id == id)
        return self.base_repository.select(stmt)
    
    def select_all(self):
        stmt = select(self.table)
        return self.base_repository.select(stmt)
    
    def delete_by_id(self,id):
        stmt = delete(self.table).where(self.table.data_set_id == id)
        self.base_repository.delete(stmt)
    
    def delete_all(self):
        stmt = delete(self.table)
        self.base_repository.delete(stmt)
    
    def insert(self,datas):
        self.base_repository.insert(datas)
    
    def update(self,data):
        values = data.asDict()
        del values['_sa_instance_state']
        stmt = insert(self.table).values(**values)
        stmt = stmt.on_conflict_do_update(index_elements=['data_set_id'],set_=data)
        self.base_repository.update(stmt)