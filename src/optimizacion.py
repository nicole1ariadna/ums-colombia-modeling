"""
Módulo de optimización para el modelado de Unidades Móviles de Salud.
Implementa algoritmos de optimización multiobjetivo y programación lineal.
"""

import numpy as np
from scipy.optimize import minimize

def funcion_objetivo(x, metas_ideales):
    """
    Función objetivo para optimización.
    Minimiza una combinación de costo y penalización por inequidad.
    
    Args:
        x: Vector de variables de decisión 
           [capacidad_diaria, eficiencia_operativa, cobertura_objetivo, costo_unitario]
        metas_ideales: Diccionario con metas ideales para comparar
    
    Returns:
        float: Valor objetivo a minimizar
    """
    # Desempacar variables de decisión
    capacidad_diaria = x[0]
    eficiencia_operativa = x[1]
    cobertura_objetivo = x[2]
    costo_unitario = x[3]
    
    # Penalización por desviación de metas ideales
    penalizacion_capacidad = abs(capacidad_diaria - metas_ideales['operacion']['capacidad_optima']) / metas_ideales['operacion']['capacidad_optima']
    penalizacion_eficiencia = abs(eficiencia_operativa - metas_ideales['operacion']['eficiencia_operativa']) / metas_ideales['operacion']['eficiencia_operativa']
    penalizacion_cobertura = abs(cobertura_objetivo - metas_ideales['cobertura']['poblacion_objetivo']) / metas_ideales['cobertura']['poblacion_objetivo']
    penalizacion_costo = abs(costo_unitario - metas_ideales['financiero']['costo_unitario_max']) / metas_ideales['financiero']['costo_unitario_max']
    
    # Costo total mensual estimado
    dias_mes = 20
    atenciones_mensuales = capacidad_diaria * eficiencia_operativa * dias_mes
    costo_fijo_mensual = 17291667  # Valor del modelo práctico
    costo_total = costo_fijo_mensual + (atenciones_mensuales * costo_unitario)
    
    # Calcular sostenibilidad financiera
    ingresos_estimados = atenciones_mensuales * costo_unitario * 1.1  # 10% de margen
    sostenibilidad = ingresos_estimados / costo_total if costo_total > 0 else 0
    penalizacion_sostenibilidad = max(0, metas_ideales['financiero']['sostenibilidad_min'] - sostenibilidad)
    
    # Función objetivo: Minimizar costo y penalizaciones
    # Pesos para cada componente
    w_costo = 0.4
    w_penalizacion = 0.6
    
    # Normalización del costo (asumiendo que 25 millones es una referencia)
    costo_normalizado = costo_total / 25000000
    
    # Suma ponderada de penalizaciones
    penalizacion_total = (
        0.25 * penalizacion_capacidad +
        0.25 * penalizacion_eficiencia +
        0.25 * penalizacion_cobertura +
        0.25 * penalizacion_costo +
        2.0 * penalizacion_sostenibilidad  # Mayor peso para sostenibilidad
    )
    
    return w_costo * costo_normalizado + w_penalizacion * penalizacion_total

def restriccion_cobertura_minima(x, valor_min):
    """Restricción: La cobertura debe ser mayor o igual al mínimo."""
    cobertura = x[2]
    return cobertura - valor_min

def restriccion_calidad_minima(x, valor_min):
    """
    Restricción: La calidad (aproximada por eficiencia) debe ser mayor 
    o igual al mínimo.
    """
    eficiencia = x[1]
    # Asumimos que la calidad es proporcional a la eficiencia
    return eficiencia - valor_min

def restriccion_sostenibilidad_minima(x, valor_min):
    """Restricción: La sostenibilidad debe ser mayor o igual al mínimo."""
    capacidad_diaria = x[0]
    eficiencia_operativa = x[1]
    costo_unitario = x[3]
    
    dias_mes = 20
    atenciones_mensuales = capacidad_diaria * eficiencia_operativa * dias_mes
    costo_fijo_mensual = 17291667  # Valor del modelo práctico
    costo_total = costo_fijo_mensual + (atenciones_mensuales * costo_unitario)
    
    ingresos_estimados = atenciones_mensuales * costo_unitario * 1.1  # 10% de margen
    sostenibilidad = ingresos_estimados / costo_total if costo_total > 0 else 0
    
    return sostenibilidad - valor_min

def optimizar_configuracion_ums(x0, metas_ideales, restricciones):
    """
    Optimiza la configuración de UMS utilizando programación no lineal.
    
    Args:
        x0: Vector inicial [capacidad_diaria, eficiencia_operativa, cobertura_objetivo, costo_unitario]
        metas_ideales: Diccionario con metas ideales para comparar
        restricciones: Lista de restricciones a aplicar
    
    Returns:
        OptimizeResult: Resultado de la optimización
    """
    # Convertir restricciones al formato requerido por scipy.optimize
    constraints = []
    
    for restriccion in restricciones:
        if restriccion['tipo'] == 'cobertura_minima':
            constraints.append({
                'type': 'ineq',
                'fun': lambda x, valor_min=restriccion['valor']: restriccion_cobertura_minima(x, valor_min)
            })
        elif restriccion['tipo'] == 'calidad_minima':
            constraints.append({
                'type': 'ineq',
                'fun': lambda x, valor_min=restriccion['valor']: restriccion_calidad_minima(x, valor_min)
            })
        elif restriccion['tipo'] == 'sostenibilidad_minima':
            constraints.append({
                'type': 'ineq',
                'fun': lambda x, valor_min=restriccion['valor']: restriccion_sostenibilidad_minima(x, valor_min)
            })
    
    # Límites para las variables
    bounds = [
        (20, 50),      # capacidad_diaria: entre 20 y 50 pacientes/día
        (0.4, 0.95),   # eficiencia_operativa: entre 40% y 95%
        (0.6, 1.0),    # cobertura_objetivo: entre 60% y 100%
        (50000, 120000) # costo_unitario: entre 50,000 y 120,000 COP
    ]
    
    # Ejecutar optimización
    result = minimize(
        fun=lambda x: funcion_objetivo(x, metas_ideales),
        x0=x0,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints,
        options={'maxiter': 1000, 'disp': False}
    )
    
    return result