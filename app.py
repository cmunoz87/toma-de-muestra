import streamlit as st

st.set_page_config(page_title="Motor de Reglas de Toma de Muestra", layout="centered")

st.image("logo.png", use_container_width=True)

st.markdown("## Motor de Reglas de Toma de Muestra")
st.caption("Herramienta explicativa para desarrolladores: lógica de asociación de tomas de muestra")

st.divider()

col1, col2 = st.columns([2, 1])
with col1:
    edad = st.number_input("Edad del paciente", min_value=0.0, step=1.0)
with col2:
    unidad = st.radio("Unidad", ["Años", "Meses"], horizontal=True)

edad_anios = edad / 12 if unidad == "Meses" else edad
grupo = "Pediátrica" if edad_anios < 15 else "Adulta"
st.info(f"Edad en años: {edad_anios:.2f} → {grupo}")

st.divider()

EXAMENES = [
    "Glucosa", "Lipasa", "Urea", "GGT",
    "Orina completa", "Gas arterial", "Gas venoso",
    "Hemocultivo", "Coprocultivo"
]

TIPOS_MUESTRA = ["Orina", "Sangre venosa", "Sangre arterial", "Deposiciones"]

TIPO_SUGERIDO = {
    "Glucosa": "Sangre venosa",
    "Lipasa": "Sangre venosa",
    "Urea": "Sangre venosa",
    "GGT": "Sangre venosa",
    "Orina completa": "Orina",
    "Gas arterial": "Sangre arterial",
    "Gas venoso": "Sangre venosa",
    "Hemocultivo": "Sangre venosa",
    "Coprocultivo": "Deposiciones"
}

examenes_sel = st.multiselect("Selecciona examen(es)", EXAMENES)
tipos_por_examen = {}

if examenes_sel:
    st.markdown("### Tipo de muestra por examen")
    for ex in examenes_sel:
        idx = TIPOS_MUESTRA.index(TIPO_SUGERIDO[ex])
        tipos_por_examen[ex] = st.selectbox(ex, TIPOS_MUESTRA, index=idx, key=ex)

st.divider()

def toma_venosa(grupo):
    return f"Toma de muestra venosa {grupo.lower()}"

def toma_arterial(grupo):
    return f"Toma de muestra arterial {grupo.lower()}"

def toma_hemocultivo(grupo):
    return f"Toma de muestra hemocultivo {grupo.lower()}"

tomas = set()

if examenes_sel:
    if "Hemocultivo" in examenes_sel:
        tomas.add(toma_hemocultivo(grupo))

    for ex in examenes_sel:
        if ex == "Hemocultivo":
            continue
        tipo = tipos_por_examen[ex]
        if tipo == "Sangre venosa":
            tomas.add(toma_venosa(grupo))
        elif tipo == "Sangre arterial":
            tomas.add(toma_arterial(grupo))

st.markdown("### Resultado")
if tomas:
    for t in sorted(tomas):
        st.write("-", t)
else:
    st.info("No corresponde agregar toma de muestra")

st.divider()
st.caption("Elaborado por TM. Camilo Muñoz, Enero 2026")
