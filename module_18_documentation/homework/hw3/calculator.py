from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/jsonrpc')


@jsonrpc.method('calculate')
def calculate(operation: str, a: float, b: float) -> float:
    """Perform calculation on two numbers.

    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide'
        a: First number
        b: Second number

    Returns:
        Result of the operation

    Raises:
        ValueError: For invalid operations or division by zero
    """
    if operation == 'add':
        return a + b
    elif operation == 'subtract':
        return a - b
    elif operation == 'multiply':
        return a * b
    elif operation == 'divide':
        if b == 0:
            raise ValueError('Division by zero')
        return a / b
    else:
        raise ValueError('Invalid operation')


if __name__ == '__main__':
    app.run()