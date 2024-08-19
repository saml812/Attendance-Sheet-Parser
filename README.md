# Volunteer Attendance Sheet Parser

A Python program designed to analyze the layout of a document using Azure's Document Intelligence API, extract table data such as Names and IDs, and save the extracted data into a CSV file with additional information such as hours.

## Features

- Analyze document layouts using Azure Document Intelligence API.
- Extract data from tables in the document.
- Generate a CSV file containing the extracted data along with additional information.
- Accepts user input for file path, hours, and output filename via a command-line interface.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.7+
- Azure SDK for Python (`azure-ai-documentintelligence`)
- A valid Azure subscription with access to the Document Intelligence API

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/saml812/Attendance-Sheet-Parser.git
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Azure credentials:

   - Create a `credentials.json` file in the project root with the following format:

    ```json
    {
      "API_KEY": "your-azure-api-key",
      "ENDPOINT": "your-azure-endpoint"
    }
    ```

4. Place your document (PDF) in the `documents/` directory, e.g., `documents/index.pdf`.

## Usage

You can analyze a document and generate a CSV by running the following command:

```bash
python main.py --file documents/index.pdf --hours 3 --output event_date.csv

Command-Line Arguments
--file: Specifies the path to the document (PDF) file you want to analyze.
--hours: The number of hours to include in the CSV file.
--output: The name of the output CSV file.
```
## Example

### PDF Preview
You can view the original attendance sheet document here:
[Sheet](https://github.com/saml812/Attendance-Sheet-Parser/blob/main/documents/index.pdf)

### CSV Preview
You can view the generated CSV file below:
[Table](https://github.com/saml812/Attendance-Sheet-Parser/blob/main/event_date.csv)







