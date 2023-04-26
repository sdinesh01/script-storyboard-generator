## imports
import numpy as np
import pandas as pd
import re


def split_script_text(data, column):
  '''
  Splits a DF column where inputs are manually encoded strings from a movie script into parts of the script 
  (i.e. scene_heading, text, dialog, speaker_heading)

  Parameters: 
    data: pandas dataframe 
    column: column name for parsing (str)
  
  '''
  heading_extractor = r"(?=scene_heading|text|dialog|speaker_heading)(scene_heading|text|dialog|speaker_heading)([^\f]+?)(?=dialog|text|scene_heading|speaker_heading|END SCENE)"
  data = data
  column = column
  df = pd.DataFrame()
  for i, x in enumerate(data[column]): 
    script_parts: list = re.findall(heading_extractor, x, flags = re.MULTILINE)
    scriptID = data.scriptID[i]
    sceneID = data.sceneID[i]
    # add script parts to new dataframe 
    for y in script_parts: 
      header = y[0]
      text = y[1]
      df = df.append({'scriptID': scriptID, 'sceneID': sceneID, 'header': header, 'text': text}, ignore_index=True)

  return df


def find_uppercase(data, column, new_col):
  '''
  Extract words in all caps from script text. 
  Params: 
    data: dataframe
    column: column to extract from
    new_col: str for new column name
  '''
  regex = r"\b[A-Z]+\b"
  data = data #dataframe
  column = column # string
  upper = []
  for i in data[column]:
    x: list = re.findall(regex, i, flags = re.MULTILINE)
    upper.append(x)
  data[new_col] = upper
  
  return

def clean_text(line): 
  '''
  Preprocess text 
  '''
  line = line.lower()  # Convert to lowercase
  line = re.sub(r"<[^>]*>", "", line)  # Remove HTML tags
  line = re.sub(r"[^a-z0-9]+", " ", line)  # Remove non-alphanumeric characters
  return line.strip()