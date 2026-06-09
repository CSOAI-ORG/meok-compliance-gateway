# DNS Configuration Templates for 28 MEOK Domains
# Generated for Namecheap / Cloudflare / Route53
# All domains point to Vercel deployment

# ============================================
# VERCEL CNAME TARGET (same for all)
# ============================================
# After Vercel deploy, each project gets a unique *.vercel.app URL
# Format: <project-name>.vercel.app
# Use CNAME for apex domains (requires CNAME flattening support)
# Use ALIAS/ANAME for root if CNAME not supported

# ============================================
# TEMPLATE PER DOMAIN
# ============================================
# For each domain <domain>.ai:
# 
# Type    | Host | Value                          | TTL
# --------|------|--------------------------------|-----
# CNAME   | @    | <vercel-project>.vercel.app   | 300
# CNAME   | www  | <vercel-project>.vercel.app   | 300
# TXT     | @    | vercel-verification=<token>   | 300
# CAA     | @    | 0 issue "letsencrypt.org"     | 300

# ============================================
# 28 DOMAINS - COPY PASTE INTO NAMECHEAP
# ============================================


# ---- accountabilityof.ai ----
# CNAME   @    accountabilityof-hive.vercel.app    300
# CNAME   www  accountabilityof-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- agisafe.ai ----
# CNAME   @    agisafe-hive.vercel.app    300
# CNAME   www  agisafe-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- asisecurity.ai ----
# CNAME   @    asisecurity-hive.vercel.app    300
# CNAME   www  asisecurity-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- biasdetectionof.ai ----
# CNAME   @    biasdetectionof-hive.vercel.app    300
# CNAME   www  biasdetectionof-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- cobolbridge.ai ----
# CNAME   @    cobolbridge-hive.vercel.app    300
# CNAME   www  cobolbridge-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- commercialvehicle.ai ----
# CNAME   @    commercialvehicle-hive.vercel.app    300
# CNAME   www  commercialvehicle-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- councilof.ai ----
# CNAME   @    councilof-hive.vercel.app    300
# CNAME   www  councilof-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- csoai.ai ----
# CNAME   @    csoai-hive.vercel.app    300
# CNAME   www  csoai-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- dataprivacyof.ai ----
# CNAME   @    dataprivacyof-hive.vercel.app    300
# CNAME   www  dataprivacyof-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- diyhelp.ai ----
# CNAME   @    diyhelp-hive.vercel.app    300
# CNAME   www  diyhelp-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- ethicalgovernanceof.ai ----
# CNAME   @    ethicalgovernanceof-hive.vercel.app    300
# CNAME   www  ethicalgovernanceof-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- fishkeeper.ai ----
# CNAME   @    fishkeeper-hive.vercel.app    300
# CNAME   www  fishkeeper-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- grabhire.ai ----
# CNAME   @    grabhire-hive.vercel.app    300
# CNAME   www  grabhire-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- koikeeper.ai ----
# CNAME   @    koikeeper-hive.vercel.app    300
# CNAME   www  koikeeper-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- landlaw.ai ----
# CNAME   @    landlaw-hive.vercel.app    300
# CNAME   www  landlaw-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- loopfactory.ai ----
# CNAME   @    loopfactory-hive.vercel.app    300
# CNAME   www  loopfactory-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- meok-compliance-gateway.ai ----
# CNAME   @    meok-compliance-gateway-hive.vercel.app    300
# CNAME   www  meok-compliance-gateway-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- meok.ai ----
# CNAME   @    meok-hive.vercel.app    300
# CNAME   www  meok-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- muckaway.ai ----
# CNAME   @    muckaway-hive.vercel.app    300
# CNAME   www  muckaway-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- openMCP.ai ----
# CNAME   @    openMCP-hive.vercel.app    300
# CNAME   www  openMCP-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- openmoe.ai ----
# CNAME   @    openmoe-hive.vercel.app    300
# CNAME   www  openmoe-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- optimobile.ai ----
# CNAME   @    optimobile-hive.vercel.app    300
# CNAME   www  optimobile-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- planthire.ai ----
# CNAME   @    planthire-hive.vercel.app    300
# CNAME   www  planthire-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- pokerhud.ai ----
# CNAME   @    pokerhud-hive.vercel.app    300
# CNAME   www  pokerhud-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- proofof.ai ----
# CNAME   @    proofof-hive.vercel.app    300
# CNAME   www  proofof-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- safetyof.ai ----
# CNAME   @    safetyof-hive.vercel.app    300
# CNAME   www  safetyof-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- socialmediamananger.ai ----
# CNAME   @    socialmediamananger-hive.vercel.app    300
# CNAME   www  socialmediamananger-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300


# ---- transparencyof.ai ----
# CNAME   @    transparencyof-hive.vercel.app    300
# CNAME   www  transparencyof-hive.vercel.app    300
# TXT     @    vercel-verification=<GET_FROM_VERCEL_DASHBOARD>  300
# CAA     @    0 issue "letsencrypt.org"     300

