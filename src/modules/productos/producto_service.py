from datetime import datetime, date
from typing import Any, Dict, List, TYPE_CHECKING
from modules.productos import ProductoModel, ProductosRepository

if TYPE_CHECKING:
    from modules.db.db_connection import DbConnection

class ProductoService:
    def __init__(self, db: 'DbConnection'):
        self._repository = ProductosRepository(db)

    def get_all(self) -> List[ProductoModel]:
        """
        Retorna todos los productos en la base de datos.
        """
        return self._repository.get_all()

    def get_by_id(self, id_producto: int) -> ProductoModel:
        """
        Retorna el producto con el id especificado.

        :param id: El id del producto a buscar.
        """
        return self._repository.get_by_id(id_producto)
    
    def agregar(self, producto: Dict[str,Any]) -> ProductoModel:
        """
        Agrega un nuevo producto a la base de datos

        :param producto: Un diccionario con los datos del producto.
        """
        producto = ProductoModel(**producto)
        self._repository.agregar(producto)
        return producto
    
    def mas_vendidos(self, desde: datetime | date | str = None, hasta: datetime | date | str = None):
        """
        Retorna una lista de productos ordenados por la cantidad total vendida.

        :param desde: La fecha inicial para filtrar las ventas.
        :param hasta: La fecha final para filtrar las ventas.
        """
        productos = map(lambda x: {**x.to_dict(),  **x.total_vendido(desde,hasta)}, self.get_all())
        return sorted(productos, key=lambda x: x["importe"], reverse=True)
