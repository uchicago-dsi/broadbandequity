FROM osgeo/gdal:ubuntu-full-3.5.2
RUN apt -y update
RUN apt -y install python3-pip libspatialindex-dev
WORKDIR /tmp
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# launch jupyter notebook
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
