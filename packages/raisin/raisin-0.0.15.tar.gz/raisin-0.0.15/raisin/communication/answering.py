#!/usr/bin/env python3

"""
|====================================|
| Repond a une requette d'un client. |
|====================================|

Il permet aussi la gestion bas niveau des sockets TCP
afin de serialiser/deserialiser les requettes et les reponses.
"""

import re
import socket

from ..tools import Printer
from ..errors import *
from . import checks


def send_data(s, data):
    """
    |====================|
    | Envoi des donnees. |
    |====================|

    Ne fait pas de verifications sur les entrees car
    cette fonction n'est pas destinee a l'utilisateur
    mais aux devlopeurs et aux autres fonctions.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket
    :param data: Les donnee serialises a envoyer.
    :type data: generator.
    """
    with Printer("Envoi des donnees...") as p:
        import raisin.serialization.tools as tools
        for is_end, data in tools.anticipate(tools.to_gen(gen=data)):
            p.show("data: %s" % data)
            s.send(bytes([is_end]) + data)

def send_object(s, obj):
    """
    |========================|
    | Envoi un objet python. |
    |========================|

    Ne fait pas de verifications sur les entrees car
    cette fonction n'est pas destinee a l'utilisateur
    mais aux developeurs et aux autres fonctions.

    Fonctione de la meme facon que 'send_data'.
    N'est efficace que pour le petits objets. Si les
    objets sont lourd, utilisez 'send_data'.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket
    :param obj: Objet python a envoyer.
    :type obj: object
    """
    with Printer("Envoi d'un objet..."):
        import raisin.serialization.serialize as serialize
        return send_data(s,
            serialize.serialize(
                obj,
                compresslevel=0,
                copy_file=False,
                psw=None,
                authenticity=False,
                parallelization_rate=0))

def send_error(s, message):
    """
    |======================================|
    | Envoi un message d'erreur au client. |
    |======================================|

    Envoi un message d'erreur bien formatter pour pouvoir
    passer les controles a la douane.
    Ferme la connection. Comme ca le client ne peut
    plus nous embeter.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket
    :param message: Le message d'erreur a envoyer.
    :type message: str
    """
    assert isinstance(message, str), \
        "Le message d'erreur doit etre une chaine de " \
        "caractere. Pas un %s." % type(message).__name__

    send_object(s, {"type": "error", "message": str(message)}) # les str compte car on verifie l'heritage.
    s.shutdown()
    s.close()

def receive(s, timeout=None):
    """
    |============================================|
    | Reception les donnees et les deserialises. |
    |============================================|

    Deserialise les donnes au fur a mesure qu'elles arrivent.
    S'assure que les donnees aient le bon format.

    Fait deja quelques verifications sur les entrees.
    Si les entree ne sont pas bonne, Le message d'erreur
    est envoye puis la communication est coupee.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket
    :param timeout: Permet de lever une exception si c'est trop long.
    :type timeout: int, float

    sortie
    ------
    :return: L'objet de depart envoye par le socket.
    :rtype: object
    :raises NotCompliantError: Si les donnes recut ne sont pas conformes.
    """
    def gen_receive(s, timeout):
        """
        Cede les donnees au fur a mesure qu'elles arrivent.
        """
        with Printer("Reception des donnees brutes...") as p:
            import raisin.serialization.constants as constants
            default_timeout = s.gettimeout() # Peut renvoyer None si il n'y a pas de timeout.
            s.settimeout(timeout)
            
            data = s.recv(constants.BUFFER_SIZE)
            p.show("Data: %s" % data)
            yield data[1:]
            while not data or data[0] == 0:
                data = s.recv(constants.BUFFER_SIZE)
                p.show("Data: %s" % data)
                yield data[1:]
            if data[0] != 1: # Normalement le premier octet vaut 0 ou 1, c'est tout!
                raise HeaderError(
                    "Les paquets recut doivent commencer par "
                    "b'\\x00' ou b'\\x01'. Pas %s." % bytes([data[0]]))

            s.settimeout(default_timeout)

    with Printer("Reception des donnes deserialisee...") as p:
        import raisin.serialization.deserialize as deserialize

        answer = deserialize.deserialize(gen_receive(s, timeout), psw=None, parallelization_rate=0)
        error = checks.check(answer)
        if error:
            p.show("Erreur detectee: %s" % error)
            send_error(s, error)
            raise NotCompliantError(
                "Reponse non conforme et donc suspicieuse.",
                "Cause de la suspicion: %s" % error)
        return answer

def answering(request):
    """
    |========================|
    | Repond a une requette. |
    |========================|

    entree
    ------
    :param request: La requette deserialise et verifiee au maximum.
        La requete est recuperee via 'receive'.
    :type request: dict

    sortie
    ------
    :return: La reponse a la requette.
    :rtype: dict
    """
    with Printer("Response to the request...") as p:
        if request["type"] == "question":
            p.show("It is a simple question.")
            if request["question"] == "identity":
                p.show("I give your identity.")
                import raisin.tools as tools
                import raisin.application.settings as settings
                return {**{"type": "answer",
                        "question": "identity",
                        "public_key": settings.settings["account"]["security"]["public_key"]},
                        **dict(tools.id_)}
            if request["question"] == "challenge":
                p.show("I try to solve a challenge.")
                import raisin.serialization.decrypt as decrypt
                print(request)
                try:
                    return {"type": "answer", "question": "challenge",
                        "challenge": decrypt.decipher(eval(request["description"]))}
                except DecryptError:
                    return {"type": "error", "message": "Challenge trop difficile."}


        return {"type": "error", "message": "incomprehensible request."}
