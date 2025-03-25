#This docker file is the foundation of the decoy ssh honeypot container
#References the requrements file using the external Paraminko library
FROM python:3

WORKDIR /usr/src/app

#setup all variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#install all the required dependancies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["ssh_honeypot_main.py","-p","2222"]
ENTRYPOINT ["python3"]
