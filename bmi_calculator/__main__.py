import pandas as pd
import argparse


def bmi_type(value):
    """
    Returns the category and risk depending on the bmi value
    :param value:
    :return: category, risk
    """
    try:
        if value <= 18.4:
            return "Underweight", "Malnutrition risk"
        elif 18.5 <= value <= 24.9:
            return "Normal weight", "Low risk"
        elif 25 <= value <= 29.9:
            return "Overweight", "Enhanced risk"
        elif 30 <= value <= 34.9:
            return "Moderately obese", "Medium risk"
        elif 35 <= value <= 39.9:
            return "Severely obese", "High risk"
        else:
            return "Very severely obese", "Very high risk"
    except Exception:
        raise ValueError


def bmi_details(row):
    """
    Get bmi details
    :param row:
    :return: bmi value , category , range
    """
    try:
        bmi_value = round(row["WeightKg"] / (row["HeightCm"] * row["HeightCm"] / 10000), 2)
        bmi_category, bmi_risk = bmi_type(bmi_value)
        return bmi_value, bmi_category, bmi_risk
    except (ValueError, Exception):
        return "", "", ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BMI Calculator")
    parser.add_argument('--version', action='version', version='BMI Calculator v1.0')
    parser.add_argument('-i', "--input", dest='input_json_file',
                        help='Input JSON file path', required=True)
    parser.add_argument('-c', "--count", dest='count_frequency',
                        help='Count frequency of BMI category (Optional)', required=False, default=None)
    parser.add_argument('-o', "--output", dest='output_path',
                        help='File path where to write the data (Optional)', required=False, default=None)
    results = parser.parse_args()
    input_json_file = results.input_json_file
    frequency = results.count_frequency
    output_path = results.output_path
    df = pd.read_json(input_json_file, orient='records')
    df[["BMI", "BMI Category", "Health risk"]] = df.apply(lambda x: bmi_details(x), result_type="expand", axis=1)
    print(df.to_dict(orient="records"))

    # Writong to file if needed
    if output_path:
        try:
            df.to_csv(output_path, index=False)
            print(f"Output successfully written to {output_path}")
        except Exception as ex:
            print("Error while writing to file")

    # Outputs the count of people in a specified BMI category
    if frequency:
        try:
            count_freq = df['BMI Category'].str.lower().value_counts()[str(frequency).lower()]
            print(f"Frequency of '{frequency}' in BMI category is {count_freq}")
        except KeyError:
            print(f"Key Error: BMI category '{frequency}' not found !")
            print(
                "Accepted Inputs : 'Underweight' , 'Normal weight' , 'Overweight' , 'Moderately obese' , 'Severely obese' , 'Very severely obese'")
