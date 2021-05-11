# Create a United Kingdom DataFrame

UK_gapminder = gapminder[gapminder["country"] == "United Kingdom"]

# Create our figure and our axes
figure, axes = plt.subplots(figsize=(6, 5))

# Plot the Data
axes.scatter(x=UK_gapminder["gdp_per_cap"], y=UK_gapminder["fertility"]); 