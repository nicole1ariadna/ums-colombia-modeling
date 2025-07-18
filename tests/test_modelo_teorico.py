"""
Pruebas unitarias para el módulo modelo_teorico.py
"""

import sys
import os
import unittest
import numpy as np

# Añadir directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modelo_teorico import UMSTeorico

class TestModeloTeorico(unittest.TestCase):
    """Clase para probar el funcionamiento del modelo teórico."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.modelo = UMSTeorico()
    
    def test_inicializacion(self):
        """Prueba la inicialización correcta del modelo."""
        # Verificar estructura de metas ideales
        self.assertIsInstance(self.modelo.metas_ideales, dict)
        
        # Verificar categorías
        categorias_esperadas = {'cobertura', 'operacion', 'financiero', 'calidad'}
        self.assertEqual(set(self.modelo.metas_ideales.keys()), categorias_esperadas)
        
        # Verificar valores específicos
        self.assertEqual(self.modelo.metas_ideales['cobertura']['poblacion_objetivo'], 1.0)
        self.assertEqual(self.modelo.metas_ideales['cobertura']['frecuencia_visitas'], 2)
        self.assertEqual(self.modelo.metas_ideales['operacion']['capacidad_optima'], 40)
        self.assertEqual(self.modelo.metas_ideales['financiero']['costo_unitario_max'], 80000)
    
    def test_optimizacion(self):
        """Prueba la ejecución de la optimización."""
        # Ejecutar optimización
        resultados = self.modelo.optimizar()
        
        # Verificar que se generaron resultados
        self.assertIsNotNone(resultados)
        self.assertIn('configuracion', resultados)
        self.assertIn('indicadores', resultados)
        
        # Verificar estructura de la configuración óptima
        config = resultados['configuracion']
        self.assertIn('capacidad_diaria', config)
        self.assertIn('eficiencia_operativa', config)
        self.assertIn('cobertura_objetivo', config)
        self.assertIn('costo_unitario', config)
        
        # Verificar que los valores están en rangos razonables
        self.assertTrue(20 <= config['capacidad_diaria'] <= 50)
        self.assertTrue(0.4 <= config['eficiencia_operativa'] <= 0.95)
        self.assertTrue(0.6 <= config['cobertura_objetivo'] <= 1.0)
        self.assertTrue(50000 <= config['costo_unitario'] <= 120000)
    
    def test_evaluar_cumplimiento(self):
        """Prueba la evaluación de cumplimiento."""
        # Ejecutar optimización primero
        self.modelo.optimizar()
        
        # Evaluar cumplimiento
        cumplimiento = self.modelo.evaluar_cumplimiento()
        
        # Verificar estructura
        self.assertIn('detallado', cumplimiento)
        self.assertIn('por_categoria', cumplimiento)
        self.assertIn('global', cumplimiento)
        
        # Verificar que el cumplimiento global es un valor entre 0 y 1
        self.assertTrue(0 <= cumplimiento['global'] <= 1)
        
        # Verificar categorías
        categorias_esperadas = {'cobertura', 'operacion', 'financiero', 'calidad'}
        self.assertEqual(set(cumplimiento['por_categoria'].keys()), categorias_esperadas)
    
    def test_restricciones_optimizacion(self):
        """Prueba las restricciones de optimización."""
        # Establecer restricciones más estrictas
        self.modelo.restricciones = [
            {'tipo': 'cobertura_minima', 'valor': 0.95},
            {'tipo': 'calidad_minima', 'valor': 0.9},
            {'tipo': 'sostenibilidad_minima', 'valor': 0.8}
        ]
        
        # Ejecutar optimización
        resultados = self.modelo.optimizar()
        config = resultados['configuracion']
        
        # Verificar que la cobertura cumple con la restricción
        self.assertGreaterEqual(config['cobertura_objetivo'], 0.95)
        
        # Verificar que la eficiencia (proxy de calidad) cumple con la restricción
        self.assertGreaterEqual(config['eficiencia_operativa'], 0.9)
        
        # La sostenibilidad es más difícil de verificar directamente porque 
        # es una función compleja de múltiples variables, pero deberíamos ver
        # que el modelo intenta aumentar el costo unitario para compensar
        self.assertTrue(config['costo_unitario'] > 70000)
    
    def test_modificar_metas(self):
        """Prueba la modificación de metas y su efecto en los resultados."""
        # Guardar valores originales
        capacidad_original = self.modelo.metas_ideales['operacion']['capacidad_optima']
        costo_original = self.modelo.metas_ideales['financiero']['costo_unitario_max']
        
        # Ejecutar optimización con valores originales
        self.modelo.optimizar()
        resultado_original = self.modelo.resultados['configuracion']['capacidad_diaria']
        
        # Modificar metas
        self.modelo.metas_ideales['operacion']['capacidad_optima'] = capacidad_original * 1.5
        self.modelo.metas_ideales['financiero']['costo_unitario_max'] = costo_original * 0.8
        
        # Ejecutar optimización con nuevos valores
        self.modelo.optimizar()
        resultado_modificado = self.modelo.resultados['configuracion']['capacidad_diaria']
        
        # Verificar que el resultado cambió en la dirección esperada
        # Capacidad óptima mayor debería llevar a capacidad diaria mayor
        self.assertTrue(resultado_modificado > resultado_original)

if __name__ == '__main__':
    unittest.main()