class State:
    """
    Starea serverului pentru protocolul UDP.

    - connections: dict adresă_client -> listă de notițe (string-uri)
      * adresă_client este tuplu (ip, port) primit din recvfrom()

    Operații:
      - add_connection(address)
      - add_note(address, note)
      - get_notes(address) -> string cu toate notițele, separate prin '\n'
      - clear_notes(address) -> (pentru studenți) șterge notițele
      - remove_connection(address)
    """

    def __init__(self):
        self.connections = {}

    def add_connection(self, address):
        """
        Înregistrează clientul în dicționar dacă nu există deja.
        """
        self.connections.setdefault(address, [])

    def add_note(self, address, note: str):
        """
        Adaugă o notiță pentru clientul identificat de 'address'.
        Presupune că address există deja în connections.
        """
        self.connections[address].append(note)

    def get_notes(self, address) -> str:
        """
        Întoarce toate notițele unui client, concatenate cu '\n'.
        Dacă nu există notițe, întoarce șir gol.
        """
        return "\n".join(self.connections[address])

    def clear_notes(self, address):
        """
        Șterge toate notițele clientului (de implementat de student în template,
        aici e implementarea de exemplu).
        """
        self.connections[address] = []

    def remove_connection(self, address):
        """
        Elimină complet clientul din dicționar.
        """
        del self.connections[address]
