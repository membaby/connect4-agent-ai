import matplotlib.pyplot as plt

# Data
algorithms = ["1", "2", "3", "4", '5']

avg_expansions_1 = [6.29, 5.33, 237.97, 109.58, 9400.57]
avg_expansions_2 = [5.38, 12.11, 111.7, 435.2, 574.34]

avg_running_time_1 = [0.05679, 0.20904, 2.10027, 3.78304, 82.33464]
avg_running_time_2 = [0.05767, 0.35625, 1.06685, 13.67029, 18.62492]

# Create subplots for each metric
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Title
fig.suptitle('Comparing Performance of Two Connect-4 Solvers\nMinimax VS Minimax with Alpha Beta Pruning\n', fontsize=12, fontweight='bold')

# Plot AVG Steps as a line graph
axs[0].plot(algorithms, avg_expansions_1, marker='o', color='lightcoral', linestyle='-')
axs[0].plot(algorithms, avg_expansions_2, marker='o', color='lightskyblue', linestyle='-')
axs[0].set_xlabel('Depth')
axs[0].set_ylabel('Expanded Nodes')
# axs[0].set_title('AVG Expansions')

# Plot AVG Expansions as a line graph
axs[1].plot(algorithms, avg_running_time_1, marker='o', color='lightgreen', linestyle='-')
axs[1].plot(algorithms, avg_expansions_2, marker='o', color='cadetblue', linestyle='-')
# axs[1].set_title('AVG Running Time')
axs[1].set_xlabel('Depth')
axs[1].set_ylabel('Time (seconds)')

for ax in axs.flat:
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    # fontsize
    ax.tick_params(axis='both', which='major', labelsize=6)
    # title fontsize
    ax.title.set_fontsize(10)

# fig.text(0.13, 0.05, '* Using a heuristic evaluation function that depends on 4 features', ha='left', fontsize=10)
# fig.text(0.13, 0.025, '* Alpha-Beta Pruning does not change the result of Minimax, but it remarkably improves efficiency.', ha='left', fontsize=10)

# Add a caption to the graph

# Save the line graphs as pictures
plt.savefig('line_graphs.png')  # Save as a PNG image
plt.savefig('line_graphs.jpg')  # Save as a JPG image

# Show the line graphs
plt.show()
