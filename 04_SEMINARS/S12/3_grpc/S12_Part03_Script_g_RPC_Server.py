
import time
from concurrent import futures

import grpc

import S12_Part02_Config_Calculator_pb2 as calculator_pb2
import S12_Part02_Config_Calculator_pb2_grpc as calculator_pb2_grpc


# Port on which the gRPC server listens
GRPC_PORT = 50051


class CalculatorService(calculator_pb2_grpc.CalculatorServicer):
    """
    Implementation of the service defined in S12_Part02_Config_Calculator.proto.

    service Calculator {
      rpc Add (AddRequest) returns (AddResponse);
      rpc Multiply (MultiplyRequest) returns (MultiplyResponse);
      rpc Power (PowerRequest) returns (PowerResponse);
    }
    """

    def Add(self, request, context):
        """
        Implementation of the Add method.

        request: AddRequest (contains fields a and b)
        context: object containing call metadata (not used here)

        Returns: AddResponse(result = a + b)
        """
        a = request.a
        b = request.b
        result = a + b

        print(f"[SERVER] Add called with a={a}, b={b}, result={result}")

        return calculator_pb2.AddResponse(result=result)

    def Multiply(self, request, context):
        """
        Implementation of the Multiply method.

        TODO (student):
        - extract a and b from the request
        - compute the product
        - print a message to the console
        - return MultiplyResponse with result = a * b
        """
        a = request.a
        b = request.b
        result = a * b

        print(f"[SERVER] Multiply called with a={a}, b={b}, result={result}")

        return calculator_pb2.MultiplyResponse(result=result)

    def Power(self, request, context):
        """
        Implementation of the Power method.

        TODO (student):
        - extract base and exponent
        - compute base ** exponent
        - print a message to the console
        - return PowerResponse with result = base ** exponent
        """
        base = request.base
        exponent = request.exponent
        result = base ** exponent

        print(f"[SERVER] Power called with base={base}, exponent={exponent}, result={result}")

        return calculator_pb2.PowerResponse(result=result)


def serve():
    """
    Function that starts the gRPC server.

    - create a server with a thread pool
    - register the CalculatorService service
    - listen on port 50051
    - run indefinitely (until Ctrl+C)
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
        # keep the server alive
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("\n[SERVER] Stopping server...")
        server.stop(0)


if __name__ == "__main__":
    serve()
