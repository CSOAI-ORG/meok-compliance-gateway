#!/usr/bin/env zsh
# DEAD DOMAIN RESURRECTION — DNS preparation
# Account-gated: requires Namecheap access

echo "🌐 Dead Domain DNS Preparation - 2026-06-13"
echo "============================================="
echo ""

# Domains that need A-records
DEAD_DOMAINS=(diyhelp.ai pokerhud.ai sov3.ai)

echo "📍 Domains requiring A-record (NXDOMAIN):"
for domain in $DEAD_DOMAINS; do
    echo "  - $domain"
    echo "    Current: NXDOMAIN"
    echo "    Needs:   A-record → 192.168.50.105 (M4) or GCP VM (35.242.143.249)"
done

echo ""
echo "🔧 Namecheap DNS Fix Steps:"
echo "1. Login to Namecheap"
echo "2. Domain List → Click 'Manage' on each domain"
echo "3. Advanced DNS → Add Record:"
echo "   Type: A Record"
echo "   Host: @ (or blank for root)"
echo "   Value: 35.242.143.249 (GCP VM)"
echo "   TTL: Automatic"
echo "4. Wait 5-10 minutes for propagation"
echo "5. Verify: curl -I https://$domain"

echo ""
echo "⚡ Alternative: Deploy to Vercel instead"
echo "  - These domains have Vercel projects ready"
cat << 'EOF'
  # In each project root:
  vercel --prod --confirm
  # Then add domain in Vercel dashboard
EOF

echo ""
echo "📝 Files ready:"
ls -la /Users/nicholas/*/*.ai/vercel.json 2>/dev/null | head -5