# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**DimeBuy** is a Thai retail investment app for buying US-listed stocks (NASDAQ/NYSE). The UI is in Thai; all monetary values display in both USD and THB (Thai Baht) in real time. Key domain concepts:

- **Dime! USD** — the user's USD wallet/account used to fund trades
- **Order types** — ราคาตลาด (market price) and ตั้งราคาเอง (limit/custom price)
- **Order confirmation flow** — ตรวจสอบคำสั่ง ("verify order") before submitting
- **Coupon/discount codes** — applied at order time

## Current Status

**Pre-development.** No source code exists yet. The only design artifact is `Designer.png` — a mobile stock-purchase screen showing AAPL with live NASDAQ pricing, THB conversion, and a buy order form.

## Matt Pocock Skills

Skills are managed via `skills-lock.json` (sourced from `mattpocock/skills` on GitHub). Relevant ones for this project:

| Skill | Purpose |
|---|---|
| `grill-me` | Stress-test a plan via relentless Q&A |
| `grill-with-docs` | Grill against specific documentation |
| `prototype` | Build a quick working prototype |
| `to-prd` | Convert a plan into a PRD |
| `to-issues` | Break a plan into tracked issues |
| `tdd` | Test-driven development workflow |
| `diagnose` | Debug/diagnose problems |
| `design-an-interface` | Design a UI/API interface |
