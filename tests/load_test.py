"""Concurrency load test for the gateway — proves the stateless server holds up
under parallel agent traffic (the whole point of the 2026-07-28 stateless move:
round-robin-LB safe, no shared session store).

Fires N concurrent requests at /healthz (a cheap custom route that needs no MCP
session) and reports success rate + latency percentiles + throughput. Defaults
are modest so it runs in CI in seconds; bump via env for real load drills.

    PORT=8000 python http_server.py &
    GATEWAY_URL=http://127.0.0.1:8000 LOAD_N=200 LOAD_CONCURRENCY=50 \
        python tests/load_test.py

Fails (exit 1) if any request errors, any non-200, or throughput collapses
below LOAD_MIN_RPS. Stdlib only (asyncio + urllib in threads) — no CI deps.
"""
import concurrent.futures
import os
import sys
import time
import urllib.request

BASE = os.environ.get("GATEWAY_URL", "http://127.0.0.1:8000").rstrip("/")
HEALTH = f"{BASE}/healthz"
N = int(os.environ.get("LOAD_N", "200"))
CONCURRENCY = int(os.environ.get("LOAD_CONCURRENCY", "50"))
MIN_RPS = float(os.environ.get("LOAD_MIN_RPS", "20"))


def _one(_i: int):
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(HEALTH, timeout=15) as resp:
            ok = resp.status == 200 and b'"ok"' in resp.read()
        return (ok, (time.perf_counter() - t0) * 1000.0, None)
    except Exception as exc:  # noqa: BLE001
        return (False, (time.perf_counter() - t0) * 1000.0, repr(exc))


def _pct(sorted_ms, p):
    if not sorted_ms:
        return 0.0
    k = max(0, min(len(sorted_ms) - 1, int(round((p / 100.0) * (len(sorted_ms) - 1)))))
    return sorted_ms[k]


def main() -> None:
    print(f"load: {N} requests, concurrency {CONCURRENCY}, target {HEALTH}")
    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        results = list(ex.map(_one, range(N)))
    wall = time.perf_counter() - t0

    oks = [r for r in results if r[0]]
    errs = [r for r in results if not r[0]]
    lat = sorted(r[1] for r in results)
    rps = N / wall if wall else 0.0

    print(f"  success: {len(oks)}/{N}")
    print(f"  latency ms: p50={_pct(lat,50):.1f} p95={_pct(lat,95):.1f} p99={_pct(lat,99):.1f} max={lat[-1]:.1f}")
    print(f"  throughput: {rps:.1f} req/s over {wall:.2f}s")

    failures = []
    if errs:
        failures.append(f"{len(errs)} requests errored (e.g. {errs[0][2]})")
    if rps < MIN_RPS:
        failures.append(f"throughput {rps:.1f} rps < floor {MIN_RPS}")

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)
        sys.exit(1)
    print("load test OK")


if __name__ == "__main__":
    main()
