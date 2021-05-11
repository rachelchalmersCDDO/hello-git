# Create the figure again - so we're saving the right thing.
figure, axes = plt.subplots(figsize=(6, 5))

# Plot the Data
axes.scatter(x=UK_gapminder["gdp_per_cap"], y=UK_gapminder["fertility"],
             color= "#A5CD46",
             alpha=0.9)

# Add Labels and titles
plt.suptitle("Graph showing Fertility by GDP per Capita", 
             fontname="Arial", size=16)

plt.title("Data from Gapminder Dataset" , 
          fontname="Arial", size=12, loc="left")

# Add Labels
axes.set_xlabel("Gross Domestic Product per Capita in International Dollars", fontname="Arial", size=12)
axes.set_ylabel("Fertility (number of children per woman)", fontname="Arial", size=12)

#Set the caption
figure.text(x=0.65, y=-0.01, s="Source: Gapminder", ha="left",
            fontname="Arial", size=12)

# Set Y axis to start at 0.
axes.set_ylim(bottom=0) 

# Set Tick Colours to the same grey as our gridlines
axes.xaxis.set_tick_params(color=(0.7451, 0.7451, 0.7451))
axes.yaxis.set_tick_params(color=(0.7451, 0.7451, 0.7451));

# NEW - Save the JPEG at 300 DPI
figure.savefig("../outputs/exercise_jpeg.jpeg", dpi=300, bbox_inches="tight")

# NEW - Save the PDF
figure.savefig("../outputs/exercise_pdf.pdf",bbox_inches="tight")

