"""
Panel de configuración para los modelos de UMS.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Añadir importación faltante de los modelos
from src.modelo_practico import UMSPractico
from src.modelo_teorico import UMSTeorico


class PanelConfiguracion:
    def __init__(self, parent, modelo_practico, modelo_teorico):
        """
        Inicializa el panel de configuración.
        
        Args:
            parent: Widget padre (notebook).
            modelo_practico: Instancia del modelo práctico.
            modelo_teorico: Instancia del modelo teórico.
        """
        self.modelo_practico = modelo_practico
        self.modelo_teorico = modelo_teorico
        
        # Crear frame principal
        self.frame = ttk.Frame(parent, padding="10")
        
        # Crear notebook para separar configuración de modelos
        self.config_notebook = ttk.Notebook(self.frame)
        self.config_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crear pestañas para cada modelo
        self.frame_practico = ttk.Frame(self.config_notebook, padding="10")
        self.frame_teorico = ttk.Frame(self.config_notebook, padding="10")
        
        self.config_notebook.add(self.frame_practico, text="Modelo Práctico")
        self.config_notebook.add(self.frame_teorico, text="Modelo Teórico")
        
        # Inicializar componentes
        self.inicializar_config_practico()
        self.inicializar_config_teorico()
        
        # Botones de acción
        frame_botones = ttk.Frame(self.frame)
        frame_botones.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            frame_botones, 
            text="Ejecutar Modelo Práctico", 
            command=self.ejecutar_modelo_practico
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            frame_botones, 
            text="Ejecutar Modelo Teórico", 
            command=self.ejecutar_modelo_teorico
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            frame_botones, 
            text="Comparar Modelos", 
            command=self.comparar_modelos
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            frame_botones, 
            text="Restaurar Valores Predeterminados", 
            command=self.restaurar_predeterminados
        ).pack(side=tk.RIGHT, padx=5)
    
    def inicializar_config_practico(self):
        """Inicializa los componentes de configuración del modelo práctico."""
        # Crear canvas con scrollbar para manejar muchos parámetros
        canvas = tk.Canvas(self.frame_practico)
        scrollbar = ttk.Scrollbar(self.frame_practico, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Secciones de configuración
        self.crear_seccion_capacidad(scrollable_frame)
        self.crear_seccion_costos(scrollable_frame)
        self.crear_seccion_personal(scrollable_frame)
        self.crear_seccion_servicios(scrollable_frame)
        self.crear_seccion_cobertura(scrollable_frame)
        self.crear_seccion_simulacion(scrollable_frame)
    
    def crear_seccion_capacidad(self, parent):
        """Crea la sección de configuración de capacidad."""
        frame = ttk.LabelFrame(parent, text="Capacidad", padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        # Variables para sliders y campos de entrada
        self.var_pacientes_dia = tk.DoubleVar(value=self.modelo_practico.datos_operativos['capacidad']['pacientes_dia'])
        self.var_dias_mes = tk.IntVar(value=self.modelo_practico.datos_operativos['capacidad']['dias_mes'])
        self.var_eficiencia = tk.DoubleVar(value=self.modelo_practico.datos_operativos['capacidad']['eficiencia'])
        
        # Pacientes por día
        ttk.Label(frame, text="Pacientes por día:").grid(row=0, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=10, to=50, 
            variable=self.var_pacientes_dia,
            command=lambda v: self.var_pacientes_dia.set(round(float(v)))
        )
        slider.grid(row=0, column=1, sticky=tk.EW)
        
        entry = ttk.Entry(frame, width=5, textvariable=self.var_pacientes_dia)
        entry.grid(row=0, column=2, padx=5)
        
        # Días operativos por mes
        ttk.Label(frame, text="Días operativos al mes:").grid(row=1, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=15, to=26, 
            variable=self.var_dias_mes,
            command=lambda v: self.var_dias_mes.set(round(float(v)))
        )
        slider.grid(row=1, column=1, sticky=tk.EW)
        
        entry = ttk.Entry(frame, width=5, textvariable=self.var_dias_mes)
        entry.grid(row=1, column=2, padx=5)
        
        # Eficiencia operativa
        ttk.Label(frame, text="Eficiencia operativa:").grid(row=2, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.1, to=0.9, 
            variable=self.var_eficiencia,
            command=lambda v: self.var_eficiencia.set(round(float(v), 2))
        )
        slider.grid(row=2, column=1, sticky=tk.EW)
        
        entry = ttk.Entry(frame, width=5, textvariable=self.var_eficiencia)
        entry.grid(row=2, column=2, padx=5)
        
        # Configurar columnas
        frame.columnconfigure(1, weight=1)
    
    def crear_seccion_costos(self, parent):
        """Crea la sección de configuración de costos."""
        frame = ttk.LabelFrame(parent, text="Costos", padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        # Variables para campos de entrada
        self.var_fijo_mensual = tk.IntVar(value=self.modelo_practico.datos_operativos['costos']['fijo_mensual'])
        self.var_variable_paciente = tk.IntVar(value=self.modelo_practico.datos_operativos['costos']['variable_paciente'])
        self.var_mantenimiento_anual = tk.IntVar(value=self.modelo_practico.datos_operativos['costos']['mantenimiento_anual'])
        self.var_costo_unitario_atencion = tk.IntVar(value=self.modelo_practico.datos_operativos['costos']['costo_unitario_atencion'])
        self.var_costo_vehiculo = tk.IntVar(value=self.modelo_practico.datos_operativos['costos']['costo_vehiculo'])
        
        # Costo fijo mensual
        ttk.Label(frame, text="Costo fijo mensual (COP):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame, width=15, textvariable=self.var_fijo_mensual).grid(row=0, column=1, padx=5)
        
        # Costo variable por paciente
        ttk.Label(frame, text="Costo variable por paciente (COP):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(frame, width=15, textvariable=self.var_variable_paciente).grid(row=1, column=1, padx=5)
        
        # Costo de mantenimiento anual
        ttk.Label(frame, text="Mantenimiento anual (COP):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(frame, width=15, textvariable=self.var_mantenimiento_anual).grid(row=2, column=1, padx=5)
        
        # Costo unitario por atención
        ttk.Label(frame, text="Costo unitario atención (COP):").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(frame, width=15, textvariable=self.var_costo_unitario_atencion).grid(row=3, column=1, padx=5)
        
        # Costo del vehículo
        ttk.Label(frame, text="Costo del vehículo (COP):").grid(row=4, column=0, sticky=tk.W)
        ttk.Entry(frame, width=15, textvariable=self.var_costo_vehiculo).grid(row=4, column=1, padx=5)
        
        # Configurar columnas
        frame.columnconfigure(1, weight=1)
    
    def crear_seccion_personal(self, parent):
        """Crea la sección de configuración de personal."""
        frame = ttk.LabelFrame(parent, text="Personal", padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        # Variables para campos de entrada
        self.var_medico = tk.IntVar(value=self.modelo_practico.datos_operativos['personal']['medico'])
        self.var_enfermera = tk.IntVar(value=self.modelo_practico.datos_operativos['personal']['enfermera'])
        self.var_conductor = tk.IntVar(value=self.modelo_practico.datos_operativos['personal']['conductor'])
        self.var_costo_personal = tk.IntVar(value=self.modelo_practico.datos_operativos['personal']['costo_personal_mes'])
        
        # Cantidad de médicos
        ttk.Label(frame, text="Médicos:").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(frame, from_=0, to=3, width=5, textvariable=self.var_medico).grid(row=0, column=1, padx=5)
        
        # Cantidad de enfermeras
        ttk.Label(frame, text="Enfermeras:").grid(row=1, column=0, sticky=tk.W)
        ttk.Spinbox(frame, from_=0, to=3, width=5, textvariable=self.var_enfermera).grid(row=1, column=1, padx=5)
        
        # Cantidad de conductores
        ttk.Label(frame, text="Conductores/Logística:").grid(row=2, column=0, sticky=tk.W)
        ttk.Spinbox(frame, from_=0, to=3, width=5, textvariable=self.var_conductor).grid(row=2, column=1, padx=5)
        
        # Costo total de personal
        ttk.Label(frame, text="Costo personal mensual (COP):").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(frame, width=15, textvariable=self.var_costo_personal).grid(row=3, column=1, padx=5)
        
        # Configurar columnas
        frame.columnconfigure(1, weight=1)
    
    def crear_seccion_servicios(self, parent):
        """Crea la sección de configuración de servicios."""
        frame = ttk.LabelFrame(parent, text="Distribución de Servicios", padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        # Variables para sliders
        self.var_consulta_general = tk.DoubleVar(value=self.modelo_practico.datos_operativos['servicios']['consulta_general'])
        self.var_vacunacion = tk.DoubleVar(value=self.modelo_practico.datos_operativos['servicios']['vacunacion'])
        self.var_control_prenatal = tk.DoubleVar(value=self.modelo_practico.datos_operativos['servicios']['control_prenatal'])
        
        # Consulta general
        ttk.Label(frame, text="Consulta general (%):").grid(row=0, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0, to=1, 
            variable=self.var_consulta_general,
            command=lambda v: self.actualizar_distribucion_servicios('consulta_general', float(v))
        )
        slider.grid(row=0, column=1, sticky=tk.EW)
        
        self.lbl_consulta_general = ttk.Label(frame, text=f"{self.var_consulta_general.get()*100:.1f}%")
        self.lbl_consulta_general.grid(row=0, column=2, padx=5)
        
        # Vacunación
        ttk.Label(frame, text="Vacunación (%):").grid(row=1, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0, to=1, 
            variable=self.var_vacunacion,
            command=lambda v: self.actualizar_distribucion_servicios('vacunacion', float(v))
        )
        slider.grid(row=1, column=1, sticky=tk.EW)
        
        self.lbl_vacunacion = ttk.Label(frame, text=f"{self.var_vacunacion.get()*100:.1f}%")
        self.lbl_vacunacion.grid(row=1, column=2, padx=5)
        
        # Control prenatal
        ttk.Label(frame, text="Control prenatal (%):").grid(row=2, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0, to=1, 
            variable=self.var_control_prenatal,
            command=lambda v: self.actualizar_distribucion_servicios('control_prenatal', float(v))
        )
        slider.grid(row=2, column=1, sticky=tk.EW)
        
        self.lbl_control_prenatal = ttk.Label(frame, text=f"{self.var_control_prenatal.get()*100:.1f}%")
        self.lbl_control_prenatal.grid(row=2, column=2, padx=5)
        
        # Total
        ttk.Label(frame, text="Total:").grid(row=3, column=0, sticky=tk.W)
        self.lbl_total_servicios = ttk.Label(frame, text="100%")
        self.lbl_total_servicios.grid(row=3, column=2, padx=5)
        
        # Configurar columnas
        frame.columnconfigure(1, weight=1)
    
    def actualizar_distribucion_servicios(self, servicio_modificado, valor):
        """
        Actualiza la distribución de servicios manteniendo el total en 100%.
        
        Args:
            servicio_modificado: Nombre del servicio que se está modificando.
            valor: Nuevo valor para ese servicio.
        """
        # Redondear valor
        valor = round(valor, 2)
        
        # Obtener valores actuales
        consulta_general = self.var_consulta_general.get()
        vacunacion = self.var_vacunacion.get()
        control_prenatal = self.var_control_prenatal.get()
        
        # Actualizar el valor modificado
        if servicio_modificado == 'consulta_general':
            consulta_general = valor
        elif servicio_modificado == 'vacunacion':
            vacunacion = valor
        elif servicio_modificado == 'control_prenatal':
            control_prenatal = valor
        
        # Calcular total
        total = consulta_general + vacunacion + control_prenatal
        
        # Si el total es diferente de 1, ajustar proporcionalmente los otros valores
        if total != 1 and total > 0:
            factor = 1 / total
            
            # Ajustar valores sin modificar el que el usuario está cambiando
            if servicio_modificado != 'consulta_general':
                consulta_general = round(consulta_general * factor, 2)
                self.var_consulta_general.set(consulta_general)
            
            if servicio_modificado != 'vacunacion':
                vacunacion = round(vacunacion * factor, 2)
                self.var_vacunacion.set(vacunacion)
            
            if servicio_modificado != 'control_prenatal':
                control_prenatal = round(control_prenatal * factor, 2)
                self.var_control_prenatal.set(control_prenatal)
        
        # Actualizar labels
        self.lbl_consulta_general.config(text=f"{consulta_general*100:.1f}%")
        self.lbl_vacunacion.config(text=f"{vacunacion*100:.1f}%")
        self.lbl_control_prenatal.config(text=f"{control_prenatal*100:.1f}%")
        
        # Recalcular total
        total = consulta_general + vacunacion + control_prenatal
        self.lbl_total_servicios.config(text=f"{total*100:.1f}%")
    
    def crear_seccion_cobertura(self, parent):
        """Crea la sección de configuración de cobertura."""
        frame = ttk.LabelFrame(parent, text="Cobertura", padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        # Variables para campos de entrada
        self.var_poblacion_objetivo = tk.IntVar(value=self.modelo_practico.datos_operativos['cobertura']['poblacion_objetivo'])
        self.var_frecuencia_visitas = tk.IntVar(value=self.modelo_practico.datos_operativos['cobertura']['frecuencia_visitas'])
        self.var_radio_cobertura = tk.IntVar(value=self.modelo_practico.datos_operativos['cobertura']['radio_cobertura'])
        self.var_poblacion_km2 = tk.DoubleVar(value=self.modelo_practico.datos_operativos['cobertura']['poblacion_por_km2'])
        
        # Población objetivo
        ttk.Label(frame, text="Población objetivo:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame, width=10, textvariable=self.var_poblacion_objetivo).grid(row=0, column=1, padx=5)
        
        # Frecuencia de visitas
        ttk.Label(frame, text="Frecuencia de visitas (por mes):").grid(row=1, column=0, sticky=tk.W)
        ttk.Spinbox(frame, from_=1, to=4, width=5, textvariable=self.var_frecuencia_visitas).grid(row=1, column=1, padx=5)
        
        # Radio de cobertura
        ttk.Label(frame, text="Radio de cobertura (km):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(frame, width=10, textvariable=self.var_radio_cobertura).grid(row=2, column=1, padx=5)
        
        # Densidad poblacional
        ttk.Label(frame, text="Densidad poblacional (hab/km²):").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(frame, width=10, textvariable=self.var_poblacion_km2).grid(row=3, column=1, padx=5)
        
        # Configurar columnas
        frame.columnconfigure(1, weight=1)
    
    def crear_seccion_simulacion(self, parent):
        """Crea la sección de configuración de simulación."""
        frame = ttk.LabelFrame(parent, text="Parámetros de Simulación", padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        # Variables para campos de entrada
        self.var_num_simulaciones = tk.IntVar(value=self.modelo_practico.parametros_simulacion['num_simulaciones'])
        self.var_horizonte_temporal = tk.IntVar(value=self.modelo_practico.parametros_simulacion['horizonte_temporal'])
        
        # Número de simulaciones
        ttk.Label(frame, text="Número de simulaciones:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame, width=10, textvariable=self.var_num_simulaciones).grid(row=0, column=1, padx=5)
        
        # Horizonte temporal
        ttk.Label(frame, text="Horizonte temporal (meses):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(frame, width=10, textvariable=self.var_horizonte_temporal).grid(row=1, column=1, padx=5)
        
        # Configurar columnas
        frame.columnconfigure(1, weight=1)
    
    def inicializar_config_teorico(self):
        """Configura el formulario para el modelo teórico."""
        # Primero identificamos el frame correcto para el modelo teórico
        # Intenta acceder a self.frame_teorico
        try:
            contenedor_teorico = self.frame_teorico
            print("Usando self.frame_teorico como contenedor")
        except AttributeError:
            # Si no existe, intenta con self.tab_teorico
            try:
                contenedor_teorico = self.tab_teorico
                print("Usando self.tab_teorico como contenedor")
            except AttributeError:
                # Si tampoco existe, busca cualquier atributo que podría ser el contenedor
                import re
                teorico_attr = None
                for attr in dir(self):
                    if re.search(r'(teorico|teorica|teori)', attr.lower()):
                        teorico_attr = attr
                        break
                
                if teorico_attr:
                    contenedor_teorico = getattr(self, teorico_attr)
                    print(f"Usando self.{teorico_attr} como contenedor")
                else:
                    # Si todo falla, usamos self.tab_config como último recurso
                    contenedor_teorico = self.tab_config
                    print("No se encontró un contenedor específico, usando self.tab_config")
        
        # Frame para metas ideales
        frame_metas = ttk.LabelFrame(contenedor_teorico, text="Metas Ideales", padding="10")
        frame_metas.pack(fill=tk.X, pady=5)
        
        # Frame para restricciones
        frame_restricciones = ttk.LabelFrame(contenedor_teorico, text="Restricciones", padding="10")
        frame_restricciones.pack(fill=tk.X, pady=5)
        
        # Frame para optimización (NUEVO)
        frame_optimizacion = ttk.LabelFrame(contenedor_teorico, text="Optimización", padding="10")
        frame_optimizacion.pack(fill=tk.X, pady=5)
        
        # Metas ideales
        # Cobertura
        self.cobertura_objetivo_var = tk.StringVar(value=str(self.modelo_teorico.metas_ideales['cobertura']['poblacion_objetivo']))
        
        ttk.Label(frame_metas, text="Cobertura objetivo (0-1):").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Entry(frame_metas, textvariable=self.cobertura_objetivo_var, width=10).grid(row=0, column=1, sticky="w", pady=2)
        
        # Operación
        self.capacidad_diaria_var = tk.StringVar(value=str(self.modelo_teorico.metas_ideales['operacion']['capacidad_optima']))
        self.eficiencia_operativa_var = tk.StringVar(value=str(self.modelo_teorico.metas_ideales['operacion']['eficiencia_operativa']))
        
        ttk.Label(frame_metas, text="Capacidad diaria (20-50):").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(frame_metas, textvariable=self.capacidad_diaria_var, width=10).grid(row=1, column=1, sticky="w", pady=2)
        
        ttk.Label(frame_metas, text="Eficiencia operativa (0-1):").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Entry(frame_metas, textvariable=self.eficiencia_operativa_var, width=10).grid(row=2, column=1, sticky="w", pady=2)
        
        # Financiero
        self.costo_unitario_var = tk.StringVar(value=str(self.modelo_teorico.metas_ideales['financiero']['costo_unitario_max']))
        self.sostenibilidad_min_var = tk.StringVar(value=str(self.modelo_teorico.metas_ideales['financiero']['sostenibilidad_min']))
        
        ttk.Label(frame_metas, text="Costo unitario máximo (COP):").grid(row=3, column=0, sticky="w", pady=2)
        ttk.Entry(frame_metas, textvariable=self.costo_unitario_var, width=15).grid(row=3, column=1, sticky="w", pady=2)
        
        ttk.Label(frame_metas, text="Sostenibilidad mínima (0-1):").grid(row=4, column=0, sticky="w", pady=2)
        ttk.Entry(frame_metas, textvariable=self.sostenibilidad_min_var, width=10).grid(row=4, column=1, sticky="w", pady=2)
        
        # Restricciones
        self.cobertura_minima_var = tk.StringVar(value=str(self.modelo_teorico.restricciones[0]['valor']))
        self.sostenibilidad_minima_var = tk.StringVar(value=str(self.modelo_teorico.restricciones[1]['valor']))
        self.calidad_minima_var = tk.StringVar(value=str(self.modelo_teorico.restricciones[2]['valor']))
        
        ttk.Label(frame_restricciones, text="Cobertura mínima (0-1):").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Entry(frame_restricciones, textvariable=self.cobertura_minima_var, width=10).grid(row=0, column=1, sticky="w", pady=2)
        
        ttk.Label(frame_restricciones, text="Sostenibilidad mínima (0-1):").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(frame_restricciones, textvariable=self.sostenibilidad_minima_var, width=10).grid(row=1, column=1, sticky="w", pady=2)
        
        ttk.Label(frame_restricciones, text="Calidad mínima (0-1):").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Entry(frame_restricciones, textvariable=self.calidad_minima_var, width=10).grid(row=2, column=1, sticky="w", pady=2)
        
        # Modo de optimización (NUEVO)
        # Inicializar el atributo en el modelo si no existe
        if not hasattr(self.modelo_teorico, 'usar_optimizacion'):
            self.modelo_teorico.usar_optimizacion = True
        
        self.usar_optimizacion_var = tk.BooleanVar(value=self.modelo_teorico.usar_optimizacion)
        
        ttk.Checkbutton(frame_optimizacion, 
                    text="Usar algoritmo de optimización (desmarcar para usar valores configurados directamente)", 
                    variable=self.usar_optimizacion_var).grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
        
        # Explicación del modo directo
        ttk.Label(frame_optimizacion, 
                text="Cuando se desmarca esta opción, los valores configurados arriba se usarán directamente\n"
                    "sin ejecutar el algoritmo de optimización. Esto permite probar valores específicos.",
                wraplength=500, justify=tk.LEFT).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
    
    def crear_seccion_metas_cobertura(self, parent):
        """Crea la sección de metas de cobertura del modelo teórico."""
        frame = ttk.LabelFrame(parent, text="Metas de Cobertura", padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        # Variables para campos de entrada
        self.var_meta_poblacion_objetivo = tk.DoubleVar(value=self.modelo_teorico.metas_ideales['cobertura']['poblacion_objetivo'])
        self.var_meta_frecuencia_visitas = tk.IntVar(value=self.modelo_teorico.metas_ideales['cobertura']['frecuencia_visitas'])
        self.var_meta_tiempo_acceso = tk.IntVar(value=self.modelo_teorico.metas_ideales['cobertura']['tiempo_acceso_max'])
        self.var_meta_satisfaccion = tk.DoubleVar(value=self.modelo_teorico.metas_ideales['cobertura']['satisfaccion_min'])
        
        # Población objetivo
        ttk.Label(frame, text="Población objetivo (proporción):").grid(row=0, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.5, to=1.0, 
            variable=self.var_meta_poblacion_objetivo,
            command=lambda v: self.var_meta_poblacion_objetivo.set(round(float(v), 2))
        )
        slider.grid(row=0, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_meta_poblacion_objetivo).grid(row=0, column=2, padx=5)
        
        # Frecuencia de visitas
        ttk.Label(frame, text="Frecuencia de visitas (por mes):").grid(row=1, column=0, sticky=tk.W)
        ttk.Spinbox(frame, from_=1, to=4, width=5, textvariable=self.var_meta_frecuencia_visitas).grid(row=1, column=1, padx=5)
        
        # Tiempo máximo de acceso
        ttk.Label(frame, text="Tiempo máximo de acceso (minutos):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(frame, width=10, textvariable=self.var_meta_tiempo_acceso).grid(row=2, column=1, padx=5)
        
        # Satisfacción mínima
        ttk.Label(frame, text="Satisfacción mínima:").grid(row=3, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.7, to=1.0, 
            variable=self.var_meta_satisfaccion,
            command=lambda v: self.var_meta_satisfaccion.set(round(float(v), 2))
        )
        slider.grid(row=3, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_meta_satisfaccion).grid(row=3, column=2, padx=5)
        
        # Configurar columnas
        frame.columnconfigure(1, weight=1)
    
    def crear_seccion_metas_operacion(self, parent):
        """Crea la sección de metas de operación del modelo teórico."""
        frame = ttk.LabelFrame(parent, text="Metas de Operación", padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        # Variables para campos de entrada
        self.var_meta_capacidad_optima = tk.IntVar(value=self.modelo_teorico.metas_ideales['operacion']['capacidad_optima'])
        self.var_meta_eficiencia_operativa = tk.DoubleVar(value=self.modelo_teorico.metas_ideales['operacion']['eficiencia_operativa'])
        self.var_meta_resolucion_primer_nivel = tk.DoubleVar(value=self.modelo_teorico.metas_ideales['operacion']['resolucion_primer_nivel'])
        self.var_meta_tiempo_espera = tk.IntVar(value=self.modelo_teorico.metas_ideales['operacion']['tiempo_espera_max'])
        
        # Capacidad óptima
        ttk.Label(frame, text="Capacidad óptima (pacientes/día):").grid(row=0, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=20, to=60, 
            variable=self.var_meta_capacidad_optima,
            command=lambda v: self.var_meta_capacidad_optima.set(round(float(v)))
        )
        slider.grid(row=0, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_meta_capacidad_optima).grid(row=0, column=2, padx=5)
        
        # Eficiencia operativa
        ttk.Label(frame, text="Eficiencia operativa:").grid(row=1, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.5, to=0.95, 
            variable=self.var_meta_eficiencia_operativa,
            command=lambda v: self.var_meta_eficiencia_operativa.set(round(float(v), 2))
        )
        slider.grid(row=1, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_meta_eficiencia_operativa).grid(row=1, column=2, padx=5)
        
        # Resolución primer nivel
        ttk.Label(frame, text="Resolución en primer nivel:").grid(row=2, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.7, to=0.95, 
            variable=self.var_meta_resolucion_primer_nivel,
            command=lambda v: self.var_meta_resolucion_primer_nivel.set(round(float(v), 2))
        )
        slider.grid(row=2, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_meta_resolucion_primer_nivel).grid(row=2, column=2, padx=5)
        
        # Tiempo de espera máximo
        ttk.Label(frame, text="Tiempo de espera máximo (minutos):").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(frame, width=10, textvariable=self.var_meta_tiempo_espera).grid(row=3, column=1, padx=5)
        
        # Configurar columnas
        frame.columnconfigure(1, weight=1)
    
    def crear_seccion_metas_financiero(self, parent):
        """Crea la sección de metas financieras del modelo teórico."""
        frame = ttk.LabelFrame(parent, text="Metas Financieras", padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        # Variables para campos de entrada
        self.var_meta_costo_unitario = tk.IntVar(value=self.modelo_teorico.metas_ideales['financiero']['costo_unitario_max'])
        self.var_meta_sostenibilidad = tk.DoubleVar(value=self.modelo_teorico.metas_ideales['financiero']['sostenibilidad_min'])
        self.var_meta_autofinanciacion = tk.DoubleVar(value=self.modelo_teorico.metas_ideales['financiero']['autofinanciacion'])
        
        # Costo unitario máximo
        ttk.Label(frame, text="Costo unitario máximo (COP):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame, width=10, textvariable=self.var_meta_costo_unitario).grid(row=0, column=1, padx=5)
        
        # Sostenibilidad mínima
        ttk.Label(frame, text="Sostenibilidad mínima:").grid(row=1, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.4, to=1.0, 
            variable=self.var_meta_sostenibilidad,
            command=lambda v: self.var_meta_sostenibilidad.set(round(float(v), 2))
        )
        slider.grid(row=1, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_meta_sostenibilidad).grid(row=1, column=2, padx=5)
        
        # Autofinanciación
        ttk.Label(frame, text="Autofinanciación:").grid(row=2, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.4, to=1.0, 
            variable=self.var_meta_autofinanciacion,
            command=lambda v: self.var_meta_autofinanciacion.set(round(float(v), 2))
        )
        slider.grid(row=2, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_meta_autofinanciacion).grid(row=2, column=2, padx=5)
        
        # Configurar columnas
        frame.columnconfigure(1, weight=1)
    
    def crear_seccion_metas_calidad(self, parent):
        """Crea la sección de metas de calidad del modelo teórico."""
        frame = ttk.LabelFrame(parent, text="Metas de Calidad", padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        # Variables para campos de entrada
        self.var_meta_continuidad = tk.DoubleVar(value=self.modelo_teorico.metas_ideales['calidad']['continuidad_atencion'])
        self.var_meta_integracion = tk.DoubleVar(value=self.modelo_teorico.metas_ideales['calidad']['integracion_historia'])
        self.var_meta_referencia = tk.DoubleVar(value=self.modelo_teorico.metas_ideales['calidad']['referencia_efectiva'])
        
        # Continuidad de atención
        ttk.Label(frame, text="Continuidad de atención:").grid(row=0, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.6, to=1.0, 
            variable=self.var_meta_continuidad,
            command=lambda v: self.var_meta_continuidad.set(round(float(v), 2))
        )
        slider.grid(row=0, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_meta_continuidad).grid(row=0, column=2, padx=5)
        
        # Integración con historia clínica
        ttk.Label(frame, text="Integración con historia clínica:").grid(row=1, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.6, to=1.0, 
            variable=self.var_meta_integracion,
            command=lambda v: self.var_meta_integracion.set(round(float(v), 2))
        )
        slider.grid(row=1, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_meta_integracion).grid(row=1, column=2, padx=5)
        
        # Referencia efectiva
        ttk.Label(frame, text="Referencia efectiva:").grid(row=2, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.7, to=1.0, 
            variable=self.var_meta_referencia,
            command=lambda v: self.var_meta_referencia.set(round(float(v), 2))
        )
        slider.grid(row=2, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_meta_referencia).grid(row=2, column=2, padx=5)
        
        # Configurar columnas
        frame.columnconfigure(1, weight=1)
    
    def crear_seccion_restricciones(self, parent):
        """Crea la sección de restricciones del modelo teórico."""
        frame = ttk.LabelFrame(parent, text="Restricciones de Optimización", padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        # Variables para campos de entrada
        self.var_restriccion_cobertura = tk.DoubleVar(value=0.9)  # Valor predeterminado
        self.var_restriccion_calidad = tk.DoubleVar(value=0.85)   # Valor predeterminado
        self.var_restriccion_sostenibilidad = tk.DoubleVar(value=0.6)  # Valor predeterminado
        
        # Restricción de cobertura mínima
        ttk.Label(frame, text="Cobertura mínima:").grid(row=0, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.5, to=0.95, 
            variable=self.var_restriccion_cobertura,
            command=lambda v: self.var_restriccion_cobertura.set(round(float(v), 2))
        )
        slider.grid(row=0, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_restriccion_cobertura).grid(row=0, column=2, padx=5)
        
        # Restricción de calidad mínima
        ttk.Label(frame, text="Calidad mínima:").grid(row=1, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.7, to=0.95, 
            variable=self.var_restriccion_calidad,
            command=lambda v: self.var_restriccion_calidad.set(round(float(v), 2))
        )
        slider.grid(row=1, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_restriccion_calidad).grid(row=1, column=2, padx=5)
        
        # Restricción de sostenibilidad mínima
        ttk.Label(frame, text="Sostenibilidad mínima:").grid(row=2, column=0, sticky=tk.W)
        slider = ttk.Scale(
            frame, 
            from_=0.4, to=0.8, 
            variable=self.var_restriccion_sostenibilidad,
            command=lambda v: self.var_restriccion_sostenibilidad.set(round(float(v), 2))
        )
        slider.grid(row=2, column=1, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.var_restriccion_sostenibilidad).grid(row=2, column=2, padx=5)
        
        # Configurar columnas
        frame.columnconfigure(1, weight=1)
    
    def actualizar_modelo_practico(self):
        """Actualiza los datos del modelo práctico con los valores de la interfaz."""
        try:
            # Actualizar capacidad
            self.modelo_practico.datos_operativos['capacidad']['pacientes_dia'] = self.var_pacientes_dia.get()
            self.modelo_practico.datos_operativos['capacidad']['dias_mes'] = self.var_dias_mes.get()
            self.modelo_practico.datos_operativos['capacidad']['eficiencia'] = self.var_eficiencia.get()
            
            # Actualizar costos
            self.modelo_practico.datos_operativos['costos']['fijo_mensual'] = self.var_fijo_mensual.get()
            self.modelo_practico.datos_operativos['costos']['variable_paciente'] = self.var_variable_paciente.get()
            self.modelo_practico.datos_operativos['costos']['mantenimiento_anual'] = self.var_mantenimiento_anual.get()
            self.modelo_practico.datos_operativos['costos']['costo_unitario_atencion'] = self.var_costo_unitario_atencion.get()
            self.modelo_practico.datos_operativos['costos']['costo_vehiculo'] = self.var_costo_vehiculo.get()
            
            # Actualizar personal
            self.modelo_practico.datos_operativos['personal']['medico'] = self.var_medico.get()
            self.modelo_practico.datos_operativos['personal']['enfermera'] = self.var_enfermera.get()
            self.modelo_practico.datos_operativos['personal']['conductor'] = self.var_conductor.get()
            self.modelo_practico.datos_operativos['personal']['costo_personal_mes'] = self.var_costo_personal.get()
            
            # Actualizar servicios
            self.modelo_practico.datos_operativos['servicios']['consulta_general'] = self.var_consulta_general.get()
            self.modelo_practico.datos_operativos['servicios']['vacunacion'] = self.var_vacunacion.get()
            self.modelo_practico.datos_operativos['servicios']['control_prenatal'] = self.var_control_prenatal.get()
            
            # Actualizar cobertura
            self.modelo_practico.datos_operativos['cobertura']['poblacion_objetivo'] = self.var_poblacion_objetivo.get()
            self.modelo_practico.datos_operativos['cobertura']['frecuencia_visitas'] = self.var_frecuencia_visitas.get()
            self.modelo_practico.datos_operativos['cobertura']['radio_cobertura'] = self.var_radio_cobertura.get()
            self.modelo_practico.datos_operativos['cobertura']['poblacion_por_km2'] = self.var_poblacion_km2.get()
            
            # Actualizar parámetros de simulación
            self.modelo_practico.parametros_simulacion['num_simulaciones'] = self.var_num_simulaciones.get()
            self.modelo_practico.parametros_simulacion['horizonte_temporal'] = self.var_horizonte_temporal.get()
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar modelo práctico: {str(e)}")
            return False
    
    def actualizar_modelo_teorico(self):
        """Actualiza el modelo teórico con los valores de la interfaz."""
        try:
            # Verificar que el modelo teórico tenga el atributo configuracion_inicial
            if not hasattr(self.modelo_teorico, 'configuracion_inicial'):
                # Si no existe, lo creamos
                self.modelo_teorico.configuracion_inicial = {
                    'capacidad_diaria': 30,
                    'eficiencia_operativa': 0.7,
                    'cobertura_objetivo': 0.8,
                    'costo_unitario': 90000
                }
                print("Se ha creado el atributo configuracion_inicial en el modelo teórico")
            
            # Actualizar el modo de optimización
            if hasattr(self, 'usar_optimizacion_var'):
                self.modelo_teorico.usar_optimizacion = self.usar_optimizacion_var.get()
                print(f"Modo de optimización: {'Activado' if self.modelo_teorico.usar_optimizacion else 'Desactivado'}")
            
            # --- Cobertura ---
            try:
                cobertura_valor = float(self.cobertura_objetivo_var.get())
                self.modelo_teorico.metas_ideales['cobertura']['poblacion_objetivo'] = cobertura_valor
                self.modelo_teorico.configuracion_inicial['cobertura_objetivo'] = cobertura_valor
                print(f"Actualizado cobertura_objetivo: {cobertura_valor}")
            except (AttributeError, ValueError) as e:
                print(f"Error al actualizar cobertura_objetivo: {str(e)}")
            
            # --- Capacidad ---
            try:
                capacidad_valor = float(self.capacidad_diaria_var.get())
                self.modelo_teorico.metas_ideales['operacion']['capacidad_optima'] = capacidad_valor
                self.modelo_teorico.configuracion_inicial['capacidad_diaria'] = capacidad_valor
                print(f"Actualizada capacidad_diaria: {capacidad_valor}")
            except (AttributeError, ValueError) as e:
                print(f"Error al actualizar capacidad_diaria: {str(e)}")
            
            # --- Eficiencia ---
            try:
                eficiencia_valor = float(self.eficiencia_operativa_var.get())
                self.modelo_teorico.metas_ideales['operacion']['eficiencia_operativa'] = eficiencia_valor
                self.modelo_teorico.configuracion_inicial['eficiencia_operativa'] = eficiencia_valor
                print(f"Actualizada eficiencia_operativa: {eficiencia_valor}")
            except (AttributeError, ValueError) as e:
                print(f"Error al actualizar eficiencia_operativa: {str(e)}")
            
            # --- Costo Unitario ---
            try:
                costo_valor = float(self.costo_unitario_var.get())
                self.modelo_teorico.metas_ideales['financiero']['costo_unitario_max'] = costo_valor
                self.modelo_teorico.configuracion_inicial['costo_unitario'] = costo_valor
                print(f"Actualizado costo_unitario: {costo_valor}")
            except (AttributeError, ValueError) as e:
                print(f"Error al actualizar costo_unitario: {str(e)}")
            
            # --- Sostenibilidad Mínima ---
            try:
                sostenibilidad_valor = float(self.sostenibilidad_min_var.get())
                self.modelo_teorico.metas_ideales['financiero']['sostenibilidad_min'] = sostenibilidad_valor
                print(f"Actualizada sostenibilidad_min: {sostenibilidad_valor}")
            except (AttributeError, ValueError) as e:
                print(f"Error al actualizar sostenibilidad_min: {str(e)}")
            
            # --- Restricciones ---
            try:
                cobertura_min_valor = float(self.cobertura_minima_var.get())
                self.modelo_teorico.restricciones[0]['valor'] = cobertura_min_valor
                print(f"Actualizada restricción cobertura_minima: {cobertura_min_valor}")
            except (AttributeError, ValueError, IndexError) as e:
                print(f"Error al actualizar restricción cobertura_minima: {str(e)}")
                
            try:
                sostenibilidad_min_valor = float(self.sostenibilidad_minima_var.get())
                self.modelo_teorico.restricciones[1]['valor'] = sostenibilidad_min_valor
                print(f"Actualizada restricción sostenibilidad_minima: {sostenibilidad_min_valor}")
            except (AttributeError, ValueError, IndexError) as e:
                print(f"Error al actualizar restricción sostenibilidad_minima: {str(e)}")
                
            try:
                calidad_min_valor = float(self.calidad_minima_var.get())
                self.modelo_teorico.restricciones[2]['valor'] = calidad_min_valor
                print(f"Actualizada restricción calidad_minima: {calidad_min_valor}")
            except (AttributeError, ValueError, IndexError) as e:
                print(f"Error al actualizar restricción calidad_minima: {str(e)}")
            
            # Imprimir resumen de la configuración inicial actualizada
            print("\nConfiguración inicial actual:")
            for key, value in self.modelo_teorico.configuracion_inicial.items():
                print(f"  {key}: {value}")
            
            return True
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error general al actualizar modelo teórico: {str(e)}")
            return False
    
    def ejecutar_modelo_practico(self):
        """Ejecuta el modelo práctico desde este panel."""
        if self.actualizar_modelo_practico():
            try:
                # Obtener ventana principal
                ventana_principal = self.frame.master.master
                
                # Si es la clase InterfazPrincipal, llamar a su método
                if hasattr(ventana_principal, 'ejecutar_modelo_practico'):
                    ventana_principal.ejecutar_modelo_practico()
                else:
                    # Ejecutar directamente
                    self.modelo_practico.simular()
                    messagebox.showinfo("Modelo Práctico", "Simulación completada con éxito.")
                
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Error al ejecutar el modelo práctico: {str(e)}")
                return False
        return False
    
    def ejecutar_modelo_teorico(self):
        """Ejecuta el modelo teórico desde este panel."""
        if self.actualizar_modelo_teorico():
            try:
                # Obtener ventana principal
                ventana_principal = self.frame.master.master
                
                # Si es la clase InterfazPrincipal, llamar a su método
                if hasattr(ventana_principal, 'ejecutar_modelo_teorico'):
                    ventana_principal.ejecutar_modelo_teorico()
                else:
                    # Ejecutar directamente
                    self.modelo_teorico.optimizar()
                    messagebox.showinfo("Modelo Teórico", "Optimización completada con éxito.")
                
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Error al ejecutar el modelo teórico: {str(e)}")
                return False
        return False
    
    def comparar_modelos(self):
        """Compara los resultados de ambos modelos."""
        # Obtener ventana principal
        ventana_principal = self.frame.master.master
        
        # Si es la clase InterfazPrincipal, llamar a su método
        if hasattr(ventana_principal, 'comparar_modelos'):
            ventana_principal.comparar_modelos()
        else:
            messagebox.showinfo("Comparación", "Esta funcionalidad requiere la interfaz principal.")
    
    def restaurar_predeterminados(self):
        """Restaura los valores predeterminados en ambos modelos."""
        # Crear instancias nuevas de los modelos con valores predeterminados
        modelo_practico_nuevo = UMSPractico()
        modelo_teorico_nuevo = UMSTeorico()
        
        # Actualizar referencias a los modelos
        self.modelo_practico.datos_operativos = modelo_practico_nuevo.datos_operativos
        self.modelo_practico.parametros_simulacion = modelo_practico_nuevo.parametros_simulacion
        
        self.modelo_teorico.metas_ideales = modelo_teorico_nuevo.metas_ideales
        self.modelo_teorico.restricciones = modelo_teorico_nuevo.restricciones
        
        # Reinicializar la interfaz
        self.config_notebook.destroy()
        self.config_notebook = ttk.Notebook(self.frame)
        self.config_notebook.pack(fill=tk.BOTH, expand=True)
        
        self.frame_practico = ttk.Frame(self.config_notebook, padding="10")
        self.frame_teorico = ttk.Frame(self.config_notebook, padding="10")
        
        self.config_notebook.add(self.frame_practico, text="Modelo Práctico")
        self.config_notebook.add(self.frame_teorico, text="Modelo Teórico")
        
        # Inicializar componentes nuevamente
        self.inicializar_config_practico()
        self.inicializar_config_teorico()
        
        messagebox.showinfo("Restaurar", "Se han restaurado los valores predeterminados.")
    
    def cargar_desde_archivo(self, archivo):
        """Carga la configuración desde un archivo JSON."""
        try:
            with open(archivo, 'r') as f:
                config = json.load(f)
            
            if 'modelo_practico' in config:
                self.modelo_practico.datos_operativos = config['modelo_practico']['datos_operativos']
                self.modelo_practico.parametros_simulacion = config['modelo_practico']['parametros_simulacion']
            
            if 'modelo_teorico' in config:
                self.modelo_teorico.metas_ideales = config['modelo_teorico']['metas_ideales']
                self.modelo_teorico.restricciones = config['modelo_teorico']['restricciones']
            
            # Reinicializar la interfaz para reflejar los nuevos valores
            self.restaurar_predeterminados()
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar configuración: {str(e)}")
            return False
    
    def guardar_a_archivo(self, archivo):
        """Guarda la configuración actual a un archivo JSON."""
        try:
            # Actualizar modelos con los valores de la interfaz
            self.actualizar_modelo_practico()
            self.actualizar_modelo_teorico()
            
            config = {
                'modelo_practico': {
                    'datos_operativos': self.modelo_practico.datos_operativos,
                    'parametros_simulacion': self.modelo_practico.parametros_simulacion
                },
                'modelo_teorico': {
                    'metas_ideales': self.modelo_teorico.metas_ideales,
                    'restricciones': self.modelo_teorico.restricciones
                }
            }
            
            with open(archivo, 'w') as f:
                json.dump(config, f, indent=4)
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar configuración: {str(e)}")
            return False