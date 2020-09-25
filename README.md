### NSC 325 Rod Pump Optimization Project

### Conoco Phillips / The University of Texas at Austin

---

#### Setting up your environment on Windows:

Check if Python 3 is installed by running `python --version` from the command prompt.

If it is not yet installed, download and install python from <https://www.python.org/downloads/windows>.  Click on Python 3.8.6 and scroll down until you find the executable installer.

Clone the github repository to your local machine and navigate to the repository in command prompt.

Update pip using `python -m pip install --upgrade pip`.

Install virtualenv using `python -m pip install --user virtualenv`.

Create a new virtualenv in the cloned repository using `python -m venv venv`.

Activate the virtualenv using `.\venv\Scripts\activate`.

Install all necessary packages using `pip install -r requirements.txt`.

When you're done, deactivate the virtualenv using `deactivate`.

#### Setting up your environment on MacOS or Windows:

Check if Python is installed by running `python3 --version`.

Clone the github repository to your local machine and navigate to the repository in command prompt.

Update pip using `python3 -m pip install --upgrade pip`.

Install virtualenv using `python3 -m pip install --user virtualenv`.

Create a new virtualenv in the cloned repository using `python3 -m venv venv`.

Source the virtual environment: `source venv/bin/activate`.

Update pip again to update pip inside the virtualenv: `pip install -U pip`  

Install requirements.txt: `pip install -r requirements.txt`  

---

#### Launching Jupyter Notebook

If you have not already, source the virtualenv using `source venv/bin/activate` on MacOS/Linux or `.\venv\Scripts\Activate` on Windows.

Open Jupyter Notebook: `jupyter notebook`  

---

#### Other useful links

Git cheatsheet: https://rogerdudler.github.io/git-guide/

Markdown cheatsheet: https://github.com/adam-p/markdown-here/wiki/Markdown-Here-Cheatsheet

