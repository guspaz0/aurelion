import csv
import os
from typing import List, TYPE_CHECKING
from modules.ventas.repository.detalle_ventas_repository import DetalleVentasRepository

if TYPE_CHECKING:
    from modules.ventas.models.detalle_venta_model import DetalleVentaModel
    from modules.db.db_connection import DbConnection

class DetalleVentasService:
    def __init__(self, db: 'DbConnection'):
        self._repository = DetalleVentasRepository(db)

    def get_all(self) -> List['DetalleVentaModel']:
        """Retorna todos los detalles de ventas en la base de datos."""
        return self._repository.get_all()
    
    def get_by_id_venta(self, id_venta: int) -> List['DetalleVentaModel']:
        """
        Retorna los detalles de ventas para una venta específica.
        
        :param id_venta: El ID de la venta para la cual se desean obtener los detalles.
        """
        return self._repository.get_by_id_venta(int(id_venta))
    
    def get_by_id_producto(self, id_producto: int) -> List['DetalleVentaModel']:
        """
        Retorna los detalles de ventas para un producto específico.

        :param id_producto: El ID del producto para el cual se desean obtener los detalles.
        """
        return self._repository.get_by_id_producto(id_producto)
