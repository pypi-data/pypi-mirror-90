#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import ipaddress
import socket
import select
import sys
import threading

import raisin


class Client(threading.Thread):
    """
    Unique client TCP.
    Unique car il faut creer un objet par connection,
    chaque client est associe a un serveur.
    """
    def __init__(self, ip, port=0, signature=None):
        assert type(ip) is str, "L'ip doit etre une chaine de caractere."
        assert type(port) is int, "Le port doit etre un entier."
        assert port >= 0, "Le port doit etre positif ou nul."

        threading.Thread.__init__(self)
        self.signature = signature          # c'est la signature pour l'imprimente
        self.server_infos = {               # les informations concernant le serveur
            "ipv4_wan": None,
            "ipv4_lan": None,
            "ipv6": None,
            "dns_ipv4": None,
            "dns_ipv6": None,
            "port": None,
            "port_forwarding": None,
            "last_check": None,
        }
        self.server_in_lan = None           # booleen qui permet de dire si le serveur que l'on cherche a joindre est sur le meme reseau local que ce client

        with raisin.Printer("Initialisation of client..." , signature=signature) as p:
            # recherche des informations permetant de creer une connection
            
            # cas d'un nom de domaine raisin
            infos = raisin.communication.dns.get(ip, signature=self.signature)
            if infos: # si le serveur est deja recence par raisin
                self.server_infos = infos
                if infos["ipv4_lan"] != None and infos["ipv4_wan"] == str(raisin.Id().ipv4_wan): # si ce serveur a la meme ip publique
                    self.server_in_lan = True # c'est qu'il fait parti du meme reseau local
                    p.show("Server (lan) ipv4: %s, port: %d." % (infos["ipv4_lan"], infos["port"]))
                elif infos["port_forwarding"]: # si il est de toute facon accessible depuis l'exterieur
                    self.server_in_lan = False # on considere que le serveur est dehors
                    if infos["ipv6"]:
                        p.show("Server ipv6: %s, port: %d." % (infos["ipv6"], infos["port_forwarding"]))
                    if infos["ipv4_wan"]:
                        p.show("Server (wan) ipv4: %s, port: %d." % (infos["ipv4_wan"], infos["port_forwarding"]))
                else:
                    raise RuntimeError("Serveur non local, son port externe est inconu.")

            else:
                # cas d'un vrai nom de dommaine
                dns = ip
                ip_dns = raisin.communication.dns.is_domain(ip, signature=signature)
                if ip_dns:
                    ip = ip_dns
                    p.show("Domain %s translated in %s." % (dns, ip))

                # cas d'une ipv6 ou d'une ipv4
                if raisin.communication.dns.is_ipv6(ip):
                    self.server_infos["ipv6"] = ip
                    p.show("Server ipv6: %s." % ip)
                    if ip_dns:
                        self.server_infos["dns_ipv6"] = dns
                elif raisin.communication.dns.is_ipv4(ip):
                    p.show("Server ipv4: %s." % ip)
                    if ip_dns:
                        self.server_infos["dns_ipv4"] = dns
                else:
                    raise RuntimeError("Entree incorrecte, ce n'est ni une ip, ni un nom de domaine.")
                self.server_in_lan = ipaddress.ip_address(ip).is_private
                if not self.server_infos["ipv6"]:
                    if self.server_in_lan:
                        self.server_infos["ipv4_lan"] = ip
                        p.show("Server in (lan).")
                    else:
                        self.server_infos["ipv4_wan"] = ip
                        p.show("Server in (wan).")

                # le port
                if 0 == port:
                    raise RuntimeError("Le port doit etre precise.")
                if self.server_in_lan:
                    self.server_infos["port"] = port
                else:
                    self.server_infos["port_forwarding"] = port
                p.show("Port: %d." % port)

            # creation de la connection
            self.tcp_socket = None
            if self.server_infos["ipv6"]:
                try: # on tente d'abord en ipv6
                    self.tcp_socket = socket.socket(
                        socket.AF_INET6,        # socket internet en ipv6
                        socket.SOCK_STREAM)     # creation d'un TCP/IP socket, SOCK_STREAM => TCP
                    self.tcp_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)
                    p.show("Socket initialised in ipv6.")
                except Exception as e: # si la connection en ipv6 a echouee
                    pass
            if self.tcp_socket == None and self.server_infos["ipv4_lan"] and self.server_infos["port"] or self.server_infos["ipv4_wan"] and self.server_infos["port_forwarding"]:
                try: # allors on essay en ipv4
                    self.tcp_socket = socket.socket(
                        socket.AF_INET,         # socket internet plutot qu'un socket unix
                        socket.SOCK_STREAM)     # creation d'un TCP/IP socket, SOCK_STREAM => TCP
                    self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # on tente de reutiliser le port si possible
                    p.show("Socket initialised in ipv4.")
                except Exception as e:
                    pass
            if self.tcp_socket == None:
                raise RuntimeError("Impossible de creer un socket TCP, peut etre n'y a-t-il pas internet?")

    def connect(self):
        """
        se connecte reelement au serveur
        """
        ip = None
        port = None
        with raisin.Printer("Connection au serveur...", signature=self.signature) as p:
            # recuperations des donnees
            if self.server_infos["ipv6"]:
                ip = self.server_infos["ipv6"]
                if self.server_in_lan:
                    port = self.server_infos["port"]
                else:
                    port = self.server_infos["port_forwarding"]
            elif self.server_infos["ipv4_wan"] or self.server_infos["ipv4_lan"]:
                if self.server_in_lan:
                    ip = self.server_infos["ipv4_lan"]
                    port = self.server_infos["port"]
                else:
                    ip = self.server_infos["ipv4_wan"]
                    port = self.server_infos["port_forwarding"]
            else:
                raise RuntimeError("Le serveur n'a pas d'ip.")
            if port == None:
                raise RuntimeError("Le port de connecvtion est inconu!")
            if ip == None:
                raise RuntimeError("L'ip n'est pas connue!")

            # connection veritable
            self.tcp_socket.connect((ip, port))


    def run(self):
        """
        Methode special appelle par la classe parente.
        Au moment ou l'on fait: self.start()
        """
        pass


"""
copier coller du site
"""

def example():
    # Choosing Nickname
    nickname = input("Choose your nickname: ")

    # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 55555))

    # Listening to Server and Sending Nickname
    def receive():
        while True:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    print(message)
            except:
                # Close Connection When Error
                print("An error occured!")
                client.close()
                break

    # Sending Messages To Server
    def write():
        while True:
            message = '{}: {}'.format(nickname, input(''))
            client.send(message.encode('ascii'))

    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()




