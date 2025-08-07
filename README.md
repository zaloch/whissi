# whissi

Whole slide imaging for surveys and synthesis of imaging.

## WSI Browser

This repository now includes a simple Streamlit front end that lets you browse for whole slide images (WSI) stored as `.svs`, `.scn` or `.czi` files.
You can either point the app to a directory containing WSIs or upload a CSV/XLSX file with paths to WSIs.
Selected files are opened using [SlideIO](https://github.com/slideio/slideio) for all supported formats.

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```bash
streamlit run wsi_browser.py
```

Use the sidebar to choose a directory or upload a CSV/XLSX with image paths. The selected WSI is displayed in the main area.
