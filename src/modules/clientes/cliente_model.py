from dataclasses import dataclass, field
from datetime import datetime, date
import json, logging
from typing import Dict, List, TYPE_CHECKING

logger = logging.getLogger(__file__)

if TYPE_CHECKING:
    from modules.ventas.venta_model import VentaModel

@dataclass
class ClienteModel:
    id_cliente: int
    nombre_cliente: str
    email: str
    ciudad: str
    departamento: str
    fecha_alta: datetime
    ventas: List['VentaModel'] = field(default_factory=list)

    def __post_init__(self):
        # Convertir `ventas` a lista de DetalleVentaModel
        if self.ventas is None or len(self.ventas) == 0:
            self.ventas = []
        else:
            # importar en tiempo de ejecución para evitar problemas de importación circular
            from modules.ventas.venta_model import VentaModel

            raw = self.ventas
            if isinstance(raw, str):
                try:
                    raw = json.loads(raw)
                except Exception:
                    raw = []
            elif not isinstance(raw, list):
                # Puede ser un file-like o similar
                try:
                    raw = json.load(raw)
                except Exception:
                    raw = []

            normalized: List[VentaModel] = []
            for item in raw:
                if isinstance(item, VentaModel):
                    normalized.append(item)
                elif isinstance(item, dict):
                    normalized.append(VentaModel(**item))
                else:
                    # ignorar elementos no reconocidos
                    continue
            self.ventas = normalized
    
    def total_ventas(self, desde: datetime = None, hasta: datetime = None) -> float:
        """ Retorna el total de ventas realizadas por el cliente en el rango de fechas especificado """
        medios_de_pago: dict = {}
        ventas: List['VentaModel'] = self.ventas
        importe: float = 0
        if all(isinstance(fecha, str) for fecha in (desde,hasta)):
            desde = datetime.strptime(desde, "%Y-%m-%d")
            hasta = datetime.strptime(hasta, "%Y-%m-%d")
        if all(isinstance(fecha, date) for fecha in (desde, hasta)):
            desde = datetime.strptime(desde.strftime("%Y-%m-%d"), "%Y-%m-%d")
            hasta = datetime.strptime(hasta.strftime("%Y-%m-%d"), "%Y-%m-%d")
        if all(isinstance(fecha, datetime) for fecha in (desde, hasta)):
            ventas = [venta for venta in self.ventas if desde <= venta.fecha <= hasta]
        
        for venta in ventas:
            medios_de_pago[venta.medio_pago] = medios_de_pago.get(venta.medio_pago, 0) + venta.importe
            importe += venta.importe
        return { "importe": importe, "cantidad_ventas": len(ventas), **medios_de_pago }
    
    def to_dict(self):
        """
        Retorna un diccionario con los datos del cliente.
        """
        return {
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "email": self.email,
            "ciudad": self.ciudad,
            "fecha_alta": self.fecha_alta,
            "ventas": [venta.to_dict() for venta in self.ventas] if self.ventas else []
        }

    def to_json(self):
        """
        Retorna un JSON con los datos del cliente.
        """
        return json.dumps({
            **self.to_dict(),
            "fecha_alta": self.fecha_alta if self.fecha_alta else None,
            "ventas": [
                {
                    **venta.to_dict(), "detalle": [dv.to_dict() for dv in venta.detalle]
                } for venta in self.ventas
            ] if self.ventas else []
        }, default=str, indent=4)
    
