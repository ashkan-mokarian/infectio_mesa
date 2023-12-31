import mesa
import numpy as np

from .cell import CellAgent, CellState
from .diffusion import Homogenous2dDiffusion

# Heat Diffusion Constants
# all the coefficient used for homogenous diffusion in one.
# \gamma = alpha * delta_t / delta_x ** 2 where alpha is the diffusion constant
GAMMA = 0.2
virions_diffusion_time_steps_per_each_model_step = 30


def count_infected(model):
    reporter = {"infected": 0}
    for c in model.schedule.agents:
        if c.state == CellState.INFECTED:
            reporter["infected"] += 1
    return reporter

class BasicModel(mesa.Model):
    """
    Basic infectio model class. Handles agent (cell) creation, place them
    randomly, infects one center cell, and scheduling.
    """

    def __init__(self, num_agents, width, height):
        super().__init__()
        self.num_agents = num_agents
        
        # By having time_infected property for each cell, we don't need to have
        # Multiple schedulers for each state. time_infected also becomes handy
        # For other computations
        # self.schedule = {state: mesa.time.SimultaneousActivation(self)
        #                  for state in CellState}
        self.schedule = mesa.time.SimultaneousActivation(self)

        self.space = mesa.space.ContinuousSpace(x_max=width, y_max=height,
            torus=True)  # TODO: remove torus, also need to change cell.move()
        
        # Virions in space, used for molecular diffusion
        self.virions = Homogenous2dDiffusion(GAMMA, width, height, virions_diffusion_time_steps_per_each_model_step)
        

        for i in range(self.num_agents - 1):
            x = self.random.uniform(0, self.space.x_max)
            y = self.random.uniform(0, self.space.y_max)
            agent = CellAgent(i, self)
            self.schedule.add(agent)
            self.space.place_agent(agent, (x, y))
        
        # put an infected cell in the middle
        agent = CellAgent(i+1, self)
        agent.infect_cell()
        self.space.place_agent(agent, (width/2, height/2))
        self.schedule.add(agent)


        # example data collector
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "infected": lambda m: len([c for c in m.schedule.agents if c.state is CellState.INFECTED])})

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
        self.datacollector.collect(self)
        self.virions.step() # Virion diffusion step
        # print('min', self.virions.u.min(), 'max', self.virions.u.max())
        self.schedule.step()
