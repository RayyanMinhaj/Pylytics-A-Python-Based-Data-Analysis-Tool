# Pylytics-A-Python-Based-Data-Analysis-Tool
Pylytics - A lightweight CLI tool to manage, explore, and visualize CSV datasets with ease, all from your terminal!

```
PyLytics/
    ├── data/          #Stores the dataset files
    |   ├── dataset1/    #Stores dataset1 data (CSV etc)
    |   |   └── data_1.csv
    |   └── dataset2/    #Stores dataset2 data (CSV etc)
    |       └── data_2.csv
    ├── reports/       #Stores generated reports (text, CSV, images)
    ├── src/          #Stores the main Python source code
    |   ├── dataset_manager.py  #Core class for managing datasets
    |   ├── data_explorer.py #Core functions for data exploration and analysis
    |   ├── visualizer.py  #Core functions for visualisation
    |   ├── cli.py    #Command-line interface logic
    |   └── utils.py   #Utility functions (e.g., loading/saving data)
    ├── tests/        #Unit tests for each module
    |   ├── test_dataset_manager.py
    |   ├── test_data_explorer.py
    |   └── test_visualizer.py
    ├── config/     
    |   └── config.json  
    ├── README.md      
    └── requirements.txt 
```