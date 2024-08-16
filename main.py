# import libraries
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest
import json
import csv
import argparse

# set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
credentials = json.load(open("credentials.json"))
key = credentials['API_KEY']
endpoint = credentials['ENDPOINT']

def analyze_layout(file_path):
    client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )

    path_to_document = file_path
    with open(path_to_document, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout", analyze_request=f, content_type="application/octet-stream"
        )
    result: AnalyzeResult = poller.result() 
    
    data = []
    for page in result.pages:
        print(f"----Analyzing layout from page #{page.page_number}----")
    if result.tables:
        for table_idx, table in enumerate(result.tables):
            for cell in table.cells:
                if cell.column_index != 1 and cell.content != "":
                    #print(cell.content)
                    data.append(cell.content)
    return data

#Create csv file
#data = ["NAME", "ID", "Sam Baker", "1234", "Test One", "4931", "Test Two", "0001", "Kyle Swam", "3749"]

import csv

def data_to_csv(data, hours, filename):
    # Set to keep track of unique IDs
    unique_ids = set()
    
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["NAME", "ID", "HOURS"]
        writer.writerow(field)

        # Iterate through the data in pairs (name, id)
        for i in range(2, len(data), 2):
            name = data[i]
            id = int(data[i + 1])
            
            # Only write the row if the ID is unique
            if id not in unique_ids:
                writer.writerow([name, id, hours])
                unique_ids.add(id)

    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PDF to CSV')
    parser.add_argument('--file', type=str, required=True, help='Path to the document (PDF) file')
    parser.add_argument('--hours', type=int, required=True, help='Number of hours to include in the CSV')
    parser.add_argument('--output', type=str, required=True, help='Output CSV filename')
    args = parser.parse_args()

    data = analyze_layout(args.file)
    data_to_csv(data, args.hours, args.output)