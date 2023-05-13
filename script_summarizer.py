import pandas as pd
import numpy as np
import random
from PIL import Image, ImageEnhance
import requests
import json

import transformers
import torch
from torch import autocast
from transformers import pipeline
from textsum.summarize import Summarizer
from diffusers import StableDiffusionPipeline
from diffusers import DPMSolverMultistepScheduler

import streamlit as st


class StableDiffusionLoader:
    """
    Stable Diffusion loader and generator class. 

    Utilises the stable diffusion models from the `Hugging Face`(https://huggingface.co/spaces/stabilityai/stable-diffusion) library

    Attributes
    ----------
    prompt : str
        a text prompt to use to generate an associated image
    pretrain_pipe : str
        a pretrained image diffusion pipeline i.e. CompVis/stable-diffusion-v1-4

    """
    def __init__(self, 
                prompt:str, 
                pretrain_pipe:str='CompVis/stable-diffusion-v1-4'):
        """
        Constructs all the necessary attributes for the diffusion class.

        Parameters
        ----------
            prompt : str
                the prompt to generate the model
            pretrain_pipe : str
                the name of the pretrained pipeline
        """
        self.prompt = prompt
        self.pretrain_pipe = pretrain_pipe
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        #if self.device == 'cpu':
            #raise MemoryError('GPU need for inference')

        assert isinstance(self.prompt, str), 'Please enter a string into the prompt field'
        assert isinstance(self.pretrain_pipe, str), 'Please use value such as `CompVis/stable-diffusion-v1-4` for pretrained pipeline'


    def generate_image_from_prompt(self, save_location='prompt.jpg', use_token=False,
                                   verbose=False):
        """
        Class method to generate images based on the prompt

        Parameters
        ----------
            save_location : str - defaults to prompt.jpg
                the location where to save the image generated by the Diffusion Model
            use_token : bool
                boolean to see if Hugging Face token should be used
            verbose : bool
                boolean that defaults to False, otherwise message printed
        """
        pipe = StableDiffusionPipeline.from_pretrained(
            self.pretrain_pipe, 
            revision="fp16", 
            torch_dtype=torch.float32, 
            use_auth_token=use_token,
            num_inference_steps=20,
            batch_size = 1
            )
        #pipe = pipe.to(self.device)
        #with autocast(self.device):
        image = pipe(self.prompt)[0][0]
        image.save(save_location)
        if verbose: 
            print(f'[INFO] saving image to {save_location}')
        return image    

    def __str__(self) -> str:
        return f'[INFO] Generating image for prompt: {self.prompt}'

    def __len__(self):
        return len(self.prompt)

if __name__ == '__main__':
   
    SAVE_LOCATION = 'prompt.jpg'
    # Create the page title 
    st.set_page_config(page_title='Script to Diffusion Model Generator')
    # Create page layout
    st.title('Storyboard generator using Stable Diffusion')
    st.caption('An app to generate storyboards for a movie scene summarized by a summarization model.')
    
    # Create a sidebar with text examples
    with st.sidebar:
        # Selectbox
        add_selectbox = st.sidebar.selectbox(
        'Which movie would you like to summarize?',
        (
            "Pan's Labryinth",
             'Whiplash', 
             '28 Days Later',
             'Jurassic Park',
             'Isle of the Dead'
        ), index=0)

        st.markdown('Use the above drop down box to select a movie')
        st.text('Application by Shradha Dinesh')
    
    # Create text prompt
    
    URL = 'https://raw.githubusercontent.com/sdinesh01/script-storyboard-generator/main/data/movie_scenes_by_header3.csv'

    @st.cache_data
    def load_data():
        df = pd.read_csv(URL, index_col=[0])
        return df

    def GetSceneComponents(option=add_selectbox):
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

    prompt, sceneID, original_text = summarize_text()

    # Handle if the text box does not have any content in
    if len(prompt) > 0:
        st.markdown(f"""
        Original scene text: {original_text}
        """)
        print(original_text)
        st.markdown(f"""
        Storyboard this scene: {prompt}
        """)
        print(prompt)
        # Create a spinner to show the image is being generated
        with st.spinner('Generating image based on prompt'):
            sd = StableDiffusionLoader(prompt)
            sd.generate_image_from_prompt(save_location=SAVE_LOCATION)
            st.success('Generated stable diffusion model')

        # Open and display the image on the site
        image = Image.open(SAVE_LOCATION)
        st.image(image)  