from __future__ import print_function

import os
import torch
import torch.nn as nn

from flask import Flask, render_template, request, make_response, jsonify, send_file
from pydub import AudioSegment


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # file_wav = request.files['file']
        # file_name = file_wav.filename.split('.wav')[0]
        # file_flac = "%s.flac" % file_name
        # song = AudioSegment.from_wav(file_wav.filename)
        # song.export(file_flac, format="flac")
        # os.system("python transcribe.py model-500000.pt " + file_flac)
        # return send_file(file_flac,
        #                  attachment_filename=file_flac,
        #                  as_attachment=True)
        file = request.files['file']
        file_name = file.filename
        os.system("python transcribe.py model-500000.pt " + file_name)
        output_name = file_name + ".pred.mid"
        return send_file(output_name,
                         attachment_filename=output_name,
                         as_attachment=True)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run("0.0.0.0")
