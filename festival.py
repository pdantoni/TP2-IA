# Festival de Comidas Internacionales

import random
from enum import IntEnum

# Categorías
PAISES       = IntEnum("PAIS",      ["JAPON", "ITALIA", "FRANCIA", "TAILANDIA", "ESPANA"])
PLATOS       = IntEnum("PLATO",     ["SUSHI", "CURRY", "TACOS", "RISOTTO", "CEVICHE"])
DIAS         = IntEnum("DIA",       ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"])
INGREDIENTES = IntEnum("ING",       ["ALBAHACA", "AJO", "AZAFRAN", "CILANTRO", "JENGIBRE"])
ESTILOS      = IntEnum("ESTILO",    ["PARRILLA", "HORNO", "AL_VAPOR", "FRITO", "HERVIDO"])

# Posiciones dentro de cada gen
POS_PLATO = 0
POS_ING = 1
POS_ESTILO = 2
POS_DIA = 3

TAM_CHEF = 4 #cantidad de características por chef
CANT_CHEF = 5 #cantidad total de chefs

# Visualización del resultado en forma de tabla
def imprimir_ind(ind):
    print(f"{'Chef':<10} | {'Día':<10} | {'Ingrediente':<11} | {'Estilo':<9} | {'Plato':<10}")
    print("-" * 60)
    for i in range(CANT_CHEF):
        start = i * TAM_CHEF
        end = start + TAM_CHEF
        chef_info = ind[start:end]
        chef = PAISES(i + 1).name
        plato = PLATOS(chef_info[POS_PLATO]).name
        ing = INGREDIENTES(chef_info[POS_ING]).name
        estilo = ESTILOS(chef_info[POS_ESTILO]).name
        dia = DIAS(chef_info[POS_DIA]).name

        print(f"{chef:<10} | {dia:<10} | {ing:<10} | {estilo:<9} | {plato:<10}")
    print("\n")

def crear_ind(cls, str_cls):
    ind = []

    # Valores únicos
    platos = random.sample(range(1, 6), 5)
    ingredientes = random.sample(range(1, 6), 5)
    estilos = random.sample(range(1, 6), 5)
    dias = random.sample(range(1, 6), 5)

    random.shuffle(platos)
    random.shuffle(ingredientes)
    random.shuffle(estilos)
    random.shuffle(dias)

    # Inicializar el individuo con valores vacíos
    ind = [None] * (CANT_CHEF * TAM_CHEF)

    # Forzar asignaciones específicas según las condiciones
    # Chef Japonés → SUSHI, MARTES
    ind[(PAISES.JAPON - 1) * TAM_CHEF + POS_PLATO] = PLATOS.SUSHI
    ind[(PAISES.JAPON - 1) * TAM_CHEF + POS_DIA] = DIAS.MARTES

    # Chef Italiano → ALBAHACA
    ind[(PAISES.ITALIA - 1) * TAM_CHEF + POS_ING] = INGREDIENTES.ALBAHACA

    # Chef Francés → MIÉRCOLES
    ind[(PAISES.FRANCIA - 1) * TAM_CHEF + POS_DIA] = DIAS.MIERCOLES

    # Chef Tailandés → CURRY y AL_VAPOR
    ind[(PAISES.TAILANDIA - 1) * TAM_CHEF + POS_PLATO] = PLATOS.CURRY
    ind[(PAISES.TAILANDIA - 1) * TAM_CHEF + POS_ESTILO] = ESTILOS.AL_VAPOR

    # Chef Español → Ninguno de estos
    # Evitar CEVICHE y AZAFRÁN más adelante

    # Asignar platos restantes
    usados_platos = {PLATOS.SUSHI, PLATOS.CURRY}
    restantes_platos = [p for p in platos if p not in usados_platos]
    for i in range(CANT_CHEF):
        if ind[i * TAM_CHEF + POS_PLATO] is None:
            ind[i * TAM_CHEF + POS_PLATO] = restantes_platos.pop()

    # Asignar ingredientes restantes
    usados_ing = {INGREDIENTES.ALBAHACA}
    restantes_ing = [i for i in ingredientes if i not in usados_ing]
    for i in range(CANT_CHEF):
        if ind[i * TAM_CHEF + POS_ING] is None:
            nuevo_ing = restantes_ing.pop()
            if i == PAISES.ESPANA - 1 and nuevo_ing == INGREDIENTES.AZAFRAN:
                restantes_ing.insert(0, nuevo_ing)  # evitar azafrán en español
                nuevo_ing = restantes_ing.pop()
            ind[i * TAM_CHEF + POS_ING] = nuevo_ing

    # Asignar estilos restantes
    usados_estilos = {ESTILOS.AL_VAPOR}
    restantes_estilos = [e for e in estilos if e not in usados_estilos]
    for i in range(CANT_CHEF):
        if ind[i * TAM_CHEF + POS_ESTILO] is None:
            ind[i * TAM_CHEF + POS_ESTILO] = restantes_estilos.pop()

    # Asignar días restantes
    usados_dias = {DIAS.MARTES, DIAS.MIERCOLES}
    restantes_dias = [d for d in dias if d not in usados_dias]
    for i in range(CANT_CHEF):
        if ind[i * TAM_CHEF + POS_DIA] is None:
            ind[i * TAM_CHEF + POS_DIA] = restantes_dias.pop()

    # Asignar una estrategia (obligatorio por DEAP)
    ind = cls(ind)
    ind.strategy = str_cls()

    return ind

def validar_condicion(v, index_chef, pos_att1, att1, pos_att2, att2):
    pos_absoluta1 = index_chef * TAM_CHEF + pos_att1
    pos_absoluta2 = index_chef * TAM_CHEF + pos_att2
    return v[pos_absoluta1] == att1 and v[pos_absoluta2] == att2

def validar_existencia_condicion(v, pos_att1, att1, pos_att2, att2):
    for i in range(5):
        if (validar_condicion(v, i, pos_att1, att1, pos_att2, att2)):
            return True
    return False

def verificar_chef(v, index_chef, pos_att, att):
    return v[(index_chef -1) * TAM_CHEF + pos_att] == att


def cumple_condicion_risotto_parrilla(v):
    dia_risotto = None
    dia_parrilla = None

    for i in range(CANT_CHEF):
        plato = v[i * TAM_CHEF + POS_PLATO]
        estilo = v[i * TAM_CHEF + POS_ESTILO]
        dia = v[i * TAM_CHEF + POS_DIA]

        if plato == PLATOS.RISOTTO:
            dia_risotto = dia
        if estilo == ESTILOS.PARRILLA:
            dia_parrilla = dia

    return (
            dia_risotto is not None and
            dia_parrilla is not None and
            dia_risotto == dia_parrilla + 1
    )

def cumple_condicion_ajo_tacos(v):
    dia_ajo = None
    dia_tacos = None

    for i in range(5):  # 5 chefs
        ingrediente = v[i * TAM_CHEF + POS_ING]
        plato = v[i * TAM_CHEF + POS_PLATO]
        dia = v[i * TAM_CHEF + POS_DIA]

        if ingrediente == INGREDIENTES.AJO:
            dia_ajo = dia
        if plato == PLATOS.TACOS:
            dia_tacos = dia

    # Verifica que ambos valores existen y cumplen la condición
    return dia_ajo is not None and dia_tacos is not None and dia_ajo + 1 == dia_tacos

def evaluar_aptitud(ind):
    puntos = 0
    puntos += calcular_condiciones_a_cumplir(ind)
    puntos += calcular_restricciones(ind)

    return [puntos]


def cuanto_se_repiten(v):
    puntaje = 0
    for i in range(0, TAM_CHEF * CANT_CHEF):
        for j in range(i + TAM_CHEF, CANT_CHEF * TAM_CHEF, TAM_CHEF):
            if v[i % (CANT_CHEF * TAM_CHEF)] == v[j % (CANT_CHEF * TAM_CHEF)]:
                puntaje += 1
    return puntaje

def calcular_condiciones_a_cumplir(ind):
    puntos = 0

    #El chef japonés cocina sushi y lo presenta el martes.
    if validar_existencia_condicion(ind, POS_PLATO, PLATOS.SUSHI, POS_DIA, DIAS.MARTES):
        puntos += 2
    if verificar_chef(ind, PAISES.JAPON, POS_PLATO, PLATOS.SUSHI):
        puntos += 2

    # El plato presentado el viernes se cocina al horno.
    if validar_existencia_condicion(ind, POS_DIA, DIAS.VIERNES, POS_ESTILO, ESTILOS.HORNO):
        puntos += 2

    # El chef italiano usa albahaca en su plato.
    if verificar_chef(ind, PAISES.ITALIA, POS_ING, INGREDIENTES.ALBAHACA):
        puntos += 2

    # El plato al vapor se presenta el mismo día que el curry.
    if verificar_chef(ind, PAISES.TAILANDIA, POS_PLATO, PLATOS.CURRY):
        puntos += 2

    # El chef francés cocina el miércoles.
    if verificar_chef(ind, PAISES.FRANCIA, POS_DIA, DIAS.MIERCOLES):
        puntos += 2

    # El chef que usa ajo presenta su plato un día antes que el que prepara tacos.
    if cumple_condicion_ajo_tacos(ind):
        puntos += 2

    # El chef tailandés cocina al vapor.
    if verificar_chef(ind, PAISES.TAILANDIA, POS_ESTILO, ESTILOS.AL_VAPOR):
        puntos += 2

    # El risotto se presenta un día después que el plato preparado a la parrilla.
    if cumple_condicion_risotto_parrilla(ind):
        puntos += 2

    # El chef que cocina ceviche presenta su plato el lunes.
    if validar_existencia_condicion(ind, POS_PLATO, PLATOS.CEVICHE, POS_DIA, DIAS.LUNES):
        puntos += 2

    return puntos


def calcular_restricciones(ind):
    puntos = 0

    puntos -= cuanto_se_repiten(ind) * 2

    #El chef español NO cocina ceviche ni usa azafrán.
    if verificar_chef(ind, PAISES.ESPANA, POS_PLATO, PLATOS.CEVICHE):
        puntos -= 2
    if verificar_chef(ind, PAISES.ESPANA, POS_ING, INGREDIENTES.AZAFRAN):
        puntos -= 2

    return puntos
