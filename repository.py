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
    def __init__(self, session):
        self.session = session

    def add(self, batch: model.Batch) -> bool:
        return self.session.add(batch)
    
    def get(self, reference: str) -> model.Batch:
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()
