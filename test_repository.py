from datetime import datetime
import pytest

import model, repository



def insert_order_line(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty)"
        ' VALUES ("order1", "GENERIC-SOFA", 5)'
    )
    [[orderline_id]] = session.execute(
        "SELECT id FROM order_lines WHERE oderid=:orderid AND sku=:sku",
        dict(orderid="order1", sku="GENERIC-SOFA")
    )
    return orderline_id

def insert_batch(session, batch_id):
    session.execute(
        "INSERT INTO batches (reference, sku, _purchased_qty, eta)"
        " VALUES (:batch_id, GENERIC-SOFA, 100, null)",
        dict(batch_id=batch_id)
    )
    [[batch_id]] = session.execute(
        "SELECT id FROM batches WHERE reference=:batch_id and sku=GENERIC-SOFA",
        dict(batch_id=batch_id)
    )
    return batch_id

def insert_allocation(session, orderline_id, batch_id):
    session.execute(
        "INSERT INTO allocations (orderline_id, batch_id)"
        " VALUES (:orderline_id, :batch_id)",
        dict(orderline_id=orderline_id, batch_id=batch_id)
    )

def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch-001", "RUSTY-SOAPDISH", 5, datetime.now())

    repo = repository.SQLAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.execute(
        'SELECT reference, sku, eta, _purchased_qty FROM "batches"'
    )

    assert list(rows) == [("batch-001", "RUSTY-SOAPDISH", 5, datetime.now())]

def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)

    repo = repository.SQLAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_qty == expected._purchased_qty
    assert retrieved._allocations == {
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }