### Install Django

`pip3 install Django`

### Create a project

`django-admin startproject PROJECT_NAME`

### Run web application

`python3 manage.py runserver`

Depending on which python you have installed on your PC, you probably need to use `python` instead of `python3` in the above command. If `manage.py` is not in your current directory, you also need to add path before the file.

After executing the above command, the output shows `starting development server at http://127.0.01:8000`. Copy the url to the browser and you will see a default Django web page.

### Create a Django app

`python3 manage.py startapp <app_name>`

Then add the app name to the `seetings.py` file in the *Application definition*. Later, develop your application in the `views.py` file.

Now create an `urls.py` file in the application folder, and define what urls are allowed in this application. 

Lastly, we need to go the project's ´urls.py´ file and add the application url by `path('hello/', include("hello.urls"))` to the project urls.