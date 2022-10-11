FROM osgeo/gdal:ubuntu-full-3.5.2
RUN apt -y update
RUN apt -y install python3-pip libspatialindex-dev
WORKDIR /tmp
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
# launch jupyter notebook
#CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
