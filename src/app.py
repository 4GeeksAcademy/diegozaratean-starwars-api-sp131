"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Empresa
from sqlalchemy import select
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    print('prueba')
    all_users = User.query.all()
    print(all_users)
    results = list(map(lambda usuario: usuario.serialize() ,all_users))
    print(results)
    

    response_body = {
        "msg": "esto son tus usuarios",
        "users": results
    }

    return jsonify(response_body), 200

@app.route('/test', methods=['GET'])
def test():

    response_body = {
        "msg": "test "
    }

    return jsonify(response_body), 200



@app.route('/company', methods=['GET'])
def get_companies():
    # all_companies = Empresa.query.all()
    all_companies = db.session.execute(select(Empresa)).scalars().all()
    results = list(map(lambda company: company.serialize() ,all_companies))

    return jsonify(results), 200


@app.route('/company/<int:company_id>', methods=['GET'])
def get_company(company_id):
    # company = Empresa.query.filter_by(id = company_id).first()
    # company = db.session.execute(select(Empresa).where(Empresa.id == company_id)).scalar_one_or_none()
    company = db.session.get(Empresa, company_id)

    return jsonify(company.serialize()), 200

@app.route('/company', methods=['POST'])
def post_company():
    body = request.get_json()
    if "nombre" not in body:
        return "Debes enviar el nombre", 400
    if body["nombre"] == "":
        return  {
        "msg": "El nombre no puede ser vacio "
    }, 400
    print(request.get_json()["nombre"])
    company = Empresa(**body)
    db.session.add(company)
    db.session.commit()

    response_body = {
        "msg": "se creo la empreas",
        "company": company.serialize()
    }


    return jsonify(response_body), 200

@app.route('/company/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    # company = Empresa.query.filter_by(id = company_id).first()
    # company = db.session.execute(select(Empresa).where(Empresa.id == company_id)).scalar_one_or_none()
    company = db.session.get(Empresa, company_id)
    if company is None:
        return {
        "msg": "erro eleminando la emrepsa",
        "msd_error": f"no se encontro la emprea con el id {company_id}" 
    }, 400
    db.session.delete(company)
    db.session.commit()
    response_body = {
        "msg": "se eliminio la empreas",
        "company": company.serialize()
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
