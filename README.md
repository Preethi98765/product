Product Catalog Tool

A simple internal tool to manage Categories, Attributes, and Products.
This project demonstrates database design, class design, and a working Flask web app.

 Features

Manage Categories (e.g., Electronics, Clothing)

Define Attributes for each category (e.g., Size, Color, Warranty)

Add and list Products

Simple Web Dashboard using Flask + HTML

Tech Stack

Backend: Python (Flask)

Frontend: HTML + CSS (Bootstrap)

Database: SQLite (lightweight, file-based DB)

Version Control: Git + GitHub

Documentation
 Database ERD (Entity Relationship Diagram)

Category → CategoryID, Name

Attribute → AttributeID, Name, CategoryID

Product → ProductID, Name, CategoryID

ProductAttributeValue → Value for each product’s attribute

 Class Design (UML Diagram)

Category: addCategory(), getCategories()

Attribute: addAttribute(), getAttributes()

Product: addProduct(), getProducts()

 Author

Developed by Preethi...!