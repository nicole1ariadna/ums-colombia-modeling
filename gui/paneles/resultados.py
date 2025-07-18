"""
Panel para visualización de resultados de los modelos.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.visualizacion import generar_graficos_practico, generar_graficos_teorico

class PanelResultados:
    def __init__(self, parent):
        """
        Inicializa el panel de resultados.
        
        Args:
            parent: Widget padre (notebook).
        """
        # Crear frame principal
        self.frame = ttk.Frame(parent, padding="10")
        
        # Mensaje inicial
        self.lbl_sin_resultados = ttk.Label(
            self.frame,
            text="No hay resultados disponibles. Ejecute un modelo para ver los resultados.",
            font=("Arial", 12)
        )
        self.lbl_sin_resultados.pack(pady=20)
        
        # Notebook para pestañas de resultados
        self.notebook = ttk.Notebook(self.frame)
        
        # Pestaña para modelo práctico
        self.tab_practico = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.tab_practico, text="Modelo Práctico")
        
        # Pestaña para modelo teórico
        self.tab_teorico = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.tab_teorico, text="Modelo Teórico")
        
        # Inicialmente el notebook está oculto
        # Se mostrará cuando haya resultados
        
        # Canvas para gráficos
        self.canvas_practico = None
        self.canvas_teorico = None
    
    def actualizar_resultados_practico(self, modelo_practico):
        """
        Actualiza la visualización con los resultados del modelo práctico.
        
        Args:
            modelo_practico: Instancia del modelo práctico con resultados.
        """
        # Ocultar mensaje de no resultados
        self.lbl_sin_resultados.pack_forget()
        
        # Mostrar notebook de resultados
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Limpiar pestaña de modelo práctico
        for widget in self.tab_practico.winfo_children():
            widget.destroy()
        
        # Crear un notebook dentro de la pestaña para organizar los resultados
        tab_notebook = ttk.Notebook(self.tab_practico)
        tab_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de gráficos
        tab_graficos = ttk.Frame(tab_notebook, padding="10")
        tab_notebook.add(tab_graficos, text="Gráficos")
        
        # Pestaña de estadísticas
        tab_estadisticas = ttk.Frame(tab_notebook, padding="10")
        tab_notebook.add(tab_estadisticas, text="Estadísticas")
        
        # Generar gráficos
        try:
            graficos = generar_graficos_practico(modelo_practico.resultados)
            
            # Si hay gráficos, crear notebook para organizarlos
            if graficos:
                graficos_notebook = ttk.Notebook(tab_graficos)
                graficos_notebook.pack(fill=tk.BOTH, expand=True)
                
                for nombre, figura in graficos.items():
                    # Crear pestaña para cada gráfico
                    tab_figura = ttk.Frame(graficos_notebook)
                    graficos_notebook.add(tab_figura, text=nombre.replace('_', ' ').title())
                    
                    # Mostrar gráfico
                    canvas = FigureCanvasTkAgg(figura, master=tab_figura)
                    canvas_widget = canvas.get_tk_widget()
                    canvas_widget.pack(fill=tk.BOTH, expand=True)
            else:
                ttk.Label(
                    tab_graficos,
                    text="No se pudieron generar gráficos con los resultados actuales.",
                    font=("Arial", 10)
                ).pack(pady=20)
        except Exception as e:
            ttk.Label(
                tab_graficos,
                text=f"Error al generar gráficos: {str(e)}",
                font=("Arial", 10)
            ).pack(pady=20)
        
        # Mostrar estadísticas
        if hasattr(modelo_practico, 'resultados') and 'estadisticas' in modelo_practico.resultados:
            stats = modelo_practico.resultados['estadisticas']
            
            # Frame para estadísticas generales
            frame_stats = ttk.LabelFrame(tab_estadisticas, text="Estadísticas Generales", padding="10")
            frame_stats.pack(fill=tk.X, pady=10)
            
            # Crear tabla de estadísticas
            stats_tree = ttk.Treeview(frame_stats, columns=('Indicador', 'Media', 'Mediana', 'Desviación', 'Min', 'Max'), show='headings', height=4)
            stats_tree.heading('Indicador', text='Indicador')
            stats_tree.heading('Media', text='Media')
            stats_tree.heading('Mediana', text='Mediana')
            stats_tree.heading('Desviación', text='Desv. Est.')
            stats_tree.heading('Min', text='Mínimo')
            stats_tree.heading('Max', text='Máximo')
            
            # Ajustar anchos de columna
            stats_tree.column('Indicador', width=100)
            stats_tree.column('Media', width=100)
            stats_tree.column('Mediana', width=100)
            stats_tree.column('Desviación', width=100)
            stats_tree.column('Min', width=100)
            stats_tree.column('Max', width=100)
            
            # Añadir datos de estadísticas
            for indicador, valores in stats.items():
                if isinstance(valores, dict) and 'media' in valores:
                    # Formatear valores según el indicador
                    if indicador == 'costos':
                        media = f"${valores['media']:,.0f}"
                        mediana = f"${valores['mediana']:,.0f}"
                        desv = f"${valores['desviacion']:,.0f}"
                        minimo = f"${valores['min']:,.0f}"
                        maximo = f"${valores['max']:,.0f}"
                    elif indicador in ['cobertura']:
                        media = f"{valores['media']*100:.1f}%"
                        mediana = f"{valores['mediana']*100:.1f}%"
                        desv = f"{valores['desviacion']*100:.2f}%"
                        minimo = f"{valores['min']*100:.1f}%"
                        maximo = f"{valores['max']*100:.1f}%"
                    else:
                        media = f"{valores['media']:.2f}"
                        mediana = f"{valores['mediana']:.2f}"
                        desv = f"{valores['desviacion']:.2f}"
                        minimo = f"{valores['min']:.2f}"
                        maximo = f"{valores['max']:.2f}"
                    
                    stats_tree.insert('', tk.END, values=(indicador.title(), media, mediana, desv, minimo, maximo))
            
            stats_tree.pack(fill=tk.BOTH, expand=True)
            
            # Frame para detalles de costos
            frame_costos = ttk.LabelFrame(tab_estadisticas, text="Detalles de Costos", padding="10")
            frame_costos.pack(fill=tk.X, pady=10)
            
            # Mostrar detalles de costos si están disponibles
            costos = modelo_practico.calcular_costos()
            
            costos_tree = ttk.Treeview(frame_costos, columns=('Concepto', 'Valor'), show='headings', height=6)
            costos_tree.heading('Concepto', text='Concepto')
            costos_tree.heading('Valor', text='Valor (COP)')
            
            # Ajustar anchos de columna
            costos_tree.column('Concepto', width=200)
            costos_tree.column('Valor', width=200)
            
            # Añadir datos de costos
            for concepto, valor in costos.items():
                # Formatear valores como moneda
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
                
                costos_tree.insert('', tk.END, values=(concepto_texto, valor_formato))
            
            costos_tree.pack(fill=tk.BOTH, expand=True)
        else:
            ttk.Label(
                tab_estadisticas,
                text="No hay estadísticas disponibles.",
                font=("Arial", 10)
            ).pack(pady=20)
    
    def actualizar_resultados_teorico(self, modelo_teorico):
        """
        Actualiza la visualización con los resultados del modelo teórico.
        
        Args:
            modelo_teorico: Instancia del modelo teórico con resultados.
        """
        # Ocultar mensaje de no resultados
        self.lbl_sin_resultados.pack_forget()
        
        # Mostrar notebook de resultados
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Limpiar pestaña de modelo teórico
        for widget in self.tab_teorico.winfo_children():
            widget.destroy()
        
        # Crear un notebook dentro de la pestaña para organizar los resultados
        tab_notebook = ttk.Notebook(self.tab_teorico)
        tab_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de configuración óptima
        tab_config = ttk.Frame(tab_notebook, padding="10")
        tab_notebook.add(tab_config, text="Configuración Óptima")
        
        # Pestaña de gráficos
        tab_graficos = ttk.Frame(tab_notebook, padding="10")
        tab_notebook.add(tab_graficos, text="Gráficos")
        
        # Pestaña de cumplimiento
        tab_cumplimiento = ttk.Frame(tab_notebook, padding="10")
        tab_notebook.add(tab_cumplimiento, text="Cumplimiento")
        
        # Mostrar configuración óptima
        if hasattr(modelo_teorico, 'resultados') and 'configuracion' in modelo_teorico.resultados:
            config = modelo_teorico.resultados['configuracion']
            
            # Crear tabla de configuración
            config_tree = ttk.Treeview(tab_config, columns=('Parámetro', 'Valor'), show='headings', height=10)
            config_tree.heading('Parámetro', text='Parámetro')
            config_tree.heading('Valor', text='Valor')
            
            # Ajustar anchos de columna
            config_tree.column('Parámetro', width=200)
            config_tree.column('Valor', width=200)
            
            # Añadir datos de configuración
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
                
                config_tree.insert('', tk.END, values=(param_texto, valor_formato))
            
            config_tree.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Mostrar estadísticas derivadas si están disponibles
            if 'estadisticas' in modelo_teorico.resultados:
                stats = modelo_teorico.resultados['estadisticas']
                
                # Frame para estadísticas derivadas
                frame_stats = ttk.LabelFrame(tab_config, text="Estadísticas Derivadas", padding="10")
                frame_stats.pack(fill=tk.BOTH, expand=True, pady=10)
                
                # Crear tabla de estadísticas
                stats_tree = ttk.Treeview(frame_stats, columns=('Indicador', 'Valor'), show='headings', height=6)
                stats_tree.heading('Indicador', text='Indicador')
                stats_tree.heading('Valor', text='Valor')
                
                # Ajustar anchos de columna
                stats_tree.column('Indicador', width=200)
                stats_tree.column('Valor', width=200)
                
                # Añadir datos de estadísticas
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
                    
                    stats_tree.insert('', tk.END, values=(indicador_texto, valor_formato))
                
                stats_tree.pack(fill=tk.BOTH, expand=True)
        else:
            ttk.Label(
                tab_config,
                text="No hay configuración óptima disponible.",
                font=("Arial", 10)
            ).pack(pady=20)
        
        # Generar gráficos
        try:
            graficos = generar_graficos_teorico(modelo_teorico.resultados)
            
            # Si hay gráficos, crear notebook para organizarlos
            if graficos:
                graficos_notebook = ttk.Notebook(tab_graficos)
                graficos_notebook.pack(fill=tk.BOTH, expand=True)
                
                for nombre, figura in graficos.items():
                    # Crear pestaña para cada gráfico
                    tab_figura = ttk.Frame(graficos_notebook)
                    graficos_notebook.add(tab_figura, text=nombre.replace('_', ' ').title())
                    
                    # Mostrar gráfico
                    canvas = FigureCanvasTkAgg(figura, master=tab_figura)
                    canvas_widget = canvas.get_tk_widget()
                    canvas_widget.pack(fill=tk.BOTH, expand=True)
            else:
                ttk.Label(
                    tab_graficos,
                    text="No se pudieron generar gráficos con los resultados actuales.",
                    font=("Arial", 10)
                ).pack(pady=20)
        except Exception as e:
            ttk.Label(
                tab_graficos,
                text=f"Error al generar gráficos: {str(e)}",
                font=("Arial", 10)
            ).pack(pady=20)
        
        # Mostrar cumplimiento
        if (hasattr(modelo_teorico, 'resultados') and 
            'cumplimiento' in modelo_teorico.resultados):
            cumplimiento = modelo_teorico.resultados['cumplimiento']
            
            # Frame para cumplimiento global
            frame_global = ttk.Frame(tab_cumplimiento, padding="10")
            frame_global.pack(fill=tk.X, pady=10)
            
            # Mostrar cumplimiento global
            global_pct = cumplimiento['global'] * 100
            ttk.Label(
                frame_global,
                text=f"Cumplimiento Global: {global_pct:.1f}%",
                font=("Arial", 16, "bold")
            ).pack(pady=10)
            
            # Barra de progreso para visualizar cumplimiento global
            pb_global = ttk.Progressbar(frame_global, orient=tk.HORIZONTAL, length=300, mode='determinate')
            pb_global['value'] = global_pct
            pb_global.pack(pady=5)
            
            # Frame para cumplimiento por categoría
            frame_categorias = ttk.LabelFrame(tab_cumplimiento, text="Cumplimiento por Categoría", padding="10")
            frame_categorias.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Crear tabla de cumplimiento
            cumpl_tree = ttk.Treeview(frame_categorias, columns=('Categoría', 'Cumplimiento'), show='headings', height=6)
            cumpl_tree.heading('Categoría', text='Categoría')
            cumpl_tree.heading('Cumplimiento', text='Cumplimiento')
            
            # Ajustar anchos de columna
            cumpl_tree.column('Categoría', width=200)
            cumpl_tree.column('Cumplimiento', width=200)
            
            # Añadir datos de cumplimiento por categoría
            if 'por_categoria' in cumplimiento:
                for categoria, valor in cumplimiento['por_categoria'].items():
                    # Formatear valores como porcentaje
                    valor_formato = f"{valor*100:.1f}%"
                    
                    # Traducir categorías
                    if categoria == 'cobertura':
                        categoria_texto = 'Cobertura'
                    elif categoria == 'operacion':
                        categoria_texto = 'Operación'
                    elif categoria == 'financiero':
                        categoria_texto = 'Financiero'
                    elif categoria == 'calidad':
                        categoria_texto = 'Calidad'
                    else:
                        categoria_texto = categoria.replace('_', ' ').title()
                    
                    cumpl_tree.insert('', tk.END, values=(categoria_texto, valor_formato))
            
            cumpl_tree.pack(fill=tk.BOTH, expand=True)
            
            # Mostrar detalles si están disponibles
            if 'detallado' in cumplimiento:
                # Frame para detalles
                frame_detalles = ttk.LabelFrame(tab_cumplimiento, text="Detalles por Indicador", padding="10")
                frame_detalles.pack(fill=tk.BOTH, expand=True, pady=10)
                
                # Crear tabla de detalles
                detalles_tree = ttk.Treeview(
                    frame_detalles, 
                    columns=('Indicador', 'Valor Real', 'Meta', 'Cumplimiento'), 
                    show='headings', 
                    height=8
                )
                detalles_tree.heading('Indicador', text='Indicador')
                detalles_tree.heading('Valor Real', text='Valor Real')
                detalles_tree.heading('Meta', text='Meta')
                detalles_tree.heading('Cumplimiento', text='Cumplimiento')
                
                # Ajustar anchos de columna
                detalles_tree.column('Indicador', width=150)
                detalles_tree.column('Valor Real', width=100)
                detalles_tree.column('Meta', width=100)
                detalles_tree.column('Cumplimiento', width=100)
                
                # Añadir datos detallados
                for indicador, datos in cumplimiento['detallado'].items():
                    # Formatear valores según indicador
                    if 'costo' in indicador.lower():
                        valor_real = f"${datos['valor_real']:,.0f}"
                        meta = f"${datos['meta']:,.0f}"
                    elif 'porcentaje' in indicador.lower() or indicador.endswith('_pct'):
                        valor_real = f"{datos['valor_real']*100:.1f}%"
                        meta = f"{datos['meta']*100:.1f}%"
                    else:
                        valor_real = f"{datos['valor_real']}"
                        meta = f"{datos['meta']}"
                    
                    # Formatear cumplimiento como porcentaje
                    cumpl = f"{datos['cumplimiento']*100:.1f}%"
                    
                    # Traducir indicador
                    indicador_texto = indicador.replace('_', ' ').title()
                    
                    detalles_tree.insert('', tk.END, values=(indicador_texto, valor_real, meta, cumpl))
                
                detalles_tree.pack(fill=tk.BOTH, expand=True)
        else:
            ttk.Label(
                tab_cumplimiento,
                text="No hay datos de cumplimiento disponibles.",
                font=("Arial", 10)
            ).pack(pady=20)