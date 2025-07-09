import model



def test_orderline_mapper_can_load_lines(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES"
        '("order1", "BIG-CHAIR", 10),'
        '("order2", "MAJESTIC-TABLE", 4),'
        '("order3", "SMALL-LAMP", 7),'
    )

    expected = [
        model.OrderLine("order1", "BIG-CHAIR", 10),
        model.OrderLine("order2", "MAJESTIC-TABLE", 4),
        model.OrderLine("order3", "SMALL-LAMP", 7)
    ]

    assert session.query(model.OrderLine).all() == expected

def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute('SELECT orderid, sku, qty FROM "order_lines"'))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]
