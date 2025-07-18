"""
Módulo principal de la interfaz gráfica para el Sistema de Modelado UMS.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import json
import os

# Importar componentes de la interfaz
from gui.paneles.configuracion import PanelConfiguracion
from gui.paneles.resultados import PanelResultados
from gui.paneles.brechas import PanelBrechas

# Importar modelos
from src.modelo_practico import UMSPractico
from src.modelo_teorico import UMSTeorico
from src.analisis_brechas import AnalisisBrechas

class InterfazPrincipal:
    def __init__(self, root):
        """
        Inicializa la interfaz principal.
        
        Args:
            root: Ventana raíz de Tkinter.
        """
        self.root = root
        self.root.title("Sistema de Modelado de Unidades Móviles de Salud")
        self.root.minsize(1000, 700)
        
        # Crear modelos
        self.modelo_practico = UMSPractico()
        self.modelo_teorico = UMSTeorico()
        self.analisis_brechas = AnalisisBrechas(self.modelo_practico, self.modelo_teorico)
        
        # Configurar interfaz
        self.crear_menu()
        self.crear_widgets()
        self.configurar_eventos()
        
        # Barra de estado
        self.barra_estado = ttk.Label(self.root, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Variables de estado
        self.ejecutando_simulacion = False
        self.ejecutando_optimizacion = False
    
    def crear_menu(self):
        """Crea la barra de menú."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Guardar configuración", command=self.guardar_configuracion)
        menu_archivo.add_command(label="Cargar configuración", command=self.cargar_configuracion)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        
        # Menú Modelos
        menu_modelos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modelos", menu=menu_modelos)
        menu_modelos.add_command(label="Ejecutar modelo práctico", command=self.ejecutar_modelo_practico)
        menu_modelos.add_command(label="Ejecutar modelo teórico", command=self.ejecutar_modelo_teorico)
        menu_modelos.add_command(label="Comparar modelos", command=self.comparar_modelos)
        menu_modelos.add_separator()
        menu_modelos.add_command(label="Restaurar valores predeterminados", command=self.restaurar_predeterminados)
        
        # Menú Informes
        menu_informes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Informes", menu=menu_informes)
        menu_informes.add_command(label="Generar informe completo", command=self.generar_informe)
        menu_informes.add_command(label="Exportar gráficos", command=self.exportar_graficos)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Manual de usuario", command=self.mostrar_manual)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
    
    def crear_widgets(self):
        """Crea los widgets principales."""
        # Notebook principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestañas principales
        # 1. Pestaña de configuración
        self.tab_config = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_config, text="Configuración")
        self.panel_config = PanelConfiguracion(self.tab_config, self.modelo_practico, self.modelo_teorico)
        self.panel_config.frame.pack(fill=tk.BOTH, expand=True)
        
        # 2. Pestaña de resultados
        self.tab_resultados = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_resultados, text="Resultados")
        self.panel_resultados = PanelResultados(self.tab_resultados)
        self.panel_resultados.frame.pack(fill=tk.BOTH, expand=True)
        
        # 3. Pestaña de análisis de brechas
        self.tab_brechas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_brechas, text="Análisis de Brechas")
        self.panel_brechas = PanelBrechas(self.tab_brechas, self.analisis_brechas)
        self.panel_brechas.frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear frame para botones de acción en la parte inferior
        self.frame_botones = ttk.Frame(self.root)
        self.frame_botones.pack(fill=tk.X, padx=10, pady=5)
        
        # Botones de acción
        self.btn_ejecutar_practico = ttk.Button(self.frame_botones, text="Ejecutar Modelo Práctico", 
                                               command=self.ejecutar_modelo_practico)
        self.btn_ejecutar_practico.pack(side=tk.LEFT, padx=5)
        
        self.btn_ejecutar_teorico = ttk.Button(self.frame_botones, text="Ejecutar Modelo Teórico", 
                                              command=self.ejecutar_modelo_teorico)
        self.btn_ejecutar_teorico.pack(side=tk.LEFT, padx=5)
        
        self.btn_comparar = ttk.Button(self.frame_botones, text="Comparar Modelos", 
                                      command=self.comparar_modelos)
        self.btn_comparar.pack(side=tk.LEFT, padx=5)
        
        # Indicador de progreso
        self.progreso = ttk.Progressbar(self.frame_botones, orient=tk.HORIZONTAL, 
                                       length=200, mode='indeterminate')
        self.progreso.pack(side=tk.RIGHT, padx=5)
    
    def configurar_eventos(self):
        """Configura eventos de la interfaz."""
        # Cambio de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.cambio_pestaña)
    
    def cambio_pestaña(self, event):
        """Maneja el cambio de pestaña."""
        pestaña_seleccionada = self.notebook.select()
        tab_id = self.notebook.index(pestaña_seleccionada)
        
        # Si se selecciona la pestaña de análisis de brechas, actualizar el análisis
        if tab_id == 2:  # Índice de la pestaña de brechas
            self.comparar_modelos()
    
    def ejecutar_modelo_practico(self):
        """Ejecuta el modelo práctico."""
        if self.ejecutando_simulacion:
            return  # Evitar ejecuciones simultáneas
        
        # Actualizar valores desde los campos de entrada
        try:
            self.actualizar_modelo_practico_desde_ui()
        except ValueError as e:
            messagebox.showerror("Error en los datos", f"Por favor verifique los valores ingresados: {str(e)}")
            return
        
        # Indicar que se está ejecutando la simulación
        self.ejecutando_simulacion = True
        self.barra_estado.config(text="Ejecutando modelo práctico...")
        self.progreso.start()
        self.btn_ejecutar_practico.state(['disabled'])
        
        # Ejecutar simulación en un hilo separado
        thread = threading.Thread(target=self._ejecutar_practico_thread)
        thread.daemon = True
        thread.start()
    
    def _ejecutar_practico_thread(self):
        """Ejecuta el modelo práctico en un hilo separado."""
        try:
            # Ejecutar simulación
            resultados = self.modelo_practico.simular()
            
            # Actualizar interfaz en el hilo principal
            self.root.after(0, self._finalizar_ejecucion_practico, resultados)
        except Exception as e:
            self.root.after(0, self._mostrar_error_practico, str(e))
    
    def _finalizar_ejecucion_practico(self, resultados):
        """Finaliza la ejecución del modelo práctico."""
        # Actualizar panel de resultados
        self.panel_resultados.actualizar_resultados_practico(self.modelo_practico)
        
        # Cambiar a pestaña de resultados
        self.notebook.select(1)  # Índice de la pestaña de resultados
        
        # Restablecer estado
        self.ejecutando_simulacion = False
        self.barra_estado.config(text="Modelo práctico ejecutado correctamente")
        self.progreso.stop()
        self.btn_ejecutar_practico.state(['!disabled'])
    
    def _mostrar_error_practico(self, mensaje_error):
        """Muestra mensaje de error al ejecutar el modelo práctico."""
        messagebox.showerror("Error al ejecutar el modelo práctico", mensaje_error)
        
        # Restablecer estado
        self.ejecutando_simulacion = False
        self.barra_estado.config(text="Error al ejecutar el modelo práctico")
        self.progreso.stop()
        self.btn_ejecutar_practico.state(['!disabled'])
    
    def ejecutar_modelo_teorico(self):
        """Ejecuta el modelo teórico."""
        if self.ejecutando_optimizacion:
            return  # Evitar ejecuciones simultáneas
        
        # Actualizar valores desde los campos de entrada
        try:
            self.actualizar_modelo_teorico_desde_ui()
        except ValueError as e:
            messagebox.showerror("Error en los datos", f"Por favor verifique los valores ingresados: {str(e)}")
            return
        
        # Indicar que se está ejecutando la optimización
        self.ejecutando_optimizacion = True
        self.barra_estado.config(text="Ejecutando modelo teórico...")
        self.progreso.start()
        self.btn_ejecutar_teorico.state(['disabled'])
        
        # Ejecutar optimización en un hilo separado
        thread = threading.Thread(target=self._ejecutar_teorico_thread)
        thread.daemon = True
        thread.start()
    
    def _ejecutar_teorico_thread(self):
        """Ejecuta el modelo teórico en un hilo separado."""
        try:
            # Ejecutar optimización
            resultados = self.modelo_teorico.optimizar()
            
            # Actualizar interfaz en el hilo principal
            self.root.after(0, self._finalizar_ejecucion_teorico, resultados)
        except Exception as e:
            self.root.after(0, self._mostrar_error_teorico, str(e))
    
    def _finalizar_ejecucion_teorico(self, resultados):
        """Finaliza la ejecución del modelo teórico."""
        # Actualizar panel de resultados
        self.panel_resultados.actualizar_resultados_teorico(self.modelo_teorico)
        
        # Cambiar a pestaña de resultados
        self.notebook.select(1)  # Índice de la pestaña de resultados
        
        # Restablecer estado
        self.ejecutando_optimizacion = False
        self.barra_estado.config(text="Modelo teórico ejecutado correctamente")
        self.progreso.stop()
        self.btn_ejecutar_teorico.state(['!disabled'])
    
    def _mostrar_error_teorico(self, mensaje_error):
        """Muestra mensaje de error al ejecutar el modelo teórico."""
        messagebox.showerror("Error al ejecutar el modelo teórico", mensaje_error)
        
        # Restablecer estado
        self.ejecutando_optimizacion = False
        self.barra_estado.config(text="Error al ejecutar el modelo teórico")
        self.progreso.stop()
        self.btn_ejecutar_teorico.state(['!disabled'])
    
    def comparar_modelos(self):
        """Compara los resultados de ambos modelos."""
        # Verificar que ambos modelos tengan resultados
        if not hasattr(self.modelo_practico, 'resultados') or not self.modelo_practico.resultados:
            messagebox.showwarning("Sin datos", "Primero debe ejecutar el modelo práctico")
            return
        
        if not hasattr(self.modelo_teorico, 'resultados') or not self.modelo_teorico.resultados:
            messagebox.showwarning("Sin datos", "Primero debe ejecutar el modelo teórico")
            return
        
        # Generar análisis de brechas
        self.analisis_brechas = AnalisisBrechas(self.modelo_practico, self.modelo_teorico)
        brechas = self.analisis_brechas.comparar_modelos()
        
        # Actualizar panel de brechas
        self.panel_brechas.actualizar_analisis(self.analisis_brechas)
        
        # Cambiar a pestaña de brechas
        self.notebook.select(2)  # Índice de la pestaña de brechas
        
        # Mensaje de estado
        self.barra_estado.config(text="Análisis de brechas generado correctamente")
    
    def actualizar_modelo_practico_desde_ui(self):
        """Actualiza el modelo práctico con los valores de la interfaz."""
        # Esta función será implementada por el panel de configuración
        self.panel_config.actualizar_modelo_practico()
    
    def actualizar_modelo_teorico_desde_ui(self):
        """Actualiza el modelo teórico con los valores de la interfaz."""
        # Esta función será implementada por el panel de configuración
        self.panel_config.actualizar_modelo_teorico()
    
    def guardar_configuracion(self):
        """Guarda la configuración actual en un archivo JSON."""
        # Solicitar ubicación del archivo
        archivo = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            title="Guardar configuración"
        )
        
        if not archivo:
            return
        
        # Recopilar configuración
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
        
        # Guardar en archivo JSON
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            
            self.barra_estado.config(text=f"Configuración guardada en {archivo}")
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo guardar la configuración: {str(e)}")
    
    def cargar_configuracion(self):
        """Carga la configuración desde un archivo JSON."""
        # Solicitar ubicación del archivo
        archivo = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            title="Cargar configuración"
        )
        
        if not archivo:
            return
        
        # Cargar archivo JSON
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Actualizar modelos
            if 'modelo_practico' in config:
                if 'datos_operativos' in config['modelo_practico']:
                    self.modelo_practico.datos_operativos = config['modelo_practico']['datos_operativos']
                
                if 'parametros_simulacion' in config['modelo_practico']:
                    self.modelo_practico.parametros_simulacion = config['modelo_practico']['parametros_simulacion']
            
            if 'modelo_teorico' in config:
                if 'metas_ideales' in config['modelo_teorico']:
                    self.modelo_teorico.metas_ideales = config['modelo_teorico']['metas_ideales']
                
                if 'restricciones' in config['modelo_teorico']:
                    self.modelo_teorico.restricciones = config['modelo_teorico']['restricciones']
            
            # Actualizar interfaz
            self.panel_config.actualizar_interfaz_desde_modelos()
            
            self.barra_estado.config(text=f"Configuración cargada desde {archivo}")
        except Exception as e:
            messagebox.showerror("Error al cargar", f"No se pudo cargar la configuración: {str(e)}")
    
    def restaurar_predeterminados(self):
        """Restaura los valores predeterminados en ambos modelos."""
        confirmacion = messagebox.askyesno(
            "Restaurar valores predeterminados",
            "¿Está seguro de que desea restaurar todos los valores a su configuración predeterminada?"
        )
        
        if not confirmacion:
            return
        
        # Crear nuevos modelos con valores predeterminados
        self.modelo_practico = UMSPractico()
        self.modelo_teorico = UMSTeorico()
        
        # Actualizar interfaz
        self.panel_config.actualizar_modelos(self.modelo_practico, self.modelo_teorico)
        
        # Actualizar análisis de brechas
        self.analisis_brechas = AnalisisBrechas(self.modelo_practico, self.modelo_teorico)
        
        self.barra_estado.config(text="Valores predeterminados restaurados")
    
    def generar_informe(self):
        """Genera un informe completo en formato PDF."""
        # Verificar que haya resultados
        if (not hasattr(self.modelo_practico, 'resultados') or not self.modelo_practico.resultados or
            not hasattr(self.modelo_teorico, 'resultados') or not self.modelo_teorico.resultados):
            messagebox.showwarning("Sin datos", "Primero debe ejecutar ambos modelos")
            return
        
        # Solicitar ubicación del archivo
        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
            title="Guardar informe"
        )
        
        if not archivo:
            return
        
        # Indicar generación en progreso
        self.barra_estado.config(text="Generando informe...")
        self.progreso.start()
        
        # Generar informe en un hilo separado (a implementar)
        thread = threading.Thread(target=self._generar_informe_thread, args=(archivo,))
        thread.daemon = True
        thread.start()
    
    def _generar_informe_thread(self, archivo):
        """Genera el informe en un hilo separado."""
        try:
            # Importar la función de generación de informes
            from gui.utils.reportes import generar_informe_completo
            
            # Generar el informe
            exito = generar_informe_completo(
                self.modelo_practico,
                self.modelo_teorico,
                self.analisis_brechas,
                archivo
            )
            
            # Finalizar generación en el hilo principal
            if exito:
                self.root.after(0, self._finalizar_generacion_informe, archivo)
            else:
                self.root.after(0, self._mostrar_error_informe, "Error al generar el informe PDF")
        except Exception as e:
            self.root.after(0, self._mostrar_error_informe, str(e))

    def _finalizar_generacion_informe(self, archivo):
        """Finaliza la generación del informe."""
        self.progreso.stop()
        self.barra_estado.config(text=f"Informe generado y guardado en {archivo}")
        messagebox.showinfo("Informe generado", f"El informe ha sido generado correctamente en:\n{archivo}")
    
    def _mostrar_error_informe(self, mensaje_error):
        """Muestra mensaje de error al generar el informe."""
        self.progreso.stop()
        self.barra_estado.config(text="Error al generar el informe")
        messagebox.showerror("Error al generar informe", mensaje_error)
    
    def exportar_graficos(self):
        """Exporta los gráficos generados como imágenes PNG."""
        # Verificar que haya resultados
        if (not hasattr(self.modelo_practico, 'resultados') or not self.modelo_practico.resultados or
            not hasattr(self.modelo_teorico, 'resultados') or not self.modelo_teorico.resultados):
            messagebox.showwarning("Sin datos", "Primero debe ejecutar ambos modelos")
            return
        
        # Solicitar directorio para guardar
        directorio = filedialog.askdirectory(title="Seleccione directorio para guardar los gráficos")
        
        if not directorio:
            return
        
        # Indicar exportación en progreso
        self.barra_estado.config(text="Exportando gráficos...")
        self.progreso.start()
        
        # Exportar gráficos en un hilo separado
        thread = threading.Thread(target=self._exportar_graficos_thread, args=(directorio,))
        thread.daemon = True
        thread.start()
    
    def _exportar_graficos_thread(self, directorio):
        """Exporta los gráficos en un hilo separado."""
        try:
            # Aquí iría la lógica para exportar los gráficos
            # Por ahora es un placeholder
            import time
            time.sleep(2)  # Simular exportación
            
            # Finalizar exportación en el hilo principal
            self.root.after(0, self._finalizar_exportacion_graficos, directorio)
        except Exception as e:
            self.root.after(0, self._mostrar_error_exportacion, str(e))
    
    def _finalizar_exportacion_graficos(self, directorio):
        """Finaliza la exportación de gráficos."""
        self.progreso.stop()
        self.barra_estado.config(text=f"Gráficos exportados a {directorio}")
        messagebox.showinfo("Gráficos exportados", f"Los gráficos han sido exportados correctamente a:\n{directorio}")
    
    def _mostrar_error_exportacion(self, mensaje_error):
        """Muestra mensaje de error al exportar gráficos."""
        self.progreso.stop()
        self.barra_estado.config(text="Error al exportar gráficos")
        messagebox.showerror("Error al exportar gráficos", mensaje_error)
    
    def mostrar_manual(self):
        """Muestra el manual de usuario en una ventana."""
        # Ruta del archivo de manual
        ruta_manual = os.path.join('docs', 'manual_usuario.md')
        
        if os.path.exists(ruta_manual):
            try:
                # Leer el contenido del archivo
                with open(ruta_manual, 'r', encoding='utf-8') as file:
                    contenido = file.read()
                
                # Crear ventana para mostrar el manual
                ventana_manual = tk.Toplevel(self.root)
                ventana_manual.title("Manual de Usuario")
                ventana_manual.geometry("800x600")
                
                # Frame con scrollbar para el contenido
                frame = ttk.Frame(ventana_manual)
                frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Scrollbar vertical
                scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                # Área de texto para mostrar el contenido
                texto = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
                texto.pack(fill=tk.BOTH, expand=True)
                scrollbar.config(command=texto.yview)
                
                # Insertar contenido
                texto.insert(tk.END, contenido)
                texto.config(state=tk.DISABLED)  # Hacer el texto de solo lectura
                
                return
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el manual: {str(e)}")
                return
        
        # Si no podemos abrir el archivo, mostrar mensaje
        messagebox.showinfo(
            "Manual de Usuario",
            "El manual de usuario se encuentra en el archivo docs/manual_usuario.md"
        )

    def mostrar_acerca_de(self):
        """Muestra información sobre la aplicación."""
        mensaje = """Sistema de Modelado de Unidades Móviles de Salud

Versión: 1.0
Fecha: 2025-07-17

Desarrollado por:
nicole1ariadna

Este software permite modelar y evaluar la viabilidad y efectividad 
de las Unidades Móviles de Salud (UMS) en contextos rurales colombianos.
"""
        messagebox.showinfo("Acerca de", mensaje)