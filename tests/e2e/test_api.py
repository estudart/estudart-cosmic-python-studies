import pytest

import requests

import config

def random_sku(sku = None):
    return sku if sku else "random_sku"

def random_batchref(ref = None):
    return str(ref) if ref else "random_batchref"

def random_orderid(order_id):
    return order_id if order_id else "random_orderid"

def post_to_add_batch(ref, sku, qty, eta):
    url = config.get_api_url()
    r = requests.post(
        url=f"{url}/allocate",
        json={
            "order_id": ref,
            "sku": sku,
            "qty": qty,
            "eta": eta,
        }
    )
    assert r.status_code == 200

@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_200_and_allocated_batch():
    sku, othersku = random_sku(), random_sku("other")
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    post_to_add_batch(laterbatch, sku, 100, "2011-01-02")
    post_to_add_batch(earlybatch, sku, 100, "2011-01-01")
    post_to_add_batch(otherbatch, othersku, 100, None)

    url = config.get_api_url()
    r = requests.post(
        f"{url}/allocate", 
        json={
            "orderid": random_orderid(), 
            "sku": sku, 
            "qty": 3
        }
    )

    assert r.status_code == 201
    assert r.json()["batchref"] == earlybatch

@pytest.mark.usefixtures("restart_api")
def test_allocations_are_persisted(add_stock):
    sku = random_sku()
    batch1, batch2 = random_batchref(1), random_batchref(2)
    order1, order2 = random_orderid(1), random_orderid(2)
    post_to_add_batch(batch1, sku, 100, "2011-01-02")
    post_to_add_batch(batch2, sku, 100, "2011-01-01")
    line1 = {"orderid": order1, "sku": sku, "qty": 10}
    line2 = {"orderid": order2, "sku": sku, "qty": 10}
    url = config.get_api_url()

    r = requests.post(f"{url}/allocate", json=line1)
    assert r.status_code == 201
    assert r.json()["batchref"] == batch1

    r = requests.post(f"{url}/allocate", json=line2)
    assert r.status_code == 201
    assert r.json()["batchref"] == batch2

@pytest.mark.usefixtures("restart_api")
def test_400_message_for_out_of_stock(add_stock):
    sku, small_batch, large_order = random_sku(), random_batchref(), random_orderid()
    post_to_add_batch(small_batch, sku, 10, "2011-01-01")

    url = config.get_api_url()
    r = requests.post(
        url=f"{url}/allocate", 
        json={
            "orderid": large_order, 
            "sku": sku, 
            "qty": 20
        }
    )

    assert r.status_code == 400
    assert r.json()["message"] == f"Out of stock for sku {sku}"

@pytest.mark.usefixtures("restart_api")
def test_400_message_for_invalid_sku():
    orderid, unknown_sku = random_orderid(), random_sku()
    url = config.get_api_url()
    r = requests.post(
        url=f"{url}/allocate", 
        json={
            "orderid": orderid, 
            "sku": unknown_sku, 
            "qty": 10
        }
    )

    assert r.status_code == 400
    assert r.json()["message"] == f"Inavlid sku {unknown_sku}"

@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_201_and_allocated_batch(add_stock):
    sku, othersku = random_sku(), random_sku("other")
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    post_to_add_batch(laterbatch, sku, 100, "2011-01-02")
    post_to_add_batch(earlybatch, sku, 100, "2011-01-01")
    post_to_add_batch(otherbatch, othersku, 100, None)

    url = config.get_api_url()
    r = requests.post(
        url=f"{url}/allocate", 
        json={
            "orderid": random_orderid(), 
            "sku": sku, 
            "qty": 3
        }
    )

    assert r.status_code == 201
    assert r.json()["batchref"] == earlybatch


@pytest.mark.usefixtures("restart_api")
def test_unhappy_path_returns_400_and_error_message():
    unknown_sku, orderid = random_sku(), random_orderid()
    data = {"orderid": orderid, "sku": unknown_sku, "qty": 20}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)
    assert r.status_code == 400
    assert r.json()["message"] == f"Invalid sku {unknown_sku}"