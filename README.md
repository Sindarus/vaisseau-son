# Installation instructions

Make sure you have python 3 installed<br/>
`python3 -V`

If you don't have the pip3 module manager, install it with<br/>
`sudo apt install python3-pip`

## setup a new virtual env
If you don't have virtualenv installed, install it with<br/>
`pip3 install virtualenv`

Create a new virtual env just for this project.<br/>
`virtualenv path_to_new_env -p python3`<br/>
Replace `path_to_new_env` by the path to the directory that you want virtualenv to create to store the new environment, preferably outside the directory of the project.

Activate the newly create virtualenv.<br/>
`source path_to_new_env/bin/activate`<br/>
You should now see the name of the new environement appear next to your command line prompt. When you are done running the project, you can return to using your global python by running `deactivate`.

## Install required python modules with `pip -r`

You can now install this project's python requirements with pip, using the `requirements.txt` file

`cd vaisseau-son`<br/>
`pip install -r requirements.txt`

## Install other dependancies
Install ffmpeg<br/>
`sudo apt install ffmpeg`

Install sphinx (if you want to build the docs)<br/>
`sudo apt install sphinx`

# Documentation
The documentation was written for use by Sphinx and its the autodoc plugin. To generate the documentation from the source code, add the project's directory to your python path (so that Sphinx can import the modules):<br/>
`export PYTHONPATH="${PYTHONPATH}:/path_to_Vaisseau_son"`

Then run `make html` inside the `docs/` directory.<br/>
`cd docs`<br/>
`make html`

Open `docs/_build/html/index.html` in a web browser to read the documentation.

# Tips
### Tip for debugging
Set the `QT_DEBUG_PLUGINS` environement variable to `1` to enable more verbosity about plugins
`export QT_DEBUG_PLUGINS="1"`.

