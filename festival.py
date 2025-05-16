# Festival de Comidas Internacionales

import random
from enum import IntEnum

# Categorías
PAISES       = IntEnum("PAIS",      ["JAPÓN", "ITALIA", "FRANCIA", "TAILANDIA", "ESPAÑA"])
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
    ind = cls()
    for i in range(CANT_CHEF * TAM_CHEF):
        ind.append(random.randint(1, 5))
    
    ind.strategy = str_cls()
    return ind

# Función de aptitud
def evaluar_aptitud(individual):
    aptitud = 0
    chef_data = []

    # Organizar los datos del individuo por chef
    for i in range(CANT_CHEF):
        start = i * TAM_CHEF
        end = start + TAM_CHEF
        chef_data.append(individual[start:end])

    # Convertir los datos a los tipos Enum para facilitar la lectura del código
    chef_enum_data = []
    for i in range(CANT_CHEF):
        plato = PLATOS(chef_data[i][POS_PLATO])
        ingrediente = INGREDIENTES(chef_data[i][POS_ING])
        estilo = ESTILOS(chef_data[i][POS_ESTILO])
        dia = DIAS(chef_data[i][POS_DIA])
        chef_enum_data.append((plato, ingrediente, estilo, dia))

    # Verificar las condiciones del problema y asignar puntajes
    for i in range(CANT_CHEF):
        plato_i, ingrediente_i, estilo_i, dia_i = chef_enum_data[i]

        # 1. El chef japonés cocina sushi y lo presenta el martes.
        if i == PAISES.JAPÓN.value - 1:  # El índice 0 corresponde a Japón
            if plato_i == PLATOS.SUSHI and dia_i == DIAS.MARTES:
                aptitud += 5
            else:
                aptitud -= 3

        # 2. El plato presentado el viernes se cocina al horno.
        if dia_i == DIAS.VIERNES and estilo_i == ESTILOS.HORNO:
            aptitud += 5
        elif dia_i == DIAS.VIERNES and estilo_i != ESTILOS.HORNO:
            aptitud -= 3

        # 3. El chef italiano usa albahaca en su plato.
        if i == PAISES.ITALIA.value - 1: # El índice 1 corresponde a Italia
            if ingrediente_i == INGREDIENTES.ALBAHACA:
                aptitud += 5
            else:
                aptitud -= 3

        # 4. El plato al vapor se presenta el mismo día que el curry.
        if estilo_i == ESTILOS.AL_VAPOR:
            for j in range(CANT_CHEF):
                if i != j:
                    plato_j, _, _, dia_j = chef_enum_data[j]
                    if plato_j == PLATOS.CURRY and dia_j == dia_i:
                        aptitud += 5
                        break
            else:
                aptitud -= 3

        # 5. El chef francés cocina el miércoles.
        if i == PAISES.FRANCIA.value - 1: # El índice 2 corresponde a Francia
            if dia_i == DIAS.MIERCOLES:
                aptitud += 5
            else:
                aptitud -= 3

        # 6. El chef que usa ajo presenta su plato un día antes que el que prepara tacos.
        if ingrediente_i == INGREDIENTES.AJO:
            dia_ajo = dia_i
            for j in range(CANT_CHEF):
                if i != j:
                    plato_j, _, _, dia_j = chef_enum_data[j]
                    if plato_j == PLATOS.TACOS:
                        if dia_ajo.value < 5 and dia_j == DIAS(dia_ajo.value + 1): # Comparar usando los valores de los Enum
                            aptitud += 5
                        else:
                            aptitud -= 3
                        break  # Asumimos solo un chef prepara tacos
            else:
                aptitud -= 1

        # 7. El chef tailandés cocina al vapor.
        if i == PAISES.TAILANDIA.value - 1: # El índice 3 corresponde a Tailandia
            if estilo_i == ESTILOS.AL_VAPOR:
                aptitud += 5
            else:
                aptitud -= 3

        # 8. El risotto se presenta un día después que el plato preparado a la parrilla.
        if plato_i == PLATOS.RISOTTO:
            dia_risotto = dia_i
            if dia_risotto.value > 1:  # Verificar que el día del risotto no sea lunes
                for j in range(CANT_CHEF):
                    if i != j:
                        _, _, estilo_j, dia_j = chef_enum_data[j]
                        if estilo_j == ESTILOS.PARRILLA and dia_j == DIAS(dia_risotto.value - 1):
                            aptitud += 5
                            break
                else:
                    aptitud -= 3
            else:
                aptitud -= 3 

        # 9. El chef español NO cocina risotto ni usa azafrán.
        if i == PAISES.ESPAÑA.value - 1: # El índice 4 corresponde a España
            if plato_i == PLATOS.RISOTTO or ingrediente_i == INGREDIENTES.AZAFRAN:
                aptitud -= 3

        # 10. El chef que cocina ceviche presenta su plato el lunes.
        if plato_i == PLATOS.CEVICHE:
            if dia_i == DIAS.LUNES:
                aptitud += 5
            else:
                aptitud -= 3
    
    # Penalizar repeticiones de platos, ingredientes, estilos o días
    platos_usados = [chef[0] for chef in chef_enum_data]
    ingredientes_usados = [chef[1] for chef in chef_enum_data]
    estilos_usados = [chef[2] for chef in chef_enum_data]
    dias_usados = [chef[3] for chef in chef_enum_data]
    
    if len(platos_usados) != len(set(platos_usados)):
        aptitud -= 10  # Penalización fuerte por platos repetidos
    if len(ingredientes_usados) != len(set(ingredientes_usados)):
        aptitud -= 5  # Penalización moderada por ingredientes repetidos
    if len(estilos_usados) != len(set(estilos_usados)):
        aptitud -= 5  # Penalización moderada por estilos repetidos
    if len(dias_usados) != len(set(dias_usados)):
        aptitud -= 5 #Penalizacion moderada por dias repetidos

    return (aptitud,)