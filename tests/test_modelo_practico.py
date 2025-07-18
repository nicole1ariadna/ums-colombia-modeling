"""
Pruebas unitarias para el módulo modelo_practico.py
"""

import sys
import os
import unittest
import numpy as np

# Añadir directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modelo_practico import UMSPractico

class TestModeloPractico(unittest.TestCase):
    """Clase para probar el funcionamiento del modelo práctico."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.modelo = UMSPractico()
        
        # Establecer parámetros de simulación más pequeños para pruebas
        self.modelo.parametros_simulacion = {
            'num_simulaciones': 10,
            'horizonte_temporal': 12  # meses
        }
    
    def test_inicializacion(self):
        """Prueba la inicialización correcta del modelo."""
        # Verificar estructura de datos
        self.assertIsInstance(self.modelo.datos_operativos, dict)
        
        # Verificar valores predeterminados
        self.assertEqual(self.modelo.datos_operativos['capacidad']['pacientes_dia'], 24)
        self.assertEqual(self.modelo.datos_operativos['capacidad']['dias_mes'], 20)
        self.assertEqual(self.modelo.datos_operativos['capacidad']['eficiencia'], 0.4)
    
    def test_simulacion(self):
        """Prueba la ejecución de la simulación."""
        # Ejecutar simulación
        resultados = self.modelo.simular()
        
        # Verificar que se generaron resultados
        self.assertIsNotNone(resultados)
        self.assertIn('estadisticas', resultados)
        self.assertIn('demanda', resultados['estadisticas'])
        self.assertIn('costos', resultados['estadisticas'])
        self.assertIn('cobertura', resultados['estadisticas'])
        self.assertIn('sostenibilidad', resultados['estadisticas'])
        
        # Verificar que la demanda media está en un rango razonable
        demanda_media = resultados['estadisticas']['demanda']['media']
        demanda_esperada = self.modelo.datos_operativos['capacidad']['pacientes_dia'] * \
                          self.modelo.datos_operativos['capacidad']['eficiencia'] * \
                          self.modelo.datos_operativos['capacidad']['dias_mes']
        
        # Permitir variación de ±30% debido a la naturaleza estocástica
        self.assertTrue(0.7 * demanda_esperada <= demanda_media <= 1.3 * demanda_esperada)
    
    def test_calcular_costos(self):
        """Prueba el cálculo de costos."""
        # Ejecutar simulación primero
        self.modelo.simular()
        
        # Calcular costos
        costos = self.modelo.calcular_costos()
        
        # Verificar estructura de costos
        self.assertIn('fijos', costos)
        self.assertIn('variables', costos)
        self.assertIn('personal', costos)
        self.assertIn('depreciacion', costos)
        self.assertIn('mantenimiento', costos)
        self.assertIn('total_mensual', costos)
        self.assertIn('costo_por_atencion', costos)
        
        # Verificar cálculos
        self.assertEqual(costos['fijos'], self.modelo.datos_operativos['costos']['fijo_mensual'])
        self.assertEqual(costos['personal'], self.modelo.datos_operativos['personal']['costo_personal_mes'])
        
        # Total debe ser suma de componentes
        total_calculado = costos['fijos'] + costos['variables'] + costos['personal'] + \
                          costos['depreciacion'] + costos['mantenimiento']
        self.assertAlmostEqual(costos['total_mensual'], total_calculado)
    
    def test_modificar_parametros(self):
        """Prueba la modificación de parámetros y su efecto en los resultados."""
        # Guardar valores originales
        pacientes_dia_original = self.modelo.datos_operativos['capacidad']['pacientes_dia']
        eficiencia_original = self.modelo.datos_operativos['capacidad']['eficiencia']
        
        # Ejecutar simulación con valores originales
        self.modelo.simular()
        resultado_original = self.modelo.resultados['estadisticas']['demanda']['media']
        
        # Modificar parámetros
        self.modelo.datos_operativos['capacidad']['pacientes_dia'] = pacientes_dia_original * 2
        self.modelo.datos_operativos['capacidad']['eficiencia'] = min(1.0, eficiencia_original * 1.5)
        
        # Ejecutar simulación con nuevos valores
        self.modelo.simular()
        resultado_modificado = self.modelo.resultados['estadisticas']['demanda']['media']
        
        # Verificar que el resultado cambió proporcionalmente
        # (no exactamente porque hay aleatoriedad)
        factor_esperado = 2 * min(1.0, eficiencia_original * 1.5) / eficiencia_original
        self.assertTrue(resultado_modificado > resultado_original)
        self.assertTrue(resultado_modificado < resultado_original * factor_esperado * 1.3)  # Con margen
    
    def test_valores_invalidos(self):
        """Prueba el comportamiento con valores inválidos."""
        # Establecer eficiencia negativa (no debería afectar el funcionamiento)
        self.modelo.datos_operativos['capacidad']['eficiencia'] = -0.1
        
        # La simulación debería ejecutarse sin errores usando un valor efectivo de 0
        self.modelo.simular()
        
        # Verificar que no hay resultados negativos
        self.assertGreaterEqual(self.modelo.resultados['estadisticas']['demanda']['media'], 0)
        self.assertGreaterEqual(self.modelo.resultados['estadisticas']['costos']['media'], 0)
        self.assertGreaterEqual(self.modelo.resultados['estadisticas']['cobertura']['media'], 0)
        self.assertGreaterEqual(self.modelo.resultados['estadisticas']['sostenibilidad']['media'], 0)

if __name__ == '__main__':
    unittest.main()