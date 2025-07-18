# Documentación Técnica - Sistema de Modelado UMS

**Autor:** nicole1ariadna  
**Última actualización:** 2025-07-17

## Índice
1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Descripción de Módulos](#descripción-de-módulos)
3. [Modelos Matemáticos](#modelos-matemáticos)
4. [Estructura de Datos](#estructura-de-datos)
5. [Interfaces y API](#interfaces-y-api)
6. [Algoritmos Principales](#algoritmos-principales)
7. [Visualización de Datos](#visualización-de-datos)
8. [Testing y Validación](#testing-y-validación)
9. [Guía de Extensibilidad](#guía-de-extensibilidad)
10. [Consideraciones Técnicas](#consideraciones-técnicas)

## Arquitectura del Sistema

El sistema sigue una arquitectura modular con separación clara entre la lógica de negocio (modelos de simulación y optimización) y la presentación (interfaz gráfica). Los principales componentes son:

### Componentes Principales
- **Módulo de Modelos (src/)**: Implementa la lógica de negocio con los modelos práctico y teórico.
- **Módulo de Interfaz (gui/)**: Implementa la interfaz gráfica usando Tkinter.
- **Módulo de Datos (data/)**: Almacena configuraciones y parámetros en formato JSON.
- **Módulo de Testing (tests/)**: Contiene pruebas unitarias y de integración.
- **Módulo de Documentación (docs/)**: Contiene documentación técnica y de usuario.

### Diagrama de Componentes
```
┌─────────────────┐     ┌─────────────────┐
│    Interfaz     │◄───►│     Modelos     │
│    Gráfica      │     │                 │
│    (Tkinter)    │     │ Práctico/Teórico│
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Visualización  │     │  Simulación y   │
│    (Gráficos)   │     │   Optimización  │
└─────────────────┘     └─────────────────┘
         ▲                       ▲
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
               ┌──────────┐
               │  Datos   │
               │  (JSON)  │
               └──────────┘
```

### Flujo de Control
1. El usuario configura parámetros en la interfaz
2. La interfaz invoca métodos en los modelos
3. Los modelos ejecutan simulaciones/optimizaciones
4. Los resultados se procesan y visualizan
5. Opcionalmente se genera análisis de brechas y reportes

## Descripción de Módulos

### Directorio `src/`

#### `modelo_practico.py`
Implementa la clase `UMSPractico` que maneja la simulación basada en datos operativos reales.

**Clases principales:**
- `UMSPractico`: Encapsula toda la lógica del modelo práctico.

**Métodos clave:**
- `simular()`: Ejecuta simulación Monte Carlo para estimar indicadores.
- `calcular_costos()`: Calcula detalles de costos operativos.
- `generar_reportes()`: Crea visualizaciones y resumenes estadísticos.

#### `modelo_teorico.py`
Implementa la clase `UMSTeorico` que maneja la optimización basada en metas normativas.

**Clases principales:**
- `UMSTeorico`: Encapsula toda la lógica del modelo teórico.

**Métodos clave:**
- `optimizar()`: Encuentra configuración óptima según restricciones.
- `evaluar_cumplimiento()`: Evalúa cumplimiento vs metas ideales.
- `cargar_metas()`: Carga metas desde archivo JSON.

#### `simulacion.py`
Contiene algoritmos de simulación estocástica para el modelo práctico.

**Funciones principales:**
- `generar_demanda_diaria()`: Genera demanda usando distribución Poisson.
- `calcular_tiempo_atencion()`: Estima tiempo usando distribución exponencial.
- `analisis_sensibilidad()`: Evalúa efectos de variación en parámetros.

#### `optimizacion.py`
Contiene algoritmos de optimización para el modelo teórico.

**Funciones principales:**
- `funcion_objetivo()`: Define función a minimizar.
- `restriccion_*()`: Define restricciones para la optimización.
- `optimizar_configuracion_ums()`: Ejecuta algoritmo de optimización.

#### `costos.py`
Implementa cálculos financieros para ambos modelos.

**Funciones principales:**
- `calcular_costos_totales()`: Suma costos fijos y variables.
- `calcular_punto_equilibrio()`: Determina punto de equilibrio financiero.
- `analizar_sostenibilidad()`: Evalúa sostenibilidad financiera.
- `calcular_flujo_caja()`: Proyecta flujos financieros a futuro.

#### `indicadores.py`
Implementa cálculo de indicadores de desempeño.

**Funciones principales:**
- `calcular_indices_desempeno()`: Calcula índices basados en configuración.
- `calcular_indice_equidad()`: Calcula índice de equidad (Gini).
- `evaluar_impacto_salud()`: Estima impacto en indicadores de salud.

#### `visualizacion.py`
Implementa funciones para generar gráficos y visualizaciones.

**Funciones principales:**
- `generar_graficos_practico()`: Crea gráficos para modelo práctico.
- `generar_graficos_teorico()`: Crea gráficos para modelo teórico.
- `generar_graficos_comparativos()`: Crea gráficos comparativos.

#### `analisis_brechas.py`
Implementa análisis comparativo entre modelos.

**Clases principales:**
- `AnalisisBrechas`: Analiza diferencias entre valores reales e ideales.

**Métodos clave:**
- `comparar_modelos()`: Calcula brechas entre modelos.
- `generar_recomendaciones()`: Sugiere mejoras basadas en brechas.

### Directorio `gui/`

#### `interfaz_principal.py`
Implementa la ventana principal y coordinación de la interfaz.

**Clases principales:**
- `InterfazPrincipal`: Coordina toda la interfaz gráfica.

#### `paneles/*.py`
Implementa paneles específicos de la interfaz.

**Archivos principales:**
- `configuracion.py`: Panel para configurar modelos.
- `resultados.py`: Panel para mostrar resultados.
- `brechas.py`: Panel para análisis de brechas.

#### `utils/*.py`
Utilidades para la interfaz gráfica.

**Archivos principales:**
- `graficos.py`: Configuración de gráficos.
- `reportes.py`: Generación de informes PDF.

### Archivo Principal `main.py`
Punto de entrada del sistema, inicializa la interfaz gráfica.

## Modelos Matemáticos

### Modelo Práctico (Empírico)

#### Simulación de Demanda
La demanda diaria se modela mediante una distribución de Poisson:

```
D ~ Poisson(λ)
```

donde λ es el número promedio de pacientes por día.

#### Tiempo de Atención
El tiempo de atención sigue una distribución exponencial:

```
T ~ Exp(1/μ)
```

donde μ es el tiempo promedio de atención.

#### Capacidad Efectiva
La capacidad efectiva diaria se calcula como:

```
CE = P * E * H
```

donde:
- P = Pacientes por día (capacidad nominal)
- E = Eficiencia operativa
- H = Horas operativas por día

#### Costos Totales
Los costos totales mensuales se calculan como:

```
CT = CF + (CV * A)
```

donde:
- CF = Costos fijos mensuales
- CV = Costo variable por atención
- A = Número de atenciones mensuales

#### Sostenibilidad
El ratio de sostenibilidad se calcula como:

```
S = I / CT
```

donde:
- I = Ingresos totales
- CT = Costos totales

### Modelo Teórico (Normativo)

#### Función Objetivo de Optimización
La función a minimizar es:

```
f(x) = w_1 * c(x) + w_2 * p(x)
```

donde:
- c(x) = Costo normalizado
- p(x) = Penalización por desviación de metas
- w_1, w_2 = Pesos de importancia

#### Restricciones
Las principales restricciones son:

```
g_1(x) = cobertura(x) - cobertura_min ≥ 0
g_2(x) = calidad(x) - calidad_min ≥ 0
g_3(x) = sostenibilidad(x) - sostenibilidad_min ≥ 0
```

#### Cálculo de Brechas
La brecha porcentual se calcula como:

```
B = (V_real - V_ideal) / V_ideal
```

donde:
- V_real = Valor real (modelo práctico)
- V_ideal = Valor ideal (modelo teórico)

## Estructura de Datos

### Modelo Práctico

#### Datos Operativos
```python
datos_operativos = {
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
        'poblacion_objetivo': 10000,
        'frecuencia_visitas': 1,
        'radio_cobertura': 50,
        'poblacion_por_km2': 15
    }
}
```

#### Resultados de Simulación
```python
resultados = {
    'demanda': [...],  # Lista de valores de demanda de cada simulación
    'costos': [...],   # Lista de valores de costos de cada simulación
    'cobertura': [...], # Lista de valores de cobertura de cada simulación
    'sostenibilidad': [...], # Lista de valores de sostenibilidad de cada simulación
    'estadisticas': {
        'demanda': {
            'media': valor,
            'mediana': valor,
            'desviacion': valor,
            'min': valor,
            'max': valor,
            'percentil_25': valor,
            'percentil_75': valor
        },
        # Similar para costos, cobertura, sostenibilidad
    }
}
```

### Modelo Teórico

#### Metas Ideales
```python
metas_ideales = {
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
        'costo_unitario_max': 80000,
        'sostenibilidad_min': 0.6,
        'autofinanciacion': 0.6
    },
    'calidad': {
        'continuidad_atencion': 0.85,
        'integracion_historia': 1.0,
        'referencia_efectiva': 0.9
    }
}
```

#### Resultados de Optimización
```python
resultados = {
    'configuracion': {
        'capacidad_diaria': valor,
        'eficiencia_operativa': valor,
        'cobertura_objetivo': valor,
        'costo_unitario': valor
    },
    'indicadores': {
        'cobertura': {...},
        'operacion': {...},
        'financiero': {...},
        'calidad': {...}
    },
    'estadisticas': {
        'atenciones_mensuales': valor,
        'poblacion_cubierta': valor,
        'ums_requeridas_100k': valor,
        'costo_total_mensual': valor,
        'costo_por_habitante_mes': valor
    }
}
```

### Análisis de Brechas

#### Matriz de Brechas
```python
matriz_brechas = {
    'cobertura': {
        'real': valor,
        'ideal': valor,
        'brecha': valor,
        'prioridad': 'Alta'
    },
    'costo_efectividad': {
        'real': valor,
        'ideal': valor,
        'brecha': valor,
        'prioridad': 'Media'
    },
    # Similar para sostenibilidad, eficiencia
}
```

## Interfaces y API

### Clase UMSPractico

```python
class UMSPractico:
    def __init__(self)
    def cargar_datos(self, ruta_archivo=None) -> bool
    def simular(self) -> dict
    def calcular_costos(self) -> dict
    def generar_reportes(self) -> dict
```

### Clase UMSTeorico

```python
class UMSTeorico:
    def __init__(self)
    def cargar_metas(self, ruta_archivo=None) -> bool
    def optimizar(self) -> dict
    def evaluar_cumplimiento(self) -> dict
```

### Clase AnalisisBrechas

```python
class AnalisisBrechas:
    def __init__(self, modelo_practico, modelo_teorico)
    def comparar_modelos(self) -> dict
    def calcular_brecha_porcentual(self, valor_real, valor_ideal, menor_mejor=False) -> float
    def generar_recomendaciones(self) -> list
```

### Clase InterfazPrincipal

```python
class InterfazPrincipal:
    def __init__(self, root)
    def ejecutar_modelo_practico()
    def ejecutar_modelo_teorico()
    def comparar_modelos()
    def generar_informe()
    def exportar_graficos()
```

## Algoritmos Principales

### Algoritmo de Simulación Monte Carlo

```python
def simular_operacion(parametros, horizonte_temporal):
    resultados_mensuales = {...}
    
    for mes in range(horizonte_temporal):
        demanda_mensual = 0
        
        # Simulación diaria
        for dia in range(dias_mes):
            # Generar demanda diaria aleatoria
            demanda_diaria = generar_demanda_diaria(capacidad_diaria)
            
            # Limitar por capacidad real
            atenciones_reales = min(demanda_diaria, capacidad_diaria * eficiencia)
            demanda_mensual += atenciones_reales
        
        # Calcular métricas mensuales
        costos_mes = calcular_costos_totales(...)
        cobertura = calcular_cobertura(...)
        sostenibilidad = calcular_sostenibilidad(...)
        
        # Almacenar resultados
        resultados_mensuales['demanda'].append(demanda_mensual)
        resultados_mensuales['costos'].append(costos_mes)
        resultados_mensuales['cobertura'].append(cobertura)
        resultados_mensuales['sostenibilidad'].append(sostenibilidad)
    
    return resultados_mensuales
```

### Algoritmo de Optimización

```python
def optimizar_configuracion_ums(x0, metas_ideales, restricciones):
    # Definir función objetivo
    def funcion_objetivo(x):
        # Desempacar variables
        capacidad_diaria = x[0]
        eficiencia_operativa = x[1]
        cobertura_objetivo = x[2]
        costo_unitario = x[3]
        
        # Calcular penalizaciones
        penalizacion_capacidad = ...
        penalizacion_eficiencia = ...
        penalizacion_cobertura = ...
        penalizacion_costo = ...
        
        # Función objetivo ponderada
        return w_costo * costo_normalizado + w_penalizacion * penalizacion_total
    
    # Convertir restricciones
    constraints = []
    for restriccion in restricciones:
        if restriccion['tipo'] == 'cobertura_minima':
            constraints.append(...)
        # Más restricciones...
    
    # Definir límites
    bounds = [
        (20, 50),      # capacidad_diaria
        (0.4, 0.95),   # eficiencia_operativa
        (0.6, 1.0),    # cobertura_objetivo
        (50000, 120000) # costo_unitario
    ]
    
    # Ejecutar optimización
    result = minimize(
        fun=funcion_objetivo,
        x0=x0,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
    
    return result
```

### Algoritmo de Análisis de Brechas

```python
def evaluar_brechas():
    # Extraer datos del modelo práctico
    cobertura_real = modelo_practico.resultados['estadisticas']['cobertura']['media']
    # Más datos...
    
    # Extraer datos del modelo teórico
    cobertura_ideal = modelo_teorico.resultados['configuracion']['cobertura_objetivo']
    # Más datos...
    
    # Calcular brechas
    brechas = {
        'cobertura': {
            'real': cobertura_real,
            'ideal': cobertura_ideal,
            'brecha': calcular_brecha_porcentual(cobertura_real, cobertura_ideal),
            'prioridad': 'Alta'
        },
        # Más indicadores...
    }
    
    # Asignar prioridades
    for indicador, datos in brechas.items():
        if abs(datos['brecha']) > 0.5:
            brechas[indicador]['prioridad'] = 'Alta'
        elif abs(datos['brecha']) > 0.2:
            brechas[indicador]['prioridad'] = 'Media'
        else:
            brechas[indicador]['prioridad'] = 'Baja'
    
    return brechas
```

## Visualización de Datos

### Gráficos del Modelo Práctico

1. **Distribución de Demanda:**
   - Histograma de demanda mensual con línea de media
   
2. **Relación Costos vs Demanda:**
   - Gráfico de dispersión con línea de tendencia

3. **Sostenibilidad vs Cobertura:**
   - Gráfico de dispersión con código de color por costos
   
4. **Dashboard:**
   - Panel con 4 gráficos principales: demanda, costos, cobertura y sostenibilidad

### Gráficos del Modelo Teórico

1. **Configuración Óptima:**
   - Gráfico de barras con los valores óptimos
   
2. **Cumplimiento por Categoría:**
   - Gráfico de radar con el nivel de cumplimiento

3. **Estadísticas:**
   - Gráfico de barras con indicadores estadísticos clave

### Gráficos Comparativos

1. **Comparación de Indicadores:**
   - Gráfico de barras agrupadas que compara valores reales vs ideales
   
2. **Radar Comparativo:**
   - Gráfico radar que compara ambos modelos en múltiples dimensiones

## Testing y Validación

### Pruebas Unitarias

Se implementan pruebas para componentes individuales:

1. **Test del Modelo Práctico:**
   - Inicialización correcta
   - Simulación dentro de rangos esperados
   - Cálculo correcto de costos
   - Comportamiento ante cambio de parámetros
   - Manejo de valores inválidos

2. **Test del Modelo Teórico:**
   - Inicialización correcta
   - Optimización con restricciones
   - Evaluación de cumplimiento
   - Efecto de cambios en metas

### Pruebas de Integración

Se implementan pruebas del flujo completo:

1. **Flujo Completo:**
   - Ejecución secuencial de todos los componentes
   - Verificación de resultados intermedios y finales
   
2. **Generación de Gráficos:**
   - Generación correcta de todos los tipos de gráficos
   
3. **Configuración:**
   - Guardar y cargar configuraciones

### Validación

1. **Validación de Datos:**
   - Verificación de rangos y tipos
   - Consistencia interna

2. **Validación de Modelos:**
   - Comparación con casos conocidos
   - Verificación de tendencias esperadas
   - Análisis de sensibilidad

## Guía de Extensibilidad

### Añadir Nuevos Indicadores

Para agregar un nuevo indicador al sistema:

1. Añadir el indicador a la estructura de datos correspondiente:
   - `datos_operativos` (modelo práctico)
   - `metas_ideales` (modelo teórico)

2. Implementar función de cálculo en el módulo apropiado:
   - `indicadores.py` para indicadores de desempeño
   - `costos.py` para indicadores financieros

3. Modificar algoritmos de simulación/optimización:
   - Incluir el nuevo indicador en los cálculos
   - Ajustar funciones objetivo o restricciones si es necesario

4. Actualizar visualización:
   - Añadir el indicador a los gráficos relevantes
   - Incluir en tablas de resultados

5. Actualizar análisis de brechas:
   - Incluir el indicador en la matriz de brechas
   - Ajustar lógica de recomendaciones

### Implementar Nuevas Regiones

Para añadir soporte para nuevas regiones:

1. Añadir datos regionales a `parametros_regionales.json`:
```json
"nueva_region": {
    "nombre": "Nombre de la Región",
    "departamentos": ["Dep1", "Dep2", ...],
    "parametros": {
        "poblacion_por_km2": valor,
        "tiempo_desplazamiento_promedio": valor,
        // Más parámetros...
    }
}
```

2. Implementar lógica de selección regional en la interfaz:
   - Añadir la región al selector de regiones
   - Implementar carga de parámetros específicos

3. Ajustar factores de corrección regional:
   - Modificar algoritmos para considerar características específicas

### Añadir Nuevos Tipos de Gráficos

Para implementar nuevos gráficos:

1. Añadir función de generación en `visualizacion.py`:
```python
def generar_grafico_nuevo(datos):
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    # Lógica de generación del gráfico
    return fig
```

2. Integrar con la función correspondiente:
   - `generar_graficos_practico()`
   - `generar_graficos_teorico()`
   - `generar_graficos_comparativos()`

3. Actualizar la interfaz para mostrar el nuevo gráfico:
   - Añadir pestaña o panel en el módulo de resultados

## Consideraciones Técnicas

### Rendimiento

1. **Optimizaciones de Simulación:**
   - Las simulaciones pesadas utilizan NumPy para vectorizar operaciones
   - El número de simulaciones se puede ajustar según capacidad de hardware
   - Considerar reducir para equipos de menor capacidad

2. **Generación de Gráficos:**
   - Se utiliza el backend 'Agg' para evitar bloqueo de la interfaz
   - Los gráficos se renderizan una vez y se almacenan

3. **Interfaz Gráfica:**
   - Operaciones pesadas se ejecutan en hilos separados para evitar congelamiento
   - Se implementan indicadores de progreso para operaciones largas

### Limitaciones Conocidas

1. **Simulación:**
   - No considera factores estacionales o epidémicos
   - Asume homogeneidad en la demanda de servicios

2. **Optimización:**
   - Puede converger a mínimos locales
   - Tiempo de ejecución aumenta con complejidad de restricciones

3. **Datos:**
   - Basados en fuentes limitadas y específicas
   - Pueden no representar toda la variabilidad regional

### Seguridad y Privacidad

1. **Datos Sensibles:**
   - El sistema no maneja datos personales ni clínicos
   - Todos los datos son agregados y anónimos

2. **Persistencia:**
   - Los archivos de configuración se almacenan localmente
   - No se envían datos a servidores externos

### Requisitos del Entorno de Desarrollo

1. **Python:**
   - Python 3.9 o superior
   - Entorno virtual recomendado

2. **Dependencias Principales:**
   - NumPy, Pandas, Matplotlib
   - SciPy, Tkinter
   - Reportlab

3. **Herramientas de Desarrollo:**
   - VS Code con extensión Python recomendada
   - Git para control de versiones
   - pytest para pruebas

Esta documentación técnica proporciona una visión completa del sistema para desarrolladores que deseen mantener, extender o modificar el sistema de modelado UMS.