#Valeria Hernández 25086

import simpy
import random

RANDOM_SEED = 42

NUM_PROCESOS = 200
INTERVALO = 1
RAM_CAPACIDAD = 100
NUMERO_CPU = 2
INSTRUCCIONES_CPU = 3

def proceso(env, nombre, ram, cpu, instrucciones_cpu, tiempos):
    #Simula el ciclo de un proceso
    #Solicita RAM, ejecuta en CPU por cierta cantidad de instrucciones
    #Puede pasar a I/O antes de terminar, y al finalizar devuelve la RAM
    tiempo_llegada = env.now

    memoria = random.randint(1, 10)
    instrucciones = random.randint(1, 10)

    yield ram.get(memoria)


    while instrucciones > 0:
        with cpu.request() as req:
            yield req

            #Ejecuta hasta ciertas cantidad de instrucciones en 1 unidad de tiempo
            ejecutar = min(instrucciones, instrucciones_cpu)
            yield env.timeout(1)
            instrucciones -= ejecutar

        #Probabilidad de pasar a I/O (1/21)
        decision = random.randint(1, 21)
        if decision == 1:
            yield env.timeout(1)
    
    yield ram.put(memoria)

    tiempo_total = env.now - tiempo_llegada
    tiempos.append(tiempo_total)


def generar_procesos(env, numero_procesos, intervalo, ram, cpu, instrucciones_cpu, tiempos):
    #Genera los procesos con llegadas exponenciales
    for i in range(numero_procesos):
        env.process(proceso(env, f"Proceso-{i}", ram, cpu, instrucciones_cpu, tiempos))
        llegada = random.expovariate(1.0 / intervalo)
        yield env.timeout(llegada)


def simular(numero_procesos, intervalo, ram, numero_cpu, instrucciones_cpu):
    random.seed(RANDOM_SEED)
    
    env = simpy.Environment()

    ram = simpy.Container(env, init=ram, capacity=ram)
    cpu = simpy.Resource(env, capacity=numero_cpu)

    tiempos = []

    env.process(generar_procesos(env, numero_procesos, intervalo, ram, cpu, instrucciones_cpu, tiempos))
    env.run()

    if len(tiempos) > 0:
        promedio = sum(tiempos) / len(tiempos)
    else:
        promedio = 0

    if len(tiempos) > 1:
        desviacion = (sum((x - promedio) ** 2 for x in tiempos) / len(tiempos)) ** 0.5
    else:
        desviacion = 0

    return promedio, desviacion 


#Llamada de la simulación
promedio, desviacion = simular(NUM_PROCESOS, INTERVALO, RAM_CAPACIDAD, NUMERO_CPU, INSTRUCCIONES_CPU)

print ("Configuración:")
print (f"  Número de procesos: {NUM_PROCESOS}")
print (f"  Intervalo de llegada: {INTERVALO}")
print (f"  RAM: {RAM_CAPACIDAD}")
print (f"  Número de CPUs: {NUMERO_CPU}")
print (f"  Instrucciones por CPU: {INSTRUCCIONES_CPU}")
print (f"  Tiempo promedio: {promedio:.4f}")
print (f"  Desviación estándar: {desviacion:.4f}")