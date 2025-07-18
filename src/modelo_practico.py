"""
Modelo Práctico (Empírico) para la evaluación de Unidades Móviles de Salud.
Este modelo se basa en datos operativos reales extraídos de trabajos relacionados.
"""

import numpy as np
import pandas as pd

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simulacion import generar_demanda_diaria, calcular_tiempo_atencion
from src.costos import calcular_costos_totales, analizar_sostenibilidad
from src.visualizacion import generar_graficos_practico

class UMSPractico:
    def __init__(self):
        """Inicializa el modelo práctico con datos operativos predeterminados."""
        # Estructura principal de datos operativos
        self.datos_operativos = {
            'capacidad': {
                'pacientes_dia': 24,
                'dias_mes': 20,
                'eficiencia': 0.4
            },
            'costos': {
                'fijo_mensual': 17291667,
                'variable_paciente': 45000,
                'mantenimiento_anual': 20750000,
                'costo_unitario_atencion': 103750,
                'costo_vehiculo': 580000000
            },
            'personal': {
                'medico': 1,
                'enfermera': 1,
                'conductor': 1,
                'costo_personal_mes': 8500000
            },
            'servicios': {
                'consulta_general': 0.70,
                'vacunacion': 0.20,
                'control_prenatal': 0.10
            },
            'cobertura': {
                'poblacion_objetivo': 10000,  # Ajustable según región
                'frecuencia_visitas': 1,      # visitas/mes
                'radio_cobertura': 50,        # km
                'poblacion_por_km2': 15       # habitantes/km²
            }
        }
        
        self.parametros_simulacion = {
            'num_simulaciones': 1000,
            'horizonte_temporal': 60  # meses
        }
        
        self.resultados = {
            'demanda': [],
            'costos': [],
            'cobertura': [],
            'sostenibilidad': [],
            'estadisticas': {}
        }
    
    def cargar_datos(self, ruta_archivo=None):
        """Carga datos operativos desde un archivo JSON o utiliza los predeterminados."""
        if ruta_archivo:
            try:
                import json
                with open(ruta_archivo, 'r') as f:
                    self.datos_operativos = json.load(f)
                return True
            except Exception as e:
                print(f"Error al cargar datos: {e}")
                return False
        return True  # Usando datos predeterminados
    
    def simular(self):
        """Ejecuta la simulación del modelo práctico."""
        # Resetear resultados previos
        self.resultados = {
            'demanda': [],
            'costos': [],
            'cobertura': [],
            'sostenibilidad': [],
            'estadisticas': {}
        }
        
        # Parámetros de la simulación
        capacidad_diaria = self.datos_operativos['capacidad']['pacientes_dia']
        dias_mes = self.datos_operativos['capacidad']['dias_mes']
        eficiencia = self.datos_operativos['capacidad']['eficiencia']
        
        # Ejecutar simulaciones
        for i in range(self.parametros_simulacion['num_simulaciones']):
            resultados_simulacion = self._simular_operacion(
                self.datos_operativos, 
                self.parametros_simulacion['horizonte_temporal']
            )
            
            # Almacenar resultados de esta simulación
            self.resultados['demanda'].append(resultados_simulacion['demanda'])
            self.resultados['costos'].append(resultados_simulacion['costos'])
            self.resultados['cobertura'].append(resultados_simulacion['cobertura'])
            self.resultados['sostenibilidad'].append(resultados_simulacion['sostenibilidad'])
        
        # Calcular estadísticas agregadas
        self._calcular_estadisticas()
        
        return self.resultados
    
    def _simular_operacion(self, parametros, horizonte_temporal):
        """Simula la operación de la UMS durante un horizonte temporal."""
        resultados_mensuales = {
            'demanda': [],
            'costos': [],
            'cobertura': [],
            'sostenibilidad': []
        }
        
        # Configuración inicial
        capacidad_diaria = parametros['capacidad']['pacientes_dia']
        dias_mes = parametros['capacidad']['dias_mes']
        eficiencia = parametros['capacidad']['eficiencia']
        poblacion_objetivo = parametros['cobertura']['poblacion_objetivo']
        
        # Simulación por mes
        for mes in range(horizonte_temporal):
            demanda_mensual = 0
            
            # Simulación por día
            for dia in range(dias_mes):
                # Generar demanda diaria aleatoria usando distribución Poisson
                demanda_diaria = generar_demanda_diaria(capacidad_diaria)
                # Limitar por capacidad real (con eficiencia operativa)
                atenciones_reales = min(demanda_diaria, capacidad_diaria * eficiencia)
                demanda_mensual += atenciones_reales
            
            # Calcular costos del mes
            costos_mes = calcular_costos_totales(
                atenciones=demanda_mensual,
                costos_fijos=parametros['costos']['fijo_mensual'],
                costo_variable=parametros['costos']['variable_paciente']
            )
            
            # Calcular cobertura (porcentaje de población atendida)
            # Asumiendo que cada persona requiere atención cada 6 meses en promedio
            poblacion_atendible_mensual = poblacion_objetivo / 6
            cobertura = min(1.0, demanda_mensual / poblacion_atendible_mensual)
            
            # Calcular sostenibilidad financiera
            sostenibilidad = analizar_sostenibilidad(
                ingresos=demanda_mensual * parametros['costos']['costo_unitario_atencion'],
                costos=costos_mes
            )
            
            # Almacenar resultados del mes
            resultados_mensuales['demanda'].append(demanda_mensual)
            resultados_mensuales['costos'].append(costos_mes)
            resultados_mensuales['cobertura'].append(cobertura)
            resultados_mensuales['sostenibilidad'].append(sostenibilidad)
        
        # Agregar resultados finales de esta simulación
        return {
            'demanda': np.mean(resultados_mensuales['demanda']),
            'costos': np.mean(resultados_mensuales['costos']),
            'cobertura': np.mean(resultados_mensuales['cobertura']),
            'sostenibilidad': np.mean(resultados_mensuales['sostenibilidad'])
        }
    
    def _calcular_estadisticas(self):
        """Calcula estadísticas descriptivas de los resultados de simulación."""
        for variable in ['demanda', 'costos', 'cobertura', 'sostenibilidad']:
            datos = np.array(self.resultados[variable])
            self.resultados['estadisticas'][variable] = {
                'media': np.mean(datos),
                'mediana': np.median(datos),
                'desviacion': np.std(datos),
                'min': np.min(datos),
                'max': np.max(datos),
                'percentil_25': np.percentile(datos, 25),
                'percentil_75': np.percentile(datos, 75)
            }
    
    def calcular_costos(self):
        """Calcula detalle de costos del modelo."""
        if not self.resultados['estadisticas']:
            self.simular()
            
        demanda_media = self.resultados['estadisticas']['demanda']['media']
        
        # Costos fijos mensuales
        costos_fijos = self.datos_operativos['costos']['fijo_mensual']
        
        # Costos variables (por atención)
        costos_variables = demanda_media * self.datos_operativos['costos']['variable_paciente']
        
        # Costo de personal
        costo_personal = self.datos_operativos['personal']['costo_personal_mes']
        
        # Depreciación del vehículo (asumiendo 5 años de vida útil)
        depreciacion_mensual = self.datos_operativos['costos']['costo_vehiculo'] / (5 * 12)
        
        # Mantenimiento mensual
        mantenimiento_mensual = self.datos_operativos['costos']['mantenimiento_anual'] / 12
        
        return {
            'fijos': costos_fijos,
            'variables': costos_variables,
            'personal': costo_personal,
            'depreciacion': depreciacion_mensual,
            'mantenimiento': mantenimiento_mensual,
            'total_mensual': costos_fijos + costos_variables + costo_personal + depreciacion_mensual + mantenimiento_mensual,
            'costo_por_atencion': (costos_fijos + costos_variables + costo_personal + depreciacion_mensual + mantenimiento_mensual) / demanda_media if demanda_media > 0 else float('inf')
        }
    
    def generar_reportes(self):
        """Genera reportes y visualizaciones de los resultados."""
        if not self.resultados['estadisticas']:
            self.simular()
            
        # Generar gráficos usando el módulo de visualización
        graficos = generar_graficos_practico(self.resultados)
        
        # Calcular costos detallados
        costos_detalle = self.calcular_costos()
        
        return {
            'graficos': graficos,
            'costos': costos_detalle,
            'estadisticas': self.resultados['estadisticas']
        }