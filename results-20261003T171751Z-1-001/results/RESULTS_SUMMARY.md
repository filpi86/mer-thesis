# Seven-category comparison results

The original seven-category vocabulary is preserved. The Hartmann checkpoint is not reproduced: a GoEmotions-trained MiniLM embedding classifier is used because raw target tweets are unavailable.

Paired sample: 4,256 participants, 6,345,978 tweets and 47,204 participant-song records.
Source model: selected C=1.0; official mapped GoEmotions test n=5,427.
Source test cross-entropy: 1.0696; baseline: 1.5360.

## Classification (fold mean AUROC +/- fold standard deviation)
- LR VAD_and_categories (20 features): 0.722 +/- 0.020; balanced accuracy 0.662.
- RF VAD_and_categories (20 features): 0.732 +/- 0.023; balanced accuracy 0.556.
- LR VAD_both (6 features): 0.641 +/- 0.021; balanced accuracy 0.601.
- RF VAD_both (6 features): 0.638 +/- 0.014; balanced accuracy 0.515.
- LR category_both (14 features): 0.721 +/- 0.016; balanced accuracy 0.658.
- RF category_both (14 features): 0.726 +/- 0.019; balanced accuracy 0.555.
- LR category_lyrics (7 features): 0.590 +/- 0.016; balanced accuracy 0.572.
- RF category_lyrics (7 features): 0.545 +/- 0.019; balanced accuracy 0.505.
- LR category_tweets (7 features): 0.716 +/- 0.015; balanced accuracy 0.651.
- RF category_tweets (7 features): 0.707 +/- 0.009; balanced accuracy 0.557.

## Interpretation

All new target results are exploratory. Separate BH families do not give an overall thesis-wide FDR. The paired OOF intervals are unadjusted and conditional on fixed predictions.
GoEmotions source errors do not validate tweet or lyric accuracy. Correlations between category scores and VAD are agreement between predictions, not independent human-rated validation.
Feature counts and scoring objectives differ. Internal depression/control label discrimination is not clinical diagnostic validity. Categorical results have not undergone the complete VAD sensitivity battery.
Original biography coefficients are historical and cannot be directly interpreted as a controlled baseline for the timeline analysis.

## Reproduction

Keep this notebook and the input bundle. The input and model manifests record hashes, splits, package versions, mappings, settings and the frozen encoder revision. Drive checkpoints resume source encoding and completed tweet files.
