
import time
from concurrent import futures

import grpc

import calculator_pb2
import calculator_pb2_grpc


# Portul pe care va asculta serverul gRPC
GRPC_PORT = 50051


class CalculatorService(calculator_pb2_grpc.CalculatorServicer):
    """
    Implementarea serviciului definit in calculator.proto.

    service Calculator {
      rpc Add (AddRequest) returns (AddResponse);
      rpc Multiply (MultiplyRequest) returns (MultiplyResponse);
      rpc Power (PowerRequest) returns (PowerResponse);
    }
    """

    def Add(self, request, context):
        """
        Implementarea metodei Add.

        request: AddRequest (contine campurile a, b)
        context: obiect care contine metadate despre apel (nu il folosim aici)

        Returneaza: AddResponse(result = a + b)
        """
        a = request.a
        b = request.b
        result = a + b

        print(f"[SERVER] Add called with a={a}, b={b}, result={result}")

        return calculator_pb2.AddResponse(result=result)

    def Multiply(self, request, context):
        """
        Implementarea metodei Multiply.

        TODO (student):
        - extrageti a si b din request
        - calculati produsul
        - afisati un mesaj in consola
        - returnati MultiplyResponse cu result = a * b
        """
        a = request.a
        b = request.b
        result = a * b

        print(f"[SERVER] Multiply called with a={a}, b={b}, result={result}")

        return calculator_pb2.MultiplyResponse(result=result)

    def Power(self, request, context):
        """
        Implementarea metodei Power.

        TODO (student):
        - extrageti base si exponent
        - calculati base ** exponent
        - afisati un mesaj in consola
        - returnati PowerResponse cu result = base ** exponent
        """
        base = request.base
        exponent = request.exponent
        result = base ** exponent

        print(f"[SERVER] Power called with base={base}, exponent={exponent}, result={result}")

        return calculator_pb2.PowerResponse(result=result)


def serve():
    """
    Functie care porneste serverul gRPC.

    - creeaza un server cu un pool de thread-uri
    - inregistreaza serviciul CalculatorService
    - asculta pe portul 50051
    - ruleaza la nesfarsit (pana la Ctrl+C)
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        CalculatorService(),
        server
    )

    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    server.start()
    print(f"[SERVER] gRPC Calculator server started on port {GRPC_PORT}")

    try:
        # mentinem serverul in viata
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("\n[SERVER] Stopping server...")
        server.stop(0)


if __name__ == "__main__":
    serve()
