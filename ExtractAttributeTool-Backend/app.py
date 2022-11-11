from flask import Flask, render_template, request, redirect, g, send_file
from werkzeug.utils import secure_filename
import sys, os, glob
import extractAttributes

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('main.html')

@app.route('/file_upload', methods = ['GET', 'POST'])
def file_upload():
    # 기존 파일 삭제
    for file in os.scandir('./downloadedFile'):
        os.remove(file.path)
    for file in os.scandir('./out'):
        os.remove(file.path)
    if request.method == 'POST':
        f = request.files['file']
        f.save('downloadedFile/' + secure_filename(f.filename))
        return redirect('/process/' + secure_filename(f.filename))
    else: 
        return render_template('main.html')
 
# 파일명 받아서 처리하는 페이지
@app.route('/process/<filename>')
def process(filename):
    outDirectory = "./out"
    csvOut = False
    documents = ['./downloadedFile/' + filename]
    attributes, attributesSN = extractAttributes.processDocuments(documents, outDirectory, csvOut)
    return redirect('/download/' + filename)

@app.route('/download/<filename>')
def Download_File(filename):
    PATH='./out/' + 'attributes.json'
    return send_file(PATH,as_attachment=True)
		
if __name__ == '__main__':
    app.run(debug = True)