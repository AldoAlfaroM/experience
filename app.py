"""Landing page del CV con Flask.

  python app.py            -> servidor de producción (waitress) en http://127.0.0.1:5000
  python app.py --build    -> genera un sitio estático en ./dist (GitHub Pages, Netlify, Cloudflare Pages)

Variables de entorno opcionales:
  HOST          interfaz donde escuchar (por defecto 127.0.0.1; usa 0.0.0.0 detrás de un proxy)
  PORT          puerto (por defecto 5000)
  FLASK_DEBUG   "1" activa el modo debug SOLO para desarrollo local
  BEHIND_HTTPS  "1" añade HSTS cuando el sitio se sirve por HTTPS
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

from flask import Flask, abort, render_template, request

from cv_data import CV

FONT_CSS = "https://fonts.googleapis.com"
FONT_FILES = "https://fonts.gstatic.com"

# Política estricta: sin scripts/estilos inline, sin eval, sin iframes, sin plugins.
CSP = "; ".join([
    "default-src 'none'",
    "script-src 'self'",
    f"style-src 'self' {FONT_CSS}",
    f"font-src {FONT_FILES}",
    "img-src 'self' data:",
    "connect-src 'none'",
    "base-uri 'none'",
    "form-action 'none'",
    "frame-ancestors 'none'",
    "object-src 'none'",
    "upgrade-insecure-requests",
])

SECURITY_HEADERS = {
    "Content-Security-Policy": CSP,
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=(), "
                          "interest-cohort=(), browsing-topics=()",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Resource-Policy": "same-origin",
    "X-Permitted-Cross-Domain-Policies": "none",
}
HSTS = "max-age=63072000; includeSubDomains; preload"

app = Flask(__name__)
app.config.update(
    DEBUG=False,
    TESTING=False,
    MAX_CONTENT_LENGTH=1024,          # la página no acepta cuerpos de petición
    SEND_FILE_MAX_AGE_DEFAULT=60 * 60 * 24,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)


@app.context_processor
def asset_helpers():
    # Añade un hash del contenido a CSS/JS para que los navegadores nunca usen una versión vieja.
    def asset(name):
        digest = hashlib.sha256((Path(app.static_folder) / name).read_bytes()).hexdigest()[:10]
        return f"{name}?v={digest}"
    return {"asset": asset}


@app.before_request
def only_safe_methods():
    if request.method not in ("GET", "HEAD"):
        abort(405)


@app.after_request
def set_security_headers(response):
    for name, value in SECURITY_HEADERS.items():
        response.headers.setdefault(name, value)
    if os.environ.get("BEHIND_HTTPS") == "1" or request.is_secure:
        response.headers.setdefault("Strict-Transport-Security", HSTS)
    response.headers.pop("Server", None)
    return response


@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(413)
@app.errorhandler(500)
def handle_error(err):
    # Respuesta genérica: no revela trazas, versiones ni rutas internas.
    code = getattr(err, "code", 500)
    return {404: "Not found", 405: "Method not allowed",
            413: "Request too large"}.get(code, "Server error"), code, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/")
def index():
    return render_template("index.html", cv=CV, static_prefix="/static", csp_meta=None)


def build(out_dir="dist"):
    out = Path(out_dir)
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(Path(app.static_folder), out / "static")
    # Los hosts estáticos no ejecutan Flask: la CSP va también en <meta>
    # (frame-ancestors no es válido en <meta>, por eso se omite ahí).
    meta_csp = "; ".join(d for d in CSP.split("; ") if not d.startswith("frame-ancestors"))
    with app.app_context():
        html = render_template("index.html", cv=CV, static_prefix="static", csp_meta=meta_csp)
    (out / "index.html").write_text(html, encoding="utf-8")
    # Cabeceras para Netlify / Cloudflare Pages.
    headers = "\n".join(f"  {k}: {v}" for k, v in {**SECURITY_HEADERS, "Strict-Transport-Security": HSTS}.items())
    (out / "_headers").write_text(f"/*\n{headers}\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")  # GitHub Pages: servir tal cual, sin Jekyll
    print(f"Sitio estático generado en {out.resolve()}")


def serve():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    if os.environ.get("FLASK_DEBUG") == "1":
        # Solo para desarrollo local: el debugger de Werkzeug permite ejecutar código.
        app.run(host="127.0.0.1", port=port, debug=True)
        return
    from waitress import serve as waitress_serve
    print(f"Serving on http://{host}:{port}")
    waitress_serve(app, host=host, port=port, ident=None)


if __name__ == "__main__":
    build() if "--build" in sys.argv else serve()
