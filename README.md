# Membrane Oxygenator Performance Simulator

A laptop-based biomedical engineering portfolio project for studying the
performance of a hollow-fiber membrane oxygenator using a reduced-order
mathematical model.

## Project goal

The project explores how selected operating and design variables influence:

- oxygen-transfer performance,
- oxygen content of blood,
- pressure drop across the oxygenator,
- transfer effectiveness,
- sensitivity to blood flow, hemoglobin concentration, and effective membrane area.

The software is designed as an **engineering / educational model** and not as
a clinical prediction or decision-support system.

## Why this project matters

Membrane oxygenators combine fluid mechanics, blood-gas transport, biomaterials,
and medical-device engineering. Their performance depends on the interaction
between blood flow, membrane geometry, mass transfer, and hydraulic resistance.

This project demonstrates the ability to translate biomedical literature and
engineering equations into a reproducible computational tool.

## Model structure

### 1. Oxygen saturation

A Hill-type approximation is used:

SaO2 = PO2^n / (P50^n + PO2^n)

### 2. Blood oxygen content

C_O2 = 1.34 × Hb × SaO2 + 0.0031 × PO2

with oxygen content expressed approximately in mL O2/dL blood.

### 3. Reduced-order gas-transfer effectiveness

An NTU-style relationship is used:

epsilon = 1 - exp(-kA / Q)

where:

- k = reduced mass-transfer coefficient,
- A = effective membrane area,
- Q = blood flow.

The outlet oxygen content is estimated as:

C_out = C_in + epsilon × (C_eq - C_in)

and oxygen transfer is calculated from the blood-flow rate and content difference.

### 4. Pressure drop

A reduced empirical relationship is used:

DeltaP = k1 × Q + k2 × Q²

This captures the increasing hydraulic resistance with increasing flow while
remaining computationally simple.

## Repository structure

- `oxygenator_model.py` — core mathematical model
- `run_analysis.py` — flow sweep and sensitivity analysis
- `app.py` — interactive Streamlit dashboard
- `requirements.txt` — Python dependencies

## Run locally

Create a virtual environment if desired, then install dependencies:

```bash
pip install -r requirements.txt
```

Run the engineering analysis:

```bash
python run_analysis.py
```

Run the interactive dashboard:

```bash
streamlit run app.py
```

## Portfolio outputs

The analysis generates:

- `flow_sweep_results.csv`
- `sensitivity_results.csv`
- `pressure_drop_vs_flow.png`
- `o2_transfer_vs_flow.png`

These results can be used in the technical report and GitHub documentation.

## Current limitations

This is intentionally a reduced-order model.

It does **not** currently include:

- patient-specific physiology,
- recirculation,
- detailed CO2 transport,
- Bohr/Haldane coupling,
- non-Newtonian blood rheology,
- local shear stress,
- thrombosis prediction,
- detailed hollow-fiber geometry,
- 3D CFD,
- experimental calibration against a commercial oxygenator.

Therefore numerical values should not be interpreted as validated clinical
predictions.

## Planned development

### Phase 2
- calibrate pressure-drop coefficients against published/device data,
- add CO2-transfer modeling,
- improve gas-transfer parameterization,
- add parameter-sensitivity ranking.

### Phase 3
- add Monte Carlo uncertainty analysis,
- compare multiple hypothetical oxygenator designs,
- generate automated engineering reports.

### Phase 4
- optional CFD extension using a porous-media representation of the fiber bundle.

## CV-ready project title

**Computational Modeling and Performance Analysis of a Membrane Oxygenator**

Suggested description after the project is completed and validated:

> Developed a Python-based reduced-order simulation of a hollow-fiber membrane
> oxygenator to investigate oxygen transfer, hydraulic pressure loss, and the
> influence of blood-flow and design parameters; implemented sensitivity analysis,
> data visualization, and an interactive Streamlit dashboard.

## Disclaimer

For educational and engineering portfolio use only. Not intended for clinical
diagnosis, therapy, device control, or patient-specific prediction.
