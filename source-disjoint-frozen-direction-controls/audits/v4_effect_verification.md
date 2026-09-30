# Independent verification of the complete V4 effects

Reviewed 2026-09-30 after the separately recorded numerical-quality clearance in `v4_numerical_adequacy.md`. The numerical judgment was made before comparative effects were inspected and is not revised here on the basis of effect signs.

**Verification result:** all six models' reported rates, paired contrasts, error partitions and source-bootstrap intervals reproduce independently from the archived prediction records. The supported finding is a model-dependent effect of a shared frozen axis on support-label selection, relative to the declared approximate magnitude control.

## Provenance and independent calculation

- Aggregate SHA-256: `ea2f888fdcb227b1b6445f29eabc636bb06c054b1dfd8a1da18c04499f29bac2`
- Aggregator SHA-256: `2e6fddf25460e0deba060f3db408e17be57734be7707831d69bd57c7d77d95ea`
- Runner SHA-256: `b1d31766484e4842d7ac8f087212470879e1df5acefc96e4e34c7612e9f3271f`
- Protocol SHA-256: `2555a933125a46fe7c8d74405c63326e9654c4000a420d366032706036e7d1a7`
- Independent checks SHA-256: `2a576bba2843f19fed0cf2b7693e1a0127b20efc7857a3aac2e5d495a011e667`

The per-prompt files match both the numerical-stage hashes and the aggregate's input hashes. For every model, I verified 800 unique evaluation prompts, 200 source clusters and four variants per source. I reconstructed correctness and error classes directly from predicted A–F pairs and gold-label sets, checked the saved categories and gold-hit counts, and independently verified the fixed random seeds.

The bootstrap was reimplemented without calling the aggregation functions. It uses integer per-source counts, an explicit matrix of source-resampling multiplicities, and the declared 20,000 draws with seed 29911. Random error counts are divided by three only when computing rates. All retained source clusters, including those with no baseline-correct variants, remain in the resampling frame. Conditional denominators are recomputed in every draw. Every point estimate and confidence interval agrees with the archived aggregate to numerical precision; the largest absolute discrepancy is below `1e-16`.

The independent results, raw counts, per-model record hashes and sensitivity checks are in `reviews/v4_effect_independent_checks.json`.

## All-six primary result

Rates and differences below are fractions, not percentages. Random is the mean over the three fixed random-displacement replicates. Intervals are paired, source-clustered, per-model 95% intervals conditional on the fitted axis and recorded seeds.

| Model | Baseline-correct n | PC1 destruction | Mean random destruction | Difference [95% CI] |
| --- | ---: | ---: | ---: | ---: |
| Llama-3B | 217 | 0.02765 | 0.01382 | 0.01382 [−0.00859, 0.03763] |
| Llama-8B | 401 | 0.37905 | 0.06068 | 0.31837 [0.24027, 0.39822] |
| Qwen-7B | 521 | 0.10557 | 0.00576 | 0.09981 [0.05838, 0.14646] |
| Qwen-14B | 636 | 0.07075 | 0.01782 | 0.05294 [0.02281, 0.08631] |
| Mistral-7B | 287 | 0.01394 | 0.02207 | −0.00813 [−0.02767, 0.01282] |
| Mistral-12B | 458 | 0.09389 | 0.02984 | 0.06405 [0.02690, 0.10538] |

Four per-model intervals lie above zero. Llama-3B and Mistral-7B are inconclusive under this comparison. Mistral-7B has a slightly negative point estimate, but its interval does not establish a negative effect or equivalence. These two cells must remain visible alongside the four positive contrasts. The intervals are not simultaneous six-model guarantees.

The supportable result is that projection removal along one axis fitted on different source questions produces greater destruction than the specified approximate-magnitude random comparator in four of six models. It does not establish a common positive effect for every model or every member of a model family.

## Error types

The four positive destruction contrasts also have positive intervals for distinct incorrect pairs. Llama-8B, Qwen-14B and Mistral-12B have no repeated-label failures in either intervention condition on the baseline-correct cohort. Qwen-7B has 55 PC1 failures: 46 distinct incorrect pairs and 9 repeated labels. Its distinct-pair excess is 0.08253 [0.04686, 0.12403], so its positive effect does not depend on counting repeated labels.

The phrase “only Qwen-7B has repeated labels” needs the intervention-cohort qualification: Mistral-7B has two repeated-label outputs at baseline, which are outside the baseline-correct analysis. The new result shows effects extending beyond repeated-label failures; it does not prove that all remaining errors are uniquely semantic or that general sequence/decision disruption has been excluded.

Most distinct PC1 errors still contain one gold label. The new breakdown supports a change in which pair is selected, not a claim that removal destroys all evidence information. Keep the denominator as all baseline-correct prompts rather than only the subset of failures.

## Prespecified numerical sensitivity

Both flagged Qwen-14B random rollouts are observed correct. Setting both to destroyed gives the worst-case lower contrast; setting both to correct gives the upper contrast, which equals the observed value. Independent reconstruction gives:

- Lower endpoint: 0.0518867925, with 95% interval [0.0217619060, 0.0854700855].
- Upper endpoint: 0.0529350105, with 95% interval [0.0228095349, 0.0863053731].
- Reassignment-range width: 0.0010482180, exactly `2/(3 × 636)`.

The lower-endpoint interval remains above zero. Therefore the Qwen-14B positive contrast survives arbitrary reassignment of the two original-bound-violating random outcomes under the predeclared analysis. This is not a bound on an ideal exact-norm intervention or on all numerical discrepancies. The other five models have no such flagged rollouts, so their reassignment endpoints coincide with their observed contrasts and intervals.

The generated sensitivity table contains the point range and lower-endpoint interval; the final paper or supplement should additionally show the upper-endpoint interval as required by the protocol. Both are already available in the aggregate.

## Interpretation appropriate for the manuscript

Suggested result wording:

> Removing the frozen direction increased support-selection errors relative to random displacements targeting the same edit magnitude in four of six models. The positive contrasts also held for distinct incorrect label pairs. The comparison was inconclusive for Llama-3B and Mistral-7B, indicating that the effect of a shared axis varies across models.

Keep this experiment separate from the primary prompt-specific PC1 intervention: pooling fitting sources changes the axis, so the rates are not a direct replication or a matched estimate of how much of the local effect transfers. Source-question IDs are disjoint for fitting and evaluation, but these are previously studied sources and historical writer windows, not an untouched benchmark or a wholly label-independent research pipeline.

The intervention acts on complete attention outputs, and its outcome is restricted support-label selection conditional on baseline correctness. It does not by itself identify a uniquely evidence-semantic mechanism, establish sufficiency of the axis, or demonstrate free-form answer faithfulness. The new evidence nevertheless addresses two concrete uncertainties missing from the earlier local result: whether a fixed axis can affect different source questions and whether that effect exceeds this approximately matched edit-size comparator.

No manuscript acceptance judgment is made until the integrated text, tables and claim boundaries are reviewed together.
