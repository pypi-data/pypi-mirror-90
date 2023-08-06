OMEGAlpes Lib for linear energy systems modelling
==================================================

**OMEGAlpes** stands for Generation of Optimization Models As Linear Programming for Energy Systems.

**OMEGAlpes** aims to be an energy systems modelling tool for linear optimisation (LP, MILP).

A **web interface** is available at https://mhi-srv.g2elab.grenoble-inp.fr/OMEGAlpes-web-front-end/ to generate scripts


We are happy that you will use or develop the OMEGAlpes library. 

It is an **Open Source** project located on GitLab at https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes


Project Presentation
====================
**OMEGAlpes library :**
Please have a look to OMEGAlpes presentation : https://omegalpes.readthedocs.io/en/latest/  
The library is available at:
    https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes.git


**Examples and article case studies :**
Please have a look to examples : https://omegalpes-examples.readthedocs.io/en/latest/  
The OMEGAlpes Examples folder is available at:
    https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes-examples.git
Some examples and article case studies are avalaible as Notebooks at:
    https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes_notebooks.git

A scientific article presenting OMEGAlpes with a detailed example is available here:
https://hal.archives-ouvertes.fr/hal-02285954v1

**Notebooks :**
Mostly all examples and article case studies are associated to a Notebook.
They can be found in the folder notebooks at : 
    https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes_examples

**OMEGAlpes-web interface :**
An web interface is available at https://mhi-srv.g2elab.grenoble-inp.fr/OMEGAlpes-web-front-end/ 
This interface enable you to generate scripts more easily using the graphical representation detailed 
in https://omegalpes.readthedocs.io/en/latest/OMEGAlpes_grah_representation.html


OMEGAlpes' Community
====================
Please subscribe to our mailing lists :
- for our newsletters: https://groupes.renater.fr/sympa/subscribe/omegalpes-news
- as an OMEGAlpes' developer: https://groupes.renater.fr/sympa/subscribe/omegalpes-users

Please use the git issues system to report an error: https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes.git  
Otherwise you can also contact de developer team using the following email adress: omegalpes-users@groupes.renater.fr 


Installation Help
=================
You can install the library as a user or as a developer. Please follow the corresponding installation steps below.

You can use any development environment
If you use Pycharm, some indications below will help you for the installation
https://www.jetbrains.com/pycharm/

Prerequisite
------------
Please install Python 3.6
https://www.python.org/downloads/

Installation as a user
----------------------
Please install OMEGAlpes Lib with pip using the command prompt.   

If you are admin on Windows or working on a virtual environment
    
    pip install omegalpes

If you want a local installation or you are not admin
    
    pip install --user omegalpes

If you are admin on Linux:
    
    sudo pip install omegalpes

Then, you can download (or clone) the OMEGAlpes Examples folder (repository) at :
https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes-examples

Launch the examples (with Pycharm for instance) to understand how the OMEGAlpes Lib works.
Remember that the examples are detailed at : https://omegalpes-examples.readthedocs.io/en/latest/

Enjoy your time using OMEGAlpes !

Installation as a developer and local branch creation
-----------------------------------------------------
1. Create a new folder in the suitable path, name it as you wish for example : OMEGAlpes

2. Clone the OMEGAlpes library repository
    
    ---
    Command lover:
    
           git clone https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes.git
    
    ---
    Pycharm lover:
    
    Open Pycharm       
    On the Pycharm window, click on "Check out from version control" then choose "Git".   
    A "clone repository" window open.      
    Copy the following link into the URL corresponding area: 
    
        https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes.git
    Copy the path of the new folder created just before.   
    Test if the connection to the git works and if it works click on "Clone".       
    Once OMEGAlpes is cloned, you must be able to see the full OMEGAlpes library on Pycharm 
    or on another development environment.
    
    -----
    If the connection does not work and if you are working with local protected network,
    please try again with the wifi.

3. First, choose or change your project interpreter
    
    ---
    Pycharm lover:
    
    Click on the yellow warning link or go to "File", "settings...", "Project Interpreter"
    
    You can:
    - either select the "Python 3.6" project interpreter but you may change the version 
    of some library that you could use for another application
    - either create a virtual environment in order to avoid this problem (recommended).  
    Click on the star wheel near the project interpreter box.  Click on "add...".   
    Select "New environment" if it not selected.    
    The location is pre-filled, if not fill it with the path of the folder as folder_path/venv   
    Select "Python 3.6" as your base interpreter   
    Then click on "Ok"
            
    ---

4. You can install the library on developing mode using the following command in command prompt
once your are located it on the former folder.
If you are calling OMEGAlpes library in another project, the following command enables you to 
refer to the OMEGAlpes library you are developing 

        python setup.py develop

5. If it is not already done, install the library requirements.
    
    ---
    Command lover:
               
            pip install <library_name>
            
    If required, the command to upgrade the library is : 
    
            pip install --upgrade <library_name>
            
    ---
    Pycharm lover:
    
    You should still have a yellow warning.   
    You can:
    - install automatically the libraries clicking on the yellow bar
    - install automatically the library using pip with Pycharm on "File", "settings...", "Project Interpreter", "+",
    and choosing the required library as indicated in the Library Installation Requirements 
    part

6. Finally, you can create your own local development branch.
    
    ---
    Command lover:
        
        git branch <branch_name>
            
    ---
    Pycharm lover:
    
    By default you are on a local branch named master.   
    Click on "Git: master" located on the bottom write of Pycharm    
    Select "+ New Branch"   
    Name the branch as you convenience for instance "dev_your_name"

7. Do not forget to "rebase" regularly to update your version of the library.
    
    ---
    Command lover:
    
        git rebase origin
            
    ---
    Pycharm lover:
    
    To do so, click on "VCS", "Git", "Fetch"
    Then, click on your branch name on the bottom write of the Pycharm window
    select "Origin/master" and click on "Rebase current onto selected"
    
8. For contribution, have a look to CONTRIBUTING.md
Once your code is ready for contribution, do a last rebase (see 7.) and then, 
request for a merge with the master branch in OMEGAlpes gitlab
https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes.git


If you want to have access to other examples and study cases, 
please have a look to the user's installation.
    
Enjoy your time developing OMEGAlpes!

Library Installation Requirements
---------------------------------
PuLP > 1.6.10

Matplotlib > 2.2.2

Numpy > 1.14.2

Pandas > 0.22.0


Main Authors: 
=============
B. DELINCHANT, S. HODENCQ, Y. MARECHAL, L. MORRIET, C. PAJOT, V. REINBOLD,
F. WURTZ


Partners:
=========
Univ. Grenoble Alpes, CNRS, Grenoble INP, G2Elab, CEA, Université Paris-Sud


Acknowledgments:
================
This work has been partially supported by the CDP Eco-SESA receiving fund from the French National Research 
Agency in the framework of the "Investissements d’avenir" program (ANR-15-IDEX-02)


Licence
=======
This code is under the Apache License, Version 2.0


Notes
=====
This library has been tested using
- PyCharm 2018.2.4
- Python 3.6.0
- pip 18.1
- setuptools 39.1.0