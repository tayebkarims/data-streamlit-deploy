"""
Shared fixtures for the Deploy Streamlit test suite.
"""

from pathlib import Path
import pytest
import tomllib


@pytest.fixture(scope="session")
def project_root():
    """Get the zoologist project root path."""
    # Navigate up from the test file to find the zoologist project
    code_folder = next(
        parent for parent in Path(__file__).resolve().parents if "code" in parent.parent.name.lower()
    )
    return code_folder / "zoologist-front"
