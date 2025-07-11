import abc

import model



class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get(self, referenc: str) -> model.Batch:
        raise NotImplementedError
    

class SQLAlchemyRepository(AbstractRepository):
    def add(self, batch: model.Batch) -> bool:
        return
    
    def get(self, reference: str) -> model.Batch:
        return