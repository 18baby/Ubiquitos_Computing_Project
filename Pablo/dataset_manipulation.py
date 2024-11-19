import pandas as pd 

# Step 1. Build the "Dong Code x Dong name" conversion table
file_path = "datasets\Dong_conversion_codes.xlsx"
dataframe_Code2Dong = pd.read_excel(file_path, usecols=["행정동코드","행정동"])

#Filtering, remove duplicates
dataframe_Code2Dong.drop_duplicates(inplace = True, subset='행정동', keep="last")
dataframe_Code2Dong.dropna(inplace = True)

# Step 2. Build on the previous conversion table and other datasets to append monthly data for each Dong, vectorizing features
datasetType1, datasetType2, datasetType3 = "LOCAL_PEOPLE_DONG_", "LONG_FOREIGNER_DONG_", "TEMP_FOREIGNER_DONG_"

date = 202406
#end = 202406
# Loop through each monthly data, averaging the values of the daily entries for each Dong
#for i in range (start, end):
file_path1 = "datasets" + "\\" + datasetType1 + str(date) + ".csv"
file_path2 = "datasets" + "\\" + datasetType2 + str(date) + ".csv"
file_path3 = "datasets" + "\\" + datasetType3 + str(date) + ".csv"
df1, df2, df3 = pd.read_csv(file_path1, index_col=False), pd.read_csv(file_path2, index_col=False), pd.read_csv(file_path3, index_col=False);

df_monthlyAverages = pd.DataFrame()                         #This is poorly optimized, every loop iteration the dataframe increases in size?
numberOfDongs = dataframe_Code2Dong.shape[0]
for j in range(0, numberOfDongs-1):
    dongCode = int(dataframe_Code2Dong.iloc[j, 0])
    # Evaluate data per each Dong
    df1_filtered = df1.loc[df1["행정동코드"] == dongCode]   #evaluate LOCAL_PEOPLE_DONG   data per each Dong
    df2_filtered = df2.loc[df2["행정동코드"] == dongCode]   #evaluate LONG_FOREIGNER_DONG data per each Dong
    df3_filtered = df3.loc[df3["행정동코드"] == dongCode]   #evaluate TEMP_FOREIGNER_DONG data per each Dong

    # Do monthly average for the given Dong
    monthlyAverage_df1 = pd.DataFrame(df1_filtered.mean()).T
    monthlyAverage_df1["기준일ID"] = date
    monthlyAverage_df2 = pd.DataFrame(df2_filtered.mean()).T
    monthlyAverage_df2["기준일ID"] = date
    monthlyAverage_df3 = pd.DataFrame(df3_filtered.mean()).T
    monthlyAverage_df3["기준일ID"] = date

    #Aggregate the dataframes
    #uncomment block below to check on indexing issue when adding the 41st dong to the dataframe
    #print(j)
    #if j == 41:
    #    print(row_filtered.head())
    #    print(df_monthlyAverages)

    row = pd.concat([monthlyAverage_df1, monthlyAverage_df2, monthlyAverage_df3], axis=1, join='inner')
    row_filtered = row.T.drop_duplicates().T
    df_monthlyAverages = pd.concat([df_monthlyAverages, row_filtered], ignore_index=True)
    
