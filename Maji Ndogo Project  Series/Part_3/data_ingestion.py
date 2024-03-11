from sqlalchemy import create_engine, text
import logging
import pandas as pd
# Name our logger so we know that logs from this module come from the data_ingestion module
logger = logging.getLogger('data_ingestion')
# Set a basic logging message up that prints out a timestamp, the name of our logger, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

### START FUNCTION

def create_db_engine(db_path):
    """
    This function creates a SQLAlchemy database engine and tests if the connection functions as intended.

    Parameters:
    - db_path (str): This is the database connection string to be used to establish a connection.

    Returns:
    - engine: The is the SQLAlchemy database engine created.

    Raises:
    - ImportError: This is the error raised if SQLAlchemy is not installed.
    - Exception: This is the error raised if there is an error creating the database engine.
    """
    try:
        engine = create_engine(db_path)
        # Test connection
        with engine.connect() as conn:
            pass
        # test if the database engine was created successfully
        logger.info("Database engine created successfully.")
        return engine # Return the engine object if it all works well
    except ImportError: #If we get an ImportError, inform the user SQLAlchemy is not installed
        logger.error("SQLAlchemy is required to use this function. Please install it first.")
        raise e
    except Exception as e:# If we fail to create an engine inform the user
        logger.error(f"Failed to create database engine. Error: {e}")
        raise e
    
def query_data(engine, sql_query):
    """
    This function executes a SQL query on the provided database engine and returns the result as a DataFrame.

    Parameters:
    - engine: SQLAlchemy database engine object to be used.
    - sql_query: The SQL query String to be executed.

    Returns:
    - df: A Pandas DataFrame containing the query result.

    Raises:
    - ValueError: The error raised when the query returns an empty DataFrame as a result.
    - Exception: If an error occurs when executing the query.
    """
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
        if df.empty:
            # Log a message or handle the empty DataFrame scenario as needed
            msg = "The query returned an empty DataFrame."
            logger.error(msg)
            raise ValueError(msg)
        logger.info("Query executed successfully.")
        return df
    except ValueError as e: 
        logger.error(f"SQL query failed. Error: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while querying the database. Error: {e}")
        raise e
    
def read_from_web_CSV(URL):
    """
    Reads a CSV file from a web URL and returns it as a Pandas DataFrame.

    Parameters:
    - URL (str): The URL pointing to the CSV file.

    Returns:
    - df: Pandas DataFrame containing the CSV data.

    Raises:
    - pd.errors.EmptyDataError: If the URL does not point to a valid CSV file.
    - Exception: If there is an error reading the CSV from the web.
    """
    try:
        df = pd.read_csv(URL)
        logger.info("CSV file read successfully from the web.")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error("The URL does not point to a valid CSV file. Please check the URL and try again.")
        raise e
    except Exception as e:
        logger.error(f"Failed to read CSV from the web. Error: {e}")
        raise e
    
### END FUNCTION

