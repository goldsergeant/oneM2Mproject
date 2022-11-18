from flask import Flask, render_template, request, redirect, g, send_file
from werkzeug.utils import secure_filename
import sys, os, glob
import extractAttributes
import io
import zipfile
import time

app = Flask(__name__)

# @app.before_request
# def before_request():
#     # csv, dup 받아오기
#     g.csv_checked = request.form.get('csv')
#     g.dup_checked = request.form.get('dup')


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/process', methods = ['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        csv_checked = 'csv' in request.form
        dup_checked = 'dup' in request.form

        # 기존 파일 삭제
        for file in os.scandir(f'.{os.path.sep}downloadedFile'):
            os.remove(file.path)
        for file in os.scandir(f'.{os.path.sep}out'):
            os.remove(file.path)

        outDirectory = f'.{os.path.sep}out'
        csvOut = False
        documents = []
        for f in files:
            # file extension check
            if secure_filename(f.filename).endswith(".docx") == False:
                return render_template('main.html', err = "docx 파일만 업로드 가능합니다.")
            f.save(f'downloadedFile{os.path.sep}' + f.filename)
            documents.append(f'downloadedFile{os.path.sep}' + f.filename)
        attributes, attributesSN = extractAttributes.processDocuments(documents, outDirectory, csvOut)

        # TODO csv나 dup 옵션 받아서 처리
        if not attributes:
            exit(1)
        if csv_checked:
            extractAttributes.printAttributeCsv(attributes, outDirectory)
        if dup_checked:
            extractAttributes.printDuplicateCsv(attributes, attributesSN, outDirectory)


        if csv_checked or dup_checked:
            return redirect('/download')
        else:
            return send_file(f'.{os.path.sep}out{os.path.sep}' + 'attributes.json', as_attachment=True)
    else: 
        return redirect('/')
 
		
@app.route('/download', methods = ['GET', 'POST'])
def download():
    file_path = f'.{os.path.sep}out'

    zip_file = zipfile.ZipFile(file_path + f"{os.path.sep}output.zip", "w")  # "w": write 모드
    for file in os.listdir(file_path):
        if file.endswith(".zip"):
            continue
        zip_file.write(os.path.join(file_path, file), compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()

    return send_file(f'.{os.path.sep}out{os.path.sep}' + 'output.zip', as_attachment=True)


if __name__ == '__main__':
    app.run(debug = True)