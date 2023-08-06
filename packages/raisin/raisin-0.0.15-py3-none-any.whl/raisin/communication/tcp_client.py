#!/usr/bin/env python3

"""
|===========================================|
| C'est la partie qui permet de             |
| contacter des serveur et de les harceler. |
|===========================================|

Ce script permet de se connecter a des serveurs tcp
et de leur demander des services. C'est la partie de raisin
qui permet d'envoyer ailleur le travail a faire.

Ce fichier est fortement influance par ce lien:
    https://www.neuralnine.com/tcp-chat-in-python/
"""


import ipaddress
import socket
import select
import sys
import threading

from ..tools import Printer
from ..application import settings
from . import answering, dns as dns_tools


class Client(threading.Thread):
    """
    |===================================|
    | Client tcp lie a un seul serveur. |
    |===================================|

    Il faut creer un objet par connection.

    exemple
    -------
    :Example:
    >>> from raisin.communication import tcp_client
    >>> c = tcp_client.Client("adresse_ip", 20001) # Il faut qu'il y ai un serveur en ecoute.
    >>> c.start()
    """
    def __init__(self, ip, port=settings.settings["server"]["port"]):
        """
        |=========================|
        | Se connecte au serveur. |
        |=========================|

        entree
        ------
        :param ip: Adresse ip (v4 ou v6) ou dns du serveur.
        :type ip: str
        :param port: Port d'ecoute du serveur.
        :type port: int
        """
        assert isinstance(ip, str), \
            "L'ip doit etre une chaine de caractere, pas un %s." % type(ip).__name__
        assert isinstance(port, int), \
            "Le port doit etre un entier, pas un %s." % type(port).__name__
        assert port >= 0, "Le port doit etre positif. Ot il vaut %d." % port

        threading.Thread.__init__(self)

        self.port = port # Port du serveur.
        self.version = None # Version ipv4 ou ipv6
        self.server_in_lan = None # Booleen qui permet de dire si le serveur que l'on
                                  # cherche a joindre est sur le meme reseau local que ce client.
        self.tcp_socket = None # Socket tcp du serveur.
        self.answers = [] # Les reponses du serveur.

        with Printer("Initialisation of client...") as p:
            # Cas connection via nom de domaine.
            self.ip = dns_tools.is_domain(ip)
            if self.ip:
                p.show("Domain %s translated in %s." % (ip, self.ip))
            self.ip = self.ip if self.ip else ip

            # Cas d'une ipv6 ou d'une ipv4.
            if dns_tools.is_ipv6(self.ip):
                self.version = 6
            elif dns_tools.is_ipv4(self.ip):
                self.version = 4
            else:
                raise RuntimeError("Entree incorrecte, ce n'est ni une ip, ni un nom de domaine.")
            p.show("Server ipv%d: %s." % (self.version, self.ip))

            self.server_in_lan = ipaddress.ip_address(self.ip).is_private
            if self.server_in_lan:
                p.show("Server in local network (LAN).")
            else:
                p.show("Server non local (WAN).")
            p.show("Port: %d." % self.port)

            # Creation du socket en local.
            self.tcp_socket = None
            if self.version == 6:
                self.tcp_socket = socket.socket(
                    socket.AF_INET6,        # socket internet en ipv6
                    socket.SOCK_STREAM)     # creation d'un TCP/IP socket, SOCK_STREAM => TCP
                self.tcp_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)
                p.show("Local socket initialised in ipv6.")
            elif self.version == 4:
                self.tcp_socket = socket.socket(
                    socket.AF_INET,         # socket internet plutot qu'un socket unix
                    socket.SOCK_STREAM)     # creation d'un TCP/IP socket, SOCK_STREAM => TCP
                self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # on tente de reutiliser le port si possible
                p.show("Local socket initialised in ipv4.")
            else:
                raise RuntimeError("Impossible de creer un socket TCP, peut etre n'y a-t-il pas internet?")

            # Connection au serveur.
            self.tcp_socket.connect((self.ip, self.port))

    def run(self):
        """
        |====================|
        | Ecoute le serveur. |
        |====================|

        Methode special appelle par la classe parente
        au moment ou l'on fait: self.start().
        """
        while 1:
            try:
                # Traitement des messages.
                with Printer("Waiting for a reponse...") as p:
                    answer = answering.receive(self.tcp_socket)
                    if answer["type"] == "question":
                        answering.send_object(self.tcp_socket, answering.answering(answer))

            except Exception as e:
                # Suppresion et extermination du client.
                self.tcp_socket.shutdown(0) # Avertissement de l'autre cote: Je n’écoute pas, bon débarras!
                self.tcp_socket.close()
                raise e from e
