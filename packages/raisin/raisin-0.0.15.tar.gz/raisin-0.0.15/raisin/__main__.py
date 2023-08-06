#!/usr/bin/env python3

"""
|=================================|
| Permet d'executer des fonctions |
| en ligne de commandes.          |
|=================================|

Permet en particulier:
1) Installer/Desinstaller raisin ou un autre module.
    -Installer raisin:
        $ python3 -m raisin install
    -Desinstaller raisin:
        $ python3 -m raisin uninstall
    -Reinstaller raisin:
        $ python3 -m raisin reinstall
    -Metre a jour raisin:
        $ python3 -m raisin install --upgrade
        $ python3 -m raisin
2) Configurer raisin.
    -Configuration generale:
        $ python3 -m raisin configure
    -Changer le mot de passe:
        $ python3 -m raisin psw
        $ python3 -m raisin configure psw
    -Configurer l'antivol:
        $ python3 -m raisin padlock
        $ python3 -m raisin configure padlock
3) Lancer l'application:
    -Demarrer le serveur:
        $ python3 -m raisin start --server
    -Lancer les mises a jours automatiques:
        $ python3 -m raisin start --upgrade
"""

import argparse
import getpass
import os
import sys


def parse_arguments():
    """
    Fait le parsing des arguments.
    """
    parser = argparse.ArgumentParser(description="Simple API pour raisin.")
    subparsers = parser.add_subparsers(dest="parser_name")

    # install
    parser_install = subparsers.add_parser("install", help="Installer un module python, possiblement raisin lui-meme.")
    parser_install.add_argument("module", type=str, nargs="?", default="raisin", help="Nom du module")
    parser_install.add_argument("-U", "--upgrade", action="store_true", default=False, help="Fait la mise a jour.")

    # uninstall
    parser_uninstall = subparsers.add_parser("uninstall", help="Desinstaller un module python, possiblement raisin lui-meme.")
    parser_uninstall.add_argument("module", type=str, nargs="?", default="raisin", help="Nom du module.")

    # reinstall
    parser_reinstall = subparsers.add_parser("reinstall", help="Reinstaller l'application de raisin.")

    # upgrade
    parser_upgrade = subparsers.add_parser("upgrade", help="Met a jour raisin depuis le depos git.")

    # configuration
    parser_configure = subparsers.add_parser("configure", help="Personnaliser l'installation de raisin.")
    parser_configure.add_argument("category", type=str, nargs="?", choices=["all", "psw", "padlock"], default="all", help="Specifiez l'element a configurer.")

    # psw
    parser_psw = subparsers.add_parser("psw", help="Ajouter/Changer/Supprimer le mot de passe de raisin.")

    # padlock
    parser_padlock = subparsers.add_parser("padlock", help="Ajouter/Changer/Desactiver l'antivol de raisin.")

    # start
    parser_start = subparsers.add_parser("start", help="Executer l'application de raisin.")
    parser_start.add_argument("-S", "--serv", "--server", action="store_true", default=False, help="Demmare le serveur raisin pour partager les resources.")
    parser_start.add_argument("-U", "--upgrade", action="store_true", default=False, help="Fait la mise a jour si l'option est cochee.")


    parser_cipher = subparsers.add_parser("cipher", help="Chiffrer un fichier ou un dossier.")
    parser_cipher.add_argument("filename", type=str, nargs="+", help="Nom du fichier a chiffrer.")
    parser_cipher.add_argument("-p", "-psw", "--psw", "--password", type=str, nargs="?", default="", help="Permet d'entrer un mot de passe, s'il il est omis, la clef publique est utilisee.")

    parser_uncipher = subparsers.add_parser("uncipher", help="Dechiffrer un fichier ou un dossier.")
    parser_uncipher.add_argument("filename", type=str, nargs="+", help="Nom du fichier a chiffrer.")
    parser_uncipher.add_argument("-p", "-psw", "--psw", "--password", type=str, nargs="?", default="", help="Permet d'entrer un mot de passe, sil il est omis, la clef privee est utilisee.")

    return parser

def _install_raisin():
    import raisin.application.install as install
    return install.main()

def _uninstall_raisin():
    import raisin.application.uninstall as uninstall
    return uninstall.main()

def _upgrade_raisin():
    import raisin.application.upgrade as upgrade
    return upgrade.main()

def _configure_raisin():
    import raisin.application.configuration as configuration
    configuration.Config()
    return 0

def _psw_raisin():
    import raisin.security as security
    security.change_psw()
    return 0

def _padlock_raisin():
    import raisin.application.configuration as configuration
    configuration.change_padlock()
    return 0

def _start_server():
    import raisin.communication.tcp_server as tcp_server
    s = tcp_server.Server()
    s.start()

def _start_upgrade():
    import raisin.application.upgrade as upgrade
    return upgrade.automatic_update()

def main(args_brut=[]):
    """
    Retourne 0 en cas de success.
    'args_brut' permet de pouvoir passer des commandes plus facilement
    depuis un script directement.
    """
    parser = parse_arguments()
    if args_brut:
        args = parser.parse_args(args_brut)
    else:
        args = parser.parse_args()
    
    if args.parser_name == "install":
        if args.module == "raisin":
            if args.upgrade:
                return _upgrade_raisin()
            else:
                return _install_raisin()
        else:
            raise NotImplementedError("Impossible d'installer un aute module que raisin.")
    elif args.parser_name == "uninstall":
        if args.module == "raisin":
            return _uninstall_raisin()
        else:
            raise NotImplementedError("Je ne suis pas capable de desinstaller un module autre que raisin.")
    elif args.parser_name == "reinstall":
        return not ((not _uninstall_raisin()) and (not _install_raisin()))
    elif args.parser_name == "upgrade":
        return _upgrade_raisin()
    elif args.parser_name == "configure":       # si il faut configurer raisin
        if args.category == "all":
            return _configure_raisin()
        elif args.category == "psw":
            return _psw_raisin()
        elif args.category == "padlock":
            return _padlock_raisin()
    elif args.parser_name == "psw":
        return _psw_raisin()
    elif args.parser_name == "padlock":
        return _padlock_raisin()
    elif args.parser_name == "start":           # si il faut lancer des scripts specifiques
        apps = [func for func, arg
            in [(_start_server, args.serv),
                (_start_upgrade, args.upgrade)]
            if arg]
        if len(apps) == 0:
            raise NotImplementedError("Il faut specifier quoi lancer.")
        elif len(apps) == 1:
            return apps[0]()
        else:
            import multiprocessing
            threads = [multiprocessing.Process(target=app) for app in apps]
            [t.start() for t in threads]
            [t.join() for t in threads]
            return 0

    elif args.parser_name in ("cipher", "uncipher"):
        raise NotImplementedError("Impossible de chiffrer/dechifrer un fichier.")
    else:
        sys.stderr.write("Argument invalide.\nPour plus d'informations, tapez '%s -m raisin --help'\n" % sys.executable)
        return 1

if __name__ == "__main__":
    main()
