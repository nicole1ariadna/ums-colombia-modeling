"""
Módulo de costos para el modelado de Unidades Móviles de Salud.
Implementa cálculos financieros y análisis de sostenibilidad.
"""

import numpy as np

def calcular_costos_totales(atenciones, costos_fijos, costo_variable):
    """
    Calcula los costos totales mensuales de operación de UMS.
    
    Args:
        atenciones: Número de atenciones en el mes.
        costos_fijos: Costos fijos mensuales (COP).
        costo_variable: Costo variable por atención (COP).
        
    Returns:
        float: Costo total mensual (COP).
    """
    return costos_fijos + (atenciones * costo_variable)

def calcular_punto_equilibrio(costos_fijos, costo_variable, precio_unitario):
    """
    Calcula el punto de equilibrio (número de atenciones para cubrir costos).
    
    Args:
        costos_fijos: Costos fijos mensuales (COP).
        costo_variable: Costo variable por atención (COP).
        precio_unitario: Precio o ingreso por atención (COP).
        
    Returns:
        float: Número de atenciones para alcanzar punto de equilibrio.
    """
    if precio_unitario <= costo_variable:
        return float('inf')  # No hay punto de equilibrio
    
    return costos_fijos / (precio_unitario - costo_variable)

def analizar_sostenibilidad(ingresos, costos):
    """
    Calcula el ratio de sostenibilidad financiera.
    
    Args:
        ingresos: Ingresos totales (COP).
        costos: Costos totales (COP).
        
    Returns:
        float: Ratio de sostenibilidad (ingresos/costos).
    """
    if costos == 0:
        return float('inf')
    
    return ingresos / costos

def calcular_flujo_caja(parametros_iniciales, horizonte_temporal=60, tasa_inflacion=0.04, tasa_descuento=0.12):
    """
    Calcula el flujo de caja proyectado para UMS.
    
    Args:
        parametros_iniciales: Diccionario con parámetros iniciales.
        horizonte_temporal: Número de meses a proyectar.
        tasa_inflacion: Tasa de inflación mensual.
        tasa_descuento: Tasa de descuento anual para VPN.
        
    Returns:
        dict: Flujo de caja proyectado y métricas financieras.
    """
    # Convertir tasa de descuento anual a mensual
    tasa_descuento_mensual = (1 + tasa_descuento) ** (1/12) - 1
    
    # Extraer parámetros iniciales
    capacidad_diaria = parametros_iniciales['capacidad']['pacientes_dia']
    dias_mes = parametros_iniciales['capacidad']['dias_mes']
    eficiencia = parametros_iniciales['capacidad']['eficiencia']
    
    costo_fijo_mensual = parametros_iniciales['costos']['fijo_mensual']
    costo_variable = parametros_iniciales['costos']['variable_paciente']
    costo_unitario_atencion = parametros_iniciales['costos']['costo_unitario_atencion']
    
    # Inversión inicial (vehículo)
    inversion_inicial = parametros_iniciales['costos']['costo_vehiculo']
    
    flujo = {
        'inversion_inicial': inversion_inicial,
        'meses': [],
        'atenciones': [],
        'ingresos': [],
        'costos_fijos': [],
        'costos_variables': [],
        'costos_totales': [],
        'flujo_neto': [],
        'flujo_descontado': []
    }
    
    # Proyección mensual
    for mes in range(horizonte_temporal):
        # Ajustes por inflación
        factor_inflacion = (1 + tasa_inflacion) ** mes
        costo_fijo_ajustado = costo_fijo_mensual * factor_inflacion
        costo_variable_ajustado = costo_variable * factor_inflacion
        precio_unitario_ajustado = costo_unitario_atencion * factor_inflacion
        
        # Capacidad y eficiencia (pueden variar con el tiempo)
        # Por simplicidad asumimos que aumentan ligeramente con la experiencia
        factor_eficiencia = min(1.0, eficiencia * (1 + 0.005 * mes))
        
        # Atenciones mensuales
        atenciones = capacidad_diaria * factor_eficiencia * dias_mes
        
        # Cálculos financieros
        ingresos = atenciones * precio_unitario_ajustado
        costo_variable_total = atenciones * costo_variable_ajustado
        costo_total = costo_fijo_ajustado + costo_variable_total
        flujo_neto = ingresos - costo_total
        
        # Valor presente del flujo
        factor_descuento = 1 / ((1 + tasa_descuento_mensual) ** mes)
        flujo_descontado = flujo_neto * factor_descuento
        
        # Guardar datos del mes
        flujo['meses'].append(mes)
        flujo['atenciones'].append(atenciones)
        flujo['ingresos'].append(ingresos)
        flujo['costos_fijos'].append(costo_fijo_ajustado)
        flujo['costos_variables'].append(costo_variable_total)
        flujo['costos_totales'].append(costo_total)
        flujo['flujo_neto'].append(flujo_neto)
        flujo['flujo_descontado'].append(flujo_descontado)
    
    # Calcular métricas financieras
    flujo['vpn'] = -inversion_inicial + sum(flujo['flujo_descontado'])
    
    # Calcular TIR (aproximación)
    try:
        flujos_con_inversion = [-inversion_inicial] + flujo['flujo_neto']
        flujo['tir'] = np.irr(flujos_con_inversion)
    except:
        flujo['tir'] = None  # No se puede calcular TIR
    
    # Periodo de recuperación descontado
    flujo_acumulado = -inversion_inicial
    for i, f in enumerate(flujo['flujo_descontado']):
        flujo_acumulado += f
        if flujo_acumulado >= 0:
            flujo['periodo_recuperacion'] = i + 1
            break
    else:
        flujo['periodo_recuperacion'] = None  # No se recupera en el horizonte temporal
    
    return flujo

def analizar_escenarios(modelo, escenarios):
    """
    Analiza múltiples escenarios variando parámetros clave.
    
    Args:
        modelo: Instancia del modelo (UMSPractico o UMSTeorico).
        escenarios: Diccionario de escenarios con variaciones porcentuales.
        
    Returns:
        dict: Resultados de los diferentes escenarios.
    """
    resultados = {}
    
    # Guardar configuración original
    config_original = {
        'capacidad': modelo.datos_operativos['capacidad'].copy(),
        'costos': modelo.datos_operativos['costos'].copy(),
        'cobertura': modelo.datos_operativos['cobertura'].copy()
    }
    
    # Analizar cada escenario
    for nombre, variaciones in escenarios.items():
        # Aplicar variaciones
        for categoria, parametros in variaciones.items():
            for param, variacion in parametros.items():
                # Variación porcentual
                valor_original = modelo.datos_operativos[categoria][param]
                modelo.datos_operativos[categoria][param] = valor_original * (1 + variacion)
        
        # Ejecutar simulación con esta configuración
        modelo.simular()
        
        # Guardar resultados
        resultados[nombre] = {
            'demanda': modelo.resultados['estadisticas']['demanda']['media'],
            'costos': modelo.resultados['estadisticas']['costos']['media'],
            'cobertura': modelo.resultados['estadisticas']['cobertura']['media'],
            'sostenibilidad': modelo.resultados['estadisticas']['sostenibilidad']['media']
        }
        
        # Restaurar configuración original
        modelo.datos_operativos['capacidad'] = config_original['capacidad'].copy()
        modelo.datos_operativos['costos'] = config_original['costos'].copy()
        modelo.datos_operativos['cobertura'] = config_original['cobertura'].copy()
    
    return resultados