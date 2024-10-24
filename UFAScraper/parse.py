import json

import matplotlib.pyplot as plt

with open("ufaevents.txt", "r") as f:
    for line in f:
        json_object = json.loads(line)
        
        XThrower = []
        yThrower = []

        xReciever = []
        yReciever = []

        for type in json_object["data"]['homeEvents']:
            if type['type'] == 18:
                XThrower.append(type['throwerX'])
                yThrower.append(type['throwerY'])
                xReciever.append(type['receiverX'])
                yReciever.append(type['receiverY'])
        



        # Create a figure and axis
        fig, ax = plt.subplots()

        for i in range(len(XThrower)):
            # Draw an arrow from (0, 0) to (1, 1)
            ax.arrow(XThrower[i], yThrower[i], xReciever[i], yReciever[i], head_width=1, head_length=1, fc='k', ec='k')

        # Set the axis limits
        ax.set_xlim([-100, 120])
        ax.set_ylim([0, 200])

        # Show the plot
        plt.show()
        
        break
        
        
        

        