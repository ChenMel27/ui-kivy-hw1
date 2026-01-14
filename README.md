# Demographics Form – HW1

## Student Information
- **Full name:** Melanie Chen
- **Email:** mchen658@gatech.edu
- **GT SSO:** 903901190

## Homework Overview
Kivy application that collects demographics information (name, age range, gender selections, and phone number) using density-independent measurements so the UI renders consistently at 400×500 dp. The extra-credit workflow adds a landing screen with a list of entries and a + button; Submit saves into the list (creating or updating), prints the dictionary payload for grading, and returns to the list, while Cancel backs out without saving.

## How to Run
```bash
python3 main.py
```

Dependencies:
- Python 3.11+
- Kivy 2.3.0
- `kivy_config_helper` supplied in course resources (optional; fallback shim exists in `main.py`).

## Validation Notes
- Name inputs filter to `A-Z`, spaces, `'`, and `-`, and require non-empty first/last names.
- Age spinner is initially unset and must match one of the predefined ranges.
- Gender group uses multi-select checkboxes; at least one must be checked.
- Phone input accepts digits plus formatting characters, enforces 10 digits, and formats to `(555) 555-5555` on blur.

## Extra Credit Status
- Extra credit list view workflow implemented? **Yes** (ScreenManager with add/edit list view)

## Known Issues / Notes for Grader
- None; all rubric requirements implemented.

## Build / Environment Notes
- Tested on macOS Sonoma 14 with Python 3.12.
- No additional build steps beyond installing dependencies.