#!/usr/bin/env python3
"""Local JSON-RPC 2.0 teaching server: evaluate(expr) and add(a, b).

Transport convention: HTTP 200 for JSON-RPC responses, HTTP 204 for notifications.
No arbitrary Python evaluation. This is a bounded classroom example, not a public service.
Specification: https://www.jsonrpc.org/specification
"""
import argparse
import ast
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import operator

OPERATORS = {ast.Add: operator.add, ast.Sub: operator.sub,
             ast.Mult: operator.mul, ast.Div: operator.truediv,
             ast.UAdd: operator.pos, ast.USub: operator.neg}


def safe_eval(expression):
    if not isinstance(expression, str) or len(expression) > 512:
        raise ValueError("expr must be a string of at most 512 characters")
    tree = ast.parse(expression, mode="eval")
    if sum(1 for _ in ast.walk(tree)) > 64:
        raise ValueError("Expression is too complex")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            result = node.value
        elif isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            result = OPERATORS[type(node.op)](visit(node.left), visit(node.right))
        elif isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            result = OPERATORS[type(node.op)](visit(node.operand))
        else:
            raise ValueError("Only numbers, parentheses and + - * / are supported")
        if not math.isfinite(result) or abs(result) > 1e100:
            raise ValueError("Result exceeds the example's numeric limit")
        return result
    return visit(tree)


def error_response(code, message, request_id=None):
    return {"jsonrpc": "2.0", "id": request_id,
            "error": {"code": code, "message": message}}


def dispatch(request):
    """Return one response or None for a valid notification (including errors)."""
    if (not isinstance(request, dict) or request.get("jsonrpc") != "2.0"
            or not isinstance(request.get("method"), str)
            or ("id" in request and type(request["id"]) not in (str, int, float, type(None)))
            or (isinstance(request.get("id"), float) and not math.isfinite(request["id"]))
            or ("params" in request and not isinstance(request["params"], (list, dict)))):
        return error_response(-32600, "Invalid Request")
    request_id = request.get("id")
    method = request["method"]
    params = request.get("params", [])
    if method not in {"evaluate", "add"}:
        response = error_response(-32601, "Method not found", request_id)
    else:
        try:
            if method == "evaluate":
                if isinstance(params, dict) and set(params) == {"expr"}:
                    expression = params["expr"]
                elif isinstance(params, list) and len(params) == 1:
                    expression = params[0]
                else:
                    raise ValueError("evaluate expects [expr] or {expr: ...}")
                result = safe_eval(expression)
            else:
                values = [params["a"], params["b"]] if isinstance(params, dict) and set(params) == {"a", "b"} else params
                if not isinstance(values, list) or len(values) != 2 or any(type(x) not in (int, float) for x in values):
                    raise ValueError("add expects two numbers")
                result = values[0] + values[1]
                if not math.isfinite(result) or abs(result) > 1e100:
                    raise ValueError("Result exceeds the numeric limit")
            response = {"jsonrpc": "2.0", "id": request_id, "result": result}
        except (ValueError, TypeError, SyntaxError, ZeroDivisionError, OverflowError):
            response = error_response(-32602, "Invalid params", request_id)
    return response if "id" in request else None


def process_body(body):
    try:
        request = json.loads(body, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (ValueError, UnicodeError, RecursionError):
        return error_response(-32700, "Parse error")
    if isinstance(request, list):
        if not request:
            return error_response(-32600, "Invalid Request")
        if len(request) > 100:
            return error_response(-32600, "Batch exceeds 100 requests")
        results = [response for item in request if (response := dispatch(item)) is not None]
        return results or None
    return dispatch(request)


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.connection.settimeout(5)
        try:
            length = int(self.headers.get("Content-Length", "-1"))
            if not 0 <= length <= 65536 or self.headers.get("Transfer-Encoding"):
                self.send_error(400, "A bounded Content-Length is required")
                return
            body = self.rfile.read(length)
            if len(body) != length:
                self.send_error(400, "Incomplete request body")
                return
            response = process_body(body)
            data = b"" if response is None else json.dumps(response, allow_nan=False).encode("utf-8")
            self.send_response(204 if response is None else 200)
            if response is not None:
                self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except (OSError, ValueError):
            self.close_connection = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    with ThreadingHTTPServer((args.host, args.port), Handler) as server:
        print(f"JSON-RPC endpoint: http://{args.host}:{args.port}/")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
