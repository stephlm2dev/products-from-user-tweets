Products from user tweets
=========================

Display a set of products depends on user tweets

Requirements
------------

```shell
[sudo] pip install django
[sudo] pip install tweepy
[sudo] pip install nltk
[sudo] pip install hunspell
[sudo] pip install python-amazon-product-api
```

### Nltk

```shell
sudo python
>> import nltk
>> nltk.download()
```

File → Change Download Directory
  * C:\nltk_data (Windows)
  * /usr/local/share/nltk_data (Mac)
  * /usr/share/nltk_data (Unix)

Install 'all-corpora' package

[More details on 'Installing NLTK Data'](http://www.nltk.org/data.html)

### Hunspell

TODO

Server
------

```shell
cd project/
python2.7 manage.py runserver
```

[http://localhost:8000/schmilka/](http://localhost:8000/schmilka/)

Information
-----------

[SocialMediaParse](https://github.com/seandolinar/socialmediaparse)
