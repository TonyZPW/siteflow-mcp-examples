# SiteFlow UK — Remote MCP Server & Examples

[![Transport](https://img.shields.io/badge/MCP-Streamable%20HTTP-1f6f66)](https://siteflow.vip/docs)
[![Auth](https://img.shields.io/badge/Auth-OAuth%202.1%20%2B%20PKCE%20%7C%20Bearer-17253a)](https://siteflow.vip/.well-known/oauth-protected-resource)
[![Coverage](https://img.shields.io/badge/Coverage-359%20GB%20Councils-2563eb)](https://siteflow.vip/areas)
[![Data](https://img.shields.io/badge/Data-15%20UK%20OGL%20v3%20Registers%20%2B%20OSM-e2603f)](https://siteflow.vip/sources)

Give **Claude**, **ChatGPT**, **Cursor**, **Claude Code**, **VS Code**, or your custom AI agents live commercial site-selection intelligence across all **359 local authorities in Great Britain** (England, Wales & Scotland).

- **Live Remote MCP Endpoint (Streamable HTTP):** `https://siteflow.vip/mcp`
- **OAuth 2.1 Protected Resource Metadata (RFC 9728):** `https://siteflow.vip/.well-known/oauth-protected-resource`
- **OAuth 2.1 Authorization Server Metadata (RFC 8414):** `https://siteflow.vip/.well-known/oauth-authorization-server`
- **Interactive Map (Free Preview):** https://siteflow.vip/people
- **Unwatermarked A4 Sample Brief (Soho, W1F 8TH):** https://siteflow.vip/sample-report
- **Full API & MCP Documentation:** https://siteflow.vip/docs

> This repository hosts runnable client configs, zero-dependency Python/Node.js MCP examples, and registry metadata for the hosted SiteFlow UK Remote MCP service.

---

## Quick Start

### 1. Claude.ai / Claude Desktop / ChatGPT (One-Click OAuth 2.1 + PKCE)

No local install or JSON editing required. SiteFlow implements **OAuth 2.1 + PKCE (S256) + Dynamic Client Registration (RFC 7591)** with automatic rolling refresh tokens:

1. Open **Settings → Connectors → Add custom connector** (in Claude.ai / ChatGPT).
2. Enter the Remote MCP URL:
   ```text
   https://siteflow.vip/mcp
   ```
3. Complete the OAuth prompt by pasting your SiteFlow Access Key (obtainable from [siteflow.vip/prices](https://siteflow.vip/prices)).

### 2. Cursor / Claude Code / Windsurf (Bearer Access Key)

Copy [`configs/cursor_mcp.json`](./configs/cursor_mcp.json) into `.mcp.json` (project root) or `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "siteflow-uk": {
      "url": "https://siteflow.vip/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_SITEFLOW_API_KEY"
      }
    }
  }
}
```

### 3. VS Code (Copilot MCP)

Copy [`configs/vscode_mcp.json`](./configs/vscode_mcp.json) into `.vscode/mcp.json` — it prompts securely for your API key without storing secrets in git.

---

## Available MCP Tools (8 Tools)

| Tool | Purpose | Key Inputs |
| :--- | :--- | :--- |
| `list_cities` | List all 359 published Great Britain councils (England, Wales, Scotland) | `country`, `offset`, `limit` |
| `search_locations` | Resolve UK postcodes (`W1F 8TH`, `M1 1AE`), stations or street names to coordinates & `city_id` | `query`, `city_id` |
| `analyze_place` | 24-hour simultaneous area presence within 250 m / 500 m / 1 km (weekday, weekend, bank holiday) | `point`, `day_type`, `radius_m` |
| `score_site` | 0–100 commercial site suitability score + street-level micro-location pitch (`prime` vs `backstreet_caution`), competitors, EPC/MEES, affluence, traffic, schools, flood & heritage flags | `business_type`, `point`, `radius_m` |
| `rank_sites` | Shortlist top-ranked 1 km areas inside one UK council for a trade | `city_id`, `business_type`, `top` |
| `compare_places` | Side-by-side comparison of 2–5 Great Britain locations on a consistent release | `places`, `day_type`, `radius_m` |
| `get_place_context` | Commercial context only: competitors, IMD/WIMD/SIMD affluence, Non-Domestic EPC/MEES, DfT AADF traffic, GIAS schools & statutory constraints | `point`, `radius_m` |
| `create_report` | Generate an exportable Markdown or CSV commercial brief with temporary download URL | `point`, `label`, `format` |

Supported `business_type` values: `cafe`, `convenience`, `restaurant`, `takeaway`, `bar`.

---

## Real Output Example (Central London Coffee Shop Benchmark)

Like-for-like comparison across three London prime pitches (`cafe`, 500 m radius, full `99.8%` council coverage):

| Pitch | Score | Weekday Peak (500 m Presence) | Weekend Peak | Mapped Competitors | EPC F/G (MEES) |
| :--- | ---: | ---: | ---: | ---: | :--- |
| **Marylebone High St (W1U)** | **75.7 / 100** | ~24,000 (12:00) | ~14,000 (14:00) | 31 | 85 (5.8%) |
| **Camden High St (NW1)** | **67.7 / 100** | ~11,000 (12:00) | ~11,000 (14:00) | 44 | 131 (8.7%) |
| **Berwick St, Soho (W1F)** | **66.5 / 100** | ~27,000 (12:00) | ~19,000 (14:00) | 119 | 478 (8.5%) |

Full interactive write-up: https://siteflow.vip/insights/soho-vs-marylebone-vs-camden-london-footfall

---

## Example Prompts for Claude / Cursor

Once connected, try asking your AI assistant:

1. *"Compare Berwick St in Soho (`W1F 8TH`) against Marylebone High St (`W1U 4RY`) for an independent coffee shop. Summarise weekday vs weekend presence, competitor saturation, and Non-Domestic EPC F/G lease risks."*
2. *"Find the top 5 restaurant areas in Birmingham and flag any flood zones, listed buildings or conservation areas before we book viewings."*
3. *"Score postcode `M1 1AE` in Manchester for a takeaway within 500 m, including nearby schools and road traffic counts."*
4. *"Generate a Markdown commercial brief for `EH1 1YZ` in Edinburgh (`cafe`) and list Scotland-specific SIMD affluence and SEPA flood checks."*

---

## Runnable Code Examples (Zero Dependencies)

Set your key and run either script directly:

```bash
export SITEFLOW_API_KEY="YOUR_SITEFLOW_API_KEY"

# Python 3.9+ (stdlib only)
python3 examples/mcp_client.py

# Node.js 18+ (built-in fetch)
node examples/mcp_client.mjs
```

---

## Open Registers & Methodology

SiteFlow fuses **15 official UK public-sector open registers (OGL v3)** + OpenStreetMap without mobile-telco tracking:

- **24-hour presence curve:** Modelled simultaneous people within the catchment radius (residents + workers + visitors) from ONS Census 2021 origin-destination flows, DfT BODS transit timetables, and OSM land-use anchors.
- **Street-level micro-location:** Pedestrian street hierarchy + 50 m / 100 m / 250 m retail frontage density (`prime`, `secondary`, `local`, `off_pitch`, `backstreet_caution`).
- **Pre-lease context:** MHCLG Non-Domestic EPC & MEES F/G risk (England & Wales), English IoD 2025 / Welsh WIMD / Scottish SIMD affluence, DfT AADF traffic, DfE GIAS schools, EA/NRW/SEPA flood zones, and Historic England/Cadw heritage registers.

> **Best practice:** Modelled presence estimates are designed for rapid shortlisting and pre-lease risk screening — always pair with two timed door-side footfall counts before signing Heads of Terms.

---

## License

MIT — see [`LICENSE`](./LICENSE). Data outputs incorporate UK public sector information licensed under the Open Government Licence v3.0 and OpenStreetMap (ODbL).
