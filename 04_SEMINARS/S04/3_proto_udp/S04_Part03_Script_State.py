class State:
    """
    Server state for the UDP protocol.

    - connections: dict client_address -> list of notes (strings)
      * client_address is a tuple (ip, port) received from recvfrom()

    Operations:
      - add_connection(address)
      - add_note(address, note)
      - get_notes(address) -> string with all notes, separated by '\\n'
      - clear_notes(address) -> (for students) clears the notes
      - remove_connection(address)
    """

    def __init__(self):
        self.connections = {}

    def add_connection(self, address):
        """
        Register the client in the dictionary if it does not already exist.
        """
        self.connections.setdefault(address, [])

    def add_note(self, address, note: str):
        """
        Add a note for the client identified by 'address'.
        Assumes that address already exists in connections.
        """
        self.connections[address].append(note)

    def get_notes(self, address) -> str:
        """
        Return all notes for a client, concatenated with '\\n'.
        If no notes exist, returns an empty string.
        """
        return "\n".join(self.connections[address])

    def clear_notes(self, address):
        """
        Clear all notes for the client (to be implemented by the student
        in the template; this is the example implementation).
        """
        self.connections[address] = []

    def remove_connection(self, address):
        """
        Completely remove the client from the dictionary.
        """
        del self.connections[address]
