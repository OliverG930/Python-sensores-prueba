import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Simulación de datos del sensor de vibración/acelerómetro.......
def generar_datos_sensor(num_muestras=1000):
    tiempo = np.linspace(0, 100, num_muestras)
    ruido = np.random.normal(0, 0.2, num_muestras)  # Pequeñas variaciones normales..
    vibracion_base = np.sin(0.5 * tiempo)  # Se simula el movimiento normal del vehículo....
    baches = (np.random.rand(num_muestras) > 0.98) * np.random.uniform(-2, 2, num_muestras)  # Se ponen Baches aleatorios.....
    datos = vibracion_base + ruido + baches
    return tiempo, datos


# Leer datos desde un archivo CSV
def leer_datos_csv(nombre_archivo):
    df = pd.read_csv(nombre_archivo)
    return df["Tiempo"].values, df["Vibración"].values


# Detección de irregularidades usando umbral de variación brusca
def detectar_irregularidades(datos, umbral=1.0):
    diferencias = np.abs(np.diff(datos))
    indices_anomalos = np.where(diferencias > umbral)[0]
    return indices_anomalos


# Guardar detecciones en un archivo CSV
def exportar_datos_csv(tiempo, datos_sensor, indices_baches, nombre_archivo="detecciones.csv"): #Ver para que ponga id y los nombre de archivos no se repitan..
    df = pd.DataFrame({"Tiempo": tiempo, "Vibración": datos_sensor})
    df["Irregularidad"] = 0
    df.loc[indices_baches, "Irregularidad"] = 1
    df.to_csv(nombre_archivo, index=False)
    print(f"Datos exportados a {nombre_archivo}")


if __name__ == "__main__":
    while True:
        print("\nMenú:")
        print("1. Generar datos simulados")
        print("2. Leer datos desde un archivo CSV") 
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            tiempo, datos_sensor = generar_datos_sensor() 
        elif opcion == "2":
            nombre_archivo = input("Introduce el nombre del archivo CSV: ")
            tiempo, datos_sensor = leer_datos_csv(nombre_archivo)
        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            continue

        # Procesamiento de datos......
        indices_baches = detectar_irregularidades(datos_sensor)
        exportar_datos_csv(tiempo, datos_sensor, indices_baches)

        # Visualización de los datos.........
        plt.figure(figsize=(10, 5))
        plt.plot(tiempo, datos_sensor, label='Vibración del vehículo', color='blue')
        plt.scatter(tiempo[indices_baches], datos_sensor[indices_baches], color='red',
                    label='Irregularidades detectadas')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Intensidad de vibración')
        plt.title('Detección de irregularidades en el camino')
        plt.legend()
        plt.grid()
        plt.show()