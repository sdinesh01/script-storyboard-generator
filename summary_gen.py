# imports

import pandas as pd
import numpy as np
import random
import transformers
import torch
from transformers import pipeline
from textsum.summarize import Summarizer
from diffusers import StableDiffusionPipeline


def load_data():
        df = pd.read_csv(URL, index_col=[0])
        return df

    def GetSceneComponents(option=option):
        '''
        Get all of the rows for a scene
        Params: 
            option: input of the movie selected by user
        '''
        df = load_data()
        movie_id = {"Pan's Labryinth":0, 'Whiplash':1, 
                    '28 Days Later':2, 'Jurassic Park':3, 'Isle of the Dead':4}
        script_id = movie_id.get(str(option))
        parts_by_movie = df.loc[(df['scriptID'] == int(script_id))]
        scenes_per_script = len(parts_by_movie['sceneID'].unique())
        scene_id =random.randint(0,scenes_per_script)
        script_components = parts_by_movie.loc[(df['sceneID'] == scene_id)]

        return script_components, scene_id

    def summarize_text(min_output=40, max_output=77, max_length=80):
        """Take a string of text and generate a summary"""

        text_to_summarize, scene_id = GetSceneComponents()

        def create_long_text():
            "Take all components from a scene and join into a single long string for summarization"

            list_of_strings = []
            for i, row in enumerate(text_to_summarize['text']): 
                list_of_strings.append(row)

            long_text = '.'.join(list_of_strings)
            return long_text

        long_text = create_long_text()  
        summarizer = Summarizer(model_name_or_path="pszemraj/long-t5-tglobal-base-16384-book-summary") 
        out_str = summarizer.summarize_string(long_text)
        print(f"summary: {out_str}")

        return out_str, scene_id, long_text
