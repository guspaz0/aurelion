import streamlit as st
import pathlib, logging

st.set_page_config(
    page_title="Documentacion ML",
    page_icon=":robot:",
    layout="wide"
)

# Load markdown files
path = pathlib.Path(__file__).parents[2] / "docs"
ENTREGA_ML_RESUMEN = path / 'ENTREGA_ML_RESUMEN.md'
GUIA_RAPIDA_ML = path / "GUIA_RAPIDA_ML.md"
ML_DOCUMENTATION =  path / "ML_DOCUMENTATION.md"


def documentacion_ml():

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["ENTREGA ML RESUMEN", "GUIA RAPIDA ML", "ML DOCUMENTATION"])

    with tab1:
        st.markdown(open(ENTREGA_ML_RESUMEN).read())

    with tab2:
        st.markdown(open(GUIA_RAPIDA_ML).read())

    with tab3:
        st.markdown(open(ML_DOCUMENTATION).read())


if __name__ == "__main__":
    # allow running the page directly for quick testing
    documentacion_ml()