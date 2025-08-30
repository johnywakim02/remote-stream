# remote-stream

This project is under construction.
Details coming soon.

## 1. environment setup

To use this project, you have to configure both the python environment and the project-level environment variables.

### 1.a. Python Environement

0. check your version of python and compare with the env_info.txt file.
   ideally, you could use pyenv to get the equivalent version of python and pip for this project

1. create a virtual environment: 
```
python -m venv venv
```

2. activate the venv:
    - on windows:
    `venv/Scripts/activate`
    - on linux/mac:
    `source venv/bin/activate`

3. install the requirements:
    `pip install -r requirements.txt`

4. if you wish to add/remove 3rd party libraries:
    1. add/remove the library's name to/from requirements.in
    2. recompile requirements.in into requirements.txt:
    `pip-compile requirements.in`
    3. synchronize your environment with requirements.txt:
    `pip-sync requirements.txt`

### 1.b. Project-Level Environment Variables

1. Create a `.env` file if you do not have any
2. Copy the content of `.env_example` file and paste it in `.env` file
3. Change the values from the example values given there to real values you would like to use.
   - You can choose the username and password that you like for the stream. When trying to access the stream from any device, you will have to enter these same username and password.

## 3. Launching

> Local Run
> 
>     - To run locally, use:
>       - `python main.py`

<br>

> Public Run
>
> If you'd like to try running on the public internet, use Pinggy to configure a free tunnel. Follow these steps
> - Run Locally in a terminal
> - Open a second terminal and run:
>   - `ssh -p 443 -R0:127.0.0.1:5000 qr@free.pinggy.io`
> - The first time you use pinggy: Enter "yes" to continue connecting. Enter blank password if prompted.
Then later, only enter blank password when prompted
>
> IMP: Pingy Provides two URLs: one with TLS certificate (HTTPS) and another without TLS certificate (HTTP). Always use the HTTPS address to protect your password and data from being intercepted during transmission.