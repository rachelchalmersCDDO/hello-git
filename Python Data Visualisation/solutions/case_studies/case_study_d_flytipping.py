figure, axes = plt.subplots(figsize = (8,4)) # Set up our figure and axis

axes.axis("off") # Removes the axis from the figure

# Create the header - This is easiest to create as a new table with 1 row and position above our existing table.
header = plt.table(cellText=[["Number of fly-tipping incidents by waste type"]], cellLoc="left", loc="left",
                   bbox=[0.111, 0.97, 0.8098, 0.12]) # x, y , length, height

# Set the properties for this text box
for (row, col), cell in header.get_celld().items():
    cell.set_text_props(fontproperties=FontProperties(family ="Arial", weight="bold", size = 14), ha = "left")
    cell.set_edgecolor("black")
    cell.set_linewidth(1)
    cell.PAD = 0.01

# Create the Main Table
table = axes.table(cellText=flytipping.values, # Values we want in the cells
                   colLabels=flytipping.columns.str.replace(" ", "\n")  , # Our column headers
                   loc="upper left", # Where we want our table located
                   edges="closed") # Draws a grid around the cells

# Set top row to Bold and make taller
for (row, col), cell in table.get_celld().items():
    if (row == 0) or (col == -1):
        cell.set_height(0.22)
        cell.set_text_props(fontproperties=FontProperties(family="Arial", weight="bold", size=14), 
                            ma="right", va="bottom")
        cell.set_edgecolor("black")
        cell.set_linewidth(1)
        cell.PAD = 0.04
    
    else:
        cell.set_text_props(fontproperties=FontProperties(family="Arial", size=12), ma="right")
        cell.set_edgecolor("black")
        cell.set_linewidth(1)
        cell.PAD=0.04
    
# Loop over column 1 and make bold
for (row, col), cell in table.get_celld().items():
    if (col == 0):
        cell.set_text_props(weight="bold")

# Loop over each column and auto set the width
for each_column in range(len(flytipping.columns)):
    table.auto_set_column_width(each_column)

# Set Title and Captions
title = "Table 3.1 Types of other fly-tipping in England, 2011/12 to 2018/19 **"
plt.figtext(x=0.04, y=1.1, s=title, ha="left", fontweight="bold", fontsize=16, fontname="sans-serif")

caption = ("""* Other identified includes vehicle parts, animal carcasses, clinical waste, asbestos and ‘chemical drums, oil 
and fuel’ \n 
** Rounded to the nearest thousand 
\n Equivalent figures for 2007/08 to 2010/11 can be seen in the accompanying dataset.""" )

plt.figtext(x=0.08, y=0.12, s=caption, ha="left", fontweight="light", fontsize=10, fontname="sans-serif")
    
# Set the layout to tight
figure.tight_layout() # Controls the amount of white space around the table