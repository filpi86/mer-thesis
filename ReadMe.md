# MER project - Relationshiops Between Tweets and Song Lyrics

This repository contains the code and analyses used to research the relationship 
between lyrics and tweets present on the Melody of Minds databse.

## Objectives

1. Estimate continuous Valence–Arousal–Dominance (VAD) scores for tweets and song lyrics.
2. classify tweets and lyrics using categorical emotion models.
3. compare the emotional characteristics of tweets and lyrics.
4. investigate whether these relationships differ between the depression and control groups.
5. evaluate the interpretability and generalizability of the resulting features and models.

## Emotion Representations

Two complementary representations of emotion are used:

- **Continuous:** valence, arousal, and dominance scores.
- **Categorical:** emotion labels and scores produced by sentiment and emotion-classification models.

The notebooks use pretrained transformer models including:

- `RobroKools/vad-bert`
- `SamLowe/roberta-base-go_emotions`
- `j-hartmann/emotion-english-distilroberta-base`
- `cardiffnlp/twitter-roberta-base-sentiment-latest`
- `bhadresh-savani/bert-base-uncased-emotion`

## Analysis Workflow

The main text-analysis workflow is:

1. Prepare and explore the Twitter and song data.
2. retrieve or preprocess the corresponding lyrics.
3. estimate emotion scores for tweets and lyrics.
4. combine the resulting features.
5. compare both sources statistically and visually.
6. examine model interpretability and validation performance.

## VA_tweets
This file is data preparation for the comparison between the tweets and the lyrics

## tweets_vs_lyrics
This file runs the VAD model and GoEmotions to get continuous and 

## Thesis_twitter_plots

This files contains the main plots merged and ready for interpretation.
It is separate mainly due to facilitating the visual resources.
This file becomes outdated since it is no longer used for plot.
For the plots look at the file interpretability plots

## interpretability plots
This file compiles several plots to provide interpretability

### Data preparation and emotion extraction

- **`Thesis_twitter.ipynb`**  
  Explores the Twitter dataset, retrieves song metadata, and tests several sentiment, emotion, and VAD models.

- **`Sentiment_models.ipynb`**  
  Applies sentiment analysis, GoEmotions, and VAD models to song lyrics at sentence and song level.

- **`VA_tweets.ipynb`**  
  Prepares the tweet data and generates emotion-related features for comparison with lyrics.

- **`tweets_vs_lyrics.ipynb`**  
  applies the VAD model to tweets and combines tweet-level and lyric-level results.

- **`Go_tweets.ipynb`**  
  Generates categorical emotion scores for tweets.

- **`NRC-VAD.ipynb`**  
  explores lexicon-based VAD scoring with the NRC-VAD lexicon.

### Statistical analysis and visualization

- **`plot-go-emotions.ipynb`**  
  compares categorical emotion scores from tweets and lyrics and evaluates their associations with VAD features.

- **`VAD_analysis_SHAP.ipynb`**  
  investigates group differences, tweet–lyric relationships, predictive performance, participant-level validation, and SHAP-based feature interpretation.

- **`Interpretability.ipynb`**, **`Interpretability2.ipynb`**, and **`interpretability3.ipynb`**  
  contain visual analyses of emotion distributions, VAD trajectories, group differences, and derived trajectory features.

- **`Thesis_twitter_plots.ipynb`**  
  contains earlier plots and is retained for reference. The newer interpretability notebooks contain the current visual analyses.

### Audio and auxiliary experiments

- **`DEAM model.ipynb`**  
  trains and evaluates a baseline convolutional neural network for predicting valence and arousal from audio using the DEAM dataset.

- **`FMA_analysis.ipynb`**  
  retrieves lyrics for the FMA dataset and explores relationships among lyrics, audio, and the Twitter-derived data.

- **`Deezer test.ipynb`**  
  explores the Deezer API and the availability of preview audio.

- **`Filipa-model.ipynb`** and **`test_filipa_model.ipynb`**  
  contain model-training and evaluation experiments.

## Data and Privacy

Some source data may contain sensitive or restricted information. Access to the original Twitter-derived datasets is therefore not necessarily included in this repository.

Processed files should be interpreted in accordance with the permissions, licenses, and ethical requirements of their original datasets. Personally identifying information should not be published.

## Interpretation Notes

The analyses examine statistical associations and should not be interpreted as evidence of causation or as a clinical diagnostic system.

Participant-level or author-grouped validation should be preferred when evaluating generalization. Row-level validation can produce overly optimistic estimates when multiple observations from the same participant appear in both training and validation data.

## Repository Status

This repository contains research code developed iteratively during the thesis. Some notebooks are exploratory, and paths or execution order may require adjustment before the analyses can be reproduced in a new environment.