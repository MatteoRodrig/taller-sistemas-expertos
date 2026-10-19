# -*- coding: utf-8 -*-
"""
Motor de inferencia para el Sistema Experto de Recomendación de Lenguajes.
Basado en el motor original entregado en clase.
"""

def cargar_json(ruta):
    """Lee un archivo JSON y lo devuelve como diccionario de Python."""
    import json
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def motor_inferencia(hechos_iniciales, reglas):
    """
    Ejecuta el encadenamiento hacia adelante.
    hechos_iniciales: lista de strings con los hechos verdaderos.
    reglas: lista de diccionarios con las reglas.
    """
    # 1. Inicializar memoria de trabajo
    hechos = set(hechos_iniciales)
    reglas_disparadas = set()

    print("\n--- INICIANDO MOTOR DE INFERENCIA ---")
    print(f"Hechos iniciales: {', '.join(hechos)}\n")

    paso = 1
    while True:
        reglas_aplicables = []
        for i, regla in enumerate(reglas):
            # Saltamos reglas ya disparadas
            if i in reglas_disparadas:
                continue
                
            antecedentes = set(regla["antecedentes"])
            
            # Verificamos si todos los antecedentes están en los hechos
            if antecedentes.issubset(hechos):
                reglas_aplicables.append((i, regla))

        # Mostrar conjunto de conflictos
        print(f"--- PASO {paso} ---")
        print("Conjunto de conflictos (reglas aplicables):")
        if reglas_aplicables:
            for _, regla in reglas_aplicables:
                print(f"  * {regla['nombre']} (Prioridad: {regla.get('prioridad', 99)})")
        else:
            print("  * Ninguna")
            print("\n--- FIN DE LA INFERENCIA ---")
            break

        # ESTRATEGIA DE RESOLUCIÓN DE CONFLICTOS
        # Criterio 1: Menor número de prioridad gana (1 es más prioritario que 2)
        # Criterio 2: Si empatan en prioridad, gana la que tenga más antecedentes
        # Criterio 3: Si siguen empatando, gana la que esté primero en el archivo
        reglas_aplicables.sort(key=lambda item: (
            item[1].get("prioridad", 99), 
            -len(item[1]["antecedentes"]), 
            item[0]
        ))

        indice_regla, regla_seleccionada = reglas_aplicables[0]
        
        print(f"\n>> Regla seleccionada: {regla_seleccionada['nombre']}")
        
        # Disparar la regla
        reglas_disparadas.add(indice_regla)
        nuevos_hechos = []
        for consecuente in regla_seleccionada["consecuentes"]:
            if consecuente not in hechos:
                hechos.add(consecuente)
                nuevos_hechos.append(consecuente)

        if nuevos_hechos:
            print(f">> Hechos nuevos inferidos: {', '.join(nuevos_hechos)}")
        else:
            print(">> No se agregaron hechos nuevos (ya existian).")
            
        print() # Línea en blanco para separar pasos
        paso += 1

    return hechos
