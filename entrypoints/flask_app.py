from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import domain.model as model
import service_layer.services as services
from adapters import repository, orm



orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)

    try:
        batchref = services.allocate(
            request.json["order_id"], 
            request.json["sku"], 
            request.json["qty"], 
            repo, 
            session,
        )
    except (model.OutofStock, services.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201
