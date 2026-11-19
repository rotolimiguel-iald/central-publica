# -*- coding: utf-8 -*-
"""Validação determinística do núcleo R3.2, sem dados experimentais."""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

import r32_motor as M

OUT = Path(__file__).with_name("validacao_r32.json")


def main() -> None:
    old_g = M.G_CLUSTERS
    try:
        M.G_CLUSTERS = 3
        diffs = np.array([[[1, 0, -1], [1, 1, 1], [-1, 0, 1], [1, 1, -1]]], dtype=np.int16)
        n = 3
        assert np.all(np.abs(diffs).sum(axis=2) <= n)
        sizes = np.ones(3, dtype=np.int16)
        got = M.signflip_pvalues(diffs, sizes, batch_size=1)
        fft_dp_max_errors = []
        for totals in (diffs, 20 * diffs + 3 * sizes, 20 * diffs - 3 * sizes):
            fft_pair = M.exact_fft_pvalues(totals, batch_size=1)
            dp_pair = M.exact_dp_reference(totals, batch_size=1)
            fft_dp_max_errors.append(max(float(np.max(np.abs(fft_pair[0] - dp_pair[0]))), float(np.max(np.abs(fft_pair[1] - dp_pair[1])))))
        fft_dp_pass = max(fft_dp_max_errors) <= 1e-12
        expected = []
        for test in range(4):
            values = diffs[0, test]
            raw = 20 * values
            plus = raw + 3 * sizes
            minus = raw - 3 * sizes
            raw_draws, plus_draws, minus_draws = [], [], []
            for signs in itertools.product((-1, 1), repeat=3):
                signs = np.asarray(signs)
                raw_draws.append(int((signs * raw).sum()))
                plus_draws.append(int((signs * plus).sum()))
                minus_draws.append(int((signs * minus).sum()))
            raw_draws = np.asarray(raw_draws)
            plus_draws = np.asarray(plus_draws)
            minus_draws = np.asarray(minus_draws)
            raw_total = int(raw.sum())
            plus_total = int(plus.sum())
            minus_total = int(minus.sum())
            primary = np.mean(raw_draws >= raw_total) if test < 2 else np.mean(plus_draws >= plus_total)
            opposite = np.mean(raw_draws <= raw_total) if test < 2 else np.mean(plus_draws <= plus_total)
            tost = max(np.mean(plus_draws >= plus_total), np.mean(minus_draws <= minus_total))
            expected.append((primary, opposite, tost))
        expected = np.asarray(expected)
        expected[2:, 2] = np.nan
        actual = np.full((4, 3), np.nan)
        actual[:, 0] = got[0][0]
        actual[:, 1] = got[1][0]
        actual[:2, 2] = got[2][0]
        spec = next(s for s in M.SCENARIOS if s.sid == "TOST_FRONTEIRA_MAIS_075_060")
        families = [M.generate_family(np.random.default_rng(2026111599 + i), 1000, spec) for i in range(3)]
        logic_pass = all(
            bool(np.all(data["A8"] <= data["PRE"]))
            and bool(np.all(data["RET"] <= data["PRE"]))
            and bool(np.all(data["Q"] <= data["RET"]))
            for data in families
        )
        boundary = M.boundary_diagnostics(spec, families)
        passed = np.allclose(actual, expected, rtol=0, atol=1e-12, equal_nan=True) and fft_dp_pass and logic_pass and boundary["pass"]
        actual_json = [[None if np.isnan(value) else float(value) for value in row] for row in actual]
        expected_json = [[None if np.isnan(value) else float(value) for value in row] for row in expected]
        payload = {
            "schema": "K06_R32_VALIDACAO_V1",
            "exact_signflip_small_case": {
                "observed": actual_json,
                "expected_bruteforce": expected_json,
                "pass": bool(passed),
            },
            "fft_vs_dp_reference": {
                "max_errors": fft_dp_max_errors,
                "pass": bool(fft_dp_pass),
            },
            "logic_A8_PRE_Q_RET": {"pass": logic_pass},
            "boundary_D_tolerance_0005": boundary,
            "no_model_executed": True,
            "no_experimental_result_read": True,
        }
        encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        OUT.write_bytes(encoded)
        print("OBSERVED", actual)
        print("EXPECTED", expected)
        print("FFT_DP_MAX_ERRORS", fft_dp_max_errors)
        print("PASS", passed)
        print("SHA256", hashlib.sha256(encoded).hexdigest())
        if not passed:
            raise SystemExit(2)
    finally:
        M.G_CLUSTERS = old_g


if __name__ == "__main__":
    main()
