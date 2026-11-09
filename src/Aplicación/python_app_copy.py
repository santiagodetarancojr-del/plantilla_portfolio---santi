import pandas as pd
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Sistema de Reservas - Robótica", page_icon="🤖", layout="wide"
)


# Cargar el inventario desde el CSV o usar la estructura inicial como respaldo
@st.cache_data
def cargar_inventario():
  try:
    df = pd.read_csv("inventario_robotica.csv")
    return dict(zip(df["nombre"], df["cantidad"]))
  except Exception:
    # Diccionario de respaldo por si no localiza el archivo CSV
    return {
        "Pack aula Bee-Bot": 4,
        "Tapete Bee-Bot transparente": 3,
        "LEGO Coding Express": 4,
        "Codificación MatataStudio": 6,
        "Codey Rocky": 4,
        "LEGO Education Science 6.º Primaria–2.º ESO": 16,
        "Invernadero inteligente (10 unidades)": 12,
        "Micro:bit Club V2": 12,
        "Bambu Lab P2S": 1,
        "HuskyLens Pro": 3,
        "Maqueen + Micro:bit": 25,
        "Kit Arduino Sensor": 20,
        "Kit de inicio Raspberry Pi 5 8 GB": 6,
        "xTool M1": 1,
        "xTool Desktop": 1,
        "Starter Set Kubo Coding": 24,
        "Classroom Kit Tale Bot Pro": 2,
        "Casa DoCasa Domótica Micro:bit": 15,
        "Coche inteligente 45 piezas": 15,
    }


INVENTARIO = cargar_inventario()

# Inicializar la lista de reservas en la memoria de sesión
if "reservas" not in st.session_state:
  st.session_state.reservas = []

st.title("🤖 Reserva de Material de Informática y Robótica")
st.write(
    "Selecciona el material, la fecha y la sesión lectiva para realizar o"
    " consultar tus reservas."
)

# Estructura en pestañas para organizar la interfaz
tab_reservar, tab_gestion = st.tabs(
    ["📝 Solicitar Reserva", "📋 Ver y Cancelar Reservas"]
)

with tab_reservar:
  col_izq, col_der = st.columns(2)

  with col_izq:
    material = st.selectbox(
        "Material que deseas reservar", list(INVENTARIO.keys())
    )
    fecha = st.date_input("Fecha de reserva")
    sesion = st.selectbox(
        "Sesión lectiva", ["1.ª", "2.ª", "3.ª", "4.ª", "5.ª", "6.ª"]
    )

  # Calcular el total de unidades reservadas previamente para ese mismo día y sesión
  cantidad_reservada_previamente = sum(
      r["cantidad"]
      for r in st.session_state.reservas
      if r["material"] == material
      and r["fecha"] == str(fecha)
      and r["sesion"] == sesion
  )

  existencias_totales = INVENTARIO[material]
  unidades_disponibles = existencias_totales - cantidad_reservada_previamente

  with col_der:
    st.info(f"**Existencias totales del centro:** {existencias_totales}")
    st.metric(
        label=f"Disponibles para el {fecha} ({sesion} sesión)",
        value=unidades_disponibles,
    )

    if unidades_disponibles > 0:
      cantidad = st.number_input(
          "Cantidad a reservar",
          min_value=1,
          max_value=unidades_disponibles,
          value=1,
          step=1,
      )

      if st.button("Confirmar reserva", type="primary"):
        # Registrar la reserva
        st.session_state.reservas.append({
            "material": material,
            "fecha": str(fecha),
            "sesion": sesion,
            "cantidad": cantidad,
        })
        st.success(
            f"✅ ¡Reserva realizada con éxito! {cantidad} unidad(es) de"
            f" '{material}' para el {fecha} ({sesion} sesión)."
        )
        st.rerun()
    else:
      st.error(
          "⚠️ No hay unidades disponibles para este material en la fecha y"
          " sesión seleccionadas."
      )

with tab_gestion:
  st.subheader("Reservas Actualmente Guardadas")

  if not st.session_state.reservas:
    st.write("No hay reservas activas en el sistema.")
  else:
    # Creamos una variable para registrar si el usuario ha pulsado algún botón de borrar
    indice_a_eliminar = None

    for idx, res in enumerate(st.session_state.reservas):
      col_info, col_accion = st.columns([4, 1])

      with col_info:
        st.write(
            f"📌 **{res['material']}** | Cantidad: **{res['cantidad']}** |"
            f" Fecha: **{res['fecha']}** | Sesión: **{res['sesion']}**"
        )
      with col_accion:
        # Si se pulsa, guardamos el índice en nuestra variable temporal
        if st.button("Cancelar", key=f"cancelar_{idx}"):
          indice_a_eliminar = idx

    # Eliminamos el elemento FUERA del bucle for y recargamos la página limpiamente
    if indice_a_eliminar is not None:
      st.session_state.reservas.pop(indice_a_eliminar)
      st.rerun()
