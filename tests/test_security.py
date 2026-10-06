import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app  # noqa: E402


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_index_has_security_headers():
    r = client().get("/")
    assert r.status_code == 200
    csp = r.headers["Content-Security-Policy"]
    assert "default-src 'none'" in csp
    assert "unsafe-inline" not in csp and "unsafe-eval" not in csp
    assert "frame-ancestors 'none'" in csp
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"
    assert "Server" not in r.headers


def test_no_inline_scripts():
    html = client().get("/").get_data(as_text=True)
    assert "<script>" not in html
    assert "onclick=" not in html.lower()


def test_hsts_only_over_https():
    assert "Strict-Transport-Security" not in client().get("/").headers
    r = client().get("/", base_url="https://localhost")
    assert "max-age=" in r.headers["Strict-Transport-Security"]


def test_unsafe_methods_rejected():
    for method in ("post", "put", "delete", "patch"):
        r = getattr(client(), method)("/")
        assert r.status_code == 405


def test_errors_do_not_leak_details():
    r = client().get("/../../etc/passwd")
    assert r.status_code == 404
    assert r.get_data(as_text=True) == "Not found"
    assert "Content-Security-Policy" in r.headers


def test_debug_disabled_by_default():
    assert app.debug is False


def test_no_email_on_page():
    html = client().get("/").get_data(as_text=True)
    assert "mailto:" not in html
    assert "@" not in html.split("<body>", 1)[1]
