import domain.model as model
import adapters.repository as repository



class InvalidSku(Exception):
    pass

def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(
        orderid: str, sku: str, qty: int, 
        repo: repository.AbstractRepository, session
    ) -> str:
    batches = repo.list()
    line = model.OrderLine(orderid, sku, qty)
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref

def deallocate(
        orderid: str, sku: str, qty: int, 
        repo: repository.AbstractRepository, session
    ) -> str:
    batches = repo.list()
    line = model.OrderLine(orderid, sku, qty)
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.deallocate(line, batches)
    session.commit()
    return batchref
