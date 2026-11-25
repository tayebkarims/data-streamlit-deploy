"""
Tests to check progress at the end of the Deploy Streamlit challenge.
"""

import re
import pytest


class TestStreamlitApp:
    """Basic checks that the Streamlit app is using secrets."""

    def test_secrets_file_exists(self, project_root):
        """The .streamlit/secrets.toml file should exist to store the API URL."""
        secrets_path = project_root / ".streamlit" / "secrets.toml"
        assert secrets_path.exists(), \
            f"{secrets_path} not found. Create a .streamlit/secrets.toml file with your API_URL"

    def test_app_uses_secrets(self, project_root):
        """app.py should read the API URL from st.secrets instead of hardcoding it."""
        app_path = project_root / "app.py"
        source = app_path.read_text()
        assert re.search(r"st\.secrets\[", source), \
            "app.py should use st.secrets[...] to read the API URL instead of hardcoding it"
