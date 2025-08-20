from flask import Flask, render_template, request

app = Flask(__name__)

categories = []  # temporary storage

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    if request.method == 'POST':
        category_name = request.form['category_name']
        categories.append(category_name)
    return render_template("categories.html", categories=categories)
attributes = []  # temporary storage

@app.route('/attributes', methods=['GET', 'POST'])
def manage_attributes():
    if request.method == 'POST':
        attribute_name = request.form['attribute_name']
        data_type = request.form['data_type']
        attributes.append({"name": attribute_name, "type": data_type})
    return render_template("attributes.html", attributes=attributes)
products = []  # temporary storage

@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'POST':
        product_name = request.form['product_name']
        category = request.form['category']

        # Collect attributes dynamically
        product_attributes = {}
        for attr in attributes:
            field_name = f"attr_{attr['name']}"
            product_attributes[attr['name']] = request.form.get(field_name)

        products.append({
            "name": product_name,
            "category": category,
            "attributes": product_attributes
        })

    return render_template("products.html", 
                           categories=categories, 
                           attributes=attributes, 
                           products=products)
    @app.route('/catalog')
def view_catalog():
    return render_template("catalog.html", products=products)




if __name__ == '__main__':
    app.run(debug=True)
