from flask import Flask, request, send_file
from http import HTTPStatus

class Product:
    def __init__(self, id: int, name: str, description: str = "", icon_path: str = ""):
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.icon_path: str = ""


    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon_path,
        }


products_db: list[Product] = []
def is_product_id_correct(product_id: int):
    return product_id >= 0 or product_id < len(products_db)


app = Flask(__name__)


@app.route("/product", methods=["POST"])
def post_product():
    try:
        json_product_data = request.get_json()
        name = json_product_data["name"]
        description = json_product_data["description"]
    except:
        return "Incorrect json", HTTPStatus.BAD_REQUEST

    product = Product(len(products_db), name, description)
    products_db.append(product)
    return product.to_json(), HTTPStatus.CREATED


@app.route("/product/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
    if not is_product_id_correct(product_id):
        return "Incorrect id", HTTPStatus.BAD_REQUEST
    product = products_db[product_id]
    if product is None:
        return "Product has been deleted", HTTPStatus.BAD_REQUEST
    return product.to_json(), HTTPStatus.OK


@app.route("/product/<int:product_id>", methods=["PUT"])
def put_product(product_id: int):
    if not is_product_id_correct(product_id):
        return "Incorrect id", HTTPStatus.BAD_REQUEST
    old_product = products_db[product_id]
    if old_product is None:
        return "Product has been deleted", HTTPStatus.BAD_REQUEST
    
    new_product = request.get_json()
    new_product_id = new_product.get("id")
    if new_product_id is not None and new_product_id != old_product.id:
        return "Incorrect id", HTTPStatus.BAD_REQUEST

    new_name = new_product.get("name")
    if new_name is not None:
        old_product.name = new_name

    new_description = new_product.get("description")
    if new_description is not None:
        old_product.description = new_description

    return old_product.to_json(), HTTPStatus.OK


@app.route("/product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int):
    if not is_product_id_correct(product_id):
        return "Incorrect id", HTTPStatus.BAD_REQUEST
    product = products_db[product_id]
    if product is None:
        return "Product has already been deleted", HTTPStatus.BAD_REQUEST

    products_db[product_id] = None
    return product.to_json(), HTTPStatus.OK


@app.route("/products")
def get_products():
    all_products = []
    for product in products_db:
        if product is not None:
            all_products.append(product.to_json())
    return all_products, HTTPStatus.OK


@app.route("/product/<int:product_id>/image", methods=["GET"])
def get_icon(product_id):
    if not is_product_id_correct(product_id):
        return "Incorrect id", HTTPStatus.BAD_REQUEST
    product = products_db[product_id]
    if product is None:
        return "Product has been deleted", HTTPStatus.BAD_REQUEST

    if product.icon_path is None:
        return "Product has no icon", HTTPStatus.NO_CONTENT

    return send_file(product.icon_path, as_attachment=True), HTTPStatus.OK
 

@app.route("/product/<int:product_id>/image", methods=["POST"])
def post_icon(product_id):
    if not is_product_id_correct(product_id):
        return "Incorrect id", HTTPStatus.BAD_REQUEST
    product = products_db[product_id]
    if product is None:
        return "Product has been deleted", HTTPStatus.BAD_REQUEST

    try:
        icon = request.files["icon"]
    except:
        return "Incorrect files", HTTPStatus.BAD_REQUEST

    icon_path = f'{product.id}_{icon.name}.png'

    product.icon_path = icon_path
    icon.save(icon_path)
    return product.to_json(), HTTPStatus.CREATED 
