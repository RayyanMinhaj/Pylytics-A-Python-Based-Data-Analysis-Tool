# PyLytics - A Python-Based Data Analysis Tool

PyLytics is a lightweight CLI tool to manage, explore, visualize, and perform statistical modeling on CSV datasets with ease, all from your terminal!


## Folder Structure
```
PyLytics/
    ├── data/          #Stores the dataset files
    |   ├── dataset1/    #Stores dataset1 data (CSV etc)
    |   |   └── data_1.csv
    |   └── dataset2/    #Stores dataset2 data (CSV etc)
    |       └── data_2.csv
    ├── reports/       # Stores generated reports (text, CSV, images)
    ├── graphs/        # Stores generated visualizations
    ├── models/        # Stores trained machine learning models
    ├── confusion_matrices/  # Stores confusion matrix plots
    ├── src/          #Stores the main Python source code
    |   ├── dataset_manager.py  #Class for dataset management
    |   ├── data_explorer.py    #Core functions for data exploration and analysis
    |   ├── visualizer.py       #Core functions for visualisation
    |   ├── modeling.py         #Core functions for statistical modeling
    |   ├── main.py             #Command-line interface logic
    |   └── report_generator.py #Generates a summary report for dataset
    ├── tests/        #Will work on it if time allows
    ├── config/     
    |   └── config.json  
    ├── README.md      
    └── requirements.txt 
```

## How to Run PyLytics!

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Pylytics.git
cd Pylytics
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Start the Program:
```bash
python src/main.py
```

### Available Commands

- `load <file_path> <dataset_name>` - Load a dataset (CSV file)
- `list` - List all loaded datasets
- `view <dataset_name> [n_rows]` - View first N rows of a dataset
- `remove <dataset_name>` - Remove a dataset from memory
- `analyze <dataset_name>` - Interactive data analysis (summary stats, missing data, frequency counts, filtering)
- `clean <dataset_name>` - Data cleaning (remove duplicates, handle missing values)
- `report <dataset_name>` - Generate a detailed analysis report for a dataset
- `visualize <dataset_name>` - Interactive visualization menu (histogram, bar chart, heatmap, scatter plot)
- `model <dataset_name>` - Train statistical models (regression, classification, clustering)
- `predict` - Make predictions using trained models
- `help` - List all available commands
- `exit` - Exit the program

---

### Example - Loading a Dataset

1. Load a dataset:
```
pylytics> load C:\Users\user\Downloads\Iris.csv my_dataset
```

2. List loaded datasets:
```
pylytics> list
```

3. View dataset contents:
```
pylytics> view my_dataset 10
```

4. Remove a dataset:
```
pylytics> remove my_dataset
```

---


## Example - Filtering and Cleaning a Dataset

1. **Filter a dataset:**
You can filter your dataset using custom conditions (similar to pandas query syntax).  

```
pylytics> analyze my_dataset
Select analysis type:
...
4. Filter data

Enter your choice (1-4): 4
Enter filter condition (e.g., age > 25 and country == "USA"):
> sepal_length > 5.0
```

2. **Clean duplicates:**
```
pylytics> analyze my_dataset
Select analysis type:
...
5. Clean duplicates

Enter your choice (1-5): 5
Specify columns for duplicate check (leave empty for all columns):
Enter column names separated by comma:
> 
```

---

## Example - Generating a Report

1. Generate a report for a dataset:
```
pylytics> report my_dataset
Report generated and saved to: reports/my_dataset_report.txt
```
The report includes:
- Dataset overview (shape, last modified)
- Column information (types, missing values)
- Missing values summary
- Numerical columns summary (all statistics)
- Categorical columns summary (frequency counts)
- Analyses performed (filtering, cleaning, etc.)
- End of file marker

---

## Example - Visualization

1. Visualize your data:
```
pylytics> visualize my_dataset

Select plot type:
1. Histogram
2. Bar Chart
3. Heatmap
4. Scatter Plot

Enter your choice (1-4): 4

Available columns: sepal_length, sepal_width, petal_length, petal_width
Enter the column name for the x-axis: sepal_length
Enter the column name for the y-axis: petal_width
Scatter plot for 'petal_width' vs 'sepal_length' generated and saved as 'my_dataset_petal_width_vs_sepal_length_scatter.png'.
```

**Visualization Options:**
- **Histogram:** For a single numeric column. Prompts for number of bins.
- **Bar Chart:** For a single categorical column. Shows top categories.
- **Heatmap:** Correlation heatmap for all columns (categorical columns are encoded automatically).
- **Scatter Plot:** For two numeric columns. Prompts for x and y columns.

---

## Example - Statistical Modeling

1. **Train a Classification Model:**
```
pylytics> model my_dataset

Select modeling type:
1. Linear Regression
2. Classification (Logistic Regression)
3. Clustering (KMeans)

Enter your choice (1-3): 2

Available columns: sepal_length, sepal_width, petal_length, petal_width, species
Enter target column: species
Enter feature columns (comma-separated, or leave blank for all except target): sepal_length, sepal_width, petal_length, petal_width

Classification model trained and saved as models/my_dataset_species_logreg.joblib
Accuracy: 0.9667
Precision: 0.9667
Recall: 0.9667
F1 Score: 0.9667

Would you like to save a confusion matrix plot? (y/n): y
Confusion matrix saved as confusion_matrices/my_dataset_species_logreg_confmat.png
```

2. **Make Predictions:**
```
pylytics> predict

Available models:
1. my_dataset_species_logreg.joblib

Enter the number of the model to use: 1

Enter feature values for prediction:
sepal_length: 5.1
sepal_width: 3.5
petal_length: 1.4
petal_width: 0.2

Prediction: 0
```

**Modeling Options:**
- **Linear Regression:** For predicting continuous values. Uses R² score for evaluation.
- **Classification (Logistic Regression):** For predicting categories/classes. Shows accuracy, precision, recall, F1 score, and classification report.
- **Clustering (KMeans):** For grouping similar data points. Assigns cluster labels to each row.

---

## Requirements

- Python 3.7+
- pandas >= 2.0.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- scikit-learn >= 1.3.0
- joblib >= 1.3.0

---