from dataclasses import dataclass
import math


@dataclass
class OxygenatorParams:
    # Blood / gas conditions
    hb_g_dl: float = 12.0
    inlet_po2_mmHg: float = 45.0
    gas_po2_mmHg: float = 713.0   # approximate dry O2 partial pressure at 1 atm
    blood_flow_l_min: float = 4.0

    # Reduced-order oxygenator parameters
    effective_area_m2: float = 1.8
    mass_transfer_coeff: float = 0.055  # tunable reduced-order coefficient
    pressure_k1: float = 9.0            # mmHg/(L/min)
    pressure_k2: float = 1.1            # mmHg/(L/min)^2


def hill_saturation(po2_mmHg: float, p50: float = 26.8, n: float = 2.7) -> float:
    """Oxygen saturation (0..1) using a Hill approximation."""
    po2 = max(float(po2_mmHg), 0.0)
    return po2**n / (p50**n + po2**n)


def oxygen_content_ml_dl(po2_mmHg: float, hb_g_dl: float) -> float:
    """
    Approximate blood oxygen content:
    C_O2 = 1.34*Hb*SaO2 + 0.0031*PO2 [mL O2/dL blood]
    """
    sat = hill_saturation(po2_mmHg)
    return 1.34 * hb_g_dl * sat + 0.0031 * po2_mmHg


def pressure_drop_mmHg(flow_l_min: float, k1: float, k2: float) -> float:
    """Empirical reduced-order pressure loss curve."""
    q = max(float(flow_l_min), 0.0)
    return k1 * q + k2 * q * q


def transfer_effectiveness(flow_l_min: float, area_m2: float, k_mass: float) -> float:
    """
    NTU-style reduced-order effectiveness.
    Higher membrane area / transfer coefficient increases effectiveness;
    increasing blood flow reduces residence time.
    """
    q = max(float(flow_l_min), 1e-6)
    ntu = max(k_mass, 0.0) * max(area_m2, 0.0) / q
    return 1.0 - math.exp(-ntu)


def simulate(params: OxygenatorParams) -> dict:
    q = max(params.blood_flow_l_min, 1e-6)

    cin = oxygen_content_ml_dl(params.inlet_po2_mmHg, params.hb_g_dl)
    c_equilibrium = oxygen_content_ml_dl(params.gas_po2_mmHg, params.hb_g_dl)

    eps = transfer_effectiveness(q, params.effective_area_m2, params.mass_transfer_coeff)
    cout = cin + eps * (c_equilibrium - cin)

    # Convert blood flow L/min -> dL/min (x10)
    o2_transfer_ml_min = (cout - cin) * q * 10.0

    dp = pressure_drop_mmHg(q, params.pressure_k1, params.pressure_k2)

    return {
        "blood_flow_l_min": q,
        "inlet_o2_content_ml_dl": cin,
        "equilibrium_o2_content_ml_dl": c_equilibrium,
        "outlet_o2_content_ml_dl": cout,
        "transfer_effectiveness": eps,
        "o2_transfer_ml_min": o2_transfer_ml_min,
        "pressure_drop_mmHg": dp,
    }


if __name__ == "__main__":
    result = simulate(OxygenatorParams())
    for key, value in result.items():
        print(f"{key}: {value:.3f}")
