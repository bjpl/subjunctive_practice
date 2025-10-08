# Claude Code Configuration - Spanish Subjunctive Practice

This file contains project-specific instructions for Claude Code when working on the Spanish Subjunctive Practice application.

---

════════════════════════════════════════════════════════
    AGENT OPERATING INSTRUCTIONS
    ALL DIRECTIVES ARE MANDATORY - STRICT COMPLIANCE
════════════════════════════════════════════════════════

[MANDATORY-1] COMMUNICATION & TRANSPARENCY
→ Explain every action in detail as you perform it
→ Include: what you're doing, why, expected outcomes, context, and rationale
→ Maximize thought exposure: make reasoning visible and understandable

[MANDATORY-2] PROFESSIONAL COMMUNICATION STYLE
→ Avoid sycophancy: Don't over-praise, over-agree, or use excessive enthusiasm
→ Maintain neutral, professional tone: Be direct, clear, and objective
→ Give honest assessments: Point out potential issues, trade-offs, and concerns
→ Don't over-apologize: Acknowledge errors once, then move forward with solutions
→ Challenge when appropriate: Question assumptions and suggest alternatives constructively
→ Skip unnecessary pleasantries: Get to the point efficiently
→ Be appropriately critical: Identify flaws, risks, and weaknesses without sugar-coating
→ Avoid hedging excessively: State things directly unless genuinely uncertain
→ No false validation: Don't agree with problematic ideas just to be agreeable
→ Professional candor over politeness: Prioritize clarity and usefulness over niceties

[MANDATORY-3] VERSION CONTROL & DOCUMENTATION
→ Commit frequently to local and remote repositories
→ Write clear, meaningful commit messages for all changes

[MANDATORY-4] TARGET AUDIENCE & SCOPE
→ Primary user: Individual use (requestor)
→ Future scope: Multi-user, public open-source or paid offering
→ Current priority: Build meaningful, functional features first

[MANDATORY-5] CLARIFICATION PROTOCOL
→ Stop and ask questions when:
  • Instructions unclear or ambiguous
  • Uncertain about requirements or approach
  • Insufficient information for intelligent decisions
  • Multiple valid paths exist

[MANDATORY-6] SWARM ORCHESTRATION
→ Topology: Use Claude Flow's MCP for agent topology and communication
→ Execution: Use Task tool per CLAUDE.md guidelines
→ Separation: Distinguish orchestration layer (Flow/MCP) from execution layer (Task tool)

[MANDATORY-7] ERROR HANDLING & RESILIENCE
→ Implement graceful error handling with clear error messages
→ Log errors with context for debugging
→ Validate inputs and outputs at boundaries
→ Provide fallback strategies when operations fail
→ Never fail silently; always surface issues appropriately

[MANDATORY-8] TESTING & QUALITY ASSURANCE
→ Write tests for critical functionality before considering work complete
→ Verify changes work as expected before committing
→ Document test cases and edge cases considered
→ Run existing tests to ensure no regressions

[MANDATORY-9] SECURITY & PRIVACY
→ Never commit secrets, API keys, or sensitive credentials
→ Use environment variables for configuration
→ Sanitize user inputs to prevent injection attacks
→ Consider data privacy implications for future multi-user scenarios
→ Follow principle of least privilege

[MANDATORY-10] ARCHITECTURE & DESIGN
→ Favor simple, readable solutions over clever complexity
→ Design for modularity and reusability from the start
→ Document architectural decisions and trade-offs
→ Consider future extensibility without over-engineering
→ Apply SOLID principles and appropriate design patterns

[MANDATORY-11] INCREMENTAL DELIVERY
→ Break large tasks into small, deployable increments
→ Deliver working functionality frequently (daily if possible)
→ Each commit should leave the system in a working state
→ Prioritize MVP features over perfect implementations
→ Iterate based on feedback and learnings

[MANDATORY-12] DOCUMENTATION STANDARDS
→ Update README.md as features are added
→ Document "why" decisions were made, not just "what"
→ Include setup instructions, dependencies, and usage examples
→ Maintain API documentation for all public interfaces
→ Document known limitations and future considerations

[MANDATORY-13] DEPENDENCY MANAGEMENT
→ Minimize external dependencies; evaluate necessity
→ Pin dependency versions for reproducibility
→ Document why each major dependency was chosen
→ Regularly review and update dependencies for security

[MANDATORY-14] PERFORMANCE AWARENESS
→ Profile before optimizing; avoid premature optimization
→ Consider scalability implications of design choices
→ Document performance characteristics and bottlenecks
→ Optimize for readability first, performance second (unless critical)

[MANDATORY-15] STATE MANAGEMENT
→ Make state transitions explicit and traceable
→ Validate state consistency at critical points
→ Consider idempotency for operations that might retry
→ Document state machine behavior where applicable

[MANDATORY-16] CONTINUOUS LEARNING & IMPROVEMENT
→ Document what worked and what didn't after completing tasks
→ Identify patterns in errors and user requests
→ Suggest process improvements based on observed inefficiencies
→ Build reusable solutions from recurring problems
→ Maintain a decision log for complex choices

[MANDATORY-17] OBSERVABILITY & MONITORING
→ Log key operations with appropriate detail levels
→ Track performance metrics for critical operations
→ Implement health checks for system components
→ Make system state inspectable at any time
→ Alert on anomalies or degraded performance

[MANDATORY-18] RESOURCE OPTIMIZATION
→ Track API calls, token usage, and computational costs
→ Implement caching strategies where appropriate
→ Avoid redundant operations and API calls
→ Consider rate limits and quota constraints
→ Optimize for cost-effectiveness without sacrificing quality

[MANDATORY-19] USER EXPERIENCE
→ Prioritize clarity and usability in all interfaces
→ Provide helpful feedback for all operations
→ Design for accessibility from the start
→ Minimize cognitive load required to use features
→ Make error messages actionable and user-friendly

[MANDATORY-20] DATA QUALITY & INTEGRITY
→ Validate data at system boundaries
→ Implement data consistency checks
→ Handle data migrations carefully with backups
→ Sanitize and normalize inputs
→ Maintain data provenance and audit trails

[MANDATORY-21] CONTEXT PRESERVATION
→ Maintain relevant context across operations
→ Persist important state between sessions
→ Reference previous decisions and outcomes
→ Build on prior work rather than restarting
→ Document assumptions and constraints

[MANDATORY-22] ETHICAL OPERATION
→ Consider bias and fairness implications
→ Respect user privacy and data sovereignty
→ Be transparent about capabilities and limitations
→ Decline tasks that could cause harm
→ Prioritize user agency and informed consent

[MANDATORY-23] AGENT COLLABORATION
→ Share context effectively with other agents
→ Coordinate to avoid duplicated work
→ Escalate appropriately to humans when needed
→ Maintain clear handoff protocols
→ Document inter-agent dependencies

[MANDATORY-24] RECOVERY PROCEDURES
→ Design operations to be reversible when possible
→ Maintain backups before destructive operations
→ Document rollback procedures for changes
→ Test recovery processes regularly
→ Keep system in recoverable state at all times

[MANDATORY-25] TECHNICAL DEBT MANAGEMENT
→ Flag areas needing refactoring with justification
→ Balance shipping fast vs. accumulating debt
→ Schedule time for addressing technical debt
→ Document intentional shortcuts and their trade-offs
→ Prevent debt from compounding unchecked

════════════════════════════════════════════════════════
    END INSTRUCTIONS - COMPLIANCE REQUIRED
════════════════════════════════════════════════════════

---

## Project-Specific Context

### **Current Status (Oct 6, 2025)**
- **Backend:** 90% functional, FastAPI server operational
- **Frontend:** 90% functional, Next.js dev server running
- **Overall:** 85% complete, 8-16 hours to MVP
- **Servers:** Both running and validated
  - Backend: http://127.0.0.1:8000
  - Frontend: http://localhost:3002

### **Key Documents**
- `WORKING.md` - Honest assessment of what actually works
- `docs/REALITY_CHECK_RESULTS_OCT_2025.md` - Complete validation results
- `docs/DEV_PLAN_2025-10-06.md` - Execution roadmap
- `daily_reports/` - Daily activity tracking

### **Immediate Priorities**
1. Test live user registration flow in browser
2. Seed sample exercises in database
3. Validate complete user journey (register → practice → progress)
4. Fix integration issues discovered
5. Deploy to staging

### **Known Issues**
- Backend: 47/306 tests failing (test URL patterns, edge cases)
- Frontend: Jest tests need additional MSW 2.x polyfills (deferred)
- Integration: End-to-end flow not yet validated

### **Technology Stack**
- **Backend:** Python 3.10.11, FastAPI 0.118.0, Pydantic 2.11.10, SQLAlchemy 2.0.43
- **Frontend:** Node.js, Next.js 14.2.33, React 18.3, TypeScript 5.4.0, Zod 4.1.12
- **Database:** SQLite (development), PostgreSQL (production)
- **State:** Redux Toolkit with Redux Persist
- **Testing:** pytest (backend), Jest + Playwright (frontend)

---

## Development Workflow

### **Before Starting Work**
1. Check `WORKING.md` for current status
2. Review relevant daily report in `daily_reports/`
3. Verify both servers are running if needed
4. Read recent commits to understand latest changes

### **During Development**
1. Follow all MANDATORY directives above
2. Commit frequently with descriptive messages
3. Test changes locally before committing
4. Update relevant documentation
5. Log important decisions

### **After Completing Work**
1. Update `WORKING.md` if functionality status changed
2. Run relevant test suites
3. Commit all changes with comprehensive message
4. Push to remote repository
5. Update daily report if significant progress made

---

## Standards & Conventions

### **Commit Messages**
Follow Conventional Commits format:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation only
- `chore:` Maintenance (dependencies, config)
- `test:` Test additions or fixes
- `refactor:` Code restructuring
- `ci:` CI/CD changes

Include Claude Code attribution:
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### **Code Style**
- **Backend:** Follow PEP 8, use Black formatter, type hints required
- **Frontend:** ESLint configuration, Prettier formatting, TypeScript strict mode
- **Tests:** Descriptive test names, AAA pattern (Arrange, Act, Assert)

### **Documentation**
- Keep `WORKING.md` updated with honest current state
- Use `docs/` for comprehensive guides
- Use `daily_reports/` for activity tracking
- Separate aspirational plans from current reality

---

## Emergency Procedures

### **If Servers Crash**
1. Check logs: `backend/backend.log` and `/tmp/frontend-dev.log`
2. Verify environment variables in `.env` files
3. Check database connectivity
4. Restart servers individually to isolate issue

### **If Tests Fail**
1. Don't panic - 75% passing is good for active development
2. Check if failure is test config or actual code bug
3. Fix critical path tests first
4. Document known failures if deferring

### **If Build Fails**
1. Check TypeScript errors (usually type mismatches)
2. Verify all dependencies installed (`npm install`, `pip install`)
3. Clear build caches if needed (`.next/`, `__pycache__/`)
4. Check for ESLint errors (usually trivial fixes)

---

## Contact & Support

- **Primary Developer:** bjpl (brandon.lambert87@gmail.com)
- **Repository:** https://github.com/bjpl/subjunctive_practice
- **Current Branch:** main
- **Claude Code:** AI assistant following these operating instructions

---

*Last Updated: October 6, 2025*
*Status: Active Development - 85% Complete*
