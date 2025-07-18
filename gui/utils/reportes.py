"""
Módulo para la generación de informes en formato PDF.
"""

import os
import datetime
from io import BytesIO

# Importar reportlab para la generación de PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Para convertir figuras de matplotlib a imágenes
import matplotlib.pyplot as plt
import numpy as np

def generar_informe_completo(modelo_practico, modelo_teorico, analisis_brechas, ruta_archivo):
    """
    Genera un informe completo en formato PDF.
    
    Args:
        modelo_practico: Instancia del modelo práctico.
        modelo_teorico: Instancia del modelo teórico.
        analisis_brechas: Instancia del análisis de brechas.
        ruta_archivo: Ruta donde guardar el archivo PDF.
    
    Returns:
        bool: True si se generó correctamente, False en caso contrario.
    """
    # Crear documento
    doc = SimpleDocTemplate(
        ruta_archivo,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Contenedor para los elementos del documento
    elementos = []
    
    # Estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos['Heading1']
    estilo_subtitulo = estilos['Heading2']
    estilo_subtitulo_pequeño = estilos['Heading3']
    estilo_normal = estilos['Normal']
    
    # Crear estilo personalizado para texto centrado
    estilo_centrado = ParagraphStyle(
        'Centrado',
        parent=estilos['Normal'],
        alignment=1  # 0=Izq, 1=Centro, 2=Der
    )
    
    # Título del informe
    elementos.append(Paragraph("Informe de Análisis de Unidades Móviles de Salud", estilo_titulo))
    elementos.append(Spacer(1, 0.25*inch))
    
    # Fecha de generación
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elementos.append(Paragraph(f"Generado el: {fecha_hora}", estilo_centrado))
    elementos.append(Spacer(1, 0.5*inch))
    
    # ===== 1. Resumen Ejecutivo =====
    elementos.append(Paragraph("1. Resumen Ejecutivo", estilo_subtitulo))
    elementos.append(Spacer(1, 0.1*inch))
    
    # Texto de resumen
    texto_resumen = """
    Este informe presenta un análisis comparativo entre el modelo práctico (basado en datos operativos reales)
    y el modelo teórico (basado en metas normativas) para Unidades Móviles de Salud (UMS).
    El análisis de brechas identifica las diferencias clave y proporciona recomendaciones
    para mejorar la efectividad y eficiencia de las UMS en contextos rurales.
    """
    elementos.append(Paragraph(texto_resumen, estilo_normal))
    elementos.append(Spacer(1, 0.2*inch))
    
    # Añadir tabla de indicadores clave
    elementos.append(Paragraph("Indicadores Clave", estilo_subtitulo_pequeño))
    
    # Crear datos para tabla de indicadores clave
    if (hasattr(modelo_practico, 'resultados') and modelo_practico.resultados and 
        hasattr(modelo_teorico, 'resultados') and modelo_teorico.resultados):
        
        # Extraer datos para la tabla
        try:
            # Modelo Práctico
            cobertura_real = modelo_practico.resultados['estadisticas']['cobertura']['media']
            eficiencia_real = modelo_practico.datos_operativos['capacidad']['eficiencia']
            
            # Calcular costo por atención
            costos_reales = modelo_practico.resultados['estadisticas']['costos']['media']
            demanda_real = modelo_practico.resultados['estadisticas']['demanda']['media']
            costo_atencion_real = costos_reales / max(1, demanda_real)
            
            # Sostenibilidad
            sostenibilidad_real = modelo_practico.resultados['estadisticas']['sostenibilidad']['media']
            
            # Modelo Teórico
            cobertura_ideal = modelo_teorico.resultados['configuracion']['cobertura_objetivo']
            eficiencia_ideal = modelo_teorico.resultados['configuracion']['eficiencia_operativa']
            costo_atencion_ideal = modelo_teorico.resultados['configuracion']['costo_unitario']
            sostenibilidad_ideal = modelo_teorico.metas_ideales['financiero']['sostenibilidad_min']
            
            # Crear datos para la tabla
            datos_tabla = [
                ['Indicador', 'Modelo Práctico', 'Modelo Teórico', 'Brecha (%)'],
                ['Cobertura', f"{cobertura_real*100:.1f}%", f"{cobertura_ideal*100:.1f}%", 
                 f"{((cobertura_real-cobertura_ideal)/cobertura_ideal)*100:.1f}%"],
                ['Eficiencia Operativa', f"{eficiencia_real*100:.1f}%", f"{eficiencia_ideal*100:.1f}%", 
                 f"{((eficiencia_real-eficiencia_ideal)/eficiencia_ideal)*100:.1f}%"],
                ['Costo por Atención', f"${costo_atencion_real:,.0f}", f"${costo_atencion_ideal:,.0f}", 
                 f"{((costo_atencion_real-costo_atencion_ideal)/costo_atencion_ideal)*100:.1f}%"],
                ['Sostenibilidad', f"{sostenibilidad_real:.2f}", f"{sostenibilidad_ideal:.2f}", 
                 f"{((sostenibilidad_real-sostenibilidad_ideal)/sostenibilidad_ideal)*100:.1f}%"]
            ]
            
            # Crear tabla
            tabla = Table(datos_tabla, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            
            # Estilo de tabla
            estilo_tabla = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey)
            ]
            
            tabla.setStyle(TableStyle(estilo_tabla))
            elementos.append(tabla)
            
        except Exception as e:
            elementos.append(Paragraph(f"Error al generar tabla de indicadores: {str(e)}", estilo_normal))
    
    elementos.append(Spacer(1, 0.5*inch))
    
    # ===== 2. Resultados del Modelo Práctico =====
    elementos.append(Paragraph("2. Resultados del Modelo Práctico", estilo_subtitulo))
    elementos.append(Spacer(1, 0.1*inch))
    
    # Descripción del modelo práctico
    texto_modelo_practico = """
    El modelo práctico simula la operación de las UMS basándose en datos operativos reales,
    incluyendo capacidad, costos, personal y distribución de servicios. Los resultados
    muestran el desempeño esperado en condiciones reales de operación.
    """
    elementos.append(Paragraph(texto_modelo_practico, estilo_normal))
    elementos.append(Spacer(1, 0.2*inch))
    
    # 2.1. Estadísticas del Modelo Práctico
    elementos.append(Paragraph("2.1. Estadísticas", estilo_subtitulo_pequeño))
    
    # Crear tabla de estadísticas del modelo práctico
    if hasattr(modelo_practico, 'resultados') and 'estadisticas' in modelo_practico.resultados:
        try:
            stats = modelo_practico.resultados['estadisticas']
            
            # Datos para la tabla de estadísticas
            datos_stats = [['Indicador', 'Media', 'Mediana', 'Desv. Est.', 'Mínimo', 'Máximo']]
            
            # Añadir filas para cada indicador
            for indicador, valores in stats.items():
                if isinstance(valores, dict) and 'media' in valores:
                    # Formatear valores según el indicador
                    if indicador == 'costos':
                        fila = [
                            indicador.title(),
                            f"${valores['media']:,.0f}",
                            f"${valores['mediana']:,.0f}",
                            f"${valores['desviacion']:,.0f}",
                            f"${valores['min']:,.0f}",
                            f"${valores['max']:,.0f}"
                        ]
                    elif indicador in ['cobertura']:
                        fila = [
                            indicador.title(),
                            f"{valores['media']*100:.1f}%",
                            f"{valores['mediana']*100:.1f}%",
                            f"{valores['desviacion']*100:.2f}%",
                            f"{valores['min']*100:.1f}%",
                            f"{valores['max']*100:.1f}%"
                        ]
                    else:
                        fila = [
                            indicador.title(),
                            f"{valores['media']:.2f}",
                            f"{valores['mediana']:.2f}",
                            f"{valores['desviacion']:.2f}",
                            f"{valores['min']:.2f}",
                            f"{valores['max']:.2f}"
                        ]
                    
                    datos_stats.append(fila)
            
            # Crear tabla
            tabla_stats = Table(datos_stats, colWidths=[1.2*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            
            # Estilo de tabla
            estilo_tabla = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey)
            ]
            
            tabla_stats.setStyle(TableStyle(estilo_tabla))
            elementos.append(tabla_stats)
            
        except Exception as e:
            elementos.append(Paragraph(f"Error al generar tabla de estadísticas: {str(e)}", estilo_normal))
    else:
        elementos.append(Paragraph("No hay estadísticas disponibles para el modelo práctico.", estilo_normal))
    
    elementos.append(Spacer(1, 0.3*inch))
    
    # 2.2. Detalles de Costos del Modelo Práctico
    elementos.append(Paragraph("2.2. Detalles de Costos", estilo_subtitulo_pequeño))
    
    # Crear tabla de costos
    if hasattr(modelo_practico, 'calcular_costos'):
        try:
            costos = modelo_practico.calcular_costos()
            
            # Datos para la tabla de costos
            datos_costos = [['Concepto', 'Valor (COP)']]
            
            # Añadir filas para cada concepto
            for concepto, valor in costos.items():
                # Formatear valor como moneda
                valor_formato = f"${valor:,.0f}"
                
                # Traducir conceptos
                if concepto == 'fijos':
                    concepto_texto = 'Costos Fijos'
                elif concepto == 'variables':
                    concepto_texto = 'Costos Variables'
                elif concepto == 'personal':
                    concepto_texto = 'Costos de Personal'
                elif concepto == 'depreciacion':
                    concepto_texto = 'Depreciación'
                elif concepto == 'mantenimiento':
                    concepto_texto = 'Mantenimiento'
                elif concepto == 'total_mensual':
                    concepto_texto = 'Total Mensual'
                elif concepto == 'costo_por_atencion':
                    concepto_texto = 'Costo por Atención'
                else:
                    concepto_texto = concepto.replace('_', ' ').title()
                
                datos_costos.append([concepto_texto, valor_formato])
            
            # Crear tabla
            tabla_costos = Table(datos_costos, colWidths=[3*inch, 3*inch])
            
            # Estilo de tabla
            estilo_tabla = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey)
            ]
            
            tabla_costos.setStyle(TableStyle(estilo_tabla))
            elementos.append(tabla_costos)
            
        except Exception as e:
            elementos.append(Paragraph(f"Error al generar tabla de costos: {str(e)}", estilo_normal))
    else:
        elementos.append(Paragraph("No hay información de costos disponible.", estilo_normal))
    
    elementos.append(Spacer(1, 0.3*inch))
    
    # 2.3. Gráficos del Modelo Práctico
    elementos.append(Paragraph("2.3. Gráficos", estilo_subtitulo_pequeño))
    
    # Añadir gráficos del modelo práctico si están disponibles
    if hasattr(modelo_practico, 'resultados') and modelo_practico.resultados:
        try:
            # Convertir figuras de matplotlib a imágenes para el PDF
            from src.visualizacion import generar_graficos_practico
            
            graficos = generar_graficos_practico(modelo_practico.resultados)
            
            for nombre, figura in graficos.items():
                # Convertir figura a imagen PNG en memoria
                img_buffer = BytesIO()
                figura.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                img_buffer.seek(0)
                
                # Crear imagen para el PDF
                img = Image(img_buffer, width=6*inch, height=4*inch)
                elementos.append(img)
                elementos.append(Spacer(1, 0.1*inch))
                elementos.append(Paragraph(f"Gráfico: {nombre.replace('_', ' ').title()}", estilo_centrado))
                elementos.append(Spacer(1, 0.3*inch))
                
        except Exception as e:
            elementos.append(Paragraph(f"Error al generar gráficos: {str(e)}", estilo_normal))
    else:
        elementos.append(Paragraph("No hay gráficos disponibles para el modelo práctico.", estilo_normal))
    
    elementos.append(Spacer(1, 0.5*inch))
    
    # ===== 3. Resultados del Modelo Teórico =====
    elementos.append(Paragraph("3. Resultados del Modelo Teórico", estilo_subtitulo))
    elementos.append(Spacer(1, 0.1*inch))
    
    # Descripción del modelo teórico
    texto_modelo_teorico = """
    El modelo teórico optimiza la configuración de las UMS basándose en metas normativas ideales,
    con el objetivo de maximizar la cobertura y calidad del servicio mientras se minimiza el costo.
    Los resultados representan el desempeño ideal al que deberían aspirar las UMS.
    """
    elementos.append(Paragraph(texto_modelo_teorico, estilo_normal))
    elementos.append(Spacer(1, 0.2*inch))
    
    # 3.1. Configuración Óptima
    elementos.append(Paragraph("3.1. Configuración Óptima", estilo_subtitulo_pequeño))
    
    # Crear tabla de configuración óptima
    if hasattr(modelo_teorico, 'resultados') and 'configuracion' in modelo_teorico.resultados:
        try:
            config = modelo_teorico.resultados['configuracion']
            
            # Datos para la tabla de configuración
            datos_config = [['Parámetro', 'Valor']]
            
            # Añadir filas para cada parámetro
            for param, valor in config.items():
                # Formatear valores según el parámetro
                if param == 'capacidad_diaria':
                    valor_formato = f"{valor:.1f} pacientes/día"
                elif param == 'eficiencia_operativa':
                    valor_formato = f"{valor*100:.1f}%"
                elif param == 'cobertura_objetivo':
                    valor_formato = f"{valor*100:.1f}%"
                elif param == 'costo_unitario':
                    valor_formato = f"${valor:,.0f}"
                else:
                    valor_formato = str(valor)
                
                # Traducir parámetros
                if param == 'capacidad_diaria':
                    param_texto = 'Capacidad Diaria'
                elif param == 'eficiencia_operativa':
                    param_texto = 'Eficiencia Operativa'
                elif param == 'cobertura_objetivo':
                    param_texto = 'Cobertura Objetivo'
                elif param == 'costo_unitario':
                    param_texto = 'Costo Unitario'
                else:
                    param_texto = param.replace('_', ' ').title()
                
                datos_config.append([param_texto, valor_formato])
            
            # Crear tabla
            tabla_config = Table(datos_config, colWidths=[3*inch, 3*inch])
            
            # Estilo de tabla
            estilo_tabla = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey)
            ]
            
            tabla_config.setStyle(TableStyle(estilo_tabla))
            elementos.append(tabla_config)
            
        except Exception as e:
            elementos.append(Paragraph(f"Error al generar tabla de configuración: {str(e)}", estilo_normal))
    else:
        elementos.append(Paragraph("No hay configuración óptima disponible.", estilo_normal))
    
    elementos.append(Spacer(1, 0.3*inch))
    
    # 3.2. Estadísticas Derivadas
    elementos.append(Paragraph("3.2. Estadísticas Derivadas", estilo_subtitulo_pequeño))
    
    # Crear tabla de estadísticas derivadas
    if (hasattr(modelo_teorico, 'resultados') and 
        'estadisticas' in modelo_teorico.resultados):
        try:
            stats = modelo_teorico.resultados['estadisticas']
            
            # Datos para la tabla de estadísticas
            datos_stats = [['Indicador', 'Valor']]
            
            # Añadir filas para cada indicador
            for indicador, valor in stats.items():
                # Formatear valores según el indicador
                if indicador == 'atenciones_mensuales':
                    valor_formato = f"{valor:.0f} atenciones"
                elif indicador == 'poblacion_cubierta':
                    valor_formato = f"{valor:.0f} habitantes"
                elif indicador == 'ums_requeridas_100k':
                    valor_formato = f"{valor:.2f} UMS"
                elif indicador == 'costo_total_mensual':
                    valor_formato = f"${valor:,.0f}"
                elif indicador == 'costo_por_habitante_mes':
                    valor_formato = f"${valor:,.0f}"
                else:
                    valor_formato = str(valor)
                
                # Traducir indicadores
                if indicador == 'atenciones_mensuales':
                    indicador_texto = 'Atenciones Mensuales'
                elif indicador == 'poblacion_cubierta':
                    indicador_texto = 'Población Cubierta'
                elif indicador == 'ums_requeridas_100k':
                    indicador_texto = 'UMS por 100,000 Habitantes'
                elif indicador == 'costo_total_mensual':
                    indicador_texto = 'Costo Total Mensual'
                elif indicador == 'costo_por_habitante_mes':
                    indicador_texto = 'Costo por Habitante (Mes)'
                else:
                    indicador_texto = indicador.replace('_', ' ').title()
                
                datos_stats.append([indicador_texto, valor_formato])
            
            # Crear tabla
            tabla_stats = Table(datos_stats, colWidths=[3*inch, 3*inch])
            
            # Estilo de tabla
            estilo_tabla = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey)
            ]
            
            tabla_stats.setStyle(TableStyle(estilo_tabla))
            elementos.append(tabla_stats)
            
        except Exception as e:
            elementos.append(Paragraph(f"Error al generar tabla de estadísticas: {str(e)}", estilo_normal))
    else:
        elementos.append(Paragraph("No hay estadísticas disponibles.", estilo_normal))
    
    elementos.append(Spacer(1, 0.3*inch))
    
    # 3.3. Gráficos del Modelo Teórico
    elementos.append(Paragraph("3.3. Gráficos", estilo_subtitulo_pequeño))
    
    # Añadir gráficos del modelo teórico si están disponibles
    if hasattr(modelo_teorico, 'resultados') and modelo_teorico.resultados:
        try:
            # Convertir figuras de matplotlib a imágenes para el PDF
            from src.visualizacion import generar_graficos_teorico
            
            graficos = generar_graficos_teorico(modelo_teorico.resultados)
            
            for nombre, figura in graficos.items():
                # Convertir figura a imagen PNG en memoria
                img_buffer = BytesIO()
                figura.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                img_buffer.seek(0)
                
                # Crear imagen para el PDF
                img = Image(img_buffer, width=6*inch, height=4*inch)
                elementos.append(img)
                elementos.append(Spacer(1, 0.1*inch))
                elementos.append(Paragraph(f"Gráfico: {nombre.replace('_', ' ').title()}", estilo_centrado))
                elementos.append(Spacer(1, 0.3*inch))
                
        except Exception as e:
            elementos.append(Paragraph(f"Error al generar gráficos: {str(e)}", estilo_normal))
    else:
        elementos.append(Paragraph("No hay gráficos disponibles para el modelo teórico.", estilo_normal))
    
    elementos.append(Spacer(1, 0.5*inch))
    
    # ===== 4. Análisis de Brechas =====
    elementos.append(Paragraph("4. Análisis de Brechas", estilo_subtitulo))
    elementos.append(Spacer(1, 0.1*inch))
    
    # Descripción del análisis de brechas
    texto_brechas = """
    El análisis de brechas compara los resultados del modelo práctico con los del modelo teórico,
    identificando las diferencias entre la operación real y la ideal. Estas brechas permiten
    priorizar áreas de mejora y establecer metas realistas para optimizar el desempeño de las UMS.
    """
    elementos.append(Paragraph(texto_brechas, estilo_normal))
    elementos.append(Spacer(1, 0.2*inch))
    
    # 4.1. Matriz de Brechas (modificación dentro de la función generar_informe_completo)
    elementos.append(Paragraph("4.1. Matriz de Brechas", estilo_subtitulo_pequeño))

    # Crear tabla de matriz de brechas
    if hasattr(analisis_brechas, 'matriz_brechas') and analisis_brechas.matriz_brechas:
        try:
            # Datos para la tabla de brechas
            datos_brechas = [['Indicador', 'Valor Real', 'Valor Ideal', 'Brecha (%)', 'Prioridad']]
            
            # Añadir filas para cada indicador
            for indicador, datos in analisis_brechas.matriz_brechas.items():
                # Formatear valores según tipo de indicador
                if indicador == 'costo_efectividad':
                    valor_real = f"${datos['real']:,.0f}"
                    valor_ideal = f"${datos['ideal']:,.0f}"
                else:
                    valor_real = f"{datos['real']*100:.1f}%"
                    valor_ideal = f"{datos['ideal']*100:.1f}%"
                
                # Formatear brecha como porcentaje
                brecha = datos['brecha'] * 100
                brecha_texto = f"{brecha:.1f}%"
                
                # Traducir indicadores
                if indicador == 'costo_efectividad':
                    indicador_texto = 'Costo-Efectividad'
                else:
                    indicador_texto = indicador.title()
                
                datos_brechas.append([
                    indicador_texto,
                    valor_real,
                    valor_ideal,
                    brecha_texto,
                    datos['prioridad']
                ])
            
            # Crear tabla
            tabla_brechas = Table(datos_brechas, colWidths=[1.5*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1*inch])
            
            # Estilo de tabla
            estilo_tabla = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey)
            ]
            
            # Aplicar colores más intensos según prioridad
            for i in range(1, len(datos_brechas)):
                prioridad = datos_brechas[i][-1]
                if prioridad == 'Alta':
                    # Color más intenso para prioridad alta (rojo claro más fuerte)
                    estilo_tabla.append(('BACKGROUND', (-1, i), (-1, i), colors.HexColor('#FF9999')))
                    # Aplicar el color a toda la fila para mayor visibilidad
                    estilo_tabla.append(('BACKGROUND', (1, i), (3, i), colors.HexColor('#FFDDDD')))
                elif prioridad == 'Media':
                    # Color para prioridad media (amarillo)
                    estilo_tabla.append(('BACKGROUND', (-1, i), (-1, i), colors.HexColor('#FFFF99')))
                    # Aplicar un tono más suave a toda la fila
                    estilo_tabla.append(('BACKGROUND', (1, i), (3, i), colors.HexColor('#FFFFDD')))
                elif prioridad == 'Baja':
                    # Color para prioridad baja (verde claro)
                    estilo_tabla.append(('BACKGROUND', (-1, i), (-1, i), colors.HexColor('#99FF99')))
                    # Aplicar un tono más suave a toda la fila
                    estilo_tabla.append(('BACKGROUND', (1, i), (3, i), colors.HexColor('#DDFFDD')))
            
            tabla_brechas.setStyle(TableStyle(estilo_tabla))
            elementos.append(tabla_brechas)
            
        except Exception as e:
            elementos.append(Paragraph(f"Error al generar matriz de brechas: {str(e)}", estilo_normal))
    else:
        elementos.append(Paragraph("No hay matriz de brechas disponible.", estilo_normal))

    # 4.2. Gráficos Comparativos
    elementos.append(Paragraph("4.2. Gráficos Comparativos", estilo_subtitulo_pequeño))
    
    # Añadir gráficos comparativos si están disponibles
    try:
        # Convertir figuras de matplotlib a imágenes para el PDF
        from src.visualizacion import generar_graficos_comparativos
        
        graficos = generar_graficos_comparativos(modelo_practico, modelo_teorico)
        
        for nombre, figura in graficos.items():
            # Convertir figura a imagen PNG en memoria
            img_buffer = BytesIO()
            figura.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            
            # Crear imagen para el PDF
            img = Image(img_buffer, width=6*inch, height=4*inch)
            elementos.append(img)
            elementos.append(Spacer(1, 0.1*inch))
            elementos.append(Paragraph(f"Gráfico: {nombre.replace('_', ' ').title()}", estilo_centrado))
            elementos.append(Spacer(1, 0.3*inch))
            
    except Exception as e:
        elementos.append(Paragraph(f"Error al generar gráficos comparativos: {str(e)}", estilo_normal))
    
    elementos.append(Spacer(1, 0.3*inch))
    
    # 4.3. Recomendaciones
    elementos.append(Paragraph("4.3. Recomendaciones", estilo_subtitulo_pequeño))
    
    # Añadir recomendaciones generadas por el análisis de brechas
    if hasattr(analisis_brechas, 'generar_recomendaciones'):
        try:
            recomendaciones = analisis_brechas.generar_recomendaciones()
            
            if recomendaciones:
                for i, rec in enumerate(recomendaciones):
                    prioridad = rec['prioridad']
                    
                    # Configurar color según prioridad
                    if prioridad == 'Alta':
                        color_prioridad = colors.red
                    elif prioridad == 'Media':
                        color_prioridad = colors.orange
                    else:
                        color_prioridad = colors.green
                    
                    # Estilo para texto de prioridad
                    estilo_prioridad = ParagraphStyle(
                        f'prioridad_{prioridad}',
                        parent=estilo_subtitulo_pequeño,
                        textColor=color_prioridad
                    )
                    
                    # Añadir recomendación
                    elementos.append(Paragraph(
                        f"{i+1}. {rec['indicador']} - Prioridad: {prioridad}",
                        estilo_prioridad
                    ))
                    elementos.append(Spacer(1, 0.05*inch))
                    elementos.append(Paragraph(rec['recomendacion'], estilo_normal))
                    elementos.append(Spacer(1, 0.2*inch))
            else:
                elementos.append(Paragraph(
                    "No se encontraron brechas significativas que requieran recomendaciones.",
                    estilo_normal
                ))
        except Exception as e:
            elementos.append(Paragraph(f"Error al generar recomendaciones: {str(e)}", estilo_normal))
    else:
        elementos.append(Paragraph("No hay recomendaciones disponibles.", estilo_normal))
    
    elementos.append(Spacer(1, 0.5*inch))
    
    # ===== 5. Conclusiones =====
    elementos.append(Paragraph("5. Conclusiones", estilo_subtitulo))
    elementos.append(Spacer(1, 0.1*inch))
    
    # Texto de conclusiones
    texto_conclusiones = """
    El análisis comparativo entre el modelo práctico y teórico proporciona insights valiosos
    para optimizar la operación de las Unidades Móviles de Salud. Las brechas identificadas
    representan oportunidades de mejora que, al ser abordadas con las recomendaciones propuestas,
    pueden incrementar significativamente la efectividad y eficiencia del servicio.
    
    La implementación de UMS con las configuraciones óptimas sugeridas por el modelo teórico,
    adaptadas a las limitaciones prácticas identificadas, permitiría mejorar la cobertura de
    servicios de salud en zonas rurales mientras se mantiene la sostenibilidad financiera del sistema.
    """
    elementos.append(Paragraph(texto_conclusiones, estilo_normal))
    
    # Construir el PDF
    try:
        doc.build(elementos)
        return True
    except Exception as e:
        print(f"Error al generar PDF: {str(e)}")
        return False