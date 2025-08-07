import os
from pathlib import Path

import pandas as pd
import streamlit as st
import slideio


WSI_EXTENSIONS = (".svs", ".scn", ".czi")


def list_wsis(directory: str):
    """Return a list of WSI files in *directory* recursively."""
    paths = []
    for root, _dirs, files in os.walk(directory):
        for name in files:
            if name.lower().endswith(WSI_EXTENSIONS):
                paths.append(Path(root) / name)
    return paths


def load_wsi(path: Path):
    """Open a WSI file and return an image array."""
    ext = path.suffix.lower()
    drivers = {
        ".svs": "SVS",
        ".scn": "SCN",
        ".czi": "CZI",
    }
    driver = drivers.get(ext)
    if driver is None:
        raise ValueError(f"Unsupported extension: {ext}")

    slide = slideio.open_slide(str(path), driver)
    scene = slide.get_scene(0)
    image = scene.read_block()
    return image


def main():
    st.title("WSI Browser")
    st.sidebar.header("Input")
    choice = st.sidebar.radio("Source", ["Directory", "CSV/XLSX"])

    selected = None
    if choice == "Directory":
        directory = st.sidebar.text_input("Directory", value=".")
        if directory:
            files = list_wsis(directory)
            selected = st.selectbox("WSI Files", files)
    else:
        uploaded = st.sidebar.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])
        if uploaded is not None:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            column = st.sidebar.selectbox("Column with paths", df.columns)
            selected = st.selectbox("WSI Files", df[column].tolist())

    if selected:
        st.write(f"Opening {selected}")
        try:
            image = load_wsi(Path(selected))
            st.image(image)
        except Exception as exc:
            st.error(str(exc))


if __name__ == "__main__":
    main()
