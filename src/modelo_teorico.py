"""
Modelo Teórico (Normativo) para la evaluación de Unidades Móviles de Salud.
Este modelo se basa en indicadores normativos ideales.
"""

import os
import json
import numpy as np
from scipy.optimize import minimize

from src.optimizacion import optimizar_configuracion_ums
from src.indicadores import calcular_indices_desempeno
from src.visualizacion import generar_graficos_teorico

class UMSTeorico:
    def __init__(self):
        """
        Inicializa el modelo teórico.
        """
        # Metas ideales para indicadores normativos
        self.metas_ideales = {
            'cobertura': {
                'poblacion_objetivo': 1.0,
                'frecuencia_visitas': 2,
                'tiempo_acceso_max': 60,
                'satisfaccion_min': 0.95
            },
            'operacion': {
                'capacidad_optima': 40,
                'eficiencia_operativa': 0.8,
                'resolucion_primer_nivel': 0.85,
                'tiempo_espera_max': 30
            },
            'financiero': {
                'costo_unitario_max': 70000,
                'sostenibilidad_min': 1.0,
                'autofinanciacion': 0.6
            },
            'calidad': {
                'continuidad_atencion': 0.85,
                'integracion_historia': 1.0,
                'referencia_efectiva': 0.9
            }
        }
        
        # Restricciones para la optimización
        self.restricciones = [
            {'tipo': 'cobertura_minima', 'valor': 0.6},
            {'tipo': 'sostenibilidad_minima', 'valor': 0.6},
            {'tipo': 'calidad_minima', 'valor': 0.7}
        ]
        
        # Configuración inicial (punto de partida para optimización)
        self.configuracion_inicial = {
            'capacidad_diaria': 30,    # pacientes/día
            'eficiencia_operativa': 0.7,   # eficiencia
            'cobertura_objetivo': 0.8,   # cobertura
            'costo_unitario': 90000  # costo unitario (COP)
        }
        
        # Resultados de la optimización
        self.resultados = {}
        
        # Flag para el modo de optimización
        self.usar_optimizacion = True
    
    def cargar_metas(self, ruta_archivo=None):
        """
        Carga metas ideales desde un archivo JSON.
        
        Args:
            ruta_archivo: Ruta al archivo JSON con metas (opcional).
            
        Returns:
            bool: True si se cargaron correctamente, False en caso contrario.
        """
        if not ruta_archivo:
            ruta_archivo = os.path.join('data', 'metas_ideales.json')
        
        try:
            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    self.metas_ideales = json.load(f)
                return True
            return False
        except Exception as e:
            print(f"Error al cargar metas: {str(e)}")
            return False
    
    def optimizar(self):
        """
        Ejecuta el algoritmo de optimización para encontrar la configuración óptima de UMS.
        
        Returns:
            dict: Resultados de la optimización incluyendo configuración óptima.
        """
        # Asegurarse de que tengamos metas cargadas
        if not self.metas_ideales:
            self.cargar_metas()
        
        # Usar la configuración actual como punto de partida para la optimización
        x0 = [
            self.configuracion_inicial['capacidad_diaria'],      # capacidad_diaria (pacientes/día)
            self.configuracion_inicial['eficiencia_operativa'],  # eficiencia_operativa
            self.configuracion_inicial['cobertura_objetivo'],    # cobertura_objetivo
            self.configuracion_inicial['costo_unitario']         # costo_unitario (COP)
        ]
        
        # Imprimir el punto de partida para depuración
        print(f"Punto de partida para optimización: {x0}")
        
        # Si no estamos usando optimización, usar directamente los valores configurados
        if not self.usar_optimizacion:
            print("Usando directamente los valores configurados sin optimización")
            self.resultados = {
                'configuracion': {
                    'capacidad_diaria': self.configuracion_inicial['capacidad_diaria'],
                    'eficiencia_operativa': self.configuracion_inicial['eficiencia_operativa'],
                    'cobertura_objetivo': self.configuracion_inicial['cobertura_objetivo'],
                    'costo_unitario': self.configuracion_inicial['costo_unitario']
                }
            }
            
            # Calcular estadísticas derivadas
            self._calcular_estadisticas_derivadas()
            
            # Evaluar cumplimiento de metas
            self._evaluar_cumplimiento_metas()
            
            return self.resultados
        
        # Ejecutar optimización
        try:
            # Definir función objetivo para minimizar
            def funcion_objetivo(x):
                # Desempacar variables
                capacidad_diaria = x[0]
                eficiencia_operativa = x[1]
                cobertura_objetivo = x[2]
                costo_unitario = x[3]
                
                # Normalizar costo (menor es mejor)
                costo_normalizado = costo_unitario / self.metas_ideales['financiero']['costo_unitario_max']
                
                # Penalizaciones por desviación de metas
                penalizacion_capacidad = abs(capacidad_diaria - self.metas_ideales['operacion']['capacidad_optima']) / self.metas_ideales['operacion']['capacidad_optima']
                penalizacion_eficiencia = abs(eficiencia_operativa - self.metas_ideales['operacion']['eficiencia_operativa']) / self.metas_ideales['operacion']['eficiencia_operativa']
                penalizacion_cobertura = abs(cobertura_objetivo - self.metas_ideales['cobertura']['poblacion_objetivo']) / self.metas_ideales['cobertura']['poblacion_objetivo']
                
                # Función objetivo ponderada (minimizar)
                return (0.4 * costo_normalizado + 
                        0.2 * penalizacion_capacidad + 
                        0.2 * penalizacion_eficiencia + 
                        0.2 * penalizacion_cobertura)
            
            # Definir restricciones
            restricciones = []
            
            # Restricción de cobertura mínima
            restricciones.append({
                'type': 'ineq',
                'fun': lambda x: x[2] - self.restricciones[0]['valor']
            })
            
            # Restricción de sostenibilidad mínima (aproximación)
            restricciones.append({
                'type': 'ineq',
                'fun': lambda x: (1 / (x[3] / 100000)) - self.restricciones[1]['valor']
            })
            
            # Definir límites para las variables
            bounds = [
                (20, 50),      # capacidad_diaria
                (0.4, 0.95),   # eficiencia_operativa
                (0.6, 1.0),    # cobertura_objetivo
                (50000, 120000) # costo_unitario
            ]
            
            # Ejecutar optimización
            resultado = minimize(
                fun=funcion_objetivo,
                x0=x0,
                method='SLSQP',
                bounds=bounds,
                constraints=restricciones
            )
            
            # Guardar configuración óptima
            self.resultados = {
                'configuracion': {
                    'capacidad_diaria': resultado.x[0],
                    'eficiencia_operativa': resultado.x[1],
                    'cobertura_objetivo': resultado.x[2],
                    'costo_unitario': resultado.x[3]
                }
            }
            
            # Calcular estadísticas derivadas
            self._calcular_estadisticas_derivadas()
            
            # Evaluar cumplimiento de metas
            self._evaluar_cumplimiento_metas()
            
            return self.resultados
        
        except Exception as e:
            print(f"Error en optimización: {str(e)}")
            return {}
    
    def _calcular_estadisticas_derivadas(self):
        """
        Calcula estadísticas derivadas basadas en la configuración óptima.
        """
        if 'configuracion' not in self.resultados:
            return
        
        # Obtener valores de configuración óptima
        config = self.resultados['configuracion']
        capacidad_diaria = config['capacidad_diaria']
        eficiencia = config['eficiencia_operativa']
        cobertura = config['cobertura_objetivo']
        costo_unitario = config['costo_unitario']
        
        # Suponer que hay 20 días operativos al mes
        dias_mes = 20
        
        # Calcular atenciones mensuales
        atenciones_mensuales = capacidad_diaria * eficiencia * dias_mes
        
        # Calcular población cubierta (suponiendo población de referencia de 10,000)
        poblacion_referencia = 10000
        poblacion_cubierta = poblacion_referencia * cobertura
        
        # Calcular UMS requeridas por 100,000 habitantes
        ums_requeridas_100k = 100000 / (poblacion_cubierta / 1)  # 1 UMS para la población cubierta
        
        # Calcular costo mensual
        costo_total_mensual = costo_unitario * atenciones_mensuales
        
        # Calcular costo por habitante al mes
        costo_por_habitante_mes = costo_total_mensual / poblacion_cubierta if poblacion_cubierta > 0 else 0
        
        # Guardar estadísticas derivadas
        self.resultados['estadisticas'] = {
            'atenciones_mensuales': atenciones_mensuales,
            'poblacion_cubierta': poblacion_cubierta,
            'ums_requeridas_100k': ums_requeridas_100k,
            'costo_total_mensual': costo_total_mensual,
            'costo_por_habitante_mes': costo_por_habitante_mes
        }
    
    def _evaluar_cumplimiento_metas(self):
        """
        Evalúa el cumplimiento de las metas establecidas.
        """
        if 'configuracion' not in self.resultados:
            return
        
        # Obtener valores de la configuración óptima
        config = self.resultados['configuracion']
        
        # Calcular cumplimiento por categoría
        cumplimiento_por_categoria = {}
        cumplimiento_detallado = {}
        
        # Cobertura
        cobertura_real = config['cobertura_objetivo']
        cobertura_meta = self.metas_ideales['cobertura']['poblacion_objetivo']
        cumplimiento_cobertura = min(cobertura_real / cobertura_meta, 1.0)
        cumplimiento_por_categoria['cobertura'] = cumplimiento_cobertura
        cumplimiento_detallado['cobertura_poblacion'] = {
            'valor_real': cobertura_real,
            'meta': cobertura_meta,
            'cumplimiento': cumplimiento_cobertura
        }
        
        # Operación
        eficiencia_real = config['eficiencia_operativa']
        eficiencia_meta = self.metas_ideales['operacion']['eficiencia_operativa']
        cumplimiento_eficiencia = min(eficiencia_real / eficiencia_meta, 1.0)
        
        capacidad_real = config['capacidad_diaria']
        capacidad_meta = self.metas_ideales['operacion']['capacidad_optima']
        cumplimiento_capacidad = min(capacidad_real / capacidad_meta, 1.0)
        
        cumplimiento_operacion = (cumplimiento_eficiencia + cumplimiento_capacidad) / 2
        cumplimiento_por_categoria['operacion'] = cumplimiento_operacion
        
        cumplimiento_detallado['eficiencia_operativa'] = {
            'valor_real': eficiencia_real,
            'meta': eficiencia_meta,
            'cumplimiento': cumplimiento_eficiencia
        }
        cumplimiento_detallado['capacidad_diaria'] = {
            'valor_real': capacidad_real,
            'meta': capacidad_meta,
            'cumplimiento': cumplimiento_capacidad
        }
        
        # Financiero
        costo_real = config['costo_unitario']
        costo_meta = self.metas_ideales['financiero']['costo_unitario_max']
        # Para costos, menor es mejor, así que invertimos la relación
        cumplimiento_costo = min(costo_meta / max(costo_real, 1), 1.0)
        
        # Asumimos sostenibilidad basada en el costo
        sostenibilidad_real = min(1.2, self.metas_ideales['financiero']['sostenibilidad_min'] + 0.1)
        sostenibilidad_meta = self.metas_ideales['financiero']['sostenibilidad_min']
        cumplimiento_sostenibilidad = min(sostenibilidad_real / sostenibilidad_meta, 1.0)
        
        cumplimiento_financiero = (cumplimiento_costo + cumplimiento_sostenibilidad) / 2
        cumplimiento_por_categoria['financiero'] = cumplimiento_financiero
        
        cumplimiento_detallado['costo_unitario'] = {
            'valor_real': costo_real,
            'meta': costo_meta,
            'cumplimiento': cumplimiento_costo
        }
        cumplimiento_detallado['sostenibilidad'] = {
            'valor_real': sostenibilidad_real,
            'meta': sostenibilidad_meta,
            'cumplimiento': cumplimiento_sostenibilidad
        }
        
        # Calidad (valores estimados basados en otros indicadores)
        calidad_estimada = (cumplimiento_cobertura + cumplimiento_operacion) / 2
        cumplimiento_por_categoria['calidad'] = calidad_estimada
        
        # Calcular cumplimiento global (promedio ponderado)
        pesos = {
            'cobertura': 0.3,
            'operacion': 0.3,
            'financiero': 0.25,
            'calidad': 0.15
        }
        
        cumplimiento_global = sum(
            valor * pesos[categoria] 
            for categoria, valor in cumplimiento_por_categoria.items()
        )
        
        # Guardar resultados de cumplimiento
        self.resultados['cumplimiento'] = {
            'global': cumplimiento_global,
            'por_categoria': cumplimiento_por_categoria,
            'detallado': cumplimiento_detallado
        }
    
    def evaluar_cumplimiento(self):
        """
        Evalúa el cumplimiento de las metas establecidas.
        
        Returns:
            dict: Resultados del cumplimiento.
        """
        # Si ya tenemos resultados de cumplimiento, devolver
        if 'cumplimiento' in self.resultados:
            return self.resultados['cumplimiento']
        
        # Si no hay configuración óptima, no podemos evaluar
        if 'configuracion' not in self.resultados:
            return {}
        
        # Evaluar cumplimiento
        self._evaluar_cumplimiento_metas()
        
        return self.resultados.get('cumplimiento', {})