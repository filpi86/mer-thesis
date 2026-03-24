# MER project - mood regulation

This project aims at predicting the user's emotional condition, and attempts to make music recommendation that direct the emotional
response towards a neutral emotional state

The following section will  shortly describe each file in the project

## Thesis_twitter

This file contains all the code used in the analysis of the data in the twitterPD.
There's some basic EDA and the models used for the lyrics classification.
The models used were: Bert sentiment analysis, GoEmotion, and the vad bert.
Bert sentiment analysis provides a single label prediction
GoEmotion provides multilabel predictions
vad bert provides VA values

## Thesis_twitter_plots

This files contains the main plots merged and ready for interpretation.
It is separate mainly due to facilitating the visual resources.
This file becomes outdated since it is no longer used for plot.
For the plots look at the file interpretability plots

## interpretability plots
This file compiles several plots to provide interpretability

## DEAM model

This file contains the code for a baseline model trained on the DEAM dataset.
Possibly the tests will be either in the bottom, moved to Thesis_twitter_plots or be performed in another file

## Deezer

This file might not be included, but if it is visible, the objective is to test the preview songs and possibly overlap the twitter database and the DEAM dataset

## form files

Those files are available as a proof of good faith and for transparency's sake.
They show how the songs were randomly selected, and the form that was sent to the expert