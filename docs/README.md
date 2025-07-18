# Sistema de Modelado de Unidades Móviles de Salud

## Descripción General

Este sistema permite modelar y evaluar la viabilidad y efectividad de las Unidades Móviles de Salud (UMS) en contextos rurales colombianos. Implementa un enfoque dual que combina un modelo práctico basado en datos operativos reales con un modelo teórico fundamentado en indicadores normativos.

## Características Principales

- **Modelo Práctico (Empírico):** Simulación estocástica basada en datos operativos reales
- **Modelo Teórico (Normativo):** Optimización basada en metas ideales y restricciones
- **Análisis de Brechas:** Comparación sistemática entre la realidad operativa y las metas ideales
- **Interfaz Gráfica:** Visualización interactiva de resultados y configuración de parámetros
- **Generación de Informes:** Exportación de resultados y recomendaciones en formato PDF

## Requisitos del Sistema

### Software
- Python 3.9+
- NumPy 1.21+
- Pandas 1.4+
- Matplotlib 3.5+
- Scipy 1.8+
- Tkinter (incluido con Python)
- Reportlab (para generación de informes PDF)

### Hardware
- **Mínimos:** CPU dual-core 2.0 GHz, 4 GB RAM, 1 GB de almacenamiento disponible
- **Recomendados:** CPU quad-core 3.0 GHz, 8 GB RAM, 2 GB de almacenamiento disponible

## Instalación

1. Clone el repositorio:
   ```
   git clone https://github.com/usuario/proyecto_ums.git
   cd proyecto_ums
   ```

2. Instale las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución Rápida

Para iniciar la aplicación:
```
python main.py
```

## Estructura del Proyecto

```
proyecto_ums/
├── main.py                # Punto de entrada principal
├── src/                   # Módulos del sistema
│   ├── modelo_practico.py # Modelo basado en datos reales
│   ├── modelo_teorico.py  # Modelo basado en indicadores normativos
│   ├── simulacion.py      # Algoritmos de simulación
│   ├── optimizacion.py    # Algoritmos de optimización
│   ├── costos.py          # Cálculos financieros
│   ├── indicadores.py     # Métricas de desempeño
│   ├── visualizacion.py   # Generación de gráficos
│   └── analisis_brechas.py # Análisis comparativo
├── gui/                   # Interfaz gráfica
├── data/                  # Datos de configuración
├── tests/                 # Pruebas unitarias e integración
└── docs/                  # Documentación
```

## Documentación

Para mayor información, consulte:
- [Manual de Usuario](manual_usuario.md)
- [Documentación Técnica](documentacion_tecnica.md)

## Licencia

Este proyecto está licenciado bajo los términos de la Licencia MIT. Vea el archivo LICENSE para más detalles.

## Autores

Desarrollado por: nicole1ariadna
Fecha de última actualización: 2025-07-17

## Contacto

Para soporte o consultas, contacte a: nicole1ariadna@github.com