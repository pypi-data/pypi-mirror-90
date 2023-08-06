#!/usr/bin/env python3

"""
|============================|
| Desinstalle l'application. |
|============================|

Ce fichier est a la fois un module est un script.

1) Retire raisin des applications au demarrage.
2) Supprime les raccourcis qui pointent vers raisin.
3) Supprime les repertoires crees par raisin
"""

import os
import shutil

import raisin.tools as tools # on ne fait pas d'import relatif
import raisin.application.settings as settings # de facon a ce qu'on puisse l'excecuter dirrectement


def uninstall_startup(home):
    """
    Supprime dans les fichiers de configuration,
    toutes les commandes qui excecutent une
    instance de raisin au demarrage.
    """
    assert isinstance(home, str), \
        "'home' have to be 'str', not %s." % type(home).__name__
    assert os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)

    with tools.Printer(
            "Removing raisin to apps at startup for {}...".format(
            repr(os.path.basename(home)))
            ) as p:
        path_ubuntu = os.path.join(home, ".config/autostart/raisin.desktop")
        path_raspberry = os.path.join(home, ".config/lxsession/LXDE-pi/autostart")
        path_windows = os.path.join(home,
            "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\raisin.pyw")
        
        if os.path.exists(path_ubuntu):
            os.remove(path_ubuntu)
            p.show("File removed (%s)." % repr(path_ubuntu))
        elif os.path.exists(path_raspberry):
            with open(path_raspberry, "r", encoding="utf-8") as f:
                content = [l for l in f if "raisin" not in l]
            with open(path_raspberry, "w", encoding="utf-8") as f:
                f.write("".join(content))
            p.show("File modified (%s)." % repr(path_raspberry))
        elif os.path.exists(path_windows):
            os.remove(path_windows)
            p.show("File removed (%s)." % repr(path_windows))
        else:
            p.show("File not found!")

def uninstall_shortcut(home):
    """
    Supprime les alias qui pointent vers une fonctionnalite de raisin
    """
    assert isinstance(home, str), \
        "'home' have to be 'str', not %s." % type(home).__name__
    assert os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)

    with tools.Printer(
            "Uninstall shortcut for {}...".format(
            repr(os.path.basename(home)))
            ) as p:
        # linux
        bashrc = os.path.join(home, ".bashrc")
        if os.path.exists(bashrc):
            p.show("Removing raisin from the '.bashrc' file")
            with open(bashrc, "r", encoding="utf-8") as f:
                lines = [l for l in f if "raisin" not in l]
                while lines and lines[-1] == "\n":
                    del lines[-1]
            with open(bashrc, "w", encoding="utf-8") as f:
                f.write("".join(lines))

        # windaube
        profile = os.path.join(home, "Documents", "profile.ps1")
        if os.path.exists(profile):
            p.show("Removing raisin from the 'profile.ps1' file")
            with open(profile, "r", encoding="utf-8") as f:
                lines = [l for l in f in "raisin" not in l]
                while lines and lines[-1] == "\n":
                    del lines[-1]
            if lines:
                with open(profile, "w", encoding="utf-8") as f:
                    f.write("".join(lines))
            else:
                os.remove(profile)

def uninstall_settings(home):
    """
    Supprime le repertoire '.raisin'.
    Supprime aussi le repertoire d'enregistrement des resultats
    si il existe.
    """
    assert isinstance(home, str), \
        "'home' have to be 'str', not %s." % type(home).__name__
    assert os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)

    with tools.Printer(
            "Uninstall settings for {}...".format(
            repr(os.path.basename(home)))
            ) as p:
        recording_directory = settings.Settings(home=home)["cluster_work"]["recording_directory"]
        if os.path.exists(recording_directory):
            p.show("Deletion of %s." % repr(recording_directory))
            shutil.rmtree(recording_directory)
        raisin_path = os.path.join(home, ".raisin")
        if os.path.exists(raisin_path):
            p.show("Deletion of %s." % repr(raisin_path))
            shutil.rmtree(raisin_path)

def _list_home():
    """
    Cede les repertoires personel de
    tous les utilisateurs qui doivent
    beneficier de la desinstallation de raisin.
    """
    if tools.id_().has_admin:
        if dialog.question_binaire(
                "Voulez vous desinstaller 'raisin' "
                "pour tous les utilisateurs?",
                default=False):
            racine = "C:\\Users" if os.name == "nt" else "/home"
            for user in os.listdir(racine):
                yield os.path.join(racine, user)
            raise StopIteration
    yield os.path.expanduser("~")

def main():
    """
    Desinstalle entierement l'application raisin.
    """
    with tools.Printer("Uninstall raisin..."):
        for home in _list_home():
            uninstall_shortcut(home)
            uninstall_startup(home)
            uninstall_settings(home)
        return 0

if __name__ == "__main__":
    main()
