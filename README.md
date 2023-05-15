# script-storyboard-generator

### Goal: Use natural language processing methodologies to distill movie scripts into prompts to create AI generated storyboards

I would like to test the current capacity of AI image generators to assist creative workflows in film. Illustration and storyboarding is a crucial process in film and television pre-production and encompasses writing, blocking, FX, sound, and cinematographic design. The goal is to develop a workflow that can assist visual artists with preliminary design.

Task challenges:
1. Meaningfully summmarize information from compositionally rigid documents (movie scripts)
2. Compose prompts for AI generators that maximize efficiency and accuracy (using MidJourney, Stable Diffusion, etc.)
3. Build a short application with a summarization + Stable Diffusion model pipeline

## Run the streamlit app locally
In a virtual environment, locate `requirements.txt` and `script_summarizer.py` in the directory.
Run the following:
```
pip install -r requirements.txt
python script_summarizer.py
streamlit run [user folder]/script_summarizer.py
```
**NOTE**: If a GPU is available, uncomment lines 50, 51, 79, 80 in `script_summarizer.py` to increase processing speed. Without GPU, the Stable Diffusion model will take 25-30 minutes to run on a machine with 16 GB RAM. 

## Dataset documentation

Title: **movie_scenes_by_header.csv** <br>
Description: This dataset contains the scripts for _28 Days Later, Isle of the Dead, Jurassic Park, Pan’s Labyrinth,_ and _Whiplash_. <br>
Data Source: I used five manually encoded scripts from [Kaggle](https://www.kaggle.com/datasets/gufukuro/movie-scripts-corpus) for my analysis. I went with manual encoding to minimize the effect of machine learning miscodings on my overall project. Human mislabeling is also possible since this dataset was user created. I used regex statements to split headings and their respective text. <br>
Date Created: March 10, 2023 <br>
Last Modified: April 20, 2023<br>

Size: 85.6 KB —  6 columns, 580 entries<br>
Format: Comma-separated values <br>
Encoding: UTF-8 <br>

Columns: scriptID, sceneID, header, text <br>
Column Descriptions: 
* scriptID: type (integer), unique integer identifier for each movie <br>
* sceneID: type (integer), unique integer identifier for each scene per movie <br>
* header: type (object), one of four scene headings (scene_heading, text, dialog, speaker_heading) <br>
* text: type (object), text that follows the header in the script <br>
* upper: type(object, list), extracted uppercase words from the screenplay text. Uppercase words in screenplay indicate important characters, blockings, camera angles, etc. <br>
* tokens: type(object), preprocessed text from the `text` column <br>
---
Title: **movie_scenes.csv** <br>
Description: This dataset contains the scripts for _28 Days Later, Isle of the Dead, Jurassic Park, Pan’s Labyrinth,_ and _Whiplash_. <br>
Data Source: I used five manually encoded scripts from [Kaggle](https://www.kaggle.com/datasets/gufukuro/movie-scripts-corpus) for my analysis. I went with manual encoding to minimize the effect of machine learning miscodings on my overall project. Human mislabeling is also possible since this dataset was user created. Data was created by using regex statements to split scripts into a dataframe, and then the dataframes for all scripts were concatenated. <br>
Date Created: March 10, 2023 <br>
Last Modified: April 20, 2023<br>

Size: 50.6 KB —  4 columns, 34 entries<br>
Format: Comma-separated values <br>
Encoding: UTF-8 <br>

Columns: scriptID, sceneID, text, upper <br>
Column Descriptions: 
* scriptID: type (integer), unique integer identifier for each movie <br>
* sceneID: type (integer), unique integer identifier for each scene per movie <br>
* text: type (object), entire text of the scene, screenplay headings included <br>
* upper: type(object, list), extracted uppercase words from the screenplay text. Uppercase words in screenplay indicate important characters, blockings, camera angles, etc. <br>
