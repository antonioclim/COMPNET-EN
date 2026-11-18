"""Native loopback and boundary regressions for the supplied seminar implementations.

These tests do not accept a VM, Docker stack, browser or Mininet topology.
Run from the repository root with: python3 -m pytest -q 04_SEMINARS/tests
"""
import contextlib
import importlib.util
import json
from pathlib import Path
import socket
import sys
import threading
from urllib.request import Request, urlopen

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(relative, name):
    path = ROOT / relative
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@contextlib.contextmanager
def connected(handler):
    """Use an actual IPv4 connection and run the real handler in a thread."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('127.0.0.1', 0))
    listener.listen(1)
    client = socket.create_connection(listener.getsockname(), timeout=2)
    peer, _ = listener.accept()
    listener.close()
    errors = []
    def serve():
        try:
            handler(peer)
        except Exception as exc:
            errors.append(exc)
        finally:
            peer.close()
    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    try:
        yield client
    finally:
        client.close()
        thread.join(3)
        assert not thread.is_alive(), 'Handler did not stop after peer closure'
        assert not errors, repr(errors)


@pytest.mark.parametrize('size', [0, 7, 8, 9, 10, 96, 97, 98, 99, 100, 999])
def test_text_frame_total_byte_length(size):
    framing = load('S04/1_text-proto_tcp/text_framing.py', 'text_framing')
    frame = framing.encode_frame('\u0103' + 'x' * size)
    assert int(frame.split(b' ', 1)[0]) == len(frame)


def test_text_fragmentation_coalescence_and_incomplete_eof():
    module = load('S04/1_text-proto_tcp/S04_Part01A_Example_Text_Proto_TCP_Server.py', 'text_server')
    framing = sys.modules['text_framing']
    with connected(module.handle_client) as client:
        frame = framing.encode_frame('add key \u0103lice')
        for byte in frame:
            client.sendall(bytes([byte]))
        assert framing.read_frame(client).split(b' ', 1)[1] == b'key added'
        client.sendall(framing.encode_frame('get key') + framing.encode_frame('remove key'))
        assert framing.read_frame(client).split(b' ', 1)[1].decode() == '\u0103lice'
        assert framing.read_frame(client).split(b' ', 1)[1] == b'key removed'
        client.sendall(b'20 incomplete')
        client.shutdown(socket.SHUT_WR)
        assert client.recv(1) == b''


def test_binary_coalescence_and_keys_argument():
    client_module = load('S04/2_binary-proto_tcp/S04_Part02B_Example_Binary_Proto_TCP_Client.py', 'binary_client')
    server = load('S04/2_binary-proto_tcp/S04_Part02A_Example_Binary_Proto_TCP_Server.py', 'binary_server')
    import pickle
    framing = sys.modules['binary_framing']
    assert client_module.get_command('keys')[0] >= 2
    with pytest.raises(ValueError):
        client_module.get_command('add huge ' + 'x' * 1000)
    with connected(server.handle_client) as client:
        client.sendall(client_module.get_command('add k value') + client_module.get_command('get k'))
        assert pickle.loads(framing.read_frame(client)[1:]).payload == 'k added'
        assert pickle.loads(framing.read_frame(client)[1:]).payload == 'value'


def test_s02_repeated_lines_and_split_utf8():
    module = load('S02/S02_Part01_Example_TCP_Server.py', 's02_server')
    with module.ThreadedTCPServer(('127.0.0.1', 0), module.TCPRequestHandler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with socket.create_connection(server.server_address, timeout=2) as client:
                with client.makefile('rb') as reader:
                    for message in ['hello', 'two', 'three', 'four', '\u0103lice']:
                        for byte in (message + '\n').encode():
                            client.sendall(bytes([byte]))
                        assert reader.readline() == (message.upper() + '\n').encode()
        finally:
            server.shutdown()
            thread.join(2)


def test_s03_reset_removes_registered_client():
    module = load('S03/S03_Part01_Example_TCP_Multi_client_Server.py', 's03_server')
    import struct
    with connected(lambda peer: (module.clients.append(peer), module.handle_client(peer, ('127.0.0.1', 1)))) as client:
        client.sendall(b'hello')
        assert client.recv(5) == b'Hello'
        client.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
    assert module.clients == []


def test_udp_serialisation_larger_than_old_buffer_and_limit():
    module = load('S04/3_proto_udp/S04_Part03_Script_Serialization.py', 'udp_serialisation')
    payload = '\u0103' * 1000
    encoded = module.serialize(payload)
    assert len(encoded) > 1024
    assert module.deserialize(encoded) == payload
    with pytest.raises(ValueError):
        module.serialize('x' * 65508)


def test_http_fragmented_headers_paths_and_byte_length(tmp_path):
    module = load('S08/3_socket-http/S08_Part03B_Example_Socket_HTTP_Server.py', 'http_manual')
    static = tmp_path / 'static'
    static.mkdir()
    (static / 'S08_Part03_Page_Index.html').write_text('\u0103lice', encoding='utf-8')
    secret = tmp_path / 'secret.txt'
    secret.write_text('not public')
    (static / 'escape.txt').symlink_to(secret)
    module.STATIC_DIR = str(static)
    for target, expected in [('/', 200), ('../secret.txt', 400), ('/../secret.txt', 403), ('/%2e%2e/secret.txt', 403), ('/escape.txt', 403), ('/missing', 404)]:
        with connected(module.handle_client) as client:
            for byte in f'GET {target} HTTP/1.1\r\nHost: localhost\r\n\r\n'.encode():
                client.sendall(bytes([byte]))
            response = bytearray()
            while chunk := client.recv(4096):
                response.extend(chunk)
            header, body = bytes(response).split(b'\r\n\r\n', 1)
            assert header.startswith(f'HTTP/1.1 {expected} '.encode())
            assert f'Content-Length: {len(body)}'.encode() in header
            assert b'not public' not in body


def test_pseudo_ftp_four_transfers_and_control_ack(tmp_path):
    server = load('S09/2_custom-pseudo-ftp/S09_Part02B_Script_Pseudo_FTP_Server.py', 'ftp_server')
    client_module = load('S09/2_custom-pseudo-ftp/S09_Part02C_Script_Pseudo_FTP_Client.py', 'ftp_client')
    server.FILE_ROOT = str(tmp_path / 'server')
    client_module.LOCAL_STORAGE = str(tmp_path / 'client')
    Path(server.FILE_ROOT).mkdir()
    Path(client_module.LOCAL_STORAGE).mkdir()
    (Path(server.FILE_ROOT) / 'a.txt').write_bytes('test \u0103'.encode())
    (Path(client_module.LOCAL_STORAGE) / 'b.txt').write_bytes(bytes(range(255)))
    with connected(server.handle_client_commands) as client:
        for command in ['active_get a.txt', 'passive_get a.txt', 'active_put b.txt', 'passive_put b.txt']:
            client_module.process_command(client, command)
        assert (Path(client_module.LOCAL_STORAGE) / 'a.txt').read_bytes() == 'test \u0103'.encode()
        assert (Path(server.FILE_ROOT) / 'b.txt').read_bytes() == bytes(range(255))
        client.sendall(b'list\n')
        assert 'b.txt' in sys.modules['pseudo_ftp_io'].read_reply(client)


def test_rpc_contract_over_http():
    module = load('S12/1_jsonrpc/S12_Part01_Script_JSONRPC_Server.py', 'rpc_server')
    with module.ThreadingHTTPServer(('127.0.0.1', 0), module.Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        cases = [
            (b'{', 200, -32700),
            (b'[]', 200, -32600),
            (b'{"jsonrpc":"2.0","method":"missing","id":7}', 200, -32601),
            (b'{"jsonrpc":"2.0","method":"evaluate","params":["__import__(1)"],"id":7}', 200, -32602),
            (b'{"jsonrpc":"2.0","method":"evaluate","params":["2+3"],"id":7}', 200, None),
            (b'{"jsonrpc":"2.0","method":"evaluate","params":["2+3"]}', 204, None),
        ]
        try:
            for body, status, code in cases:
                req = Request(f'http://127.0.0.1:{server.server_port}/', data=body, headers={'Content-Type':'application/json'})
                with urlopen(req, timeout=2) as response:
                    assert response.status == status
                    raw = response.read()
                if status == 204:
                    assert raw == b''
                else:
                    result = json.loads(raw)
                    if code:
                        assert result['error']['code'] == code
                        if code in {-32601, -32602}:
                            assert result['id'] == 7
                    else:
                        assert result == {'jsonrpc':'2.0','id':7,'result':5}
        finally:
            server.shutdown()
            thread.join(2)


def test_s13_port_exhaustion_and_env_comments(tmp_path):
    ports = load('S13/generate_env_ports.py', 'ports_generator')
    with socket.socket() as held:
        held.bind(('127.0.0.1', 0))
        with pytest.raises(ValueError, match='No free'):
            ports.pick_port(held.getsockname()[1], window=0)
    with pytest.raises(ValueError):
        ports.pick_port(65535, window=1)
    env = load('S13/s13_env.py', 's13_env')
    path = tmp_path / '.env'
    path.write_text('A_HOST_PORT=19102 # local\nB_HOST_PORT="19103" # local\nC_HOST_PORT=\'19104\'\n')
    assert env.load_env_file(path) == {'A_HOST_PORT':'19102','B_HOST_PORT':'19103','C_HOST_PORT':'19104'}
    path.write_text('A_HOST_PORT=not-a-port\n')
    with pytest.raises(ValueError):
        env.load_env_file(path)


def test_rpc_batch_notifications_and_nonfinite_ids():
    rpc = load('S12/1_jsonrpc/S12_Part01_Script_JSONRPC_Server.py', 'rpc_batch')
    batch = [
        {'jsonrpc': '2.0', 'method': 'add', 'params': [1, 2], 'id': 'item'},
        {'jsonrpc': '2.0', 'method': 'unknown'},
        17,
    ]
    result = rpc.process_body(json.dumps(batch).encode())
    assert result[0] == {'jsonrpc': '2.0', 'id': 'item', 'result': 3}
    assert len(result) == 2 and result[1]['error']['code'] == -32600
    assert result[1]['id'] is None
    assert rpc.process_body(b'[{"jsonrpc":"2.0","method":"add","params":[1,2]}]') is None
    assert rpc.process_body(b'[]')['error']['code'] == -32600
    assert rpc.process_body(b'{"jsonrpc":"2.0","method":"add","params":[1,2],"id":1e400}')['error']['code'] == -32600
    nested = rpc.process_body(b'[' * 2000 + b']' * 2000)
    # Decoders may accept this valid JSON nesting or report their nesting limit.
    if isinstance(nested, list):
        assert nested[0]['error']['code'] == -32600
    else:
        assert nested['error']['code'] == -32700
