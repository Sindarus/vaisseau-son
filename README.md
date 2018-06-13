# Installation instructions

Make sure you have python 3 installed<br/>
`python3 -V`

Install pip module manager<br/>
`sudo apt install python3-pip`

Install pyqt5<br/>
`pip3 install pyqt5`

Install ffmpeg<br/>
`sudo apt install ffmpeg`

Install sphinx<br/>
`sudo apt install sphinx`

# Documentation
The documentation was written for use by Sphinx and its the autodoc plugin. To generate the documentation from the source code, add this directory to your python path (so that Sphinx can import the modules) :<br/>
`export PYTHONPATH="${PYTHONPATH}:/path_to_Vaisseau_son"`

Then run `make html` inside the `docs/` directory.<br/>
`cd docs`<br/>
`make html`

Open `docs/_build/html/index.html` in a web browser to read the documentation.

# Tips
### Tip for debugging
Set the `QT_DEBUG_PLUGINS` environement variable to `1` to enable more verbosity about plugins
`export QT_DEBUG_PLUGINS="1"`.

