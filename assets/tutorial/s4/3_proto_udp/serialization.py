import pickle
import io


def serialize(message) -> bytes:
    """
    Serializare generică a unui RequestMessage sau ResponseMessage
    într-o secvență de bytes, folosind pickle.

    Folosim BytesIO ca buffer în memorie:
      - pickle.dump(message, stream)
      - stream.getvalue() -> bytes
    """
    stream = io.BytesIO()
    pickle.dump(message, stream)
    serialized_message = stream.getvalue()
    return serialized_message


def deserialize(message_bytes: bytes):
    """
    Deserializare din bytes către un RequestMessage sau ResponseMessage.

    Folosim BytesIO + pickle.load().
    """
    stream = io.BytesIO(message_bytes)
    deserialized_message = pickle.load(stream)
    return deserialized_message
