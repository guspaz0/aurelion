from inspect import _void
from typing import Any, Dict, List, TYPE_CHECKING
from .producto_model import ProductoModel

if TYPE_CHECKING:
    from modules.db.db_connection import DbConnection

class ProductosRepository:
    def __init__(self, db: 'DbConnection'):
        self._db = db
        self.categorias = db.productosDao.get_categorias()

    def get_all(self) -> List[ProductoModel]:
        """
        Returns all products from the database.
        """
        return self._db.productosDao.get_all()

    def get_by_id(self, id: int) -> ProductoModel:
        """
        Returns the product with the given id.
        """
        return self._db.productosDao.get_by_id(id)
    
    def agregar(self, producto: ProductoModel) -> _void:
        """
        Adds a new product to the database.

        :param producto: The product to add.
        """
        self._db.productosDao.insert_product(**producto.to_dict())
