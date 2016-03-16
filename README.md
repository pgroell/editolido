[![Build Status](https://travis-ci.org/flyingeek/editolido.svg?branch=master)](https://travis-ci.org/flyingeek/editolido)

Je sais je dois faire la doc... :-)

Pour la première utilisation il faut être connecté à Internet.

Usage:
-----
 - Installez le worklow [Lido2Mapsme+](https://workflow.is/workflows/ea27b4ab34dc4275b954723748ce754e)
 - Installez le workflow Editorial [Lido2Mapsme+](http://www.editorial-workflows.com/workflow/5800601703153664/o7BioyJJW8o#)

Changements:
------------
 - Configurable (dans Editorial, éditez le workflow)
 - Possibilité de tracer la route Ogimet (OFF par défaut, mais configurable) pour le futur workflow GRAMET.
 - Archivage des données en entrée et du KML en sortie (ON par défaut)
 - Le lancement de Mapsme intervient dans l'app Worflow iso Editorial

Coding
------
- apply PEP8
- Use smart tabs for easyer editing on IOS
  (indent with tabs, align with spaces)

Run unittests
-------------
To run the unittests:

    python -m unittest discover -s test

or with coverage:

    coverage run -m unittest discover -s test && coverage report
