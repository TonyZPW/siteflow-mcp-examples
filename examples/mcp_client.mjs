#!/usr/bin/env node
/**
 * Minimal zero-dependency Node.js 18+ client for SiteFlow UK Streamable HTTP MCP.
 *
 * Usage:
 *   export SITEFLOW_API_KEY="YOUR_SITEFLOW_API_KEY"
 *   node examples/mcp_client.mjs
 */

const MCP_URL = process.env.SITEFLOW_MCP_URL || "https://siteflow.vip/mcp";
const API_KEY = (process.env.SITEFLOW_API_KEY || "").trim();

if (!API_KEY) {
  console.error("Set SITEFLOW_API_KEY first (get a key at https://siteflow.vip/prices).");
  process.exit(1);
}

async function rpc(method, params = undefined, id = 1) {
  const body = { jsonrpc: "2.0", method };
  if (id !== null) body.id = id;
  if (params !== undefined) body.params = params;

  const res = await fetch(MCP_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  }
  const text = await res.text();
  return text.trim() ? JSON.parse(text) : null;
}

const init = await rpc(
  "initialize",
  { protocolVersion: "2025-03-26", clientInfo: { name: "siteflow-node-example", version: "1.0.0" } },
  1
);
console.log("Connected to:", init.result.serverInfo);
await rpc("notifications/initialized", undefined, null);

const listed = await rpc("tools/list", undefined, 2);
console.log("Available tools:", listed.result.tools.map((t) => t.name).join(", "));

const scored = await rpc(
  "tools/call",
  {
    name: "score_site",
    arguments: {
      city_id: "e09000033",
      business_type: "cafe",
      point: { lat: 51.5205, lon: -0.1518 },
      radius_m: 500,
    },
  },
  3
);

const data = scored.result.structuredContent;
const wdPeak = Math.round(Math.max(...(data.hours_weekday || [0])));
console.log("\nMarylebone High St (W1U) — Coffee Shop (500 m):");
console.log("  Composite Score:", `${data.composite}/100`);
console.log("  Street Pitch:   ", data.micro_location?.pitch_label);
console.log("  Weekday Peak:   ", `~${wdPeak.toLocaleString()} simultaneous people`);
console.log("  Competitors:    ", data.details?.competition?.competing_premises_within_radius);
