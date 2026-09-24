# %%
"""
Funciones de preparación de datos para el análisis de SECOP II.

Incluye:
- carga del archivo
- limpieza básica
- filtro de modalidades
- creación del identificador del proveedor
"""
# %%
import pandas as pd

# %%
def cargar_datos(ruta):
    """
    Carga únicamente las columnas necesarias del archivo Excel.
    Parámetros
    ----------
    ruta : str
        Ruta del archivo de datos.

    Retorna
    -------
    DataFrame
        Tabla con las variables requeridas para el análisis.
    """

    columnas = [
        "Proceso de Compra",
        "ID Contrato",
        "Documento Proveedor",
        "Proveedor Adjudicado",
        "Valor del Contrato",
        "Codigo Entidad",
        "Nombre Entidad",
        "Modalidad de Contratacion",
        "Fecha de Firma",
        "Departamento"
    ]

    tabla = pd.read_excel(
        ruta,
        usecols=columnas
    )
    return tabla

# %%
def limpiar_datos(tabla):
    """
    Limpia nombres de columnas y campos de texto.
    Se trabaja sobre una copia para conservar intacta la tabla original.
    """

    tabla = tabla.copy()

    # Normaliza los nombres de las columnas
    tabla.columns = (
        tabla.columns
        .str.strip()
        .str.lower()
        .str.normalize("NFKD")
        .str.encode("ascii", "ignore")
        .str.decode("utf-8")
        .str.replace(" ", "_", regex=False)
    )

    # Los códigos se manejan como texto porque son identificadores
    tabla["codigo_entidad"] = (
        tabla["codigo_entidad"].astype("string")
    )

    columnas_texto = [
        "nombre_entidad",
        "departamento",
        "proceso_de_compra",
        "id_contrato",
        "modalidad_de_contratacion",
        "documento_proveedor",
        "proveedor_adjudicado",
        "codigo_entidad"
    ]

    # Elimina espacios innecesarios en variables de texto
    for columna in columnas_texto:
        tabla[columna] = tabla[columna].str.strip()

    return tabla

# %%
def filtrar_modalidades(tabla):
    """
    Conserva únicamente las modalidades incluidas en el alcance del estudio.
    """

    modalidades = [
        "Licitación pública",
        "Licitación pública Obra Publica"
    ]

    resultado = tabla[
        tabla["modalidad_de_contratacion"].isin(modalidades)
    ].copy()

    return resultado

# %%
def preparar_proveedor(tabla):
    """
    Construye un identificador auxiliar del proveedor.

    Cuando existe documento se utiliza ese identificador.
    Si el documento está vacío o aparece como 'No Definido',
    se utiliza el nombre normalizado del proveedor.
    """

    tabla = tabla.copy()

    tabla["proveedor_id"] = (
        "DOC_" + tabla["documento_proveedor"].astype("string")
    )

    sin_documento = (
        tabla["documento_proveedor"].isna()
        | (tabla["documento_proveedor"] == "No Definido")
    )

    tabla.loc[sin_documento, "proveedor_id"] = (
        "NOM_"
        + tabla.loc[
            sin_documento,
            "proveedor_adjudicado"
        ]
        .str.strip()
        .str.upper()
    )

    return tabla



# %%
