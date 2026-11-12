import base64
import os
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# CONFIGURACIÓN E INYECCIÓN DE ESTILO Y FONDO
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sistema de Reservas - Robótica", page_icon="🤖", layout="wide"
)


def obtener_imagen_base64(ruta_imagen):
    if os.path.exists(ruta_imagen):
        with open(ruta_imagen, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""


directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_fondo = os.path.join(directorio_actual, "fondo.png")
imagen_base64 = obtener_imagen_base64(ruta_fondo)

if imagen_base64:
    css_background = f"background-image: url('data:image/png;base64,{imagen_base64}');"
else:
    css_background = (
        "background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);"
    )

st.markdown(
    f"""
    <style>
    html, body, [data-testid="stAppViewContainer"], .stApp, p, div, label, button, span {{
        font-family: 'Inter', sans-serif !important;
    }}
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stMain {{
        background-color: transparent !important;
        background: transparent !important;
    }}
    .stApp {{
        {css_background}
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    [data-testid="stMainBlockContainer"] {{
        background-color: transparent !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 2.5rem 3.5rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }}
    h1, h2, h3 {{
        color: #0F172A !important;
        font-weight: 700 !important;
    }}
    button[data-testid="stMarkdownContainer"] p {{
        font-weight: 600 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# CARGA DE INVENTARIO DESDE CSV (O RESPALDO)
# ---------------------------------------------------------
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
            "Coche inteligente 45 pieces": 15,
        }


INVENTARIO = cargar_inventario()

# ---------------------------------------------------------
# ESTADOS DE SESIÓN (NAVEGACIÓN Y RESERVAS)
# ---------------------------------------------------------
if "ciclo_seleccionado" not in st.session_state:
    st.session_state.ciclo_seleccionado = None

if "reservas" not in st.session_state:
    st.session_state.reservas = []


def eliminar_reserva(indice):
    st.session_state.reservas.pop(indice)


# ---------------------------------------------------------
# PANTALLA PRINCIPAL: SELECCIÓN DE CICLO
# ---------------------------------------------------------
if st.session_state.ciclo_seleccionado is None:
    st.title("🤖 Reserva de Material de Informática y Robótica")
    st.write(
        "Por favor, selecciona el ciclo educativo en el que deseas consultar o"
        " reservar el material:"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🧸 Infantil", use_container_width=True, type="primary"):
            st.session_state.ciclo_seleccionado = "Infantil"
            st.rerun()

    with col2:
        if st.button("📚 Primaria", use_container_width=True, type="primary"):
            st.session_state.ciclo_seleccionado = "Primaria"
            st.rerun()

    with col3:
        if st.button("🔬 Secundaria", use_container_width=True, type="primary"):
            st.session_state.ciclo_seleccionado = "Secundaria"
            st.rerun()

# ---------------------------------------------------------
# PANTALLA ESPECÍFICA POR CICLO SELECCIONADO
# ---------------------------------------------------------
else:
    ciclo_actual = st.session_state.ciclo_seleccionado

    # Botón superior para volver al menú principal (Back / Exit)
    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ Back / Exit", use_container_width=True):
            st.session_state.ciclo_seleccionado = None
            st.rerun()

    st.title(f"🤖 Reserva de Material - Ciclo {ciclo_actual}")

    # Configuración de tramos horarios según el ciclo seleccionado
    if ciclo_actual in ["Infantil", "Primaria"]:
        horarios = [
            "09:00 - 09:45",
            "09:45 - 10:30",
            "10:30 - 11:15",
            "11:45 - 12:30",
            "12:30 - 13:15",
            "13:15 - 14:00",
            "15:00 - 15:45",
            "15:45 - 16:30",
        ]
    else:
        horarios = [
            "8:00 - 8:55 (1.ª)",
            "8:55 - 9:50 (2.ª)",
            "9:50 - 10:45 (3.ª)",
            "11:05 - 12:00 (4.ª)",
            "12:00 - 12:55 (5.ª)",
            "12:55 - 13:50 (6.ª)",
            "14:10 - 15:05 (7.ª)",
        ]

    tab_reservar, tab_gestion = st.tabs(
        ["📝 Solicitar Reserva", "📋 Ver y Cancelar Reservas"]
    )

    with tab_reservar:
        col_izq, col_der = st.columns(2)

        with col_izq:
            usuario = st.text_input(
                "Nombre de la persona / profesor que reserva *"
            )
            material = st.selectbox(
                "Material que deseas reservar", list(INVENTARIO.keys())
            )
            fecha = st.date_input("Fecha de reserva")
            sesion = st.selectbox("Tramo horario", horarios)

            # Restricción clave: El stock disminuye SOLO dentro del mismo ciclo educativo
            cantidad_reservada_previamente = sum(
                r["cantidad"]
                for r in st.session_state.reservas
                if r["ciclo"] == ciclo_actual
                and r["material"] == material
                and r["fecha"] == str(fecha)
                and r["sesion"] == sesion
            )

            existencias_totales = INVENTARIO[material]
            unidades_disponibles = existencias_totales - cantidad_reservada_previamente

        with col_der:
            st.info(f"**Existencias totales del centro:** {existencias_totales}")
            st.metric(
                label=f"Disponibles en {ciclo_actual} para el {fecha} ({sesion})",
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
                    if not usuario.strip():
                        st.error(
                            "⚠️ Debes indicar tu nombre en el campo de registro para poder reservar."
                        )
                    else:
                        st.session_state.reservas.append({
                            "usuario": usuario,
                            "ciclo": ciclo_actual,
                            "material": material,
                            "fecha": str(fecha),
                            "sesion": sesion,
                            "cantidad": cantidad,
                        })
                        st.success(
                            f"✅ ¡Reserva a nombre de **{usuario}** guardada con éxito! "
                            f"{cantidad} unidad(es) de '{material}' para el {fecha} ({sesion})."
                        )
                        st.rerun()
            else:
                st.error(
                    "⚠️ No hay unidades disponibles para este material en la fecha y sesión seleccionadas."
                )

    with tab_gestion:
        st.subheader(f"Reservas Registradas para el Ciclo: {ciclo_actual}")

        # Filtrar para ver solo lo reservado en esta pantalla activa
        reservas_ciclo = [
            (idx, r)
            for idx, r in enumerate(st.session_state.reservas)
            if r["ciclo"] == ciclo_actual
        ]

        if not reservas_ciclo:
            st.write(f"No hay reservas registradas para {ciclo_actual}.")
        else:
            for idx, res in reservas_ciclo:
                col_info, col_accion = st.columns([5, 1])
                with col_info:
                    st.write(
                        f"👤 **{res['usuario']}** | 📌 **{res['material']}** | Cantidad: **{res['cantidad']}** | "
                        f"Fecha: **{res['fecha']}** | Horario: **{res['sesion']}**"
                    )
                with col_accion:
                    st.button(
                        "Cancelar",
                        key=f"cancelar_{idx}",
                        on_click=eliminar_reserva,
                        args=(idx,),
                    )
