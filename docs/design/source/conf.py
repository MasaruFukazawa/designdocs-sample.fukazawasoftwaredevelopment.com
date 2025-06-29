# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '設計書サンプル'
copyright = '2025, MasaruFukazawa'
author = 'MasaruFukazawa'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinxcontrib.mermaid',
    'sphinxcontrib.openapi',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ja'

# -- Mermaid configuration ---------------------------------------------------
# Mermaidの出力形式（'raw', 'png', 'svg'）
mermaid_output_format = 'raw'

# Mermaidのバージョン
mermaid_version = '11.2.0'

# Mermaidの初期化コード
mermaid_init_js = """
mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    themeVariables: {
        fontFamily: 'Arial, sans-serif',
        fontSize: '14px'
    }
});
"""

# Mermaidのパラメータ（テーマ、幅、背景色など）
mermaid_params = [
    '--theme', 'default',
    '--width', '800',
    '--backgroundColor', 'white'
]

# 全てのMermaid図でズーム機能を有効化
mermaid_d3_zoom = True

# 詳細モードを有効化（デバッグ用）
mermaid_verbose = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
#html_theme = 'alabaster'

html_static_path = ['../_static']

html_css_files = [
    #'custom.css',
]
