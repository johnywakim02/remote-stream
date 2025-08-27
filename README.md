# remote-stream

This project is under construction.
Details coming soon.

## 1. environment setup

To use this project.

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