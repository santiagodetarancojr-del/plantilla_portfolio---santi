import streamlit as st

# Inventario del aula de robótica: todo incluido en este archivo.
INVENTARIO = {
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

st.title("Reservas del aula de robótica")
st.write("Selecciona el material que quieres reservar.")

material = st.selectbox("Material", list(INVENTARIO.keys()))
fecha = st.date_input("Fecha de reserva")
sesion = st.selectbox(
    "Sesión lectiva", ["1.ª", "2.ª", "3.ª", "4.ª", "5.ª", "6.ª"]
)
cantidad = st.number_input(
    "Cantidad", min_value=1, max_value=INVENTARIO[material], value=1, step=1
)

st.caption(f"Existencias totales de {material}: {INVENTARIO[material]}")

if st.button("Solicitar reserva"):
    st.success(
        f"Solicitud: {cantidad} unidad(es) de {material}, "
        f"para el {fecha}, sesión {sesion}."
    )

st.info(
    "Esta es la versión inicial: todavía no guarda reservas, "
    "no controla la disponibilidad por sesión ni permite cancelaciones."
)