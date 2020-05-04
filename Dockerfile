FROM python:3.7-slim


MAINTAINER Yuxiao Xie (yx1885@nyu.edu)

ADD requirements.txt .
RUN apt-get update 
RUN apt-get install -y git
RUN pip install -r requirements.txt --user
ADD model-500000.pt .
ADD transcribe.py .
ADD train.py .
ADD evaluate.py .
ADD /onsets_and_frames ./onsets_and_frames
ADD /templates ./templates
ADD app.py .
RUN apt-get install -y libsndfile-dev
#CMD ["python", "train.py", "with", "logdir=runs/model","iterations=100"]
CMD ["python","app.py"]
