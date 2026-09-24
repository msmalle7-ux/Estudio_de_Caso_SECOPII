"""
Funciones para calcular y clasificar los indicadores
del estudio de caso SECOP II.
"""
# %%

def calcular_indicadores(tabla):
    """
    Calcula los tres indicadores del estudio:

    1. Recurrencia de adjudicaciones.
    2. Concentración por número de contratos.
    3. Concentración por valor adjudicado.

    Retorna una tabla por combinación entidad-proveedor.
    """

    # Resumen por entidad y proveedor
    indicadores = (
        tabla
        .groupby(
            ["codigo_entidad", "proveedor_id"],
            as_index=False
        )
        .agg(
            proveedor=("proveedor_adjudicado", "first"),
            recurrencia=("id_contrato", "count"),
            valor_adjudicado=("valor_del_contrato", "sum")
        )
    )

    # Totales de contratos por entidad
    total_contratos = (
        tabla
        .groupby("codigo_entidad", as_index=False)
        .agg(
            contratos_entidad=("id_contrato", "count")
        )
    )

    # Totales de valor adjudicado por entidad
    total_valor = (
        tabla
        .groupby("codigo_entidad", as_index=False)
        .agg(
            valor_total_entidad=("valor_del_contrato", "sum")
        )
    )

    # Une los totales con la tabla de proveedores
    indicadores = indicadores.merge(
        total_contratos,
        on="codigo_entidad",
        how="left"
    )

    indicadores = indicadores.merge(
        total_valor,
        on="codigo_entidad",
        how="left"
    )

    # Porcentaje de contratos adjudicados al proveedor
    indicadores["concentracion_numero_pct"] = (
        indicadores["recurrencia"]
        / indicadores["contratos_entidad"]
        * 100
    ).round(2)

    # Porcentaje del valor total adjudicado al proveedor
    indicadores["concentracion_valor_pct"] = (
        indicadores["valor_adjudicado"]
        / indicadores["valor_total_entidad"]
        * 100
    ).round(2)

    return indicadores

# %%

def clasificar_prioridad(indicadores):
    """
    Aplica las reglas provisionales de priorización.

    Recurrencia:
        3 o más adjudicaciones.

    Concentración por número:
        50 % o más.

    Concentración por valor:
        50 % o más.

    La recurrencia funciona como condición base.
    """

    indicadores = indicadores.copy()

    indicadores["senal_recurrencia"] = (
        indicadores["recurrencia"] >= 3
    )

    indicadores["senal_concentracion_numero"] = (
        indicadores["concentracion_numero_pct"] >= 50
    )

    indicadores["senal_concentracion_valor"] = (
        indicadores["concentracion_valor_pct"] >= 50
    )

    indicadores["prioridad"] = "Sin prioridad"

    # Recurrencia sin concentración
    indicadores.loc[
        indicadores["senal_recurrencia"],
        "prioridad"
    ] = "Baja"

    # Recurrencia más una señal de concentración
    indicadores.loc[
        indicadores["senal_recurrencia"]
        & (
            indicadores["senal_concentracion_numero"]
            | indicadores["senal_concentracion_valor"]
        ),
        "prioridad"
    ] = "Media"

    # Recurrencia más ambas señales de concentración
    indicadores.loc[
        indicadores["senal_recurrencia"]
        & indicadores["senal_concentracion_numero"]
        & indicadores["senal_concentracion_valor"],
        "prioridad"
    ] = "Alta"

    # Variable contextual: no modifica la prioridad
    indicadores["contexto_volumen"] = "Volumen suficiente"

    indicadores.loc[
        indicadores["contratos_entidad"] < 5,
        "contexto_volumen"
    ] = "Bajo volumen"

    return indicadores

