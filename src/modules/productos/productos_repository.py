from inspect import _void
import os, csv
import pathlib
from typing import Any, Dict, List
from .producto_model import ProductoModel

class ProductosRepository:
    def __init__(self):
        self.db_path = (pathlib.Path(__file__).parents[3] / "bd" / "productos.csv").resolve()
        self.productos: List[ProductoModel] = []
        self.categorias = set()
        self._load()

    def _load(self):
        """
        Loads the data from the csv file into memory.
        """
        with open(self.db_path, mode='r',encoding='utf-8') as csvfile:
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
                dict['precio_unitario'] = float(dict['precio_unitario'])
                self.categorias.add(dict['categoria'])
                self.productos.append(ProductoModel(**dict))
            csvfile.close()

    def get_all(self) -> List[ProductoModel]:
        """
        Returns all products from the database.
        """
        return self.productos

    def get_by_id(self, id: int) -> ProductoModel:
        """
        Returns the product with the given id.
        """
        return [producto for producto in self.productos if producto.id_producto == id][0]
    
    def agregar(self, producto: ProductoModel) -> _void:
        """
        Adds a new product to the database.

        :param producto: The product to add.
        """
        try:
            ## chequeo que no halla repetidos, si no existe, entra al except
            set = [i.to_dict() for i in self.productos]
            set.index(producto.to_dict())
        except Exception as e:
            self.productos.append(producto)
            #escribo a la base de datos csv
            with open(self.db_path, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(producto.to_dict().values())
