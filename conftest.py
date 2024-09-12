
import os
import shutil

import pytest


@pytest.fixture(scope="session", autouse=True)
def clear_allure_results():

    print("Fixture clear_allure_results() has been invoked.")
    allure_results_directory = "/Users/mantsv/PycharmProjects/pythonProject17/Haust_Oracle/allure_result_folder"
    print(f"Checking if directory exists: {allure_results_directory}")

    if os.path.exists(allure_results_directory):
        try:
            for filename in os.listdir(allure_results_directory):
                file_path = os.path.join(allure_results_directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
            print(f"Allure results in {allure_results_directory} have been cleared successfully.")
        except Exception as e:
            print(f"Error occurred while clearing Allure results: {e}")
    else:
        print(f"Directory does not exist: {allure_results_directory}")
