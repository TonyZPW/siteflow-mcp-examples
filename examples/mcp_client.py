#!/usr/bin/env python3
"""Minimal zero-dependency Python client for SiteFlow UK Streamable HTTP MCP.

Usage:
    export SITEFLOW_API_KEY="YOUR_SITEFLOW_API_KEY"
    python3 examples/mcp_client.py
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

MCP_URL = os.environ.get("SITEFLOW_MCP_URL", "https://siteflow.vip/mcp")
API_KEY = os.environ.get("SITEFLOW_API_KEY", "").strip()


def rpc(method: str, params: dict | None = None, req_id: int | None = 1) -> dict | None:
    payload: dict = {"jsonrpc": "2.0", "method": method}
    if req_id is not None:
        payload["id"] = req_id
    if params is not None:
        payload["params"] = params

    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else None


def main() -> None:
    if not API_KEY:
        sys.exit("Set SITEFLOW_API_KEY first (get a key at https://siteflow.vip/prices).")

    # 1. MCP Handshake
    init = rpc("initialize", {"protocolVersion": "2025-03-26", "clientInfo": {"name": "siteflow-py-example", "version": "1.0.0"}}, req_id=1)
    print("Connected to:", init["result"]["serverInfo"])
    rpc("notifications/initialized", req_id=None)

    # 2. Discover tools
    tools_resp = rpc("tools/list", req_id=2)
    tool_names = [t["name"] for t in tools_resp["result"]["tools"]]
    print(f"Available tools ({len(tool_names)}):", ", ".join(tool_names))

    # 3. Call score_site for Marylebone High St, London (cafe, 500 m)
    score_resp = rpc(
        "tools/call",
        {
            "name": "score_site",
            "arguments": {
                "city_id": "e09000033",
                "business_type": "cafe",
                "point": {"lat": 51.5205, "lon": -0.1518},
                "radius_m": 500,
            },
        },
        req_id=3,
    )
    result = score_resp["result"]["structuredContent"]
    mloc = result.get("micro_location") or {}
    epc = (result.get("commercial_context") or {}).get("epc") or {}
    comps = ((result.get("details") or {}).get("competition") or {}).get("competing_premises_within_radius")

    print("\nMarylebone High St (W1U) — Coffee Shop (500 m):")
    print(f"  Composite Score:  {result.get('composite')}/100")
    print(f"  Street Pitch:     {mloc.get('pitch_label')} ({mloc.get('shops_100m')} shops within 100 m)")
    print(f"  Weekday Peak:     ~{int(round(max(result.get('hours_weekday') or [0]))):,} simultaneous people")
    print(f"  Competitors:      {comps} mapped OSM cafes")
    print(f"  MEES EPC F/G:     {epc.get('mees_risk_count')} commercial units")


if __name__ == "__main__":
    main()
