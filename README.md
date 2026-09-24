# Identificación de señales de priorización en contratación pública - SECOP II

## 1. Descripción del proyecto

Este proyecto desarrolla un análisis exploratorio de contratación pública registrada en SECOP II, orientado a identificar señales de priorización para revisión en procesos de Licitación pública y Licitación pública de obra pública.

El análisis se concentra en la relación entre entidades contratantes y proveedores adjudicados, utilizando indicadores de recurrencia y concentración.

Los resultados corresponden a señales de priorización para revisión y no constituyen evidencia ni confirmación de prácticas colusorias.

---

## 2. Pregunta de análisis

¿Qué combinaciones entidad-proveedor presentan mayores señales de priorización, de acuerdo con la recurrencia de adjudicaciones y la concentración por número de contratos y valor adjudicado, en los registros analizados de SECOP II durante el segundo semestre de 2025?

---

## 3. Alcance de los datos

La base utilizada corresponde a registros disponibles de SECOP II para el segundo semestre de 2025.

El análisis se limita a las siguientes modalidades de contratación:

- Licitación pública.
- Licitación pública Obra Publica.

La base original contiene 445.011 registros y 85 variables.

Para el proyecto se seleccionaron únicamente 10 variables necesarias para el análisis:

- Proceso de Compra.
- ID Contrato.
- Documento Proveedor.
- Proveedor Adjudicado.
- Valor del Contrato.
- Codigo Entidad.
- Nombre Entidad.
- Modalidad de Contratacion.
- Fecha de Firma.
- Departamento.

Después de aplicar el filtro de modalidades se obtuvieron 2.257 contratos.

Para el cálculo de los indicadores, los registros fueron agrupados por entidad y proveedor, obteniendo 2.157 combinaciones entidad-proveedor.

---

## 4. Unidad de análisis

La unidad utilizada para el cálculo de los indicadores es la combinación:

**Entidad + Proveedor**

Esto permite identificar cuántas adjudicaciones recibió un mismo proveedor dentro de una entidad y qué proporción representan frente al total de contratos y al valor total adjudicado por dicha entidad.

---

## 5. Preparación de los datos

El procesamiento incluye las siguientes etapas:

1. Carga de las columnas necesarias del archivo Excel.
2. Normalización de nombres de columnas.
3. Limpieza de espacios en variables de texto.
4. Conversión del código de entidad a tipo texto.
5. Selección de las modalidades incluidas en el estudio.
6. Construcción de un identificador auxiliar del proveedor.
7. Agrupación por entidad y proveedor.
8. Cálculo de los indicadores.
9. Clasificación del nivel de prioridad.

### Identificador auxiliar del proveedor

La variable `proveedor_id` se construyó para evitar que los registros cuyo documento aparece como `No Definido` sean agrupados como si correspondieran a un mismo proveedor.

La regla aplicada es:

- Si existe documento del proveedor: se utiliza el documento.
- Si el documento está vacío o aparece como `No Definido`: se utiliza el nombre normalizado del proveedor.

Esta variable es únicamente un identificador auxiliar para el análisis y no corresponde a un identificador oficial.

---

## 6. Indicadores

Se definieron tres indicadores.

### 6.1. Recurrencia de adjudicaciones

Mide el número de contratos adjudicados a un mismo proveedor dentro de una entidad.

**Fórmula:**

Recurrencia = Número de contratos adjudicados al proveedor dentro de la entidad

Regla provisional:

- Señal de recurrencia: 3 o más adjudicaciones.

---

### 6.2. Concentración por número de contratos

Mide qué proporción de los contratos de una entidad fue adjudicada al proveedor.

**Fórmula:**

Concentración por número (%) =  
(Contratos adjudicados al proveedor / Total de contratos de la entidad) × 100

Regla provisional:

- Señal de concentración por número: 50 % o más.

---

### 6.3. Concentración por valor adjudicado

Mide qué proporción del valor total contratado por una entidad fue adjudicada al proveedor.

**Fórmula:**

Concentración por valor (%) =  
(Valor adjudicado al proveedor / Valor total adjudicado por la entidad) × 100

Regla provisional:

- Señal de concentración por valor: 50 % o más.

---

## 7. Regla de priorización

La recurrencia se utiliza como condición base para continuar con la clasificación.

Las reglas aplicadas son:

- **Sin prioridad:** recurrencia menor a 3.
- **Baja:** recurrencia igual o superior a 3, sin señales de concentración.
- **Media:** recurrencia igual o superior a 3 y al menos una señal de concentración.
- **Alta:** recurrencia igual o superior a 3 y cumplimiento simultáneo de las dos señales de concentración.

La clasificación representa un nivel de prioridad para revisión y no una calificación definitiva de riesgo de colusión.

---

## 8. Contexto de volumen

Se incorporó la variable `contexto_volumen` para apoyar la interpretación de los porcentajes de concentración.

La regla utilizada es:

- Menos de 5 contratos en la entidad: `Bajo volumen`.
- 5 contratos o más: `Volumen suficiente`.

Esta variable no modifica el nivel de prioridad.

Su objetivo es advertir que una concentración elevada calculada sobre pocos contratos debe interpretarse con mayor cautela.

---

## 9. Resultados principales

Se analizaron 2.157 combinaciones entidad-proveedor.

La distribución de recurrencia fue:

- 2.076 combinaciones con 1 adjudicación.
- 65 combinaciones con 2 adjudicaciones.
- 14 combinaciones con 3 adjudicaciones.
- 1 combinación con 4 adjudicaciones.
- 1 combinación con 5 adjudicaciones.

Por tanto, 2.141 combinaciones no alcanzaron el umbral mínimo de recurrencia de tres adjudicaciones.

La clasificación final fue:

- Sin prioridad: 2.141 casos.
- Prioridad baja: 11 casos.
- Prioridad media: 2 casos.
- Prioridad alta: 3 casos.

En total, 16 combinaciones entidad-proveedor cumplieron la condición de recurrencia y fueron priorizadas para revisión.

---

## 10. Verificación del algoritmo

Se construyó un miniarchivo de prueba de 12 registros con resultados conocidos previamente.

El conjunto permitió comprobar:

- El filtro de modalidades.
- La creación del identificador auxiliar del proveedor.
- La recurrencia.
- La concentración por número de contratos.
- La concentración por valor adjudicado.
- La clasificación de prioridad.
- El tratamiento de casos de bajo volumen.

Los resultados esperados fueron comparados con los obtenidos por el algoritmo.

La verificación produjo:

`¿Todas las prioridades coinciden?: True`

Esto confirma que las reglas programadas generaron los resultados esperados para los escenarios de prueba definidos.

---

## 11. Visualizaciones

El análisis incluye tres gráficos elaborados con `seaborn`:

1. Distribución de casos según nivel de prioridad.
2. Relación entre concentración por número de contratos y concentración por valor adjudicado.
3. Recurrencia de adjudicaciones en los casos priorizados.

Los gráficos se encuentran en la carpeta:

`figuras/`

---

## 12. Estructura del proyecto

```text
Actividad5_secop/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── SECOP_II_2025_02.xlsx
│   └── mini_prueba_SECOP.xlsx
│
├── src/
│   ├── procesamiento.py
│   └── indicadores.py
│
├── notebooks/
│   └── analisis_SECOP.ipynb
│
├── figuras/
│   ├── grafico_prioridades.png
│   ├── grafico_concentraciones.png
│   └── grafico_recurrencia.png
│
└── informe/
    └── informe_ejecutivo.pdf