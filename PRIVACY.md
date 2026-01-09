# Privacy and Data Handling Policy

## Overview

This document describes how the Skill Intelligence application handles user data and ensures privacy protection.

## Data Collection and Storage

### What We DO NOT Collect or Store

1. **Personal Identifiable Information (PII)**
   - No names, email addresses, phone numbers, or other personal identifiers
   - No IP addresses (logs may contain IPs but they are not stored or associated with user data)
   - No location data beyond general region categories (e.g., "Global", "North America")

2. **User Input Content**
   - Job description text is processed in-memory but **NOT stored**
   - Resume or profile text is **NOT saved** to disk or database
   - Form submissions (role, industry, region) are treated as search queries, not stored

3. **Usage Tracking**
   - No user sessions are tracked
   - No individual user behavior is logged or stored
   - No cookies or tracking identifiers

### What We DO Process (Temporarily)

1. **Search Query Parameters**
   - Role, industry, and region are used as search criteria
   - These are treated as categorical filters, not personal identifiers
   - Processed in-memory and discarded after request completion

2. **Job Description Text** (if provided)
   - Text is processed in-memory for skill extraction
   - **Never stored** to disk or database
   - Discarded immediately after processing
   - Maximum length: 50,000 characters per description

3. **Aggregated Analytics**
   - Only aggregate, anonymized metrics are logged (e.g., "5 skills extracted")
   - No individual queries or content are logged
   - No way to identify individual users from logs

## Data Anonymization

### Response Data

All API responses contain only:
- **Aggregated skill data**: Skill names and counts, no source attribution
- **Category information**: General categories (role type, industry type), not specific entities
- **Statistical summaries**: Counts and frequencies, no individual records

### Logging

Logs contain:
- **Anonymized metrics**: "X requests processed", "Y skills extracted"
- **Error messages**: Technical error details (without user data)
- **System events**: Service health, performance metrics

Logs do NOT contain:
- User input text
- Personal identifiers
- Search queries
- Individual request details

## Data Retention

- **In-memory processing**: Data is discarded immediately after request completion
- **Historical trend data**: Only aggregated skill frequency counts stored (no personal data)
- **Logs**: Standard application logs, rotated and deleted according to server policy

## Security Measures

1. **Input Sanitization**
   - All user inputs are sanitized and validated
   - Maximum length limits prevent resource exhaustion
   - Control characters are removed to prevent injection attacks

2. **Error Handling**
   - Error messages do not expose internal system details
   - Stack traces are not returned to clients
   - No sensitive information in error responses

3. **No Authentication Required** (MVP)
   - No user accounts or authentication
   - No personal data associated with requests
   - All endpoints are public (rate limiting recommended in production)

## Third-Party Services

### GitHub API (if enabled)
- Uses public GitHub repository data only
- No authentication required for public repos
- No personal GitHub account information accessed
- Only repository metadata (names, descriptions, languages, topics) is used

### Future Considerations
- When adding external APIs, ensure they comply with privacy standards
- When adding authentication, implement proper data protection measures
- When adding databases, ensure no PII is stored

## User Rights

Since no personal data is collected or stored:
- No data deletion requests needed (nothing is stored)
- No data export requests (no personal data exists)
- No opt-out required (nothing is tracked)

## Compliance

This MVP application is designed to:
- Minimize data collection (collect only what's necessary)
- Process data in-memory (no persistent storage of user content)
- Return only aggregated, anonymized results
- Follow privacy-by-design principles

## Contact

For privacy concerns or questions, refer to the project repository.

## Changes to This Policy

As the application evolves (adding features like authentication, databases, etc.), this privacy policy will be updated to reflect new data handling practices.

