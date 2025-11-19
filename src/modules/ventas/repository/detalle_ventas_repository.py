import csv, logging
from typing import Any, Dict, List, TYPE_CHECKING
from modules.ventas.models.detalle_venta_model import DetalleVentaModel

if TYPE_CHECKING:
    from modules import DbConnection
    from modules.db.dao.detalle_ventas_dao import DetalleVentasDao

logger = logging.getLogger(__name__)

class DetalleVentasRepository:
    def __init__(self, db: 'DbConnection'):
        self._dao: 'DetalleVentasDao' = db.detalleVentasDao
    
    def get_all(self) -> List[DetalleVentaModel]:
        """
        Returns all the ventas stored in the repository.
        """
        return self._dao.get_all()
    
    def get_by_id_venta(self, id_venta: int) -> List[DetalleVentaModel]:
        """
        Returns ventas by id venta

        :param id_venta: The id of the venta to retrieve.
        """
        return self._dao.get_by_venta(id_venta)
    
    def get_by_id_producto(self, id_producto: int) -> List[DetalleVentaModel]:
        """
        Returns ventas by id producto

        :param id_producto: The id of the producto to retrieve
        """
        return self._dao.get_by_producto(id_producto)

    def agregar(self, detalle_venta: DetalleVentaModel):
        """
        Saves the venta to the repository and writes it to a CSV file.
        """
        id = self._dao.insert_detalle_venta(
            detalle_venta.id_venta, 
            detalle_venta.id_producto,
            detalle_venta.cantidad,
            detalle_venta.precio_unitario
        )
        logger.info(f"DetalleVentaModel saved with id: {id}")
