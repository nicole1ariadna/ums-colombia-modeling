"""
Aplicación principal para el Sistema de Modelado de UMS.
Este módulo coordina la ejecución de todos los componentes.
"""

import os
import sys
import tkinter as tk
import matplotlib
matplotlib.use('Agg')  # Para evitar problemas con el backend de matplotlib

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.interfaz_principal import InterfazPrincipal

def main():
    """Función principal que inicia la aplicación."""
    # Crear ventana principal
    root = tk.Tk()
    root.title("Sistema de Modelado de Unidades Móviles de Salud")
    
    # Configurar tamaño y posición
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    ancho_ventana = 1200
    alto_ventana = 800
    x = (ancho_pantalla - ancho_ventana) // 2
    y = (alto_pantalla - alto_ventana) // 2
    root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
    
    # Crear interfaz principal
    app = InterfazPrincipal(root)
    
    # Configurar cierre de ventana
    root.protocol("WM_DELETE_WINDOW", root.quit)
    
    # Iniciar bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()