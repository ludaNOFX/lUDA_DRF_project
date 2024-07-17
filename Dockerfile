FROM python:3.10-buster

RUN useradd LUDA_DRF_API

WORKDIR /home/LUDA_DRF_API

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY django_luda_project django_luda_project
COPY manage.py ./

COPY boot.sh ./
RUN chmod a+x boot.sh

RUN chown -R LUDA_DRF_API:LUDA_DRF_API ./

USER LUDA_DRF_API

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]