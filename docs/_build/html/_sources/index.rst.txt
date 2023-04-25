.. Reminder about commiting the changes and all that
   1. make changes on the file itself (node_a and so on) inside main branch and do:
      on vscode (inside src/docs/):
         doxygen Doxyfile && make html

      on terminal running on src/ (or just use github desktop):
         git init
         git branch
         git add .
         git commit -m "message"
         git push -u origin main
   
   2. send the differences to the gh-pages branch:
      on terminal running on src/:
         git init (if not itialized before, as well as all the add . and commit -m "whatever")
         git subtree push --prefix docs/_build/html/ origin gh-pages


Welcome to S5646764_rt2_a1's documentation!
###########################################

Indices and tables
******************

* :ref:`genindex`
* :ref:`search`

Introduction
************

This documentation is part of the continuous assessment for the **Research Track 2** course,
done by **Vinícius Ferreira (S5646764)**.

The documentation itself is about the codes designed for the final assignment on Research
Track 1, adding comments and explanation about the nodes on the custom package :mod:`vinicius_assignment_2_rt1`.
The codes are separated in further sections, which can be explored when clicking on the desired module.

Modules
=======

Presentation of the modules used for the code are shown on the links below.

.. toctree::
   :maxdepth: 1
   :caption: Modules list:

   node_a.rst
   node_b.rst
   node_c.rst

