# import libraries
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest
import json
import csv

# set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
credentials = json.load(open("credentials.json"))
key = credentials['API_KEY']
endpoint = credentials['ENDPOINT']

def analyze_layout(file_path):
    client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )

    path_to_document = "images/index.pdf"
    with open(path_to_document, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout", analyze_request=f, content_type="application/octet-stream"
        )

    result: AnalyzeResult = poller.result() 

    if result.styles and any([style.is_handwritten for style in result.styles]):
        print("Document contains handwritten content")
    else:
        print("Document does not contain handwritten content")
    
    data = []
    for page in result.pages:
        print(f"----Analyzing layout from page #{page.page_number}----")
        print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

        # if page.lines:
        #     for line_idx, line in enumerate(page.lines):
        #         words = get_words(page, line)
        #         print(
        #             f"...Line # {line_idx} has word count {len(words)} and text '{line.content}' "
        #             f"within bounding polygon '{line.polygon}'"
        #         )

        #         for word in words:
        #             print(f"......Word '{word.content}' has a confidence of {word.confidence}")

        # if page.selection_marks:
        #     for selection_mark in page.selection_marks:
        #         print(
        #             f"Selection mark is '{selection_mark.state}' within bounding polygon "
        #             f"'{selection_mark.polygon}' and has a confidence of {selection_mark.confidence}"
        #         )

    if result.tables:
        for table_idx, table in enumerate(result.tables):
            # print(f"Table # {table_idx} has {table.row_count} rows and " f"{table.column_count} columns")
            # if table.bounding_regions:
            #     for region in table.bounding_regions:
            #         print(f"Table # {table_idx} location on page: {region.page_number} is {region.polygon}")
            for cell in table.cells:
                
                if cell.column_index != 1 and cell.content != "":
                    #print(cell.content)
                    data.append(cell.content)
                # print(f"...Cell[{cell.row_index}][{cell.column_index}] has text '{cell.content}'")
                # if cell.bounding_regions:
                #     for region in cell.bounding_regions:
                #         print(f"...content on page {region.page_number} is within bounding polygon '{region.polygon}'")

    print("----------------------------------------")
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

file = "images/index.pdf"
data = analyze_layout(file)
data_to_csv(data, 3, "event_date.csv")

# if __name__ == "__main__":
#     data = analyze_layout("images/index.pdf")
#     data_to_csv(data, 3, "event_date.csv")
