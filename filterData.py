"""
The data from csv file is processed in this file
"""
import numpy
import pandas
from datetime import datetime
import dataframe_image as dfi
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#This function use dataframe to modifiy the input file.
def filterData():

    df = pandas.read_csv('input.csv', sep = ',',header = 0)
    df = df[:-1]

    # Remove bith year from bith date
    df["year_of_birth"] = pandas.DatetimeIndex(df["BIRTH DATE"]).year.astype(int)

    # Unkown death location we assume them as alive.
    df["LOCATION OF DEATH"].fillna('ALIVE', inplace=True)

    # Added a new variable "current_living_date" to calculate lived_dates, lived_months and lived_years.
    current_date = datetime.now().strftime("%b %d, %Y")
    df["current_living_date"] = df["DEATH DATE"]
    df["current_living_date"].fillna(current_date, inplace=True)

    # Calculating lived_years, lived_months and lived_days
    count_dates = pandas.DatetimeIndex(df["current_living_date"]) - pandas.DatetimeIndex(df["BIRTH DATE"])
    df["lived_years"] = count_dates / numpy.timedelta64(1, "Y")
    df["lived_months"] = count_dates / numpy.timedelta64(1, "M")
    df["lived_days"] = (count_dates/ numpy.timedelta64(1, "D"))

    #Updating the empty values in Death DATE column to ALIVE
    df["DEATH DATE"].fillna('ALIVE', inplace=True)

    # Function to return style to highlight living presidents in tables.
    def mark_alive(data):
        mark_living = ['background-color: yellow'] * len(data)
        mark_death = ['background-color: transparent'] * len(data)
    
        return mark_living if data['DEATH DATE'] == 'ALIVE' else mark_death

    # Find top 10 Presidents from longest lived to shortest lived.
    top_10_oldest_df= df.sort_values("lived_days", ascending=False).head(10)
    top_10_oldest_df["lived_years"] = top_10_oldest_df["lived_years"].astype(int)
    top_10_oldest_df.rename(columns={"lived_years": "AGE"}, inplace=True)

    top_10_oldest = top_10_oldest_df.style
    top_10_oldest.hide(axis="index")
    top_10_oldest.apply(mark_alive, axis=1)
    top_10_oldest.set_caption("Top 10 Presidents of the United States from longest lived to shortest lived")
    # show image of table
    dfi.export(top_10_oldest, "top_10_oldest.png")
    img = mpimg.imread('top_10_oldest.png')
    imgplot = plt.imshow(img)
    plt.axis('off')
    plt.show()

    # Find Output top 10 Presidents from shortest lived to longest lived.
    top_10_young_df = df.sort_values("lived_days", ascending=True).head(10)
    top_10_young_df["lived_years"] = top_10_young_df["lived_years"].astype(int)
    top_10_young_df.rename(columns={"lived_years": "AGE"}, inplace=True)

    top_10_young = top_10_young_df.style
    top_10_young.hide(axis="index")
    top_10_young.apply(mark_alive, axis=1)
    top_10_young.set_caption("Top 10 Presidents of the United States from shortest lived to longest lived")
    dfi.export(top_10_young, "top_10_young.png")
    img = mpimg.imread('top_10_young.png')
    imgplot = plt.imshow(img)
    plt.axis('off')
    plt.show()

    print("Exit filterData")

    return df