import pandas as pd
import pytest
from field_data_processor import FieldDataProcessor
from weather_data_processor import WeatherDataProcessor

# Define config_params dictionary for testing
config_params = {
    "sql_query": """
        SELECT *
        FROM geographic_features
        LEFT JOIN weather_features USING (Field_ID)
        LEFT JOIN soil_and_crop_features USING (Field_ID)
        LEFT JOIN farm_management_features USING (Field_ID)
    """,
    "db_path": "sqlite:///Maji_Ndogo_farm_survey_small.db",
    "columns_to_rename": {'Annual_yield': 'Crop_type', 'Crop_type': 'Annual_yield'},
    "values_to_rename": {'cassaval': 'cassava', 'wheatn': 'wheat', 'teaa': 'tea'},
    "weather_csv_path": "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_station_data.csv",
    "weather_mapping_csv": "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_data_field_mapping.csv",
    "regex_patterns": {
        'Rainfall': r'(\d+(\.\d+)?)\s?mm',
        'Temperature': r'(\d+(\.\d+)?)\s?C',
        'Pollution_level': r'=\s*(-?\d+(\.\d+)?)|Pollution at \s*(-?\d+(\.\d+)?)'
    },
}

# Test to check if the shape of the weather DataFrame is correct
def test_read_weather_DataFrame_shape():
    weather_processor = WeatherDataProcessor(config_params)
    weather_processor.process()
    weather_df = weather_processor.weather_df
    expected_rows, expected_columns = 1843, 4
    assert weather_df.shape == (expected_rows, expected_columns), "Test failed"

# Test to check if the shape of the field DataFrame is correct
def test_read_field_DataFrame_shape():
    field_processor = FieldDataProcessor(config_params)
    field_processor.process()
    field_df = field_processor.df
    expected_rows, expected_columns = 5654, 20
    assert field_df.shape == (expected_rows, expected_columns), "Test failed"

# Add more tests as needed
# Test to check if the columns of the weather DataFrame are correct
def test_weather_DataFrame_columns():
    weather_processor = WeatherDataProcessor(config_params)
    weather_processor.process()
    weather_df = weather_processor.weather_df
    expected_columns = ['Weather_station_ID', 'Message', 'Measurement', 'Value']
    assert list(weather_df.columns) == expected_columns, "Test failed"

# Test to check if the columns of the field DataFrame are correct
def test_field_DataFrame_columns():
    field_processor = FieldDataProcessor(config_params)
    field_processor.process()
    field_df = field_processor.df
    expected_columns = [
        'Field_ID', 'Elevation', 'Latitude', 'Longitude', 'Location', 'Slope', 'Rainfall',
        'Min_temperature_C', 'Max_temperature_C', 'Ave_temps', 'Soil_fertility', 'Soil_type',
        'pH', 'Pollution_level', 'Plot_size', 'Annual_yield', 'Crop_type', 'Standard_yield',
        'Unnamed: 0', 'Weather_station'
    ]
    assert list(field_df.columns) == expected_columns, "Test failed"

# Test to check if elevation values in the field DataFrame are non-negative
def test_field_DataFrame_non_negative_elevation():
    field_processor = FieldDataProcessor(config_params)
    field_processor.process()
    field_df = field_processor.df
    assert (field_df['Elevation'] >= 0).all(), "Test failed"

# Test to check if crop types in the field DataFrame are valid
def test_crop_types_are_valid():
    field_processor = FieldDataProcessor(config_params)
    field_processor.process()
    field_df = field_processor.df
    valid_crop_types = ['cassava', 'tea', 'wheat', 'potato', 'banana', 'coffee', 'rice',
       'maize', 'wheat ', 'tea ', 'cassava ']
    assert field_df['Crop_type'].isin(valid_crop_types).all(), "Test failed"

# Test to check if rainfall values in the field DataFrame are positive
def test_positive_rainfall_values():
    field_processor = FieldDataProcessor(config_params)
    field_processor.process()
    field_df = field_processor.df
    assert (field_df['Rainfall'] >= 0).all(), "Test failed"

if __name__ == "__main__":
    # Run pytest with the specified options
    pytest.main(["-v", "--html=pytest_report.html"])

