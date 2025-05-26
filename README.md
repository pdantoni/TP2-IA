# TP2 - Inteligencia Artificial 🧠

Este proyecto implementa un **algoritmo genético** para resolver un acertijo llamado **Festival Gastronómico Internacional**.

## 🧩 Descripción del problema
Cinco chefs participan en un festival gastronómico. Cada uno es de un país diferente, prepara un plato típico distinto (Sushi, Curry, Tacos, Risotto, Ceviche), usa un ingrediente especial (Albahaca, Ajo, Azafrán, Cilantro, Jengibr), tiene un estilo de cocina particular (Parrilla, Horno, Al vapor, Frito, Hervido), y presenta su plato en un día diferente de la semana (lunes a viernes).

### 🔎 Pistas 

- El **chef japonés** cocina **sushi** y lo presenta el **martes**.  
- El plato presentado el **viernes** es preparado **al horno**.  
- El **chef italiano** usa **albahaca** en su plato.  
- El plato **al vapor** se presenta el mismo día que el **curry**.  
- El **chef francés** cocina el **miércoles**.  
- El **chef que usa ajo** presenta su plato **un día antes** que el chef que prepara **tacos**.  
- El **chef tailandés** cocina **al vapor**.  
- El **risotto** se presenta **un día después** que el plato preparado **a la parrilla**.  
- El **chef español** _NO_ cocina **paella** ni usa **azafrán**.  
- El chef que cocina **ceviche** presenta su plato el **lunes**.
- El plato hervido se sirve el lunes.
- El chef que usa cilantro presenta su plato dos días después que el chef que usa azafrán.


## 🛠️ Tecnologías y Librerías
- Python 3.13
- [DEAP](https://github.com/DEAP/deap): para la implementación del algoritmo genético.
- Matplotlib: para visualizar la evolución.
- Seaborn: para mejorar los gráficos.

## 🚀 Ejecución

1. Clonar el repo
2. Instalar las librerías

```bash
pip install deap matplotlib seaborn
```
3. Posicionarse en el directorio donde esta el archivo y correr:
```bash
py ag_festival.py
```
