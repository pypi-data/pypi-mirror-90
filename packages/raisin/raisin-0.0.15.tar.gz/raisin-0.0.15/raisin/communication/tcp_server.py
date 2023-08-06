#!/usr/bin/env python3

"""
|========================================|
| C'est la partie qui permet de recevoir |
| des clients et de leur repondre.       |
|========================================|

Ce script permet seulement de faire le lien entre
les clients et le reste du programe. Les reponses
aux requettes ne sont pas faites ici.

Ce fichier est fortement influance par ce lien:
    https://www.neuralnine.com/tcp-chat-in-python/
"""

import multiprocessing
import os
import socket
import threading
import uuid

from ..tools import Printer, id_, Lock
from ..application import settings
from ..errors import *
from . import answering, checks


class Server:
    """
    |================================================|
    | Serveur raisin qui accepte les clients raisin. |
    |================================================|

    C'est un serveur qui supporte les requettes ipv6 et ipv4.
    Il accepte plusieurs clients a la fois jusqu'a la limite autorisee.

    exemple
    -------
    :Example:
    >>> from raisin.communication import tcp_server
    >>> s = tcp_server.Server()
    >>> s.start() # Methode bloquante.
    """
    def __init__(self):
        """
        Constructeur qui initialise juste les 
        sockets de facon locale.
        """
        with Printer("Initialisation of TCP servers...") as p:
            
            # partie environement
            self.clients = {}               # c'est tous les clients connectes

            # partie serveur
            self.port = settings.settings["server"]["port"]
            self.listen = settings.settings["server"]["listen"]
            self.ipv4 = id_["ipv4_lan"]
            self.ipv6 = id_["ipv6"]
            if self.ipv4 == None and self.ipv6 == None:
                raise OSError("Impossible de detecter l'ip, peut etre n'y a-t-il pas internet?")

            addr = ("", self.port)  # Toutes les interfaces, port 'self.port'
            if socket.has_dualstack_ipv6():
                self.tcp_socket = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True, reuse_port=True)
            else:
                self.tcp_socket = socket.create_server(addr, reuse_port=True)

    def is_accepted(self, public_key):
        """
        |====================================|
        | S'assure que le client est fiable. |
        |====================================|

        Ne pose aucune question a l'utilisateur, retourne sans attendre.

        entree
        ------
        :param public_key: C'est la clef publique du client a scruter.
        :type public_key: str

        sortie
        ------
        :return: True si le client a le droit de se connecter, False sinon.
        :rtype: boolean
        """
        with Printer("Testing if a pecific client is accepted...") as p:
            blacklisted = os.path.join(os.path.expanduser("~"), ".raisin/blacklisted.py")
            if os.path.exists(blacklisted):
                with open(blacklisted, "r", encoding="utf-8") as f:
                    if public_key.replace(b"\n", b"") in eval(f.read()):
                        p.show("It is accepted.")
                        return False
            whitelisted = os.path.join(os.path.expanduser("~"), ".raisin/whitelisted.py")
            if os.path.exists(whitelisted):
                with open(whitelisted, "r", encoding="utf-8") as f:
                    if public_key.replace(b"\n", b"") in eval(f.read()):
                        p.show("It is refoule.")
                        return True
            if settings.settings["server"]["accept_new_client"]:
                p.show("It is accepted.")
                return True
            p.show("Maybe, we must ask the question.")
            return None

    def accept(self, identity):
        """
        |=====================|
        | Memorise le client. |
        |=====================|

        Ajoute le client passe en parametre dans la liste blanche
        ou a la liste noir si l'utilisateur le veut.
        Si il faut attendre l'approbation de l'utilisateur,
        cette fonction est bloquante.

        entree
        ------
        :param identity: Carte d'identite du client.
        :type identity: dict

        sortie
        ------
        :return: True si le client est en mis en liste blanche, False sinon.
        :rtype: boolean
        """
        with Printer("Ask to user for accept a new client...") as p:
            import raisin.application.hmi.dialog as dialog

            is_a = self.is_accepted(identity["public_key"])
            if is_a == True:
                p.show("The client is already accepted.")
                return True
            if is_a == False:
                p.show("This client is already baned.")
                return False
            question =  "'%s' client shouaite se connecter.\n" % identity["username"] \
                        + "Il travail sur l'os '%s' sur le PC %s.\n" % (identity["os_version"], identity["hostname"]) \
                        + "Il est localise en %s a %s.\n" % (identity["country"], identity["city"]) \
                        + "Il pretend avoir l'adresse mac %s.\n" % identity["mac"]
            rep = dialog.question_binaire(question, default=None, existing_window=None)
            listed = "whitelisted.py" if rep else "blacklisted.py"
            path = os.path.join(os.path.expanduser("~"), ".raisin", listed)
            data = set()
            with Lock(id="listed", timeout=30, locality_degrees=2):
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        data = eval(f.read())
                data.add(identity["public_key"].replace(b"\n", b""))
                with open(path, "w", encoding="utf-8") as f:
                    f.write(repr(data))
            if rep:
                p.show("The client is desormais accepted.")
            else:
                p.show("This client is desormais baned.")
            return rep

    def close(self):
        """
        Permet de fermer proprement les sockets.
        """
        with Printer("Shutdown the server..."):
            # if self.tcp_socket_ipv4:
            #     self.receiver_ipv4.kill()
            #     self.tcp_socket_ipv4.close()
            # if self.tcp_socket_ipv6:
            #     self.receiver_ipv4.kill()
            #     self.tcp_socket_ipv6.close()
            for client in self.clients:
                client["socket"].shutdown() # Avertissement de l'autre cote: Je n’écoute pas, bon débarras!
                client["socket"].close()
            if hasattr(self, "tcp_socket"): # Si le constructeur n'a pas echoue.
                self.tcp_socket.close()

    def receive(self):
        """
        |==============================|
        | Cede les sockets des clients |
        | qui tentent de se connecter. |
        |==============================|

        sortie
        ------
        :return: Cede les variables:
            client_socket, (ip_client, port_client)
            des l'ors qu'un client tente de se connecter,
            que se soit en ipv4 ou en ipv6.
        :rtype: socket.socket
        :rtype: str
        :rtype: int
        """
        if self.ipv4 and self.ipv6:
            message = "aux adresses '%s' et '%s'" % (self.ipv6, self.ipv4)
        else:
            message = "a l'adresse '%s'" % (self.ipv6 if self.ipv6 else self.ipv4)
        with Printer("En ecoute sur le port %d %s..." % (self.port, message)) as p:
            '''
            Example de socket:
            en ipv6:
            (   <
                    socket.socket
                    fd=6,
                    family=AddressFamily.AF_INET6,
                    type=SocketKind.SOCK_STREAM,
                    proto=0,
                    laddr=('2a01:e0a:392:b810:ec:6034:b3de:5afa', 1025, 0, 0),
                    raddr=('2a01:e0a:392:b810:ec:6034:b3de:5afa', 52332, 0, 0)
                >,
                ('2a01:e0a:392:b810:ec:6034:b3de:5afa', 52332, 0, 0)
            )
            en ipv4:
            (   <
                    socket.socket
                    fd=5,
                    family=AddressFamily.AF_INET,
                    type=SocketKind.SOCK_STREAM,
                    proto=0,
                    laddr=('192.168.0.48', 1025),
                    raddr=('192.168.0.48', 35758)
                >,
                ('192.168.0.48', 35758)
            )
            '''
            while True:
                yield self.tcp_socket.accept()

    def handle(self, client_socket, key):
        """
        |====================================|
        | Satisfait les besoins d'un client. |
        |====================================|

        Cette methode doit etre lancee dans un thread.
        Sinon elle bloquerait tout et seul le premier
        client serait servis.
        Cette methode est bloquante.

        entree
        ------
        :param client_socket: Socket tcp du client que l'on ecoute.
        :type client_socket: socket.socket
        :param key: Clef publique du client.
        :type key: str

        sortie
        ------
        :return: True si la discution s'est bien passe. False si il y a un quoic.
        :rtype: boolean
        """
        while True:
            # Traitement des messages
            with Printer("Waiting for a reponse...") as p:
                try:
                    answer = answering.receive(client_socket)
                except NotCompliantError:
                    p.show("Not complient answer.")
                    del self.clients[key]
                    return False
                except OSError:
                    p.show("Erreur avec le socket TCP.")
                    try:
                        client_socket.shutdown() # Avertissement de l'autre cote: Je n’écoute pas, bon débarras!
                        client_socket.close()
                    except OSError:
                        pass
                    del self.clients[key]
                    return False
                else:
                    raise NotImplementedError

    def select(self):
        """
        |===============================|
        | Acceuil les nouveaux clients. |
        |===============================|

        Si le client est accepte, il est ajoute dans les clients connectes
        et un nouveau thread est cree rien que pour lui.
        Comme c'est ici que les clients debarquent tout d'abord, on est extremement mefiant
        envers eux pour une question de securitee. Plein de tests dont fait de
        facon a s'assurer qu'ils soit bien en regles.
        """
        for client_socket, inf in self.receive(): # on ne fait pas directement
            ip_client = inf[0]                     # client_socket, (ip_client, port_client)
            port_client = inf[1]                    # car le deuxieme tuple contient parfois 4 elements
            with Printer("Un client d'ip %s se connecte via le port %d..." % (ip_client, port_client)) as p:
                try:
                    if len(self.clients) >= settings.settings["server"]["listen"]: # si il y a deja trop de monde
                        p.show("Client expulse car il y a deja trop de monde connecte.")
                        answering.send_error(client_socket, "Desole, il y a deja trop de monde.")
                        answering.send_object(client_socket, answer)
                        continue
                    with Printer("Demande de plus amples informations..."):
                        question1 = {"type": "question", "question": "identity", "description": "How are you?"}
                        answering.send_object(client_socket, question1)
                        try:
                            identity = answering.receive(client_socket, timeout=30)
                        except socket.timeout:
                            p.show("Client expulse car il met trop de temps a repondre.")
                            answering.send_error(client_socket, "Tu es trop lent a repondre.")
                            continue
                        except NotCompliantError:
                            p.show("Client expulse car il est potentiellement dangereux.")
                            continue # Le message d'erreur est deja envoye depuis 'receive'
                        with Printer("Verification de la reponse..."):
                            error = checks.check_coherence(identity, question1)
                            if error:
                                p.show("Client expulse car il repond pas bien a la question.")
                                answering.send_error(client_socket, error)
                                continue
                            p.show("Le client a livre son identite.")
                        if settings.settings["server"]["force_authentication"]:
                            with Printer("Envoi d'un challenge pour confirmer l'identite..."):
                                import raisin.serialization.encrypt as encrypt
                                challenge = uuid.uuid4().bytes   # creation aleatoire d'une phrase 
                                question2 = {  
                                    "type": "question",                  # on chiffre cette phrase avec la clef publique du client
                                    "question": "challenge",
                                    "description": repr(encrypt.cipher(
                                        challenge,
                                        psw=identity["public_key"]))}
                                answering.send_object(client_socket, question2) # on demande au client de la dechiffrer
                                try:
                                    answer_challenge = answering.receive(client_socket, timeout=30)
                                except socket.timeout:
                                    p.show("Client expulse car il met trop de temps a repondre.")
                                    answering.send_error(client_socket, "Tu es trop lent a repondre.")
                                    continue
                                except NotCompliantError:
                                    p.show("Client expulse car il est potentiellement dangereux.")
                                    continue # Le message d'erreur est deja envoye depuis 'receive'
                                error = checks.check_coherence(answer_challenge, question2)
                                if error:
                                    p.show("Client expulse car il repond pas bien a la question.")
                                    answering.send_error(client_socket, error)
                                    continue
                                if answer_challenge["challenge"] != challenge:
                                    p.show("Client expulse car il n'a pas reussi le defit.")
                                    answering.send_error(client_socket, "Vous etes un escrot, vous n'avez pas reussi le defit!")
                                    continue
                                p.show("Le client a reussi le defit.")
                        autorization = self.is_accepted(identity["public_key"])
                        if autorization == None: # si il faut demander l'avis
                            threading.Thread(target=self.accept, args=(identity.copy(),)).start() # on pose la question a l'utilisateur
                            p.show("Client expulse car l'utilisateur n'a pas encore donne son accord.") # mais on attend pas qu'il reponde
                            answering.send_error(client_socket, "Il faut attendre l'avis de l'utilisateur.")
                            continue
                        elif autorization == False:  # si il faut le virer
                            p.show("Client expulse car il n'a pas le droit de metre les pieds ici!")
                            answering.send_error(client_socket, "Tu n'a pas le droit de metre les pieds ici!")
                            continue
                        if identity["public_key"].replace(b"\n", b"") in self.clients:
                            p.show("Client expulse car il est deja connecte.")
                            answering.send_error(client_socket, "Tu es deja connecte.")
                            continue
                        p.show("Client accepte.")
                    with Printer("Ajout de ce client dans le serveur..."):
                        key = identity["public_key"].replace(b"\n", b"")
                        self.clients[key] = {
                            "username": identity["username"],
                            "os_version": identity["os_version"],
                            "hostname": identity["hostname"],
                            "country": identity["country"],
                            "city": identity["city"],
                            "mac": identity["mac"],
                            "ip": ip_client,
                            "port": port_client,
                            "socket": client_socket,
                            "thread": multiprocessing.Process(
                                target=self.handle,
                                args=(client_socket, key))}
                        self.clients[key]["thread"].start()
                except OSError: # Si il y a un proble avec ce socket entre temps,
                    continue # on ne fait pas planter le serveur en entier.

    def start(self):
        """
        |====================|
        | Demare le serveur. |
        |====================|
        """
        return self.select()

    def __del__(self):
        self.close()

def main():
    """
    Lance le serveur.
    """
    s = Server()
    s.start()

if __name__ == '__main__':
    main()
