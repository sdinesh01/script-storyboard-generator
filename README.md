# script-storyboard-generator

### Goal: Use natural language processing methologies to distill movie scripts into prompts to create AI generated storyboards

I would like to test the current capacity of AI image generators to assist creative workflows in film. Illustration and storyboarding is a crucial process in film and television pre-production and encompasses writing, blocking, FX, sound, and cinematographic design. The goal is to develop a workflow that can assist visual artists with preliminary design.

Task challenges:
1. Writing scripts to standardize, distill, and meaningfully extract information from compositionally rigid documents (movie scripts)
2. Composing prompts for AI generators that maximize efficiency and accuracy (using MidJourney, Stable Diffusion, etc.)
3. (Optional) Analyze scripts to select a genre-appropriate illustration style for storyboard generation

Initial coding challenges: 
1. Creating a corpus of movie scripts (usually available online in PDF formatting)
2. Identifying key elements of a screenplay (scene headings, action descriptions, shots/transitions) 
3. Standardizing text formatting across different documents, varied writing styles, and genres
3. Associating characters with actions, characters with other characters, and characters in relation to the setting

## Dataset documentation
Title: **movie_scenes_by_header.csv** <br>
Description: This dataset contains the scripts for _28 Days Later, Isle of the Dead, Jurassic Park, Pan’s Labyrinth,_ and _Whiplash_. <br>
Data Source: I used five manually encoded scripts from Kaggle for my analysis. I went with manual encoding to minimize the effect of machine learning miscodings on my overall project. Human mislabeling is also possible since this dataset was user created. I used regex statements to split headings and their respective text. <br>
Date Created: March 10, 2023 <br>
Last Modified: April 20, 2023<br>

Size: 85.6 KB —  6 columns, 543 entries<br>
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



