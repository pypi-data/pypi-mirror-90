#!/usr/bin/env python3

"""
|==================================|
| Met a jour raisin depuis le git. |
|==================================|

Telecharge l'archive depuis le depos.
Ce qui implique que c'est avec la version
en cours de devloppement, c'est a dire la
version instable que la mise a niveau
est effectuee. Les nouveaux fichiers
ecrasents la version locale exisyante de raisin.
"""


import os
import requests
import shutil
import sys
import tarfile

import raisin.tools as tools


URL = "https://framagit.org/robinechuca/raisin/"
    "-/archive/master/raisin-master.tar.gz?path=raisin"


def automatic_update():
    """
    Fait la mise a jour seulement si l'option est cochee.
    La version mise a jour est une version stable.

    :return: 0 si La mise a jour c'est bien passe ou qu'il n'y en a pas eu.
    :rtype: int
    """
    import raisin.application.settings as settings
    if not settings.settings["account"]["automatic_update"]:
        return 0
    return os.system("%s -m pip install --upgrade raisin" % sys.executable)

def find_folder():
    """
    Recherche le repertoir dans lequel se trouve raisin.

    :return: Le chemin du dossier 'raisin'.
    :rtype: str
    """
    with tools.Printer("Searching for the destination folder...") as p:
        candidats = set()
        for path in sys.path:
            if os.path.isdir(path):
                if "raisin" in os.listdir(path):
                    candidats.add(path)
        if len(candidats) >= 2:
            candidats = {c for c in candidats if c != os.getcwd()}
        if not candidats:
            p.show("Folder not found!")
            raise FileNotFoundError("'raisin' ne semble pas etre bien installe dans l'ordinateur.\n"
                "Si il est installe a un endroit bizzard, ajoutez le repertoire au PYTHONPATH.\n"
                "Si il n'est pas installe, tapez '%s -m raisin install'" % sys.executable)
        if len(candidats) >= 2:
            p.show("'raisin' is installed in too many places!")
            raise FileNotFoundError(
                "'raisin' est installe a differents endroits.\n" \
                + "les voici: {}\n".format(", ".join(candidats)) \
                + "Supprimez les doublons de raisin.")
        dest = os.path.join(list(candidats)[0], "raisin")
        p.show("Folder: %s" % repr(dest))
        return dest

def main():
    """
    Met a jour raisin avec la version en cours de developpement.
    """
    with tools.Printer("Upgrade raisin...") as p:
        # Recherche du dossier de destination
        dest = find_folder()

        # Telechargement.
        with tools.Printer("Download files..."):
            r = requests.get(URL)
            archive = os.path.join(str(tools.temprep), "raisin.tar.gz")
            data = r.content
            p.show("Datasize: %.2f Mio" % (len(data)/2**20))
            with open(archive, "wb") as f:
                f.write(data)
        
        # Extraction dans le bon dossier
        with tools.Printer("Archive extraction..."):
            archive_ex = os.path.join(str(tools.temprep), "raisin")
            with tarfile.open(archive) as fs:
                fs.extractall(path=archive_ex)
            if not os.path.exists(archive_ex):
                raise PermissionError("Impossible d'extraire l'archice la: %s" % repr(archive_ex))
            os.remove(archive)
            p.show("Datasize: %.2f Mio" % (sum(os.path.getsize(os.path.join(pa, f))
                    for pa, _, fs in os.walk(archive_ex) for f in fs)/2**20))

        # Remplacement
        with tools.Printer("Substitution of the old 'raisin' by the new one"):
            src = os.path.join(archive_ex, os.listdir(archive_ex)[0], "raisin")
            # Supression ancien.
            for old_mod in os.listdir(dest): # On ne fait pas juste shutil.copytree(src, dest)
                if os.path.isfile(os.path.join(dest, old_mod)):  # car les droits du dossier raisin sraient perdus.
                    os.remove(os.path.join(dest, old_mod))
                else:
                 shutil.rmtree(os.path.join(dest, old_mod))
            
            for new_mod in os.listdir(src):
                shutil.move(os.path.join(src, new_mod), os.path.join(dest, new_mod))
            shutil.rmtree(archive_ex)

        if tools.id_["has_admin"]:
            os.chmod(dest, 0o777)

if __name__ == "__main__":
    main()