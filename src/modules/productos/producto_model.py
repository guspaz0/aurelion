from dataclasses import dataclass
from datetime import datetime, date
import json
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from modules.ventas.models.detalle_venta_model import DetalleVentaModel

@dataclass
class ProductoModel:
    id_producto: int
    nombre_producto: str
    categoria: str
    precio_unitario: float

    @property
    def ventas(self) -> List['DetalleVentaModel']:
        from modules.ventas.service.detalle_ventas_service import DetalleVentasService
        self._ventas = DetalleVentasService().get_by_id_producto(self.id_producto)
        return self._ventas
    
    @ventas.setter
    def ventas(self, value: List['DetalleVentaModel']):
        if isinstance(value, list) and all(isinstance(item, DetalleVentaModel) for item in value):
            self._ventas = value


    def total_vendido(self, desde: datetime | str = None, hasta: datetime | str = None) -> Dict[str, int | float]:
        """
        Retorna el total vendido de este producto entre las fechas especificadas o todas las fechas si no se especifican.

        :param desde: Fecha inicial para filtrar las ventas.
        :param hasta: Fecha final para filtrar las ventas
        """
        cantidad: int = 0
        importe: float = 0
        ventas: List[DetalleVentaModel] = self.ventas
        if all(isinstance(fecha, str) for fecha in (desde, hasta)):
            desde = datetime.strptime(desde, "%Y-%m-%d")
            hasta = datetime.strptime(hasta, "%Y-%m-%d")
        if all(isinstance(fecha, date) for fecha in (desde, hasta)):
            desde = datetime.strptime(desde.strftime("%Y-%m-%d"), "%Y-%m-%d")
            hasta = datetime.strptime(hasta.strftime("%Y-%m-%d"), "%Y-%m-%d")
        if all(isinstance(fecha, datetime) for fecha in (desde, hasta)):
            ventas = [venta for venta in self.ventas if desde <= venta.get_fecha() <= hasta]
        for venta in ventas:
            cantidad += venta.cantidad
            importe += venta.precio_unitario * venta.cantidad
        return {"cantidad": cantidad, "importe": importe}

    def to_dict(self):
        """
        Retorna un diccionario con los datos del producto
        """
        return {
            "id_producto": self.id_producto,
            "nombre_producto": self.nombre_producto,
            "categoria": self.categoria,
            "precio_unitario": self.precio_unitario
        }

    def to_json(self):
        """
        Retorna un JSON con los datos del producto y sus ventas asociadas
        """
        return json.dumps({
            **self.to_dict(),
            "ventas": [venta.to_dict() for venta in self.ventas] if self.ventas else []
            }, default=str, indent=4)
