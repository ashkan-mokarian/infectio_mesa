"""
Configure visualization elements and instantiate a server
"""

from .model import BasicModel
from .SimpleContiunousModule import SimpleCanvas
from .cell import CellState

import mesa

def circle_portrayal_example(agent):
    if agent is None:
        return
    
    color = "Blue" if agent.state is CellState.HEALTHY else (
        "Green" if agent.state is CellState.INFECTED else "Black")

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "r": 2,
        "Color": color,
    }
    return portrayal


canvas_element = SimpleCanvas(
    circle_portrayal_example, 500, 500
)
chart_element = mesa.visualization.ChartModule([
    {"Label": "infected", "Color": "Green"},
    {"Label": "dead", "Color": "Black"}
    ])

model_kwargs = {"num_agents": 2000, "width": 500, "height": 500}

# server = mesa.visualization.ModularServer(
#     BasicModel, [canvas_element], "Infectio (Mesa)", model_kwargs)

server = mesa.visualization.ModularServer(
    BasicModel,
    [canvas_element, chart_element],
    "Infectio_Mesa",
    model_kwargs,
)