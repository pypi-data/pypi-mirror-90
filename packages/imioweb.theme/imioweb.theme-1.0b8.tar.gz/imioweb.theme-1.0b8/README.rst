.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=============
imioweb.theme
=============
Actuel theme for the new IMIO website.

Preview
-------

.. image:: ./src/imioweb/theme/theme/images/thumb.png
   :alt: Classic Theme
   :target: http://www.affinitic.be


Installation du package
-----------------------

Développer le buildout et ses dépendances::
    $ make build-dev

ou::
    $ virtualenv-2.7 .
    $ bin/pip install -I -r requirements.txt
    $ ln -s dev.cfg buildout.cfg
    $ bin/buildout

Lancer l'instance::
    $ bin/instance fg


Installer le package
--------------------

  - Aller sur http://localhost:8080/
  - Créer un nouveau site plone
  - [Aller dans le control panel section "Modules"](http://localhost:8080/Plone/prefs_install_products_form)
  - Installer "imioweb.theme"

Ajouter le contenu d'exemple
----------------------------

  - [Aller dans le control panel section "Modules"](http://localhost:8080/Plone/prefs_install_products_form)
  - Ajouter "affinitic.demo.content" dans les dépendances et l'installer


Le theme Classic est installé!
==============================
