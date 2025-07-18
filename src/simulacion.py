"""
Módulo de simulación para el modelado de Unidades Móviles de Salud.
Implementa algoritmos de simulación Monte Carlo y análisis de sensibilidad.
"""

import numpy as np
from scipy import stats

def generar_demanda_diaria(lambda_poisson):
    """
    Genera una demanda diaria aleatoria usando distribución de Poisson.
    
    Args:
        lambda_poisson: Parámetro lambda (media) de la distribución Poisson.
        
    Returns:
        int: Número de pacientes que demandan atención en un día.
    """
    return np.random.poisson(lambda_poisson)

def calcular_tiempo_atencion(tiempo_promedio):
    """
    Calcula tiempo de atención aleatorio usando distribución exponencial.
    
    Args:
        tiempo_promedio: Tiempo promedio de atención en minutos.
        
    Returns:
        float: Tiempo de atención en minutos.
    """
    # Distribución exponencial con lambda = 1/tiempo_promedio
    return np.random.exponential(tiempo_promedio)

def simular_operacion(parametros, horizonte_temporal, num_simulaciones=1000):
    """
    Realiza múltiples simulaciones de la operación de UMS.
    
    Args:
        parametros: Diccionario con parámetros operativos.
        horizonte_temporal: Número de meses a simular.
        num_simulaciones: Número de simulaciones a ejecutar.
        
    Returns:
        dict: Resultados agregados de las simulaciones.
    """
    resultados = {
        'demanda': [],
        'costos': [],
        'cobertura': [],
        'sostenibilidad': []
    }
    
    # Ejecutar simulaciones
    for i in range(num_simulaciones):
        # Simulación individual
        demanda_total = 0
        costos_totales = 0
        
        # Simulación por mes
        for mes in range(horizonte_temporal):
            # Generar demanda mensual
            demanda_mes = 0
            for dia in range(parametros['capacidad']['dias_mes']):
                demanda_dia = generar_demanda_diaria(parametros['capacidad']['pacientes_dia'])
                capacidad_real = parametros['capacidad']['pacientes_dia'] * parametros['capacidad']['eficiencia']
                atenciones_reales = min(demanda_dia, capacidad_real)
                demanda_mes += atenciones_reales
            
            # Calcular costos del mes
            costo_fijo = parametros['costos']['fijo_mensual']
            costo_variable = demanda_mes * parametros['costos']['variable_paciente']
            costo_mes = costo_fijo + costo_variable
            
            demanda_total += demanda_mes
            costos_totales += costo_mes
        
        # Calcular cobertura y sostenibilidad
        demanda_promedio = demanda_total / horizonte_temporal
        costos_promedio = costos_totales / horizonte_temporal
        
        poblacion_objetivo = parametros['cobertura']['poblacion_objetivo']
        poblacion_atendible_mensual = poblacion_objetivo / 6  # Asumiendo atención semestral
        cobertura = min(1.0, demanda_promedio / poblacion_atendible_mensual)
        
        ingresos_promedio = demanda_promedio * parametros['costos']['costo_unitario_atencion']
        sostenibilidad = ingresos_promedio / costos_promedio if costos_promedio > 0 else 0
        
        # Guardar resultados de esta simulación
        resultados['demanda'].append(demanda_promedio)
        resultados['costos'].append(costos_promedio)
        resultados['cobertura'].append(cobertura)
        resultados['sostenibilidad'].append(sostenibilidad)
    
    # Calcular estadísticas
    estadisticas = {}
    for variable in resultados:
        datos = np.array(resultados[variable])
        estadisticas[variable] = {
            'media': np.mean(datos),
            'mediana': np.median(datos),
            'desviacion': np.std(datos),
            'intervalo_confianza': stats.norm.interval(0.95, loc=np.mean(datos), scale=stats.sem(datos))
        }
    
    return {
        'resultados': resultados,
        'estadisticas': estadisticas
    }

def analisis_sensibilidad(modelo, parametro, rango, num_pasos=10):
    """
    Realiza análisis de sensibilidad variando un parámetro específico.
    
    Args:
        modelo: Instancia del modelo (UMSPractico o UMSTeorico).
        parametro: Tupla (categoria, nombre) del parámetro a variar.
        rango: Tuple (min, max) con rango de variación.
        num_pasos: Número de puntos a evaluar en el rango.
        
    Returns:
        dict: Resultados del análisis de sensibilidad.
    """
    categoria, nombre = parametro
    valores = np.linspace(rango[0], rango[1], num_pasos)
    resultados = {
        'valores': valores.tolist(),
        'demanda': [],
        'costos': [],
        'cobertura': [],
        'sostenibilidad': []
    }
    
    # Valor original
    valor_original = modelo.datos_operativos[categoria][nombre]
    
    for valor in valores:
        # Modificar parámetro
        modelo.datos_operativos[categoria][nombre] = valor
        
        # Ejecutar simulación
        modelo.simular()
        
        # Guardar resultados
        resultados['demanda'].append(modelo.resultados['estadisticas']['demanda']['media'])
        resultados['costos'].append(modelo.resultados['estadisticas']['costos']['media'])
        resultados['cobertura'].append(modelo.resultados['estadisticas']['cobertura']['media'])
        resultados['sostenibilidad'].append(modelo.resultados['estadisticas']['sostenibilidad']['media'])
    
    # Restaurar valor original
    modelo.datos_operativos[categoria][nombre] = valor_original
    
    return resultados