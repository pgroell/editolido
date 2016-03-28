[![Build Status](https://travis-ci.org/flyingeek/editolido.svg?branch=master)](https://travis-ci.org/flyingeek/editolido)

Je sais je dois faire la doc... :-)

Installation:
-------------
 - Installez le worklow [Lido2Mapsme+](https://workflow.is/workflows/ea27b4ab34dc4275b954723748ce754e)
 - Installez le workflow Editorial [Lido2Mapsme+](http://www.editorial-workflows.com/workflow/5800601703153664/o7BioyJJW8o#)
 - Lancez au moins une fois l'un des deux workflow pour télécharger le module editolido
 - Pour la première utilisation il faut être connecté à Internet.
 - Les utilisateurs des Beta doivent effacer l'ancien dossier site-package, relancer (tué) Editorial, supprimer l'ancien workflow Lido2Mapsme+
 
Réglages:
--------
 - depuis Editorial, choisissez "Edit Worflow". (icône en forme de clé en haut à droite d'Editorial, puis toucher le i sur la ligne correspondant au workflow Lido2Mapsme+)
 - Les différentes actions du workflow peuvent se déplier et permettent les réglages

Mise à jour:
-----------
 - réinstallez le workflow Editorial (les personnalisations sont perdues)
 - Ou laisser le mode automatique activé (réglages dans la première action du workflow).
 
En cas de problèmes:
--------------------
 Vous vous êtes déjà servi des workflows => envoyez votre OFP (Ici en ouvrant un ticket dans Issues ou sur Yammer).
 
 Vous êtes utilisateur d'une ancienne version ou vous installez pour la première fois:
 
 - Il ne faut qu'un seul workflow Editorial Lido2Mapsme+ dans le doute, effacez l'ancien (ou les anciens) et réinstallez. Actuellement le workflow Editorial version 1.0.1 ou plus est à jour (lien au début de ce readme).
 - Assurez-vous d'utiliser la dernière version du module editolido (switch Mise à jour auto sur ON) et effacez le dossier editolido, il sera téléchargé à nouveau.
 - si ça ne fonctionne toujours pas, effacez encore une fois le dossier editolido relancez python en redémarrant Editorial après l'avoir "tué" (double click sur le bouton iPhone, balayer l'app Editorial vers le haut)
 - Envoyez aussi votre OFP

Changements:
------------
##v1.0.2
 - Le track du FPL est affiché en entier avec pin à chaque extrémité
 - correction d'un bug sur la couleur du dégagement

##v1.0.1
 - Configurable (dans Editorial, éditez le workflow)
 - Possibilité de tracer la route Ogimet (OFF par défaut, mais configurable) pour le futur workflow GRAMET.
 - Archivage des données en entrée et du KML en sortie (ON par défaut)
 - Le lancement de Mapsme intervient dans l'app Worflow iso Editorial
 - mise à jour automatique du module (ON par défaut)
 - affichage possible de la route du dégagement (off par défaut)
 - Les bugs connus sur les derniers OFP sont corrigés

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
