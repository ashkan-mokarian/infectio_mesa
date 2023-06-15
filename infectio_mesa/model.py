import mesa

from enum import Enum


class CellAgent(mesa.Agent):
    """
    A Cell agent
    """

    # Cell states
    class CellState(Enum):
        HEALTHY = 1
        INFECTED = 2
        DEAD = 3

    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        super().__init__(unique_id, model)

        # Cell state
        self.cell_state = CellAgent.CellState.HEALTHY



    def step(self):
        """
        Modify this method to change what an individual agent will do during each step.
        Can include logic based on neighbors states.
        """
        pass


class BasicModel(mesa.Model):
    """
    Basic infectio model class. Handles agent (cell) creation, place them
    randomly, infects one center cell, and scheduling.
    """

    def __init__(self, num_agents, width, height):
        super().__init__()
        self.num_agents = num_agents
        self.schedule = mesa.time.RandomActivation(self)
        self.space = mesa.space.ContinuousSpace(x_max=width, y_max=height,
            torus=False)

        for i in range(self.num_agents):
            agent = CellAgent(i, self)
            self.schedule.add(agent)

            x = self.random.uniform(0, self.space.x_max)
            y = self.random.uniform(0, self.space.y_max)
            self.space.place_agent(agent, (x, y))

        # example data collector
        self.datacollector = mesa.datacollection.DataCollector()

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
        self.datacollector.collect(self)
        self.schedule.step()
