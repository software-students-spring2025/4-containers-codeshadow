"""Unit tests for the web app routes."""

import pytest
from web_app import app

def test_index_page():
    """Test index page returns a 200 status code."""
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
