"""
Panel para el análisis de brechas entre los modelos práctico y teórico.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from src.visualizacion import generar_graficos_comparativos

class PanelBrechas:
    def __init__(self, parent, analisis_brechas=None):
        """
        Inicializa el panel de análisis de brechas.
        
        Args:
            parent: Widget padre (notebook).
            analisis_brechas: Instancia de la clase AnalisisBrechas.
        """
        self.analisis_brechas = analisis_brechas
        
        # Crear frame principal
        self.frame = ttk.Frame(parent, padding="10")
        
        # Mensaje inicial si no hay análisis
        self.lbl_sin_analisis = ttk.Label(
            self.frame,
            text="No hay análisis disponible. Ejecute ambos modelos y compare los resultados.",
            font=("Arial", 12)
        )
        self.lbl_sin_analisis.pack(pady=20)
        
        # Crear frames para resultados (inicialmente ocultos)
        self.frame_matriz_brechas = ttk.LabelFrame(self.frame, text="Matriz de Brechas", padding="10")
        self.frame_graficos_comparativos = ttk.LabelFrame(self.frame, text="Gráficos Comparativos", padding="10")
        self.frame_recomendaciones = ttk.LabelFrame(self.frame, text="Recomendaciones Prioritarias", padding="10")
        
        # Canvas para gráficos
        self.canvas_comparativo = None
    
    def actualizar_analisis(self, analisis_brechas):
        """
        Actualiza la visualización con un nuevo análisis de brechas.
        
        Args:
            analisis_brechas: Instancia de la clase AnalisisBrechas.
        """
        self.analisis_brechas = analisis_brechas
        
        # Si no hay análisis, salir
        if not self.analisis_brechas:
            return
        
        # Ocultar mensaje de no análisis
        self.lbl_sin_analisis.pack_forget()
        
        # Comparar modelos si no se ha hecho antes
        if not self.analisis_brechas.matriz_brechas:
            self.analisis_brechas.comparar_modelos()
        
        # Verificar que se haya generado la matriz de brechas
        if not self.analisis_brechas.matriz_brechas:
            self.lbl_sin_analisis.configure(
                text="No se pudo generar la matriz de brechas. Verifique que ambos modelos tengan resultados válidos."
            )
            self.lbl_sin_analisis.pack(pady=20)
            return
        
        # Limpiar frames anteriores
        for widget in self.frame_matriz_brechas.winfo_children():
            widget.destroy()
        
        for widget in self.frame_graficos_comparativos.winfo_children():
            widget.destroy()
        
        for widget in self.frame_recomendaciones.winfo_children():
            widget.destroy()
        
        # Actualizar componentes
        self.mostrar_matriz_brechas()
        self.mostrar_graficos_comparativos()
        self.mostrar_recomendaciones()
    
    def mostrar_matriz_brechas(self):
        """Muestra la matriz de brechas en una tabla."""
        # Mostrar frame
        self.frame_matriz_brechas.pack(fill=tk.X, pady=10)
        
        # Crear tabla (Treeview)
        columns = ('Indicador', 'Valor Real', 'Valor Ideal', 'Brecha (%)', 'Prioridad')
        tree = ttk.Treeview(self.frame_matriz_brechas, columns=columns, show='headings', height=5)
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        
        # Añadir datos
        for indicador, datos in self.analisis_brechas.matriz_brechas.items():
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
            
            # Añadir fila con código de color según prioridad
            prioridad = datos['prioridad']
            item = tree.insert('', tk.END, values=(
                indicador.replace('_', ' ').title(),
                valor_real,
                valor_ideal,
                brecha_texto,
                prioridad
            ))
            
            # Aplicar color según prioridad
            if prioridad == 'Alta':
                tree.tag_configure('alta', background='#FFCCCC')  # Rojo claro
                tree.item(item, tags=('alta',))
            elif prioridad == 'Media':
                tree.tag_configure('media', background='#FFFFCC')  # Amarillo claro
                tree.item(item, tags=('media',))
            else:
                tree.tag_configure('baja', background='#CCFFCC')  # Verde claro
                tree.item(item, tags=('baja',))
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(self.frame_matriz_brechas, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Colocar elementos
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def mostrar_graficos_comparativos(self):
        """Muestra gráficos comparativos entre ambos modelos."""
        # Mostrar frame
        self.frame_graficos_comparativos.pack(fill=tk.BOTH, expand=True, pady=10)
        
        try:
            # Generar gráficos comparativos
            graficos = generar_graficos_comparativos(
                self.analisis_brechas.modelo_practico, 
                self.analisis_brechas.modelo_teorico
            )
            
            # Notebook para organizar los gráficos
            graficos_notebook = ttk.Notebook(self.frame_graficos_comparativos)
            graficos_notebook.pack(fill=tk.BOTH, expand=True)
            
            # Crear una pestaña para cada gráfico
            for nombre, figura in graficos.items():
                frame_grafico = ttk.Frame(graficos_notebook)
                graficos_notebook.add(frame_grafico, text=nombre.replace('_', ' ').title())
                
                canvas = FigureCanvasTkAgg(figura, master=frame_grafico)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            ttk.Label(
                self.frame_graficos_comparativos,
                text=f"Error al generar gráficos comparativos: {str(e)}",
                font=("Arial", 10)
            ).pack(pady=10)
    
    def mostrar_recomendaciones(self):
        """Muestra recomendaciones basadas en el análisis de brechas."""
        # Mostrar frame
        self.frame_recomendaciones.pack(fill=tk.X, pady=10)
        
        # Generar recomendaciones
        recomendaciones = self.analisis_brechas.generar_recomendaciones()
        
        if not recomendaciones:
            ttk.Label(
                self.frame_recomendaciones,
                text="No se encontraron brechas significativas que requieran recomendaciones.",
                font=("Arial", 10)
            ).pack(pady=10)
            return
        
        # Crear lista de recomendaciones
        for i, rec in enumerate(recomendaciones):
            # Frame para cada recomendación
            frame_rec = ttk.Frame(self.frame_recomendaciones, padding=5)
            frame_rec.pack(fill=tk.X, pady=5)
            
            # Número y prioridad
            prioridad = rec['prioridad']
            
            # Configurar color según prioridad
            if prioridad == 'Alta':
                color = 'red'
            elif prioridad == 'Media':
                color = 'orange'
            else:
                color = 'green'
            
            # Etiqueta de número y prioridad
            lbl_num = ttk.Label(
                frame_rec,
                text=f"{i+1}. [{prioridad}]",
                font=("Arial", 10, "bold"),
                foreground=color
            )
            lbl_num.grid(row=0, column=0, padx=(0, 10), sticky=tk.NW)
            
            # Etiqueta de indicador
            lbl_indicador = ttk.Label(
                frame_rec,
                text=f"{rec['indicador']}:",
                font=("Arial", 10, "bold")
            )
            lbl_indicador.grid(row=0, column=1, sticky=tk.NW)
            
            # Etiqueta de recomendación
            lbl_rec = ttk.Label(
                frame_rec,
                text=rec['recomendacion'],
                wraplength=500,
                justify=tk.LEFT
            )
            lbl_rec.grid(row=1, column=0, columnspan=2, padx=(20, 0), sticky=tk.W)
            
            # Separador
            if i < len(recomendaciones) - 1:
                ttk.Separator(self.frame_recomendaciones, orient='horizontal').pack(fill=tk.X, pady=5)