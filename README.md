# Literate Python Container
A minimal environment to develop python projects in a literal way.

Basically a wrapper around 
[pylit](https://slott56.github.io/PyLit-3/)
[docutils](https://docutils.sourceforge.io/)

A `docker-compose up` command will spin up the container, which will expose a simple 
http server on `localhost:8080`. 

There are three main folders in our project:

- pylit
- src
- docs

#### Workflow
The _pylit_ folder contains a _watcher.py_ file and a _style.css_ file 
which are necessary to auto parse our python files in Restructured Text 
format first and into HTML next. 

Once the container is up, one should _bash_ inside the container in order to 
execute the _watcher.py_ script, which will start the auto-update feature, and
will keep updating files as long as the process is up. 

The conversion is made automatically whenever a `*.py` file changes inside _src_
folder. For any file in the _src_ folder there will be two files
generated:

- one inside _docs/rst/_ folder
- one inside _docs/html/_ folder

The generated HTML files are visible from `localhost:8088` url and the 
Restructured Text files inside _docs/rst_ folder could be edited as well,
action which will trigger an auto-update on both `.py` file and `.html` files.