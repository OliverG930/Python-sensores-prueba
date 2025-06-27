import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime #Sive para las fechas y se utiliza cuando se guarda el archivo ".csv" que se genera, para documentar la fecha en la que se genero el archivo....
import random #Genera los numeros aleatorios para hacer simulaciones de casos que pueden ocurrir....
import tkinter as tk
from tkinter import filedialog

# Se crea la carpeta de "informes" si no existe.
if not os.path.exists("informes"):
    os.makedirs("informes")

def generar_datos(situacion='normal', cantidad=100):
    if situacion == 'normal':
        temperatura = np.random.normal(loc=70, scale=5, size=cantidad)
        velocidad = np.random.normal(loc=1500, scale=100, size=cantidad)
        presion = np.random.normal(loc=30, scale=3, size=cantidad)
    else:
        temperatura = np.random.normal(loc=90, scale=10, size=cantidad)
        velocidad = np.random.normal(loc=1800, scale=200, size=cantidad)
        presion = np.random.normal(loc=45, scale=7, size=cantidad)
    return list(zip(temperatura, velocidad, presion))

def guardar_csv(datos, riesgo=False):
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    codigo = f"_{random.randint(1000,9999)}" if riesgo else ""
    filename = f"informes/simulacion_{fecha}{codigo}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Temperatura (°C)', 'Velocidad (rpm)', 'Presión (bar)'])
        writer.writerows(datos)
    print(f"✅ Archivo guardado como: {filename}")
    return filename

def analizar_datos(datos):
    datos_np = np.array(datos)
    print("\n📈 Estadísticas:")
    for i, sensor in enumerate(['Temperatura', 'Velocidad', 'Presión']):
        print(f"{sensor}: media={np.mean(datos_np[:, i]):.2f}, desviación={np.std(datos_np[:, i]):.2f}, min={np.min(datos_np[:, i]):.2f}, max={np.max(datos_np[:, i]):.2f}")

def graficar_datos(datos, tipo_simulacion='SIMULACIÓN'):
    datos_np = np.array(datos)
    tiempo = range(len(datos))
    plt.figure(figsize=(12, 6))
    plt.plot(tiempo, datos_np[:, 0], label='Temperatura (°C)', color='red')
    plt.plot(tiempo, datos_np[:, 1], label='Velocidad (rpm)', color='blue')
    plt.plot(tiempo, datos_np[:, 2], label='Presión (bar)', color='green')
    plt.title(f'Simulación de sensores - Turbina Hidroeléctrica ({tipo_simulacion})')
    plt.xlabel('Tiempo (simulado)')
    plt.ylabel('Valores de sensores')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)

def cargar_csv():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=[("CSV files", "*.csv"), ("Archivos Word", "*.doc *.docx")]) #Validacion para solo recibir archivos ".csv" de Excel y ".docx" de Word....
    if file_path:
        print(f"📂 Archivo cargado: {file_path}")
        if file_path.endswith('.csv'):
            with open(file_path, newline='') as file:
                reader = csv.reader(file)
                next(reader)
                datos = [tuple(map(float, row)) for row in reader]
            return datos
        else:
            print("📄 Archivo de Word cargado (no se puede analizar, solo se registró).")
            return None
    else:
        print("❌ No se seleccionó ningún archivo.")
        return None

#  Menú principal...........
salir = False
while not salir:
    print("\n--- Menú Principal ---")
    print("1. Generar Simulación")
    print("2. Cargar archivo CSV")
    print("3. Salir")
    opcion = input("Seleccione una opción (1/2/3): ").strip()

    if opcion == '1':
        tipo = input("¿Desea simular situación Normal (N) o de Riesgo (R)? (n/r): ").strip().lower() #validado por si el usuario digita mayusculas o minusculas.
        while tipo not in ['n', 'r']:
            tipo = input("Entrada inválida. Ingrese 'n' para normal o 'r' para riesgo: ").strip().lower()

        situacion = 'normal' if tipo == 'n' else 'riesgo'
        tipo_simulacion = 'CASO NORMAL' if situacion == 'normal' else 'CASO DE RIESGO'

        print(f"\n🔍 Generando simulación de tipo: {tipo_simulacion}")
        datos = generar_datos(situacion=situacion)
        archivo = guardar_csv(datos, riesgo=(situacion == 'riesgo'))
        analizar_datos(datos)
        graficar_datos(datos, tipo_simulacion=tipo_simulacion)
        input("\nPresione ENTER para volver al menú...")

    elif opcion == '2':
        datos = cargar_csv()
        if datos:
            analizar_datos(datos)
            graficar_datos(datos, tipo_simulacion='ARCHIVO CARGADO')
            input("\nPresione ENTER para volver al menú...")

    elif opcion == '3':
        salir = True
        print("👋 Programa finalizado. ¡Hasta luego!")
    else:
        print("❗ Opción no válida. Intente nuevamente.")
