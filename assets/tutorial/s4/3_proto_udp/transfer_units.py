from enum import Enum


class RequestMessageType(Enum):
    """
    Tipuri de mesaje pe care clientul le poate trimite serverului.

    CONNECT    -> clientul se "înregistrează" la server
    SEND       -> trimite o notiță ce va fi stocată
    LIST       -> cere lista de notițe stocate
    DISCONNECT -> se "dezregistrează" de la server
    CLEAR      -> (de implementat de student) șterge notițele clientului
    """

    CONNECT = 1
    SEND = 2
    LIST = 3
    DISCONNECT = 4
    CLEAR = 5  # nou tip de mesaj (pentru studenți)


class ResponseMessageType(Enum):
    """
    Tipuri de răspunsuri pe care serverul le poate trimite clientului.

    OK            -> operație reușită
    ERR_CONNECTED -> clientul nu este înregistrat (ex. SEND fără CONNECT)
    ERR_UNKNOWN   -> tip de cerere necunoscut sau neacceptat
    """

    OK = 1
    ERR_CONNECTED = 2
    ERR_UNKNOWN = 3  # pentru cazuri neacoperite explicit


class RequestMessage:
    """
    Mesaj trimis de client către server.

    message_type -> un RequestMessageType
    payload      -> text opțional (folosit pentru SEND)
    """

    def __init__(self, message_type, payload=""):
        self.message_type = message_type
        self.payload = payload

    def __str__(self):
        return f"""
-------------REQUEST-------------
TYPE: {self.message_type}
PAYLOAD:
{self.payload}
---------------------------------
"""


class ResponseMessage:
    """
    Mesaj trimis de server către client.

    message_type -> un ResponseMessageType
    payload      -> text opțional (de ex. notițele la LIST)
    """

    def __init__(self, message_type, payload=""):
        self.message_type = message_type
        self.payload = payload

    def __str__(self):
        return f"""
-------------RESPONSE-------------
TYPE: {self.message_type}
PAYLOAD:
{self.payload}
----------------------------------
"""
