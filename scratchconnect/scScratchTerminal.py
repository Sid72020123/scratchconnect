"""
The Terminal File
"""

from scratchconnect.Exceptions import DependencyException


def _terminal(sc):
    try:
        import rich
        from scScratchTerminal import Terminal
        return Terminal(sc)
    except ModuleNotFoundError:
        DependencyException(
            "The dependencies required for the Terminal feature to work were not found. Please install them using the command: 'pip install scratchconnect[terminal]'")
