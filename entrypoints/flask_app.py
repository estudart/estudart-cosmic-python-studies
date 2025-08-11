from datetime import datetime

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from domain import model
from service_layer import services, unit_of_work
from adapters import orm



orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/batch", methods=["POST"])
def add_batch_endpoint():
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    services.add_batch(
        request.json["order_id"], 
        request.json["sku"], 
        request.json["qty"],
        eta,
        unit_of_work.SqlAlchemyUnitOFWork(),
    )
    return "OK", 201

@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    try:
        batchref = services.allocate(
            request.json["order_id"], 
            request.json["sku"], 
            request.json["qty"],
            unit_of_work.SqlAlchemyUnitOFWork(),
        )
    except (model.OutofStock, services.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201
