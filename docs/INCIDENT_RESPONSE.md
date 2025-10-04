# Incident Response Guide

Comprehensive incident response procedures for handling security incidents, service outages, and critical system failures.

## Table of Contents

1. [Incident Classification](#incident-classification)
2. [Response Team Structure](#response-team-structure)
3. [Incident Response Process](#incident-response-process)
4. [Common Incident Scenarios](#common-incident-scenarios)
5. [Communication Protocols](#communication-protocols)
6. [Post-Incident Procedures](#post-incident-procedures)
7. [Incident Response Toolkit](#incident-response-toolkit)

---

## Incident Classification

### Severity Levels

| Level | Description | Impact | Response Time | Escalation |
|-------|-------------|--------|---------------|------------|
| **P0 - Critical** | Complete service outage | All users affected | 15 minutes | Immediate |
| **P1 - High** | Major feature unavailable | Large user subset | 1 hour | 30 minutes |
| **P2 - Medium** | Minor feature broken | Small user subset | 4 hours | 2 hours |
| **P3 - Low** | Cosmetic or minor issue | Minimal impact | Next business day | N/A |

### Examples by Severity

**P0 - Critical:**
- Database server down
- Application completely unavailable
- Data breach detected
- Payment system failure
- Authentication system down

**P1 - High:**
- Critical API endpoints failing
- Database performance severely degraded
- Memory leak causing crashes
- Security vulnerability actively exploited

**P2 - Medium:**
- Single feature not working
- Performance degradation (non-critical)
- Intermittent errors affecting some users
- Minor security vulnerability

**P3 - Low:**
- UI glitches
- Documentation errors
- Minor performance issues
- Feature enhancement requests

---

## Response Team Structure

### Roles and Responsibilities

#### Incident Commander (IC)
**Responsibility:** Overall incident coordination
- Declare incident severity
- Coordinate response efforts
- Make critical decisions
- Communicate with stakeholders
- Lead post-mortem

**Primary:** On-call Engineering Manager
**Backup:** Senior Engineer

#### Technical Lead
**Responsibility:** Technical investigation and resolution
- Investigate root cause
- Implement fixes
- Coordinate with engineers
- Provide technical updates to IC

**Primary:** On-call Senior Engineer
**Backup:** Backend/Frontend Lead

#### Communications Lead
**Responsibility:** Internal and external communication
- Update status page
- Communicate with users
- Post updates to Slack/email
- Draft incident reports

**Primary:** Product Manager
**Backup:** Engineering Manager

#### Scribe
**Responsibility:** Documentation
- Record timeline of events
- Document actions taken
- Track decision-making
- Maintain incident log

**Primary:** Available team member
**Backup:** Rotates

### On-Call Rotation

```
Week 1:
  Primary: Engineer A
  Secondary: Engineer B
  IC: Manager X

Week 2:
  Primary: Engineer B
  Secondary: Engineer C
  IC: Manager Y

Week 3:
  Primary: Engineer C
  Secondary: Engineer A
  IC: Manager X
```

### Escalation Path

```
┌──────────────────┐
│   On-Call        │
│   Engineer       │  (0-15 min)
└────────┬─────────┘
         │ Escalate if cannot resolve
         ▼
┌──────────────────┐
│   Team Lead      │  (15-30 min)
└────────┬─────────┘
         │ Escalate if high impact
         ▼
┌──────────────────┐
│   Engineering    │  (30-60 min)
│   Manager        │
└────────┬─────────┘
         │ Escalate if critical
         ▼
┌──────────────────┐
│   CTO/VP Eng     │  (60+ min)
└──────────────────┘
```

---

## Incident Response Process

### 1. Detection & Alert

**Automated Detection:**
- Monitoring alerts (Sentry, uptime monitors)
- Health check failures
- Error rate spikes
- Performance degradation

**Manual Detection:**
- User reports
- Support ticket escalation
- Team member observation

**Initial Actions:**
1. Acknowledge alert within 5 minutes
2. Assess severity
3. Assign Incident Commander
4. Create incident channel/room

### 2. Triage & Assessment

```bash
# Quick assessment script
#!/bin/bash

echo "=== Incident Triage ==="
echo "Time: $(date)"

# Check application status
echo -e "\n1. Application Health:"
curl -s https://api.subjunctivepractice.com/health

# Check database
echo -e "\n2. Database Status:"
psql -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"

# Check error rate
echo -e "\n3. Recent Errors:"
# Query from Sentry or logs
tail -100 /var/log/subjunctive/app.log | grep ERROR | wc -l

# Check system resources
echo -e "\n4. System Resources:"
top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}'
free -h | awk '/^Mem:/ {print $3 "/" $2}'
```

**Triage Checklist:**
- [ ] Determine severity level
- [ ] Identify affected systems
- [ ] Estimate user impact
- [ ] Check recent changes/deployments
- [ ] Review monitoring dashboards
- [ ] Gather initial evidence

### 3. Communication

**Internal Communication:**
```
Incident #123 - P1: API Slow Response Times
Status: Investigating
Detected: 2025-01-15 14:32 UTC
IC: @john.doe
Tech Lead: @jane.smith

Impact: 30% of API requests > 5s response time
Systems Affected: Backend API, Database
Recent Changes: Database migration deployed at 14:00 UTC

Current Actions:
- Investigating database query performance
- Checking for deadlocks
- Reviewing recent migration

Updates will be posted every 15 minutes.
```

**External Communication:**
```
Status Page Update:

[Investigating] API Performance Issues
Posted: Jan 15, 14:35 UTC

We are currently investigating reports of slow API response times.
Some users may experience delays when loading exercises.

We will provide an update within 30 minutes.

Next Update: Jan 15, 15:05 UTC
```

### 4. Investigation

**Investigation Framework:**

```
┌─────────────────────────────────────┐
│         Five Whys Analysis          │
├─────────────────────────────────────┤
│ Problem: API slow response times    │
│                                     │
│ Why? Database queries slow          │
│   Why? High CPU on database         │
│     Why? Inefficient query          │
│       Why? Missing index            │
│         Why? Recent migration       │
│           didn't add index          │
│                                     │
│ Root Cause: Missing index after     │
│             migration               │
└─────────────────────────────────────┘
```

**Investigation Tools:**

```bash
# Database investigation
psql << 'EOF'
-- Active queries
SELECT pid, query_start, state, query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY query_start;

-- Slow queries
SELECT query, mean_time, calls
FROM pg_stat_statements
WHERE mean_time > 100
ORDER BY mean_time DESC
LIMIT 10;

-- Locks
SELECT * FROM pg_locks WHERE NOT granted;
EOF

# Application logs
tail -f /var/log/subjunctive/app.log | grep -E "ERROR|SLOW|TIMEOUT"

# System metrics
htop
iostat -x 1 5
netstat -an | grep ESTABLISHED | wc -l
```

### 5. Mitigation & Resolution

**Immediate Mitigation (Stop the bleeding):**
- Rollback recent deployment
- Restart affected services
- Scale up resources
- Enable maintenance mode
- Route traffic away from affected systems

**Permanent Resolution:**
- Deploy fix
- Add missing index
- Optimize query
- Patch vulnerability
- Update configuration

**Verification:**
```bash
# Verify fix
curl -w "\nTime: %{time_total}s\n" https://api.subjunctivepractice.com/api/v1/exercises

# Monitor error rate
watch -n 5 'tail -100 /var/log/subjunctive/app.log | grep ERROR | wc -l'

# Check performance metrics
# Review dashboard for 15-30 minutes
```

### 6. Recovery

**Recovery Checklist:**
- [ ] Verify all systems operational
- [ ] Confirm fix resolves issue
- [ ] Monitor for regression
- [ ] Update status page
- [ ] Notify stakeholders
- [ ] Schedule post-mortem

---

## Common Incident Scenarios

### Scenario 1: Database Connection Exhaustion

**Symptoms:**
- "Too many connections" errors
- Slow API responses
- Timeouts

**Immediate Actions:**
```bash
# 1. Check connection count
psql -c "SELECT count(*) FROM pg_stat_activity;"
psql -c "SHOW max_connections;"

# 2. Identify connection sources
psql -c "SELECT application_name, count(*) FROM pg_stat_activity GROUP BY application_name;"

# 3. Kill idle connections
psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle' AND state_change < now() - interval '1 hour';"

# 4. Increase pool size (temporary)
# Update backend configuration
# Restart application

# 5. Permanent fix
# Optimize connection pooling
# Add connection limits per service
```

### Scenario 2: Memory Leak

**Symptoms:**
- Increasing memory usage
- Application crashes
- OOM errors

**Immediate Actions:**
```bash
# 1. Check memory usage
ps aux | grep -E "gunicorn|uvicorn" | awk '{print $4, $6, $11}'

# 2. Restart affected workers
kill -HUP $(cat /var/run/backend.pid)

# 3. Monitor memory growth
watch -n 5 'ps aux | grep gunicorn | awk "{sum+=\$6} END {print sum/1024 \"MB\"}"'

# 4. Investigate leak
# Use memory profiler
pip install memory-profiler
python -m memory_profiler backend/main.py

# 5. Permanent fix
# Fix memory leak in code
# Deploy patch
```

### Scenario 3: DDoS Attack

**Symptoms:**
- Unusual traffic spike
- High server load
- Legitimate users cannot access

**Immediate Actions:**
```bash
# 1. Verify attack
tail -1000 /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -20

# 2. Enable rate limiting
# Update nginx config
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20;

# 3. Block attacking IPs
# Add to firewall
for ip in $(cat attacking_ips.txt); do
    ufw deny from $ip
done

# 4. Enable CloudFlare protection
# Enable "Under Attack" mode

# 5. Contact hosting provider
# Request DDoS mitigation
```

### Scenario 4: Data Breach

**CRITICAL - Follow Security Incident Protocol**

**Immediate Actions:**
```bash
# 1. ISOLATE affected systems
# Disconnect from network if necessary
sudo systemctl stop subjunctive-backend

# 2. PRESERVE evidence
# Take snapshots, save logs
tar -czf evidence-$(date +%Y%m%d).tar.gz /var/log/subjunctive/

# 3. ASSESS scope
# Check logs for unauthorized access
grep "401\|403" /var/log/nginx/access.log > unauthorized_access.log

# 4. CONTAIN breach
# Revoke all sessions
redis-cli FLUSHDB

# Rotate all secrets
# Update JWT_SECRET_KEY
# Update database passwords

# 5. NOTIFY
# Legal team
# Security team
# Affected users (if required by law)

# 6. DO NOT
# Delete logs
# Make changes without documentation
# Delay notification
```

### Scenario 5: SSL Certificate Expired

**Symptoms:**
- SSL/TLS errors
- "Certificate expired" warnings
- API calls failing

**Immediate Actions:**
```bash
# 1. Verify expiration
echo | openssl s_client -servername api.subjunctivepractice.com \
    -connect api.subjunctivepractice.com:443 2>/dev/null | \
    openssl x509 -noout -dates

# 2. Renew certificate
sudo certbot renew --force-renewal

# 3. Reload web server
sudo systemctl reload nginx

# 4. Verify fix
curl -I https://api.subjunctivepractice.com

# 5. Setup auto-renewal
sudo crontab -e
# Add: 0 0 * * 0 certbot renew --quiet && systemctl reload nginx
```

---

## Communication Protocols

### Status Page Updates

**Template:**
```
[STATUS] Brief Issue Description
Posted: MMM DD, HH:MM UTC

Detailed description of the issue and impact.

Current status: [Investigating/Identified/Monitoring/Resolved]

Affected Services:
- Service A
- Service B

Workaround (if available):
Steps users can take to mitigate impact.

Next Update: MMM DD, HH:MM UTC
```

### Internal Updates

**Update Frequency:**
- P0: Every 15 minutes
- P1: Every 30 minutes
- P2: Every hour
- P3: As needed

**Update Template:**
```
Incident #123 Update [HH:MM UTC]

Status: [Investigating/Fixing/Monitoring/Resolved]

What we know:
- Key findings from investigation

What we're doing:
- Current actions being taken

Impact:
- Current user impact

ETA: [If known]

Next update: [HH:MM UTC]
```

### User Communication

**Notification Channels:**
1. Status page (primary)
2. Twitter/social media
3. Email (for extended outages)
4. In-app notification

**Communication Guidelines:**
- Be transparent but avoid technical jargon
- Focus on user impact
- Provide workarounds if available
- Set clear expectations for updates
- Acknowledge frustration

---

## Post-Incident Procedures

### Incident Closure

**Closure Checklist:**
- [ ] Incident resolved
- [ ] Monitoring confirms stability (24 hours)
- [ ] Status page updated to "Resolved"
- [ ] Internal communication sent
- [ ] Incident timeline documented
- [ ] Post-mortem scheduled

### Post-Mortem Meeting

**Schedule:** Within 48 hours of resolution

**Attendees:**
- Incident Commander
- Technical Lead
- All responders
- Relevant stakeholders

**Agenda:**
1. Incident timeline review
2. What went well
3. What could be improved
4. Root cause analysis
5. Action items
6. Prevention measures

**Post-Mortem Template:**
```markdown
# Post-Mortem: [Incident Title]

## Incident Summary
- Incident #: 123
- Date: 2025-01-15
- Duration: 2 hours 15 minutes
- Severity: P1
- Incident Commander: John Doe

## Impact
- Users Affected: 30%
- Revenue Impact: $X
- Services Affected: Backend API

## Timeline
14:00 - Database migration deployed
14:32 - Slow response alerts triggered
14:35 - Incident declared
14:40 - Root cause identified (missing index)
14:55 - Fix deployed
15:10 - Monitoring shows improvement
16:45 - Incident resolved

## Root Cause
Database migration script failed to create required index on
user_progress table, causing full table scans.

## What Went Well
- Quick detection (3 minutes)
- Effective triage
- Clear communication

## What Could Be Improved
- Migration testing process
- Index creation validation
- Rollback procedures

## Action Items
1. [ ] Add migration validation checks (Owner: DevOps, Due: Jan 20)
2. [ ] Update deployment checklist (Owner: IC, Due: Jan 17)
3. [ ] Improve monitoring for slow queries (Owner: DBA, Due: Jan 25)
4. [ ] Document rollback procedure (Owner: Team Lead, Due: Jan 19)

## Lessons Learned
- Always verify indexes after migrations
- Need better pre-deployment testing
- Communication worked well
```

---

## Incident Response Toolkit

### Quick Reference Commands

```bash
# System Status
curl https://api.subjunctivepractice.com/health
ps aux | grep -E "gunicorn|uvicorn"
netstat -tupln | grep LISTEN

# Database
psql -c "SELECT count(*) FROM pg_stat_activity;"
psql -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"

# Logs
tail -f /var/log/subjunctive/app.log
journalctl -u subjunctive-backend -f

# Resources
htop
free -h
df -h
iostat -x 1 5

# Network
netstat -an | grep ESTABLISHED | wc -l
tcpdump -i any port 8000

# Emergency Actions
sudo systemctl restart subjunctive-backend
railway rollback -e production
```

### Contact Information

**Emergency Contacts:**
```
Incident Commander: +1-555-0001
Technical Lead: +1-555-0002
DevOps On-Call: +1-555-0003
Security Team: +1-555-0004
```

**External Vendors:**
```
Railway Support: support@railway.app
Vercel Support: https://vercel.com/support
CloudFlare: https://www.cloudflare.com/support
```

**Escalation Hotlines:**
```
Engineering Manager: +1-555-0010
CTO: +1-555-0011
```

---

## Incident Response Checklist

**Detection Phase:**
- [ ] Alert acknowledged
- [ ] Severity assessed
- [ ] IC assigned
- [ ] Incident channel created
- [ ] Initial assessment completed

**Response Phase:**
- [ ] Team assembled
- [ ] Investigation started
- [ ] Status page updated
- [ ] Internal communication sent
- [ ] Mitigation implemented

**Resolution Phase:**
- [ ] Fix deployed
- [ ] Verification completed
- [ ] Monitoring confirmed stable
- [ ] Status page updated
- [ ] Users notified

**Recovery Phase:**
- [ ] Services fully restored
- [ ] Documentation completed
- [ ] Post-mortem scheduled
- [ ] Action items created
- [ ] Runbook updated

---

Remember: **Communication is key during incidents. Keep stakeholders informed, even if you don't have all the answers yet.**
