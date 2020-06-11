# sfr_ftth
sfr_ftth est une bibliotheque python permettant d'interroger son éligibilité FTTH via l'api rest SFR.

## Prérequis
python >= 3.8.x

## Installation

### Avec git

cloner le repository:
```
git clone https://github.com/mem0x959c/sfr_ftth
cd sfr_ftth
```

mise a jour (si le repository remote contient des modifications):
```
git pull 
```

### Ou utilisez le bouton "clone or download"

## Utilisations et exemples

### Eligibilite d'une addresse
voir test_sfr_ftth1.py qui permet d'interroger l'elibilité d'une adresse

```
import sfr_ftth
print(sfr_ftth.GetEligibilityByPostalAddress('401 route du saunier, 38090 Roche'))
```

### Comparer l'éligibilité SFR a celui déclaré dans le fichier open-data ARCEP

Télécharger [le fichier open-data ARCEP](https://www.data.gouv.fr/fr/datasets/le-marche-du-haut-et-tres-haut-debit-fixe-deploiements/#_)
Par exemple le fichier csv "202T1-Immeuble".
Son format est donné sur ce meme site:
```
x : longitude
y : latitude
imb_id : code de l’immeuble
num_voie : numéro de voie
cp_no_voie : complément
type_voie : type de voie
nom_voie : nom de la voie
batiment : nom du bâtiment
code_poste : code postal
nom_com : nom de la commune
imb_etat : état de déploiement de l’immeuble
pm_ref : code du PM
pm_etat : état de déploiement du PM
code_l331 : code de l’opérateur
geom_mod : indicateur de modification de la géométrie par l’Arcep
type_imb : type d’immeuble {pavillon/immeuble}
```

Comme ce fichier est très gros (2 GB), nous allons extraire les donnees pour une ville donnée.
Pour cela, sur LINUX utiliser les commandes suivantes; sur Windows, installer d'abord [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10) pour avoir un shell linux.
```
head -1 mv_immeubles_2020t1.csv > mv_immeubles_2020t1_bj.csv
grep "38300,Bourgoin-Jallieu" mv_immeubles_2020t1.csv >> mv_immeubles_2020t1_bj.csv
```

Le fichier test_sfr_ftth2.py permet alors d'interroger le site SFR et 
d'afficher les addresses qui sont déclarées éligibles sur le site SFR mais non éligibles dans le fichier ARCEP.
```
python test_sfr_ftth2.py mv_immeubles_2020t1_bj.csv
```