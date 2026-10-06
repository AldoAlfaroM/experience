# experience

Live: https://aldoalfarom.github.io/experience/

Personal CV landing page for **Aldo Alfaro**, built with Python + Flask.

## Run locally

```bash
pip install -r requirements.txt
python app.py              # production server (waitress) on http://127.0.0.1:5000
```

Development with auto-reload: `FLASK_DEBUG=1 python app.py`

## Static build

```bash
python app.py --build      # outputs ./dist (GitHub Pages, Netlify, Cloudflare Pages)
```

Every push to `main` runs the tests and, if they pass, deploys the static build to the `gh-pages` branch (GitHub Pages).

## Edit content

All CV content lives in [`cv_data.py`](cv_data.py).

## Tests

```bash
pip install pytest && pytest -q
```

See [SECURITY.md](SECURITY.md) for the security measures in place.
