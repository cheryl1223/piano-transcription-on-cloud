import torch
import torch.nn as nn

from flask import Flask, render_template, request, make_response, jsonify, send_file
#from pydub import AudioSegment

from transcribe import *
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

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
        # attachment_filename=file_flac,
        # as_attachment=True)
        file = request.files['file']
        model_name = str(request.form.get('model'))
        file_name = file.filename
        #file_path = os.path.join(APP_ROOT, file_name)
        #file.save(file_path)
        file.save(file_name)
        #partial_name = file_path.split(".")[0]
        #flac_name = partial_name + ".flac"
        #os.system("ffmpeg -y -i " + file_path + " -ar 16000 "+ flac_name)
        #transcribe_file(model_file="model-500000.pt", flac_paths=file_path)
        os.system("python transcribe.py "+ model_name + " "+ file_name )
        output_name = file_name +'.'+model_name+ ".pred.mid"
        #os.remove(file_path)
        os.remove(file_name)
        #os.remove(output_name)
        return send_file(output_name, attachment_filename=output_name, as_attachment=True)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run("0.0.0.0")
