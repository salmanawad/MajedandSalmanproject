from flask import Flask, request, render_template
import requests, validators
from bs4 import BeautifulSoup

app = Flask(__name__)

def is_valid_url(url):
    return validators.url(url)

def trace_redirects(url):
    session = requests.Session()
    try:
        r = session.get(url, allow_redirects=True, timeout=10)
        return r.url, r.text
    except:
        return None, None

def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    return [a["href"] for a in soup.find_all("a", href=True)]

def is_tracking_url(url):
    keywords = ["track", "spy", "log", "ads", "click", "redirect"]
    return any(word in url.lower() for word in keywords)

@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    final_url = ""
    status = ""
    if request.method == "POST":
        url = request.form.get("url")
        if not is_valid_url(url):
            status = "❌ الرابط غير صالح"
        else:
            final_url, html = trace_redirects(url)
            if not final_url:
                status = "⚠️ تعذر تتبع الرابط"
            else:
                status = "⚠️ مشبوه" if is_tracking_url(final_url) else "✅ آمن"
                links = extract_links(html or "")
                for link in links:
                    label = "⚠️" if is_tracking_url(link) else "✅"
                    result.append((label, link))
    return render_template("index.html", result=result, final_url=final_url, status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
