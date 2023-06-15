"""
Configure visualization elements and instantiate a server
"""

from .model import BasicModel
from .SimpleContiunousModule import SimpleCanvas

import mesa

def circle_portrayal_example(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
        "Color": "Blue",
    }
    return portrayal


canvas_element = SimpleCanvas(
    circle_portrayal_example, 500, 500
)
# chart_element = mesa.visualization.ChartModule([{"Label": "Infectio_Mesa", "Color": "Pink"}])

model_kwargs = {"num_agents": 10, "width": 10, "height": 10}

server = mesa.visualization.ModularServer(
    BasicModel, [canvas_element], "Infectio (Mesa)", model_kwargs
)

# server = mesa.visualization.ModularServer(
#     BasicModel,
#     [canvas_element, chart_element],
#     "Infectio_Mesa",
#     model_kwargs,
# )
