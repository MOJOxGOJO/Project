from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re

# Set Chrome options
options = Options()
options.add_argument("start-maximized")
options.add_argument("user-data-dir=/Users/akshat/Library/Application Support/Google/Chrome")  # Replace with your Chrome user directory
options.add_argument("profile-directory=Default")  # Default Chrome profile

# Set the path for ChromeDriver
service = Service("/opt/homebrew/bin/chromedriver")  # Replace with your chromedriver path
driver = webdriver.Chrome(service=service, options=options)

# Regular expression to match Input and Output blocks
input_pattern = r"Input:\s*(.*)"
output_pattern = r"Output:\s*(.*)"

def fetch_test_cases(url):
    driver.get(url)
    
    # Wait for the example section to load
    try:
        examples_section = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'example'))
        )
        print("Examples section loaded!")
    except Exception as e:
        print(f"Error loading examples: {str(e)}")
        return []
    
    # Find all example sections
    examples = driver.find_elements(By.CSS_SELECTOR, "strong.example")
    test_cases = []

    # Iterate through each example section and extract the input and output
    for example in examples:
        try:
            # Extract the following <pre> tag content that holds both Input and Output
            pre_tag = example.find_element(By.XPATH, "following::pre[1]").text.strip()

            # Separate input and output using the regex
            input_match = re.search(input_pattern, pre_tag)
            output_match = re.search(output_pattern, pre_tag)

            if input_match and output_match:
                input_data = input_match.group(1).strip()
                output_data = output_match.group(1).strip()

                # Append the input and output to the test_cases list
                test_cases.append({
                    'input': input_data,
                    'output': output_data
                })
            else:
                print(f"Error: Could not match input/output in example: {pre_tag}")
        except Exception as e:
            print(f"Error extracting input/output: {str(e)}")

    return test_cases

# Prompt user for the LeetCode problem URL
problem_url = input("Enter the LeetCode problem URL: ").strip()

# Fetch test cases for the provided URL
test_cases = fetch_test_cases(problem_url)

# Save test cases to a JSON file
if test_cases:
    # Generate a file name based on the problem title
    file_name = "test_cases.json"
    with open(file_name, "w") as f:
        json.dump(test_cases, f, indent=4)
    print(f"Test cases saved to {file_name}")
else:
    print("No test cases found or an error occurred.")

# Quit the driver
driver.quit()
