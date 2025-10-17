# Architecture Decision Record (ADR)
## Spanish Subjunctive Practice Application Backend Choice

**Date:** 2025-08-26  
**Status:** PROPOSED  
**Deciders:** Development Team, Product Owner  
**Technical Story:** Migration from desktop PyQt application to web-based solution

## Context and Problem Statement

The Spanish Subjunctive Practice Application currently exists as a desktop-only PyQt application with local data storage. We need to modernize this to a web-based solution that supports:

- Multi-platform access (web, mobile, desktop)
- User authentication and personalization
- Cloud-based progress synchronization
- Real-time features and collaboration
- Scalable architecture for growing user base
- Advanced learning analytics and AI integration

We must choose between **Supabase (Backend-as-a-Service)** and **FastAPI (Custom Backend)** as our backend architecture.

## Decision Drivers

### Functional Requirements
- User authentication and profile management
- Exercise generation with adaptive difficulty
- Progress tracking and analytics
- Real-time features (live updates, collaboration)
- File storage for user data
- Advanced accessibility features
- Multi-language support
- Offline functionality

### Non-Functional Requirements
- **Development Speed:** Time to market is critical
- **Scalability:** Support 1,000+ concurrent users initially, 50,000+ eventually
- **Performance:** Sub-200ms API response times
- **Security:** GDPR compliance, secure data handling
- **Maintainability:** Long-term codebase sustainability
- **Cost:** Predictable scaling costs
- **Team Expertise:** Current team has strong Python/JavaScript skills

### Constraints
- **Budget:** Limited initial funding
- **Timeline:** 3-month MVP deadline
- **Team Size:** 2-3 developers
- **Compliance:** Educational data privacy requirements

## Considered Options

### Option A: Supabase (Backend-as-a-Service)

**Architecture Overview:**
```
Frontend (React/Vue) ↔ Supabase Client SDK ↔ Supabase Platform
                                            ├─ PostgreSQL + RLS
                                            ├─ Real-time Engine
                                            ├─ Authentication
                                            ├─ Storage
                                            └─ Edge Functions
```

**Pros:**
- ✅ **Rapid Development:** 3-4 weeks to MVP vs 8-10 weeks
- ✅ **Built-in Authentication:** OAuth, MFA, user management included
- ✅ **Real-time by Default:** WebSocket subscriptions automatically configured
- ✅ **Row Level Security:** Multi-tenant security built into database
- ✅ **Auto-generated APIs:** REST and GraphQL endpoints from schema
- ✅ **Edge Functions:** Serverless compute with database access
- ✅ **Offline Support:** Built-in client-side caching and sync
- ✅ **Developer Experience:** Excellent tooling and documentation
- ✅ **Deployment:** Zero-config hosting and CDN

**Cons:**
- ❌ **Vendor Lock-in:** Significant migration cost if switching needed
- ❌ **Limited Customization:** Complex business logic requires workarounds
- ❌ **Cost Scaling:** Unpredictable costs at scale (user-based pricing)
- ❌ **Performance Limits:** Less control over query optimization
- ❌ **Edge Function Limitations:** Deno runtime, cold start latency
- ❌ **Complex Queries:** Limited support for advanced SQL operations

### Option B: FastAPI (Custom Backend)

**Architecture Overview:**
```
Frontend ↔ Load Balancer ↔ FastAPI App ↔ PostgreSQL
                           ├─ Redis Cache
                           ├─ Background Jobs
                           ├─ WebSocket Manager
                           └─ Custom Auth
```

**Pros:**
- ✅ **Full Control:** Complete customization of all business logic
- ✅ **Performance Optimization:** Fine-tuned caching, queries, algorithms
- ✅ **No Vendor Lock-in:** Can deploy anywhere, migrate easily
- ✅ **Python Ecosystem:** Full access to ML libraries, data tools
- ✅ **Advanced Analytics:** Custom algorithms for learning insights
- ✅ **Predictable Costs:** Infrastructure-based pricing
- ✅ **Complex Business Logic:** No limitations on backend processing
- ✅ **Enterprise Features:** Custom integrations, compliance controls

**Cons:**
- ❌ **Development Time:** 8-10 weeks to MVP vs 3-4 weeks
- ❌ **Infrastructure Complexity:** Manual setup of auth, real-time, caching
- ❌ **Maintenance Overhead:** Security updates, scaling, monitoring
- ❌ **Team Expertise Required:** Need experienced backend developers
- ❌ **Initial Setup Cost:** DevOps, monitoring, backup systems
- ❌ **Security Responsibility:** Must implement all security measures

## Decision Outcome

**Chosen Option:** **Supabase (Backend-as-a-Service)** with migration path to FastAPI

### Rationale

1. **Time to Market Priority:** The 3-month MVP deadline makes Supabase's rapid development crucial
2. **Team Efficiency:** Current team can focus on user experience rather than infrastructure
3. **Feature Completeness:** Built-in authentication, real-time, and storage cover 80% of requirements
4. **Risk Mitigation:** Can validate product-market fit before investing in custom backend
5. **Learning Application Fit:** Standard CRUD operations with some real-time features align well with BaaS model

### Implementation Strategy

**Phase 1: Supabase MVP (Months 1-3)**
- Implement core features with Supabase
- Validate user engagement and requirements
- Identify custom logic needs through real usage

**Phase 2: Enhancement (Months 4-6)**
- Add advanced features within Supabase capabilities
- Implement complex business logic in Edge Functions
- Scale to initial user base

**Phase 3: Evaluation (Months 7-9)**
- Assess performance, costs, and limitations
- Evaluate need for custom backend based on actual requirements
- Plan potential migration if necessary

**Phase 4: Migration (If Needed)**
- Gradual migration to FastAPI for specific components
- Maintain Supabase for authentication and basic CRUD
- Hybrid architecture leveraging strengths of both

## Implementation Details

### Database Schema with Supabase
```sql
-- Users (handled by Supabase Auth)
-- Automatic user management with auth.users table

-- User Progress with Row Level Security
CREATE TABLE user_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  exercise_type TEXT NOT NULL,
  correct_answers INTEGER DEFAULT 0,
  total_attempts INTEGER DEFAULT 0,
  streak_count INTEGER DEFAULT 0,
  difficulty_level INTEGER DEFAULT 1,
  mastered_topics JSONB DEFAULT '[]'::jsonb,
  weak_areas JSONB DEFAULT '[]'::jsonb,
  last_practiced TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can only access their own progress"
  ON user_progress FOR ALL
  USING (auth.uid() = user_id);

-- Exercise Sessions
CREATE TABLE exercise_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  session_start TIMESTAMPTZ DEFAULT NOW(),
  session_end TIMESTAMPTZ,
  exercises_completed INTEGER DEFAULT 0,
  accuracy_rate REAL DEFAULT 0,
  session_data JSONB DEFAULT '{}'::jsonb
);

-- Real-time subscriptions automatically available
```

### Edge Function for Exercise Generation
```typescript
// supabase/functions/generate-exercise/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async (req) => {
  const { user_id, exercise_type, difficulty_level } = await req.json()
  
  // Get user's learning history
  const { data: userProgress } = await supabase
    .from('user_progress')
    .select('*')
    .eq('user_id', user_id)
    .single()
  
  // Generate personalized exercise with OpenAI
  const exercise = await generateWithAI(userProgress, exercise_type, difficulty_level)
  
  return new Response(JSON.stringify(exercise))
})
```

### Migration Triggers
We will migrate to FastAPI if we encounter:

1. **Performance Issues:** API response times > 500ms consistently
2. **Cost Scaling:** Monthly costs exceed $500 for expected user base
3. **Customization Limits:** Core business logic can't be implemented effectively
4. **Advanced Analytics Needs:** ML models require complex data processing
5. **Enterprise Requirements:** Custom compliance or integration needs

### Risk Mitigation

**Vendor Lock-in Mitigation:**
- Use standard PostgreSQL features, avoid Supabase-specific extensions
- Keep business logic in client-side code or portable Edge Functions
- Document all Supabase-specific implementations for future migration
- Regular data exports and backup procedures

**Performance Monitoring:**
- Set up comprehensive monitoring from day one
- Track API response times, database query performance
- Monitor user engagement and feature usage
- Regular load testing as user base grows

**Cost Management:**
- Implement usage tracking and alerting
- Regular cost optimization reviews
- Plan for pricing tier changes
- Monitor competitors and alternatives

## Consequences

### Positive Consequences
- **Faster MVP delivery** enabling quicker user feedback
- **Lower initial development costs** and infrastructure complexity
- **Focus on user experience** rather than backend infrastructure
- **Built-in best practices** for security, performance, real-time features
- **Easier team onboarding** with comprehensive documentation

### Negative Consequences
- **Vendor dependency** requiring future migration planning
- **Limited customization** may constrain advanced features
- **Cost uncertainty** as user base scales
- **Performance constraints** for complex operations
- **Learning curve** for Supabase-specific patterns

### Neutral Consequences
- **Database choice locked to PostgreSQL** (acceptable for this use case)
- **JavaScript/TypeScript for Edge Functions** (team is comfortable with this)
- **Real-time features implementation** differs from custom WebSocket setup

## Compliance and Approval

**Technical Review:** ✅ Approved by Lead Developer  
**Product Review:** ✅ Approved by Product Owner  
**Security Review:** 🔄 Pending security assessment  
**Cost Review:** ✅ Approved within budget constraints

## Follow-up Actions

1. **Week 1:** Set up Supabase project and initial database schema
2. **Week 2:** Implement user authentication and basic CRUD operations
3. **Week 3:** Add real-time features and Edge Functions
4. **Week 4:** Integrate with frontend and conduct initial testing
5. **Month 2:** Performance monitoring setup and optimization
6. **Month 3:** User testing and feedback incorporation
7. **Quarterly:** Architectural review and migration decision evaluation

## Success Metrics

**Development Metrics:**
- Time to MVP: Target 3 months (vs 6+ months with custom backend)
- Feature completeness: 95% of requirements met with Supabase
- Development team satisfaction: >8/10 with developer experience

**Performance Metrics:**
- API response time: <200ms for 95% of requests
- Real-time message latency: <100ms
- User authentication success rate: >99.5%
- Database query performance: <50ms for 95% of queries

**Business Metrics:**
- User engagement: Target active usage within first month
- Cost efficiency: Stay within $100/month for first 1000 users
- Scalability: Support 50% month-over-month user growth
- Feature velocity: Maintain 2-week sprint cycles

## References and Links

- [Supabase Documentation](https://supabase.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Current PyQt Application Analysis](./SUPABASE_VS_FASTAPI_ARCHITECTURE_ANALYSIS.md)
- [Implementation Examples](../examples/)
- [Security Requirements Document](./SECURITY_REQUIREMENTS.md)
- [Performance Requirements](./PERFORMANCE_REQUIREMENTS.md)

---

**Document Owner:** Technical Architecture Team  
**Last Updated:** 2025-08-26  
**Next Review:** 2025-11-26 (Quarterly Review)