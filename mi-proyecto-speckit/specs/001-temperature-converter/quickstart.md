# Quickstart Validation Guide: Temperature Unit Converter

**Feature**: Temperature Unit Converter (`001-temperature-converter`)  
**Purpose**: Runnable end-to-end validation scenarios proving the feature satisfies all acceptance criteria.

---

## Prerequisites

1. **Python `>= 3.12`**
2. **`uv` installed**
3. Verify environment from repository root:
   ```bash
   uv sync
   ```

---

## 1. Automated Test Execution

Run the complete test suite with `pytest`:

```bash
uv run pytest
```

Expected Outcome:
- All unit, boundary, and CLI tests pass without errors (`100% passed`).

---

## 2. CLI Validation Scenarios

### Scenario 1: Celsius to Fahrenheit (Acceptance Criteria 1)
```bash
uv run python -m temperature_converter.cli 100 C F
```
**Expected stdout**: `212.00 F` (Exit code: `0`)

```bash
uv run python -m temperature_converter.cli -40 C F
```
**Expected stdout**: `-40.00 F` (Exit code: `0`)

---

### Scenario 2: Fahrenheit to Celsius (Acceptance Criteria 1)
```bash
uv run python -m temperature_converter.cli 32 F C
```
**Expected stdout**: `0.00 C` (Exit code: `0`)

---

### Scenario 3: Celsius to Kelvin (Acceptance Criteria 2)
```bash
uv run python -m temperature_converter.cli 0 C K
```
**Expected stdout**: `273.15 K` (Exit code: `0`)

```bash
uv run python -m temperature_converter.cli 25 C K
```
**Expected stdout**: `298.15 K` (Exit code: `0`)

---

### Scenario 4: Kelvin to Celsius (Acceptance Criteria 2)
```bash
uv run python -m temperature_converter.cli 373.15 K C
```
**Expected stdout**: `100.00 C` (Exit code: `0`)

---

### Scenario 5: Rounding to 2 Decimal Places (Acceptance Criteria 3)
```bash
uv run python -m temperature_converter.cli 100 F C
```
**Expected stdout**: `37.78 C` (Exit code: `0`)

---

### Scenario 6: Rejection of Kelvin Below 0 (Acceptance Criteria 4)
```bash
uv run python -m temperature_converter.cli -1 K C
```
**Expected stderr**: `Error: Temperature -1.00 K is below absolute zero.`  
**Expected Exit Code**: `1`

---

## 3. Python Library Validation Scenario

Run an interactive Python verification:

```bash
uv run python -c "from temperature_converter import convert; print(convert(100, 'C', 'F').formatted)"
```
**Expected stdout**: `212.00 F`
