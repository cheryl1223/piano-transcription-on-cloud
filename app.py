from flask import Flask, render_template, request, make_response, jsonify, send_file
import os
import glob

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for f in glob.glob("*.png") + glob.glob("*.mid") +  glob.glob("*.flac") +  glob.glob("*.wav") +  glob.glob("*.mp3"):
            os.remove(f)
        file = request.files['file']
        model_name = str(request.form.get('model'))
        file_name = file.filename
        file.save(file_name)
        partial_name = file_name.split(".")[0]
        flac_name = partial_name + ".flac"
        os.system("ffmpeg -y -i " + file_name+ " -sample_fmt s16 -ac 1 -ar 16000 " + flac_name)
        os.system("python transcribe.py "+ model_name + " "+ flac_name)
        output_name = flac_name +'.' + model_name+ ".pred.mid"
        return send_file(output_name, attachment_filename=output_name, as_attachment=True)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run("0.0.0.0")