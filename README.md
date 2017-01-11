# Newspaper
Newspaper project is similar project with Hacker News. This appliction is built on django 1.10 and Python 3.5.x

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

# Test
Now, this project have one test about title parsing from URL.
```
$ python3 manage.py test
```

# Used module
* beautifulsoup4==4.5.3
* Django==1.10.5
* django-tastypie==0.13.3
* python-dateutil==2.6.0
* python-mimeparse==1.6.0
* six==1.10.0

