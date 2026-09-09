# Accel-verl integration

The standalone augmenter does not depend on Accel-verl. In the dissertation
experiments, the same implementation lived under `verl_accel/` and was called by the
existing `PromptAugmenter` immediately after Reasoning Gym generated a question.

To reproduce that connection in another Accel-verl checkout:

1. Install this package in the training environment.
2. Import `DecimalSubproblemAugmenter` in `verl_accel/prompt_augment.py`.
3. Construct it with the shared seeded `random.Random` instance used by
   `PromptAugmenter`.
4. Dispatch `mode=subproblem` to
   `augmenter.augment(question, task_name=task_name)`.
5. Add the following configuration below `data.accel.prompt_augmentation`:

```yaml
mode: subproblem
probability: 0.5
seed: 42
subproblem:
  task_names: [decimal_arithmetic]
  variables: [x, y, d, q, r]
  renderer_source: mixed
  renderer_bank_path: data/decimal_subproblem_wordings.json
  offline_probability: 0.5
  allow_unreviewed_renderer_bank: false
  two_step_probability: 0.25
  two_subproblem_probability: 0.15
```

The outer `probability` is handled by Accel-verl's `PromptAugmenter`; the standalone
class controls only the structure and wording after augmentation has been selected.

The clean-curriculum-scoring intervention is conceptually separate from this package.
All prompts contribute to the policy update, but augmented rows are filtered before
updating level regret and other curriculum-controller statistics.

