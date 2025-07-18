"""
Utilidades para configuración de gráficos en la interfaz.
"""

import matplotlib.pyplot as plt

class ConfiguracionGraficos:
    """Clase para configurar aspectos visuales de los gráficos."""
    
    @staticmethod
    def configurar_tema(tema="default"):
        """
        Configura el tema visual para los gráficos.
        
        Args:
            tema: Nombre del tema a utilizar.
        """
        if tema == "dark":
            plt.style.use('dark_background')
        elif tema == "seaborn":
            plt.style.use('seaborn')
        elif tema == "ggplot":
            plt.style.use('ggplot')
        else:
            plt.style.use('default')
    
    @staticmethod
    def configurar_colores_modelo():
        """Retorna los colores para representar cada modelo."""
        return {
            'practico': 'blue',
            'teorico': 'green',
            'brecha': 'red'
        }
    
    @staticmethod
    def ajustar_tamano_fuente(tamano=10):
        """
        Ajusta el tamaño de fuente para todos los gráficos.
        
        Args:
            tamano: Tamaño de fuente base.
        """
        plt.rc('font', size=tamano)          # Tamaño por defecto
        plt.rc('axes', titlesize=tamano+2)    # Títulos de ejes
        plt.rc('axes', labelsize=tamano)      # Etiquetas de ejes
        plt.rc('xtick', labelsize=tamano-1)   # Etiquetas de ticks en x
        plt.rc('ytick', labelsize=tamano-1)   # Etiquetas de ticks en y
        plt.rc('legend', fontsize=tamano-1)   # Leyenda
        plt.rc('figure', titlesize=tamano+4)  # Título de figura
    
    @staticmethod
    def formato_etiquetas_moneda(x, pos):
        """
        Formatea valores numéricos como moneda (COP).
        
        Args:
            x: Valor numérico.
            pos: Posición (requerido por matplotlib).
            
        Returns:
            str: Representación formateada.
        """
        if x >= 1e6:
            return f'${x*1e-6:.1f}M'
        elif x >= 1e3:
            return f'${x*1e-3:.0f}K'
        else:
            return f'${x:.0f}'
    
    @staticmethod
    def formato_etiquetas_porcentaje(x, pos):
        """
        Formatea valores numéricos como porcentaje.
        
        Args:
            x: Valor numérico.
            pos: Posición (requerido por matplotlib).
            
        Returns:
            str: Representación formateada.
        """
        return f'{x*100:.0f}%'