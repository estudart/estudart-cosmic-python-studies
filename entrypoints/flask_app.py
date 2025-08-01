from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import domain.model as model
import service_layer.services as services
from adapters import (
    SQLAlchemyRepository,
    start_mappers
)



start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    batches = SQLAlchemyRepository(session).list()
    line = model.OrderLine(
        request.json["order_id"], request.json["sku"], request.json["qty"],
    )

    try:
        batchref = services.allocate(line, batches)
    except services.InvalidSku as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201
