[![Build Status](https://travis-ci.org/flyingeek/editolido.svg?branch=master)](https://travis-ci.org/flyingeek/editolido)

Je sais je dois faire la doc... :-)

Pour la première utilisation il faut être connecté à Internet.

Usage:
-----
 - Installez le worklow [Lido2Mapsme+](https://workflow.is/workflows/ea27b4ab34dc4275b954723748ce754e)
 - Installez le workflow Editorial [Lido2Mapsme+](http://www.editorial-workflows.com/workflow/5800601703153664/o7BioyJJW8o#)

Mise à jour:
-----------
 - réinstallez le workflow Editorial (les personnalisations sont perdues)
 - Ou (sauf contre indication), mettez juste à jour la version dans l'URL de l'action Installation (dans Editorial, Editez le workflow puis dépliez l'action "Installation/Mise à jour" et modifiez l'URL).
 
Après une mise à jour, il faut lancer le worflow au moins une fois en étant connecté.
 
Changements:
------------
##v1.0.0.b4: (début de publication des workflows)
 - Configurable (dans Editorial, éditez le workflow)
 - Possibilité de tracer la route Ogimet (OFF par défaut, mais configurable) pour le futur workflow GRAMET.
 - Archivage des données en entrée et du KML en sortie (ON par défaut)
 - Le lancement de Mapsme intervient dans l'app Worflow iso Editorial

##v1.0.0b5: rlatsm fix
 - voir (https://github.com/flyingeek/editolido/issues/2)

##v1.0.0b7: rlatsm message format fix
 - voir (https://github.com/flyingeek/editolido/issues/5)

Coding
------
- apply PEP8
- Use spaces for identation

Run unittests
-------------
To run the unittests:

    python -m unittest discover -s test

or with coverage:

    coverage run -m unittest discover -s test && coverage report
