"""
Pruebas de integración para el sistema de modelado UMS.
"""

import sys
import os
import unittest
import tempfile

# Añadir directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modelo_practico import UMSPractico
from src.modelo_teorico import UMSTeorico
from src.analisis_brechas import AnalisisBrechas
from src.visualizacion import (
    generar_graficos_practico, 
    generar_graficos_teorico, 
    generar_graficos_comparativos
)

class TestIntegracion(unittest.TestCase):
    """Clase para probar la integración entre componentes."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear instancias con parámetros reducidos para pruebas
        self.modelo_practico = UMSPractico()
        self.modelo_practico.parametros_simulacion = {
            'num_simulaciones': 5,
            'horizonte_temporal': 6  # meses
        }
        
        self.modelo_teorico = UMSTeorico()
    
    def test_flujo_completo(self):
        """Prueba el flujo completo de operación del sistema."""
        # 1. Ejecutar modelo práctico
        resultado_practico = self.modelo_practico.simular()
        
        # Verificar resultados del modelo práctico
        self.assertIsNotNone(resultado_practico)
        self.assertIn('estadisticas', resultado_practico)
        
        # 2. Ejecutar modelo teórico
        resultado_teorico = self.modelo_teorico.optimizar()
        
        # Verificar resultados del modelo teórico
        self.assertIsNotNone(resultado_teorico)
        self.assertIn('configuracion', resultado_teorico)
        
        # 3. Analizar brechas
        analisis = AnalisisBrechas(self.modelo_practico, self.modelo_teorico)
        brechas = analisis.comparar_modelos()
        
        # Verificar matriz de brechas
        self.assertIsNotNone(brechas)
        indicadores_esperados = {'cobertura', 'costo_efectividad', 'sostenibilidad', 'eficiencia'}
        self.assertEqual(set(brechas.keys()), indicadores_esperados)
        
        # 4. Generar recomendaciones
        recomendaciones = analisis.generar_recomendaciones()
        
        # Las recomendaciones pueden ser vacías si no hay brechas significativas
        self.assertIsInstance(recomendaciones, list)
        
        # Si hay recomendaciones, verificar su estructura
        if recomendaciones:
            self.assertIn('indicador', recomendaciones[0])
            self.assertIn('prioridad', recomendaciones[0])
            self.assertIn('recomendacion', recomendaciones[0])
    
    def test_generacion_graficos(self):
        """Prueba la generación de gráficos."""
        # Ejecutar modelos
        self.modelo_practico.simular()
        self.modelo_teorico.optimizar()
        
        # Generar gráficos del modelo práctico
        graficos_practico = generar_graficos_practico(self.modelo_practico.resultados)
        
        # Verificar gráficos del modelo práctico
        self.assertIsNotNone(graficos_practico)
        graficos_esperados = {'demanda', 'costos_demanda', 'sostenibilidad', 'dashboard'}
        self.assertTrue(set(graficos_practico.keys()).issuperset(graficos_esperados))
        
        # Generar gráficos del modelo teórico
        graficos_teorico = generar_graficos_teorico(self.modelo_teorico.resultados)
        
        # Verificar gráficos del modelo teórico
        self.assertIsNotNone(graficos_teorico)
        
        # Generar gráficos comparativos
        graficos_comp = generar_graficos_comparativos(self.modelo_practico, self.modelo_teorico)
        
        # Verificar gráficos comparativos
        self.assertIsNotNone(graficos_comp)
    
    def test_guardar_cargar_configuracion(self):
        """Prueba guardar y cargar configuración."""
        # Modificar algunos parámetros
        self.modelo_practico.datos_operativos['capacidad']['pacientes_dia'] = 30
        self.modelo_practico.datos_operativos['costos']['variable_paciente'] = 55000
        
        self.modelo_teorico.metas_ideales['operacion']['capacidad_optima'] = 45
        self.modelo_teorico.metas_ideales['financiero']['costo_unitario_max'] = 90000
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
            temp_filename = temp.name
        
        try:
            # Guardar configuración en formato JSON
            import json
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
            
            with open(temp_filename, 'w') as f:
                json.dump(config, f)
            
            # Crear nuevas instancias
            modelo_practico_nuevo = UMSPractico()
            modelo_teorico_nuevo = UMSTeorico()
            
            # Cargar configuración
            with open(temp_filename, 'r') as f:
                config_cargada = json.load(f)
            
            modelo_practico_nuevo.datos_operativos = config_cargada['modelo_practico']['datos_operativos']
            modelo_practico_nuevo.parametros_simulacion = config_cargada['modelo_practico']['parametros_simulacion']
            
            modelo_teorico_nuevo.metas_ideales = config_cargada['modelo_teorico']['metas_ideales']
            modelo_teorico_nuevo.restricciones = config_cargada['modelo_teorico']['restricciones']
            
            # Verificar valores cargados
            self.assertEqual(modelo_practico_nuevo.datos_operativos['capacidad']['pacientes_dia'], 30)
            self.assertEqual(modelo_practico_nuevo.datos_operativos['costos']['variable_paciente'], 55000)
            
            self.assertEqual(modelo_teorico_nuevo.metas_ideales['operacion']['capacidad_optima'], 45)
            self.assertEqual(modelo_teorico_nuevo.metas_ideales['financiero']['costo_unitario_max'], 90000)
            
            # Verificar que los modelos funcionan correctamente con la configuración cargada
            modelo_practico_nuevo.simular()
            modelo_teorico_nuevo.optimizar()
            
            self.assertIsNotNone(modelo_practico_nuevo.resultados.get('estadisticas'))
            self.assertIsNotNone(modelo_teorico_nuevo.resultados.get('configuracion'))
            
        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

if __name__ == '__main__':
    unittest.main()