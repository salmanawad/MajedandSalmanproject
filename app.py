from flask import Flask, request, render_template_string
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
    result = ""
    if request.method == "POST":
        url = request.form.get("url")
        if not is_valid_url(url):
            result = "<p style='color:red'>❌ الرابط غير صالح</p>"
        else:
            final_url, html = trace_redirects(url)
            if not final_url:
                result = "<p style='color:orange'>⚠️ تعذر تتبع الرابط</p>"
            else:
                status = "⚠️ مشبوه" if is_tracking_url(final_url) else "✅ آمن"
                result = f"<p><b>URLTrap كشف:</b> {status}</p><p>الرابط النهائي: {final_url}</p><hr><p><b>روابط داخل الصفحة:</b></p>"
                for link in extract_links(html or ""):
                    label = "⚠️" if is_tracking_url(link) else "✅"
                    result += f"<p>{label} {link}</p>"
    return render_template_string(f"""
    <html dir="rtl" style="background:#222;color:#eee;font-family:tahoma;">
      <head><title>URLTrap</title></head>
      <body><h2>🔍 URLTrap</h2>
        <form method="post">
          <input name="url" placeholder="أدخل الرابط" style="width:300px;padding:5px;">
          <button type="submit" style="padding:5px;">فحص</button>
        </form><div style="margin-top:20px;">{result}</div>
      </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
