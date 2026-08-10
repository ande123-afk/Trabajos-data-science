# 1. Registro de estudiantes
estudiantes = [
    ("Ana", 20, 4.5),
    ("Luis", 22, 3.8),
    ("Maria", 19, 4.9),
    ("Pedro", 21, 2.7),
    ("Jorge", 23, 4.0),
    ("Sofia", 20, 3.2),
    ("Carlos", 24, 4.7),
    ("Laura", 18, 3.6)
]

# 2. Mostrar la informacion
for nombre, edad, nota in estudiantes:
    print(f"{nombre} tiene {edad} años y obtuvo una nota de {nota}")

# 3. Clasificacion de estudiantes
print("\n--- Clasificacion ---")
for nombre, edad, nota in estudiantes:
    if nota >= 4.5:
        clasificacion = "Excelente"
    elif nota >= 4.0:
        clasificacion = "Bueno"
    elif nota >= 3.0:
        clasificacion = "Aceptable"
    else:
        clasificacion = "Reprobo"
    print(f"{nombre}: {clasificacion}")

# 4. Promedio general
suma_notas = 0
for nombre, edad, nota in estudiantes:
    suma_notas += nota
promedio = suma_notas / len(estudiantes)
print(f"\nPromedio general: {round(promedio, 2)}")

# 5. Busqueda de estudiante
nombre_buscado = input("\nIngresa el nombre del estudiante a buscar: ")
encontrado = False
for nombre, edad, nota in estudiantes:
    if nombre.lower() == nombre_buscado.lower():
        encontrado = True
        break

if encontrado:
    print(f"Estudiante {nombre_buscado} encontrado.")
else:
    print(f"No se encontro ningun estudiante con el nombre {nombre_buscado}.")

# 6. Diccionario de ciudades
ciudades = {
    "Ana": "Bogota",
    "Luis": "Medellin",
    "Maria": "Cali",
    "Pedro": "Bogota",
    "Jorge": "Medellin",
    "Sofia": "Pereira",
    "Carlos": "Bogota",
    "Laura": "Cali"
}

print("\n--- Ciudades ---")
for nombre, ciudad in ciudades.items():
    print(f"{nombre} vive en {ciudad}")

# 7. Cantidad de estudiantes por ciudad
conteo_ciudades = {}
for nombre, ciudad in ciudades.items():
    if ciudad in conteo_ciudades:
        conteo_ciudades[ciudad] += 1
    else:
        conteo_ciudades[ciudad] = 1

print("\n--- Cantidad de estudiantes por ciudad ---")
print(conteo_ciudades)

# 8. Ciclo while - ingresar numeros hasta 0
cantidad = 0
suma_total = 0

while True:
    numero = float(input("\nIngresa un numero (0 para terminar): "))
    if numero == 0:
        break
    cantidad += 1
    suma_total += numero

if cantidad > 0:
    promedio_numeros = suma_total / cantidad
    print(f"\nCantidad de numeros ingresados: {cantidad}")
    print(f"Suma total: {suma_total}")
    print(f"Promedio: {round(promedio_numeros, 2)}")
else:
    print("\nNo se ingresaron numeros.")

# 9. Uso de break y continue
print("\n--- Numeros procesados ---")
for numero in range(1, 31):
    if numero % 3 == 0:
        continue
    if numero == 25:
        break
    print(numero)