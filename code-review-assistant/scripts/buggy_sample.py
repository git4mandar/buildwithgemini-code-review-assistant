"""Sample module demonstrating clean code practices, security hardening, and type safety."""

import ast
import operator


def add_to_x(base_value: int, num: int) -> int:
    """Adds a numeric value to a base integer without mutating global state.

    Args:
        base_value (int): The starting integer value.
        num (int): The integer value to add.

    Returns:
        int: The sum of base_value and num.
    """
    return base_value + num


def append_to_list(val: int, my_list: list[int] | None = None) -> list[int]:
    """Appends an integer to a list using an immutable default parameter.

    Args:
        val (int): The integer value to append.
        my_list (list[int] | None, optional): The target list. Defaults to None.

    Returns:
        list[int]: The list containing the appended value.
    """
    if my_list is None:
        my_list = []
    my_list.append(val)
    return my_list


def calculate_expression(expr: str) -> int | float:
    """Safely evaluates basic arithmetic expressions using AST parsing.

    Args:
        expr (str): The expression string to evaluate safely.

    Returns:
        int | float: The evaluated numeric result.

    Raises:
        ValueError: If the expression is unsafe or invalid.
    """
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def _eval(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        elif isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = _eval(node.left)
            right = _eval(node.right)
            return allowed_operators[type(node.op)](left, right)
        raise ValueError("Unsupported or unsafe expression component.")

    try:
        parsed_ast = ast.parse(expr, mode="eval")
        return _eval(parsed_ast)
    except (SyntaxError, ValueError) as err:
        raise ValueError(f"Invalid or unsafe expression: '{expr}'") from err


def divide_numbers(a: float, b: float) -> float:
    """Divides two numbers with explicit exception handling.

    Args:
        a (float): The numerator.
        b (float): The denominator.

    Returns:
        float: The quotient of a / b.

    Raises:
        ValueError: If denominator b is zero.
    """
    try:
        return a / b
    except ZeroDivisionError as err:
        raise ValueError("Division by zero is not permitted.") from err


def greet_user(name: str = "world") -> str:
    """Returns a greeting message.

    Args:
        name (str, optional): Name of the user to greet. Defaults to "world".

    Returns:
        str: Formatted greeting string.
    """
    greeting = f"Hello, {name}!"
    print(greeting)
    return greeting


if __name__ == "__main__":
    print(f"Added value: {add_to_x(10, 5)}")
    print(f"First list: {append_to_list(1)}")
    print(f"Second list: {append_to_list(2)}")
    print(f"Calculated: {calculate_expression('10 + 5')}")
    print(f"Division result: {divide_numbers(10, 2)}")
    try:
        divide_numbers(10, 0)
    except ValueError as e:
        print(f"Caught expected error: {e}")