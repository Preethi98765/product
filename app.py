from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage (simple-a keep pannrom)
categories = []              # [{id, name}]
attributes = []              # [{id, category_id, code, label, data_type, options(list or None), is_required}]
products = []                # [{id, category_id, sku, name}]
product_values = {}          # { product_id: { attr_code: value } }

# Helpers
def get_next_id(items): return (items[-1]["id"] + 1) if items else 1
def find_category(cid): return next((c for c in categories if c["id"] == cid), None)
def find_attr_by_code(cid, code): 
    return next((a for a in attributes if a["category_id"] == cid and a["code"] == code), None)
def find_product(pid): return next((p for p in products if p["id"] == pid), None)

@app.route("/")
def home():
    return "Product Catalog Tool Working!"

# ---------- Categories ----------
@app.route("/category", methods=["POST"])
def add_category():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    # prevent duplicates by name (simple)
    if any(c["name"].lower() == name.lower() for c in categories):
        return jsonify({"error": "category already exists"}), 400
    cat = {"id": get_next_id(categories), "name": name}
    categories.append(cat)
    return jsonify({"message": "Category added successfully!", "category": cat})

@app.route("/category", methods=["GET"])
def list_categories():
    return jsonify(categories)

# ---------- Attributes (per category) ----------
# Allowed data types for demo: string | int | decimal | bool | enum
ALLOWED_TYPES = {"string", "int", "decimal", "bool", "enum"}

@app.route("/category/<int:category_id>/attributes", methods=["POST"])
def add_attribute(category_id: int):
    cat = find_category(category_id)
    if not cat:
        return jsonify({"error": "category not found"}), 404
    data = request.get_json(force=True)
    code = (data.get("code") or "").strip()
    label = (data.get("label") or "").strip()
    data_type = (data.get("data_type") or "").strip().lower()
    options = data.get("options")  # for enum: list[str]
    is_required = bool(data.get("is_required", False))

    if not code or not label or data_type not in ALLOWED_TYPES:
        return jsonify({"error": "code, label and valid data_type are required"}), 400
    if find_attr_by_code(category_id, code):
        return jsonify({"error": "attribute code already exists in this category"}), 400
    if data_type == "enum":
        if not isinstance(options, list) or not options:
            return jsonify({"error": "enum requires non-empty 'options' list"}), 400
        # normalize options
        options = [str(o).strip() for o in options if str(o).strip()]

    attr = {
        "id": get_next_id(attributes),
        "category_id": category_id,
        "code": code,
        "label": label,
        "data_type": data_type,
        "options": options if data_type == "enum" else None,
        "is_required": is_required
    }
    attributes.append(attr)
    return jsonify({"message": "Attribute added", "attribute": attr})

@app.route("/category/<int:category_id>/attributes", methods=["GET"])
def list_attributes(category_id: int):
    if not find_category(category_id):
        return jsonify({"error": "category not found"}), 404
    result = [a for a in attributes if a["category_id"] == category_id]
    return jsonify(result)

# ---------- Products ----------
@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json(force=True)
    category_id = int(data.get("category_id", 0))
    sku = (data.get("sku") or "").strip()
    name = (data.get("name") or "").strip()

    if not category_id or not sku or not name:
        return jsonify({"error": "category_id, sku, name are required"}), 400
    if not find_category(category_id):
        return jsonify({"error": "invalid category_id"}), 400
    if any(p["sku"].lower() == sku.lower() for p in products):
        return jsonify({"error": "sku already exists"}), 400

    prod = {"id": get_next_id(products), "category_id": category_id, "sku": sku, "name": name}
    products.append(prod)
    product_values[prod["id"]] = {}
    return jsonify({"message": "Product created", "product": prod})

@app.route("/products", methods=["GET"])
def list_products():
    # include values in response for convenience
    result = []
    for p in products:
        vals = product_values.get(p["id"], {})
        result.append({**p, "values": vals})
    return jsonify(result)

# ---------- Set/Get attribute values for a product ----------
def _validate_type(attr, value):
    dt = attr["data_type"]
    if dt == "string":
        return isinstance(value, str)
    if dt == "int":
        return isinstance(value, int)
    if dt == "decimal":
        return isinstance(value, (int, float))
    if dt == "bool":
        return isinstance(value, bool)
    if dt == "enum":
        return isinstance(value, str) and value in (attr["options"] or [])
    return False

@app.route("/products/<int:product_id>/values", methods=["POST"])
def set_product_values(product_id: int):
    prod = find_product(product_id)
    if not prod:
        return jsonify({"error": "product not found"}), 404

    data = request.get_json(force=True)
    values = data.get("v
