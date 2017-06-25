"""
Flask App for Paper Git as a front end.
"""
import markdown

from flask import (
    Flask, render_template, redirect, url_for, jsonify, flash, Markup)
from paper_to_git.models import PaperDoc, PaperFolder


app = Flask(__name__)
app.secret_key = 'thenewsecretkeyforflashingandsessionmanagement'


@app.route('/', methods=['GET'])
def index():
    docs = PaperDoc.select()
    return render_template('index.html',
                           docs=PaperDoc.select().order_by(PaperDoc.last_updated.desc()),
                           folders=PaperFolder.select())


@app.route('/update/<doc_id>', methods=['POST'])
def update_document(doc_id):
    doc = PaperDoc.get_by_paper_id(doc_id)
    doc.get_changes()
    return jsonify(message="The document was successfully updated",
                   type="success")


@app.route('/document/<doc_id>', methods=['GET'])
def view_document(doc_id):
    doc = PaperDoc.get_by_paper_id(doc_id)
    fs_path = PaperDoc.generate_file_path(doc.paper_id)
    with open(fs_path) as fp:
        file_content = Markup(markdown.markdown(fp.read()))
        return jsonify(document=file_content,
                       title=doc.title)


@app.route('/refresh', methods=['GET'])
def refresh():
    PaperDoc.sync_docs()
    flash("Refreshed changes from Dropbox!")
    return redirect(url_for('index'))
