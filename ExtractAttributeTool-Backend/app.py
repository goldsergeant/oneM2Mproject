from flask import Flask, render_template, request, redirect, g, send_file, after_this_request, Response
from werkzeug.utils import secure_filename
import sys, os, glob
import extractAttributes
import zipfile
import io
import pathlib
import time
import random
import shutil

app = Flask(__name__)

# @app.before_request
# def before_request():
#     # csv, dup 받아오기
#     csv_checked = request.form.get('csv')
#     dup_checked = request.form.get('dup')


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/process', methods = ['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        csv_checked = 'csv' in request.form
        dup_checked = 'dup' in request.form

        csvOut = False
        documents = []
        num = 0

        while True:
            try:
                num = random.randrange(0, 1000)
                directory = f'downloadedFile{num}{os.path.sep}'
                outDirectory = f'.{os.path.sep}out{num}'

                if not os.path.exists(directory):
                    os.makedirs(directory)
                    os.makedirs(outDirectory)
                    break
            except:
                continue

        for f in files:
            # file extension check
            if secure_filename(f.filename).endswith(".docx") == False:
                return render_template('main.html', err = "docx 파일만 업로드 가능합니다.")
            f.save(f'{directory}{os.path.sep}' + f.filename)
            documents.append(f'{directory}{os.path.sep}' + f.filename)
        attributes, attributesSN = extractAttributes.processDocuments(documents, outDirectory, csvOut)

        # TODO csv나 dup 옵션 받아서 처리
        if not attributes:
            exit(1)
        if csv_checked:
            extractAttributes.printAttributeCsv(attributes, outDirectory)
        if dup_checked:
            extractAttributes.printDuplicateCsv(attributes, attributesSN, outDirectory)


        
        # 파일 삭제
        @after_this_request
        def remove_file(response):
            try:
                shutil.rmtree(directory)
                shutil.rmtree(outDirectory)
            except Exception as error:
                app.logger.error("Error removing or closing downloaded file handle", error)
            return response


        if csv_checked or dup_checked:
            base_path = pathlib.Path(f'.{os.path.sep}out{num}{os.path.sep}')
            data = io.BytesIO()
            with zipfile.ZipFile(data, mode='w') as z:
                for f_name in base_path.iterdir():
                    z.write(f_name)
            data.seek(0)
            return send_file(
                data,
                mimetype='application/zip',
                as_attachment=True,
                download_name='output.zip')

        else:
            file_path = pathlib.Path(f'.{os.path.sep}out{num}{os.path.sep}attributes.json')
            data = io.BytesIO()
            with open(file_path, 'rb') as fo:
                data.write(fo.read())
            # (after writing, cursor will be at last byte, so move it to start)
            data.seek(0)

            return send_file(
                data, 
                mimetype='application/json',
                as_attachment=True,
                download_name='attributes.json')
    else: 
        return redirect('/')
 
		
if __name__ == '__main__':
    app.run(debug = True, threaded=True)