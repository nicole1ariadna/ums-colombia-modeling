# Manual de Usuario - Sistema de Modelado UMS

**Autor:** nicole1ariadna 
**Última actualización:** 2025-07-17

## Índice
1. [Introducción](#introducción)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Interfaz Principal](#interfaz-principal)
4. [Configuración de Modelos](#configuración-de-modelos)
5. [Ejecución de Simulaciones](#ejecución-de-simulaciones)
6. [Visualización de Resultados](#visualización-de-resultados)
7. [Análisis de Brechas](#análisis-de-brechas)
8. [Generación de Informes](#generación-de-informes)
9. [Preguntas Frecuentes](#preguntas-frecuentes)
10. [Solución de Problemas](#solución-de-problemas)

## Introducción

El Sistema de Modelado de Unidades Móviles de Salud (UMS) es una herramienta diseñada para evaluar la viabilidad y efectividad de las UMS en contextos rurales colombianos, utilizando dos enfoques complementarios:

- **Modelo Práctico:** Basado en datos operativos reales extraídos de experiencias documentadas.
- **Modelo Teórico:** Basado en indicadores normativos y metas ideales del sistema de salud.

Este manual le guiará en el uso de todas las funcionalidades del sistema.

## Instalación y Configuración

### Requisitos Previos
- Python 3.9 o superior
- Dependencias listadas en `requirements.txt`

### Pasos de Instalación
1. Descomprima el archivo del programa o clone el repositorio
2. Abra una terminal o línea de comandos
3. Navegue al directorio del proyecto
4. Instale las dependencias:
   ```
   pip install -r requirements.txt
   ```

### Ejecución del Programa
Para iniciar la aplicación, ejecute:
```
python main.py
```

## Interfaz Principal

Al iniciar el programa, verá la interfaz principal que consta de:

1. **Barra de Menú:** Ubicada en la parte superior, contiene opciones para archivo, modelos, informes y ayuda.
2. **Pestañas Principales:** 
   - **Configuración:** Para ajustar parámetros de ambos modelos
   - **Resultados:** Para visualizar los resultados de las simulaciones
   - **Análisis de Brechas:** Para comparar ambos modelos
3. **Barra de Estado:** Ubicada en la parte inferior, muestra mensajes informativos sobre el estado del programa.

## Configuración de Modelos

### Modelo Práctico
En la pestaña de Configuración, seleccione "Modelo Práctico" para ajustar:

1. **Capacidad:**
   - Pacientes por día (10-50)
   - Días operativos al mes (15-26)
   - Eficiencia operativa (0.1-0.9)

2. **Costos:**
   - Costo fijo mensual (COP)
   - Costo variable por paciente (COP)
   - Mantenimiento anual (COP)
   - Costo unitario por atención (COP)
   - Costo del vehículo (COP)

3. **Personal:**
   - Cantidad de médicos, enfermeras y conductores
   - Costo total de personal mensual

4. **Distribución de Servicios:**
   - Porcentaje de consulta general
   - Porcentaje de vacunación
   - Porcentaje de control prenatal

5. **Cobertura:**
   - Población objetivo
   - Frecuencia de visitas por mes
   - Radio de cobertura (km)
   - Densidad poblacional (hab/km²)

6. **Parámetros de Simulación:**
   - Número de simulaciones
   - Horizonte temporal (meses)

### Modelo Teórico
Seleccione "Modelo Teórico" para ajustar:

1. **Metas de Cobertura:**
   - Población objetivo (proporción)
   - Frecuencia de visitas
   - Tiempo máximo de acceso (minutos)
   - Satisfacción mínima

2. **Metas de Operación:**
   - Capacidad óptima (pacientes/día)
   - Eficiencia operativa
   - Resolución en primer nivel
   - Tiempo de espera máximo (minutos)

3. **Metas Financieras:**
   - Costo unitario máximo (COP)
   - Sostenibilidad mínima
   - Autofinanciación

4. **Metas de Calidad:**
   - Continuidad de atención
   - Integración con historia clínica
   - Referencia efectiva

5. **Restricciones de Optimización:**
   - Cobertura mínima
   - Calidad mínima
   - Sostenibilidad mínima

## Ejecución de Simulaciones

### Ejecutar el Modelo Práctico
1. Configure los parámetros deseados
2. Haga clic en "Ejecutar Modelo Práctico" en la parte inferior de la pestaña de Configuración
3. Espere a que la simulación termine
4. El sistema cambiará automáticamente a la pestaña de Resultados

### Ejecutar el Modelo Teórico
1. Configure las metas y restricciones deseadas
2. Haga clic en "Ejecutar Modelo Teórico" en la parte inferior
3. Espere a que la optimización termine
4. El sistema cambiará automáticamente a la pestaña de Resultados

## Visualización de Resultados

### Resultados del Modelo Práctico
En la pestaña "Resultados", seleccione "Modelo Práctico" para ver:

1. **Gráficos:**
   - Distribución de demanda mensual
   - Relación entre demanda y costos
   - Relación entre cobertura y sostenibilidad
   - Dashboard con indicadores clave

2. **Estadísticas:**
   - Tabla con media, mediana, desviación estándar y percentiles
   - Detalle de costos (fijos, variables, personal, etc.)

### Resultados del Modelo Teórico
Seleccione "Modelo Teórico" para ver:

1. **Configuración Óptima:**
   - Capacidad diaria óptima
   - Eficiencia operativa
   - Cobertura objetivo
   - Costo unitario

2. **Estadísticas Derivadas:**
   - Atenciones mensuales estimadas
   - Población cubierta
   - Número de UMS requeridas por 100,000 habitantes
   - Costos mensuales y por habitante

3. **Cumplimiento de Metas:**
   - Porcentaje de cumplimiento por categoría
   - Cumplimiento global

## Análisis de Brechas

Para realizar un análisis comparativo entre ambos modelos:

1. Ejecute ambos modelos (práctico y teórico)
2. Seleccione la pestaña "Análisis de Brechas"
3. Examine:
   - **Matriz de Brechas:** Muestra las diferencias entre valores reales e ideales
   - **Gráficos Comparativos:** Visualización de la comparación
   - **Recomendaciones Prioritarias:** Sugerencias para mejorar indicadores críticos

Las recomendaciones se clasifican por prioridad (Alta, Media, Baja) y se enfocan en los indicadores con mayores brechas.

## Generación de Informes

Para generar informes de los resultados:

1. Vaya al menú "Informes"
2. Seleccione:
   - **Generar Informe Completo:** Crea un PDF con todos los resultados y análisis
   - **Exportar Gráficos:** Guarda todos los gráficos generados como imágenes PNG

Al seleccionar "Generar Informe Completo", deberá:
1. Elegir la ubicación donde guardar el archivo PDF
2. Esperar a que el sistema genere el informe
3. El sistema mostrará un mensaje cuando el informe esté listo

## Preguntas Frecuentes

**P: ¿Puedo guardar mis configuraciones para uso futuro?**
R: Sí, use la opción "Guardar configuración" en el menú Archivo.

**P: ¿Qué significa el ratio de sostenibilidad?**
R: Es la relación entre ingresos y costos. Un valor mayor a 1 indica que los ingresos superan los costos.

**P: ¿Cómo interpreto las brechas negativas?**
R: Una brecha negativa significa que el valor real está por debajo del ideal (excepto en indicadores donde menos es mejor, como costos).

**P: ¿Puedo usar datos de diferentes regiones?**
R: Sí, los parámetros regionales están disponibles en el archivo de configuración regional.

## Solución de Problemas

### El programa no inicia
- Verifique que Python 3.9 o superior esté instalado
- Confirme que todas las dependencias estén instaladas
- Compruebe permisos de escritura en el directorio

### Error al ejecutar simulaciones
- Asegúrese de que los valores ingresados estén dentro de los rangos permitidos
- Evite valores extremos (demasiado grandes o pequeños)
- Revise que la suma de porcentajes de servicios sea 100%

### Problemas con los gráficos
- Actualice matplotlib a la última versión
- Asegúrese de tener un backend gráfico compatible

### Errores al generar informes PDF
- Verifique que reportlab esté instalado
- Compruebe permisos de escritura en el directorio destino

Si persisten los problemas, contacte al soporte técnico.