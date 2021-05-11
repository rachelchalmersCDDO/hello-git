# Create a new DataFrame for each year
fires_2008_09 = fires[fires["year"] == "2008/09"].reset_index()

fires_2018_19 = fires[fires["year"] == "2018/19"].reset_index()

########################################### Set Up ###########################################

# Set up the colours
colour_list = ["#8F23B3", "#BC7BD1",  "#E8D1EF"]

# Manually set our centre texts
# 08/09
total_2008_09 = fires_2008_09["count"].sum()
ct_0809 = ("{:,}\n{}".format(total_2008_09, "incidents") )
# 18/19
total_2018_19 = fires_2018_19["count"].sum()
ct_1819 = ("{:,}\n{}".format(total_2018_19, "incidents") )

#Manualy Set Up labels
#08/09
labels_0809 = []
for inc_type in fires_2008_09["incident_type"]:
    labels_0809.append("{}\n{:.0f}\n{:.2f}".format(
       inc_type, 
       list(fires_2008_09[fires_2008_09["incident_type"] == inc_type]["count"])[0], 
       list(fires_2008_09[fires_2008_09["incident_type"] == inc_type]["count"])[0] / fires_2008_09["count"].sum() * 100))

#18/19
labels_1819 = []
for inc_type in fires_2008_09["incident_type"]:
    labels_1819.append("{}\n{:.0f}\n{:.2f}".format(
       inc_type, 
       list(fires_2008_09[fires_2008_09["incident_type"] == inc_type]["count"])[0], 
       list(fires_2008_09[fires_2008_09["incident_type"] == inc_type]["count"])[0] / fires_2008_09["count"].sum() * 100))

# Plot the figure and axes

figure, (axes1, axes2) = plt.subplots(figsize=(14, 6), ncols = 2)

# Adjust the white space between each figure
figure.subplots_adjust(wspace= 0.4)

########################################### Pie 1 (08/09) ###########################################

# Plot the Data
axes1.axis("equal") # No one likes a squished donut
axes1.pie(x=fires_2008_09["count"],
          startangle=90,
          counterclock=False,
          labels=labels_0809,
          wedgeprops=dict(width=0.5, edgecolor="white", linewidth=2.5),
          textprops=dict(fontname="Arial", color="black", fontsize=12, multialignment="center"),
          labeldistance=1.2,        
          colors=colour_list)

# Set the title and center text
axes1.set_title("2008/2009", fontname="Arial", size=14, color="black", weight="bold")
axes1.text(s=ct_0809, x=0, y=0, ha="center", va="center", color="black", weight="bold", size=20)

########################################### Pie 2 (18/19) ###########################################

# Plot the Data
axes2.axis("equal") # No one likes a squished donut
axes2.pie(x=fires_2018_19["count"],
        startangle=90,
        counterclock=False,
        labels=labels_1819,
        wedgeprops=dict(width=0.5, edgecolor="white", linewidth=2.5),
        textprops=dict(fontname="Arial", color="black", fontsize=12, multialignment="center"),
        labeldistance=1.2,        
        colors=colour_list)

# Set the title and center text
axes2.set_title("2018/2019", fontname="Arial", size=14, color="black", weight="bold")
axes2.text(s=ct_1819, x=0, y=0, ha="center", va="center", color="black", weight="bold", size=20)

########################################### Plot Text ###########################################

plt.suptitle("Incidents attended by fire and rescue services in England, by incident \n type, for 2008/09 and 2018/19", 
             fontname="Arial", size=16, y=1.05, x=0.2, horizontalalignment="left",
             color="#8F23B3", weight="bold")

plt.text(s="Chart 1:", fontname="Arial", size=16, y=1.715, x=-4.8,
         horizontalalignment="left", color="#8F23B3", weight="bold")

plt.text(s="Source: FIRE0102", fontname="Arial", size=14, y=-1.4, x=-4.4,
         horizontalalignment="left", color="black", weight="bold");  
# Note the URL isn't easy to do so we've ommitted it
