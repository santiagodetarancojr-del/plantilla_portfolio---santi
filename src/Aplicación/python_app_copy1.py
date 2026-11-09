import base64
import os
import pandas as pd
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Sistema de Reservas - Robótica", page_icon="🤖", layout="wide"
)


# Función para cargar la imagen local de fondo de forma segura en Base64
def obtener_imagen_base64(ruta_imagen):
  if os.path.exists(ruta_imagen):
    with open(ruta_imagen, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode()
  return ""


# BUSCA LA IMAGEN EN TU CARPETA: Asegúrate de que tu imagen se llame 'fondo.png' y esté en la misma carpeta
ruta_fondo = "fondo.png"
imagen_base64 = obtener_imagen_base64(ruta_fondo)

if imagen_base64:
  css_background = (
      f"background-image: url('data:image/png;base64,{imagen_base64}');"
  )
else:
  css_background = (
      "background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);"
  )

# Inyección de CSS corregido y optimizado sin fallos de renderizado
st.markdown(
    f"""
    <style>
    /* Importación correcta de la fuente Inter desde Google Fonts */
    @import url('https://googleapis.com');

    /* Aplicar fuente global a todos los elementos posibles de Streamlit */
    html, body, [data-testid="stAppViewContainer"], .stApp, p, div, label, button, span {{
        font-family: 'Inter', sans-serif !important;
    }}

    /* Aplicar fondo a la clase raíz global para evitar cortes o franjas */
    .stApp {{
        {css_background}
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}

    /* Estilo del panel contenedor principal (Modo Tarjeta Flotante) */
    [data-testid="stMainBlockContainer"] {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2.5rem 3.5rem;
        border-radius: 16px;
        box-shadow: 0px 12px 40px rgba(0, 0, 0, 0.06);
        margin-top: 2rem;
        margin-bottom: 2rem;
    }}

    /* Personalización visual de los títulos */
    h1, h2, h3 {{
        color: #0F172A !important;
        font-weight: 700 !important;
    }}
    
    /* Pequeño retoque a las pestañas */
    button[data-testid="stMarkdownContainer"] p {{
        font-weight: 600 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# Cargar el inventario desde el CSV o usar la estructura inicial como respaldo
@st.cache_data
def cargar_inventario():
  try:
    df = pd.read_csv("inventario_robotica.csv")
    return dict(zip(df["nombre"], df["cantidad"]))
  except Exception:
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

# CORRECCIÓN AQUÍ: Inicializar correctamente la lista vacía con []
if "reservas" not in st.session_state:
  st.session_state.reservas = []


def eliminar_reserva(indice):
  st.session_state.reservas.pop(indice)


st.title("🤖 Reserva de Material de Informática y Robótica")
st.write(
    "Selecciona el material, la fecha y la sesión lectiva para realizar o"
    " consultar tus reservas."
)

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
    for idx, res in enumerate(st.session_state.reservas):
      col_info, col_accion = st.columns([4, 1])

      with col_info:
        st.write(
            f"📌 **{res['material']}** | Cantidad: **{res['cantidad']}** |"
            f" Fecha: **{res['fecha']}** | Sesión: **{res['sesion']}**"
        )
      with col_accion:
        st.button(
            "Cancelar",
            key=f"cancelar_{idx}",
            on_click=eliminar_reserva,
            args=(idx,),
        )
