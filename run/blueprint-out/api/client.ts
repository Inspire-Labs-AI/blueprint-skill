// MProfit clone — inferred typed API client skeleton (Blueprint Stage 3, API).
// Confidence: INFERRED. No HAR, no authorized session — every endpoint here is a
// plausible REST surface reverse-inferred from UI screenshots + DOM under
// blueprint-out/recon/ and the inferred data model (blueprint-out/db/schema.prisma).
// live = false. Adjust paths/shapes once real traffic is captured.
//
// Conventions:
//   - Base URL: https://api.mprofit.in (product app "MProfit Cloud"; marketing
//     site is a separate Gatsby+Sanity SSG and has no first-party API).
//   - REST/JSON, cookie or Bearer JWT session, tenant scoped by the authed account.
//   - Money as string-decimals (matches Prisma Decimal); dates as ISO-8601 strings.
//   - Collection endpoints are cursor/paginated: { data, nextCursor }.

// ---------------------------------------------------------------------------
// Shared types (mirror db/schema.prisma enums & models)
// ---------------------------------------------------------------------------

export type UserType = "INVESTOR" | "WEALTH_PROFESSIONAL";
export type SubscriberSegment = "INVESTOR" | "WEALTH_PROFESSIONAL";
export type AssetClass =
  | "EQUITY" | "MUTUAL_FUND" | "BOND" | "FNO" | "FIXED_DEPOSIT" | "NPS"
  | "PMS" | "AIF" | "EPF_PPF" | "INSURANCE" | "ULIP" | "PRIVATE_EQUITY"
  | "DEPOSIT" | "LOAN" | "REAL_ESTATE" | "OTHER";
export type FnoSegment = "EQUITY" | "CURRENCY" | "COMMODITY";
export type FnoInstrumentType = "FUTURE" | "CALL_OPTION" | "PUT_OPTION";
export type TransactionType =
  | "BUY" | "SELL" | "DIVIDEND" | "INTEREST" | "BONUS" | "SPLIT" | "RIGHTS"
  | "MERGER" | "DEMERGER" | "DEPOSIT" | "WITHDRAWAL" | "CHARGE" | "MATURITY"
  | "SIP" | "EXPIRY";
export type CorporateActionType =
  | "DIVIDEND" | "BONUS" | "SPLIT" | "MERGER" | "DEMERGER" | "RIGHTS" | "BUYBACK";
export type CapitalGainTerm = "SHORT_TERM" | "LONG_TERM" | "INTRA_DAY";
export type ImportStatus =
  | "PENDING" | "PARSING" | "PARSED" | "IMPORTED" | "FAILED" | "NEEDS_REVIEW";
export type ImportChannel = "MANUAL_UPLOAD" | "EMAIL_FORWARD" | "BROKER_SYNC";
export type ReportType =
  | "INCOME" | "DUE_DATES" | "TRANSACTIONS" | "HOLDING_PERIOD"
  | "ASSET_ALLOCATION" | "CAPITAL_GAINS" | "AUM";
export type ReportFormat =
  | "PDF" | "EXCEL" | "ITR" | "CLEARTAX" | "WINMAN" | "COMPUTAX";

export type ID = string;
export type Decimal = string; // decimal-as-string to avoid float loss
export type ISODate = string;

export interface Page<T> { data: T[]; nextCursor?: string | null }
export interface PageQuery { cursor?: string; limit?: number }

export interface Account {
  id: ID; name: string; segment: SubscriberSegment;
  brandLogoUrl?: string | null; brandColor?: string | null; brandName?: string | null;
  createdAt: ISODate; updatedAt: ISODate;
}
export interface User {
  id: ID; accountId: ID; email: string; fullName?: string | null;
  phone?: string | null; userType: UserType; emailVerified: boolean;
  lastLoginAt?: ISODate | null; createdAt: ISODate; updatedAt: ISODate;
}
export interface Plan {
  id: ID; code: string; name: string; segment: SubscriberSegment;
  priceInr?: Decimal | null; billingPeriod?: string | null; features?: unknown;
}
export interface Subscription {
  id: ID; accountId: ID; planId: ID; status: string;
  startsAt: ISODate; endsAt?: ISODate | null;
}
export interface Referral {
  id: ID; referrerId: ID; refereeEmail: string; code: string; status: string;
  createdAt: ISODate;
}
export interface AdvisorClient {
  id: ID; advisorAccountId: ID; clientAccountId: ID;
  displayName?: string | null; category?: string | null; createdAt: ISODate;
}
export interface Portfolio {
  id: ID; accountId: ID; ownerId?: ID | null; name: string;
  description?: string | null; baseCurrency: string;
  createdAt: ISODate; updatedAt: ISODate;
}
export interface PortfolioGroup {
  id: ID; accountId: ID; name: string; createdAt: ISODate; memberIds?: ID[];
}
export interface Instrument {
  id: ID; assetClass: AssetClass; name: string; symbol?: string | null;
  isin?: string | null; exchange?: string | null; amcName?: string | null;
  sector?: string | null; metadata?: unknown;
}
export interface Holding {
  id: ID; portfolioId: ID; instrumentId: ID; quantity: Decimal; avgCost: Decimal;
  investedValue: Decimal; currentPrice?: Decimal | null; currentValue?: Decimal | null;
  updatedAt: ISODate; instrument?: Instrument;
}
export interface Transaction {
  id: ID; portfolioId: ID; instrumentId?: ID | null; type: TransactionType;
  tradeDate: ISODate; settlementDate?: ISODate | null;
  quantity?: Decimal | null; price?: Decimal | null; amount: Decimal;
  brokerage?: Decimal | null; taxes?: Decimal | null; charges?: Decimal | null;
  narration?: string | null; importJobId?: ID | null; createdAt: ISODate;
}
export interface FnoPosition {
  id: ID; portfolioId: ID; instrumentId?: ID | null; segment: FnoSegment;
  instrType: FnoInstrumentType; underlying: string; expiryDate: ISODate;
  strikePrice?: Decimal | null; lots: number; lotSize: number; entryPrice: Decimal;
  markPrice?: Decimal | null; realisedPnl?: Decimal | null; unrealisedPnl?: Decimal | null;
}
export interface FixedDeposit {
  id: ID; instrumentId: ID; principal: Decimal; interestRate: Decimal;
  startDate: ISODate; maturityDate: ISODate; payoutType?: string | null; bankName?: string | null;
}
export interface NpsAccount {
  id: ID; instrumentId: ID; pran?: string | null; tier?: string | null; schemeName?: string | null;
}
export interface Price {
  id: ID; instrumentId: ID; priceDate: ISODate; price: Decimal;
  priceType: string; source?: string | null;
}
export interface CorporateAction {
  id: ID; instrumentId: ID; type: CorporateActionType; exDate?: ISODate | null;
  recordDate?: ISODate | null; ratioFrom?: Decimal | null; ratioTo?: Decimal | null;
  amountPerUnit?: Decimal | null; notes?: string | null;
}
export interface PortfolioValuation {
  id: ID; portfolioId: ID; asOfDate: ISODate; investedValue: Decimal;
  marketValue: Decimal; absoluteGain: Decimal; xirr?: Decimal | null;
}
export interface CapitalGain {
  id: ID; transactionId: ID; term: CapitalGainTerm; buyDate?: ISODate | null;
  sellDate?: ISODate | null; quantity: Decimal; costOfAcquisition: Decimal;
  saleValue: Decimal; gainAmount: Decimal; grandfatheredValue?: Decimal | null;
  indexedCost?: Decimal | null; financialYear?: string | null;
}
export interface ImportSource {
  id: ID; name: string; category: string; fileFormats: string[];
  assetClasses: AssetClass[]; isActive: boolean;
}
export interface ImportJob {
  id: ID; accountId: ID; portfolioId?: ID | null; sourceId?: ID | null;
  channel: ImportChannel; fileName?: string | null; fileType?: string | null;
  fileUrl?: string | null; status: ImportStatus; rowsParsed?: number | null;
  rowsImported?: number | null; errorMessage?: string | null;
  createdAt: ISODate; completedAt?: ISODate | null;
}
export interface EmailImportRule {
  id: ID; userId: ID; forwardingAddress: string; fromFilter?: string | null;
  portfolioId?: ID | null; isActive: boolean;
}
export interface Report {
  id: ID; accountId: ID; type: ReportType; scope?: string | null; scopeId?: ID | null;
  fromDate?: ISODate | null; toDate?: ISODate | null; format?: ReportFormat | null;
  fileUrl?: string | null; createdAt: ISODate;
}

// Auth payloads
export interface Session { token: string; expiresAt: ISODate; user: User; account: Account }
export interface SignupInput {
  email: string; password: string; fullName?: string; phone?: string;
  userType: UserType; referralCode?: string;
}
export interface LoginInput { email: string; password: string }
export interface ResetRequestInput { email: string }
export interface ResetConfirmInput { email: string; resetCode: string; newPassword: string }

// Analytics payloads (derived; no direct table)
export interface PerformanceSummary {
  scope: "portfolio" | "group" | "account" | "global"; scopeId?: ID;
  investedValue: Decimal; marketValue: Decimal; absoluteGain: Decimal;
  absoluteGainPct: Decimal; xirr: Decimal; asOf: ISODate;
}
export interface AllocationSlice { key: string; label: string; marketValue: Decimal; weightPct: Decimal }
export interface AllocationBreakdown {
  by: "assetClass" | "instrument" | "sector" | "portfolio"; asOf: ISODate; slices: AllocationSlice[];
}
export interface AumSummary { totalAum: Decimal; clientCount: number; asOf: ISODate; byClient: Array<{ clientAccountId: ID; displayName?: string; aum: Decimal }> }

// ---------------------------------------------------------------------------
// Transport
// ---------------------------------------------------------------------------

export interface ClientOptions { baseUrl?: string; token?: string; fetchImpl?: typeof fetch }

export class MProfitClient {
  private baseUrl: string;
  private token?: string;
  private fetchImpl: typeof fetch;

  constructor(opts: ClientOptions = {}) {
    this.baseUrl = opts.baseUrl ?? "https://api.mprofit.in";
    this.token = opts.token;
    this.fetchImpl = opts.fetchImpl ?? fetch;
  }

  setToken(token?: string) { this.token = token; }

  private async req<T>(method: string, path: string, body?: unknown, query?: Record<string, unknown>): Promise<T> {
    const url = new URL(this.baseUrl + path);
    if (query) for (const [k, v] of Object.entries(query)) if (v != null) url.searchParams.set(k, String(v));
    const headers: Record<string, string> = { Accept: "application/json" };
    if (this.token) headers.Authorization = `Bearer ${this.token}`;
    let init: RequestInit = { method, headers };
    if (body instanceof FormData) { init.body = body; }
    else if (body !== undefined) { headers["Content-Type"] = "application/json"; init.body = JSON.stringify(body); }
    const res = await this.fetchImpl(url.toString(), init);
    if (!res.ok) throw new MProfitApiError(res.status, await res.text().catch(() => ""));
    return (res.status === 204 ? undefined : await res.json()) as T;
  }

  // ---- auth ---------------------------------------------------------------
  auth = {
    signup: (i: SignupInput) => this.req<Session>("POST", "/v1/auth/signup", i),
    login: (i: LoginInput) => this.req<Session>("POST", "/v1/auth/login", i),
    logout: () => this.req<void>("POST", "/v1/auth/logout"),
    refresh: () => this.req<Session>("POST", "/v1/auth/refresh"),
    me: () => this.req<{ user: User; account: Account }>("GET", "/v1/auth/me"),
    verifyEmail: (token: string) => this.req<void>("POST", "/v1/auth/verify-email", { token }),
    requestReset: (i: ResetRequestInput) => this.req<void>("POST", "/v1/auth/password/reset-request", i),
    confirmReset: (i: ResetConfirmInput) => this.req<Session>("POST", "/v1/auth/password/reset-confirm", i),
  };

  // ---- account / tenant / branding ---------------------------------------
  account = {
    get: () => this.req<Account>("GET", "/v1/account"),
    update: (patch: Partial<Pick<Account, "name" | "brandLogoUrl" | "brandColor" | "brandName">>) =>
      this.req<Account>("PATCH", "/v1/account", patch),
    users: (q?: PageQuery) => this.req<Page<User>>("GET", "/v1/account/users", undefined, q),
    inviteUser: (i: { email: string; fullName?: string; userType: UserType }) =>
      this.req<User>("POST", "/v1/account/users", i),
  };

  // ---- billing: plans, subscriptions, referrals ---------------------------
  billing = {
    plans: (segment?: SubscriberSegment) => this.req<Plan[]>("GET", "/v1/plans", undefined, { segment }),
    subscription: () => this.req<Subscription>("GET", "/v1/subscription"),
    subscribe: (i: { planId: ID }) => this.req<Subscription>("POST", "/v1/subscription", i),
    cancel: () => this.req<Subscription>("POST", "/v1/subscription/cancel"),
    referrals: (q?: PageQuery) => this.req<Page<Referral>>("GET", "/v1/referrals", undefined, q),
    createReferral: (i: { refereeEmail: string }) => this.req<Referral>("POST", "/v1/referrals", i),
  };

  // ---- advisor ↔ client (wealth professional) -----------------------------
  advisor = {
    listClients: (q?: PageQuery & { category?: string }) =>
      this.req<Page<AdvisorClient>>("GET", "/v1/advisor/clients", undefined, q),
    provisionClient: (i: { email: string; displayName?: string; category?: string; fullName?: string }) =>
      this.req<AdvisorClient>("POST", "/v1/advisor/clients", i),
    updateClient: (id: ID, patch: Partial<Pick<AdvisorClient, "displayName" | "category">>) =>
      this.req<AdvisorClient>("PATCH", `/v1/advisor/clients/${id}`, patch),
    removeClient: (id: ID) => this.req<void>("DELETE", `/v1/advisor/clients/${id}`),
    // switch active tenant context to a client account
    impersonate: (clientAccountId: ID) => this.req<Session>("POST", `/v1/advisor/clients/${clientAccountId}/session`),
    globalAum: (asOf?: ISODate) => this.req<AumSummary>("GET", "/v1/advisor/aum", undefined, { asOf }),
  };

  // ---- portfolios & groups ------------------------------------------------
  portfolios = {
    list: (q?: PageQuery) => this.req<Page<Portfolio>>("GET", "/v1/portfolios", undefined, q),
    create: (i: { name: string; description?: string; baseCurrency?: string; ownerId?: ID }) =>
      this.req<Portfolio>("POST", "/v1/portfolios", i),
    get: (id: ID) => this.req<Portfolio>("GET", `/v1/portfolios/${id}`),
    update: (id: ID, patch: Partial<Pick<Portfolio, "name" | "description">>) =>
      this.req<Portfolio>("PATCH", `/v1/portfolios/${id}`, patch),
    remove: (id: ID) => this.req<void>("DELETE", `/v1/portfolios/${id}`),
    holdings: (id: ID, q?: { assetClass?: AssetClass }) =>
      this.req<Holding[]>("GET", `/v1/portfolios/${id}/holdings`, undefined, q),
    valuations: (id: ID, q?: { from?: ISODate; to?: ISODate }) =>
      this.req<PortfolioValuation[]>("GET", `/v1/portfolios/${id}/valuations`, undefined, q),
  };

  groups = {
    list: (q?: PageQuery) => this.req<Page<PortfolioGroup>>("GET", "/v1/portfolio-groups", undefined, q),
    create: (i: { name: string; portfolioIds?: ID[] }) => this.req<PortfolioGroup>("POST", "/v1/portfolio-groups", i),
    get: (id: ID) => this.req<PortfolioGroup>("GET", `/v1/portfolio-groups/${id}`),
    update: (id: ID, patch: { name?: string }) => this.req<PortfolioGroup>("PATCH", `/v1/portfolio-groups/${id}`, patch),
    remove: (id: ID) => this.req<void>("DELETE", `/v1/portfolio-groups/${id}`),
    addMembers: (id: ID, portfolioIds: ID[]) => this.req<PortfolioGroup>("POST", `/v1/portfolio-groups/${id}/members`, { portfolioIds }),
    removeMember: (id: ID, portfolioId: ID) => this.req<void>("DELETE", `/v1/portfolio-groups/${id}/members/${portfolioId}`),
  };

  // ---- holdings (read; derived from ledger) -------------------------------
  holdings = {
    list: (q?: PageQuery & { portfolioId?: ID; groupId?: ID; assetClass?: AssetClass }) =>
      this.req<Page<Holding>>("GET", "/v1/holdings", undefined, q),
    get: (id: ID) => this.req<Holding>("GET", `/v1/holdings/${id}`),
  };

  // ---- transactions (CRUD ledger) -----------------------------------------
  transactions = {
    list: (q?: PageQuery & { portfolioId?: ID; instrumentId?: ID; type?: TransactionType; from?: ISODate; to?: ISODate }) =>
      this.req<Page<Transaction>>("GET", "/v1/transactions", undefined, q),
    create: (i: Omit<Transaction, "id" | "createdAt">) => this.req<Transaction>("POST", "/v1/transactions", i),
    bulkCreate: (rows: Array<Omit<Transaction, "id" | "createdAt">>) =>
      this.req<{ created: number; ids: ID[] }>("POST", "/v1/transactions/bulk", { rows }),
    get: (id: ID) => this.req<Transaction>("GET", `/v1/transactions/${id}`),
    update: (id: ID, patch: Partial<Omit<Transaction, "id" | "portfolioId" | "createdAt">>) =>
      this.req<Transaction>("PATCH", `/v1/transactions/${id}`, patch),
    remove: (id: ID) => this.req<void>("DELETE", `/v1/transactions/${id}`),
  };

  // ---- F&O positions ------------------------------------------------------
  fno = {
    list: (q?: PageQuery & { portfolioId?: ID; segment?: FnoSegment; underlying?: string }) =>
      this.req<Page<FnoPosition>>("GET", "/v1/fno-positions", undefined, q),
    create: (i: Omit<FnoPosition, "id">) => this.req<FnoPosition>("POST", "/v1/fno-positions", i),
    update: (id: ID, patch: Partial<FnoPosition>) => this.req<FnoPosition>("PATCH", `/v1/fno-positions/${id}`, patch),
    remove: (id: ID) => this.req<void>("DELETE", `/v1/fno-positions/${id}`),
  };

  // ---- instruments (security master) + asset-class extensions -------------
  instruments = {
    search: (q: { query?: string; assetClass?: AssetClass; isin?: string; exchange?: string } & PageQuery) =>
      this.req<Page<Instrument>>("GET", "/v1/instruments", undefined, q),
    get: (id: ID) => this.req<Instrument>("GET", `/v1/instruments/${id}`),
    create: (i: Omit<Instrument, "id">) => this.req<Instrument>("POST", "/v1/instruments", i),
    fixedDeposit: (id: ID) => this.req<FixedDeposit>("GET", `/v1/instruments/${id}/fixed-deposit`),
    upsertFixedDeposit: (id: ID, i: Omit<FixedDeposit, "id" | "instrumentId">) =>
      this.req<FixedDeposit>("PUT", `/v1/instruments/${id}/fixed-deposit`, i),
    npsAccount: (id: ID) => this.req<NpsAccount>("GET", `/v1/instruments/${id}/nps`),
    upsertNps: (id: ID, i: Omit<NpsAccount, "id" | "instrumentId">) =>
      this.req<NpsAccount>("PUT", `/v1/instruments/${id}/nps`, i),
  };

  // ---- market data: prices & corporate actions ----------------------------
  marketData = {
    prices: (instrumentId: ID, q?: { from?: ISODate; to?: ISODate; priceType?: string }) =>
      this.req<Price[]>("GET", `/v1/instruments/${instrumentId}/prices`, undefined, q),
    latestPrice: (instrumentId: ID) => this.req<Price>("GET", `/v1/instruments/${instrumentId}/prices/latest`),
    quotes: (instrumentIds: ID[]) => this.req<Price[]>("GET", "/v1/market-data/quotes", undefined, { ids: instrumentIds.join(",") }),
    corporateActions: (instrumentId: ID, q?: { from?: ISODate; to?: ISODate }) =>
      this.req<CorporateAction[]>("GET", `/v1/instruments/${instrumentId}/corporate-actions`, undefined, q),
  };

  // ---- import engine (the moat) -------------------------------------------
  imports = {
    sources: (q?: PageQuery & { category?: string; query?: string }) =>
      this.req<Page<ImportSource>>("GET", "/v1/import/sources", undefined, q),
    jobs: (q?: PageQuery & { status?: ImportStatus; portfolioId?: ID }) =>
      this.req<Page<ImportJob>>("GET", "/v1/import/jobs", undefined, q),
    job: (id: ID) => this.req<ImportJob>("GET", `/v1/import/jobs/${id}`),
    // multipart upload of a broker/RTA/CAS file -> parse job
    upload: (form: FormData) => this.req<ImportJob>("POST", "/v1/import/jobs", form),
    // confirm/commit a parsed job into the ledger (after NEEDS_REVIEW)
    commit: (id: ID) => this.req<ImportJob>("POST", `/v1/import/jobs/${id}/commit`),
    retry: (id: ID) => this.req<ImportJob>("POST", `/v1/import/jobs/${id}/retry`),
    // email auto-import rules
    emailRules: () => this.req<EmailImportRule[]>("GET", "/v1/import/email-rules"),
    createEmailRule: (i: { fromFilter?: string; portfolioId?: ID }) =>
      this.req<EmailImportRule>("POST", "/v1/import/email-rules", i),
    updateEmailRule: (id: ID, patch: Partial<Pick<EmailImportRule, "fromFilter" | "portfolioId" | "isActive">>) =>
      this.req<EmailImportRule>("PATCH", `/v1/import/email-rules/${id}`, patch),
    deleteEmailRule: (id: ID) => this.req<void>("DELETE", `/v1/import/email-rules/${id}`),
  };

  // ---- analytics (derived engines: XIRR / gain / allocation) --------------
  analytics = {
    performance: (q: { scope: "portfolio" | "group" | "account" | "global"; scopeId?: ID; asOf?: ISODate }) =>
      this.req<PerformanceSummary>("GET", "/v1/analytics/performance", undefined, q),
    allocation: (q: { by: "assetClass" | "instrument" | "sector" | "portfolio"; scope?: string; scopeId?: ID; asOf?: ISODate }) =>
      this.req<AllocationBreakdown>("GET", "/v1/analytics/allocation", undefined, q),
    xirr: (q: { scope: "portfolio" | "group" | "account"; scopeId: ID; from?: ISODate; to?: ISODate }) =>
      this.req<{ xirr: Decimal; asOf: ISODate }>("GET", "/v1/analytics/xirr", undefined, q),
  };

  // ---- capital gains (India ITR) ------------------------------------------
  capitalGains = {
    list: (q: { scope?: string; scopeId?: ID; financialYear?: string; term?: CapitalGainTerm } & PageQuery) =>
      this.req<Page<CapitalGain>>("GET", "/v1/capital-gains", undefined, q),
    // trigger (re)computation for a scope + FY
    compute: (i: { scope: string; scopeId: ID; financialYear: string }) =>
      this.req<{ jobId: ID; status: string }>("POST", "/v1/capital-gains/compute", i),
    export: (i: { scope: string; scopeId: ID; financialYear: string; format: ReportFormat }) =>
      this.req<Report>("POST", "/v1/capital-gains/export", i),
  };

  // ---- reports ------------------------------------------------------------
  reports = {
    list: (q?: PageQuery & { type?: ReportType }) => this.req<Page<Report>>("GET", "/v1/reports", undefined, q),
    generate: (i: { type: ReportType; scope?: string; scopeId?: ID; fromDate?: ISODate; toDate?: ISODate; format?: ReportFormat }) =>
      this.req<Report>("POST", "/v1/reports", i),
    get: (id: ID) => this.req<Report>("GET", `/v1/reports/${id}`),
    download: (id: ID) => this.req<{ url: string; expiresAt: ISODate }>("GET", `/v1/reports/${id}/download`),
  };
}

export class MProfitApiError extends Error {
  constructor(public status: number, public body: string) {
    super(`MProfit API error ${status}: ${body}`);
    this.name = "MProfitApiError";
  }
}
