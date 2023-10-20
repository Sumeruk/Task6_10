from flask import Flask, render_template, request
from docx import Document
from odf import text, teletype
import difflib

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file1 = request.files['file1']
    file2 = request.files['file2']
    file1_text = extract_text(file1)
    file2_text = extract_text(file2)
    diff = difflib.ndiff(file1_text.splitlines(), file2_text.splitlines())

    first_subs = []
    second_subs = []
    for line in diff:
        if line.startswith('-'):
            first_subs.append(line[2:])
        else:
            second_subs.append(line[2:])

    return render_template('diff.html', diff=diff)


def extract_text(file):
    if file.filename.endswith('.docx'):
        doc1 = Document(file)
        text1 = '\n'.join([para.text for para in doc1.paragraphs])
        return text1
    elif file.filename.endswith('.odt'):
        doc1 = text.load(file)
        text1 = teletype.extractText(doc1)
        return text1
    else:
        return 'Unsupported file type'


if __name__ == '__main__':
    app.run(debug=True)
