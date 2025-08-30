# SpeedyIndex Clone - GitHub & Render Ready

### Features
- Shortlink expansion
- Feeder HTML generation
- Sitemap generation + Google ping (local/test only)
- CSV report
- Basic index check (Pending placeholder)
- Ready for Render.com deployment

### Setup
1. Clone repo
2. python -m venv venv
3. Activate virtualenv
4. pip install -r requirements.txt
5. python app.py
6. Open http://127.0.0.1:5000

### Render Deployment
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn app:app
- Connect GitHub repo → Deploy
