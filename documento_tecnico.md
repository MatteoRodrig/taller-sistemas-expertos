# Documento Técnico: Sistema Experto Recomendador de Lenguajes

## 1. Introducción y Caso de Estudio
El presente proyecto implementa un Sistema Experto diseñado para resolver un problema cotidiano en el ámbito de la informática: **la elección del primer lenguaje de programación**. Muchas personas que desean incursionar en la programación no saben por dónde empezar. El sistema emula el razonamiento de un experto (un docente o mentor) evaluando los intereses del usuario, su experiencia previa, su disponibilidad de tiempo y sus recursos, para arrojar una recomendación fundamentada.

## 2. Arquitectura del Sistema
El sistema sigue una arquitectura clásica de Sistemas Expertos basados en reglas, compuesta por tres módulos principales:
1. **Base de Conocimiento (BC):** Almacenada de forma externa en `datos/conocimiento.json`. Contiene 18 reglas de producción (estructuras IF-THEN).
2. **Memoria de Trabajo (MT):** Almacenada en `datos/hechos_ejemplo.json` o ingresada por el usuario. Representa el estado actual del problema (los hechos verdaderos).
3. **Motor de Inferencia:** Programado en `motor.py`. Se encarga de evaluar las reglas, aplicar la estrategia de resolución de conflictos y generar nuevos hechos (encadenamiento).

## 3. Representación de Hechos y Reglas
- **Hechos:** Se representan como cadenas de texto (strings) en Python. Por ejemplo: `"quiere_web"` o `"tiene_poco_tiempo"`. Solo los hechos verdaderos (`True`) se cargan en la Memoria de Trabajo.
- **Reglas:** Se representan mediante diccionarios en formato JSON. Cada regla tiene:
  - `nombre`: Identificador legible.
  - `antecedentes`: Lista de hechos que deben ser verdaderos para activar la regla (condición IF).
  - `consecuentes`: Lista de hechos nuevos que se infieren (resultado THEN).
  - `prioridad`: Número entero (1, 2 o 3) usado para resolver conflictos.
  - `justificacion`: Explicación de la regla (no procesada por el motor, pero útil para el usuario).

## 4. Estrategia de Resolución de Conflictos
Cuando varios antecedentes de diferentes reglas se cumplen al mismo tiempo, se genera un "Conjunto de Conflictos". Para decidir qué regla disparar primero, el motor implementa una estrategia híbrida basada en referentes clásicos de sistemas de producción:

1. **Prioridad Explícita (Menor número es mayor prioridad):** Inspirado en el funcionamiento de sistemas como CLIPS y OPS5, donde las reglas pueden tener un factor de saliencia. Las reglas que emiten recomendaciones directas (Prioridad 1) se disparan antes que las que generan necesidades intermedias (Prioridad 2) y rutas de aprendizaje (Prioridad 3).
2. **Especificidad (Mayor número de antecedentes):** Si dos reglas tienen la misma prioridad, se dispara la que requiera más condiciones (más específica), evitando reglas genéricas. Referencia: Algoritmo de Rete y principios de sistemas basados en reglas (Rich & Knight, Inteligencia Artificial).
3. **Orden de Aparición:** Como último criterio de desempate, se respeta el orden de carga del archivo JSON (first-come, first-served).

## 5. Encadenamiento
El motor utiliza **Encadenamiento hacia Adelante (Forward Chaining)**. Un consecuente de una regla pasa a formar parte de la Memoria de Trabajo, lo que puede activar nuevos antecedentes de otras reglas. Ejemplo de esto en el sistema:
`quiere_datos` + `le_gustan_matematicas` → dispara `recomendar_python`. 
Este hecho `recomendar_python` se vuelve antecedente de la regla R11, que infiere `ruta_rapida_python`, la cual activa R12, generando una cadena de inferencia.

## 6. Declaración de Uso de Herramientas de IA Generativa
En cumplimiento de las directrices del taller, declaramos que se utilizaron herramientas de Inteligencia Artificial Generativa (como asistentes conversacionales) como apoyo para:
- La estructuración inicial de la sintaxis del código en Python.
- La redacción y formato de este documento técnico.
- La revisión de la lógica de las reglas y la depuración de errores de sintaxis en JSON.
*Nota: La lógica del caso de estudio, la selección de las reglas y la comprensión del motor fueron realizadas y validadas por los integrantes del grupo.*
