#!/usr/bin/env python3
"""Analyze Apache JMeter JTL/CSV results.

Usage:
    python scripts/analyze_jtl.py results/sample/stress_503_sample.csv --out results/analysis
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def read_jtl(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_csv(path)
    required = {"timeStamp", "elapsed", "responseCode", "success"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df = df.copy()
    df["timeStamp"] = pd.to_numeric(df["timeStamp"], errors="coerce")
    df["elapsed"] = pd.to_numeric(df["elapsed"], errors="coerce")
    df = df.dropna(subset=["timeStamp", "elapsed"])
    df["time"] = pd.to_datetime(df["timeStamp"], unit="ms")
    df["success_bool"] = df["success"].astype(str).str.lower().eq("true")
    df["responseCode"] = df["responseCode"].astype(str)
    return df


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    total = len(df)
    errors = int((~df["success_bool"]).sum())
    duration_sec = max((df["timeStamp"].max() - df["timeStamp"].min()) / 1000, 1)

    return pd.DataFrame([
        {
            "samples": total,
            "success": int(df["success_bool"].sum()),
            "errors": errors,
            "error_pct": round(errors / total * 100, 2) if total else 0,
            "avg_ms": round(df["elapsed"].mean(), 2),
            "min_ms": round(df["elapsed"].min(), 2),
            "max_ms": round(df["elapsed"].max(), 2),
            "p90_ms": round(df["elapsed"].quantile(0.90), 2),
            "p95_ms": round(df["elapsed"].quantile(0.95), 2),
            "p99_ms": round(df["elapsed"].quantile(0.99), 2),
            "throughput_rps": round(total / duration_sec, 2),
        }
    ])


def save_response_time_plot(df: pd.DataFrame, out_dir: Path) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["elapsed"], linewidth=1)
    plt.title("Response time over time")
    plt.xlabel("Time")
    plt.ylabel("Elapsed, ms")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(out_dir / "response_time_over_time.png", dpi=160)
    plt.close()


def save_throughput_plot(df: pd.DataFrame, out_dir: Path) -> None:
    per_second = df.set_index("time").resample("1s").size()
    plt.figure(figsize=(10, 5))
    plt.plot(per_second.index, per_second.values, linewidth=1)
    plt.title("Throughput over time")
    plt.xlabel("Time")
    plt.ylabel("Requests per second")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(out_dir / "throughput_over_time.png", dpi=160)
    plt.close()


def save_response_codes_plot(df: pd.DataFrame, out_dir: Path) -> None:
    codes = df["responseCode"].value_counts().sort_index()
    plt.figure(figsize=(8, 5))
    plt.bar(codes.index.astype(str), codes.values)
    plt.title("HTTP response codes")
    plt.xlabel("Response code")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(out_dir / "response_codes.png", dpi=160)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Apache JMeter JTL/CSV results")
    parser.add_argument("jtl", type=Path, help="Path to JMeter .jtl/.csv file")
    parser.add_argument("--out", type=Path, default=Path("results/analysis"), help="Output directory")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    df = read_jtl(args.jtl)

    summary = build_summary(df)
    summary.to_csv(args.out / "summary.csv", index=False)

    save_response_time_plot(df, args.out)
    save_throughput_plot(df, args.out)
    save_response_codes_plot(df, args.out)

    print(summary.to_string(index=False))
    print(f"\nSaved analysis to: {args.out}")


if __name__ == "__main__":
    main()
