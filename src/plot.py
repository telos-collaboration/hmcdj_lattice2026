from argparse import ArgumentParser

import matplotlib.pyplot as plt
import numpy as np


def get_args():
    parser = ArgumentParser()
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")
    parser.add_argument("--plot_styles", default=None)
    return parser.parse_args()


def get_data(input_filename):
    plaquettes = {}
    acceptances = {}
    mdsteps = {}
    trajectory = 0
    
    with open(input_filename) as f:
        for line in f:
            split_line = line.split()
            if "Current acceptance rate is" in line:
                acceptances[trajectory] = float(split_line[11]), float(split_line[13])
            elif "Plaquette" in line:
                if len(split_line) > 7 and split_line[7] == "Plaquette:":
                    trajectory = int(split_line[9])
                    plaquettes[trajectory] = float(split_line[11])
            elif "Number of MD steps" in line:
                mdsteps[trajectory] = int(split_line[-1])
            elif line.startswith("double targetAcceptance"):
                target_acceptance = float(split_line[3])
            elif line.startswith("double deltaTargetAcceptance"):
                delta_target_acceptance = float(split_line[3])
            elif line.startswith("int rethermalisationTrajectories"):
                rethermalisations = int(split_line[3])
            elif line.startswith("int thermalisationTrajectories"):
                thermalisations = int(split_line[3])
            elif line.startswith("int maxTuningTrajectories"):
                max_tuning_trajectories = int(split_line[3])

    return {
        "plaquettes": plaquettes,
	"acceptances": acceptances,
	"mdsteps": mdsteps,
        "rethermalisations": rethermalisations,
        "thermalisations": thermalisations,
        "max_tuning_trajectories": max_tuning_trajectories,
        "target_acceptance": target_acceptance,
        "delta_target_acceptance": delta_target_acceptance,
    }


def plot(data):
    fig, ax = plt.subplots(layout="constrained", figsize=(7, 3))

    # Plot average plaquette history
    ax.plot(*zip(*data["plaquettes"].items()), label="Plaquette", color="C0")
    ax.set_ylabel("Plaquette")

    # Set up acceptance axis
    ax2 = ax.twinx()
    ax2.set_ylim(0, 1)
    ax2.axhline(data["target_acceptance"], color="C1")
    ax2.axhline(data["target_acceptance"] + data["delta_target_acceptance"], color="C1", dashes=(6, 5))
    ax2.axhline(data["target_acceptance"] - data["delta_target_acceptance"], color="C1", dashes=(6, 5))
    ax2.set_ylabel("Acceptance")
    ax.axhline(np.nan, color="C1", label="Target acceptance")

    # Plot acceptance blocks as function of trajectory window they are averages for
    previous_trajectory = data["thermalisations"] + data["rethermalisations"]
    for trajectory, (value, error) in data["acceptances"].items():
        ax2.fill_between((previous_trajectory, trajectory), (value - error, value - error), (value + error, value + error), color="C1", alpha=0.1)
        previous_trajectory = trajectory
    ax.fill_between([1], [np.nan], [np.nan], color="C1", alpha=0.1, label="Acceptance")

    # Set up MD steps
    ax3 = ax.twinx()
    ax3.spines.right.set_position(("axes", 1.15))
    ax3.set_ylabel("Molecular dynamics steps per trajectory")

    # Plot MD steps history as function of trajectory window it was active for
    previous_trajectory = 1000
    for trajectory, steps in reversed(data["mdsteps"].items()):
        ax3.plot((previous_trajectory, trajectory), (steps, steps), color="C2", dashes=(1, 1))
        previous_trajectory = trajectory
    ax3.set_ylim(0, None)
    ax.plot([1], [np.nan], color="C2", label="Step size", dashes=(1, 1))

    # We have three y-axes; colour code them so it's easier to see which relates to each data series
    ax.yaxis.label.set_color("C0")
    ax2.yaxis.label.set_color("C1")
    ax3.yaxis.label.set_color("C2")
    
    ax.tick_params(axis='y', colors="C0")
    ax2.tick_params(axis='y', colors="C1")
    ax3.tick_params(axis='y', colors="C2")

    # Label end of tuning/start of monitoring
    ax.axvline(data["max_tuning_trajectories"], color="black", lw=1, dashes=(4, 2), label="Tuning ends")

    # Axes labels
    ax.set_xlabel("Trajectory")
    ax.set_ylabel("Plaquette")
    ax.legend(loc="best")
    
    return fig


def main():
    args = get_args()
    if args.plot_styles:
        plt.style.use(args.plot_styles)

    data = get_data(args.input_filename)
    fig = plot(data)
    if args.output_filename is None:
        plt.show()
    else:
        fig.savefig(args.output_filename)


if __name__ == "__main__":
   main()
