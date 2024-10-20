import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import warnings
warnings.filterwarnings("ignore")

# Model path (make sure this is the correct path)
model_path = 'gaussalgo/T5-LM-Large-text2sql-spider'

# Load the model and tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Check if CUDA is available and use it if possible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Define a sample question and schema
question = "What is the average, minimum, and maximum age for all French musicians?"
schema = """
   "stadium" "Stadium_ID" int , "Location" text , "Name" text , "Capacity" int , "Highest" int , "Lowest" int , "Average" int , foreign_key:  primary key: "Stadium_ID" [SEP] 
   "singer" "Singer_ID" int , "Name" text , "Country" text , "Song_Name" text , "Song_release_year" text , "Age" int , "Is_male" bool , foreign_key:  primary key: "Singer_ID" [SEP] 
   "concert" "concert_ID" int , "concert_Name" text , "Theme" text , "Year" text , foreign_key: "Stadium_ID" text from "stadium" "Stadium_ID" , primary key: "concert_ID" [SEP] 
   "singer_in_concert"  foreign_key: "concert_ID" int from "concert" "concert_ID" , "Singer_ID" text from "singer" "Singer_ID" , primary key: "concert_ID" "Singer_ID"
"""

# Prepare the input text
input_text = " ".join(["Question:", question, "Schema:", schema])

# Tokenize the input text
model_inputs = tokenizer(input_text, return_tensors="pt").to(device)

# Generate the SQL query
with torch.no_grad():
    outputs = model.generate(**model_inputs, max_length=512)

# Decode the output back to text
output_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)

print("SQL Query:")
print(output_text[0])

