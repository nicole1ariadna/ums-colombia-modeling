"""
Módulo para la visualización de resultados y generación de gráficos.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
from io import BytesIO

def generar_graficos_practico(resultados):
    """
    Genera gráficos para el modelo práctico.
    
    Args:
        resultados: Diccionario con resultados del modelo práctico.
        
    Returns:
        dict: Diccionario de figuras generadas.
    """
    if not resultados or 'estadisticas' not in resultados:
        return {}
    
    graficos = {}
    
    # Gráfico de distribución de demanda
    graficos['demanda'] = generar_grafico_demanda(resultados)
    
    # Gráfico de relación entre costos y demanda
    graficos['costos_demanda'] = generar_grafico_costos_demanda(resultados)
    
    # Gráfico de sostenibilidad vs cobertura
    graficos['sostenibilidad'] = generar_grafico_sostenibilidad(resultados)
    
    # Dashboard con indicadores principales
    graficos['dashboard'] = generar_dashboard_practico(resultados)
    
    return graficos

def generar_grafico_demanda(resultados):
    """Genera histograma de demanda."""
    # Crear la figura explícitamente
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    
    if 'demanda' in resultados:
        demanda = resultados['demanda']
        
        # Crear histograma
        n, bins, patches = ax.hist(demanda, bins=20, color='skyblue', alpha=0.7)
        
        # Añadir línea con la media
        media = resultados['estadisticas']['demanda']['media']
        ax.axvline(media, color='red', linestyle='dashed', linewidth=2, label=f'Media: {media:.1f}')
        
        # Configurar gráfico
        ax.set_title('Distribución de Demanda Mensual', fontsize=14)
        ax.set_xlabel('Número de atenciones por mes', fontsize=12)
        ax.set_ylabel('Frecuencia', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        
    return fig

def generar_grafico_costos_demanda(resultados):
    """Genera gráfico de dispersión entre costos y demanda."""
    # Crear la figura explícitamente
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    
    if 'costos' in resultados and 'demanda' in resultados:
        costos = resultados['costos']
        demanda = resultados['demanda']
        
        # Crear gráfico de dispersión
        ax.scatter(demanda, costos, alpha=0.6, color='blue')
        
        # Añadir línea de tendencia
        z = np.polyfit(demanda, costos, 1)
        p = np.poly1d(z)
        ax.plot(demanda, p(demanda), "r--", alpha=0.8, 
                label=f"Tendencia: y={z[0]:.0f}x+{z[1]:.0f}")
        
        # Configurar gráfico
        ax.set_title('Relación entre Demanda y Costos', fontsize=14)
        ax.set_xlabel('Demanda (atenciones por mes)', fontsize=12)
        ax.set_ylabel('Costos mensuales (COP)', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        
        # Formatear eje Y como moneda
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${x:,.0f}"))
        
    return fig

def generar_grafico_sostenibilidad(resultados):
    """Genera gráfico de dispersión entre cobertura y sostenibilidad."""
    # Crear la figura explícitamente
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    
    if 'cobertura' in resultados and 'sostenibilidad' in resultados and 'costos' in resultados:
        cobertura = np.array(resultados['cobertura'])
        sostenibilidad = np.array(resultados['sostenibilidad'])
        costos = np.array(resultados['costos'])
        
        # Crear gráfico de dispersión con color según costos
        sc = ax.scatter(cobertura, sostenibilidad, c=costos, cmap='viridis', 
                       alpha=0.7, s=50)
        
        # Añadir línea horizontal en sostenibilidad = 1
        ax.axhline(y=1, color='red', linestyle='--', alpha=0.7, 
                  label='Equilibrio')
        
        # Configurar gráfico
        ax.set_title('Relación entre Cobertura y Sostenibilidad', fontsize=14)
        ax.set_xlabel('Cobertura (%)', fontsize=12)
        ax.set_ylabel('Ratio de Sostenibilidad (Ingresos/Costos)', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        
        # Formatear ejes
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{x*100:.1f}%"))
        
        # Añadir barra de color - FIX: usar fig en lugar de plt
        cbar = fig.colorbar(sc, ax=ax)
        cbar.set_label('Costos (COP)')
        cbar.formatter = ticker.FuncFormatter(lambda x, p: f"${x:,.0f}")
        cbar.update_ticks()
        
    return fig

def generar_dashboard_practico(resultados):
    """Genera un dashboard con múltiples indicadores."""
    # Crear la figura explícitamente
    fig = Figure(figsize=(10, 8))
    
    if 'estadisticas' in resultados:
        stats = resultados['estadisticas']
        
        # Crear subplots
        ax1 = fig.add_subplot(221)  # Demanda
        ax2 = fig.add_subplot(222)  # Costos
        ax3 = fig.add_subplot(223)  # Cobertura
        ax4 = fig.add_subplot(224)  # Sostenibilidad
        
        # Gráfico 1: Demanda (barras)
        ax1.bar(['Media', 'Mediana'], 
               [stats['demanda']['media'], stats['demanda']['mediana']], 
               color=['blue', 'lightblue'])
        ax1.set_title('Demanda Mensual')
        ax1.grid(True, linestyle='--', alpha=0.7, axis='y')
        
        # Gráfico 2: Costos (barras)
        ax2.bar(['Media', 'Mediana'], 
               [stats['costos']['media'], stats['costos']['mediana']], 
               color=['green', 'lightgreen'])
        ax2.set_title('Costos Mensuales')
        ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${x/1000000:.1f}M"))
        ax2.grid(True, linestyle='--', alpha=0.7, axis='y')
        
        # Gráfico 3: Cobertura (gauge)
        cobertura = stats['cobertura']['media']
        gauge_cobertura(ax3, cobertura, 'Cobertura')
        
        # Gráfico 4: Sostenibilidad (gauge)
        sostenibilidad = stats['sostenibilidad']['media']
        gauge_sostenibilidad(ax4, sostenibilidad, 'Sostenibilidad')
        
        # Ajustar espaciado
        fig.tight_layout()
    
    return fig

def gauge_cobertura(ax, value, title):
    """Crea un gráfico tipo gauge para cobertura."""
    # Configuración
    angles = np.linspace(0.1, np.pi-0.1, 1000)
    value = min(max(value, 0), 1)  # Asegurar que esté entre 0 y 1
    
    # Dibujar arco de fondo
    ax.plot(angles, [0.9]*len(angles), 'lightgrey', linewidth=15)
    
    # Dibujar arco de valor
    value_angles = np.linspace(0.1, 0.1 + (np.pi-0.2)*value, 1000)
    if value <= 0.3:
        color = 'red'
    elif value <= 0.7:
        color = 'orange'
    else:
        color = 'green'
    ax.plot(value_angles, [0.9]*len(value_angles), color, linewidth=15)
    
    # Configurar aspecto
    ax.set_title(title)
    ax.text(np.pi/2, 0.6, f"{value*100:.1f}%", ha='center', fontsize=18)
    ax.set_ylim(0, 1.2)
    ax.set_xlim(0, np.pi)
    ax.grid(False)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])

def gauge_sostenibilidad(ax, value, title):
    """Crea un gráfico tipo gauge para sostenibilidad."""
    # Configuración
    angles = np.linspace(0.1, np.pi-0.1, 1000)
    norm_value = min(max(value/2, 0), 1)  # Normalizar valor para gauge
    
    # Dibujar arco de fondo
    ax.plot(angles, [0.9]*len(angles), 'lightgrey', linewidth=15)
    
    # Dibujar arco de valor
    value_angles = np.linspace(0.1, 0.1 + (np.pi-0.2)*norm_value, 1000)
    if value < 0.8:
        color = 'red'
    elif value < 1:
        color = 'orange'
    else:
        color = 'green'
    ax.plot(value_angles, [0.9]*len(value_angles), color, linewidth=15)
    
    # Configurar aspecto
    ax.set_title(title)
    ax.text(np.pi/2, 0.6, f"{value:.2f}", ha='center', fontsize=18)
    ax.set_ylim(0, 1.2)
    ax.set_xlim(0, np.pi)
    ax.grid(False)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])

def generar_graficos_teorico(resultados):
    """
    Genera gráficos para el modelo teórico.
    
    Args:
        resultados: Diccionario con resultados del modelo teórico.
        
    Returns:
        dict: Diccionario de figuras generadas.
    """
    if not resultados or 'configuracion' not in resultados:
        return {}
    
    graficos = {}
    
    # Gráfico de configuración óptima
    graficos['configuracion_optima'] = generar_grafico_configuracion(resultados)
    
    # Gráfico de cumplimiento
    if 'cumplimiento' in resultados:
        graficos['cumplimiento'] = generar_grafico_cumplimiento(resultados['cumplimiento'])
    
    # Gráfico de estadísticas derivadas
    if 'estadisticas' in resultados:
        graficos['estadisticas'] = generar_grafico_estadisticas(resultados['estadisticas'])
    
    return graficos

def generar_grafico_configuracion(resultados):
    """Genera gráfico de configuración óptima."""
    # Crear figura
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    
    config = resultados['configuracion']
    
    # Valores normalizados para visualización uniforme
    valores = [
        config['capacidad_diaria'] / 50,  # Normalizado a máximo de 50
        config['eficiencia_operativa'],    # Ya está en rango 0-1
        config['cobertura_objetivo'],      # Ya está en rango 0-1
        config['costo_unitario'] / 120000  # Normalizado a máximo de 120k
    ]
    
    # Crear gráfico de barras
    categorias = ['Capacidad Diaria', 'Eficiencia\nOperativa', 
                  'Cobertura\nObjetivo', 'Costo\nUnitario']
    colores = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    
    bars = ax.bar(categorias, valores, color=colores)
    
    # Añadir etiquetas con valores originales
    etiquetas = [
        f"{config['capacidad_diaria']:.0f}",
        f"{config['eficiencia_operativa']*100:.1f}%",
        f"{config['cobertura_objetivo']*100:.1f}%",
        f"${config['costo_unitario']:,.0f}"
    ]
    
    for i, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
               etiquetas[i], ha='center', va='bottom', fontsize=11)
    
    # Configurar gráfico
    ax.set_title('Configuración Óptima UMS', fontsize=14)
    ax.set_ylim(0, 1.2)
    ax.set_ylabel('Valor Normalizado', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # Añadir descripción de normalización
    fig.text(0.5, 0.01, 
             "Valores normalizados para visualización. Rangos: Capacidad (0-50), Eficiencia (0-100%), Cobertura (0-100%), Costo (0-120k)", 
             ha='center', fontsize=8)
    
    return fig

def generar_grafico_cumplimiento(cumplimiento):
    """Genera gráfico de radar para el cumplimiento."""
    # Crear figura
    fig = Figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    
    # Obtener datos
    categorias = list(cumplimiento['por_categoria'].keys())
    valores = [cumplimiento['por_categoria'][cat] for cat in categorias]
    
    # Añadir el primer valor al final para cerrar el polígono
    valores.append(valores[0])
    
    # Crear categorías para el radar (añadir la primera al final)
    categorias = [cat.capitalize() for cat in categorias]
    categorias.append(categorias[0])
    
    # Calcular ángulos para cada categoría
    num_categorias = len(categorias) - 1  # Restar 1 porque duplicamos la primera
    angulos = np.linspace(0, 2*np.pi, num_categorias, endpoint=False).tolist()
    
    # Añadir el primer ángulo al final para cerrar el polígono
    angulos.append(angulos[0])
    
    # Crear gráfico radar
    ax.plot(angulos, valores, 'o-', linewidth=2, label='Cumplimiento')
    ax.fill(angulos, valores, alpha=0.25)
    
    # Configurar gráfico
    ax.set_thetagrids(np.degrees(angulos[:-1]), categorias[:-1])
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
    ax.grid(True)
    
    # Añadir título y cumplimiento global
    ax.set_title(f"Cumplimiento de Metas\nGlobal: {cumplimiento['global']*100:.1f}%", 
                 va='bottom', pad=20)
    
    return fig

def generar_grafico_estadisticas(estadisticas):
    """Genera gráfico de estadísticas derivadas."""
    # Crear figura
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    
    # Seleccionar indicadores clave
    indicadores = [
        'atenciones_mensuales',
        'poblacion_cubierta',
        'ums_requeridas_100k',
        'costo_total_mensual'
    ]
    
    etiquetas = {
        'atenciones_mensuales': 'Atenciones\nmensuales',
        'poblacion_cubierta': 'Población\ncubierta',
        'ums_requeridas_100k': 'UMS por\n100k hab.',
        'costo_total_mensual': 'Costo\nmensual'
    }
    
    # Valores y colores
    valores = []
    colores = ['#3498db', '#2ecc71', '#9b59b6', '#e74c3c']
    etiquetas_valores = []
    
    # Normalizar valores para visualización
    for i, ind in enumerate(indicadores):
        if ind in estadisticas:
            valor = estadisticas[ind]
            
            # Normalizar según tipo de indicador
            if ind == 'atenciones_mensuales':
                valores.append(min(valor / 1000, 1.0))  # Normalizar a 1000
                etiquetas_valores.append(f"{valor:.0f}")
            elif ind == 'poblacion_cubierta':
                valores.append(min(valor / 10000, 1.0))  # Normalizar a 10000
                etiquetas_valores.append(f"{valor:.0f}")
            elif ind == 'ums_requeridas_100k':
                valores.append(min(valor / 10, 1.0))  # Normalizar a 10
                etiquetas_valores.append(f"{valor:.2f}")
            elif ind == 'costo_total_mensual':
                valores.append(min(valor / 30000000, 1.0))  # Normalizar a 30M
                etiquetas_valores.append(f"${valor/1000000:.1f}M")
    
    # Crear gráfico de barras
    categorias = [etiquetas[ind] for ind in indicadores]
    bars = ax.bar(categorias, valores, color=colores)
    
    # Añadir etiquetas con valores originales
    for i, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
               etiquetas_valores[i], ha='center', va='bottom', fontsize=11)
    
    # Configurar gráfico
    ax.set_title('Estadísticas Derivadas', fontsize=14)
    ax.set_ylim(0, 1.2)
    ax.set_ylabel('Valor Normalizado', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # Añadir descripción de normalización
    fig.text(0.5, 0.01, 
             "Valores normalizados para visualización. Rangos: Atenciones (0-1000), Población (0-10000), UMS (0-10), Costo (0-30M)", 
             ha='center', fontsize=8)
    
    return fig

def generar_graficos_comparativos(modelo_practico, modelo_teorico):
    """
    Genera gráficos comparativos entre ambos modelos.
    
    Args:
        modelo_practico: Instancia del modelo práctico con resultados.
        modelo_teorico: Instancia del modelo teórico con resultados.
        
    Returns:
        dict: Diccionario de figuras generadas.
    """
    # Verificar que ambos modelos tengan resultados
    if (not hasattr(modelo_practico, 'resultados') or not modelo_practico.resultados or 
        not hasattr(modelo_teorico, 'resultados') or not modelo_teorico.resultados):
        return {}
    
    graficos = {}
    
    # Gráfico de barras comparativo
    graficos['barras_comparativo'] = generar_grafico_barras_comparativo(modelo_practico, modelo_teorico)
    
    # Gráfico radar comparativo
    graficos['radar_comparativo'] = generar_grafico_radar_comparativo(modelo_practico, modelo_teorico)
    
    return graficos

def generar_grafico_barras_comparativo(modelo_practico, modelo_teorico):
    """Genera gráfico de barras comparativo entre ambos modelos."""
    # Crear figura
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    
    # Obtener datos del modelo práctico
    if 'estadisticas' in modelo_practico.resultados:
        cobertura_real = modelo_practico.resultados['estadisticas']['cobertura']['media']
        eficiencia_real = modelo_practico.datos_operativos['capacidad']['eficiencia']
        
        # Calcular costo por atención
        costos_reales = modelo_practico.resultados['estadisticas']['costos']['media']
        demanda_real = modelo_practico.resultados['estadisticas']['demanda']['media']
        costo_atencion_real = costos_reales / max(1, demanda_real)
        
        # Sostenibilidad
        sostenibilidad_real = modelo_practico.resultados['estadisticas']['sostenibilidad']['media']
    else:
        return fig  # Retornar figura vacía si no hay datos
    
    # Obtener datos del modelo teórico
    if 'configuracion' in modelo_teorico.resultados:
        cobertura_ideal = modelo_teorico.resultados['configuracion']['cobertura_objetivo']
        eficiencia_ideal = modelo_teorico.resultados['configuracion']['eficiencia_operativa']
        costo_atencion_ideal = modelo_teorico.resultados['configuracion']['costo_unitario']
        sostenibilidad_ideal = modelo_teorico.metas_ideales['financiero']['sostenibilidad_min']
    else:
        return fig  # Retornar figura vacía si no hay datos
    
    # Normalizar costo atención para visualización
    costo_max = max(costo_atencion_real, costo_atencion_ideal)
    costo_atencion_real_norm = costo_atencion_real / costo_max
    costo_atencion_ideal_norm = costo_atencion_ideal / costo_max
    
    # Normalizar sostenibilidad para visualización
    sost_max = max(sostenibilidad_real, sostenibilidad_ideal, 1.0)  # Al menos 1.0
    sostenibilidad_real_norm = sostenibilidad_real / sost_max
    sostenibilidad_ideal_norm = sostenibilidad_ideal / sost_max
    
    # Datos para el gráfico
    categorias = ['Cobertura', 'Eficiencia', 'Costo Atención\n(normalizado)', 'Sostenibilidad\n(normalizada)']
    
    reales = [cobertura_real, eficiencia_real, costo_atencion_real_norm, sostenibilidad_real_norm]
    ideales = [cobertura_ideal, eficiencia_ideal, costo_atencion_ideal_norm, sostenibilidad_ideal_norm]
    
    # Crear barras agrupadas
    x = np.arange(len(categorias))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, reales, width, label='Real (Práctico)', color='#3498db')
    bars2 = ax.bar(x + width/2, ideales, width, label='Ideal (Teórico)', color='#e74c3c')
    
    # Añadir etiquetas con valores originales
    etiquetas_reales = [
        f"{cobertura_real*100:.1f}%",
        f"{eficiencia_real*100:.1f}%",
        f"${costo_atencion_real:,.0f}",
        f"{sostenibilidad_real:.2f}"
    ]
    
    etiquetas_ideales = [
        f"{cobertura_ideal*100:.1f}%",
        f"{eficiencia_ideal*100:.1f}%",
        f"${costo_atencion_ideal:,.0f}",
        f"{sostenibilidad_ideal:.2f}"
    ]
    
    for i, bar in enumerate(bars1):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
               etiquetas_reales[i], ha='center', va='bottom', fontsize=9)
    
    for i, bar in enumerate(bars2):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
               etiquetas_ideales[i], ha='center', va='bottom', fontsize=9)
    
    # Configurar gráfico
    ax.set_title('Comparación de Indicadores Clave', fontsize=14)
    ax.set_ylim(0, 1.3)
    ax.set_ylabel('Valor Normalizado', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categorias)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    return fig

def generar_grafico_radar_comparativo(modelo_practico, modelo_teorico):
    """Genera gráfico radar comparativo entre ambos modelos."""
    # Crear figura
    fig = Figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    
    # Obtener datos del modelo práctico
    if 'estadisticas' in modelo_practico.resultados:
        cobertura_real = modelo_practico.resultados['estadisticas']['cobertura']['media']
        eficiencia_real = modelo_practico.datos_operativos['capacidad']['eficiencia']
        
        # Normalizar costo (menos es mejor, así que invertimos)
        costos_reales = modelo_practico.resultados['estadisticas']['costos']['media']
        demanda_real = modelo_practico.resultados['estadisticas']['demanda']['media']
        costo_atencion_real = costos_reales / max(1, demanda_real)
        costo_normalizado = 1 - min(costo_atencion_real / 150000, 1)  # 150k como referencia
        
        # Sostenibilidad
        sostenibilidad_real = min(modelo_practico.resultados['estadisticas']['sostenibilidad']['media'], 2) / 2  # Max 2
    else:
        return fig  # Retornar figura vacía si no hay datos
    
    # Obtener datos del modelo teórico
    if 'configuracion' in modelo_teorico.resultados:
        cobertura_ideal = modelo_teorico.resultados['configuracion']['cobertura_objetivo']
        eficiencia_ideal = modelo_teorico.resultados['configuracion']['eficiencia_operativa']
        
        # Normalizar costo (menos es mejor, así que invertimos)
        costo_atencion_ideal = modelo_teorico.resultados['configuracion']['costo_unitario']
        costo_ideal_normalizado = 1 - min(costo_atencion_ideal / 150000, 1)  # 150k como referencia
        
        # Sostenibilidad
        sostenibilidad_ideal = min(modelo_teorico.metas_ideales['financiero']['sostenibilidad_min'], 2) / 2  # Max 2
    else:
        return fig  # Retornar figura vacía si no hay datos
    
    # Datos para el radar
    categorias = ['Cobertura', 'Eficiencia\nOperativa', 'Costo-Efectividad', 'Sostenibilidad']
    
    valores_reales = [cobertura_real, eficiencia_real, costo_normalizado, sostenibilidad_real]
    valores_ideales = [cobertura_ideal, eficiencia_ideal, costo_ideal_normalizado, sostenibilidad_ideal]
    
    # Añadir el primer valor al final para cerrar el polígono
    valores_reales.append(valores_reales[0])
    valores_ideales.append(valores_ideales[0])
    
    # Añadir la primera categoría al final
    categorias.append(categorias[0])
    
    # Calcular ángulos para cada categoría
    num_categorias = len(categorias) - 1  # Restar 1 porque duplicamos la primera
    angulos = np.linspace(0, 2*np.pi, num_categorias, endpoint=False).tolist()
    angulos.append(angulos[0])  # Añadir el primer ángulo al final
    
    # Crear gráfico radar
    ax.plot(angulos, valores_reales, 'o-', linewidth=2, color='#3498db', label='Real (Práctico)')
    ax.fill(angulos, valores_reales, alpha=0.1, color='#3498db')
    
    ax.plot(angulos, valores_ideales, 'o-', linewidth=2, color='#e74c3c', label='Ideal (Teórico)')
    ax.fill(angulos, valores_ideales, alpha=0.1, color='#e74c3c')
    
    # Configurar gráfico
    ax.set_thetagrids(np.degrees(angulos[:-1]), categorias[:-1])
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
    ax.grid(True)
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # Título
    ax.set_title("Comparación de Desempeño", va='bottom', pad=20)
    
    return fig