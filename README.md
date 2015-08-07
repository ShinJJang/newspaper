# Newspaper
Newspaper project is similar project with Hacker News. This appliction is built on django 1.7 and Python 3.4.

# Installation
On termial, type below:

```
$ init.sh
```
Equivalent to,

```
$ pip3 install -r requirements.txt	 # install python packages used in projcet
$ python3 manage.py makemigrations   # make migration config
$ python3 manage.py migrate          # apply to db
$ python3 manage.py createsuperuser  # create admin
```

# Run
On termial, type below:
```
$ run.sh
```
Equivalent to,

```
$ python3 manage.py runserver        # run server
```

# Used module
* Django==1.7
* beautifulsoup4==4.4.0
* django-tastypie==0.12.2

