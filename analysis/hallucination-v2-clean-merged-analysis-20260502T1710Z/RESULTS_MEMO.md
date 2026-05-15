# Hallucination Prompt-Structure Results

Score root: `scored/hallucination-v2-clean-merged-scoring-20260502T1705Z`
Source dataset: `runs/hallucination-v2-clean-merged-20260502T1648Z`

Boundary: API providers are the primary result. Qwen is degraded/sensitivity evidence because 35/50 Qwen rows remain capped after rerun.

## API Primary Condition Rates

| Condition | Positive | N | Rate |
|---|---:|---:|---:|
| false_anchor_forced | 14 | 60 | 0.233 |
| false_anchor_plain | 5 | 30 | 0.167 |
| open_structure_control | 0 | 30 | 0.000 |
| true_premise_control | 0 | 30 | 0.000 |

## API Primary Thresholds

- Forced minus true-premise control: `0.233`
- Forced minus open-structure control: `0.233`
- Forced minus plain false-anchor: `0.067`
- Primary threshold met: `False`
- Mode-accelerant threshold met: `False`

## New-Anchors-Only API Condition Rates

| Condition | Positive | N | Rate |
|---|---:|---:|---:|
| false_anchor_forced | 12 | 54 | 0.222 |
| false_anchor_plain | 5 | 24 | 0.208 |
| open_structure_control | 0 | 30 | 0.000 |
| true_premise_control | 0 | 30 | 0.000 |

## New-Anchors-Only API Thresholds

- Forced minus true-premise control: `0.222`
- Forced minus open-structure control: `0.222`
- Forced minus plain false-anchor: `0.014`
- Primary threshold met: `False`
- Mode-accelerant threshold met: `False`

## All Providers Sensitivity

| Condition | Positive | N | Rate |
|---|---:|---:|---:|
| false_anchor_forced | 15 | 80 | 0.188 |
| false_anchor_plain | 5 | 40 | 0.125 |
| open_structure_control | 0 | 40 | 0.000 |
| true_premise_control | 0 | 40 | 0.000 |

## All Uncapped Sensitivity

| Condition | Positive | N | Rate |
|---|---:|---:|---:|
| false_anchor_forced | 14 | 60 | 0.233 |
| false_anchor_plain | 5 | 30 | 0.167 |
| open_structure_control | 0 | 39 | 0.000 |
| true_premise_control | 0 | 36 | 0.000 |

## Qwen Degraded Cell

| Condition | Positive | N | Rate |
|---|---:|---:|---:|
| false_anchor_forced | 1 | 20 | 0.050 |
| false_anchor_plain | 0 | 10 | 0.000 |
| open_structure_control | 0 | 10 | 0.000 |
| true_premise_control | 0 | 10 | 0.000 |

## Per-Provider API Rates

| Provider | Condition | Positive | N | Rate |
|---|---|---:|---:|---:|
| anthropic | false_anchor_forced | 0 | 20 | 0.000 |
| anthropic | false_anchor_plain | 0 | 10 | 0.000 |
| anthropic | open_structure_control | 0 | 10 | 0.000 |
| anthropic | true_premise_control | 0 | 10 | 0.000 |
| openai | false_anchor_forced | 12 | 20 | 0.600 |
| openai | false_anchor_plain | 3 | 10 | 0.300 |
| openai | open_structure_control | 0 | 10 | 0.000 |
| openai | true_premise_control | 0 | 10 | 0.000 |
| xai | false_anchor_forced | 2 | 20 | 0.100 |
| xai | false_anchor_plain | 2 | 10 | 0.200 |
| xai | open_structure_control | 0 | 10 | 0.000 |
| xai | true_premise_control | 0 | 10 | 0.000 |

## Tell-Word / Structural Pattern Check

| Pattern | Positive docs | Negative docs |
|---|---:|---:|
| the study | 5 | 3 |
| the directive | 1 | 1 |
| the report | 1 | 2 |
| the finding | 2 | 0 |
| the trial | 1 | 4 |
| the memorandum | 4 | 0 |
| according to the | 0 | 0 |
| supporting evidence | 1 | 2 |
| certainty_score | 0 | 0 |
| confidence | 3 | 10 |

Top positive-associated tokens, API only:

andrew, executive-led, feasibility, suggested, amid, behaviors, cas14b, centralization, cleave, compact, complement, copies, detectable, diversity, drafted, emphasis, encourages, engineered, eventual, exposed

## Claims Still Not Allowed

- Do not claim final publication-grade rates until scoring is independently audited.
- Do not make a headline four-provider pooled claim; Qwen is degraded.
- Do not claim the prompt structure is causal beyond this controlled association.
- Do not claim tell-words generalize beyond this corpus without a held-out replication.
