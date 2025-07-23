from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import model
import orm
import repository



orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    batches = repository.SQLAlchemyRepository(session).list()
    line = model.OrderLine(
        request.json["order_id"], request.json["sku"], request.json["qty"],
    )

    if not is_valid_sku(line.sku, batches):
        return {"message": f"Inavlid sku {line.sku}"}, 400

    try:
        batchref = model.allocate(line, batches)
    except model.OutofStock as e:
        return {"message": str(e)}, 400

    session.commit()
    return {"batchref": batchref}, 201