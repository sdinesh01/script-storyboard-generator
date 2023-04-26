# imports
import pandas as pd
## transfomer models
import transformers
from transfomers import pipeline


def GetSceneComponents(df, scriptID, sceneID: int): 
  '''
  Get all of the rows from a dataframe for a requested scene
  Params: 
    df: input dataframe to extract data from
    scriptID: id corresponding to the script
    sceneID: id corresponding to the scene in a movie
  '''
  extracted = df.loc[(df['scriptID'] == scriptID) & (df['sceneID'] == sceneID)]

  return extracted

# summarize_text pipeline for dataframe with scenes split by scene components
def summarize_text(df, scriptID, sceneID, min_output=40, max_output=100, max_length=80):
    """Take a string of text and generate a summary"""

    def GetSceneComponents(): 
      '''
      Get all of the rows for a scene
      Params: 
        df: input dataframe to extract data from
        scriptID: id corresponding to the script
        sceneID: id corresponding to the scene in a movie
      '''
      extracted = df.loc[(df['scriptID'] == scriptID) & (df['sceneID'] == sceneID)]
      return extracted
    
    subset = GetSceneComponents()
    summarizer = pipeline('summarization','pszemraj/long-t5-tglobal-base-16384-book-summary')
    summarized_scene = []
    for i, row in enumerate(subset): 
      text = df['text'][i]
      result = summarizer(text)
      summarized_scene.append(result)

    return summarized_scene

# summarize_text pipeline for dataframe with a single scene per row
def summarize_text1(df, scriptID, sceneID, min_output=40, max_output=100, max_length=80):
    """Take a string of text and generate a summary"""

    def GetSceneComponents(): 
      '''
      Get all of the rows for a scene
      Params: 
        df: input dataframe to extract data from
        scriptID: id corresponding to the script
        sceneID: id corresponding to the scene in a movie
      '''
      extracted = df.loc[(df['scriptID'] == scriptID) & (df['sceneID'] == sceneID)]
      return extracted
    
    subset = GetSceneComponents()
    summarizer = pipeline('summarization','pszemraj/long-t5-tglobal-base-16384-book-summary')
    summarized_scene = []
    
    text = subset['text'][0]
    result = summarizer(text)
    summarized_scene.append(result)

    return summarized_scene