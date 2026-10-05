import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from oxygenator_model import OxygenatorParams, simulate


def flow_sweep():
    flows = np.linspace(0.5, 7.0, 40)
    rows = []

    for q in flows:
        p = OxygenatorParams(blood_flow_l_min=float(q))
        r = simulate(p)
        rows.append(r)

    df = pd.DataFrame(rows)
    df.to_csv("flow_sweep_results.csv", index=False)

    plt.figure(figsize=(7, 4.5))
    plt.plot(df["blood_flow_l_min"], df["pressure_drop_mmHg"])
    plt.xlabel("Blood flow [L/min]")
    plt.ylabel("Pressure drop [mmHg]")
    plt.title("Predicted Oxygenator Pressure Drop")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig("pressure_drop_vs_flow.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    plt.plot(df["blood_flow_l_min"], df["o2_transfer_ml_min"])
    plt.xlabel("Blood flow [L/min]")
    plt.ylabel("O2 transfer [mL/min]")
    plt.title("Reduced-Order O2 Transfer vs Blood Flow")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig("o2_transfer_vs_flow.png", dpi=180)
    plt.close()

    return df


def sensitivity_sweep():
    flows = [2.0, 3.5, 5.0, 6.5]
    hbs = [8.0, 10.0, 12.0, 14.0]
    areas = [1.0, 1.5, 2.0, 2.5]

    rows = []
    for q in flows:
        for hb in hbs:
            for area in areas:
                p = OxygenatorParams(
                    blood_flow_l_min=q,
                    hb_g_dl=hb,
                    effective_area_m2=area,
                )
                r = simulate(p)
                rows.append({
                    "blood_flow_l_min": q,
                    "hb_g_dl": hb,
                    "effective_area_m2": area,
                    "o2_transfer_ml_min": r["o2_transfer_ml_min"],
                    "pressure_drop_mmHg": r["pressure_drop_mmHg"],
                    "effectiveness": r["transfer_effectiveness"],
                })

    df = pd.DataFrame(rows)
    df.to_csv("sensitivity_results.csv", index=False)
    return df


if __name__ == "__main__":
    flow_df = flow_sweep()
    sens_df = sensitivity_sweep()

    print("\nFlow sweep:")
    print(flow_df.round(3).to_string(index=False))
    print("\nSaved:")
    print("  flow_sweep_results.csv")
    print("  sensitivity_results.csv")
    print("  pressure_drop_vs_flow.png")
    print("  o2_transfer_vs_flow.png")
