OMEGAlpes Installation
======================

.. contents::
    :depth: 1
    :local:
    :backlinks: top

Install OMEGAlpes
-----------------
Do not hesitate to listen to a really nice music to be sure...
... it's going to work!

Python 3.6.0
************
Please use Python 3.6.0 for the project interpreter:
`Python 3.6 <https://www.python.org/downloads/release/python-360/>`_


pip install omegalpes
*********************
Please install OMEGAlpes Lib with pip using on of the following the command prompt:


    - **If you are admin on Windows or working on a virtual environment**::

        pip install omegalpes

    - **If you want a local installation or you are not admin**::

        pip install --user omegalpes

    - **If you are admin on Linux**::

        sudo pip install omegalpes

Then, you can download (or clone) the OMEGAlpes Examples folder (repository) at :
`OMEGAlpes Examples`_
Make shure that the name of the examples folder is: "omegalpes_examples".

Launch the examples (with Pycharm for instance) to understand how the OMEGAlpes Lib works.
Remember that the examples are presented at : `OMEGAlpes Examples Documentation`_

**Enjoy your time using OMEGAlpes !**



Other installation requirements
-------------------------------
If the music was enough catchy, the following libraries should be
already installed.
If not, increase the volume and install the following libraries
with the help below.

    - **PuLP >= 2.1**

    PuLP is an LP modeler written in python.
    PuLP can generate MPS or LP files and call GLPK, COIN CLP/CBC,
    CPLEX, and GUROBI to solve linear problems :
    `PuLP <https://github.com/coin-or/pulp>`_


    - **Matplotlib >= 2.2.2**

    Matplotlib is a Python 2D plotting library :
    `Matplotlib <https://matplotlib.org/>`_


    - **Numpy >= 1.14.2**

    NumPy is the fundamental package needed for scientific computing with Python.
    `Numpy <https://github.com/numpy/numpy>`_


    - **Pandas >= 0.22.0**

    Pandas is a Python package providing fast, flexible, and expressive data
    structures designed to make working with "relational" or "labeled" data
    both easy and intuitive.
    `Pandas <https://pandas.pydata.org/pandas-docs/version/0.23.1/index.html>`_


    ---
    **Command lover**
    --- ::

        pip install <library_name>==version

    If required, the command to upgrade the library is ::

        pip install --upgrade <library_name>

    ---
    **Pycharm lover**
    ---

    Install automatically the library using pip with Pycharm on "File", "settings...", "Project Interpreter", "+",
    and choosing the required library



Install OMEGAlpes as a developer
--------------------------------
Installation as a developer and local branch creation
******************************************************
Absolute silence, keep calm and stay focus... you can do it! :`<https://www.youtube.com/watch?v=g4mHPeMGTJM>`_

1. Create a new folder in the suitable path, name it as you wish for instance : OMEGAlpes

2. Clone the OMEGAlpes library repository

    ---
    **Command lover**
    --- ::

           git clone https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes.git

    ---
    **Pycharm lover**
    ---

    | Open Pycharm
    | On the Pycharm window, click on "Check out from version control" then choose "Git".
    | A "clone repository" window open.
    | Copy the following link into the URL corresponding area:

        https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes.git

    | Copy the path of the new folder created just before.
    | Test if the connection to the git works and if it works click on "Clone".
    | Once OMEGAlpes is cloned, you must be able to see the full OMEGAlpes library on Pycharm
      or on another development environment.

    If the connection does not work and if you are working with local protected network,
    please try again with the wifi.

3. First, choose or change your project interpreter

    ---
    **Pycharm lover**
    ---

    Click on the yellow warning link or go to "File", "settings...", "Project Interpreter"

    You can:

    - either select the "Python 3.6" project interpreter but you may change the version
      of some library that you could use for another application.

    - either create a virtual environment in order to avoid this problem (recommended).
     | Click on the star wheel near the project interpreter box.
     | Click on "add...".
     | Select "New environment" if it not selected.
     | The location is pre-filled, if not fill it with the path of the folder as folder_path/venv
     | Select "Python 3.6" as your base interpreter
     | Then click on "Ok"

4. You can install the library on developing mode using the following command in command prompt
once your are located it on the former folder.
If you are calling OMEGAlpes library in another project, the following command enables you to
refer to the OMEGAlpes library you are developing::

        python setup.py develop

5. If it is not already done, install the library requirements.

    ---
    **Command lover**
    --- ::

            pip install <library_name>

    If required, the command to upgrade the library is ::

            pip install --upgrade <library_name>

    ---
    **Pycharm lover**
    ---

    You should still have a yellow warning.
    You can:

    - install automatically the libraries clicking on the yellow bar.

    - install automatically the library using pip with Pycharm on "File", "settings...", "Project Interpreter", "+",
      and choose the required library as indicated in the Library Installation Requirements
      part.

6. Finally, you can create your own local development branch.

    ---
    **Command lover**
    --- ::

        git branch <branch_name>

    ---
    **Pycharm lover**
    ---

    | By default you are on a local branch named master.
    | Click on "Git: master" located on the bottom write of Pycharm
    | Select "+ New Branch"
    | Name the branch as you convenience for instance "dev_your_name"

7. Do not forget to "rebase" regularly to update your version of the library.

    ---
    **Command lover**
    --- ::

        git rebase origin

    ---
    **Pycharm lover**
    ---

    To do so, click on your branch name on the bottom write of the Pycharm window
    select "Origin/master" and click on "Rebase current onto selected"

If you want to have access to examples and study cases,
download (or clone) the OMEGAlpes Examples folder (repository) from :
`OMEGAlpes Examples`_ .    \
Make shure that the name of the examples folder is: "omegalpes_examples".
Remember that the examples are presented at : `OMEGAlpes Examples Documentation`_


**Enjoy your time developing OMEGAlpes!**


.. _OMEGAlpes Gitlab: https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes
.. _OMEGAlpes Examples Documentation: https://omegalpes_examples.readthedocs.io/
.. _OMEGAlpes Examples: https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes_examples