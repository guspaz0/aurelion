# La tienda de Aurelio

Proyecto para guayerd, fundamentos de inteligencia artificial.

## Introduccion

Aurelion es una tienda/despensa/supermercado que vende productos de limpieza y alimentos al por menor y mayor. Desarrolla sus actividades principales dentro de la provincia de cordoba, Argentina.

## Observaciones

la base de datos presenta inconsistencias en los campos de las tablas siguintes: 
- `productos`:
    - `categorias`: el nombre de la categoria es inconsistente con la descripcion del producto. Se le pidio a GPT-5 mini que lo corrija. lo corrijio pero aun asi se encontraron 2 articulos mal categorizados.

# Instrucciones
- tener python 3.7 o superior instalado.
- crear un entorno virtual antes de instalar dependencias.

```bash
# instala dependencias
pip install -r requirements.txt
```