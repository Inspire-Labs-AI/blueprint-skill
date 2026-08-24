-- MProfit clone — inferred SQL DDL (Blueprint Stage 2, DB)
-- Confidence: INFERRED from UI screenshots + DOM. No HAR, no live DB access.
-- Dialect: PostgreSQL.

-- ============================ ENUMS ============================
CREATE TYPE user_type            AS ENUM ('INVESTOR','WEALTH_PROFESSIONAL');
CREATE TYPE subscriber_segment   AS ENUM ('INVESTOR','WEALTH_PROFESSIONAL');
CREATE TYPE asset_class          AS ENUM ('EQUITY','MUTUAL_FUND','BOND','FNO','FIXED_DEPOSIT','NPS','PMS','AIF','EPF_PPF','INSURANCE','ULIP','PRIVATE_EQUITY','DEPOSIT','LOAN','REAL_ESTATE','OTHER');
CREATE TYPE fno_segment          AS ENUM ('EQUITY','CURRENCY','COMMODITY');
CREATE TYPE fno_instrument_type  AS ENUM ('FUTURE','CALL_OPTION','PUT_OPTION');
CREATE TYPE transaction_type     AS ENUM ('BUY','SELL','DIVIDEND','INTEREST','BONUS','SPLIT','RIGHTS','MERGER','DEMERGER','DEPOSIT','WITHDRAWAL','CHARGE','MATURITY','SIP','EXPIRY');
CREATE TYPE corporate_action_type AS ENUM ('DIVIDEND','BONUS','SPLIT','MERGER','DEMERGER','RIGHTS','BUYBACK');
CREATE TYPE capital_gain_term    AS ENUM ('SHORT_TERM','LONG_TERM','INTRA_DAY');
CREATE TYPE import_status        AS ENUM ('PENDING','PARSING','PARSED','IMPORTED','FAILED','NEEDS_REVIEW');
CREATE TYPE import_channel       AS ENUM ('MANUAL_UPLOAD','EMAIL_FORWARD','BROKER_SYNC');

-- ==================== TENANCY / IDENTITY / BILLING ====================
CREATE TABLE account (
  id            TEXT PRIMARY KEY,
  name          TEXT NOT NULL,
  segment       subscriber_segment NOT NULL DEFAULT 'INVESTOR',
  brand_logo_url TEXT,
  brand_color   TEXT,
  brand_name    TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_account_segment ON account(segment);

CREATE TABLE app_user (
  id              TEXT PRIMARY KEY,
  account_id      TEXT NOT NULL REFERENCES account(id),
  email           TEXT NOT NULL UNIQUE,
  password_hash   TEXT,
  full_name       TEXT,
  phone           TEXT,
  user_type       user_type NOT NULL DEFAULT 'INVESTOR',
  email_verified  BOOLEAN NOT NULL DEFAULT false,
  reset_code      TEXT,
  reset_code_expires_at TIMESTAMPTZ,
  last_login_at   TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_user_account ON app_user(account_id);

CREATE TABLE advisor_client (
  id                 TEXT PRIMARY KEY,
  advisor_account_id TEXT NOT NULL REFERENCES account(id),
  client_account_id  TEXT NOT NULL REFERENCES account(id),
  display_name       TEXT,
  category           TEXT,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (advisor_account_id, client_account_id)
);
CREATE INDEX idx_advisor_client_advisor ON advisor_client(advisor_account_id);

CREATE TABLE plan (
  id             TEXT PRIMARY KEY,
  code           TEXT NOT NULL UNIQUE,
  name           TEXT NOT NULL,
  segment        subscriber_segment NOT NULL,
  price_inr      NUMERIC(12,2),
  billing_period TEXT,
  features       JSONB,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE subscription (
  id         TEXT PRIMARY KEY,
  account_id TEXT NOT NULL REFERENCES account(id),
  plan_id    TEXT NOT NULL REFERENCES plan(id),
  status     TEXT NOT NULL DEFAULT 'active',
  starts_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  ends_at    TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_subscription_account ON subscription(account_id);

CREATE TABLE referral (
  id            TEXT PRIMARY KEY,
  referrer_id   TEXT NOT NULL REFERENCES app_user(id),
  referee_email TEXT NOT NULL,
  code          TEXT NOT NULL UNIQUE,
  status        TEXT NOT NULL DEFAULT 'pending',
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_referral_referrer ON referral(referrer_id);

-- ==================== PORTFOLIOS & GROUPING ====================
CREATE TABLE portfolio (
  id            TEXT PRIMARY KEY,
  account_id    TEXT NOT NULL REFERENCES account(id),
  owner_id      TEXT REFERENCES app_user(id),
  name          TEXT NOT NULL,
  description   TEXT,
  base_currency TEXT NOT NULL DEFAULT 'INR',
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_portfolio_account ON portfolio(account_id);

CREATE TABLE portfolio_group (
  id         TEXT PRIMARY KEY,
  account_id TEXT NOT NULL REFERENCES account(id),
  name       TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_portfolio_group_account ON portfolio_group(account_id);

CREATE TABLE portfolio_group_member (
  id           TEXT PRIMARY KEY,
  group_id     TEXT NOT NULL REFERENCES portfolio_group(id),
  portfolio_id TEXT NOT NULL REFERENCES portfolio(id),
  UNIQUE (group_id, portfolio_id)
);

-- ==================== INSTRUMENT / HOLDINGS / LEDGER ====================
CREATE TABLE instrument (
  id          TEXT PRIMARY KEY,
  asset_class asset_class NOT NULL,
  name        TEXT NOT NULL,
  symbol      TEXT,
  isin        TEXT,
  exchange    TEXT,
  amc_name    TEXT,
  sector      TEXT,
  metadata    JSONB,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (isin, exchange)
);
CREATE INDEX idx_instrument_asset_class ON instrument(asset_class);
CREATE INDEX idx_instrument_symbol ON instrument(symbol);

CREATE TABLE holding (
  id             TEXT PRIMARY KEY,
  portfolio_id   TEXT NOT NULL REFERENCES portfolio(id),
  instrument_id  TEXT NOT NULL REFERENCES instrument(id),
  quantity       NUMERIC(24,6) NOT NULL,
  avg_cost       NUMERIC(24,6) NOT NULL,
  invested_value NUMERIC(24,2) NOT NULL,
  current_price  NUMERIC(24,6),
  current_value  NUMERIC(24,2),
  updated_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (portfolio_id, instrument_id)
);
CREATE INDEX idx_holding_instrument ON holding(instrument_id);

CREATE TABLE import_source (
  id           TEXT PRIMARY KEY,
  name         TEXT NOT NULL,
  category     TEXT NOT NULL,
  file_formats TEXT[] NOT NULL DEFAULT '{}',
  asset_classes asset_class[] NOT NULL DEFAULT '{}',
  is_active    BOOLEAN NOT NULL DEFAULT true,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (name, category)
);
CREATE INDEX idx_import_source_category ON import_source(category);

CREATE TABLE import_job (
  id            TEXT PRIMARY KEY,
  account_id    TEXT NOT NULL REFERENCES account(id),
  portfolio_id  TEXT REFERENCES portfolio(id),
  source_id     TEXT REFERENCES import_source(id),
  channel       import_channel NOT NULL DEFAULT 'MANUAL_UPLOAD',
  file_name     TEXT,
  file_type     TEXT,
  file_url      TEXT,
  status        import_status NOT NULL DEFAULT 'PENDING',
  rows_parsed   INT,
  rows_imported INT,
  error_message TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at  TIMESTAMPTZ
);
CREATE INDEX idx_import_job_account ON import_job(account_id);
CREATE INDEX idx_import_job_status ON import_job(status);

CREATE TABLE transaction (
  id              TEXT PRIMARY KEY,
  portfolio_id    TEXT NOT NULL REFERENCES portfolio(id),
  instrument_id   TEXT REFERENCES instrument(id),
  type            transaction_type NOT NULL,
  trade_date      TIMESTAMPTZ NOT NULL,
  settlement_date TIMESTAMPTZ,
  quantity        NUMERIC(24,6),
  price           NUMERIC(24,6),
  amount          NUMERIC(24,2) NOT NULL,
  brokerage       NUMERIC(24,2),
  taxes           NUMERIC(24,2),
  charges         NUMERIC(24,2),
  narration       TEXT,
  import_job_id   TEXT REFERENCES import_job(id),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_transaction_portfolio_date ON transaction(portfolio_id, trade_date);
CREATE INDEX idx_transaction_instrument ON transaction(instrument_id);
CREATE INDEX idx_transaction_import_job ON transaction(import_job_id);

CREATE TABLE fno_position (
  id             TEXT PRIMARY KEY,
  portfolio_id   TEXT NOT NULL REFERENCES portfolio(id),
  instrument_id  TEXT REFERENCES instrument(id),
  segment        fno_segment NOT NULL,
  instr_type     fno_instrument_type NOT NULL,
  underlying     TEXT NOT NULL,
  expiry_date    TIMESTAMPTZ NOT NULL,
  strike_price   NUMERIC(24,6),
  lots           INT NOT NULL,
  lot_size       INT NOT NULL,
  entry_price    NUMERIC(24,6) NOT NULL,
  mark_price     NUMERIC(24,6),
  realised_pnl   NUMERIC(24,2),
  unrealised_pnl NUMERIC(24,2),
  updated_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_fno_portfolio ON fno_position(portfolio_id);
CREATE INDEX idx_fno_underlying_expiry ON fno_position(underlying, expiry_date);

CREATE TABLE fixed_deposit (
  id            TEXT PRIMARY KEY,
  instrument_id TEXT NOT NULL UNIQUE REFERENCES instrument(id),
  principal     NUMERIC(24,2) NOT NULL,
  interest_rate NUMERIC(8,4) NOT NULL,
  start_date    TIMESTAMPTZ NOT NULL,
  maturity_date TIMESTAMPTZ NOT NULL,
  payout_type   TEXT,
  bank_name     TEXT
);

CREATE TABLE nps_account (
  id            TEXT PRIMARY KEY,
  instrument_id TEXT NOT NULL UNIQUE REFERENCES instrument(id),
  pran          TEXT,
  tier          TEXT,
  scheme_name   TEXT
);

-- ==================== MARKET DATA / CORP ACTIONS / VALUATION ====================
CREATE TABLE price (
  id            TEXT PRIMARY KEY,
  instrument_id TEXT NOT NULL REFERENCES instrument(id),
  price_date    TIMESTAMPTZ NOT NULL,
  price         NUMERIC(24,6) NOT NULL,
  price_type    TEXT NOT NULL DEFAULT 'CLOSE',
  source        TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (instrument_id, price_date, price_type)
);
CREATE INDEX idx_price_instrument_date ON price(instrument_id, price_date);

CREATE TABLE corporate_action (
  id             TEXT PRIMARY KEY,
  instrument_id  TEXT NOT NULL REFERENCES instrument(id),
  type           corporate_action_type NOT NULL,
  ex_date        TIMESTAMPTZ,
  record_date    TIMESTAMPTZ,
  ratio_from     NUMERIC(18,6),
  ratio_to       NUMERIC(18,6),
  amount_per_unit NUMERIC(24,6),
  notes          TEXT,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_corp_action_instrument_date ON corporate_action(instrument_id, ex_date);

CREATE TABLE portfolio_valuation (
  id             TEXT PRIMARY KEY,
  portfolio_id   TEXT NOT NULL REFERENCES portfolio(id),
  as_of_date     TIMESTAMPTZ NOT NULL,
  invested_value NUMERIC(24,2) NOT NULL,
  market_value   NUMERIC(24,2) NOT NULL,
  absolute_gain  NUMERIC(24,2) NOT NULL,
  xirr           NUMERIC(10,4),
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (portfolio_id, as_of_date)
);
CREATE INDEX idx_valuation_portfolio_date ON portfolio_valuation(portfolio_id, as_of_date);

-- ==================== CAPITAL GAINS (INDIA ITR) ====================
CREATE TABLE capital_gain (
  id                  TEXT PRIMARY KEY,
  transaction_id      TEXT NOT NULL REFERENCES transaction(id),
  term                capital_gain_term NOT NULL,
  buy_date            TIMESTAMPTZ,
  sell_date           TIMESTAMPTZ,
  quantity            NUMERIC(24,6) NOT NULL,
  cost_of_acquisition NUMERIC(24,2) NOT NULL,
  sale_value          NUMERIC(24,2) NOT NULL,
  gain_amount         NUMERIC(24,2) NOT NULL,
  grandfathered_value NUMERIC(24,2),
  indexed_cost        NUMERIC(24,2),
  financial_year      TEXT,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_capital_gain_transaction ON capital_gain(transaction_id);
CREATE INDEX idx_capital_gain_fy ON capital_gain(financial_year);

-- ==================== EMAIL AUTO-IMPORT & REPORTS ====================
CREATE TABLE email_import_rule (
  id                 TEXT PRIMARY KEY,
  user_id            TEXT NOT NULL REFERENCES app_user(id),
  forwarding_address TEXT NOT NULL,
  from_filter        TEXT,
  portfolio_id       TEXT REFERENCES portfolio(id),
  is_active          BOOLEAN NOT NULL DEFAULT true,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_email_rule_user ON email_import_rule(user_id);

CREATE TABLE report (
  id         TEXT PRIMARY KEY,
  account_id TEXT NOT NULL REFERENCES account(id),
  type       TEXT NOT NULL,
  scope      TEXT,
  scope_id   TEXT,
  from_date  TIMESTAMPTZ,
  to_date    TIMESTAMPTZ,
  format     TEXT,
  file_url   TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_report_account_type ON report(account_id, type);
