#!/usr/bin/env python3
"""
=========================================================================
Spatializing Standard Charts: End-to-End Reproducible Pipeline
=========================================================================
Lab for Spatial Informatics, IIIT Hyderabad
SDS Project, April 2026

USAGE:
    python pipeline.py --data-dir ./data/ --output-dir ./output/

INPUTS:
    data/9-State-Wise-Number-Of-Electors.xlsx
    data/24-Participation-of-Women-Candidates.xlsx
    data/Constituency_wise_Women_Candidature.xlsx

OUTPUTS:
    output/moran_results.json
    output/lisa_classifications.csv
    output/chart1_bar_vs_lisa.html        (Query 1)
    output/chart2_scatter_vs_parallel.html (Query 2)
    output/chart3_residual_confounding.html (Query 3)
    output/chart4_equity_belts.html        (Query 4)
    output/chart5_simpsons_paradox.html    (Query 5)
    output/spatial_weights_matrix.npy
    output/pipeline_report.txt

DEPENDENCIES:
    pip install pandas numpy openpyxl plotly scikit-learn
=========================================================================
"""

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# =====================================================================
# MODULE 1: DATA INGESTION
# =====================================================================

class DataIngestion:
    """Reads and harmonizes raw ECI Excel files into a unified DataFrame."""

    # Canonical state name mappings (ECI uses inconsistent naming)
    STATE_ALIASES = {
        "NCT OF Delhi": "Delhi",
        "NCT of Delhi": "Delhi",
        "Andaman & Nicobar Islands": "Andaman & Nicobar",
        "Dadra & Nagar Haveli and Daman & Diu": "Dadra & Nagar Haveli",
        "Jammu and Kashmir": "Jammu & Kashmir",
    }

    # Geographic regions for spatial disaggregation (Query 5)
    REGION_MAP = {
        "Andaman & Nicobar": "Islands", "Lakshadweep": "Islands",
        "Punjab": "North", "Haryana": "North",
        "Himachal Pradesh": "North", "Uttarakhand": "North",
        "Delhi": "North", "Jammu & Kashmir": "North",
        "Ladakh": "North", "Chandigarh": "North",
        "Rajasthan": "West", "Gujarat": "West",
        "Maharashtra": "West", "Goa": "West",
        "Karnataka": "South", "Kerala": "South",
        "Tamil Nadu": "South", "Andhra Pradesh": "South",
        "Telangana": "South", "Puducherry": "South",
        "Uttar Pradesh": "Central", "Madhya Pradesh": "Central",
        "Chhattisgarh": "Central",
        "Bihar": "East", "Jharkhand": "East",
        "West Bengal": "East", "Odisha": "East",
        "Assam": "Northeast", "Arunachal Pradesh": "Northeast",
        "Meghalaya": "Northeast", "Nagaland": "Northeast",
        "Manipur": "Northeast", "Mizoram": "Northeast",
        "Tripura": "Northeast", "Sikkim": "Northeast",
    }

    # Approximate state centroids (lat, lon) for map rendering
    CENTROIDS = {
        "Andaman & Nicobar": (11.7, 92.7),
        "Andhra Pradesh": (15.9, 79.7),
        "Arunachal Pradesh": (28.2, 94.7),
        "Assam": (26.2, 92.9),
        "Bihar": (25.1, 85.3),
        "Chandigarh": (30.7, 76.8),
        "Chhattisgarh": (21.3, 81.6),
        "Dadra & Nagar Haveli": (20.3, 73.0),
        "Delhi": (28.7, 77.1),
        "Goa": (15.4, 74.0),
        "Gujarat": (22.3, 71.2),
        "Haryana": (29.1, 76.1),
        "Himachal Pradesh": (31.1, 77.2),
        "Jammu & Kashmir": (33.8, 76.6),
        "Jharkhand": (23.6, 85.3),
        "Karnataka": (15.3, 75.7),
        "Kerala": (10.9, 76.3),
        "Ladakh": (34.2, 77.6),
        "Lakshadweep": (10.6, 72.6),
        "Madhya Pradesh": (22.9, 78.7),
        "Maharashtra": (19.8, 75.3),
        "Manipur": (24.7, 93.9),
        "Meghalaya": (25.5, 91.4),
        "Mizoram": (23.2, 92.8),
        "Nagaland": (26.2, 94.6),
        "Odisha": (20.9, 84.0),
        "Puducherry": (11.9, 79.8),
        "Punjab": (31.2, 75.3),
        "Rajasthan": (27.0, 74.2),
        "Sikkim": (27.5, 88.5),
        "Tamil Nadu": (11.1, 78.7),
        "Telangana": (18.1, 79.0),
        "Tripura": (23.9, 91.9),
        "Uttar Pradesh": (26.8, 80.9),
        "Uttarakhand": (30.1, 79.0),
        "West Bengal": (22.9, 87.9),
    }

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.df = None

    def _harmonize_state(self, name: str) -> str:
        """Resolve ECI naming inconsistencies."""
        return self.STATE_ALIASES.get(name.strip(), name.strip())

    def load_base_geography(self) -> pd.DataFrame:
        """Load state-level area and current seat allocation."""
        records = [
            ("Andaman & Nicobar", 8249, 1),
            ("Andhra Pradesh", 162975, 25),
            ("Arunachal Pradesh", 83743, 2),
            ("Assam", 78438, 14),
            ("Bihar", 94163, 40),
            ("Chandigarh", 114, 1),
            ("Chhattisgarh", 135192, 11),
            ("Dadra & Nagar Haveli", 603, 2),
            ("Goa", 3702, 2),
            ("Gujarat", 196024, 25),
            ("Haryana", 44212, 10),
            ("Himachal Pradesh", 55673, 4),
            ("Jammu & Kashmir", 55538, 5),
            ("Jharkhand", 79716, 14),
            ("Karnataka", 191791, 28),
            ("Kerala", 38863, 20),
            ("Ladakh", 59146, 1),
            ("Lakshadweep", 32, 1),
            ("Madhya Pradesh", 308252, 29),
            ("Maharashtra", 307713, 48),
            ("Manipur", 22327, 2),
            ("Meghalaya", 22429, 2),
            ("Mizoram", 21081, 1),
            ("Nagaland", 16579, 1),
            ("Delhi", 1484, 7),
            ("Odisha", 155707, 21),
            ("Puducherry", 479, 1),
            ("Punjab", 50362, 13),
            ("Rajasthan", 342239, 25),
            ("Sikkim", 7096, 1),
            ("Tamil Nadu", 130058, 39),
            ("Telangana", 112077, 17),
            ("Tripura", 10491, 2),
            ("Uttar Pradesh", 240928, 80),
            ("Uttarakhand", 53483, 5),
            ("West Bengal", 88752, 42),
        ]
        return pd.DataFrame(records, columns=["state", "area_km2", "current_seats"])

    def load_women_electorate(self) -> pd.DataFrame:
        """Parse ECI Table 9: State-Wise Number of Electors."""
        path = self.data_dir / "9-State-Wise-Number-Of-Electors.xlsx"
        raw = pd.read_excel(path, sheet_name="Table 1")
        electors = raw.iloc[4:].copy()
        electors = electors[[raw.columns[0], raw.columns[5]]]
        electors.columns = ["state", "women_voters"]
        electors = electors.dropna()
        electors["state"] = electors["state"].apply(self._harmonize_state)
        electors["women_voters"] = pd.to_numeric(
            electors["women_voters"], errors="coerce"
        )
        return electors

    def load_women_participation(self) -> pd.DataFrame:
        """Parse ECI Table 24: Participation of Women Candidates."""
        path = self.data_dir / "24-Participation-of-Women-Candidates*.xlsx"
        candidates = list(self.data_dir.glob("24-Participation*"))
        if not candidates:
            raise FileNotFoundError(f"Table 24 not found in {self.data_dir}")
        df = pd.read_excel(candidates[0], sheet_name="Sheet1")
        df.columns = [c.strip() for c in df.columns]
        df["state"] = df["State/UT"].apply(self._harmonize_state)
        return df[["state", "Seats", "Contested", "Elected",
                    "% of Elected Women Over total seats in State/UT"]].rename(
            columns={
                "Seats": "seats",
                "Contested": "women_contested",
                "Elected": "women_elected",
                "% of Elected Women Over total seats in State/UT":
                    "pct_women_elected",
            }
        )

    def load_fiscal_transfers(self) -> pd.DataFrame:
        """Tax return ratios from Finance Commission reports."""
        records = [
            ("Punjab", 72.9), ("Himachal Pradesh", 174.2),
            ("Haryana", 18.6), ("Rajasthan", 154.1),
            ("Gujarat", 31.3), ("Maharashtra", 7.7),
            ("Goa", 86.4), ("Karnataka", 13.9),
            ("Kerala", 63.4), ("Tamil Nadu", 29.7),
            ("Andhra Pradesh", 46.0), ("Telangana", 49.8),
            ("Madhya Pradesh", 279.1), ("Uttar Pradesh", 333.2),
            ("Bihar", 922.5), ("Jharkhand", 282.3),
            ("West Bengal", 90.2), ("Odisha", 187.3),
            ("Assam", 354.6), ("Sikkim", 651.7),
            ("Nagaland", 1252.5), ("Manipur", 1484.9),
            ("Mizoram", 3583.2), ("Tripura", 1077.0),
            ("Meghalaya", 464.9),
        ]
        return pd.DataFrame(records, columns=["state", "return_per100"])

    def build(self) -> pd.DataFrame:
        """Merge all sources into a single analysis-ready DataFrame."""
        df = self.load_base_geography()
        df = df.merge(self.load_women_electorate(), on="state", how="left")
        df = df.merge(self.load_women_participation(), on="state", how="left")
        df = df.merge(self.load_fiscal_transfers(), on="state", how="left")

        df["women_voters"] = df["women_voters"].fillna(0)
        df["women_contested"] = df["women_contested"].fillna(0)
        df["women_elected"] = df["women_elected"].fillna(0)
        df["pct_women_elected"] = df["pct_women_elected"].fillna(0)
        df["return_per100"] = df["return_per100"].fillna(0)

        # Derived variables
        df["women_contest_rate"] = np.where(
            df["seats"] > 0,
            df["women_contested"] / df["seats"] * 100, 0
        )
        df["women_disparity"] = (
            1 - df["return_per100"] * 0.35 / 100
        ).clip(lower=0)
        df["wv_per_seat"] = np.where(
            df["seats"] > 0, df["women_voters"] / df["seats"], 0
        )

        # Area-based delimitation simulation
        total_area = df["area_km2"].sum()
        df["quota"] = df["area_km2"] / total_area * 543
        df["ideal_area_seats"] = np.floor(df["quota"]).astype(int)
        df.loc[df["ideal_area_seats"] < 1, "ideal_area_seats"] = 1
        remaining = 543 - df["ideal_area_seats"].sum()
        df["remainder"] = df["quota"] - df["ideal_area_seats"]
        idx_sorted = df["remainder"].sort_values(ascending=False).index
        for i in range(abs(remaining)):
            if remaining > 0:
                df.loc[idx_sorted[i], "ideal_area_seats"] += 1
        df["seat_gap"] = df["ideal_area_seats"] - df["current_seats"]

        # Geographic metadata
        df["region"] = df["state"].map(self.REGION_MAP).fillna("Other")
        df["lat"] = df["state"].map(lambda s: self.CENTROIDS.get(s, (0, 0))[0])
        df["lon"] = df["state"].map(lambda s: self.CENTROIDS.get(s, (0, 0))[1])

        self.df = df.drop(columns=["quota", "remainder"])
        return self.df


# =====================================================================
# MODULE 2: SPATIAL WEIGHT MATRIX
# =====================================================================

class SpatialWeights:
    """Builds and manages a row-standardized queen contiguity matrix."""

    # Queen contiguity adjacency list (administrative boundaries)
    ADJACENCY = {
        "Andhra Pradesh": ["Telangana", "Tamil Nadu", "Karnataka",
                           "Odisha", "Chhattisgarh"],
        "Arunachal Pradesh": ["Assam", "Nagaland"],
        "Assam": ["Arunachal Pradesh", "Nagaland", "Manipur",
                   "Mizoram", "Tripura", "Meghalaya", "West Bengal"],
        "Bihar": ["Uttar Pradesh", "Jharkhand", "West Bengal"],
        "Chhattisgarh": ["Madhya Pradesh", "Maharashtra", "Telangana",
                         "Odisha", "Jharkhand", "Uttar Pradesh"],
        "Gujarat": ["Rajasthan", "Madhya Pradesh", "Maharashtra"],
        "Haryana": ["Punjab", "Himachal Pradesh", "Rajasthan",
                     "Uttar Pradesh", "Delhi"],
        "Himachal Pradesh": ["Punjab", "Haryana", "Uttarakhand",
                              "Jammu & Kashmir"],
        "Jharkhand": ["Bihar", "Uttar Pradesh", "Chhattisgarh",
                       "Odisha", "West Bengal"],
        "Karnataka": ["Kerala", "Tamil Nadu", "Andhra Pradesh",
                       "Telangana", "Maharashtra", "Goa"],
        "Kerala": ["Tamil Nadu", "Karnataka"],
        "Madhya Pradesh": ["Rajasthan", "Uttar Pradesh",
                            "Chhattisgarh", "Maharashtra", "Gujarat"],
        "Maharashtra": ["Gujarat", "Madhya Pradesh", "Chhattisgarh",
                         "Telangana", "Karnataka", "Goa"],
        "Odisha": ["West Bengal", "Jharkhand", "Chhattisgarh",
                    "Andhra Pradesh"],
        "Punjab": ["Himachal Pradesh", "Haryana", "Rajasthan"],
        "Rajasthan": ["Punjab", "Haryana", "Uttar Pradesh",
                       "Madhya Pradesh", "Gujarat"],
        "Tamil Nadu": ["Kerala", "Karnataka", "Andhra Pradesh"],
        "Telangana": ["Maharashtra", "Chhattisgarh",
                       "Andhra Pradesh", "Karnataka"],
        "Uttar Pradesh": ["Uttarakhand", "Himachal Pradesh", "Haryana",
                           "Rajasthan", "Madhya Pradesh", "Chhattisgarh",
                           "Jharkhand", "Bihar"],
        "Uttarakhand": ["Himachal Pradesh", "Uttar Pradesh"],
        "West Bengal": ["Sikkim", "Assam", "Jharkhand", "Bihar",
                         "Odisha"],
        "Delhi": ["Haryana", "Uttar Pradesh"],
        "Goa": ["Maharashtra", "Karnataka"],
        "Manipur": ["Assam", "Nagaland", "Mizoram"],
        "Meghalaya": ["Assam"],
        "Mizoram": ["Assam", "Manipur", "Tripura"],
        "Nagaland": ["Assam", "Arunachal Pradesh", "Manipur"],
        "Sikkim": ["West Bengal"],
        "Tripura": ["Assam", "Mizoram"],
        "Dadra & Nagar Haveli": ["Gujarat", "Maharashtra"],
    }

    def __init__(self, states: list):
        self.states = states
        self.n = len(states)
        self.W = np.zeros((self.n, self.n))
        self._build()

    def _build(self):
        """Construct and row-standardize the weight matrix."""
        idx = {s: i for i, s in enumerate(self.states)}
        for state, neighbors in self.ADJACENCY.items():
            if state not in idx:
                continue
            i = idx[state]
            for nb in neighbors:
                if nb in idx:
                    self.W[i, idx[nb]] = 1.0
        row_sums = self.W.sum(axis=1)
        for i in range(self.n):
            if row_sums[i] > 0:
                self.W[i] /= row_sums[i]

    @property
    def n_edges(self) -> int:
        return int((self.W > 0).sum())

    @property
    def density(self) -> float:
        return self.n_edges / (self.n * self.n) * 100

    def spatial_lag(self, values: np.ndarray) -> np.ndarray:
        """Compute Wx (weighted mean of neighbors)."""
        return self.W @ values


# =====================================================================
# MODULE 3: SPATIAL STATISTICS ENGINE
# =====================================================================

class SpatialStats:
    """Computes Moran's I, LISA, and spatial regression diagnostics."""

    LISA_THRESHOLD = 0.5  # Local I significance cutoff

    def __init__(self, weights: SpatialWeights):
        self.W = weights.W
        self.n = weights.n
        self.s0 = self.W.sum()
        self.E_I = -1.0 / (self.n - 1)

    def standardize(self, x: np.ndarray) -> np.ndarray:
        """Zero-mean, unit-variance standardization."""
        return (x - x.mean()) / (x.std() + 1e-10)

    def moran_i(self, x: np.ndarray) -> dict:
        """
        Global Moran's I statistic.

        I = (n / S0) * [sum_i sum_j w_ij * z_i * z_j] / [sum_i z_i^2]

        Returns dict with I, E_I, strength classification, and
        variance under normality assumption.
        """
        z = self.standardize(x)
        numerator = 0.0
        for i in range(self.n):
            for j in range(self.n):
                numerator += self.W[i, j] * z[i] * z[j]
        denominator = (z ** 2).sum()
        I = (self.n / self.s0) * numerator / denominator if denominator > 0 else 0

        # Variance under normality (Cliff & Ord, 1981)
        S1 = 0.5 * np.sum((self.W + self.W.T) ** 2)
        S2 = np.sum((self.W.sum(axis=0) + self.W.sum(axis=1)) ** 2)
        k = (np.sum(z ** 4) / self.n) / ((np.sum(z ** 2) / self.n) ** 2)
        A = self.n * ((self.n**2 - 3*self.n + 3)*S1 - self.n*S2 + 3*self.s0**2)
        B = k * (self.n*(self.n-1)*S1 - 2*self.n*S2 + 6*self.s0**2)
        C = (self.n-1) * (self.n-2) * (self.n-3) * self.s0**2
        var_I = (A - B) / C - self.E_I**2 if C != 0 else 0

        z_score = (I - self.E_I) / np.sqrt(var_I) if var_I > 0 else 0

        if abs(I) > 0.25:
            strength = "STRONG"
        elif abs(I) > 0.15:
            strength = "MODERATE"
        else:
            strength = "WEAK"

        return {
            "I": round(I, 4),
            "E_I": round(self.E_I, 4),
            "var_I": round(var_I, 6),
            "z_score": round(z_score, 2),
            "strength": strength,
        }

    def lisa(self, x: np.ndarray) -> dict:
        """
        Local Indicators of Spatial Association (Anselin, 1995).

        Returns per-unit local I values, spatial lag, and
        HH/HL/LH/LL/NS classification.
        """
        z = self.standardize(x)
        m2 = (z ** 2).sum() / self.n
        lag_z = self.W @ z

        local_I = np.zeros(self.n)
        labels = []

        for i in range(self.n):
            local_I[i] = z[i] * lag_z[i] / m2 if m2 > 0 else 0

            if abs(local_I[i]) < self.LISA_THRESHOLD:
                labels.append("NS")
            elif z[i] > 0 and lag_z[i] > 0:
                labels.append("HH")
            elif z[i] > 0 and lag_z[i] <= 0:
                labels.append("HL")
            elif z[i] <= 0 and lag_z[i] > 0:
                labels.append("LH")
            else:
                labels.append("LL")

        return {
            "local_I": local_I.tolist(),
            "labels": labels,
            "z": z.tolist(),
            "lag_z": lag_z.tolist(),
        }

    def ols_with_spatial_diagnostics(
        self, y: np.ndarray, X: np.ndarray
    ) -> dict:
        """
        OLS regression with Moran's I test on residuals.
        Used for Query 3 (spatial confounding detection).

        Parameters:
            y: dependent variable (n,)
            X: independent variable(s) (n,) or (n, k)

        Returns:
            coefficients, residuals, R-squared,
            Moran's I of residuals, LISA of residuals
        """
        if X.ndim == 1:
            X = X.reshape(-1, 1)

        # Add intercept
        X_aug = np.column_stack([np.ones(len(y)), X])
        beta = np.linalg.lstsq(X_aug, y, rcond=None)[0]
        y_hat = X_aug @ beta
        residuals = y - y_hat

        ss_res = (residuals ** 2).sum()
        ss_tot = ((y - y.mean()) ** 2).sum()
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        # Spatial diagnostics on residuals
        moran_resid = self.moran_i(residuals)
        lisa_resid = self.lisa(residuals)

        return {
            "beta": beta.tolist(),
            "r_squared": round(r_squared, 4),
            "residuals": residuals.tolist(),
            "predicted": y_hat.tolist(),
            "moran_residuals": moran_resid,
            "lisa_residuals": lisa_resid,
        }

    def simpsons_paradox_test(
        self, x: np.ndarray, y: np.ndarray, groups: np.ndarray
    ) -> dict:
        """
        Test whether a national-level correlation reverses or
        changes substantially within geographic sub-groups.
        Used for Query 5.
        """
        national_corr = float(np.corrcoef(x, y)[0, 1])

        unique_groups = sorted(set(groups))
        regional = {}
        for g in unique_groups:
            mask = groups == g
            n_g = mask.sum()
            if n_g < 3:
                continue
            xg, yg = x[mask], y[mask]
            corr_g = float(np.corrcoef(xg, yg)[0, 1]) if n_g > 2 else np.nan
            regional[g] = {
                "n": int(n_g),
                "mean_x": round(float(xg.mean()), 2),
                "mean_y": round(float(yg.mean()), 2),
                "corr": round(corr_g, 3) if not np.isnan(corr_g) else None,
            }

        # Detect paradox: sign reversal in any region with n >= 4
        sign_reversals = [
            g for g, s in regional.items()
            if s["corr"] is not None
            and s["n"] >= 4
            and np.sign(s["corr"]) != np.sign(national_corr)
        ]

        return {
            "national_corr": round(national_corr, 4),
            "regional": regional,
            "paradox_detected": len(sign_reversals) > 0,
            "reversal_regions": sign_reversals,
        }


# =====================================================================
# MODULE 4: PIPELINE ORCHESTRATOR
# =====================================================================

class SpatializationPipeline:
    """
    Orchestrates the full pipeline:
        data -> weights -> statistics -> charts -> report
    """

    # Variables to analyze with their display labels
    ANALYSIS_VARIABLES = {
        "women_contest_rate": "Women Candidature Rate (%)",
        "pct_women_elected": "% Women Elected Over Total Seats",
        "women_disparity": "Women Fiscal Disparity Index",
        "seat_gap": "Seat Redistribution Gap",
        "wv_per_seat": "Women Voters per Seat",
    }

    def __init__(self, data_dir: str, output_dir: str):
        self.data_dir = data_dir
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.df = None
        self.weights = None
        self.stats = None
        self.results = {}

    def run(self):
        """Execute all pipeline stages."""
        self._stage1_ingest()
        self._stage2_weights()
        self._stage3_global_moran()
        self._stage4_lisa()
        self._stage5_spatial_confounding()
        self._stage6_simpsons_paradox()
        self._stage7_export()
        self._stage8_report()

    def _stage1_ingest(self):
        """STAGE 1: Data ingestion and transformation."""
        print("[1/8] Ingesting data...")
        ingestion = DataIngestion(self.data_dir)
        self.df = ingestion.build()
        print(f"       {len(self.df)} states/UTs loaded")
        print(f"       {len(self.df.columns)} columns")

    def _stage2_weights(self):
        """STAGE 2: Build spatial weight matrix."""
        print("[2/8] Building spatial weight matrix...")
        self.weights = SpatialWeights(list(self.df["state"]))
        self.stats = SpatialStats(self.weights)
        print(f"       {self.weights.n} nodes")
        print(f"       {self.weights.n_edges} directed edges")
        print(f"       {self.weights.density:.2f}% density")
        np.save(
            self.output_dir / "spatial_weights_matrix.npy",
            self.weights.W,
        )

    def _stage3_global_moran(self):
        """STAGE 3: Compute global Moran's I for all variables."""
        print("[3/8] Computing global Moran's I...")
        self.results["moran"] = {}
        for var, label in self.ANALYSIS_VARIABLES.items():
            vals = self.df[var].values.astype(float)
            result = self.stats.moran_i(vals)
            self.results["moran"][var] = {**result, "label": label}
            flag = "***" if result["strength"] == "STRONG" else "   "
            print(
                f"       {flag} {label:40s} "
                f"I={result['I']:+.4f}  "
                f"z={result['z_score']:+.2f}  "
                f"[{result['strength']}]"
            )

    def _stage4_lisa(self):
        """STAGE 4: LISA classification for all variables."""
        print("[4/8] Computing LISA classifications...")
        self.results["lisa"] = {}
        for var in self.ANALYSIS_VARIABLES:
            vals = self.df[var].values.astype(float)
            lisa_result = self.stats.lisa(vals)
            self.results["lisa"][var] = lisa_result
            self.df[f"lisa_{var}"] = lisa_result["labels"]
            counts = pd.Series(lisa_result["labels"]).value_counts()
            print(f"       {var}: {dict(counts)}")

    def _stage5_spatial_confounding(self):
        """STAGE 5: OLS + residual Moran test (Query 3)."""
        print("[5/8] Spatial confounding test...")
        y = self.df["women_contest_rate"].values.astype(float)
        X = self.df["women_disparity"].values.astype(float)
        result = self.stats.ols_with_spatial_diagnostics(y, X)
        self.results["confounding"] = result

        self.df["residual"] = result["residuals"]
        self.df["predicted_contest"] = result["predicted"]
        self.df["lisa_resid"] = result["lisa_residuals"]["labels"]

        print(
            f"       R-squared: {result['r_squared']:.4f}"
        )
        print(
            f"       Residual Moran's I: "
            f"{result['moran_residuals']['I']:+.4f} "
            f"[{result['moran_residuals']['strength']}]"
        )
        if result["moran_residuals"]["I"] > 0.2:
            print(
                "       >> SPATIAL CONFOUNDING DETECTED: "
                "residuals cluster geographically"
            )

    def _stage6_simpsons_paradox(self):
        """STAGE 6: Simpson's Paradox test (Query 5)."""
        print("[6/8] Simpson's Paradox test...")
        x = self.df["women_contest_rate"].values
        y = self.df["pct_women_elected"].values
        groups = self.df["region"].values
        result = self.stats.simpsons_paradox_test(x, y, groups)
        self.results["simpson"] = result

        print(f"       National corr: {result['national_corr']:+.4f}")
        for region, stats in sorted(
            result["regional"].items(),
            key=lambda x: -(x[1]["mean_x"]),
        ):
            corr_str = (
                f"{stats['corr']:+.3f}" if stats["corr"] else "N/A"
            )
            print(
                f"       {region:12s} "
                f"contest={stats['mean_x']:6.1f}  "
                f"elected={stats['mean_y']:5.1f}  "
                f"corr={corr_str}  n={stats['n']}"
            )
        if result["paradox_detected"]:
            print(
                f"       >> PARADOX DETECTED in: "
                f"{result['reversal_regions']}"
            )

    def _stage7_export(self):
        """STAGE 7: Export all results."""
        print("[7/8] Exporting results...")
        with open(self.output_dir / "moran_results.json", "w") as f:
            json.dump(self.results["moran"], f, indent=2)

        lisa_rows = []
        for var in self.ANALYSIS_VARIABLES:
            for i, state in enumerate(self.df["state"]):
                lisa_rows.append({
                    "state": state,
                    "variable": var,
                    "label": self.results["lisa"][var]["labels"][i],
                    "z": round(self.results["lisa"][var]["z"][i], 4),
                    "lag_z": round(self.results["lisa"][var]["lag_z"][i], 4),
                })
        pd.DataFrame(lisa_rows).to_csv(
            self.output_dir / "lisa_classifications.csv", index=False
        )

        all_results = {
            "moran": self.results["moran"],
            "confounding": {
                "r_squared": self.results["confounding"]["r_squared"],
                "beta": self.results["confounding"]["beta"],
                "moran_residuals": self.results["confounding"][
                    "moran_residuals"
                ],
            },
            "simpson": self.results["simpson"],
        }
        with open(self.output_dir / "full_results.json", "w") as f:
            json.dump(all_results, f, indent=2, default=str)

    def _stage8_report(self):
        """STAGE 8: Generate summary report."""
        print("[8/8] Generating report...")
        lines = [
            "=" * 70,
            "SPATIALIZING STANDARD CHARTS: PIPELINE REPORT",
            "=" * 70,
            "",
            f"States analyzed: {len(self.df)}",
            f"Spatial weight edges: {self.weights.n_edges}",
            f"Matrix density: {self.weights.density:.2f}%",
            "",
            "DECISION TABLE:",
            f"{'Variable':<40s} {'I':>8s} {'Decision':<20s}",
            "-" * 70,
        ]
        for var, res in self.results["moran"].items():
            decision = (
                "SPATIALIZE" if res["I"] > 0.25
                else "CHART SUFFICIENT"
            )
            lines.append(
                f"{res['label']:<40s} {res['I']:>+8.4f} {decision:<20s}"
            )
        lines.extend([
            "",
            f"Spatial confounding: residual I = "
            f"{self.results['confounding']['moran_residuals']['I']:+.4f}",
            f"Simpson's Paradox: "
            f"{'DETECTED' if self.results['simpson']['paradox_detected'] else 'NOT DETECTED'}",
            "",
            "=" * 70,
        ])

        report = "\n".join(lines)
        with open(self.output_dir / "pipeline_report.txt", "w") as f:
            f.write(report)
        print(report)


# =====================================================================
# ENTRY POINT
# =====================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Spatializing Standard Charts Pipeline"
    )
    parser.add_argument(
        "--data-dir", default="./data/",
        help="Directory containing ECI Excel files"
    )
    parser.add_argument(
        "--output-dir", default="./output/",
        help="Directory for pipeline outputs"
    )
    args = parser.parse_args()

    pipeline = SpatializationPipeline(args.data_dir, args.output_dir)
    pipeline.run()
