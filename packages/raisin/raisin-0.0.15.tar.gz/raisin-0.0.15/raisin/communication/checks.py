#!/usr/bin/env python3

"""
|====================|
| Client protection. |
|====================|

C'est une sorte de mini anti-virus.
Quand le serveur raisin recoit des requettes client ou que
les clients recoivent des requettes du serveur, les donnees
sont deserialisee puis sont imediatement verifiees. En python,
Il est aise de faire des extension de classe et de redefinir (hacker)
certaine methodes pour qu'elle fassent des choses vilaines.
Ici, on s'assure que les objets deserialises soit le plus inofancif
possible. On s'assure qu'ils ne soient pas issus d'extansion douteuse de classe
et qu'ils respectent a la lettre les convention de raisin.
Tout cela dans le but d'assurer un maximum de secrite.
"""

import re

def check(obj):
    """
    |===========================|
    | S'assure que l'objet      |
    | respecte les conventions. |
    |===========================|

    C'est la fonction principale de ce module.
    Pour limiter les risques, la verification doit
    etre faite le plus tot possible.

    entree
    ------
    :param obj: L'objet que l'on vient de recevoir
        du client ou du serveur.

    sortie
    ------
    :return: Le message d'erreur si l'objet
        n'est pas convenable. Une chaine vide
        si l'objet passe tous les tests.
    :rtype: str
    """
    # Verifications generales.
    if type(obj) is not dict:
        return "Un dictionaire est attendu. Or c'est un %s." \
            % type(obj).__name__
    if "type" not in obj:
        return "Il doit y avoir une clef 'type'."
    if type(obj["type"]) is not str:
        return "La valeur associee a la clef 'type'" \
            "doit imperativement etre de type str. Pas %s." \
            % type(obj["type"]).__name__

    # Verifications specifiques.
    if obj["type"] == "error":
        return check_error(obj)
    elif obj["type"] == "question":
        return check_question(obj)
    elif obj["type"] == "answer":
        return check_answer(obj)
    else:
        return "Le type %s n'est pas accepte." % repr(obj["type"])

def check_type(obj):
    """
    |====================================|
    | Verifie que l'objet soit standard. |
    |====================================|

    S'assure que l'objet est entierement constitue
    de types de base present nativement dans python.
    Pour les objet iterable, une veriication
    recursive est effectuee.
    Les seuls type autorises sont: int, float, str,
    tuple, list, dict, None, bool, complex, set, bytes

    entree
    ------
    :param obj: L'objet que l'on souaite surveiller.
    :type obj: object

    sortie
    ------
    :return: Un booleen qui vaut:
        -True si l'objet est standard.
        -False si il possede un autre type
    :rtype: boolean
    """
    # Cas standard non iterable.
    if type(obj) in [int, float, str, bool, complex, bytes, type(None)]:
        return True
    # Cas standard simplement iterable.
    elif type(obj) in [tuple, list, set]:
        return all(map(check_type, obj))
    # Cas dictionaire
    elif type(obj) is dict:
        return check_type(list(obj.keys())) and check_type(list(obj.values()))
    return False

def check_error(error):
    """
    |===============================|
    | S'assure que 'error' soit     |
    | un message d'erreur correcte. |
    |===============================|
    
    S'assure que 'error' soit de la forme:
    {'type': 'error', 'message': str}
    Une pre-verification doit deja etre faite.
    Cette pre-verification s'assure que 'error' soit
    un dictionaire et que le champ 'error' soit bien
    associe a la clef 'type'.

    entree
    ------
    :param error: Message recut par le serveur.
    :type error: dict

    sortie
    ------
    :return: Le message d'erreur si quelque
        chose ne va pas. Une chaine vide si tou est bon.
    :rtype: str
    """
    assert isinstance(error, dict), "La pre-verification n'a pas ete faite."

    # Contenu non hacke.
    if not check_type(error):
        return "Le message contient des classes interdites."
    
    # Type des clefs.
    if not all(map(lambda k: isinstance(k, str), error.keys())):
        return "Toute les clefs doivent etre de type 'str'."
    
    # Valeur des clefs.
    keys = {"type", "message"}
    if set(error.keys()) != keys:
        if set(error.keys()) - keys:
            return "Les/la clef(s) %s sont en trop dans le message d'erreur." \
                % ", ".join(set(error.keys()) - keys)
        return "Il manque les clefs %s dans le message." \
            % ", ".join(keys - set(error.keys()))

    # Type du message.
    if not isinstance(error["message"], str):
        return "Le message d'erreur doit etre de type str, pas %s." \
            % type(error["message"]).__name__

    return ""

def check_question(question):
    """
    |==============================|
    | S'assure que 'question' soit |
    | une requette correcte.       |
    |==============================|
    
    S'assure que 'question' soit de la forme:
    {'type': 'question', 'question': str, 'description': str}
    Une pre-verification doit deja etre faite.
    Cette pre-verification s'assure que 'question' soit
    un dictionaire et que le champ 'type' soit bien
    associe a la clef 'question'.

    entree
    ------
    :param question: Message que l'on shouaite
        envoyer au client ou au serveur.
    :type question: dict

    sortie
    ------
    :return: Le message d'erreur si quelque
        chose ne va pas. Une chaine vide si tout est bon.
    :rtype: str
    """
    assert isinstance(question, dict), "La pre-verification n'a pas ete faite."

    # Contenu non hacke.
    if not check_type(question):
        return "La question contient des classes interdites."

    # Type des clefs.
    if not all(map(lambda k: isinstance(k, str), question.keys())):
        return "Toute les clefs doivent etre des type 'str'."

    # Valeur des clefs.
    keys = {"type", "question", "description"}
    if set(question.keys()) != keys:
        if set(question.keys()) - keys:
            return "Les/la clef(s) %s sont en trop dans la question." \
                % ", ".join(set(question.keys()) - keys)
        return "Il manque les clefs %s dans la question." \
            % ", ".join(keys - set(question.keys()))

    # Type question["question"]
    if type(question["question"]) not in [int, str]:
        return "La question doit etre de type str, ou int pas %s." \
            % type(question["question"]).__name__

    # Type question["description"]
    if not isinstance(question["description"], str):
        return "La description doit etre de type str pas %s." \
            % type(question["description"]).__name__

    # Cas d'un challenge.
    if question["question"] == "challenge":
        try:
            if not isinstance(eval(question["description"]), bytes):
                return "Le challenge doit etre la representation d'une chaine d'octet."
        except (ValueError, SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
            return ", ".join(e.args)

    return ""

def check_answer(answer):
    """
    |============================|
    | S'assure que 'answer' soit |
    | une reponse correcte.      |
    |============================|
    
    S'assure que 'answer' soit de la forme:
    {'type': 'answer', 'question', str}
    Une pre-verification doit deja etre faite.
    Cette pre-verification s'assure que 'answer' soit
    un dictionaire et que le champ 'type' soit bien
    associe a la clef 'answer'.

    entree
    ------
    :param answer: Message recu par un client
        ou un serveur juste apres lui avoir pose une question.
    :type question: dict

    sortie
    ------
    :return: Le message d'erreur si quelque
        chose ne va pas. Une chaine vide si tout est bon.
    :rtype: str
    """
    assert isinstance(answer, dict), "La pre-verification n'a pas ete faite."

    if "question" not in answer:
        return "Il manque la clef 'question'"

    if type(answer["question"]) is not str:
        return "Le champ associe a la clef 'question' doit etre str. Pas %s." \
            % type(answer["question"]).__name__

    # Reponse a un challenge.
    if answer["question"] == "challenge":
        if not check_type(answer):
            return "Seul les types standard sont autorises."
    
    # Piece d'identite
    elif answer["question"] == "identity":
        if not check_type(answer):
            return "Seul les types standard sont autorises."
        required_keys = {"type": str, "question": str, "username": str,
            "os_version": str, "hostname": str, "country": str,
            "city": str, "mac": str, "public_key": bytes}
        
        if set(required_keys.keys()) - set(answer.keys()):
            return "Il manque la/les clef(s): %s." \
                % ", ".join(set(required_keys.keys()) - set(answer.keys()))
        if not all(isinstance(answer[k], t) for k, t in required_keys.items()):
            return "Le type des valeur n'est pas " \
                "respecter, il doit etre: %s." % required_keys
        try:
            if not re.search(
                    r"-----BEGIN PUBLIC KEY-----(.|\n)+-----END PUBLIC KEY-----",
                    answer["public_key"].decode()):
                return "La clef publique n'est pas au format 'PEM'."
        except UnicodeDecodeError as e:
            return "La clef publique RSA n'est pas au format PEM"

    return ""

def check_coherence(answer, question):
    """
    |==============================|
    | S'assure que la reponse soit |
    | coherente avec la question.  |
    |==============================|

    'answer' doit etre deja verifie par 'check'.
    Les verifications des conventions doivent donc etre
    deja faites par ailleur.
    'question' ne doit pas etre verifier car elle a etee
    generer localement.
    Plus precisement, s'assure la reponse
    est bien la reponse a la bonne question.

    entree
    ------
    :param question: La question posee.
    :type question: dict
    :param answer: La reponse recut deja scannee par l'anti-virus.
    :type answer: dict

    sortie
    ------
    :return: Le message d'erreur si quelque
        chose ne va pas. Une chaine vide si tout est bon.
    :rtype: str
    """
    assert isinstance(answer, dict), "La pre-verification n'a pas ete faite."

    if answer["type"] != "answer":
        return "Une reponse est attendue, pas un %s." % repr(answer["type"])

    if question["question"] != answer["question"]:
        return "Il faut repondre a la question %s. Pas %s." \
            % (repr(question["question"]), repr(answer["question"]))


    return ""


