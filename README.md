[![Build Status](https://travis-ci.org/flyingeek/editolido.svg?branch=master)](https://travis-ci.org/flyingeek/editolido)

Je sais je dois faire la doc... :-)

Pour la première utilisation il faut être connecté à Internet.
De plus à la première installation un message "module editolido manquant" apparait, il faut redémarrer Editorial en attendant une correction de ce pb.

Usage:
-----
 - Installez le worklow [Lido2Mapsme+](https://workflow.is/workflows/ea27b4ab34dc4275b954723748ce754e)
 - Installez le workflow Editorial [Lido2Mapsme+](http://www.editorial-workflows.com/workflow/5800601703153664/o7BioyJJW8o#)
 - Lancez au moins une fois l'un des deux workflow pour télécharger le module editolido
 
Réglages:
--------
 - depuis le Editorial, choisissez "Edit Worflow". (icone en forme de clé en haut à droite d'Editorial, puis toucher le i sur la ligne correspondant au workflow Lido2Mapsme+)
 - Les différentes actions du workflow peuvent de déplier et permettent les réglages

Mise à jour:
-----------
 - réinstallez le workflow Editorial (les personnalisations sont perdues)
 - Ou laisser le mode automatique activé (réglages dans la première action du workflow).
 
Changements:
------------
IMPORTANT pour la 1.0.1, Les utilisateurs des versions beta doivent:
- Noter dans un coin leurs customisations de l'ancien workflow Editorial
- Effacer l'ancien dossier site-package (ou au minimum le dossier editolido qui s'y trouve)
- Relancer Editorial (Tuer l'application via double click sur le bouton de l'iPad, puis balayer vers le haut l'application Editorial)
- Mettre à jour le workflow Editorial (effacer et reinstaller, lien au dessus)

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
