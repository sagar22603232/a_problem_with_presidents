import filterData
import show_Result

def main():
    # Processes the input data
    dataframe = filterData.filterData()

    # Draws the necessary plots
    show_Result.showResult(dataframe)
    
    return 0

if __name__ == "__main__":
    main()