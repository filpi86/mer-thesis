# Thesis final checks

Completed all four configured checks. These are exploratory follow-ups to the primary results.

## 1. Sadness correspondence between groups
Depression rho: 0.125; control rho: 0.100.
Difference: +0.026; basic 95% CI [-0.055, 0.101]; approximate BH q across 10 differences: 0.6486.
A small positive difference is not automatically convincing evidence of a group difference. An interval containing zero leaves it uncertain; it does not establish equality.

## 2. Known music-sharing posts removed
Removed 23,383 eligible known posts. Remaining: 4,255 participants and 6,322,595 tweets.
Independent VAD reproduction error: 2.38e-07. Lyrics and saved fold IDs were retained.
Matching correlations and group effects use the same remaining people before and after removal.

LR: category-both exclusion-minus-original pooled AUROC change -0.0004, conditional 95% CI [-0.0013, 0.0004].
RF: category-both exclusion-minus-original pooled AUROC change -0.0050, conditional 95% CI [-0.0094, -0.0006].

## 3. Activity checks
Pooled sadness correspondence: raw rho 0.115; activity/group-adjusted partial rank correlation 0.098.
Adjusted correlations are descriptive, and adjusting these measured counts does not remove every source of confounding.
Separate minimum-activity cohorts change the population; their performance differences from the full sample are not paired treatment effects.

LR, emotion information beyond activity: pooled AUROC difference +0.1099, conditional 95% CI [0.0902, 0.1310].
LR, lyrics increment with activity controls: pooled AUROC difference +0.0053, conditional 95% CI [0.0005, 0.0100].
RF, emotion information beyond activity: pooled AUROC difference +0.1743, conditional 95% CI [0.1477, 0.2007].
RF, lyrics increment with activity controls: pooled AUROC difference +0.0158, conditional 95% CI [0.0053, 0.0262].

## 4. Original classification errors
LR with both category sources: sensitivity 65.3%, specificity 66.4%, precision 29.5%, balanced accuracy 65.8%.
Missed depression-labelled participants: 262; incorrectly flagged controls: 1,177.
These are disclosure-derived dataset-label errors, not clinically validated diagnostic errors.

## Interpretation limits
The emotion models are fixed; human-rated emotion accuracy on these tweets/lyrics is unknown. Known sharing-post removal cannot identify all music-related text. Participant bootstrap intervals omit shared-song/social dependence and complete retraining uncertainty. Predictive paired intervals are exploratory and unadjusted for multiple comparisons. No threshold was selected from held-out outcomes.

## Files to inspect
- analysis/group_correlation_differences.csv
- analysis/music_exclusion_audit.json and music_exclusion_correlations.csv
- analysis/activity_adjusted_correlations.csv and activity_cohort_sizes.csv
- analysis/followup_classification_summary.csv and followup_paired_comparisons.csv
- analysis/original_classification_errors.csv
- figures/: matching group differences, group scatter plots, robustness, confusion matrices and precision/recall

The thesis PDF is not modified by this notebook.
