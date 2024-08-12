import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.impute import SimpleImputer

# Read the data
X_full = pd.read_csv("C:\Users\nelly\OneDrive - University of Cape Town\Data Science\PERSONAL PROJECTS\Machine Learning\Housing Prices predictions\Data\train.csv", index_col='Id')
X_test_full = pd.read_csv("C:\Users\nelly\OneDrive - University of Cape Town\Data Science\PERSONAL PROJECTS\Machine Learning\Housing Prices predictions\Data\test.csv"", index_col='Id')

# Remove rows with missing target, separate target from predictors
X_full.dropna(axis=0, subset=['SalePrice'], inplace=True)
y = X_full.SalePrice
X_full.drop(['SalePrice'], axis=1, inplace=True)

# To keep things simple, we'll use only numerical predictors
X = X_full.select_dtypes(exclude=['object'])
X_test = X_test_full.select_dtypes(exclude=['object'])

# Break off validation set from training data
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# Function for comparing different approaches for models
def score_dataset(X_train, X_valid, y_train, y_valid):
    model = RandomForestRegressor(n_estimators=100, random_state=0)
    model.fit(X_train, y_train)
    preds = model.predict(X_valid)
    return mean_absolute_error(y_valid, preds)

#Checking for number of missing values in each column of training data
missing_val_count_by_column = (X_train.isnull().sum())
print(missing_val_count_by_column[missing_val_count_by_column >0])

#APPROACH ONE: Dropping columns with missing values
reduced_X_train = X_train.drop(['LotFrontage','MasVnrArea','GarageYrBlt'], axis =1)
reduced_X_valid = X_valid.drop(['LotFrontage','MasVnrArea','GarageYrBlt'], axis = 1)

print("MAE (Drop columns with missing values):")
print(score_dataset(reduced_X_train, reduced_X_valid, y_train, y_valid))

#APPROACH TWO: Imputation

imputer = SimpleImputer()
imputed_X_train = pd.DataFrame(imputer.fit_transform(X_train))
imputed_X_valid = pd.DataFrame(imputer.transform(X_valid))

#imputation removed column names; put them back
imputed_X_train.columns = X_train.columns
imputed_X_valid.columns = X_valid.columns

print("MAE (Imputation):")
print(score_dataset(imputed_X_train, imputed_X_valid, y_train, y_valid))

#Based on the data for, the Mean Absolute Error for the second approach is smaller so we train the model
# with the second approach

# Preprocessed training and validation features
final_X_train = imputed_X_train.copy()
final_X_valid = imputed_X_valid.copy()

# Define and fit model
model = RandomForestRegressor(n_estimators=100, random_state=0)
model.fit(final_X_train, y_train)

# Get validation predictions and MAE
preds_valid = model.predict(final_X_valid)
print("MAE (Your approach):")
print(mean_absolute_error(y_valid, preds_valid))

# Preprocess test data
final_imputer = SimpleImputer()
final_X_test = pd.DataFrame(final_imputer.fit_transform(X_test))

# Get test predictions
preds_test = model.predict(final_X_test)


