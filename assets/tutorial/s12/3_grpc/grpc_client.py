
import grpc

import calculator_pb2
import calculator_pb2_grpc


GRPC_TARGET = "localhost:50051"
LOG_FILE = "grpc_client_log.txt"


def call_add(stub, a, b):
    """
    Apeleaza metoda Add(a, b) de pe server si intoarce rezultatul.
    """
    request = calculator_pb2.AddRequest(a=a, b=b)
    response = stub.Add(request)
    return response.result


def call_multiply(stub, a, b):
    """
    Apeleaza metoda Multiply(a, b).

    TODO (student):
    - creati un MultiplyRequest
    - apelati stub.Multiply(...)
    - intoarceti response.result
    """
    request = calculator_pb2.MultiplyRequest(a=a, b=b)
    response = stub.Multiply(request)
    return response.result


def call_power(stub, base, exponent):
    """
    Apeleaza metoda Power(base, exponent).

    TODO (student):
    - creati un PowerRequest
    - apelati stub.Power(...)
    - intoarceti response.result
    """
    request = calculator_pb2.PowerRequest(base=base, exponent=exponent)
    response = stub.Power(request)
    return response.result


def main():
    print("[CLIENT] Connecting to gRPC server at", GRPC_TARGET)

    with grpc.insecure_channel(GRPC_TARGET) as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)

        print("[CLIENT] Connected. You can now call Add, Multiply and Power.")

        with open(LOG_FILE, "w") as log:
            log.write("gRPC client log\n")
            log.write("================\n")

            # Exemplu 1: apel Add cu valori fixe
            result_add = call_add(stub, 2, 3)
            print(f"Add(2, 3) = {result_add}")
            log.write(f"Add(2, 3) = {result_add}\n")

            # TODO (student):
            # 1. Cititi de la tastatura valori pentru a si b
            #    pentru apeluri Add si Multiply
            # 2. Cititi valori pentru base si exponent pentru Power
            # 3. Apelati functiile helper si afisati/logati rezultatele

            # Exemplu ghidat:

            # Citim input pentru Add
            a_str = input("Introduceti a pentru Add: ")
            b_str = input("Introduceti b pentru Add: ")
            a = int(a_str)
            b = int(b_str)

            result_add2 = call_add(stub, a, b)
            print(f"Add({a}, {b}) = {result_add2}")
            log.write(f"Add({a}, {b}) = {result_add2}\n")

            # Citim input pentru Multiply
            a_str = input("Introduceti a pentru Multiply: ")
            b_str = input("Introduceti b pentru Multiply: ")
            a = int(a_str)
            b = int(b_str)

            result_mul = call_multiply(stub, a, b)
            print(f"Multiply({a}, {b}) = {result_mul}")
            log.write(f"Multiply({a}, {b}) = {result_mul}\n")

            # Citim input pentru Power
            base_str = input("Introduceti base pentru Power: ")
            exponent_str = input("Introduceti exponent pentru Power: ")
            base = int(base_str)
            exponent = int(exponent_str)

            result_pow = call_power(stub, base, exponent)
            print(f"Power({base}, {exponent}) = {result_pow}")
            log.write(f"Power({base}, {exponent}) = {result_pow}\n")

    print("[CLIENT] Finished. Results logged to", LOG_FILE)


if __name__ == "__main__":
    main()
