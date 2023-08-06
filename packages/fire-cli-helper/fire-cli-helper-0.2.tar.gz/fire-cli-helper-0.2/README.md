# fire-commands
Easy to use helper library for creating google fire based CLIs <br>
https://github.com/google/python-fire <br>

See example application firehelper_example for usage. <br>

# CLI entry point
In the CLI entry point, import relevant CLI commands, and use start_fire_cli initialise the fire app. <br>

```python
import firehelper
from .commands import *  #noqa

def main():
    firehelper.start_fire_cli('firehelper_example')

if __name__ == '__main__':
    main()
```

# Commands

Import each command in the main app to ensure code to register the command is run.<br>

To register commands:
```python
print_commands = {
    'print': lambda mytext: print(mytext) 
}

firehelper.CommandRegistry.register(print_commands)
```
To register commands with subcommands:
```python
maths_commands = {
    'maths': {
        'double': double,
        'square': square
    }
}

firehelper.CommandRegistry.register(maths_commands)
```
You can import all commands within a module as follows:
```python
# commands.__init__.py
"""Ensure all commands to be registered are referenced here."""

__all__ = ['maths', 'print']
```
```python
# __main__.py
from commands import *  # noqa
```