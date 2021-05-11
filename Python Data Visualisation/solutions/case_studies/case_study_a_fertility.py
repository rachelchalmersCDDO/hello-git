# Set up the arguments for the loop
age_groups = fertility["age_group"].unique().tolist() # Create a list for each unique age group (this is already sorted)
age_colours = ["#206095", "#118C7B", "#003C57", "#A8BD3A", "#27A0CC", "#B26C96" ]
    
# zips together our continent names and pallete colours into one list of tuples
age_palette = zip(age_groups, age_colours) 

# Create our figure and our axes
figure, axes = plt.subplots(figsize=(12, 5))

# Loop through each continent and each colour in turn
for age_group, age_colours in age_palette: 
    # Get only the data for the continent we are looking at
    age_rows = fertility[fertility["age_group"] == age_group]
    
    axes.plot(age_rows["year"], 
              age_rows["count"],
              c=age_colours, # Use corresponding colour from continent_palette
              label=age_group) # Gives each continent a label for our legend

# Set the Ticks
my_xticks = np.arange(start=1941, stop=2020, step=6) #Note this grouping DOESN'T match the data increments  
my_yticks = np.arange(start=0, stop=220, step=20) 
axes.set_xticks(my_xticks)
axes.set_yticks(my_yticks)

# Set the X ticks to point outwards, and change the colour of the Y ticks
axes.tick_params(axis="x", direction="out", length=4, width=1, colors="#6D6D6D")
axes.tick_params(axis="y", colors="#6D6D6D")

# Remove the padding (blank space) on the X axis
axes.margins(x=0)

# As we want the bottom spine to be visible for our ticks our previous setframeon(False) code won't work
# Strangely the answer is to turn OFF the ones you don't want, leaving just the one you do "on"
axes.spines["right"].set_visible(False)
axes.spines["top"].set_visible(False)
axes.spines["left"].set_visible(False)
# Set the bottom Spine (with the visible ticks) to align with the 0 of our Y.
# Set this BEFORE the gridlines, or it'll add them back on.
axes.spines["bottom"].set_position("zero")

# Gridlines
axes.grid(b=True, which="both", axis="x", color="white") 
axes.grid(b=True, which="both", axis="y", color="#BEBEBE")

# Add Labels, Title and Captions
plt.title("Age-specific fertility rates, England and Wales, 1938 to 2019", 
          fontname="Arial", size=14, loc="left", y=1.05, x=0 )

figure.text(x=0.11, y=-0.06, 
            s="Source: Office for National Statistics – Births in England and Wales", ha="left",
            fontname="Arial", size=12)

axes.annotate("Live births per 1,000 women in age group",
              xy=(1938,200),
              color="#6D6D6D" ) # Set colour)

# Set Legends
legend = axes.legend(bbox_to_anchor=(0, -0.2, 1, .102), loc="lower left",
                     ncol=6, mode="expand", borderaxespad=0,
                     prop={"family": "Arial", "size":12},
                     frameon=False);

# Loop through each thing in the legend to change the text colour
for text in legend.get_texts():
    text.set_color("#6D6D6D")