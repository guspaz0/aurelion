from inspect import _void
import os, csv
import pathlib
from typing import Any, Dict, List
from .producto_model import ProductoModel
from .productos_dao import ProductosDao

class ProductosRepository:
    def __init__(self):
        self._dao = ProductosDao()
        self.categorias = set()

    def get_all(self) -> List[ProductoModel]:
        """
        Returns all products from the database.
        """
        return [ProductoModel(*row) for row in self._dao.get_all()]

    def get_by_id(self, id: int) -> ProductoModel:
        """
        Returns the product with the given id.
        """
        return ProductoModel(*self._dao.get_by_id(id))
    
    def agregar(self, producto: ProductoModel) -> _void:
        """
        Adds a new product to the database.

        :param producto: The product to add.
        """
        self._dao.insert_product(**producto.to_dict())
