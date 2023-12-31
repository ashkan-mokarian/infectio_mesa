import numpy as np
from enum import Enum

import mesa

# Cell states
class CellState(Enum):
    SUSCEPTIBLE = 1
    INFECTED = 2
    REMOVED = 3

def cell_speed(cell_state: CellState):
    return {
        CellState.SUSCEPTIBLE: 1,
        CellState.INFECTED: 5,
        CellState.REMOVED: 0
    }[cell_state]

# Search radius for deciding cell-cell infection rate based on number of
# infected cells in the radius
CELL2CELL_INFECTION_RADIUS_SEARCH = 5

# For now, let's choose a simple sigmoid function for deciding cell-cell infection chance
def cell2cell_infection_chance(num_infected_neighbors):
    if num_infected_neighbors == 0:
        return 0.0
    return 1 / (1 + np.exp(-0.5 * (num_infected_neighbors - 5)))

class CellAgent(mesa.Agent):
    """
    A Cell agent
    """

    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        super().__init__(unique_id, model)

        # Cell state
        self.state = CellState.SUSCEPTIBLE
        self.time_infected = None
    
    @property
    def speed(self):
        return cell_speed(self.state)

    def move(self):
        """Random walk of cell based on speed."""
        dx, dy = self.random.random()-0.5, self.random.random()-0.5
        velocity = np.array([dx, dy])
        velocity /= np.linalg.norm(velocity)
        new_pos = self.pos + velocity * self.speed
        self.model.space.move_agent(self, new_pos)
    
    def infect_cell(self):
        assert self.state is CellState.SUSCEPTIBLE, "Only healthy cells can get infected."
        self.state = CellState.INFECTED
        self.time_infected = 0

    def decide_to_infect(self):
        """Randomly infect healthy cells based on proximity to other infected cells."""
        if self.state is not CellState.SUSCEPTIBLE:
            return
        # Simple cell-cell infection only based on numbers
        infected_neighbors = [c for c in self.model.space.get_neighbors(
            self.pos, radius=CELL2CELL_INFECTION_RADIUS_SEARCH, include_center=False)
            if c.time_infected]  # c.time_infected checks for both, if cell is
                                 # infected, and also, if it wasn't decided to
                                 # get infected in the current step
        # TODO: what distribution to use and what parameters. For now, sigmoid
        # with linear exponentiation
        infection_prob = cell2cell_infection_chance(len(infected_neighbors))
        if infection_prob > self.random.random():
            self.infect_cell()
    
    def add_virions_via_lysis(self):
        # x, y = self.pos
        # print(int(x), int(y), self.model.virions.u.shape)
        # self.model.virions.u[int(x), int(y)] += 20
        pass

    def kill_cell(self):
        # assert self.state is CellState.INFECTED, "Only infected cells can die."
        # self.state = CellState.DEAD
        # self.time_infected = None
        pass

        # Cell lysis and changing model's virions at the position with a step function
        # self.add_virions_via_lysis()
    
    def decide_to_kill(self):
        # if self.state is not CellState.INFECTED:
        #     return
        # if self.time_infected > 50:
        #     self.kill_cell()
        pass

    def step(self):
        """
        Modify this method to change what an individual agent will do during each step.
        Can include logic based on neighbors states.
        """
        self.decide_to_infect()
        # self.decide_to_kill()
    
    def advance(self) -> None:
        self.move()
        if self.state is CellState.INFECTED:
            self.time_infected += 1
            x, y = self.pos
            self.model.virions.u[int(x), int(y)] += 1

