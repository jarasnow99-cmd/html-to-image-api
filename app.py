import os
from flask import Flask, request, send_file
from playwright.sync_api import sync_playwright
import io

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_html():
    data = request.get_json()
    html_code = data.get('html', '')

    if not html_code:
        return {'error': 'No HTML provided'}, 400

    with sync_playwright() as p:
        # تشغيل المتصفح بوضع Headless
        browser = p.chromium.launch(headless=True)
        # إعداد مقاس إنستغرام العمودي 1080x1440 (نسبة 3:4)
        page = browser.new_page(viewport={"width": 1080, "height": 1440})
        page.set_content(html_code)
        
        # التقاط الصورة
        img_bytes = page.screenshot(type="png")
        browser.close()

    return send_file(
        io.BytesIO(img_bytes),
        mimetype='image/png'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)