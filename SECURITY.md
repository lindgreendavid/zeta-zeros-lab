# Security policy

## Supported version

Security fixes are applied to the latest Zeta Zeros Lab release. The project is research and
educational software; it performs deterministic numerical statistics on frozen number-theory data
only, accepts no untrusted file uploads, and must not be treated as a proof of any mathematical claim.

## Reporting a vulnerability

Please use GitHub's private vulnerability-reporting flow for this repository. Do not include
secrets, personal data, or exploit payloads in a public issue.

## Dependency boundary

CI rejects known high-severity vulnerabilities in production web dependencies
(`pnpm audit --prod --audit-level high`). The interactive site accepts no user file uploads,
no authentication, and no server-side persistence of visitor input — every simulator control is
a choice between two fixed blocks of zeros and two fixed charts; the site accepts no free-text input.
