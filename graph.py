import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def calculate_catch_probability(throw_stat, accuracy_stat, catch_stat, offense_elo, defense_elo):
    # Define weights for each stat
    throw_weight = 0.3
    accuracy_weight = 0.5
    catch_weight = 0.6
    
    # Calculate the Elo modifier
    elo_diff = offense_elo - defense_elo
    """
    Modify the action probabilities based on the Elo difference.
    
    Parameters:
    - elo_diff: The Elo difference between two teams (team1_elo - team2_elo).
    - max_effect: The maximum modifier effect on the probabilities (default is 45%).
    
    Returns:
    - modifier: A multiplicative factor to adjust transition matrix probabilities for actions.
    """
    # Cap the Elo difference to prevent extreme adjustments
    capped_diff = np.clip(elo_diff, -1000, 1000)
    
    # Calculate the adjustment factor based on Elo difference
    elo_modifier = 1 + (0.45 * (capped_diff / 1000))

    # Calculate base probability with weighted stats
    weighted_throw = throw_stat * throw_weight
    weighted_accuracy = accuracy_stat * accuracy_weight
    weighted_catch = catch_stat * catch_weight
    base_probability = (weighted_throw + weighted_accuracy + weighted_catch) / (throw_weight + accuracy_weight + catch_weight)

    # Apply logarithmic scaling for stats below 80
    if base_probability < 80:
        base_probability = 90 - (10 * np.log(81 - base_probability))
        base_probability = max(0, min(base_probability, 90))

    # Adjust with Elo modifier and clamp probability to 0-100
    final_probability = min(100, base_probability * elo_modifier)
    return max(0, final_probability)

# Initial stat values
throw_stat_init = 50
accuracy_stat_init = 50
catch_stat_init = 50
offense_elo_init = 1500
defense_elo_init = 1500

# Create a figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.4)
probability_text = ax.text(0.5, 0.5, '', ha='center', va='center', fontsize=15)

# Plot initial probability
probability = calculate_catch_probability(throw_stat_init, accuracy_stat_init, catch_stat_init, offense_elo_init, defense_elo_init)
probability_text.set_text(f'Catch Probability: {probability:.2f}%')
ax.axis('off')  # Hide axes

# Sliders for throw, accuracy, and catch stats
ax_throw = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_accuracy = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_catch = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_offense_elo = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_defense_elo = plt.axes([0.25, 0.05, 0.65, 0.03])

slider_throw = Slider(ax_throw, 'Throw Stat', 0, 100, valinit=throw_stat_init)
slider_accuracy = Slider(ax_accuracy, 'Accuracy Stat', 0, 100, valinit=accuracy_stat_init)
slider_catch = Slider(ax_catch, 'Catch Stat', 0, 100, valinit=catch_stat_init)
slider_offense_elo = Slider(ax_offense_elo, 'Offense Elo', 1000, 2500, valinit=offense_elo_init)
slider_defense_elo = Slider(ax_defense_elo, 'Defense Elo', 1000, 2500, valinit=defense_elo_init)

# Update function
def update(val):
    throw_stat = slider_throw.val
    accuracy_stat = slider_accuracy.val
    catch_stat = slider_catch.val
    offense_elo = slider_offense_elo.val
    defense_elo = slider_defense_elo.val
    
    probability = calculate_catch_probability(throw_stat, accuracy_stat, catch_stat, offense_elo, defense_elo)
    probability_text.set_text(f'Catch Probability: {probability:.2f}%')
    fig.canvas.draw_idle()

# Connect sliders to update function
slider_throw.on_changed(update)
slider_accuracy.on_changed(update)
slider_catch.on_changed(update)
slider_offense_elo.on_changed(update)
slider_defense_elo.on_changed(update)

plt.show()
