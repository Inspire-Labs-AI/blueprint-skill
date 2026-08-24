# Blueprint — MProfit (https://www.mprofit.in/)

Master synthesis document. Target: MProfit, an Indian multi-asset portfolio
management + investment-accounting product for retail investors, HNIs, family
offices and wealth professionals (advisors, distributors, RIAs, CAs).

Evidence basis: 14 recon screenshots + rendered DOM (public site only). Every
claim below is tagged `observed` (seen in a shot/DOM) or `inferred` (reasoned).
The actual application is behind `/login`, so all app-internal claims are
`[inferred — behind auth]`.

---

## 1. Overview

MProfit is an automated, multi-asset **portfolio tracker + investment
accounting** platform for the Indian market. Its core promise (`observed`,
root.png hero): *"Manage your investments the right way — consolidate multi-asset
investments for your family in one place, auto-import trade data from 700+
brokers, track XIRR & get capital gain reports in ITR format."* It serves two
distinct buyer groups from one engine (`observed`, root + pricing + sign_up):
**Investors** (individuals, traders, HNIs, family offices) and **Wealth
Professionals** (financial advisors, distributors, RIAs, chartered accountants
who manage client portfolios). The differentiating value is the **auto-import**
pipeline that ingests contract notes, CAS files and back-office statements from
700+ brokers/institutions and normalizes them into a unified, tax-aware ledger
(capital gains in ITR format, grandfathering, XIRR). Social proof is heavy:
"200,000+ sign-ups", "300+ cities", "700+ supported institutions", $2mn raise
from Zerodha's Rainmatter/Enam (`observed`, root banner + stats strip).

---

## 2. Feature map

### Public marketing site (`observed`)
- **Home** (`/`) — hero, stats (200k+ sign-ups, 300+ cities, 700+ institutions),
  "Featured in" (ET, Mint, Inc42, YourStory, VCCircle, BW Disrupt), trust logos
  (Barclays, CGS-CIMB, JM Financial, Pidilite, Shemaroo, Trade Smart, Bharat
  Forge/Kalyani, Capitalmind), 4 personas (Investors / Family Offices /
  Financial Advisors / Chartered Accountants).
- **Features** (`/features`) — asset-class tracking, multiple portfolios &
  portfolio groups, auto-import from 700+ brokers, F&O position tracking,
  mobile/web/anywhere access, live prices + corporate-action updates, Capital
  Gains in ITR format, analytical/performance insights (XIRR, asset allocation,
  income/dues/transactions reports), and "provide MProfit logins to your
  clients" for wealth pros.
- **Pricing** (`/pricing`) — splits into two subscription tracks: **For
  Investors** and **For Wealth Professionals** (each a separate sub-page/route,
  `[inferred — not captured]`). DOM mentions plan tokens "Basic", "Investor",
  "Professional".
- **Import** (`/import`) — searchable directory of supported brokers/banks,
  grouped: Stockbrokers, Mutual Fund files & statements, Banks & Credit Card
  statements, Back-office & Trade-book files, PMS statements, Other files
  (MProfit Bond / Deposit / Insurance / EPF-PPF / Loan / ULIP / Fixed &
  Private Equity / eNPS / SBICAPS Bond transactions). Search box + asset-type
  filter dropdown.
- **About** (`/about`), **Reviews** (`/reviews`, 500+ testimonials, paginated
  ~10 pages, EmbedSocial-style cards + "Featured in" ET Now / Outlook Money),
  **Blog** (`/blog`), **Refer / Referral Program** (`/refer`), **Contact Us**
  (`/contact-us`, routed through Freshworks widget — no native form in DOM),
  **Terms of Use** (`/terms-of-use`), **Privacy Policy** (`/privacy`).
- **Mobile apps** — App Store + Google Play badges (`observed`, footer).

### Auth / conversion gates (`observed` shell, flow `[inferred — behind auth]`)
- **Sign up** (`/sign-up`) — persona chooser: "I am an Investor" vs "I am a
  Wealth Professional" (two cards).
- **Login** (`/login`) — **email-first, passwordless-style**: single Email
  field → "Continue" (`observed`). A secondary "Login to **MProfit Cloud**
  instead" button implies two runtimes: a legacy **desktop** product and
  **MProfit Cloud** (web/mobile). Password/OTP step served after Continue
  `[inferred — behind auth]`.
- **Buy / Subscribe** (`/buy`) — "Subscribe to MProfit → Login to your MProfit
  account" email gate, then plan checkout `[inferred — behind auth]`.

### Gated application (all `[inferred — behind auth]`, corroborated by product screenshots on marketing pages)
- Portfolio dashboard: "My Family" view, tabs PMS / F&O / ACT / All / Stocks /
  Mutual Funds / Traded Bonds / FDs / Insurance; Net Worth, Asset Allocation
  pie, holdings tables with Avg/Buy price, current value, gain %.
- Multi-portfolio + portfolio-group management (individual + consolidated +
  family view; advisor client grouping).
- Auto-import engine: email-forwarding rule per file type, parsing of contract
  notes / CAS / RTA / back-office / PMS / NPS files (PDF, Excel, HTML, CSV, TXT,
  DBF).
- F&O position book (mark-to-market, realized/unrealized P&L).
- Live prices + EOD NAV + corporate actions (dividend, bonus, split, merger,
  demerger).
- Capital Gains reports (ITR format, LTCG grandfathering + indexation),
  export compatible with ClearTax/Winman/CompuTax.
- Analytics/AUM reports for advisors; client-login provisioning + white-label
  branding on reports.

---

## 3. Tech stack (observed)

| Layer | Evidence | Conclusion |
|---|---|---|
| Site generator | `<meta name="generator" content="Gatsby 2.23.3">` (sign_up.html) | **Gatsby v2** static site (React SSR/SSG) |
| UI framework | `data-react-helmet` attrs on `<html>`; react-helmet in head; hashed chunk `component---src-pages-index-js-*.js` | **React** (Gatsby's page-component code-splitting) |
| Bundling | `commons-*.js`, `styles-*.js`, `styles.e6884ef521d01e587d5a.css`, SHA-named chunks | Webpack (Gatsby default) |
| Carousels | `slick-slider` / `slick-track` CSS classes | **react-slick / slick-carousel** |
| Fonts | Google Fonts `@import`: Source Sans Pro, Poppins, Open Sans, Material Icons | Google Fonts CDN |
| Analytics | `googletagmanager`, `gtag`, `google-analytics` refs | **Google Tag Manager + GA** |
| Support/chat | `fwSettings`, `Freshworks`, freshworks widget refs | **Freshworks (Freshchat/Freshdesk)** — also powers Contact Us + "MProfit Help Center" |
| Payments | `stripe` refs in head | **Stripe** loaded on public pages (subscription checkout) `inferred` |
| Reviews widget | `EmbedSocialHashtagScript` (`embedsocial.com/cdn/ht.js`) | **EmbedSocial** for testimonials |
| Hosting/domain | assets served same-origin `/…` under `www.mprofit.in` | Static host / CDN `inferred` |
| App backend | not exposed on marketing site | separate API + "MProfit Cloud" app `[inferred — behind auth]` |

The marketing site (`www.mprofit.in`) is a **decoupled Gatsby static front-end**.
The actual product ("MProfit Cloud") is a **separate authenticated application**
(different runtime, likely different subdomain/stack) plus a **legacy Windows
desktop** app — the login page explicitly distinguishes them.

---

## 4. Data model

Inferred from the portfolio UI, import categories, asset tabs and report types.
All app tables are `[inferred — behind auth]`.

```prisma
// ---- Identity & tenancy ----
model User {
  id            String   @id @default(cuid())
  email         String   @unique          // login is email-first
  name          String?
  userType      UserType                   // INVESTOR | WEALTH_PRO
  phone         String?
  createdAt     DateTime @default(now())
  families      Family[]
  clients       Client[]                   // wealth-pro -> managed clients
  subscription  Subscription?
}

enum UserType { INVESTOR WEALTH_PRO }

// A wealth professional manages many clients; each client owns portfolios.
model Client {
  id        String @id @default(cuid())
  advisorId String
  advisor   User   @relation(fields: [advisorId], references: [id])
  name      String
  email     String?
  hasLogin  Boolean @default(false)        // "provide MProfit logins to clients"
  families  Family[]
}

// "My Family" view = grouping of portfolios (self + dependents)
model Family {
  id         String      @id @default(cuid())
  ownerId    String
  owner      User        @relation(fields: [ownerId], references: [id])
  clientId   String?
  name       String
  portfolios Portfolio[]
}

model Portfolio {
  id         String      @id @default(cuid())
  familyId   String
  family     Family      @relation(fields: [familyId], references: [id])
  name       String
  groupId    String?                        // portfolio groups
  group      PortfolioGroup? @relation(fields: [groupId], references: [id])
  holdings   Holding[]
  transactions Transaction[]
}

model PortfolioGroup {
  id         String      @id @default(cuid())
  ownerId    String
  name       String
  portfolios Portfolio[]
}

// ---- Instruments & holdings ----
enum AssetClass {
  STOCK MUTUAL_FUND TRADED_BOND FD PMS AIF FNO INSURANCE
  BOND DEPOSIT EPF_PPF NPS ULIP LOAN CASH REAL_ESTATE OTHER
}

model Instrument {
  id         String     @id @default(cuid())
  assetClass AssetClass
  symbol     String?                         // ticker / ISIN / scheme code
  isin       String?
  name       String
  exchange   String?                         // NSE/BSE
  prices     PriceQuote[]
  corpActions CorporateAction[]
}

model Holding {
  id           String     @id @default(cuid())
  portfolioId  String
  portfolio    Portfolio  @relation(fields: [portfolioId], references: [id])
  instrumentId String
  instrument   Instrument @relation(fields: [instrumentId], references: [id])
  quantity     Decimal
  avgBuyPrice  Decimal
  currentValue Decimal                        // recomputed from PriceQuote
  unrealizedPL Decimal
}

model Transaction {
  id           String     @id @default(cuid())
  portfolioId  String
  instrumentId String
  type         TxnType                        // BUY SELL DIVIDEND BONUS SPLIT ...
  quantity     Decimal
  price        Decimal
  amount       Decimal
  tradeDate    DateTime
  charges      Decimal?                       // brokerage/taxes from contract note
  sourceFileId String?                        // provenance -> ImportJob
  import       ImportJob? @relation(fields: [sourceFileId], references: [id])
}

enum TxnType { BUY SELL DIVIDEND BONUS SPLIT MERGER DEMERGER INTEREST OTHER }

// ---- Auto-import pipeline (the core moat) ----
model Broker {
  id        String   @id @default(cuid())
  name      String                            // "Zerodha", "ICICI Direct" ...
  category  BrokerCategory                     // grouping on /import page
  fileFormats String[]                         // PDF, Excel, HTML, CSV, TXT, DBF
}

enum BrokerCategory {
  STOCKBROKER MUTUAL_FUND_STATEMENT BANK_CC_STATEMENT
  BACKOFFICE_TRADEBOOK PMS_STATEMENT OTHER_FILE
}

model ImportJob {
  id         String   @id @default(cuid())
  userId     String
  brokerId   String?
  fileName   String
  fileType   String
  status     ImportStatus                      // via email-forward rule or upload
  parsedRows Int?
  createdAt  DateTime @default(now())
  transactions Transaction[]
}

enum ImportStatus { PENDING PARSING PARSED FAILED REVIEW }

// ---- Market data ----
model PriceQuote {
  id           String   @id @default(cuid())
  instrumentId String
  date         DateTime
  price        Decimal                         // live for equity/ETF, EOD NAV for MF
  @@unique([instrumentId, date])
}

model CorporateAction {
  id           String   @id @default(cuid())
  instrumentId String
  type         TxnType                          // dividend/bonus/split/merger...
  exDate       DateTime
  ratio        String?
}

// ---- Reporting / tax ----
model CapitalGainRecord {
  id          String   @id @default(cuid())
  portfolioId String
  instrumentId String
  buyDate     DateTime
  sellDate    DateTime
  gainType    String                            // STCG | LTCG
  grandfathered Boolean @default(false)         // pre-2018 LTCG grandfathering
  indexedCost Decimal?
  gainAmount  Decimal
}

// ---- Billing ----
model Subscription {
  id        String   @id @default(cuid())
  userId    String   @unique
  plan      String                              // Basic / Investor / Professional
  track     UserType                            // Investor vs Wealth-Pro pricing
  status    String
  provider  String   @default("stripe")
  renewsAt  DateTime?
}
```

Top inferred tables: **Portfolio, Holding, Transaction, Instrument, ImportJob,
Broker, CapitalGainRecord** — the import→transaction→holding→capital-gain chain
is the product's spine.

---

## 5. API surface

Marketing site is static (no XHR observed in DOM). App endpoints are `inferred`
(`[behind auth]`). Paths are illustrative REST guesses.

| Feature | Method + path | Purpose | Tag |
|---|---|---|---|
| Login (email step) | `POST /api/auth/check-email` | email-first; branch to password/OTP or "Cloud" | inferred |
| Login (complete) | `POST /api/auth/login` | issue session/JWT | inferred |
| Sign up | `POST /api/auth/signup` | create user w/ `userType` | inferred |
| Subscribe / checkout | `POST /api/billing/checkout` (Stripe) | start subscription | inferred (Stripe observed) |
| Broker directory | `GET /api/brokers?category=&q=` | powers `/import` search+filter | inferred |
| List portfolios | `GET /api/portfolios` | dashboard load | inferred |
| Portfolio detail | `GET /api/portfolios/:id/holdings` | holdings + net worth | inferred |
| Asset-class view | `GET /api/portfolios/:id/holdings?class=STOCK` | tab filtering | inferred |
| Asset allocation | `GET /api/portfolios/:id/allocation` | pie chart | inferred |
| Transactions | `GET/POST /api/portfolios/:id/transactions` | ledger CRUD | inferred |
| Import (upload) | `POST /api/imports` (multipart) | file upload → parse | inferred |
| Import (email rule) | `POST /api/imports/email-rules` | auto-forward rule setup | inferred |
| Import status | `GET /api/imports/:id` | parse progress | inferred |
| Prices/NAV | `GET /api/instruments/:id/prices` | live + EOD | inferred |
| Corporate actions | `GET /api/instruments/:id/corporate-actions` | dividends/splits | inferred |
| Capital gains report | `GET /api/reports/capital-gains?fy=&format=itr` | ITR export | inferred |
| Analytics/XIRR | `GET /api/reports/performance?portfolio=` | XIRR, AUM | inferred |
| Advisor: clients | `GET/POST /api/clients` | wealth-pro client mgmt | inferred |
| Client login provisioning | `POST /api/clients/:id/login` | give clients access | inferred |
| Reviews (public) | EmbedSocial CDN (`embedsocial.com/cdn/ht.js`) | testimonials widget | observed |
| Support | Freshworks widget API | chat/help center | observed |

---

## 6. Dataflow map

| UI element | Data fields | API endpoint | DB table(s) |
|---|---|---|---|
| Login email box → Continue | email | `POST /api/auth/check-email` | User |
| Sign-up persona cards | userType (Investor/WealthPro) | `POST /api/auth/signup` | User |
| Subscribe email gate + plan | email, plan, track | `POST /api/billing/checkout` (Stripe) | Subscription, User |
| Dashboard "My Family" + Net Worth | family, portfolios, totals | `GET /api/portfolios` | Family, Portfolio, Holding |
| Asset tabs (Stocks/MF/Bonds/FD/F&O/Insurance) | assetClass filter | `GET /portfolios/:id/holdings?class=` | Holding, Instrument |
| Asset Allocation pie | class → value % | `GET /portfolios/:id/allocation` | Holding, Instrument, PriceQuote |
| Holdings table (avg/current/gain%) | qty, avgBuy, current, P&L | `GET /portfolios/:id/holdings` | Holding, Instrument, PriceQuote |
| `/import` broker search + filter | q, category | `GET /api/brokers?category=&q=` | Broker |
| Import upload / email-forward | file, brokerId, type | `POST /api/imports` | ImportJob → Transaction |
| Capital Gains (ITR) report | FY, format, grandfathering | `GET /api/reports/capital-gains` | CapitalGainRecord, Transaction |
| F&O position book | positions, MTM, P&L | `GET /portfolios/:id/holdings?class=FNO` | Holding, Instrument, PriceQuote |
| Advisor client list + logins | clients, hasLogin | `GET/POST /api/clients` | Client, User |
| Reviews page cards | testimonial text/author | EmbedSocial CDN | (external) |
| Contact Us / Help | ticket | Freshworks widget | (external) |

---

## 7. Clone implementation plan

1. **Scaffold marketing site** — Gatsby/Next static site, React + slick
   carousels, Google Fonts (Poppins/Source Sans/Open Sans). Pages: home,
   features, pricing (→ investors / wealth sub-routes), import, about, reviews,
   blog, refer, contact, terms, privacy. Wire GTM+GA, Freshworks chat,
   EmbedSocial reviews widget.
2. **Auth** — email-first login (`check-email` → password/OTP), persona-based
   sign-up (`userType`), sessions/JWT. Distinguish "Cloud" (web app) from any
   legacy path.
3. **Core domain DB** — implement the Prisma schema (User/Family/Portfolio/
   Holding/Transaction/Instrument). Seed AssetClass + Broker directory
   (categories mirror `/import`).
4. **Import engine (the moat)** — file upload + per-user email-forwarding
   inbox; pluggable parsers per Broker/format (PDF/Excel/HTML/CSV/TXT/DBF) →
   normalized Transactions → recompute Holdings. Build parser plugins one broker
   at a time; ship review/queue UI (`ImportStatus`).
5. **Market data** — ingest live equity/ETF prices + EOD MF NAV + corporate
   actions; nightly recompute of Holding.currentValue/allocation.
6. **Portfolio dashboard** — "My Family" view, asset-class tabs, Net Worth,
   Asset Allocation pie, holdings tables, F&O position book, XIRR/performance.
7. **Tax & reports** — Capital Gains engine (STCG/LTCG, 2018 grandfathering,
   indexation) → ITR-format export + ClearTax/Winman/CompuTax-compatible files.
8. **Wealth-pro mode** — client management, consolidated AUM, client login
   provisioning, white-label branding on reports.
9. **Billing** — Stripe subscriptions, two pricing tracks (Investor vs
   Wealth-Pro), plan tiers (Basic/Investor/Professional).
10. **Mobile** — React Native / Flutter apps consuming the same API (App
    Store + Play Store presence).

Build order priority: 3 → 4 → 6 → 7 (import + capital-gains is the actual
differentiator; the marketing site is trivial by comparison).

---

## 8. Stage → agent → model matrix

| Stage | Agent | Tool reused | Model (default) | Status for this target |
|---|---|---|---|---|
| 0 recon | recon-agent | Playwright (recon.mjs) | none (mechanical) | DONE — 14 routes captured (shots+DOM) |
| 1 intel | intel-agent | saas-reverse | Claude Opus (vision+reasoning) | THIS DOC — stack + feature map |
| 2 database | db-agent | native Claude vision | Claude Opus | THIS DOC — §4 Prisma model |
| 3 api | api-agent | reverse-api-engineer / Integuru | Claude Opus (+ Sonnet codegen) | Partial — inferred only (no HAR/auth) |
| 4 dataflow | dataflow-agent | — (fusion) | Claude Opus | THIS DOC — §6 map |
| 5 frontend | frontend-agent | ai-website-cloner-template | Opus planner + Sonnet section builders | Feasible from DOM/shots (Gatsby/React) |
| 6 assemble | assembler-agent | — (glue) | Claude Sonnet | Pending build phase |

---

## 9. Risks & gaps

- **Entire application is behind `/login`** — no dashboard, import UI, report
  builder or settings observed directly. Product-screen claims are inferred
  from marketing screenshots embedded on public pages, not the live app.
- **No HAR captured** (`recon.json` `har: null`) — so all API paths/methods in
  §5 are inferred, not verified. An authorized, logged-in run with network
  capture would replace §5/§6 with real endpoints, payloads and auth scheme.
- **Two-runtime ambiguity** — login distinguishes **MProfit desktop** vs
  **MProfit Cloud**; the desktop product's data model (likely a local DB) and
  sync mechanism are unseen and may differ from the web schema.
- **Pricing detail not captured** — `/pricing` only splits into Investors vs
  Wealth-Pro cards; the actual plan tiers/prices live on un-recon'd sub-routes
  (`/pricing/...`). Plan tokens (Basic/Investor/Professional) seen but not
  priced.
- **Import parser specifics** — the 700+ broker/format parsers are the real IP;
  formats are listed but parsing logic is entirely opaque from recon.
- **Third-party coupling** — Stripe, Freshworks, EmbedSocial, GTM/GA are
  observed on the marketing shell; their exact configuration/keys and whether
  Stripe is the in-app billing provider need authenticated confirmation.

What an authorized run would add: live API/HAR trace, real DB field names via
network payloads, pricing tables, the import upload/review flow, and the
advisor (wealth-pro) console.
