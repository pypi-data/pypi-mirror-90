#!/usr/bin/env python3

"""
En cas de plantage de raisin,
Les erreurs sont recuperes et envoyees
par couriel. Ainsi, les developeurs peuvent corriger
des erreurs de raisin.
"""

import os
import re
import sys
import time

def crash_report(exc_type, value, traceback):
    """
    Il faut uiliser cet objet de la facon suivante:
    sys.excepthook = crash_report
    """
    def get_filenames(traceback):
        if traceback:
            return list(set([os.path.abspath(traceback.tb_frame.f_code.co_filename)]+get_filenames(traceback.tb_next)))
        return []

    def get_raisin_filenames():
        """
        genere tous les fichiers qui constituent le module raisin
        """
        for father, dirs, files in os.walk(os.path.dirname(raisin.__file__)):
            for file in files:
                yield os.path.join(father, file)

    def is_time():
        """
        Retourne True si cette fonction a ete appellee
        il y a plus d'une heure.
        """
        filename = os.path.join(os.path.expanduser("~"), ".raisin", "last_crash")
        t = 0
        if os.path.exists(filename):
            with open(filename, "r") as f:
                t = eval(f.read())

        if time.time() - t > 3600:
            with open(filename, "w") as f:
                f.write(str(time.time()))
            return True
        return False

    import raisin
    import raisin.tools
    import raisin.communication.mail as mail
    import raisin.serialization.decrypt as decrypt

    sys.stderr.write("Uh... I planted! I am dead!")

    if is_time() and exc_type not in [KeyboardInterrupt, EOFError, decrypt.DecryptError]:
        filenames = get_filenames(traceback)            # recuperation de tous les fichiers qui contribuent au plantage
        if set(filenames) & set(get_raisin_filenames()):# si raisin est concerne par ce plantage
            ancien_stderr = sys.stderr
            with open(os.path.join(raisin.tools.temprep(), "erreur.txt"), "w") as f:
                sys.stderr = f
                sys.__excepthook__(exc_type, value, traceback)
            sys.stderr = ancien_stderr
            with open(os.path.join(raisin.tools.temprep(), "erreur.txt"), "r") as f:
                traceback_txt = f.read()
            sys.stderr.write(traceback_txt)
            os.remove(os.path.join(raisin.tools.temprep(), "erreur.txt"))
            raisin.tools.Printer(display=5)                   # on force l'affichage

            with raisin.tools.Printer("Envoi du rapport de plantage..."):
                message = "type:%s\nvalue:%s\n\n%s\n\n%s" % (exc_type, value, raisin.tools.id_, traceback_txt)
                adresse = re.search(r"[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]{2,}\.[a-z]{2,4}", raisin.__author__).group() # recuperation de l'adresse du createur
                mail.send(adresse, "raisin: crash report", message, attachment=get_filenames(traceback))
        else:
            sys.__excepthook__(exc_type, value, traceback)
    else:
        sys.__excepthook__(exc_type, value, traceback)
