# Implementation Tasks: Temperature Unit Converter

**Feature**: Temperature Unit Converter  
**Branch**: `001-temperature-converter`  
**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)  

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, directory structure, and packaging configuration.

- [X] T001 Configure packaging entry point `temp-conv = "temperature_converter.cli:main"` in `pyproject.toml`
- [X] T002 [P] Create source package and test directory structure in `src/temperature_converter/` and `tests/`
- [X] T003 [P] Initialize package exports in `src/temperature_converter/__init__.py` and `tests/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models, units enum, exceptions, and conversion structures that MUST exist before user stories can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T004 [P] Define `TemperatureUnit` enum with case-insensitive parsing in `src/temperature_converter/models.py`
- [X] T005 [P] Define domain exception hierarchy (`TemperatureError`, `AbsoluteZeroError`, `InvalidUnitError`, `InvalidInputError`) in `src/temperature_converter/models.py`
- [X] T006 Implement `Temperature` and `ConversionResult` value objects with 2-decimal rounding logic in `src/temperature_converter/models.py`
- [X] T007 Implement base conversion dispatcher and identity conversion logic in `src/temperature_converter/converter.py`

**Checkpoint**: Core domain models and dispatch infrastructure complete. User stories can now proceed.

---

## Phase 3: User Story 1 - Convert Between Celsius and Fahrenheit (Priority: P1) 🎯 MVP

**Goal**: Enable bidirectional conversion between Celsius and Fahrenheit scales with exact 2-decimal rounding.

**Independent Test**: Verify standard calibration points: `0.00 C` -> `32.00 F`, `100.00 C` -> `212.00 F`, `32.00 F` -> `0.00 C`, `98.60 F` -> `37.00 C`, and `-40.00 C` -> `-40.00 F`.

### Tests for User Story 1
- [ ] T008 [P] [US1] Create unit tests for Celsius <-> Fahrenheit conversions in `tests/test_converter.py`

### Implementation for User Story 1
- [ ] T009 [US1] Implement `celsius_to_fahrenheit` and `fahrenheit_to_celsius` mathematical conversion algorithms in `src/temperature_converter/converter.py`
- [ ] T010 [US1] Wire Celsius-Fahrenheit conversions into public `convert()` dispatcher in `src/temperature_converter/converter.py`
- [ ] T011 [US1] Implement CLI argument parsing and stdout formatting for C <-> F conversions in `src/temperature_converter/cli.py`

**Checkpoint**: User Story 1 is functional and independently testable as an MVP.

---

## Phase 4: User Story 2 - Convert Between Celsius and Kelvin (Priority: P2)

**Goal**: Enable bidirectional conversion between Celsius and thermodynamic Kelvin scales using the 273.15 offset.

**Independent Test**: Verify benchmark points: `0.00 C` -> `273.15 K`, `25.00 C` -> `298.15 K`, `273.15 K` -> `0.00 C`, and `373.15 K` -> `100.00 C`.

### Tests for User Story 2
- [ ] T012 [P] [US2] Create unit tests for Celsius <-> Kelvin conversions in `tests/test_converter.py`

### Implementation for User Story 2
- [ ] T013 [US2] Implement `celsius_to_kelvin` and `kelvin_to_celsius` conversion algorithms in `src/temperature_converter/converter.py`
- [ ] T014 [US2] Wire Celsius-Kelvin conversions into `convert()` dispatcher and CLI in `src/temperature_converter/converter.py`

**Checkpoint**: User Stories 1 and 2 are functional and independently testable.

---

## Phase 5: User Story 3 - Convert Between Fahrenheit and Kelvin (Priority: P3)

**Goal**: Enable direct bidirectional conversion between Fahrenheit and Kelvin without manual intermediate steps.

**Independent Test**: Verify benchmark points: `32.00 F` -> `273.15 K`, `212.00 F` -> `373.15 K`, `0.00 K` -> `-459.67 F`, and `459.67 K` -> `367.74 F`.

### Tests for User Story 3
- [ ] T015 [P] [US3] Create unit tests for Fahrenheit <-> Kelvin conversions in `tests/test_converter.py`

### Implementation for User Story 3
- [ ] T016 [US3] Implement `fahrenheit_to_kelvin` and `kelvin_to_fahrenheit` conversion algorithms in `src/temperature_converter/converter.py`
- [ ] T017 [US3] Wire Fahrenheit-Kelvin conversions into `convert()` dispatcher and CLI in `src/temperature_converter/converter.py`

**Checkpoint**: Complete conversion matrix (C, F, K) operational across all scale pairs.

---

## Phase 6: User Story 4 - Input Validation and Absolute Zero Enforcement (Priority: P4)

**Goal**: Prevent physical law violations by rejecting temperatures below absolute zero ($K < 0$, $C < -273.15$, $F < -459.67$) and invalid input formats.

**Independent Test**: Verify that Kelvin values $< 0$ raise `AbsoluteZeroError` and CLI exits with code `1` and descriptive stderr.

### Tests for User Story 4
- [ ] T018 [P] [US4] Create unit tests for absolute zero boundary conditions and invalid values in `tests/test_converter.py`
- [ ] T019 [P] [US4] Create CLI error handling, stderr message, and exit code tests in `tests/test_cli.py`

### Implementation for User Story 4
- [ ] T020 [US4] Implement absolute zero bounds validation in `Temperature` model in `src/temperature_converter/models.py`
- [ ] T021 [US4] Implement CLI error handling for domain exceptions and exit code mapping in `src/temperature_converter/cli.py`

**Checkpoint**: All domain validation rules and physical bounds enforced across API and CLI.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Command line formatting options, convenience exports, and end-to-end verification.

- [ ] T022 [P] Implement `--json` and `-q`/`--quiet` output formatting flags in `src/temperature_converter/cli.py`
- [ ] T023 [P] Add convenience shortcut functions (`celsius_to_fahrenheit`, etc.) and export them in `src/temperature_converter/__init__.py`
- [ ] T024 Execute complete test suite with `uv run pytest` across `tests/`
- [ ] T025 Execute end-to-end quickstart validation scenarios defined in `specs/001-temperature-converter/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories.
- **User Stories (Phases 3-6)**: Depend on Foundational (Phase 2).
  - Can proceed sequentially: US1 (MVP) → US2 → US3 → US4.
  - Or in parallel once Phase 2 is complete.
- **Polish (Phase 7)**: Depends on completion of desired user stories.

### Parallel Opportunities
- In Phase 1: `T002` and `T003` can execute in parallel.
- In Phase 2: `T004` and `T005` can execute in parallel.
- In User Stories: Test tasks (`T008`, `T012`, `T015`, `T018`, `T019`) can run in parallel before or alongside implementation.
- In Phase 7: `T022` and `T023` can execute in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch test and implementation tasks:
Task: "Create unit tests for Celsius <-> Fahrenheit conversions in tests/test_converter.py"
Task: "Implement celsius_to_fahrenheit and fahrenheit_to_celsius in src/temperature_converter/converter.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1 (Setup) and Phase 2 (Foundational).
2. Complete Phase 3 (User Story 1: Celsius <-> Fahrenheit).
3. Validate User Story 1 independently with `pytest` and CLI.
4. Deliver working MVP.

### Incremental Delivery
1. Foundation ready (Phases 1 & 2).
2. Deliver MVP: Celsius <-> Fahrenheit (Phase 3).
3. Expand scale: Add Kelvin support (Phase 4).
4. Complete matrix: Add Fahrenheit <-> Kelvin (Phase 5).
5. Harden domain: Add absolute zero validation & error handling (Phase 6).
6. Polish: Add CLI output modes (`--json`, `-q`) and verify quickstart (Phase 7).
