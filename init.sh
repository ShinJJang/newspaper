pip3 install -r requirements.txt   # install python packages used in project
python3 manage.py makemigrations   # make migration config
python3 manage.py migrate          # apply to db
python3 manage.py createsuperuser  # create admin