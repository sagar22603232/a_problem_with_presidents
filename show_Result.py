"""
The code to draw results from the input data.
"""
import numpy
import pandas
import dataframe_image as dfi
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# The results are drawn in the form of graphs in this function.
def showResult(df):
    lived_years_col = df["lived_years"].astype(int)
    value_counts = lived_years_col.value_counts()
    lived_days_col = df["lived_days"]

    weights = []
    for i in range(len(lived_years_col)):
        year = lived_years_col[i]
        weights.append(value_counts[year])
    weights = numpy.array(weights)
    weighted_values = weights * lived_days_col

    # Calculating the statistics as per years
    years_mean = lived_years_col.mean()
    weighted_years_mean = lived_years_col.sum() / weights.sum()
    years_median = lived_years_col.median()
    years_mode = lived_years_col.mode()
    years_max = lived_years_col.max()
    years_min = lived_years_col.min()
    years_std = lived_years_col.std()

    # REQ007 - REQ013 - Calculating the statistics (in days)
    days_mean = lived_days_col.mean()
    days_weighted_mean = weighted_values.sum() / weights.sum()
    days_median = lived_days_col.median()
    days_mode = lived_years_col.mode() * 365
    days_max = lived_days_col.max()
    days_min = lived_days_col.min()
    days_std = lived_days_col.std()

    data = {
        "Statistic": ["Mean Age", "Weighted Mean Age", "Median Age", "Mode Age", "Maximum Age", "Minimum Age", "Standard Deviation"],
        "Age (Days)": [days_mean, days_weighted_mean, days_median, list(days_mode), days_max, days_min, days_std],
        "Age (Years)": [years_mean, weighted_years_mean, years_median, [x for x in list(years_mode)], years_max, years_min, years_std]
    }

    def add_labels_barGraph(x,y):
        for i in range(len(x)):
            plt.text(i, round(y[i]//2,1), round(y[i],1), ha = 'center')

    df_stats = pandas.DataFrame.from_dict(data)
    df_stats.style.hide(axis="index")
    dfi.export(df_stats, "stats_in_barGraph.png")
    img = mpimg.imread('stats_in_barGraph.png')
    imgplot = plt.imshow(img)
    plt.axis('off')
    plt.show()

    # Show Stats in bar graph
    x_axis = ["Mean", "Weighted Mean", "Median", "Maximum", "Minimum"]
    x_axis_positions = range(len(x_axis))
    y_axis = [days_mean, days_weighted_mean, days_median, days_max, days_min]
    plt.figure(figsize=(8, 6))
    plt.bar(x_axis_positions, y_axis, 0.7, color=['#FFBF00', '#FFBF00', '#FFAC1C', '#CD7F32', '#DAA06D'])
    add_labels_barGraph(x_axis_positions, y_axis)
    plt.ylabel("Age (in Days)")
    plt.title("Statistics of Presidential Ages")

    plt.axhline(y = days_mean + days_std, color = 'r', linestyle = '--', label='Standard Deviation')
    plt.axhline(y = days_mean, color = 'gray', linestyle = '-.', label='Mean')
    plt.axhline(y = days_mean - days_std, color = 'r', linestyle = '--')

    plt.legend(labels=['Standard Deviation', 'Mean'])

    plt.xticks(x_axis_positions, x_axis)
    plt.show()

    # Show stats in range of ages in line graph
    def add_labels_to_line_graph(x, y):
        for x,y in zip(x,y):
            label = y
            plt.annotate(label, 
                        (x,y),
                        textcoords="offset points", 
                        xytext=(3,7),
                        ha='center') 

    df['age_range'] = pandas.cut(df['lived_years'].astype(int), [45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100], 
                        labels=['45-50', '51-55', '56-60', '61-65', '66-70', '71-75', '76-80', '81-85', '86-90', '91-95', '96-100'])
    
    age_range_column = df["age_range"].value_counts().sort_index().rename_axis('range').reset_index(name='counts')
    print(age_range_column['range'])

    x_axis = list(age_range_column['range'])
    y_axis = list(age_range_column['counts'])
    plt.figure(figsize=(15, 4))
    plt.plot(x_axis, y_axis, color='blue', marker='o')
    add_labels_to_line_graph(x_axis, y_axis)
    plt.title('Frequency Distribution of Presidential Ages', fontsize=14)
    plt.xlabel('Age Range', fontsize=10)
    plt.ylabel('No. of Presidents', fontsize=10)
    plt.grid(True)
    plt.show()

    print("Exit ProcessData")
    return 0