
import grpc

import S12_Part02_Config_Calculator_pb2 as calculator_pb2
import S12_Part02_Config_Calculator_pb2_grpc as calculator_pb2_grpc


GRPC_TARGET = "localhost:50051"
LOG_FILE = "grpc_client_log.txt"


def call_add(stub, a, b):
    """
    Call the Add(a, b) method on the server and return the result.
    """
    request = calculator_pb2.AddRequest(a=a, b=b)
    response = stub.Add(request)
    return response.result


def call_multiply(stub, a, b):
    """
    Call the Multiply(a, b) method.

    TODO (student):
    - create a MultiplyRequest
    - call stub.Multiply(...)
    - return response.result
    """
    request = calculator_pb2.MultiplyRequest(a=a, b=b)
    response = stub.Multiply(request)
    return response.result


def call_power(stub, base, exponent):
    """
    Call the Power(base, exponent) method.

    TODO (student):
    - create a PowerRequest
    - call stub.Power(...)
    - return response.result
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

            # Example 1: Add call with fixed values
            result_add = call_add(stub, 2, 3)
            print(f"Add(2, 3) = {result_add}")
            log.write(f"Add(2, 3) = {result_add}\n")

            # TODO (student):
            # 1. Read values for a and b from the keyboard
            #    for Add and Multiply calls
            # 2. Read values for base and exponent for Power
            # 3. Call the helper functions and print/log the results

            # Guided example:

            # Read input for Add
            a_str = input("Enter a for Add: ")
            b_str = input("Enter b for Add: ")
            a = int(a_str)
            b = int(b_str)

            result_add2 = call_add(stub, a, b)
            print(f"Add({a}, {b}) = {result_add2}")
            log.write(f"Add({a}, {b}) = {result_add2}\n")

            # Read input for Multiply
            a_str = input("Enter a for Multiply: ")
            b_str = input("Enter b for Multiply: ")
            a = int(a_str)
            b = int(b_str)

            result_mul = call_multiply(stub, a, b)
            print(f"Multiply({a}, {b}) = {result_mul}")
            log.write(f"Multiply({a}, {b}) = {result_mul}\n")

            # Read input for Power
            base_str = input("Enter base for Power: ")
            exponent_str = input("Enter exponent for Power: ")
            base = int(base_str)
            exponent = int(exponent_str)

            result_pow = call_power(stub, base, exponent)
            print(f"Power({base}, {exponent}) = {result_pow}")
            log.write(f"Power({base}, {exponent}) = {result_pow}\n")

    print("[CLIENT] Finished. Results logged to", LOG_FILE)


if __name__ == "__main__":
    main()
