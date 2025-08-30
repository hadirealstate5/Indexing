from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os, uuid, csv, time, requests, datetime
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "dev-secret-speedy"
BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, "uploads")
REPORTS = os.path.join(BASE, "reports")
FEEDERS = os.path.join(BASE, "static", "feeders")
SITEMAPS = os.path.join(BASE, "sitemaps")
os.makedirs(UPLOADS, exist_ok=True)
os.makedirs(REPORTS, exist_ok=True)
os.makedirs(FEEDERS, exist_ok=True)
os.makedirs(SITEMAPS, exist_ok=True)

UA = "Mozilla/5.0"

def expand_url(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=10, headers={"User-Agent": UA})
        return r.url
    except:
        return url

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f:
        flash("No file uploaded")
        return redirect(url_for("index"))
    content = f.read().decode("utf-8", errors="ignore").splitlines()
    urls = [ln.strip() for ln in content if ln.strip()]
    job = str(uuid.uuid4())[:8]
    expanded = [expand_url(u) for u in urls]
    rows = []
    for u in expanded:
        try:
            r = requests.head(u, allow_redirects=True, timeout=10, headers={"User-Agent": UA})
            ping = f"Ping {r.status_code}"
        except:
            ping = "Error"
        rows.append([u, ping, "Pending"])
        time.sleep(0.5)
    ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    rpt = os.path.join(REPORTS, f"report_{job}_{ts}.csv")
    with open(rpt, "w", newline="", encoding="utf-8") as csvf:
        w = csv.writer(csvf)
        w.writerow(["URL","Ping","IndexCheck"])
        w.writerows(rows)
    return render_template("results.html", rows=rows, report_file=os.path.basename(rpt))

@app.route("/download/<name>")
def download(name):
    path = os.path.join(REPORTS, name)
    if not os.path.exists(path):
        flash("Report not found")
        return redirect(url_for("index"))
    return send_file(path, as_attachment=True, download_name=name)

if __name__ == "__main__":
    app.run(debug=True)
