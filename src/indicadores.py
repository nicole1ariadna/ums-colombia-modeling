"""
Módulo de indicadores para el modelado de Unidades Móviles de Salud.
Implementa métricas de desempeño y evaluación de calidad.
"""

import numpy as np

def calcular_indices_desempeno(configuracion, metas_ideales):
    """
    Calcula los índices de desempeño basados en la configuración óptima.
    
    Args:
        configuracion: Diccionario con la configuración a evaluar
        metas_ideales: Diccionario con metas normativas ideales
        
    Returns:
        dict: Indicadores calculados por categoría
    """
    # Extraer valores de configuración
    capacidad_diaria = configuracion['capacidad_diaria']
    eficiencia_operativa = configuracion['eficiencia_operativa']
    cobertura_objetivo = configuracion['cobertura_objetivo']
    costo_unitario = configuracion['costo_unitario']
    
    # Calcular indicadores por categoría
    indicadores = {
        'cobertura': {},
        'operacion': {},
        'financiero': {},
        'calidad': {}
    }
    
    # Indicadores de cobertura
    indicadores['cobertura']['poblacion_objetivo'] = cobertura_objetivo
    indicadores['cobertura']['frecuencia_visitas'] = metas_ideales['cobertura']['frecuencia_visitas'] * cobertura_objetivo
    # Tiempo de acceso es inversamente proporcional a la cobertura
    indicadores['cobertura']['tiempo_acceso_max'] = metas_ideales['cobertura']['tiempo_acceso_max'] / cobertura_objetivo
    # Satisfacción aproximada
    indicadores['cobertura']['satisfaccion_min'] = min(
        metas_ideales['cobertura']['satisfaccion_min'],
        0.7 + (0.3 * eficiencia_operativa)
    )
    
    # Indicadores de operación
    indicadores['operacion']['capacidad_optima'] = capacidad_diaria
    indicadores['operacion']['eficiencia_operativa'] = eficiencia_operativa
    # Resolución de primer nivel está relacionada con eficiencia
    indicadores['operacion']['resolucion_primer_nivel'] = min(
        metas_ideales['operacion']['resolucion_primer_nivel'],
        0.7 + (0.3 * eficiencia_operativa)
    )
    # Tiempo de espera inversamente proporcional a eficiencia
    indicadores['operacion']['tiempo_espera_max'] = metas_ideales['operacion']['tiempo_espera_max'] / eficiencia_operativa
    
    # Indicadores financieros
    indicadores['financiero']['costo_unitario_max'] = costo_unitario
    
    # Sostenibilidad calculada
    dias_mes = 20
    atenciones_mensuales = capacidad_diaria * eficiencia_operativa * dias_mes
    costo_fijo_mensual = 17291667  # Valor del modelo práctico
    costo_total = costo_fijo_mensual + (atenciones_mensuales * costo_unitario)
    
    ingresos_estimados = atenciones_mensuales * costo_unitario * 1.1  # 10% de margen
    sostenibilidad = ingresos_estimados / costo_total if costo_total > 0 else 0
    
    indicadores['financiero']['sostenibilidad_min'] = sostenibilidad
    
    # Autofinanciación relacionada con sostenibilidad
    indicadores['financiero']['autofinanciacion'] = min(1.0, sostenibilidad)
    
    # Indicadores de calidad
    # Continuidad de atención relacionada con cobertura
    indicadores['calidad']['continuidad_atencion'] = min(
        metas_ideales['calidad']['continuidad_atencion'],
        cobertura_objetivo * 0.9
    )
    
    # Integración de historia clínica (constante)
    indicadores['calidad']['integracion_historia'] = metas_ideales['calidad']['integracion_historia']
    
    # Referencia efectiva relacionada con eficiencia
    indicadores['calidad']['referencia_efectiva'] = min(
        metas_ideales['calidad']['referencia_efectiva'],
        0.8 + (0.2 * eficiencia_operativa)
    )
    
    return indicadores

def calcular_indice_equidad(poblacion, cobertura):
    """
    Calcula el índice de equidad (coeficiente Gini invertido).
    
    Args:
        poblacion: Lista de tamaños de población por región.
        cobertura: Lista de porcentajes de cobertura por región.
        
    Returns:
        float: Índice de equidad (1-Gini), donde 1 es perfecta equidad.
    """
    # Verificar que las listas tengan el mismo tamaño
    if len(poblacion) != len(cobertura):
        raise ValueError("Las listas de población y cobertura deben tener el mismo tamaño")
    
    # Calcular población atendida por región
    poblacion_atendida = [p * c for p, c in zip(poblacion, cobertura)]
    
    # Ordenar por cobertura ascendente
    regiones_ordenadas = sorted(zip(poblacion, poblacion_atendida), key=lambda x: x[1]/x[0] if x[0] > 0 else 0)
    
    # Calcular coeficiente de Gini
    poblacion_total = sum(p for p, _ in regiones_ordenadas)
    poblacion_atendida_total = sum(a for _, a in regiones_ordenadas)
    
    # Acumuladores para el cálculo de Gini
    poblacion_acum = 0
    poblacion_atendida_acum = 0
    area = 0
    
    for p, a in regiones_ordenadas:
        # Incremento en el eje X
        x_increment = p / poblacion_total
        
        # Altura previa en el eje Y
        y_prev = poblacion_atendida_acum / poblacion_atendida_total if poblacion_atendida_total > 0 else 0
        
        # Incremento en población atendida
        poblacion_atendida_acum += a
        
        # Nueva altura en el eje Y
        y_new = poblacion_atendida_acum / poblacion_atendida_total if poblacion_atendida_total > 0 else 0
        
        # Área del trapecio
        area += x_increment * (y_prev + y_new) / 2
        
        # Actualizar acumulado de población
        poblacion_acum += p
    
    # Coeficiente de Gini = 1 - 2 * área bajo la curva de Lorenz
    gini = 1 - 2 * area
    
    # Índice de equidad = 1 - Gini (donde 1 es perfecta equidad)
    return 1 - gini

def calcular_cobertura_efectiva(poblacion_regional, capacidad_ums, distancia_centros):
    """
    Calcula la cobertura efectiva considerando la capacidad y distancia.
    
    Args:
        poblacion_regional: Lista de tamaños de población por región.
        capacidad_ums: Lista de capacidades de atención por UMS en cada región.
        distancia_centros: Lista de distancias promedio a centros de salud (horas).
        
    Returns:
        list: Porcentajes de cobertura efectiva por región.
    """
    cobertura_efectiva = []
    
    for i in range(len(poblacion_regional)):
        # Ajustar capacidad por población
        if poblacion_regional[i] > 0:
            ratio_capacidad = min(1.0, capacidad_ums[i] / (poblacion_regional[i] / 6))  # 1 atención cada 6 meses
        else:
            ratio_capacidad = 0
        
        # Factor de disminución por distancia
        # Asumimos que a mayor distancia, menor cobertura efectiva (relación inversa)
        factor_distancia = 1.0 / (1.0 + distancia_centros[i])
        
        # Cobertura efectiva
        cobertura = ratio_capacidad * factor_distancia
        cobertura_efectiva.append(min(1.0, cobertura))
    
    return cobertura_efectiva

def evaluar_impacto_salud(cobertura_inicial, cobertura_proyectada, indicadores_salud_base):
    """
    Evalúa el impacto en indicadores de salud basado en cambios de cobertura.
    
    Args:
        cobertura_inicial: Cobertura de servicios antes de UMS (%).
        cobertura_proyectada: Cobertura de servicios con UMS implementadas (%).
        indicadores_salud_base: Diccionario con indicadores de salud base.
        
    Returns:
        dict: Indicadores de salud proyectados.
    """
    # Extraer indicadores base
    mortalidad_infantil_base = indicadores_salud_base.get('mortalidad_infantil', 18)
    cobertura_vacunacion_base = indicadores_salud_base.get('cobertura_vacunacion', 0.68)
    acceso_aps_base = indicadores_salud_base.get('acceso_aps', 0.42)
    
    # Calcular incremento en cobertura
    if cobertura_inicial > 0:
        incremento_cobertura = (cobertura_proyectada - cobertura_inicial) / cobertura_inicial
    else:
        incremento_cobertura = cobertura_proyectada
    
    # Estimar impacto en indicadores
    # Mortalidad infantil: reducción proporcional al aumento de cobertura
    factor_reduccion_mortalidad = 0.3 * min(1.0, incremento_cobertura)
    mortalidad_infantil_proyectada = mortalidad_infantil_base * (1 - factor_reduccion_mortalidad)
    
    # Cobertura de vacunación: aumento directo pero con límite superior
    incremento_vacunacion = min(0.27, incremento_cobertura * 0.5)  # Máximo incremento de 27%
    cobertura_vacunacion_proyectada = min(0.95, cobertura_vacunacion_base + incremento_vacunacion)
    
    # Acceso a APS: aumento directo pero con límite superior
    incremento_aps = min(0.48, incremento_cobertura * 0.7)  # Máximo incremento de 48%
    acceso_aps_proyectado = min(0.9, acceso_aps_base + incremento_aps)
    
    return {
        'mortalidad_infantil': mortalidad_infantil_proyectada,
        'cobertura_vacunacion': cobertura_vacunacion_proyectada,
        'acceso_aps': acceso_aps_proyectado
    }