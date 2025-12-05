-- VC Investor OSINT Scraper Database Schema

CREATE TABLE IF NOT EXISTS firms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cik TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    sic_code TEXT,
    state TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_firms_name ON firms(name);
CREATE INDEX IF NOT EXISTS idx_firms_cik ON firms(cik);

CREATE TABLE IF NOT EXISTS form_d_filings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    accession_number TEXT NOT NULL UNIQUE,
    cik TEXT NOT NULL,
    issuer_name TEXT NOT NULL,
    filing_date DATE NOT NULL,
    is_amendment BOOLEAN DEFAULT FALSE,
    total_offering_amount INTEGER,
    total_amount_sold INTEGER,
    total_remaining INTEGER,
    investor_count INTEGER,
    minimum_investment INTEGER,
    sales_commission INTEGER,
    finders_fee INTEGER,
    revenue_range TEXT,
    industry_group TEXT,
    issuer_state TEXT,
    issuer_city TEXT,
    date_of_first_sale DATE,
    raw_xml TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cik) REFERENCES firms(cik)
);

CREATE INDEX IF NOT EXISTS idx_filings_cik ON form_d_filings(cik);
CREATE INDEX IF NOT EXISTS idx_filings_date ON form_d_filings(filing_date);
CREATE INDEX IF NOT EXISTS idx_filings_issuer ON form_d_filings(issuer_name);

CREATE TABLE IF NOT EXISTS related_persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filing_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    title TEXT,
    relationship TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    FOREIGN KEY (filing_id) REFERENCES form_d_filings(id)
);

CREATE INDEX IF NOT EXISTS idx_persons_name ON related_persons(name);
CREATE INDEX IF NOT EXISTS idx_persons_filing ON related_persons(filing_id);

CREATE TABLE IF NOT EXISTS press_releases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    published_at TIMESTAMP NOT NULL,
    summary TEXT,
    matched_firm_cik TEXT,
    extracted_round_size INTEGER,
    extracted_company TEXT,
    raw_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pr_published ON press_releases(published_at);
CREATE INDEX IF NOT EXISTS idx_pr_firm ON press_releases(matched_firm_cik);

CREATE TABLE IF NOT EXISTS searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    selected_cik TEXT,
    results_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

