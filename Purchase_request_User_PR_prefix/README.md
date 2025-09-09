# Purchase Request User PR Prefix & Auto Number

[English] | [中文说明](README.zh.md)

Adds a PR Prefix on users and generates Purchase Request numbers with that prefix and year-based sequences.

## Features
- Per-user PR Prefix field (e.g., `K1-WH-PR-`)
- Auto number format: `PREFIXYYYY-####` (e.g., `K1-WH-PR-2025-0001`)
- Yearly sequence reset
- Works with OCA `purchase_request`
- Used by other modules (e.g., department approval) to partition data by prefix

## Installation
- Dependencies: `base`, `purchase_request`
- Install via Apps; set each user’s PR Prefix in Access Rights

