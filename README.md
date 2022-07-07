https://cs50.harvard.edu/web/2020/

A very good explanation about Django Form [here](https://www.geeksforgeeks.org/render-html-forms-get-post-in-django/).

### Some notes taken from the course

1. Django notes: [Django/](https://github.com/AIXjing/web50/tree/main/Django)


2. Javascript notes: [Javascript/](https://github.com/AIXjing/web50/tree/main/Javascript)

3. Python [notes](https://github.com/AIXjing/web50/blob/main/python_notes/python_node.md)

4. CI/CD 

    CI/CD can be implemented by GitHub Actions. To do so, we can make a *yaml* file and create a workflow. 

    Create a `workflows` directory under`.github`, and then create a `ci.yml` file with the following code in the `workflows` directory. 

    ```yml
    name: Testing
    on: push # define which action will triger it to run the code

    # define what actions will happen
    jobs:
        test_project:
            # which type of virtual machine
            runs-on:ubuntu.latest 
            steps: 
                # specify what steps will happen
                uses: actions/checkout@v2
                name: Run Django unit tests
                run:
                    pip3 install --user django
                    python3 manage.py test
    ```

5. Docker

    To deploy application independent on developers' work environment, we can use a Docker container by creating a *Dockerfile*.

    A dockerfile describes instructions for creating a Docker container where the Docker image represents all of the libraries and other installed items. Based on that image, we're able to create a whole bunch of containers that are all based on that same image where each container has its own files and can run the web application inside of it.

    ```dockerfile
    FROM python3
    # copy all the files in my current directory to where I want to store my application (a container)
    COPY . /usr/src/app 
    # use the created container as my working directory
    WORKDIR /usr/src/app 
    RUN pip install -r requirements.txt
    CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
    ```

    Docker compose: allows us to compose different servers by creating a `docker-compose.yml`

    ```yml
    version: 3

    services:
        db: 
            image: postgres

        web:
            build:
            volumes:
                -.:/usr/src/app
            ports:
                -"8000:8000"
    ```

    run `docker-compose up` in the command line to start up the application, which is inside the container.

    Enable to execute a command inside a container, we need to specify which container we are gonna use. `docker exec -it <container_id> bash -l` Once we are in the container, we can run any commands like run on your computer. 