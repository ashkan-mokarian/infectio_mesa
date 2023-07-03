import time
import numpy as np
import matplotlib.pyplot as plt
import os

from infectio_mesa.model import BasicModel
from infectio_mesa.cell import CellState

MAX_SIM_ITER = 500

if __name__ == '__main__':
    file_name = "output/plots/plot_{}.png"
    # os.makedirs(file_name.format(0), exist_ok=True)
    start_time = time.perf_counter()
    model = BasicModel(2000, 500, 500)

    fig = plt.figure(figsize=(14, 8))
    grid = plt.GridSpec(4, 7, wspace=0.01, hspace=0.01)
    ax_pos = fig.add_subplot(grid[:-1, :3])
    ax_dif = fig.add_subplot(grid[:-1, 3:])
    ax_colorbar = fig.add_subplot(grid[:-1, -1], frameon=False)
    ax_lin = fig.add_subplot(grid[-1, :])

    ax_pos.set_aspect('auto')  # Set aspect ratio to 'auto' for ax_pos subplot
    ax_dif.set_aspect('auto') 

    state_lists = {k: [] for k in CellState}
    style = {
        CellState.SUSCEPTIBLE: 'ob',
        CellState.INFECTED: 'og',
        CellState.REMOVED: 'ok'
    }

    # Line plots
    steps = []
    num_lists = {k: [] for k in CellState if k is not CellState.REMOVED}

    colorbar = None
    for t in range(MAX_SIM_ITER):
        print(f'step {t}/{MAX_SIM_ITER} Starting ...')
        # Initialize three lists for each cell state
        state_lists = {k: [] for k in CellState}
        _ = [state_lists[a.state].append(a) for a in model.schedule.agents]

        # visualize using plot and not scatter
        ax_pos.cla()
        for state in CellState:
            pos = [a.pos for a in state_lists[state]]
            if pos:
                x, y = zip(*pos)
                ax_pos.plot(x, y, style[state], markersize=4)
                
        # Line plots
        steps.append(t)
        ax_lin.cla()
        for k, v in num_lists.items():
            v.append(len(state_lists[k]))
            ax_lin.plot(steps, v, '-' + style[k])
        
        # Diffusion plot
        ax_dif.cla() # This makes the program run much faster
        diff_plot = ax_dif.imshow(model.virions.u.T, vmin=0, vmax=0.5,
                      origin='lower')
        # diff_plot.collections[0].colorbar.update_normal(diff_plot)
        # if colorbar:
        #     colorbar.set_clim(vmin=np.min(model.virions.u), vmax=np.max(model.virions.u))
        if not colorbar:
            colorbar = fig.colorbar(diff_plot, ax=ax_colorbar)
            # colorbar.outline.set_visible(False)
            # colorbar.ax.yaxis.set_ticks_position('right')
            # colorbar.ax.yaxis.set_label_position('right')
            # colorbar.ax.yaxis.set_ticks([])
            # colorbar.ax.yaxis.set_ticklabels([])

            # diff_plot.set_clim(0, 0.5)
        # diff_plot.set_clim(vmin=np.min(model.virions.u), vmax=np.max(model.virions.u))
            
        # line.set_data(t, len(state_lists[CellState.INFECTED]))
        
        plt.draw()
        # plt.savefig(file_name.format(t))
        model.step()
        plt.pause(0.000001)
    print(f"Elapsed time: {time.perf_counter() - start_time:.3f}")
    plt.waitforbuttonpress()
