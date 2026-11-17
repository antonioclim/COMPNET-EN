"""Bounded lecture regressions: native Python/loopback and explicit transport doubles.

Run from the repository root after installing tests/requirements.txt.
These tests do not establish Docker, Mininet, OVA or browser acceptance.
"""
from __future__ import annotations

import contextlib
import gzip
import http.client
import importlib.util
import io
import json
import socket
import struct
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from types import SimpleNamespace

import pytest

LECTURES = Path(__file__).resolve().parents[1]


def load(relative):
    path = LECTURES / relative
    spec = importlib.util.spec_from_file_location(path.stem.replace('-', '_'), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('path,args,expected', [
    ('scenario-cidr-basic/cidr-calc.py', ['0.0.0.0/0'], '4294967294'),
    ('scenario-cidr-basic/cidr-calc.py', ['192.0.2.0/31'], 'Usable hosts: 2'),
    ('scenario-cidr-basic/cidr-calc.py', ['192.0.2.1/32'], 'Usable hosts: 1'),
    ('scenario-subnetting-flsm/flsm-split.py', ['0.0.0.0/0', '1'], '(4294967294 usable)'),
    ('scenario-vlsm/vlsm-alloc.py', ['0.0.0.0/0', '4294967294'], '0.0.0.0/0'),
])
def test_address_calculators_do_not_materialise_hosts(path, args, expected):
    # Large networks used to allocate enormous host lists. Bound both time and memory.
    kwargs = {}
    if sys.platform.startswith('linux'):
        import resource
        def limit_memory():
            resource.setrlimit(resource.RLIMIT_AS, (128 * 1024**2, 128 * 1024**2))
        kwargs['preexec_fn'] = limit_memory
    result = subprocess.run([sys.executable, str(LECTURES / 'C05/assets' / path), *args],
                            capture_output=True, text=True, timeout=3, **kwargs)
    assert result.returncode == 0, result.stderr
    assert expected in result.stdout


@pytest.mark.parametrize('path,args', [
    ('scenario-cidr-basic/cidr-calc.py', ['2001:db8::/64']),
    ('scenario-subnetting-flsm/flsm-split.py', ['192.0.2.0/24', '0']),
    ('scenario-vlsm/vlsm-alloc.py', ['192.0.2.0/24', '-1']),
    ('scenario-vlsm/vlsm-alloc.py', ['192.0.2.0/24', '300']),
])
def test_address_calculator_errors_are_nonzero_without_traceback(path, args):
    result = subprocess.run([sys.executable, str(LECTURES / 'C05/assets' / path), *args],
                            capture_output=True, text=True, timeout=3)
    assert result.returncode == 2
    assert 'ERROR:' in result.stderr and 'Traceback' not in result.stderr


def tcp_pair():
    with socket.create_server(('127.0.0.1', 0)) as listener:
        client = socket.create_connection(listener.getsockname(), timeout=2)
        server, _ = listener.accept()
        server.settimeout(2)
    return client, server


def test_tunnel_preserves_half_close_and_delivers_final_reply():
    tunnel = load('C03/assets/scenario-tcp-tunnel/tunnel.py')
    client, relay_in = tcp_pair()
    relay_out, target = tcp_pair()
    stop = threading.Event()
    workers = [threading.Thread(target=tunnel.forward_stream, args=args, daemon=True)
               for args in ((relay_in, relay_out, 'out', stop), (relay_out, relay_in, 'back', stop))]
    try:
        for worker in workers:
            worker.start()
        client.sendall(b'request')
        client.shutdown(socket.SHUT_WR)
        assert target.recv(7) == b'request'
        assert target.recv(1) == b''
        assert not stop.is_set()  # EOF in one direction is not cancellation.
        target.sendall(b'final reply')
        target.shutdown(socket.SHUT_WR)
        assert client.recv(11) == b'final reply'
        assert client.recv(1) == b''
        for worker in workers:
            worker.join(2)
        assert not any(worker.is_alive() for worker in workers)
    finally:
        for channel in (client, relay_in, relay_out, target):
            with contextlib.suppress(OSError):
                channel.shutdown(socket.SHUT_RDWR)
            channel.close()
        for worker in workers:
            worker.join(2)


def test_tunnel_error_wakes_both_directions():
    tunnel = load('C03/assets/scenario-tcp-tunnel/tunnel.py')
    client, relay_in = tcp_pair()
    relay_out, target = tcp_pair()
    # Idle timeout in one direction must unblock the opposite receive.
    relay_in.settimeout(0.05)
    stop = threading.Event()
    workers = [threading.Thread(target=tunnel.forward_stream, args=args, daemon=True)
               for args in ((relay_in, relay_out, 'out', stop), (relay_out, relay_in, 'back', stop))]
    try:
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(1)
        assert stop.is_set()
        assert not any(worker.is_alive() for worker in workers)
    finally:
        for channel in (client, relay_in, relay_out, target):
            channel.close()


@pytest.mark.parametrize('accept,expected_status,compressed', [
    ('gzip', 200, True), ('gzip;q=0', 200, False), ('xgzip', 200, False),
    ('GZip;q=1, identity;q=0', 200, True), ('*;q=0', 406, False),
    ('gzip;q=0, identity;q=0', 406, False), ('gzip;q=0.1, identity;q=0.8', 200, False),
])
def test_content_encoding_negotiation_on_real_http(tmp_path, accept, expected_status, compressed):
    server = load('C09/assets/scenario-mime-encoding-gzip/server.py')
    payload = b'{"message":"a real loopback response"}'
    file = tmp_path / 'data.json'
    file.write_bytes(payload)
    server.FILES = {'/data.json': (str(file), 'application/json')}
    with HTTPServer(('127.0.0.1', 0), server.Handler) as httpd:
        worker = threading.Thread(target=httpd.serve_forever, daemon=True)
        worker.start()
        connection = http.client.HTTPConnection(*httpd.server_address, timeout=2)
        try:
            connection.request('GET', '/data.json', headers={'Accept-Encoding': accept})
            response = connection.getresponse()
            body = response.read()
            assert response.status == expected_status
            if expected_status == 200:
                assert (response.getheader('Content-Encoding') == 'gzip') is compressed
                assert response.getheader('Vary') == 'Accept-Encoding'
                assert (gzip.decompress(body) if compressed else body) == payload
        finally:
            connection.close()
            httpd.shutdown()
            worker.join(2)


def test_smoke_test_observes_redirect_before_following_it():
    smoke = load('C14/assets/scenario-week14-integration-lab/client/smoke_test.py')
    seen = []
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            seen.append(self.path)
            self.send_response(302 if self.path == '/' else 200)
            if self.path == '/':
                self.send_header('Location', '/app/')
            self.end_headers()
            self.wfile.write(b'test')
        def log_message(self, *_):
            pass
    with HTTPServer(('127.0.0.1', 0), Handler) as httpd:
        worker = threading.Thread(target=httpd.serve_forever, daemon=True)
        worker.start()
        try:
            base = 'http://127.0.0.1:' + str(httpd.server_port)
            code, headers, _ = smoke.http_get(base + '/')
            assert code == 302 and headers['Location'] == '/app/'
            assert seen == ['/']
            assert smoke.http_get(base + '/app/')[0] == 200
        finally:
            httpd.shutdown()
            worker.join(2)


@pytest.mark.parametrize('flags,rdata', [(0x0100, b'\x7f\0\0\1'), (0x8380, b'\x7f\0\0\1'),
                                         (0x8180, b'\x7f\0\0')])
def test_dns_parser_rejects_nonresponse_truncation_and_short_rdata(monkeypatch, flags, rdata):
    dns = load('C14/assets/scenario-week14-integration-lab/client/dns_query.py')
    monkeypatch.setattr(dns.random, 'randint', lambda *_: 42)
    packet = (struct.pack('!6H', 42, flags, 1, 1, 0, 0) +
              dns._encode_qname('example.test') + struct.pack('!HH', 1, 1) + b'\x00' +
              struct.pack('!HHIH', 1, 1, 30, 4) + rdata)
    class Socket:
        closed = False
        def settimeout(self, _): pass
        def sendto(self, *_): pass
        def recvfrom(self, _): return packet, ('127.0.0.1', 53)
        def close(self): self.closed = True
    peer = Socket()
    monkeypatch.setattr(dns.socket, 'socket', lambda *_: peer)
    with pytest.raises(ValueError):
        dns.query_a('127.0.0.1', 'example.test')
    assert peer.closed


def test_ssh_drains_streams_concurrently_and_propagates_exit_status():
    provision = load('C11/assets/scenario-ssh-provision/controller/provision.py')
    def command(status):
        barrier = threading.Barrier(2)
        class Stream:
            channel = SimpleNamespace(recv_exit_status=lambda: status)
            def __init__(self, data): self.data = data
            def read(self):
                barrier.wait(timeout=2)
                return self.data
        stdin = io.BytesIO()
        return SimpleNamespace(exec_command=lambda _: (stdin, Stream(b'output'), Stream(b'failed detail')))
    assert provision.run_cmd(command(0), 'true') == ('output', 'failed detail')
    with pytest.raises(RuntimeError, match=r'exit 7.*'):
        provision.run_cmd(command(7), 'false')


def test_websocket_rejects_wrong_shapes_and_isolates_dead_recipient():
    module = load('C10/assets/scenario-websocket-protocol/server.py')
    class Peer:
        def __init__(self, incoming=(), broken=False):
            self.incoming = iter(incoming)
            self.sent = []
            self.broken = broken
        def receive(self): return next(self.incoming, None)
        def send(self, raw):
            if self.broken: raise RuntimeError('recipient disconnected')
            self.sent.append(json.loads(raw))
    broken = Peer(broken=True)
    healthy = Peer()
    module.clients[:] = [(broken, {'joined': True, 'room': 'r'}), (healthy, {'joined': True, 'room': 'r'})]
    sender = Peer(map(json.dumps, [[], {'type': 'join', 'room': [], 'name': 'n'},
                                  {'type': 'join', 'room': 'r', 'name': 'n'},
                                  {'type': 'msg', 'room': 'r', 'text': {}},
                                  {'type': 'msg', 'room': 'r', 'text': 'hello'}]))
    # Flask-Sock registers a wraps-decorated transport adapter; exercise its original handler.
    module.app.view_functions["ws_endpoint"].__wrapped__(sender)
    assert [x['type'] for x in sender.sent] == ['error', 'error', 'joined', 'error', 'deliver', 'ack']
    assert healthy.sent[0]['text'] == 'hello'
    assert module.clients == [(healthy, {'joined': True, 'room': 'r'})]


@pytest.mark.parametrize('mode,connack,ack,expected', [
    ('publish', 135, 0, 1), ('publish', 0, 135, 1), ('publish', 0, 0, 0),
    ('subscribe', 0, 135, 1),
])
def test_mqtt_cli_reports_broker_rejections(monkeypatch, mode, connack, ack, expected):
    cli = load('C13/assets/scenario-iot-basic/client/mqtt_cli.py')
    from paho.mqtt.reasoncodes import ReasonCode
    from paho.mqtt.packettypes import PacketTypes
    class Peer:
        stopped = disconnected = False
        def connect(self, *_args, **_kwargs): pass
        def loop_start(self):
            self.on_connect(self, None, None, ReasonCode(PacketTypes.CONNACK, identifier=connack), None)
        def publish(self, *_args, **_kwargs):
            self.on_publish(self, None, 1, ReasonCode(PacketTypes.PUBACK, identifier=ack), None)
            return SimpleNamespace(rc=0)
        def subscribe(self, *_args, **_kwargs):
            self.on_subscribe(self, None, 1, [ReasonCode(PacketTypes.SUBACK, identifier=ack)], None)
            return 0, 1
        def disconnect(self): self.disconnected = True
        def loop_stop(self): self.stopped = True
    peer = Peer()
    monkeypatch.setattr(cli.mqtt, 'Client', lambda **_: peer)
    monkeypatch.setattr(cli.signal, 'signal', lambda *_: None)
    monkeypatch.setattr(sys, 'argv', ['mqtt_cli.py', '--mode', mode, '--topic', 'test', '--qos', '1'])
    assert cli.main() == expected
    assert peer.stopped and peer.disconnected


def test_udp_loss_counts_missing_first_and_last_sequence_numbers(monkeypatch, capsys):
    receiver = load('C08/assets/scenario-udp-vs-tcp-loss/udp_receiver.py')
    bound = threading.Event()
    original_socket = socket.socket
    class ObservedSocket(socket.socket):
        def bind(self, address):
            super().bind(('127.0.0.1', 0))
            receiver.PORT = self.getsockname()[1]
            bound.set()
    monkeypatch.setattr(receiver.socket, 'socket', ObservedSocket)
    monkeypatch.setattr(sys, 'argv', ['udp_receiver.py', '--count', '5'])
    worker = threading.Thread(target=receiver.main, daemon=True)
    worker.start()
    assert bound.wait(2)
    with original_socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for number in (1, 2, 2, 3, 100):
            sender.sendto(f'MSG {number}'.encode(), ('127.0.0.1', receiver.PORT))
    worker.join(7)
    assert not worker.is_alive()
    captured = capsys.readouterr().out
    assert 'received 3/5' in captured and 'missing count: 2' in captured and '[0, 4]' in captured


@pytest.mark.parametrize('status,expected', [('done', None), ('failed', 'Job failed')])
def test_async_client_handles_terminal_states(monkeypatch, status, expected):
    cli = load('C10/assets/scenario-custom-http-semantics/client.py')
    calls = []
    class Response:
        status_code = 202
        headers = {'Location': '/jobs/1'}
        def raise_for_status(self): pass
        def json(self):
            return {'status': status, 'progress': 100, 'error': 'intentional failure',
                    'links': {'result': '/jobs/1/result'}, 'value': 120}
    def request(*args, **kwargs):
        assert kwargs['timeout'] == 5
        calls.append(args[0])
        return Response()
    monkeypatch.setattr(cli.requests, 'post', request)
    monkeypatch.setattr(cli.requests, 'get', request)
    if expected:
        with pytest.raises(SystemExit, match=expected):
            cli.main()
        assert len(calls) == 2
    else:
        cli.main()
        assert len(calls) == 3
