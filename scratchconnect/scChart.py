"""
The Charts File
"""

from scratchconnect.Exceptions import DependencyException


def _chart(sc):
    try:
        import pyhtmlchart  # Using pyhtmlchart as a temporary library... This may change in the future
        from scChart import Chart
        return Chart(sc)
    except ModuleNotFoundError:
        DependencyException(
            "The dependencies required for the Chart feature to work were not found. Please install them using the command: 'pip install scratchconnect[chart]'")
