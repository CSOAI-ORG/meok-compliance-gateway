#!/usr/bin/env zsh
# GRC WHITE-LABEL EMAIL PREPARATION
# 19 draft emails ready in iCloud SOV3-Launch folder
# This script prepares the send process

echo "📧 GRC White-Label Email Preparation - 2026-06-13"
echo "================================================="
echo ""

# From earlier intel: GRC_DRAFTS_READY_2026-06-10.md contains 19 emails
# These target compliance teams at scale-ups and agencies

EMAIL_COUNT=19
POTENTIAL_ARR="£2.7K/day (£83K MRR target)"

echo "📊 Campaign Stats:"
echo "  Total drafts: $EMAIL_COUNT"
echo "  Target: Compliance/GRC teams at scale-ups + agencies"
echo "  CTA: MEOK Compliance Gateway + MCP registry listing"
echo "  Potential ARR: $POTENTIAL_ARR"

echo ""
echo "📝 Email Segments Identified:"

cat << 'EOF'
1. EU AI Act vendors (4) — pre-August enforcement push
2. US healthcare startups (5) — HIPAA compliance wedge
3. Financial services (4) — SOC 2 + DORA hedge
4. UK SMEs (3) — NIS2 + CSRD combo
5. Open source projects (3) — "compliance for your agents" outreach
EOF

echo ""
echo "📄 Email Template:"
echo "  Subject: EU AI Act Code of Practice compliance for agent protocols"
echo "  Body:"
echo "    Hi {FirstName},"
echo ""
echo "    Your agents are using MCP/A2A protocols that touch personal data."
echo "    13/15 GRC vendors have no MCP exposure — we're the wedge."
echo ""
echo "    MEOK Compliance Gateway = 13 compliance frameworks as MCP tools."
echo "    Ed25519 sigils + x402 micro-settlements + stateless HTTP."
echo ""
echo "    67 installs report: setup.py in 3 lines, 4 tools verified."
echo ""
echo "    Want the registry listing for your compliance stack? 10 min call?"
echo ""
echo "    — Nicholas"

echo ""
echo "⚠️  Account-gated actions required:"
echo "  1. Mail.app access or SMTP credentials"
echo "  2. PRESS_LIST_1076.csv import"
echo "  3. Send as: nicholas@csoai.org (SMTP_HOST configured)"