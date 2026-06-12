## 10. GEO/AEO Optimization Playbook

Generative Engine Optimization (GEO) and Answer Engine Optimization (AEO) represent the most significant shift in digital visibility since mobile-first indexing. AI Overviews now appear in 18-21% of Google searches [^468^], ChatGPT processes 2.5 billion prompts daily [^496^], and AI-referred sessions have grown 527% year-over-year [^512^]. For the 25-domain portfolio, these changes redefine how content must be structured, maintained, and measured. This chapter provides a platform-specific playbook covering AI Overview optimization, featured snippet domination, voice search strategy, and LLM citation building, with implementation frameworks tailored to each domain cluster.

---

### 10.1 AI Overview Optimization

#### 10.1.1 Twelve Key Strategies for Google AI Overviews

Google AI Overviews appear in 18-21% of searches, with prevalence varying by vertical: Science (25.96%), Computers & Electronics (17.92%), and People & Society (17.29%) lead [^468^]. Critically, 99.5% of AI Overview sources originate from the top 10 organic results [^468^], making traditional SEO foundations the non-negotiable prerequisite for GEO success. Google's guidance confirms this integration: AI Overviews are rooted in the same core ranking and quality systems as regular Search [^496^].

The Princeton/Georgia Tech GEO study — testing 9 optimization methods across 10,000 diverse queries — found that expert quotations increase AI visibility by 35%, verifiable statistics by 40%, and authoritative citations by 40% [^482^]. The optimal combination, fluency plus statistics together, delivers a 45.5% visibility lift [^482^]. Keyword stuffing reduces AI visibility by 9%, underscoring the divergence between legacy SEO manipulation and GEO best practices [^482^].

![Princeton GEO Study: AI Citation Visibility Lift by Optimization Tactic](chart_sec10_princeton_geo_tactics.png)

The twelve core strategies, synthesized from cross-platform analysis [^468^] [^470^], are: (1) place direct answers within the first 50-70 words; (2) align content with search intent rather than keyword density; (3) open with plain, natural-language factual sentences; (4) use descriptive H2/H3 subheadings that explicitly state the question being answered; (5) format for extraction using numbered steps, bullet lists, and comparison tables; (6) embed expertise signals including author bios with credentials; (7) deploy FAQ, HowTo, and Article schema markup; (8) maintain freshness with updated timestamps; (9) strengthen topical coverage through internal linking clusters; (10) ensure technical fundamentals including page speed and mobile usability; (11) incorporate visuals with descriptive alt text; and (12) monitor AI Overview citation performance weekly.

Pages with FAQPage schema are 3.2 times more likely to appear in AI Overviews, and content with proper schema markup has a 2.5x higher chance of inclusion in AI-generated answers [^471^]. For the portfolio's AI governance cluster, every policy explainer should carry FAQPage schema with 40-60 word answers. Construction domains should prioritize HowTo schema for equipment guides, while hobby domains benefit from combining HowTo with VideoObject markup for tutorial content.

#### 10.1.2 ChatGPT/Perplexity/Gemini Citation Optimization

Each AI platform exhibits fundamentally different citation behavior — no single strategy wins across all three major engines [^474^]. ChatGPT accounts for 64.1% of analyzed AI citations, preferring webpage content (47%), and lifts TL;DRs verbatim [^474^]. Perplexity contributes 20.8%, favoring blog and article content (54.8%), and weights freshness highest [^474^]. Gemini accounts for 15.1% and deliberately avoids community sources [^474^]. The overlap is minimal: 89% of sources cited by one platform are not cited by the others [^509^].

**ChatGPT** prioritizes brand entity recognition, requiring consistent mentions across authoritative sources and Wikipedia presence (47.9% top source preference). Seventy-six point four percent of its top-cited pages were updated within 30 days [^467^]. For the portfolio, each domain must establish itself as a distinct entity through Organization schema, sameAs links, and third-party profiles on Crunchbase, LinkedIn, and industry directories.

**Perplexity** values freshness as the primary lever, with 46.7% top source preference for Reddit and 3-4 mandatory clickable citations per response [^467^]. Maintaining active, helpful presence on relevant Reddit communities significantly improves Perplexity citation rates across all verticals.

**Google AI Overviews** maintain the strongest correlation with traditional organic rankings (93.67% from top-10 results), making technical SEO the most impactful lever [^467^]. **Claude** operates as the most conservative citer, preferring fewer, higher-authority sources [^467^].

Citation eligibility begins with crawler access. Every domain must allow OAI-SearchBot, GPTBot, PerplexityBot, ClaudeBot, Google-Extended, and Applebot-Extended in robots.txt [^467^]. Most citation failures trace to five fixable mistakes: buried answers, branded headings, missing JSON-LD, crawler blocks, and zero outbound citations [^467^].

#### 10.1.3 Schema Types by Domain Cluster

| Schema Type | AI Governance (9 domains) | Construction (5 domains) | Hobby/Lifestyle (4 domains) | Professional Services (7 domains) | Priority |
|-------------|---------------------------|--------------------------|----------------------------|-----------------------------------|----------|
| **FAQPage** | Critical — policy Q&A [^471^] | High — service FAQs [^52^] | Critical — hobby Q&A [^52^] | High — process FAQs | P0 |
| **HowTo** | High — framework guides | Medium — equipment guides | Critical — tutorials [^52^] | Medium — process guides | P0 Hobby; P1 Others |
| **Article** | High — thought leadership [^475^] | Medium — industry news | High — blog content | High — case studies | P1 |
| **Organization** | Critical — entity recognition [^475^] | Critical — LocalBusiness | High — brand entity | Critical — ProfessionalService | P0 |
| **Product** | N/A | Critical — equipment [^58^] | High — equipment reviews | Medium — software/tools | P0 Construction |
| **VideoObject** | Medium | Low | High — tutorials [^498^] | Medium | P1 Hobby |
| **Person** | High — expert bios [^475^] | Low | Medium | High — provider profiles | P1 |
| **BreadcrumbList** | High | High | High | High | P0 |

FAQPage schema delivers the highest ROI per implementation hour across all 25 domains — FAQ and HowTo schemas boost visibility by 30-40% with minimal effort [^471^]. AI governance domains should layer Organization schema with sameAs links to Wikidata and academic profiles. Construction domains require LocalBusiness schema for every service area page given that 80%+ of hire searches carry local intent [^72^]. Hobby domains benefit most from HowTo schema paired with VideoObject, since HowTo increases citation rates approximately 1.7x for instructional queries.

---

### 10.2 Featured Snippet and PAA Domination

#### 10.2.1 Featured Snippet Formats by Content Type

Featured snippets remain the most powerful zero-click visibility tool, with approximately 41% of voice search results sourced directly from them [^504^]. Four primary formats dominate SERPs [^504^] [^509^].

**Paragraph snippets** (40-60 words) answer "how," "what," and "why" questions. The winning structure places the answer in the opening sentence immediately below an H2 heading matching the query verbatim. AI governance domains should prioritize this format because definitional queries — "What is AI accountability?" — dominate informational search in this vertical.

**List snippets** use bullet points or numbered steps for "how-to" queries. Each item should be one sentence with consistent formatting. The hobby cluster should prioritize list snippets for care guides and troubleshooting workflows.

**Table snippets** compare data across 3-4 rows and 2-3 columns. The construction cluster has the highest table-snippet opportunity: equipment comparisons and pricing matrices map naturally to this format.

**Definition snippets** provide concise definitions followed by elaboration. AI governance domains targeting emerging terminology — "What is Constitutional AI?" — should capture definitional queries before competitors establish ownership.

Three universal rules govern optimization: H2 wording must match target queries verbatim; the first sentence must answer in isolation; and content must stay within each format's length cap [^47^].

#### 10.2.2 PAA Box Optimization

People Also Ask (PAA) boxes function as dynamic, AI-powered follow-up question interfaces. Google's June 2025 Core Update filters AI-generated filler content from PAA, meaning winning content must combine efficiency with genuine expertise [^55^]. Sites creating multi-format content — PAA sections, AI Overview targets, and traditional snippets — perform best [^55^].

The optimization process begins with research: extract all PAA questions using AlsoAsked or AnswerThePublic, group by intent, and create dedicated FAQ sections with H2 headings matching PAA phrasing exactly, followed by 40-60 word direct answers [^468^]. AI governance domains should target policy follow-ups: "What are the penalties for EU AI Act non-compliance?" Construction domains optimize for operational questions: "How much does grab hire cost per day?" Hobby domains capture beginner questions: "What is the best fish for beginners?"

#### 10.2.3 Featured Snippet Opportunity Map

The following heatmap visualizes featured snippet opportunity scores by domain cluster and snippet format, derived from query pattern analysis across each vertical.

![Featured Snippet Opportunity Map by Domain Cluster](chart_sec10_snippet_opportunity_map.png)

The map reveals clear vertical-specific patterns. AI governance domains score highest on paragraph (9/10) and definition (9/10) snippets because the vertical is dominated by definitional queries. The construction cluster peaks at table snippets (9/10) because equipment hire decisions require structured comparisons across pricing, specifications, and availability. Hobby domains show the strongest list-snippet opportunity (9/10), as care guides and tutorials naturally decompose into sequential steps. Professional services present the most balanced profile (7-8 across all formats), reflecting query diversity. These scores should guide content format investment: governance domains prioritize definitional paragraphs, construction domains build comparison tables, and hobby domains focus on numbered step-by-step guides.

---

### 10.3 Voice Search and Zero-Click Strategy

#### 10.3.1 Voice Search Optimization

Voice search accounts for 20.5% of global internet user queries, with voice queries averaging 29 words compared to 1-3 words for typed search [^504^] [^507^]. Voice searches are 7 times more likely to include question words than typed searches [^504^]. Critically, 41% of voice search results come directly from featured snippets [^504^], linking voice strategy inseparably to snippet optimization.

The 29-word average query length fundamentally changes keyword targeting. Instead of optimizing for "AI governance framework," voice-optimized content must target "What is the best AI governance framework for small businesses?" For all 25 domains, H2 headings should be rewritten as complete questions: not "Benefits of ISO 42001" but "What are the benefits of ISO 42001 for AI governance?"

Technical requirements are stringent: voice search result pages load 52% faster than typical pages, and websites with schema are 4 times more likely to appear in voice search [^504^]. Reading level matters too — voice assistants prefer content at an 8th-9th grade level, requiring complex AI governance concepts to be simplified without sacrificing accuracy.

#### 10.3.2 Zero-Click Strategy

Sixty-five percent of Google searches end without a click [^496^]. In Google AI Mode, the zero-click rate reaches 93%, and organic CTR for queries with AI Overviews has dropped 61% — from 1.76% to 0.61% [^513^]. GEO value is often zero-click: content is read without the user visiting the site, and brand awareness compounds at the point of consumption [^496^].

The strategic response requires four mechanisms: structure content as the source AI selects through 40-60 word direct answers and schema markup; ensure the brand name appears in extractable content; deploy structured data for rich results eligibility; and monitor brand mention frequency even without clicks, since AI-referred visitors convert at 23 times the rate of traditional organic visitors [^512^].

Segmentation distinguishes when to optimize for visibility versus clicks. Top-of-funnel informational queries — "What is AI bias?" — optimize for zero-click visibility. Mid-funnel consideration queries — "Best AI governance platforms comparison" — optimize for clicks with compelling meta descriptions. Bottom-funnel transactional queries — "Hire mini digger London" — require aggressive click-through optimization.

#### 10.3.3 Voice Search Keyword Variations by Domain Cluster

| Domain Cluster | Typed Query | Voice Query Variation | Conversational H2 Target | Priority Domains |
|----------------|------------|----------------------|--------------------------|-----------------|
| **AI Governance** | "AI governance framework" | "What is the best AI governance framework for my company?" | "What AI governance framework should small businesses use?" | accountabilityof.ai, ethicalgovernanceof.ai, councilof.ai |
| **AI Safety** | "AGI safety principles" | "What are the main safety principles for artificial general intelligence?" | "What safety principles should AGI developers follow?" | agisafe.ai, safetyof.ai, asisecurity.ai |
| **Construction Hire** | "grab hire near me" | "Where can I hire a grab truck near me today?" | "Where to hire grab trucks with same-day delivery" | grabhire.ai, planthire.ai, muckaway.ai |
| **Fishkeeping** | "koi pond maintenance" | "How do I maintain a koi pond in winter?" | "How to maintain a healthy koi pond during winter" | fishkeeper.ai, koikeeper.ai |
| **DIY** | "fix leaking tap" | "How do I fix a leaking kitchen tap myself?" | "How to fix a leaking kitchen tap step by step" | diyhelp.ai |
| **Crisis Support** | "suicide helpline" | "What do I do if I'm thinking about suicide?" | "What should you do if you're having thoughts of suicide?" | suicidestop.ai |
| **Food Tech** | "meal planning app" | "What is the best app for planning my meals every week?" | "What is the best meal planning app for busy people?" | meok.ai, openmoe.ai |
| **Legal** | "land law guide" | "What are my rights as a landowner in the UK?" | "What rights do UK landowners have under current law?" | landlaw.ai |
| **Gaming Tools** | "poker HUD software" | "What is the best poker HUD software for beginners?" | "What poker HUD software should beginners use?" | pokerhud.ai |

The voice query variations reveal a consistent pattern: voice searches add contextual qualifiers ("for my company," "in winter," "step by step") that typed queries omit. Every domain should maintain a voice keyword map where each primary target expands into 3-5 conversational long-tail variants, with H2 headings mirroring spoken patterns exactly. Construction domains have additional voice opportunity through local intent: 76% of local voice searches convert to visits within 24 hours [^87^], making "near me" and "today" qualifiers high-value targets for grabhire.ai and planthire.ai.

---

### 10.4 Citation Building for LLMs

#### 10.4.1 Seven-Step Citation Framework

**Step 1: Identify 10 key questions** your target audience asks AI platforms. AI governance domains target "What is the EU AI Act compliance checklist?"; construction domains target "How much does plant hire cost?"

**Step 2: Audit current citations** manually across ChatGPT, Perplexity, Gemini, and Claude to establish a baseline.

**Step 3: Build dedicated answer pages** for each key question, opening with a 40-60 word self-contained answer under an H2 matching the query verbatim. AI engines score passages, not documents [^467^].

**Step 4: Structure for extraction** using Princeton GEO findings: add verifiable statistics (+40% visibility), cite authoritative sources (+40%), and include expert quotations (+35%). The fluency-plus-statistics combination delivers +45.5% [^482^].

**Step 5: Earn third-party mentions** across review platforms, forums, and publications. Brands with active Trustpilot, G2, and Capterra profiles have a 3x higher chance of being cited by ChatGPT [^486^]. AI governance domains should prioritize academic citations; construction domains should target trade publications; hobby domains should engage Reddit communities, given that 46.5% of Perplexity citations draw from Reddit [^474^].

**Step 6: Optimize per platform.** ChatGPT requires Wikipedia presence and consistent authoritative mentions. Perplexity demands maximum freshness. Google AI Overviews depend on rankings and schema. Claude requires being among the most-cited pages for a topic across the broader web [^467^] [^481^].

**Step 7: Measure and iterate** through weekly citation audits tracking citation share, position in answers, verbatim quotation rate, and surrounding sentiment [^482^].

#### 10.4.2 Citation Measurement Framework

| Metric | Weekly Target | Measurement Method | Benchmark | Action Trigger |
|--------|--------------|--------------------|-----------|---------------|
| **Citation frequency** | 5+ per domain | Audit across ChatGPT, Perplexity, Gemini, Claude | 5-10% lift post-refresh [^509^] | <3 = content refresh |
| **Citation rate** | 40%+ of queries | (Cited / Total) x 100 | 12% to 47% (292% improvement) [^509^] | <20% = rewrite |
| **Verbatim quotation rate** | 30%+ | Manual review | Higher = stronger extraction | <15% = reformat |
| **Positive sentiment** | 90%+ | Qualitative review | Neutral/positive acceptable | Negative = review |
| **AI referral traffic** | Growing WoW | GA4 custom channel [^482^] | 23x conversion vs. organic [^512^] | 2-week decline = audit |
| **Content freshness** | 100% <13 weeks | lastmod date audit | 50% of cited content <13 weeks [^512^] | >12 weeks = queue refresh |
| **Brand mentions** | 10+ unlinked/week | Ahrefs Alerts, Brand24 | 60% of mentions unlinked [^51^] | New = outreach |

The weekly audit follows a structured cadence [^482^]: define 20-50 target queries per cluster; sample each platform with standardized prompts; record citation presence, position, and context; track the seven metrics above; and iterate by refreshing underperforming content, adding missing schema, and expanding high-opportunity topic clusters. GA4 should be configured with a custom "AI Traffic" channel using the regex `chatgpt\.com|perplexity\.ai|claude\.ai|gemini\.google\.com` [^482^]. True AI influence is estimated at 2-3x reported analytics because mobile app visits and zero-click consumption evade standard referral tracking.

#### 10.4.3 Content Freshness Tiers

Content freshness operates as a competitive moat. Fifty percent of AI-cited content is under 13 weeks old, 76.4% of ChatGPT's top-cited pages were updated within 30 days, and pages not refreshed quarterly are 3 times more likely to lose citations [^512^] [^509^]. A three-tier system allocates resources efficiently.

**Monthly tier** applies to AI governance domains (accountabilityof.ai, ethicalgovernanceof.ai, biasdetectionof.ai, safetyof.ai, transparencyof.ai, dataprivacyof.ai, councilof.ai, proofof.ai). This content ages rapidly as regulations evolve: EU AI Act enforcement timelines, 550+ US state bills, and emerging NIST guidance create constant change. Monthly updates replace statistics, refresh policy references, and update dateModified schema. A documented case showed a page going from 0/10 to 7/10 AI citations after a 3-hour refresh — pages meeting all five refresh criteria achieved an 83% citation rate [^518^].

**Quarterly tier** covers stable topics across construction, hobby, and professional services domains. Equipment specifications, care guides, and service processes change slowly; quarterly updates verify accuracy and ensure content remains within the 13-week freshness window.

**Event-triggered tier** activates on regulatory changes, product launches, and crisis events. For AI governance, EU AI Act milestones and new ISO standard releases trigger immediate updates. For suicidestop.ai, helpline number changes require same-day updates under YMYL standards. Construction domains should refresh pricing when fuel costs shift significantly.

The "Red Queen" dynamic — where domains must publish continuously to maintain rankings — is a competitive moat, not a weakness [^512^]. Organizations unable to sustain systematic refresh operations will drop out of AI Overviews and GEO citations permanently. Domains with tiered refresh systems, editorial calendars, automated regulatory alerts, and quarterly audit protocols compound their advantage while competitors fall behind.

---

*This playbook integrates GEO, AEO, and traditional SEO into a unified optimization framework. Implementation should proceed in parallel across all 25 domains, with cluster-specific prioritization guided by the schema, voice search, and citation measurement tables in each section.*
