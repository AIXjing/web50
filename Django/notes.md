### Install Django

`pip3 install Django`

### Create a project

`django-admin startproject PROJECT_NAME`

### Run web application

`python3 manage.py runserver`

Depending on which python you have installed on your PC, you probably need to use `python` instead of `python3` in the above command. If `manage.py` is not in your current directory, you also need to add path before the file.

After executing the above command, the output shows `starting development server at http://127.0.01:8000`. Copy the url to the browser and you will see a default Django web page.

### Create a Django app

#### General steps

First create an application by executing

`python3 manage.py startapp <app_name>`

Then add the app name to the `settings.py` file in the *Application definition*. Later, develop your application in the `views.py` file. For example,

```py
def index(request):
    return render(request, "hello/index.html")
```

*index.html* is the default url for an application.

Now create an `urls.py` file in the application folder, and define what urls are allowed in this application by typing the following codes. 

```py
urlpatterns = [
    path("", views.index, name="index")
]
```

Lastly, we need to go the project's ´urls.py´ file and add the application url by `path('hello/', include("hello.urls"))` to the project urls.

#### Parameterize request

Aside from *index.html*, we could also create other urls in the application. To do so, we can define functions like:

```py
def greet(request):
    return HttpResponse("Hello, world!")
```

To make it more *generic*, i.e., to greet whoever with a given name, we could pass another parameter to the function:

```py
def greet(request,name):
    return HttpResponse(f"Hello, {name}!")
```

In the curly brackets, we can also pass a method, e.g., `name.capitcalize()` to capitalize the give name.

In the application *urls.py* file, we need to add *greet* url accordingly `path("<str:name>", views.greet, name="greet")` with `name` passing as a variable.


#### render url

Aside from requesting a web page, we can also render the whole url in the application, which helps seperate python and html logic.

```py
def index(request):
    return render(request, "hello/index.html")
```

Then create a folder named *templates*. Under the *templates* folder, create a folder named as the same as the application name, e.g., *hello*; and under this folder, create a `index.html` file where we can write html.

Additionally, we can added the third arguement (a dict) to pass a variable to the html file in the `render()` method, e.g.,

```py
def greet(request, name):
    return render(request, "hello/greet.html", {
        "name" : name.capitalize()
    })
```

In the `templates/hello/index.html` file, we can pass the *name* variable by using {{ name }}. If we need to write python logic in the html file, use {% python code %} fomart.





