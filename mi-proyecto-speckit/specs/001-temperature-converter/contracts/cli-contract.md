# Interface Contract: Command-Line Interface (CLI)

**Command Name**: `temp-conv` (or `python -m temperature_converter.cli`)  
**Feature**: Temperature Unit Converter (`001-temperature-converter`)  

---

## 1. Syntax & Arguments

```text
temp-conv <value> <from_unit> <to_unit> [options]
temp-conv <value> --from <from_unit> --to <to_unit> [options]
```

### 1.1 Positional Arguments
- `value`: Numeric temperature value (e.g. `100`, `32.5`, `-40`).
- `from_unit`: (Optional if `--from` is passed) Source scale (`C`, `F`, `K`, `celsius`, etc.).
- `to_unit`: (Optional if `--to` is passed) Destination scale (`C`, `F`, `K`, `celsius`, etc.).

### 1.2 Options
- `--from, -f <unit>`: Source temperature scale.
- `--to, -t <unit>`: Target destination scale.
- `--quiet, -q`: Output only the numeric result rounded to 2 decimal places (e.g. `212.00`).
- `--json`: Output full structured JSON response.
- `--help, -h`: Display usage guidelines and exit.

---

## 2. Standard Output & Error Conventions

### 2.1 Standard Output (`stdout`)
- **Default Format**: `<rounded_value> <target_unit>`
  - Example: `temp-conv 100 C F` -> `212.00 F`
- **Quiet Mode (`-q`)**: `<rounded_value>`
  - Example: `temp-conv 100 C F -q` -> `212.00`
- **JSON Mode (`--json`)**:
  ```json
  {
    "source": { "value": 100.0, "unit": "C" },
    "target_unit": "F",
    "value": 212.0,
    "formatted": "212.00 F"
  }
  ```

### 2.2 Standard Error (`stderr`)
Errors are output to `stderr` with a descriptive prefix:
- Domain error example:
  ```text
  Error: Temperature -5.00 K is below absolute zero (0.00 K).
  ```
- Unrecognized unit example:
  ```text
  Error: Unrecognized unit 'X'. Valid units: C, F, K.
  ```

---

## 3. Exit Codes

| Exit Code | Meaning | Example Condition |
|-----------|---------|-------------------|
| `0`       | Success | Successful conversion executed |
| `1`       | Domain / Validation Error | Input below absolute zero ($K < 0$), invalid unit string |
| `2`       | CLI Usage Error | Missing required arguments, non-numeric value passed |
