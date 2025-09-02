# remote-stream

This project is under construction.
Details coming soon.

<br>
<br>
<br>

## 0. Table of Content

- [remote-stream](#remote-stream)
  - [0. Table of Content](#0-table-of-content)
  - [1. Environment Setup](#1-environment-setup)
    - [1.a. Python Environement](#1a-python-environement)
    - [1.b. Project-Level Environment Variables](#1b-project-level-environment-variables)
  - [2. Launching](#2-launching)
  - [3. Results and Outputs](#3-results-and-outputs)
    - [3.a. Visualizing the Stream from the cameras](#3a-visualizing-the-stream-from-the-cameras)
    - [3.b. Saving images periodically to a folder](#3b-saving-images-periodically-to-a-folder)
  - [4. Project Structure](#4-project-structure)
    - [4.a. main.py](#4a-mainpy)
    - [4.b. core folder](#4b-core-folder)
    - [4.c. utils folder](#4c-utils-folder)
- [Future Steps](#future-steps)
  - [1. Near Future](#1-near-future)
  - [2. Far Future](#2-far-future)

<br>
<br>
<br>

## 1. Environment Setup

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


<br>
<br>
<br>

## 2. Launching

This program can run indefinitely on a private network. It can also be temporarily exposed to the public internet using Pinggy's free tunnel, for testing purposes. Better alternatives are currently being explored.

> Local Run
> 
> - To run locally, use:
>   - `python main.py`

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


<br>
<br>
<br>

## 3. Results and Outputs

- After you launch the project, you will get 2 features for now:
  - Visualizing the Stream from the cameras
  - Saving images periodically to a folder

### 3.a. Visualizing the Stream from the cameras

> Local Network
>
> On you local network (home network, etc...), you can access the stream from any device at http://<ip>:<port>
>
> The `ip` to use is the one of your PC that launches this program. When you launch, flask will provide it for you (as well as the port).
> Ex:
> ```
> * Running on all addresses (0.0.0.0)
> * Running on http://localhost:5000
> * Running on http://<your-local-ip>:5000
> ```
> 
> In the example above, any device on this local network can access the stream of the cameras at `http://<your-local-ip>:5000`

<br>

> Public Network
> 
> For now we use Pinggy to create a tunnel to the public internet.
> This allows us to see the stream for the duration of 1 hour, for free. 
>
> Pinggy will provide you with a url on which you can visualize the stream. Please use the HTTPS version and not the HTTP version to guarantee the security of the password you use when accessing the page.

### 3.b. Saving images periodically to a folder

The app also saves images periodically to a folder (each 5 seconds by default). 

By default, the save folder is named `saved_img`. Inside, you will get a subfolder for each camera. This subfolder will either be named `camera_<index>` or `camera_<name>`.

In a particular camera's subfolder, the images are saved in the following format: `hh_mm_ss.jpg`
  - hh: the hour (between 0 and 23)
  - mm: the minute (between 0 and 60)
  - ss: the second (between 0 and 60)
  
So for example:
  - 07_18_53.jpg means that the image was taken and 7 o'clock, 18 minutes and 53 seconds, AM. 
  - 15_46_21.jpg means that the image was taken a 3 o'clock, 46 minutes and 21 seconds, PM

By default, each time you run the program again, all existing images are deleted (for now). This allows memory space consumption to stay controlled as of the current version of this program.

<br>
<br>
<br>

## 4. Project Structure

This project has 3 main parts:
- main.py file
- core folder
- utils folder

### 4.a. main.py

The main program file that one should run ideally. It serves as a singular entry point to access the functionalities of this project.

### 4.b. core folder

The core folder contains packages that provide the main functionalities of the project, such as the `camera` and `server` packages.

It differs from the utils folder in that it groups central, essential functionalities rather than generic, reusable helper modules.

### 4.c. utils folder

It groups helper modules that can be used both in the core folder's packages and in main.py.

These are useful for logging, retries, and other miscellaneous, convenient utilities.


# Future Steps

## 1. Near Future

- Calculating save space consummed by hour
- Add folder for the year_month_day when taking images
- Integrating WiFi cameras through RTSP or ONVIF 
- Allow for streaming publicly without the use of temporary tunnels

## 2. Far Future

- Detect Objects and take a close-up of them