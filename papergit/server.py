"""
Flask App for Paper Git as a front end.
"""
import markdown
import traceback

from flask import (
    Flask, render_template, redirect, url_for, jsonify, flash, Markup,
    send_from_directory)
from papergit.models import PaperDoc, PaperFolder


app = Flask(__name__, static_url_path='')
app.secret_key = 'thenewsecretkeyforflashingandsessionmanagement'


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('templates/static', path)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
        docs=PaperDoc.select().order_by(PaperDoc.last_updated.desc()),
        folders=PaperFolder.select())


@app.route('/update/<doc_id>', methods=['POST'])
def update_document(doc_id):
    doc = PaperDoc.get_by_paper_id(doc_id)
    doc.get_changes()
    return jsonify(message="The document was successfully updated",
                   type="success")


@app.route('/publish/<doc_id>', methods=['POST'])
def publish_document(doc_id):
    doc = PaperDoc.get_by_paper_id(doc_id)
    _, final_path = doc.sync_path
    try:
        doc.publish()
        print("{} was published".format(doc))
        return jsonify(message="Document successfully published at {}".format(final_path),  # noqa
                       type="success")
    except Exception as e:
        print("Error {0} occurred while publishing {1}".format(str(e), doc))
        traceback.print_exc()
        return jsonify(message="Error occurred while publishing\n{}".format(str(e)),       # noqa
                       type="danger")


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
