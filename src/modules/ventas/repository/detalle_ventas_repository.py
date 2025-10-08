import csv
import os
from typing import Any, Dict, List
from modules.ventas.models.detalle_venta_model import DetalleVentaModel

class DetalleVentasRepository:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), "bd", "detalle_ventas.csv")
        self.detalle_ventas: List[DetalleVentaModel] = []
        self._load()

    def _load(self):
        """
        Loads the data from the CSV file into the repository.
        """
        with open(self.db_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            keys: List[str] = []
            for row in reader:
                dict: Dict[str, Any] = {}
                if len(keys) == 0:
                    keys = row
                    continue
                for i in range(0,len(keys)):
                    dict[keys[i]] = row[i] or ''
                dict['id_producto'] = int(dict['id_producto'])
                dict['id_venta'] = int(dict['id_venta'])
                dict['cantidad'] = int(dict['cantidad'])
                dict['precio_unitario'] = float(dict['precio_unitario'])
                dict['importe'] = float(dict['importe'])
                self.detalle_ventas.append(DetalleVentaModel(**dict))
            csvfile.close()
    
    def get_all(self) -> List[DetalleVentaModel]:
        """
        Returns all the ventas stored in the repository.
        """
        return self.detalle_ventas
    
    def get_by_id_venta(self, id_venta: int) -> List[DetalleVentaModel]:
        """
        Returns ventas by id venta

        :param id_venta: The id of the venta to retrieve.
        """
        return [dv for dv in self.detalle_ventas if dv.id_venta == id_venta]
    
    def get_by_id_producto(self, id_producto: int) -> List[DetalleVentaModel]:
        """
        Returns ventas by id producto

        :param id_producto: The id of the producto to retrieve
        """
        return [dv for dv in self.detalle_ventas if dv.id_producto == id_producto]

    def agregar(self, detalle_venta: DetalleVentaModel):
        """
        Saves the venta to the repository and writes it to a CSV file.
        """
        self.detalle_ventas.append(detalle_venta)

        with open(self.db_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(detalle_venta.to_dict().values())