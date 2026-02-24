import pickle
import io


def serialize(message) -> bytes:
    """
    Generic serialisation of a RequestMessage or ResponseMessage
    into a byte sequence, using pickle.

    BytesIO is used as an in-memory buffer:
      - pickle.dump(message, stream)
      - stream.getvalue() -> bytes
    """
    stream = io.BytesIO()
    pickle.dump(message, stream)
    serialized_message = stream.getvalue()
    return serialized_message


def deserialize(message_bytes: bytes):
    """
    Deserialisation from bytes into a RequestMessage or ResponseMessage.

    Uses BytesIO + pickle.load().
    """
    stream = io.BytesIO(message_bytes)
    deserialized_message = pickle.load(stream)
    return deserialized_message
