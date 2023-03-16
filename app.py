from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kebcuevas:v2_42Cf9_eBxPsZrNW98RSUepEgpTMTk@db.bit.io:5432/kebcuevas.sampledb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URLHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_url = db.Column(db.String(500), nullable=False)
    output_url = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<URLHistory {self.input_url}>'

def glb_scraper(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("lang=en")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome("chromedriver", options=options)

    driver.get(url)

    time.sleep(5)

    button_text_regex = re.compile(r"See\s+This\s+Item\s+in\s+3D", re.IGNORECASE)
    button_element = driver.find_element(by=By.XPATH, value="//button[@aria-label='See this item in 3D']")

    button_element.click()

    time.sleep(25)

    dialog_source = driver.page_source
    urls = re.findall(r'((?:http|ftp)s?://\S+\.glb)', dialog_source)[0]

    driver.quit()

    return urls

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        glb_url = glb_scraper(url)
        
        url_history = URLHistory(input_url=url, output_url=glb_url)
        db.session.add(url_history)
        db.session.commit()

        return render_template('result.html', glb_url=glb_url)
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
