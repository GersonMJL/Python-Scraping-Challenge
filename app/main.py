from fastapi import FastAPI
from controllers import main

app = FastAPI()


@app.get("/list_products")
def list_products():
    """Returns a list with all products in the page,
    for now working with one paremeter at a time
    """
    return main.list_products()
