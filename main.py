# -*- coding: utf-8 -*-
"""
Programa principal del Sistema Experto.
Se encarga de la interfaz de usuario y de cargar los archivos.
"""
import os
from motor import cargar_json, motor_inferencia

def mostrar_menu():
    print("\n" + "="*50)
    print(" SISTEMA EXPERTO: RECOMENDADOR DE LENGUAJES")
    print("="*50)
    print("1. Probar un caso de ejemplo (Caso 1, 2 o 3)")
    print("2. Ingresar sintomas manualmente")
    print("3. Salir")
    print("="*50)

def recomendar_final(hechos_finales):
    """Analiza los hechos finales y muestra una conclusión legible."""
    print("\n" + "*"*50)
    print(" RECOMENDACIÓN FINAL DEL SISTEMA EXPERTO")
    print("*"*50)
    
    # Buscamos si el motor llegó a alguna recomendación de lenguaje
    lenguajes = {
        "recomendar_python": "Python",
        "recomendar_html_css": "HTML y CSS",
        "recomendar_javascript": "JavaScript",
        "recomendar_flutter": "Flutter",
        "recomendar_java": "Java",
        "recomendar_unity_csharp": "Unity con C#"
    }
    
    encontrados = []
    for clave, nombre in lenguajes.items():
        if clave in hechos_finales:
            encontrados.append(nombre)
            
    if encontrados:
        print(f"Se recomienda empezar a aprender: {', '.join(encontrados)}")
    else:
        print("No se pudo determinar un lenguaje con los datos ingresados.")
        
    # Mostramos rutas o advertencias extra si se activaron
    if "advertir_requiere_equipo" in hechos_finales:
        print("\n[ADVERTENCIA] El lenguaje recomendado puede requerir un equipo con más recursos.")
    if "sugerir_curso_corto" in hechos_finales:
        print("[CONSEJO] Te sugerimos buscar un curso corto o tutorial express para empezar.")
    if "recomendar_publicar_en_github" in hechos_finales:
        print("[CONSEJO] Sube tus proyectos a GitHub para armar tu portafolio.")
        
    print("*"*50 + "\n")

def ejecutar_caso(nombre_caso, datos_caso, reglas):
    """Prepara los hechos y llama al motor."""
    # Convertimos el diccionario a una lista SOLO con los que son True
    hechos_iniciales = [hecho for hecho, valor in datos_caso.items() if valor is True]
    
    # Llamamos al motor
    hechos_finales = motor_inferencia(hechos_iniciales, reglas)
    
    # Mostramos la conclusión
    recomendar_final(hechos_finales)

def main():
    # 1. Cargar archivos (usando rutas relativas a la carpeta datos)
    ruta_reglas = os.path.join("datos", "conocimiento.json")
    ruta_casos = os.path.join("datos", "hechos_ejemplo.json")
    
    try:
        datos_reglas = cargar_json(ruta_reglas)
        reglas = datos_reglas["reglas"]
        casos = cargar_json(ruta_casos)
    except FileNotFoundError:
        print("Error: No se encontraron los archivos en la carpeta 'datos'.")
        print("Asegurate de ejecutar el programa desde la carpeta raiz del proyecto.")
        return
    except Exception as e:
        print(f"Error al leer los archivos JSON: {e}")
        return

    while True:
        mostrar_menu()
        opcion = input("Elige una opcion (1-3): ")
        
        if opcion == "1":
            print("\nCasos disponibles:")
            for key in casos.keys():
                print(f"- {key}")
            caso_elegido = input("Escribe el nombre del caso (ej. caso_1): ")
            
            if caso_elegido in casos:
                ejecutar_caso(caso_elegido, casos[caso_elegido], reglas)
            else:
                print("Caso no encontrado.")
                
        elif opcion == "2":
            print("\nIngresa los sintomas separados por coma.")
            print("Ejemplo: quiere_web, es_principiante, tiene_poco_tiempo")
            entrada = input("Sintomas: ")
            
            # Limpiamos la entrada (quitamos espacios y creamos la lista)
            hechos_iniciales = [h.strip() for h in entrada.split(",") if h.strip()]
            
            if hechos_iniciales:
                hechos_finales = motor_inferencia(hechos_iniciales, reglas)
                recomendar_final(hechos_finales)
            else:
                print("No ingresaste ningun sintoma.")
                
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion no valida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
