#!/usr/bin/env python3

"""
|=========================|
| Installe l'application. |
|=========================|

Ce fichier est a la fois un module est un script.

1) Installation des modules qui dependent de raisin.
2) Installation de raisin comme une application au demarrage.
3) Creation des parametres du dossier '.raisin'.
"""

import os
import sys

import raisin.tools as tools # on ne fait pas d'import relatif
import raisin.application.hmi.dialog as dialog # afin de pouvoir le faire
import raisin.application.module as module # fonctionner comme un script
import raisin.application.uninstall as uninstall
import raisin.application.settings as settings


def install_dependencies():
    """
    Recherche les dependances non satisfaites de raisin
    et tente de les installer si l'utilisateur est d'accord.
    """
    # global tkinter, ttk # evite l'erreur: UnboundLocalError: local variable 'tkinter' referenced before assignment

    dependencies = module.get_unmet_dependencies("raisin") # recherches des dependances non satisfaites de raisin
    if dependencies:
        if dialog.question_binaire(
                "'raisin' depend des modules suivants:\n" \
                + " %s\n" % ", ".join(dependencies) \
                + "Voulez-vous les installer?", default=True):
            if not tools.id_().has_admin:
                if dialog.question_binaire(
                        "Vous n'avez pas les droits administrateur.\n"
                        "Preferez-vous installer les modules en tant "
                        "qu'administrateur?", default=True):
                    command = '%s -c "\n' % sys.executable
                    command += 'from raisin.application import module\n' \
                            + 'for dep in %s:\n' % repr(dependencies) \
                            + '\tmodule.install(dep)\n' \
                            + '"'
                    if os.name == "nt":
                        sudo = "runas /user:%s\\administrator" \
                                % tools.id_().hostname
                    else:
                        sudo = "sudo"
                    sudo_command = sudo + " " + command
                    with tools.Printer(
                        "Install dependencies as administrator...") as p:
                        p.show("$ %s" % repr(sudo_command))
                        os.system(sudo_command)
                    return
                else:
                    message = "Install dependencies without administrator rights..."
            else:
                message = "Install dependencies with administrator rights..."
            with tools.Printer(message):
                for dep in dependencies:
                    module.install(dep)

def install_startup(home):
    """
    Met raisin dans les applications au demarrage.
    'home' est le repertoire courant de l'utilisateur.
    """
    assert isinstance(home, str), \
        "'home' have to be 'str', not %s." % type(home).__name__
    assert os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)


    with tools.Printer(
            "Adding raisin to apps at startup for {}...".format(
            repr(os.path.basename(home)))
            ) as p:
        path_ubuntu = os.path.join(home, ".config/autostart")
        path_raspberry = os.path.join(home, ".config/lxsession/LXDE-pi")
        path_windows = os.path.join(home,
            "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        command = "%s -m raisin start" % sys.executable
        
        # Linux qui suit la norme d'ubuntu.
        if os.path.exists(path_ubuntu):
            filename = os.path.join(path_ubuntu, "raisin.desktop")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("[Desktop Entry]\n"
                        "Name=raisin\n"
                        "Type=Application\n"
                        "Exec=%s\n" % command \
                      + "Terminal=false")
            p.show("File append (%s)." % repr(filename))
        
        # Raspberry Pi
        elif os.path.exists(path_raspberry):
            filename = os.path.join(path_raspberry, "autostart")
            if not os.path.isfile(filename):
                open(filename, "w").close()
                p.show("File created (%s)." % repr(filename))
            with open(filename, "r", encoding="utf-8") as f: # il faut que l'on s'assure que raisin n'y est pas deja
                content = [l for l in f if "raisin" not in l]
            with open(filename, "w", encoding="utf-8") as f:
                f.write("".join(content).lstrip())
                f.write("\n{}\n".format(command))
            p.show("File modified (%s)." % repr(filename))
        
        # Microchiotte Windaube
        elif os.path.exists(path_windows):
            filename = os.path.join(path_windows, "raisin.pyw")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("import raisin.__main__\n"
                        "\n"
                        "raisin.__main__.main(['start'])\n")
            p.show("File append (%s)." % repr(filename))
        
        # Os inconu
        else:
            raise TypeError("Cannot put raisin as an application at startup.")

def install_shortcut(home):
    """
    Ajoute des alias qui pointent vers raisin.
    """
    assert isinstance(home, str), \
        "'home' have to be 'str', not %s." % type(home).__name__
    assert os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)

    with tools.Printer(
            "Install shortcut for {}...".format(
            repr(os.path.basename(home)))
            ):
        uninstall.uninstall_shortcut(home)
        if os.name == "nt":
            config_file = os.path.join(home, "Documents", "profile.ps1")
            command = "Set-Alias raisin '%s -m raisin'" % sys.executable
        else:
            config_file = os.path.join(home, ".bashrc")
            command = "alias raisin='%s -m raisin'" % sys.executable

        os.system(command) # pour rendre la commande effective de suite
        with open(config_file, "a", encoding="utf-8") as f:
            f.write("\n")
            f.write(command)
            f.write("\n")

def install_settings(home, action):
    """
    Initialise et enregistre les paremetre de l'utilisateur.
    """
    assert isinstance(home, str), \
        "'home' have to be 'str', not %s." % type(home).__name__
    assert os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)
    assert action in ("paranoiac", "normal", "altruistic", "custom"), \
            "Les actions ne peuvent que etre 'paranoiac', " \
            + "'normal', 'altruistic' ou 'custom'. Pas '%s'." % action

    with tools.Printer(
            "Install settings for {}...".format(
            repr(os.path.basename(home)))
            ):
        s = settings.Settings(home=home, action=action)
        s.flush()

def _list_home():
    """
    Cede les repertoires personel de
    tous les utilisateurs qui doivent
    beneficier de l'installation de raisin.
    """
    if tools.id_().has_admin:
        if dialog.question_binaire(
                "Voulez vous installer 'raisin' "
                "pour tous les utilisateurs?",
                default=False):
            racine = "C:\\Users" if os.name == "nt" else "/home"
            for user in os.listdir(racine):
                yield os.path.join(racine, user)
            raise StopIteration
    yield os.path.expanduser("~")

def main():
    """
    Installe les elements fondamentaux
    pour le bon fonctionnement de l'application.
    """
    with tools.Printer("Install raisin..."):
        actions = ["paranoiac", "normal", "altruistic", "custom"] # ce sont les 4 types d'installations possibles
        install_dependencies()
        action = actions[
            dialog.question_choix_exclusif(
                "Quel mode d'installation ?",
                ["paranoiac (maximum security)",
                 "normal (compromise between safety and efficiency)",
                 "altruistic (maximum performance)",
                 "custom (request your detailed opinion)"])]  # on selectionne le bon type d'installation
        for home in _list_home():
            install_startup(home)
            install_shortcut(home)
            install_settings(home, action)
        return 0

if __name__ == "__main__":
    main()
