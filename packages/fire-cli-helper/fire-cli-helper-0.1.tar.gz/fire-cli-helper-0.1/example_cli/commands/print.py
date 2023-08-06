from firehelper import CommandRegistry

def prt(printme: str):
    """print printme

    Args:
        printme (str): [description]
    """
    print(printme)

print_commands = {
    'print': prt
}

CommandRegistry.register(print_commands)
