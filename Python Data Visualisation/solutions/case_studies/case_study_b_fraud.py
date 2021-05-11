figure, axes = plt.subplots(figsize=(10, 5))

bar_plot = sns.barplot(x="cases", y="fraud", data=fraud,
                       hue="year", # colour the bar according to the continent
                       palette=["#206095", "#118c7b"], # Set our colour order
                       orient="h") # Set the orientation to horizontal

# Add Labels, Title and Captions (this comes from Matplotlib!)
plt.title("England and Wales, year ending March 2019 and year ending March 2020" , 
          fontname="Arial", size=14, x=0.35, y=1.05, color="#6D6D6D")
plt.text(x=-900, y=6.0, s="Source: Office for National Statistics - Crime Survey for England and Wales",
         ha="left", color="#6D6D6D")
plt.text(x=2500, y=5.0, s="Number of incidents (thousands)",
         ha="left", color="#6D6D6D")
bar_plot.set_xlabel("") # The source image doesn't have X or Y labels so we can set them to blank to "hide" them
bar_plot.set_ylabel("") # The source image doesn't have X or Y labels so we can set them to blank to "hide" them

# Legend
# To display circles in the legend instead of rectangles we need to make a "fake" data plot with "o" markers.
legend_elements = [Line2D([0], [0], marker="o", color="w", label="Year ending March 2019", # labeling here to remove _
                          markerfacecolor="#206095", markersize=10),  # Blue for 2019
                   Line2D([0], [0], marker="o", color="w", label="Year ending March 2020", # labeling here to remove _
                          markerfacecolor="#118c7b", markersize=10)]  # Green for 2020

# Actually create the legend, using the legend_elements we created above.
legend = bar_plot.legend(handles=legend_elements, bbox_to_anchor=(-0.2, -0.2, 0.65, .102), loc="lower left",
                         ncol=2, mode="expand", borderaxespad=0,
                         prop={"family": "Arial", "size":12},
                         frameon=False)
# Loop through each thing in the legend to change the text colour
for text in legend.get_texts():
    text.set_color("#6D6D6D")

# The original Dataframe uses additonal lines to show the grouping.
# Multiple ways to do this but one the simplest is to create a second set of axes
# This usually creates a mirror image with the Y axis on the right 
#(Usefull for plotting multiple things with different scales!)
# Happily the ticks are in the exact place we want them to be - but could alter in the usual way
axes2 = axes.twinx() # Creates a copy of our existing axis
axes2.spines["left"].set_visible(True) # Shows the left side we want
axes2.yaxis.set_ticks_position("left") # Shows our ticks on the left
axes2.yaxis.set_ticklabels("") # The ticks are numeric - hide them like this
axes2.tick_params(axis = "y", direction="out", length=6, width=1, colors= "#BEBEBE") # Set tick marks
axes2.grid(b = False ) # Turn our Gridlines off for axes 2

# Gridlines for general axes - needs to come after setting axes2
axes.grid(b = True , which = "both", axis = "x", color = "#BEBEBE")
axes.tick_params(colors= "#6D6D6D")

# Removes the "spines" or edges of our vis
sns.despine(right=False, bottom=True) # right = False here or the last gridline doesn't show