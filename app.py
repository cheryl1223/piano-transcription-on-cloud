from flask import Flask, render_template, request, make_response, jsonify, send_file
import os
import glob
from transcribe import transcribe_file
import time

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

output_name = ""

# @app.route('/', methods=['GET'])
# def upload():
#     display_text = ''
#     return render_template('index.html',display_text= display_text,download = False)

@app.route('/', methods=['GET','POST'])
def run_transcribe():
    if request.method == 'POST':
        global output_name
        for f in glob.glob("*.png") + glob.glob("*.mid") +  glob.glob("*.flac") +  glob.glob("*.wav") +  glob.glob("*.mp3"):
            os.remove(f)
        file = request.files['file']
        model_name = str(request.form.get('model'))
        file_name = file.filename
        print('Filename-->'+file_name)
        file.save(file_name)
        partial_name = file_name.split(".")[0]
        flac_name = "converted.flac"
        os.system("ffmpeg -y -i " + file_name+ " -sample_fmt s16 -ac 1 -ar 16000 " + flac_name)
        # time.sleep(10)
        # transcribe_file(model_name,flac_name,'.',None,0.5,0.5)
        
        os.system("python transcribe.py "+ model_name + " "+ flac_name)
        display_text = 'The file is ready to download'
        output_name = flac_name +'.' + model_name+ ".pred.mid"
        print(output_name + "::" + file_name)
        # return render_template('index.html',display_text = display_text,download=True)
        return send_file(output_name, attachment_filename=output_name, as_attachment=True)
    else:
        return render_template('index.html',download=False)

@app.route('/download', methods=['POST'])
def download():
    global output_name
    print('Output File-->' + output_name + "::" + str(os.path.exists(output_name)))
    if os.path.exists(output_name):
        return send_file(output_name, attachment_filename=output_name, as_attachment=True)
    else:    
        return render_template('index.html',download=True)



if __name__ == '__main__':
    app.run("0.0.0.0")
