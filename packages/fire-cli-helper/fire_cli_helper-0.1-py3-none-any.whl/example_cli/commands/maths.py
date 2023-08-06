from firehelper import CommandRegistry

def double(number):
    """Double a number.

    Args:
        number (num): [description]

    Returns:
        num: doubled number.
    """
    return number * 2

def square(number):
    """Square a number.

    Args:
        number (num): [description]

    Returns:
        num: squared number.
    """
    return number * number

maths_commands = {
    'maths': {
        'double': double,
        'square': square
    }
}

CommandRegistry.register(maths_commands)
