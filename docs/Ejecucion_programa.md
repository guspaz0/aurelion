## Cómo ejecutar (entorno)

- Requisitos: Python 3.7+ y `pip`.
- Crear y activar un entorno virtual (recomendado) y luego instalar dependencias:

```bash
# crear y activar (ejemplo para POSIX)
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

- Ejecutar el script principal (si existe) o lanzar los módulos de limpieza según la estructura del proyecto. Por ejemplo, si el proyecto tiene un `index.py` que orquesta la limpieza:

```bash
python src/main.py
```

Si prefiere ejecutar por pasos, crear un pequeño script `scripts/limpiar.py` que importe las funciones de `modules/*` y siga el pseudocódigo.

## Notas y próximos pasos

- Revisión manual de las recategorizaciones automáticas: las heurísticas ayudan, pero es recomendable validar casos fronteras.
- Normalizar `ventas.csv` para eliminar datos redundantes (dejar solo `id_cliente` y referenciar los datos del cliente desde `clientes.csv`).
- Añadir tests unitarios para validaciones clave (recalculo de importes, detección de ventas sin detalle, integridad de IDs).

---

Instrucciones previas:

- tener python 3.7 o superior instalado.
- crear un entorno virtual antes de instalar dependencias.

```bash
# instala dependencias
pip install -r requirements.txt
```