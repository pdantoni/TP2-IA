# Festival de Comidas Internacionales

import random
from enum import IntEnum

# 1. Enumeraciones
PAISES = IntEnum("PAIS", ["JAPON", "ITALIA", "FRANCIA", "TAILANDIA", "ESPAÑA"])
PLATOS = IntEnum("PLATO", ["SUSHI", "CURRY", "TACOS", "RISOTTO", "CEVICHE"])
INGREDIENTES = IntEnum("INGREDIENTE", ["ALBAHACA", "AJO", "AZAFRAN", "CILANTRO", "JENGIBRE"])
ESTILOS = IntEnum("ESTILO", ["PARRILLA", "HORNO", "AL_VAPOR", "FRITO", "HERVIDO"])
DIAS = IntEnum("DIA", ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"])

# 2. Posiciones en cromosoma
POS_PLATO  = 0
POS_ING    = 1
POS_ESTILO = 2
POS_DIA    = 3

TAM_CHEF  = 4             # genes por chef
CANT_CHEF = len(PAISES)   # 5 chefs

# 3. Crear individuo
def crear_ind(cls, str_cls):
    """Crea un individuo con CANT_CHEF*TAM_CHEF genes aleatorios en [1..5]."""
    ind = cls()
    for _ in range(CANT_CHEF * TAM_CHEF):
        ind.append(random.randint(1, 5))
    ind.strategy = str_cls()
    return ind

# 4. Impresión ordenada por día
def imprimir_ind(ind):
    filas = []
    for i in range(CANT_CHEF):
        base   = i * TAM_CHEF
        datos  = ind[base:base+TAM_CHEF]
        chef   = PAISES(i+1).name.capitalize()
        plato  = PLATOS(datos[POS_PLATO]).name.capitalize()
        ing    = INGREDIENTES(datos[POS_ING]).name.capitalize()
        estilo = ESTILOS(datos[POS_ESTILO]).name.replace("_", " ").capitalize()
        dia    = DIAS(datos[POS_DIA]).name.capitalize()
        valor  = DIAS(datos[POS_DIA]).value
        filas.append((valor, chef, dia, plato, ing, estilo))

    # Ordenar por día (1=Lunes ... 5=Viernes)
    filas.sort(key=lambda x: x[0])

    # Imprimir tabla
    print(f"{'Día':<10} | {'Chef':<10} | {'Plato':<10} | {'Ingrediente':<12} | {'Estilo':<10}")
    print("-" * 66)
    for _, chef, dia, plato, ing, estilo in filas:
        print(f"{dia:<10} | {chef:<10} | {plato:<10} | {ing:<12} | {estilo:<10}")
    print()

# 5. Evaluar aptitud
def evaluar_aptitud(ind):
    #Suma +5 por cada pista cumplida y resta -3 por cada restricción que no cumpla,
    aptitud = 0

    chef_enum = []
    for i in range(CANT_CHEF):
        base = i * TAM_CHEF
        p = PLATOS(ind[base + POS_PLATO])
        ig = INGREDIENTES(ind[base + POS_ING])
        es = ESTILOS(ind[base + POS_ESTILO])
        di = DIAS(ind[base + POS_DIA])
        chef_enum.append((p, ig, es, di))

    # — Condiciones +5 —
    # 1. Japón + sushi + martes
    p, _, _, d = chef_enum[PAISES.JAPON.value - 1]
    if p == PLATOS.SUSHI and d == DIAS.MARTES:
        aptitud += 5

    # 2. Viernes y horno
    if any(es == ESTILOS.HORNO and di == DIAS.VIERNES for _, _, es, di in chef_enum):
        aptitud += 5

    # 3. El chef italiano usa albahaca
    _, ig, _, _ = chef_enum[PAISES.ITALIA.value - 1]
    if ig == INGREDIENTES.ALBAHACA:
        aptitud += 5

    # 4. Al vapor = mismo día que curry
    dias_vapor = {di for _, _, es, di in chef_enum if es == ESTILOS.AL_VAPOR}
    dias_curry = {di for p, _, _, di in chef_enum if p == PLATOS.CURRY}
    if dias_vapor & dias_curry:
        aptitud += 5

    # 5. Francia + miércoles
    _, _, _, d = chef_enum[PAISES.FRANCIA.value - 1]
    if d == DIAS.MIERCOLES:
        aptitud += 5

    # 6. Ajo un día antes que tacos
    dia_ajo = next((di for _, ig, _, di in chef_enum if ig == INGREDIENTES.AJO), None)
    dia_tac = next((di for p, _, _, di in chef_enum if p == PLATOS.TACOS), None)
    if dia_ajo and dia_tac and dia_tac.value == dia_ajo.value + 1:
        aptitud += 5

    # 7. Tailandia cocina al vapor
    _, _, es, _ = chef_enum[PAISES.TAILANDIA.value - 1]
    if es == ESTILOS.AL_VAPOR:
        aptitud += 5

    # 8. Risotto un día después del chef que usa estilo parrilla
    dia_parr = next((di for _, _, es, di in chef_enum if es == ESTILOS.PARRILLA), None)
    dia_riss = next((di for p, _, _, di in chef_enum if p == PLATOS.RISOTTO), None)
    if dia_parr and dia_riss and dia_riss.value == dia_parr.value + 1:
        aptitud += 5

    # 9. Ceviche + lunes
    if any(p == PLATOS.CEVICHE and di == DIAS.LUNES for p, _, _, di in chef_enum):
        aptitud += 5

    # 10. Hervido + lunes
    if any(es == ESTILOS.HERVIDO and di == DIAS.LUNES for _, _, es, di in chef_enum):
        aptitud += 5

    # 11. Cilantro 2 días después de azafrán
    dia_azaf = next((di for _, ig, _, di in chef_enum if ig == INGREDIENTES.AZAFRAN), None)
    dia_cila = next((di for _, ig, _, di in chef_enum if ig == INGREDIENTES.CILANTRO), None)
    if dia_azaf and dia_cila and dia_cila.value == dia_azaf.value + 2:
        aptitud += 5

    # — Restricciones -3 —
    # a) España no cocina risotto ni azafrán
    p_sp, ig_sp, _, _ = chef_enum[PAISES.ESPAÑA.value - 1]
    if p_sp == PLATOS.RISOTTO or ig_sp == INGREDIENTES.AZAFRAN:
        aptitud -= 3

    # b) Solo Japón puede hacer sushi el martes
    cond_sushi = any(p == PLATOS.SUSHI and di == DIAS.MARTES for p, _, _, di in chef_enum)
    if not (cond_sushi and chef_enum[PAISES.JAPON.value - 1][0] == PLATOS.SUSHI):
        aptitud -= 3

    # c) Solo el chef italiano usa albahaca
    total_alb = sum(1 for _, ig, _, _ in chef_enum if ig == INGREDIENTES.ALBAHACA)
    if total_alb != 1 or chef_enum[PAISES.ITALIA.value - 1][1] != INGREDIENTES.ALBAHACA:
        aptitud -= 3

    # d) Curry + al vapor y Risotto + parrilla
    if not (dias_vapor & dias_curry):
        aptitud -= 3
    if not (dia_parr and dia_riss and dia_riss.value == dia_parr.value + 1):
        aptitud -= 3

    # e) Unicidad de platos, ingredientes, estilos y días
    def pen(lista):
        extra = len(lista) - len(set(lista))
        return extra * 3

    estilos = [es for _, _, es, _ in chef_enum]
    ings    = [ig for _, ig, _, _ in chef_enum]
    platos = [p for p, _, _, _ in chef_enum]
    dias_lst = [di for _, _, _, di in chef_enum]

    aptitud -= pen(estilos)
    aptitud -= pen(ings)
    aptitud -= pen(platos)
    aptitud -= pen(dias_lst)

    return (aptitud,)