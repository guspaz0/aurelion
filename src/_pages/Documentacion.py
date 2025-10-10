from datetime import datetime, date
import re
import streamlit as st
import pathlib
import logging
import streamlit_mermaid as stmd

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Documentacion",
    page_icon=":books:",
    layout="wide"
)

def get_pasos_pseudocodigo():
    """Get pasos detallados y pseudocódigo from pasos_programa.md"""
    pasos_programa_path = (pathlib.Path(__file__).parents[2] / "docs" / "pasos_programa.md").resolve()
    md_text = pasos_programa_path.read_text()
    st.markdown(md_text, unsafe_allow_html=True)
    st.caption(f"Archivo: {pasos_programa_path} — renderizado: {datetime.now().isoformat()}")

def get_ejecucion_programa():
    """Get pasos detallados y pseudocódigo from ejecucion_programa.md"""
    ejecucion_programa_path = (pathlib.Path(__file__).parents[2] / "docs" / "Ejecucion_programa.md").resolve()
    md_text = ejecucion_programa_path.read_text()
    st.markdown(md_text, unsafe_allow_html=True)
    st.caption(f"Archivo: {ejecucion_programa_path} — renderizado: {datetime.now().isoformat()}")

def render_diagrama():
    """Read docs/diagrama.md, extract mermaid code blocks and render them
    inside two Streamlit tabs: a rendered diagram tab and the markdown source tab.
    """
    diagrama_path = (pathlib.Path(__file__).parents[2] / "docs" / "diagrama.md").resolve()
    md_text = diagrama_path.read_text(encoding="utf-8")
    # find all mermaid fenced code blocks
    mermaid_blocks = re.findall(r"```mermaid\s*([\s\S]*?)```", md_text, flags=re.IGNORECASE)

    for i,md in enumerate(mermaid_blocks):
        stmd.st_mermaid(md)

def documentacion():
    logger.info("renderizando documentación")

    readme_path = (pathlib.Path(__file__).parents[2] / "README.md").resolve()

    if not readme_path.exists():
        st.error(f"README no encontrado en: {readme_path}")
        return
    
    md_text = readme_path.read_text(encoding="utf-8")

    intro, diagrama, pasos_pseudocodigo, ejecucion_programa = st.tabs(["Introduccion", "Diagrama", "Pasos detallados y pseudocodigo", "Ejecucion del programa"])
    with intro:
        st.markdown(md_text, unsafe_allow_html=True)
        st.caption(f"Archivo: {readme_path} — renderizado: {datetime.now().isoformat()}")
    
    with diagrama:
        render_diagrama()
    
    with pasos_pseudocodigo:
        get_pasos_pseudocodigo()
    
    with ejecucion_programa:
        get_ejecucion_programa()

if __name__ == "__main__":
    # allow running the page directly for quick testing
    documentacion()