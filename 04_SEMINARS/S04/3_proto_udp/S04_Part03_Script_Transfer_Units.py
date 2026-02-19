from enum import Enum


class RequestMessageType(Enum):
    """
    Message types that the client may send to the server.

    CONNECT    -> the client "registers" with the server
    SEND       -> sends a note to be stored
    LIST       -> requests the list of stored notes
    DISCONNECT -> "deregisters" from the server
    CLEAR      -> (to be implemented by the student) clears the client's notes
    """

    CONNECT = 1
    SEND = 2
    LIST = 3
    DISCONNECT = 4
    CLEAR = 5  # new message type (for students)


class ResponseMessageType(Enum):
    """
    Response types that the server may send to the client.

    OK            -> operation succeeded
    ERR_CONNECTED -> the client is not registered (e.g. SEND without CONNECT)
    ERR_UNKNOWN   -> unrecognised or unsupported request type
    """

    OK = 1
    ERR_CONNECTED = 2
    ERR_UNKNOWN = 3  # for explicitly uncovered cases


class RequestMessage:
    """
    Message sent from the client to the server.

    message_type -> a RequestMessageType
    payload      -> optional text (used for SEND)
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
    Message sent from the server to the client.

    message_type -> a ResponseMessageType
    payload      -> optional text (e.g. the notes for LIST)
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
