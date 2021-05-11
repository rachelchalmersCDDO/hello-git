# Create our figure and our axes
figure, axes = plt.subplots(figsize=(6, 5))

# Plot the Data
axes.scatter(x=UK_gapminder["gdp_per_cap"], y=UK_gapminder["fertility"],
             color= "#A5CD46",
             alpha=0.9)

# Add Labels and titles
axes.set_title("Graph showing Fertility by GDP per Capita", fontname="Arial", size=16)
axes.set_xlabel("Gross Domestic Product per Capita in International Dollars", fontname="Arial", size=12)
axes.set_ylabel("Fertility (number of children per woman)", fontname="Arial", size=12)

# Axes colour, line visibility
axes.yaxis.grid(True, color=(0.745, 0.745, 0.745))
axes.set_frame_on(False)
axes.set_axisbelow(True);

# Set Y axis to start at 0.
axes.set_ylim(bottom=0) 

# NEW - Set Tick Colours to the same grey as our gridlines
axes.xaxis.set_tick_params(color=(0.745, 0.745, 0.745))
axes.yaxis.set_tick_params(color=(0.745, 0.745, 0.745));