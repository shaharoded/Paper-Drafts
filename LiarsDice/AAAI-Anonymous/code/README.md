# Anonymous code supplement

Source-only snapshot accompanying the anonymous Liar's Dice paper.

- `liars_dice/`: game engine, agent implementations, training utilities, and persistence.
- `scripts/`: training, simulation, and evaluation source code.
- `tests/`: unit tests.
- `NOTEBOOKS.md`: notebook inventory only.

No trained weights, checkpoints, datasets, recorded matches, evaluation results, plots, notebook cells/outputs, UI assets, Git history, or original repository README are included.

Use Python 3.10+ and install `python -m pip install -r requirements.txt`. Dependencies are unpinned; this is not an exact environment lockfile.
Run engine tests with `python -m unittest discover -s tests -v`.
Training entry points (from this directory):

```
python scripts/train_nash_cfr_agent.py --help
python scripts/train_ppo_curriculum.py --help
python scripts/train_adaptive_agent.py --help
```

Learned agents require locally trained weights at the paths configured in the modules. Their inference and evaluations cannot run from this source-only archive until those artifacts are generated. LLM opponents require an API key supplied through the environment. No credentials are included.
