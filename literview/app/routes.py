from flask import render_template, request

from app import app

@app.after_request
def add_header(r):    
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Expires"] = "0"
    r.headers["Pragma"] = "no-cache"

    return r

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')

@app.route('/search', methods=['GET','POST'])
def search():

    from .pipeline import run

    html = run(base_keywords=request.form['base_keywords'],
               n=int(request.form['sample_size']),
               class_keywords=request.form['class_keywords'],
               class_name=request.form['class_label'])

    return render_template('result.html', title=request.form['base_keywords'], html=str(html))
