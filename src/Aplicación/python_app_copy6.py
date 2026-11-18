import base64
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sistema de Reservas - Robótica", page_icon="🤖", layout="wide"
)

if "usuario_autenticado" not in st.session_state:
    st.session_state.usuario_autenticado = None

if "ciclo_seleccionado" not in st.session_state:
    st.session_state.ciclo_seleccionado = None

if "vista_danos" not in st.session_state:
    st.session_state.vista_danos = False

if "reservas" not in st.session_state:
    st.session_state.reservas = []

if "danos" not in st.session_state:
    st.session_state.danos = []


def obtener_imagen_base64(ruta_imagen):
    if os.path.exists(ruta_imagen):
        with open(ruta_imagen, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""


directorio_actual = os.path.dirname(os.path.abspath(__file__))

if st.session_state.vista_danos:
    archivo_fondo = "fondo1.png"
    css_tarjeta_principal = """
        background-color: rgba(255, 255, 255, 0.78) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        border-radius: 24px !important;
        border: 1.5px solid rgba(255, 255, 255, 0.85) !important;
        box-shadow: 0 15px 35px rgba(15, 23, 42, 0.15) !important;
    """
elif (
    st.session_state.usuario_autenticado is None
    or st.session_state.ciclo_seleccionado is None
):
    archivo_fondo = "fondo1.png"
    css_tarjeta_principal = """
        background-color: transparent !important;
        background: transparent !important;
        box-shadow: none !important;
    """
else:
    if st.session_state.ciclo_seleccionado == "Infantil":
        archivo_fondo = "fondoinfantil1.png"
    elif st.session_state.ciclo_seleccionado == "Primaria":
        archivo_fondo = "fondoprimaria1.png"
    else:
        archivo_fondo = "fondo_secundaria1.png"

    css_tarjeta_principal = """
        background-color: rgba(224, 242, 254, 0.55) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        border-radius: 24px !important;
        border: 1.5px solid rgba(255, 255, 255, 0.75) !important;
        box-shadow: 0 15px 35px rgba(15, 23, 42, 0.15) !important;
    """

ruta_fondo = os.path.join(directorio_actual, archivo_fondo)
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
    html, body, [data-testid="stAppViewContainer"], .stApp, p, label, button {{
        font-family: 'Inter', sans-serif !important;
    }}
    [data-testid="stExpander"] summary {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
    }}
    [data-testid="stExpander"] summary span[data-testid="stIconMaterial"] {{
        font-family: 'Material Symbols Rounded' !important;
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
        {css_tarjeta_principal}
        padding: 2.5rem 3.5rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }}
    h1, h2, h3 {{
        color: #0F172A !important;
        font-weight: 700 !important;
    }}

    /* ---------------------------------------------------------
       TARJETAS AZULES GRANDES PARA LOS BOTONES PRINCIPALES
       --------------------------------------------------------- */
    div[data-testid="stButton"] button[kind="primary"] {{
        background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%) !important;
        color: #ffffff !important;
        min-height: 170px !important;
        padding: 1.5rem 1rem !important;
        border-radius: 20px !important;
        border: 2px solid rgba(255, 255, 255, 0.7) !important;
        box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.35), 0 8px 10px -6px rgba(2, 132, 199, 0.2) !important;
        transition: all 0.25s ease !important;
        white-space: pre-line !important;
    }}

    div[data-testid="stButton"] button[kind="primary"] p {{
        font-size: 1.65rem !important;
        font-weight: 800 !important;
        line-height: 1.4 !important;
        color: #ffffff !important;
        text-shadow: 0 1px 2px rgba(15, 23, 42, 0.2) !important;
    }}

    div[data-testid="stButton"] button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #0369a1 0%, #0ea5e9 100%) !important;
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 20px 30px -10px rgba(2, 132, 199, 0.5) !important;
        border-color: #ffffff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def cargar_inventario():
    try:
        ruta_csv = os.path.join(directorio_actual, "inventario_robotica.csv")
        df = pd.read_csv(ruta_csv)
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


def obtener_stock_disponible_ciclo(ciclo, material):
    stock_base = INVENTARIO.get(material, 0)
    danadas = sum(
        d["Cantidad"]
        for d in st.session_state.danos
        if d["Ciclo"] == ciclo and d["Material"] == material
    )
    return max(0, stock_base - danadas)


def eliminar_reserva(indice):
    st.session_state.reservas.pop(indice)
# --- FIN DE LA PARTE 1 (Pega la Parte 2 justo debajo de esta línea) ---
# ---------------------------------------------------------
# PANTALLA 1: LOGIN / REGISTRO DE ACCESO
# ---------------------------------------------------------
if st.session_state.usuario_autenticado is None:
    st.title("🔑 Registro de Acceso - Sistema de Reservas")
    st.write("Por favor, introduzca sus datos para registrar la reserva:")

    nombre_profesor = st.text_input("Nombre y apellidos del profesor/a *")

    if st.button("Ingresar al Sistema"):
        if not nombre_profesor.strip():
            st.error("⚠️ Debes introducir un nombre válido para continuar.")
        else:
            st.session_state.usuario_autenticado = nombre_profesor.strip()
            st.rerun()

# ---------------------------------------------------------
# PANTALLA 2: GESTIÓN DE DAÑOS E INVENTARIO
# ---------------------------------------------------------
elif st.session_state.vista_danos:
    usuario = st.session_state.usuario_autenticado

    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("⬅️ Volver a Ciclos"):
            st.session_state.vista_danos = False
            st.rerun()

    st.title("🛠️ Informe de Daños e Inventario")
    st.caption(f"Sesión activa de: **{usuario}**")

    st.subheader("📢 Notificar material dañado")
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        ciclo_dano = st.selectbox(
            "Ciclo afectado", ["Infantil", "Primaria", "Secundaria"]
        )
        material_dano = st.selectbox(
            "Material dañado", list(INVENTARIO.keys())
        )

    with col_d2:
        stock_operativo = obtener_stock_disponible_ciclo(ciclo_dano, material_dano)
        stock_total = INVENTARIO[material_dano]

        if stock_operativo > 0:
            cantidad_dano = st.number_input(
                f"Unidades dañadas (Operativas en {ciclo_dano}: {stock_operativo} de {stock_total})",
                min_value=1,
                max_value=stock_operativo,
                value=1,
            )
        else:
            st.warning(
                f"⚠️ Todas las unidades de '{material_dano}' en {ciclo_dano} ya están reportadas como dañadas."
            )
            cantidad_dano = 0

        comentario_dano = st.text_input(
            "Comentario sobre la avería (opcional)",
            placeholder="Ej: No carga la batería, rueda rota, falta cable USB...",
        )

    if stock_operativo > 0:
        if st.button("🚨 Registrar incidencia"):
            nuevo_dano = {
                "Usuario": usuario,
                "Ciclo": ciclo_dano,
                "Material": material_dano,
                "Cantidad": cantidad_dano,
                "Comentario": comentario_dano.strip() if comentario_dano.strip() else "Sin comentarios",
            }
            st.session_state.danos.append(nuevo_dano)
            st.rerun()

    st.markdown("---")
    st.subheader("📋 Registro Público de Materiales Dañados")

    if not st.session_state.danos:
        st.info("No hay material dañado registrado actualmente. ¡Todo el inventario está operativo!")
    else:
        df_danos = pd.DataFrame(st.session_state.danos)
        st.dataframe(df_danos, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🔧 Rehabilitar material reparado")

        opciones_reparacion = [
            f"#{i + 1} | [{d['Ciclo']}] {d['Cantidad']}x {d['Material']} — Reportado por {d['Usuario']} ({d['Comentario']})"
            for i, d in enumerate(st.session_state.danos)
        ]

        seleccion_reparar = st.selectbox(
            "Selecciona el reporte que ya ha sido reparado:",
            opciones_reparacion,
        )

        if st.button("✅ Marcar como reparado"):
            indice_a_eliminar = opciones_reparacion.index(seleccion_reparar)
            st.session_state.danos.pop(indice_a_eliminar)
            st.rerun()

# ---------------------------------------------------------
# PANTALLA 3: SELECCIÓN DE CICLOS
# ---------------------------------------------------------
elif st.session_state.ciclo_seleccionado is None:
    col_logout, _, col_danos = st.columns([1.2, 2.3, 1.2])
    with col_logout:
        if st.button("❌ Cambiar de Profesor / Salir"):
            st.session_state.usuario_autenticado = None
            st.rerun()
    with col_danos:
        if st.button("🛠️ Informe de daños", use_container_width=True):
            st.session_state.vista_danos = True
            st.rerun()

    st.title("🤖 Reserva de Material de Informática y Robótica")
    st.subheader(f"Bienvenido/a, **{st.session_state.usuario_autenticado}**")
    st.write(
        "Selecciona el ciclo educativo en el que deseas consultar o reservar el material:"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        if st.button(
            "🧸\nINFANTIL\n(3 - 6 años)", use_container_width=True, type="primary"
        ):
            st.session_state.ciclo_seleccionado = "Infantil"
            st.rerun()

    with col2:
        if st.button(
            "📚\nPRIMARIA\n(6 - 12 años)", use_container_width=True, type="primary"
        ):
            st.session_state.ciclo_seleccionado = "Primaria"
            st.rerun()

    with col3:
        if st.button(
            "🔬\nSECUNDARIA\n(ESO / Bach.)", use_container_width=True, type="primary"
        ):
            st.session_state.ciclo_seleccionado = "Secundaria"
            st.rerun()

# ---------------------------------------------------------
# PANTALLA 4: RESERVAS DEL CICLO SELECCIONADO
# ---------------------------------------------------------
else:
    ciclo_actual = st.session_state.ciclo_seleccionado
    usuario = st.session_state.usuario_autenticado

    col_back, _ = st.columns(2)
    with col_back:
        if st.button("⬅️ Back / Exit"):
            st.session_state.ciclo_seleccionado = None
            st.rerun()

    st.title(f"🤖 Reserva de Material - Ciclo {ciclo_actual}")
    st.caption(f"Reserva activa a nombre de: **{usuario}**")

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
            "08:00 - 08:55",
            "08:55 - 09:50",
            "09:50 - 10:45",
            "11:05 - 12:00",
            "12:00 - 12:55",
            "12:55 - 13:50",
            "14:10 - 15:05",
        ]

    st.subheader("📝 Nueva Reserva")
    col_form1, col_form2 = st.columns(2)

    with col_form1:
        fecha = st.date_input("Fecha de la reserva")
        tramo = st.selectbox("Tramo horario", horarios)

    with col_form2:
        material = st.selectbox("Selecciona el material", list(INVENTARIO.keys()))
        stock_operativo_ciclo = obtener_stock_disponible_ciclo(ciclo_actual, material)
        stock_total = INVENTARIO[material]

        reservadas_en_tramo = sum(
            res["Cantidad"]
            for res in st.session_state.reservas
            if res["Ciclo"] == ciclo_actual
            and res["Material"] == material
            and res["Fecha"] == str(fecha)
            and res["Horario"] == tramo
        )
        disponibles = max(0, stock_operativo_ciclo - reservadas_en_tramo)

        if disponibles > 0:
            cantidad = st.number_input(
                f"Cantidad (Disponibles: {disponibles} de {stock_operativo_ciclo} operativos)",
                min_value=1,
                max_value=disponibles,
                value=1,
            )
        else:
            if stock_operativo_ciclo == 0:
                st.warning(
                    f"⚠️ Todas las unidades de '{material}' en {ciclo_actual} están averiadas actualmente."
                )
            else:
                st.warning(
                    f"⚠️ No quedan unidades disponibles de '{material}' para este horario."
                )
            cantidad = 0

    if disponibles > 0:
        if st.button("✅ Confirmar Reserva"):
            nueva_reserva = {
                "Profesor": usuario,
                "Ciclo": ciclo_actual,
                "Fecha": str(fecha),
                "Horario": tramo,
                "Material": material,
                "Cantidad": cantidad,
            }
            st.session_state.reservas.append(nueva_reserva)
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander(f"🔒 Ventana Privada: Gestionar / Eliminar reservas de {usuario}"):
        mis_reservas = [
            (i, res)
            for i, res in enumerate(st.session_state.reservas)
            if res["Profesor"].lower() == usuario.lower()
        ]

        if not mis_reservas:
            st.info("No tienes ninguna reserva registrada a tu nombre.")
        else:
            st.write("Aquí puedes cancelar únicamente tus propias reservas:")
            for indice_real, res in mis_reservas:
                col_txt, col_btn = st.columns(2)
                with col_txt:
                    st.write(
                        f"**📅 {res['Fecha']}** | 🕒 `{res['Horario']}` | "
                        f"**{res['Ciclo']}** — **{res['Cantidad']}x {res['Material']}**"
                    )
                with col_btn:
                    if st.button("🗑️ Eliminar mi reserva", key=f"priv_del_{indice_real}"):
                        eliminar_reserva(indice_real)
                        st.rerun()

    st.markdown("---")
    st.subheader("📋 Registro General de Reservas (Solo Consulta)")

    if not st.session_state.reservas:
        st.info("Aún no hay reservas registradas en el sistema.")
    else:
        for res in st.session_state.reservas:
            st.write(f"• {res['Fecha']} | {res['Horario']} | {res['Ciclo']} — "
f"{res['Cantidad']}x {res['Material']} (Reservado por: {res['Profesor']})"
)
