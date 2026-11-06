# Indonesia Market Integrity Project — Brief

Nov 6, 2026 · @Keane
## Project summary

This project tests whether Indonesia's 2026 market-integrity reforms are working, using machine learning and causal methods on Indonesia Stock Exchange (IDX) data. It combines anomaly detection for suspicious trading, an event study around MSCI warnings and regulatory responses, and a live dashboard that tracks the market ahead of MSCI's June 2027 classification decision. The output is a policy brief, a reproducible notebook, and a public Streamlit dashboard.

## Policy question and hypotheses

**Core question:** Have Indonesia's 2026 market-integrity reforms (higher free float, ownership disclosure, enforcement against manipulation) made price behaviour on the IDX more normal and investable?

**Hypotheses**

1. Stocks with low free float or concentrated ownership show more anomalous trading (abnormal volatility, volume spikes, price runs with no news) than other stocks.
2. After the reforms, anomaly rates fall for stocks forced to raise their free float, relative to stocks already compliant.
3. Firm fundamentals (revenue growth, leverage, margins) explain returns better after the reforms than before.
4. MSCI announcements caused larger abnormal returns and outflows for index constituents than for non-constituents.

## Background and context

MSCI has spent 2026 warning that opaque ownership and coordinated trading undermine Indonesia's investability, and Indonesia has responded with a series of reforms. The key events below form the project's event timeline.

| Date (2026) | Event | Source |
| --- | --- | --- |
| Oct 26 | Indonesia adds independent parties to the committee that identifies stocks with concentrated ownership | [The Edge](https://theedgemalaysia.com/node/823195) |
| Oct 15–19 | MSCI warns of a demotion to "standalone" status; deepest two-day selloff on record, index at lowest since 2020 | [The Edge](https://theedgemalaysia.com/node/823195) |
| Oct | OJK sanctions more than a dozen entities for manipulation-related violations | [The Edge](https://theedgemalaysia.com/node/823916) |
| Jun 24 | MSCI extends its review to November, keeping a frontier downgrade on the table | [NST/Reuters](https://www.nst.com.my/amp/business/corporate/2026/06/1471218/msci-extends-indonesia-review-november-flags-downgrade-risk) |
| May 13 | MSCI removes several major Indonesian stocks in its rebalancing review | [Jakarta Post](https://www.thejakartapost.com/business/2026/05/13/idx-falls-as-msci-review-drops-major-indonesian-stocks) |
| Jan 29 | OJK announces the minimum free float will rise to 15% | [Business Indonesia](https://business-indonesia.org/news/ojk-raises-free-float-requirement-to-15-as-idx-suffers-sharp-sell-off) |
| Jan 27–28 | MSCI freezes index changes and warns of a frontier downgrade; IDX trading halted | [Jakarta Post](https://www.thejakartapost.com/business/2026/01/28/idx-plunges-after-msci-warning-about-ri-stocks) |

**Next milestone:** MSCI's market classification decision in June 2027 ([Indonesia Business Post](https://indonesiabusinesspost.com/7657/markets-and-finance/msci-presses-jakarta-to-tackle-market-manipulation)).

## Data sources and access

Start with free sources; upgrade to a paid price API only if yfinance proves unreliable for the dashboard.

| Data | Source | Access | Cost |
| --- | --- | --- | --- |
| Daily prices and volume | yfinance (".JK" tickers) | Python, no key | Free |
| Prices and fundamentals (upgrade) | [EODHD](https://eodhd.com/financial-summary/TLKM.JK) | API key | From US$19.99/mo; fundamentals from US$59.99/mo |
| Free float, shareholders above 1% | IDX website (idx.co.id) | Manual download | Free |
| Ownership composition | KSEI (ksei.co.id) | Manual download | Free |
| Financial statements | IDX filings (XBRL, annual reports) | Download, PDF extraction | Free |
| Manipulation sanctions | OJK announcements (ojk.go.id) | Manual, hand-coded | Free |
| Market classification events | MSCI announcements (msci.com) | Manual, hand-coded | Free |
| Macro (GDP, inflation) | [BPS WebAPI](https://pypi.org/project/stadata/0.1.1) | Free API key (2 subjects: PDB, IHK) | Free |
| Macro cross-check (GDP, inflation) | [World Bank Open Data API](https://data.worldbank.org/) | Python, no key | Free |
| Trade balance (confounder) | [UN Comtrade](https://comtradeplus.un.org/) | Python, no key | Free |
| Rates, rupiah, portfolio flows | Bank Indonesia SEKI | Download | Free |

Keep API keys in environment variables or Streamlit secrets, never in the GitHub repo.

## Methodology

The analysis moves from a simple baseline to ML and causal methods, so each step shows what it adds.

1. **Data pipeline:** pull prices, merge free float and ownership data, and hand-code the event timeline. Flag stocks with free float below 15% or insider ownership of 95% or more.
2. **Baseline:** rule-based anomaly flags, such as returns or volume more than 3 standard deviations above a stock's own history.
3. **ML anomaly detection:** Isolation Forest on trading features (returns, volume, volatility, turnover, price-volume divergence). Where OJK-sanctioned firms are known, use them as labels to check whether the model ranks them as anomalous; compare against the baseline using precision at top-k.
4. **Event study:** abnormal returns around each MSCI and OJK event, comparing index constituents with non-constituents.
5. **Difference-in-differences:** anomaly rates before and after the free float rule, for non-compliant (treated) stocks versus compliant (control) stocks.
6. **Fundamentals model:** gradient boosting (LightGBM) predicting returns from fundamentals, trained separately before and after January 2026, to test whether prices track fundamentals more closely after the reforms.
7. **Interpretation:** SHAP values to explain which features drive anomaly scores and predictions.

**Validation:** time-based splits only (train on earlier periods, test on later), robustness checks with and without flagged stocks, and a regime variable for the period after January 2026.

## Deliverables

Three outputs, each aimed at a different reader.

| Deliverable | Reader | Contents |
| --- | --- | --- |
| Policy brief (2 pages) | Hiring managers, policy teams | Question, key finding, implications for investors and for Singapore's engagement with Indonesia, limitations |
| Live dashboard (Streamlit) | Anyone browsing the portfolio | IDX index vs event timeline, anomaly rate by free float group, flagged stocks, countdown to MSCI June 2027 decision; refreshed daily |
| Notebook and GitHub repo | Technical reviewers | Reproducible pipeline, models, validation, README with setup steps |

## Risks and limitations

The biggest risk is that manipulated prices contaminate the data the models learn from; the mitigations below keep conclusions honest.

| Risk | Mitigation |
| --- | --- |
| Prices distorted by coordinated trading | Rely on fundamentals for growth; treat anomaly scores as signals, not proof |
| Ownership data judged unreliable by MSCI | State this limitation; cross-check IDX and KSEI figures |
| Structural break in 2026 | Regime variable; separate pre- and post-reform models |
| Few confirmed manipulation labels | Use OJK cases for validation only, not as full training labels |
| Confounders (rupiah, global flows, politics) | Macro controls; compare treated and control stocks in the same period |
| Trade balance self-reported, same manipulation-independence concern as other BPS series | Use UN Comtrade instead, which mirrors each flow against partner-country reports |
| yfinance outages or gaps | Cache data locally; EODHD as fallback |
| Defamation risk from naming firms | Show flagged stocks as statistical outliers, with clear wording that this is not an accusation |
| BPS macro figures politically influenced | Cross-check against World Bank Open Data (IMF SDDS-reviewed); use macro series as control variables only, not causal drivers |

## Timeline and milestones

A 12-week plan gets a working version out by end-January 2027, leaving time to update it before MSCI's June 2027 decision.

&#91;embedded content: project plan · 6 phases, 2 milestones\]

The MVP checkpoint (cleaned data, one key chart, a one-page note) is the minimum to protect if time runs short. After publishing, refresh the dashboard daily and add a follow-up post when MSCI announces its decision.

## Portfolio and career relevance

The project shows end-to-end data work on a live regional policy issue, which suits data and policy roles in Singapore's public and financial sectors.

- **Skills shown:** data pipelines, anomaly detection, gradient boosting, event studies, difference-in-differences, SHAP, dashboarding, policy writing.
- **Target employers:** MAS, SGX, MTI, EDB, Enterprise Singapore, ISEAS, regional banks (DBS, UOB, OCBC), consultancies.
- **Why it stands out:** it combines an international relations lens with ML on a story that is unfolding now, and has a natural follow-up when MSCI decides in June 2027.
- **Interview pitch:** "I tested whether Indonesia's 2026 market reforms reduced suspicious trading, and built a dashboard that tracks it ahead of MSCI's decision."
