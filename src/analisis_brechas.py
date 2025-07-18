"""
Módulo para el análisis de brechas entre los modelos práctico y teórico.
"""

import numpy as np

class AnalisisBrechas:
    def __init__(self, modelo_practico, modelo_teorico):
        """
        Inicializa el análisis de brechas.
        
        Args:
            modelo_practico: Instancia del modelo práctico.
            modelo_teorico: Instancia del modelo teórico.
        """
        self.modelo_practico = modelo_practico
        self.modelo_teorico = modelo_teorico
        self.matriz_brechas = {}
    
    def comparar_modelos(self):
        """
        Compara los resultados entre ambos modelos y calcula brechas.
        
        Returns:
            dict: Matriz de brechas.
        """
        # Verificar que ambos modelos tengan resultados
        if (not hasattr(self.modelo_practico, 'resultados') or 
            not self.modelo_practico.resultados or 
            not hasattr(self.modelo_teorico, 'resultados') or 
            not self.modelo_teorico.resultados):
            print("No hay resultados disponibles para comparar")
            return {}
        
        # Inicializar matriz
        self.matriz_brechas = {}
        
        # Calcular brecha de cobertura
        if ('estadisticas' in self.modelo_practico.resultados and 
            'configuracion' in self.modelo_teorico.resultados):
            
            # Obtener valores reales del modelo práctico
            cobertura_real = self.modelo_practico.resultados['estadisticas']['cobertura']['media']
            eficiencia_real = self.modelo_practico.datos_operativos['capacidad']['eficiencia']
            
            # Calcular costo por atención en el modelo práctico
            costos_reales = self.modelo_practico.resultados['estadisticas']['costos']['media']
            demanda_real = self.modelo_practico.resultados['estadisticas']['demanda']['media']
            costo_atencion_real = costos_reales / max(1, demanda_real)  # Evitar división por cero
            
            # Obtener sostenibilidad del modelo práctico
            sostenibilidad_real = self.modelo_practico.resultados['estadisticas']['sostenibilidad']['media']
            
            # Obtener valores ideales del modelo teórico
            cobertura_ideal = self.modelo_teorico.resultados['configuracion']['cobertura_objetivo']
            eficiencia_ideal = self.modelo_teorico.resultados['configuracion']['eficiencia_operativa']
            costo_atencion_ideal = self.modelo_teorico.resultados['configuracion']['costo_unitario']
            sostenibilidad_ideal = self.modelo_teorico.metas_ideales['financiero']['sostenibilidad_min']
            
            # Calcular brechas y determinar prioridades
            self.matriz_brechas['cobertura'] = {
                'real': cobertura_real,
                'ideal': cobertura_ideal,
                'brecha': self.calcular_brecha_porcentual(cobertura_real, cobertura_ideal),
                'prioridad': 'Baja'  # Se asignará luego
            }
            
            self.matriz_brechas['eficiencia'] = {
                'real': eficiencia_real,
                'ideal': eficiencia_ideal,
                'brecha': self.calcular_brecha_porcentual(eficiencia_real, eficiencia_ideal),
                'prioridad': 'Baja'
            }
            
            self.matriz_brechas['costo_efectividad'] = {
                'real': costo_atencion_real,
                'ideal': costo_atencion_ideal,
                'brecha': self.calcular_brecha_porcentual(costo_atencion_real, costo_atencion_ideal, menor_mejor=True),
                'prioridad': 'Baja'
            }
            
            self.matriz_brechas['sostenibilidad'] = {
                'real': sostenibilidad_real,
                'ideal': sostenibilidad_ideal,
                'brecha': self.calcular_brecha_porcentual(sostenibilidad_real, sostenibilidad_ideal),
                'prioridad': 'Baja'
            }
            
            # Asignar prioridades según magnitud de brechas
            for indicador, datos in self.matriz_brechas.items():
                if abs(datos['brecha']) >= 0.5:  # 50% o más de brecha
                    self.matriz_brechas[indicador]['prioridad'] = 'Alta'
                elif abs(datos['brecha']) >= 0.2:  # 20% o más de brecha
                    self.matriz_brechas[indicador]['prioridad'] = 'Media'
                else:
                    self.matriz_brechas[indicador]['prioridad'] = 'Baja'
        
        return self.matriz_brechas
    
    def calcular_brecha_porcentual(self, valor_real, valor_ideal, menor_mejor=False):
        """
        Calcula la brecha porcentual entre el valor real y el ideal.
        
        Args:
            valor_real: Valor real (modelo práctico).
            valor_ideal: Valor ideal (modelo teórico).
            menor_mejor: Si True, valores menores son mejores (ej: costos).
            
        Returns:
            float: Brecha porcentual.
        """
        if valor_ideal == 0:
            return 0  # Evitar división por cero
        
        brecha = (valor_real - valor_ideal) / valor_ideal
        
        # Si menor es mejor (ej: costos), invertir el signo de la brecha
        if menor_mejor:
            brecha = -brecha
        
        return brecha
    
    def generar_recomendaciones(self):
        """
        Genera recomendaciones basadas en el análisis de brechas.
        
        Returns:
            list: Lista de recomendaciones ordenadas por prioridad.
        """
        if not self.matriz_brechas:
            self.comparar_modelos()
        
        if not self.matriz_brechas:
            return []
        
        recomendaciones = []
        
        # Generar recomendaciones para cada indicador con brecha significativa (>10%)
        for indicador, datos in self.matriz_brechas.items():
            if abs(datos['brecha']) < 0.1:  # Menos de 10% de brecha
                continue
            
            recomendacion = {
                'indicador': indicador.replace('_', ' ').title(),
                'prioridad': datos['prioridad'],
                'recomendacion': self._generar_texto_recomendacion(indicador, datos)
            }
            
            recomendaciones.append(recomendacion)
        
        # Ordenar por prioridad (Alta > Media > Baja)
        orden_prioridad = {'Alta': 0, 'Media': 1, 'Baja': 2}
        recomendaciones.sort(key=lambda x: orden_prioridad[x['prioridad']])
        
        return recomendaciones
    
    def _generar_texto_recomendacion(self, indicador, datos):
        """
        Genera texto de recomendación para un indicador específico.
        
        Args:
            indicador: Nombre del indicador.
            datos: Datos de la brecha.
            
        Returns:
            str: Texto de recomendación.
        """
        brecha_abs = abs(datos['brecha'])
        brecha_pct = datos['brecha'] * 100
        
        if indicador == 'cobertura':
            if datos['brecha'] < 0:
                return (f"La cobertura actual ({datos['real']*100:.1f}%) está {brecha_pct:.1f}% por debajo del "
                        f"objetivo ideal ({datos['ideal']*100:.1f}%). Se recomienda aumentar la frecuencia "
                        f"de visitas o ampliar el alcance geográfico de las UMS.")
            else:
                return (f"La cobertura actual ({datos['real']*100:.1f}%) supera en {brecha_pct:.1f}% al "
                        f"objetivo ideal ({datos['ideal']*100:.1f}%). Se recomienda mantener el esquema actual "
                        f"de operación y considerar optimizar recursos.")
        
        elif indicador == 'eficiencia':
            if datos['brecha'] < 0:
                return (f"La eficiencia operativa actual ({datos['real']*100:.1f}%) está {brecha_pct:.1f}% por debajo "
                        f"del nivel ideal ({datos['ideal']*100:.1f}%). Se recomienda optimizar procesos, "
                        f"mejorar capacitación del personal y revisar protocolos de atención.")
            else:
                return (f"La eficiencia operativa actual ({datos['real']*100:.1f}%) supera en {brecha_pct:.1f}% al "
                        f"nivel ideal ({datos['ideal']*100:.1f}%). Se recomienda documentar las buenas prácticas "
                        f"y extenderlas a otras UMS.")
        
        elif indicador == 'costo_efectividad':
            if datos['brecha'] < 0:  # Recordar que menor es mejor para costos
                return (f"El costo por atención actual (${datos['real']:,.0f}) está {brecha_pct:.1f}% por encima "
                        f"del objetivo ideal (${datos['ideal']:,.0f}). Se recomienda revisar la estructura de costos, "
                        f"optimizar rutas y buscar eficiencias operativas.")
            else:
                return (f"El costo por atención actual (${datos['real']:,.0f}) está {brecha_pct:.1f}% por debajo "
                        f"del umbral ideal (${datos['ideal']:,.0f}). Se recomienda mantener la estructura de costos "
                        f"actual y evaluar si se pueden realizar mejoras adicionales en calidad.")
        
        elif indicador == 'sostenibilidad':
            if datos['brecha'] < 0:
                return (f"El ratio de sostenibilidad actual ({datos['real']:.2f}) está {brecha_pct:.1f}% por debajo "
                        f"del objetivo ideal ({datos['ideal']:.2f}). Se recomienda evaluar fuentes adicionales de "
                        f"financiamiento, revisar tarifas y optimizar costos operativos.")
            else:
                return (f"El ratio de sostenibilidad actual ({datos['real']:.2f}) supera en {brecha_pct:.1f}% al "
                        f"objetivo ideal ({datos['ideal']:.2f}). Se recomienda reinvertir los excedentes en "
                        f"mejoras de equipamiento o ampliación de servicios.")
        
        else:
            return f"Se identificó una brecha de {brecha_pct:.1f}% en {indicador}. Se recomienda revisar este indicador."