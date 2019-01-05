# Prérequis
- `$ git config --global credential.helper store`
- `$ git config --global user.name "Votre Nom"`
- `$ pip install --user -r requirements.txt`
- [Outils AVR](http://www.groupes.polymtl.ca/inf1900/fichiers/)

# Comment ça marche
- Lancez le script `./start.py`.
- Suivez les étapes linéairement (`clone`, puis `grade`, puis `assemble`).

# Résumé des différentes étapes
- `clone` récupérera les informations des élèves (nom, prénom, équipe,
  groupe) depuis le site du cours et clonera le repo de chaque équipe.
  
- `grade` vérifiera les fichiers inutiles, compilera le code des
  élèves et écrira un fichier de notes dans chaque repo.  Il faut
  attribuer les notes manuellement, mais la majorité du travail
  répétitif est déjà automatisée.

- `assemble` fera un commit et merge sur chaque repo, puis générera un
  fichier de notes `grades.csv`.

# Notes
- Certaines informations sont redemandées entre plusieurs étapes afin
  de pouvoir corriger plusieurs travaux simultanément.

# Ce qui manque
- Utiliser clang-format et clang-tidy pour plus d'automatisations.
- Envoi du fichier de notes par email à Jérôme.

# Contributeurs
- Anes Belfodil
- Philippe Carphin
- Olivier Dion
