# Contributing

Open an issue before changing label IDs, temporal boundaries, or class names. Dataset corrections must include the affected recording IDs, evidence for the correction, and regenerated aggregate files.

Before submitting a pull request, run:

```bash
python tools/validation/validate_release.py
python -m unittest discover -s tools/validation/tests
```

Do not commit recorded RGB frames, IMU CSV files, generated videos, personal data, or access credentials. Do not silently replace an existing released data archive; publish corrections under a new version.
