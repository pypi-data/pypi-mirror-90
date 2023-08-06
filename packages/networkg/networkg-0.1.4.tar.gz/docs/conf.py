"""Sphinx configuration."""

import os
import sys

# Add the project root directory to path to make networkg importable without installing.
# This is required since Read the Docs is not able to build the Rust extensions.
# NB: Sphinx is not able to document extension classes if the package is not installed.
sys.path.insert(0, os.path.abspath("../"))

project = "networkg"
author = "Gustav Gränsbo"
copyright = f"2020, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_autodoc_typehints"]
autodoc_mock_imports = ["networkg.networkg"]
