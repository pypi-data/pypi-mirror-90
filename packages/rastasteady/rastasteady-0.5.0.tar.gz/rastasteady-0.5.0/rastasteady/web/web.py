#!/usr/bin/env python
# coding=utf-8

# based on https://gist.github.com/dAnjou/2874714

from flask import Flask, flash, render_template, request, jsonify
from werkzeug.utils import secure_filename
from rastasteady.rastasteady import RastaSteady
import os
import pathlib
from persistqueue import Queue
import threading
import uuid

# default configuration
DEBUG = os.environ.get('DEBUG', True)
PORT = os.environ.get('PORT', 8080)
UPLOAD_PATH = os.environ.get('UPLOAD_FOLDER', 'uploads')
UPLOAD_EXTENSIONS = set(['mp4', 'txt'])

# inintialize Flask
app = Flask(__name__)
app.secret_key = 'djistabilizationsoftware'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['UPLOAD_PATH'] = UPLOAD_PATH
app.config['UPLOAD_EXTENSIONS'] = UPLOAD_EXTENSIONS

# compose upload dir
uploaddir = os.path.join(str(os.getcwd()), app.config['UPLOAD_PATH'])

# initialize the pending files queue
pending = Queue(os.getcwd() + '/queue', autosave = True)

# check if a filename is valid based on its extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['UPLOAD_EXTENSIONS']

# process a file in a new thread
def processInThread(filename = ''):
    # calculate input directory and temporary location
    inputpathlib = pathlib.Path(filename)
    tmppathlib = pathlib.Path(str(inputpathlib.parent) + '/tmp/.placeholder')

    myVideo = RastaSteady(inputpathlib, tmppathlib, verbose = 0)
    myVideo.stabilize()

# process the next file if possible
@app.route('/api/process', methods = ['GET'])
def process():
    if pending._qsize() == 0:
        return jsonify(
            status = 200,
            result = 'empty',
            pending = str(pending._qsize()),
            working = threading.active_count() - 3,
            msg = 'No hay ficheros pendientes de procesar'
        )

    if threading.active_count() < 5:
        # get next item in queue
        filename = pending.get()

        # process it in another thread
        videoThread = threading.Thread(target = processInThread, args = (filename,))
        videoThread.start()

        return jsonify(
            status = 200,
            result = 'ok',
            pending = str(pending._qsize()),
            working = threading.active_count() - 3,
            msg = 'Iniciado proceso de video %s' % filename
        )

    return jsonify(
        status = 200,
        result = 'pending',
        pending = str(pending._qsize()),
        working = threading.active_count() - 3,
        msg = 'Todos los recursos ocupados. Por favor espera.'
    )

# main route
@app.route('/')
def index():
    return render_template('index.html')

# returns the status of the queue and jobs
@app.route('/api/status', methods = ['GET'])
def size():
    return jsonify(
        status = 200,
        result = 'ok',
        pending = str(pending._qsize()),
        working = threading.active_count() - 3,
    )

# upload a file and enqueue it
# TODO: more error detection when saving the file
@app.route('/api/upload', methods = ['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        fileuuid = uuid.uuid4()
        filedir = os.path.join(uploaddir, str(fileuuid))
        os.mkdir(filedir)

        file.save(os.path.join(filedir, secure_filename(file.filename)))
        pending.put(os.path.join(filedir, secure_filename(file.filename)))

        return jsonify(
            status = 200,
            result = 'ok',
            pending = str(pending._qsize()),
            working = threading.active_count() - 3,
            msg = 'Video ' + file.filename + ' subido correctamente<br/>No cierres esta ventana, de lo contrario el perderás tu sitio en la cola y tendras que comenzar de nuevo',
            uuid = fileuuid
        )
    else:
        return jsonify(
            status = 400,
            result = 'error',
            pending = str(pending._qsize()),
            working = threading.active_count() - 3,
            msg = 'Error: Error en el envío o extensión invalida'
        )

# runs the server
def web():
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

# main function
if __name__ == '__main__':
    if not os.path.exists(uploaddir):
        os.mkdir(uploaddir)
    web()
