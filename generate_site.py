import os, requests
from config import BING_API_KEY, SITE_URL, GITHUB_REPO
from datetime import datetime
import subprocess

BACKLINKS_FILE = 'backlinks.txt'
OUTPUT_DIR = 'site'
SITEMAP_FILE = 'sitemap.xml'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read backlinks
with open(BACKLINKS_FILE, 'r') as f:
    backlinks = [line.strip() for line in f if line.strip()]

# Generate HTML pages
for i, url in enumerate(backlinks, 1):
    page_name = f'page{i}.html'
    html_content = f"""
    <html>
    <head>
        <title>Backlink {i}</title>
        <meta name="description" content="Backlink page for {url}">
    </head>
    <body>
        <h1>Backlink {i}</h1>
        <p>Original URL: <a href="{url}">{url}</a></p>
    </body>
    </html>
    """
    with open(os.path.join(OUTPUT_DIR, page_name), 'w', encoding='utf-8') as f:
        f.write(html_content)

# Generate sitemap
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for i in range(1, len(backlinks)+1):
    sitemap += f'  <url>\n    <loc>{SITE_URL}/page{i}.html</loc>\n'
    sitemap += f'    <lastmod>{datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}</lastmod>\n  </url>\n'
sitemap += '</urlset>'
with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f"[+] Generated {len(backlinks)} pages + sitemap.xml")

# Optional GitHub push
if GITHUB_REPO:
    subprocess.run(["git", "init"], cwd=OUTPUT_DIR)
    subprocess.run(["git", "add", "."], cwd=OUTPUT_DIR)
    subprocess.run(["git", "commit", "-m", "Update site"], cwd=OUTPUT_DIR)
    subprocess.run(["git", "remote", "add", "origin", GITHUB_REPO], cwd=OUTPUT_DIR)
    subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=OUTPUT_DIR)
    print("[+] Pushed site to GitHub")

# Submit URLs to Bing
endpoint = f'https://ssl.bing.com/webmaster/api.svc/json/SubmitUrl?apikey={BING_API_KEY}'
for i in range(1, len(backlinks)+1):
    page_url = f"{SITE_URL}/page{i}.html"
    payload = {"siteUrl": SITE_URL, "url": page_url}
    try:
        response = requests.post(endpoint, json=payload)
        print(f"[BING] Submitted: {page_url} -> {response.json()}")
    except Exception as e:
        print(f"[ERROR] {page_url}: {e}")
