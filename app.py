from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary in-memory database (dictionary lists)
categories = []

@app.route('/')
def home():
    return "Product Catalog Tool Working!"

# ✅ 1. Add Category
@app.route('/category', methods=['POST'])
def add_category():
    data = request.json
    category = {
        "id": len(categories) + 1,
        "name": data.get("name")
    }
    categories.append(category)
    return jsonify({"message": "Category added successfully!", "category": category})

# ✅ 2. List Categories
@app.route('/category', methods=['GET'])
def list_categories():
    return jsonify(categories)


if __name__ == '__main__':
    app.run(debug=True)
