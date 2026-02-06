# Scraping Issues Log

**Date**: 2026-02-06
**Status**: Complete

## Pass 2 Issues (PDF Discovery)

### Issue 1: ASEAN CDN Blocks curl Downloads
- **Severity**: Medium (resolved)
- **Category**: 6b ASEAN Trade
- **Description**: curl downloads from asean.org returned 275-byte HTML instead of PDFs
- **Root Cause**: ASEAN CDN blocks requests without a browser-like User-Agent header
- **Resolution**: Added `-H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"` to all curl commands

### Issue 2: Cathay Cargo HTTP2 Protocol Errors
- **Severity**: Low (no workaround)
- **Category**: 6e Air Carriers
- **URLs affected**:
  - cathaycargo.com/en-us/solutions/cathay-pharma.html
  - cathaycargo.com/en-us/solutions/cathay-fresh.html
  - cathaycargo.com/en-us/solutions/cathay-live-animal.html
- **Error**: `net::ERR_HTTP2_PROTOCOL_ERROR`
- **Impact**: Could not scan 3 product pages for PDFs
- **Resolution**: Skipped — about-us page loaded successfully with 0 PDFs, suggesting product pages likely also have no downloadable PDFs

### Issue 3: Thailand Customs Timeout
- **Severity**: Low
- **Category**: 6c Country-specific
- **URL**: customs.go.th
- **Error**: Navigation timeout exceeded 15 seconds
- **Resolution**: Skipped — Thai customs portal is a web application unlikely to host downloadable PDFs

### Issue 4: Philippines Customs 403 Forbidden
- **Severity**: Low
- **Category**: 6c Country-specific
- **URL**: customs.gov.ph
- **Error**: 403 Forbidden — access blocked
- **Resolution**: Skipped

### Issue 5: Philippines DTI SSL Certificate Expired
- **Severity**: Low
- **Category**: 6c Country-specific
- **URL**: dti.gov.ph
- **Error**: `ERR_CERT_DATE_INVALID`
- **Resolution**: Skipped — site SSL certificate has expired

### Issue 6: ASEAN Tariff Finder Requires Authentication
- **Severity**: Low
- **Category**: 6b ASEAN Trade
- **URL**: tariff-finder.asean.org
- **Description**: Redirected to login page (asean.mendel-online.com)
- **Resolution**: Skipped — cannot access without credentials

## Pass 1 Notes

- All 30 documents copied/enriched/created successfully
- 5 documents enriched with new content (Fixes 1-9 from Task 1)
- 1 new FAQ document created
- No issues encountered during Pass 1
