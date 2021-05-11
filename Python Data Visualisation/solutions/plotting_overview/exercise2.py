# Create our figure and our axes
figure, axes = plt.subplots(figsize=(6, 5))

# Plot the Data
axes.scatter(x=UK_gapminder["gdp_per_cap"], y=UK_gapminder["fertility"])

# NEW - Add Labels and titles
axes.set_title("Graph showing Fertility by GDP Per Capita")
axes.set_xlabel("Gross Domestic Product per Capita in International Dollars")
axes.set_ylabel("Fertility (number of children per woman)");