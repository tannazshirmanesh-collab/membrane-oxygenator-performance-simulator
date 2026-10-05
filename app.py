import streamlit as st
import pandas as pd
import numpy as np

from oxygenator_model import OxygenatorParams, simulate

st.set_page_config(
    page_title="Membrane Oxygenator Performance Simulator",
    layout="wide"
)

st.title("Membrane Oxygenator Performance Simulator")
st.caption(
    "Educational reduced-order engineering model for portfolio/research use. "
    "Not a clinical decision-support tool."
)

with st.sidebar:
    st.header("Model inputs")
    flow = st.slider("Blood flow [L/min]", 0.5, 7.0, 4.0, 0.1)
    hb = st.slider("Hemoglobin [g/dL]", 6.0, 18.0, 12.0, 0.5)
    inlet_po2 = st.slider("Inlet PO₂ [mmHg]", 20.0, 100.0, 45.0, 1.0)
    area = st.slider("Effective membrane area [m²]", 0.5, 3.0, 1.8, 0.1)
    km = st.slider("Reduced mass-transfer coefficient", 0.01, 0.20, 0.055, 0.005)

params = OxygenatorParams(
    hb_g_dl=hb,
    inlet_po2_mmHg=inlet_po2,
    blood_flow_l_min=flow,
    effective_area_m2=area,
    mass_transfer_coeff=km,
)
result = simulate(params)

c1, c2, c3 = st.columns(3)
c1.metric("Pressure drop", f"{result['pressure_drop_mmHg']:.1f} mmHg")
c2.metric("O₂ transfer", f"{result['o2_transfer_ml_min']:.1f} mL/min")
c3.metric("Transfer effectiveness", f"{100*result['transfer_effectiveness']:.1f}%")

st.subheader("Flow-response analysis")
flows = np.linspace(0.5, 7.0, 60)
rows = []

for q in flows:
    p = OxygenatorParams(
        hb_g_dl=hb,
        inlet_po2_mmHg=inlet_po2,
        blood_flow_l_min=float(q),
        effective_area_m2=area,
        mass_transfer_coeff=km,
    )
    r = simulate(p)
    rows.append({
        "Blood flow [L/min]": q,
        "Pressure drop [mmHg]": r["pressure_drop_mmHg"],
        "O2 transfer [mL/min]": r["o2_transfer_ml_min"],
    })

df = pd.DataFrame(rows)

col1, col2 = st.columns(2)
with col1:
    st.line_chart(df.set_index("Blood flow [L/min]")[["Pressure drop [mmHg]"]])

with col2:
    st.line_chart(df.set_index("Blood flow [L/min]")[["O2 transfer [mL/min]"]])

st.subheader("Current operating point")
st.dataframe(
    pd.DataFrame([{
        "Flow [L/min]": result["blood_flow_l_min"],
        "Hb [g/dL]": hb,
        "Inlet O2 content [mL/dL]": result["inlet_o2_content_ml_dl"],
        "Outlet O2 content [mL/dL]": result["outlet_o2_content_ml_dl"],
        "O2 transfer [mL/min]": result["o2_transfer_ml_min"],
        "Pressure drop [mmHg]": result["pressure_drop_mmHg"],
    }]).round(3),
    use_container_width=True
)

st.warning(
    "The coefficients are illustrative model parameters and require experimental "
    "calibration/validation before quantitative interpretation."
)
