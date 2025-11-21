# 📋 PCCM Integration Project Tasks

**Complete checklist for integrating PCCM Schedule and Moonlighter systems**

Use this document to create tasks in your GitHub Project board. Each task includes:
- 📝 Clear description
- ✅ Acceptance criteria
- 📎 Relevant files/locations
- ⚠️ Dependencies
- 💡 Implementation notes

---

## 🎯 Stage 1: Current State (COMPLETE) ✅

### ✅ DONE: MVP Vacation Scheduler
**Status**: Production  
**Repository**: [PCCMSchedule](https://github.com/kbenfield-716ths/PCCMSchedule)

---

## 🚀 Stage 2: Moonlighting Integration (IN PROGRESS)

### Phase 2.1: Planning & Architecture

#### Task 2.1.1: Review Current Systems
**Priority**: High  
**Estimate**: 2 hours

**Description**:
- Review PCCMSchedule production code
- Review moonlighter-web production code
- Document all existing features
- Identify integration points
- Map shared data structures

**Acceptance Criteria**:
- [ ] List of all features in both systems
- [ ] Data model comparison documented
- [ ] Integration touchpoints identified
- [ ] Shared vs. unique components mapped

**Files**:
- `docs/CURRENT_SYSTEMS_COMPARISON.md` (create this)
- Production repos for reference

**Notes**:
- Both systems use Supabase
- Both have faculty authentication
- Need to identify schema overlaps

---

#### Task 2.1.2: Design Unified Database Schema
**Priority**: High  
**Estimate**: 4 hours  
**Dependencies**: Task 2.1.1

**Description**:
- Merge faculty tables from both systems
- Add moonlighting_requests table
- Add moonlighting_assignments table
- Create unified views for reporting
- Design migration strategy

**Acceptance Criteria**:
- [ ] Complete SQL schema for integrated system
- [ ] Migration scripts from both systems
- [ ] Backward compatibility plan
- [ ] Test data scripts

**Files**:
- `database/migrations/001-merge-faculty-tables.sql`
- `database/migrations/002-add-moonlighting-tables.sql`
- `database/migrations/003-create-unified-views.sql`
- `database/integrated-schema.sql`

**Notes**:
```sql
-- Key tables to create/modify:
-- 1. Unified faculty table
-- 2. moonlighting_requests (faculty_id, night_date, priority, status)
-- 3. moonlighting_assignments (faculty_id, night_date, assigned_at)
-- 4. moonlighting_nights (date, min_staff, max_staff, night_type)
```

---

#### Task 2.1.3: Define Moonlighting Business Rules
**Priority**: High  
**Estimate**: 3 hours

**Description**:
- Document point rules for moonlighting
- Define fairness constraints
- Specify minimum/maximum shifts
- Create request priority rules
- Document conflict resolution

**Acceptance Criteria**:
- [ ] Complete business rules document
- [ ] Examples for common scenarios
- [ ] Edge cases identified
- [ ] Admin override policies

**Files**:
- `docs/MOONLIGHTING_BUSINESS_RULES.md`

**Notes**:
- Faculty request nights they WANT to work (opposite of vacation)
- System must ensure fair distribution
- Consider: seniority, past assignments, work limits
- Need conflict resolution (multiple requests, one slot)

---

### Phase 2.2: Database Setup

#### Task 2.2.1: Create Test Supabase Project
**Priority**: High  
**Estimate**: 1 hour

**Description**:
- Create new Supabase project for integration testing
- Set up environment variables
- Configure authentication
- Test connection

**Acceptance Criteria**:
- [ ] New Supabase project created
- [ ] Connection credentials documented
- [ ] Test connection successful
- [ ] Environment documented in README

**Files**:
- `database/SUPABASE_SETUP.md`
- `.env.example` (create this)

**Notes**:
- Keep separate from production databases
- Document connection string format
- Add to .gitignore

---

#### Task 2.2.2: Run Migration Scripts
**Priority**: High  
**Estimate**: 2 hours  
**Dependencies**: Tasks 2.1.2, 2.2.1

**Description**:
- Apply faculty table migrations
- Create moonlighting tables
- Set up Row Level Security (RLS)
- Create necessary views/functions
- Load test data

**Acceptance Criteria**:
- [ ] All tables created successfully
- [ ] RLS policies applied
- [ ] Views/functions working
- [ ] Test data loaded
- [ ] Can query all tables

**Files**:
- Execute all SQL files in `database/migrations/`
- `database/test-data/faculty.sql`
- `database/test-data/moonlighting-nights.sql`

**Notes**:
- Test RLS policies thoroughly
- Verify foreign key constraints
- Check indexes for performance

---

#### Task 2.2.3: Create Database Views for Dashboard
**Priority**: Medium  
**Estimate**: 3 hours  
**Dependencies**: Task 2.2.2

**Description**:
- Create view for faculty dashboard stats
- Create view for admin overview
- Create view for moonlighting availability
- Optimize for performance

**Acceptance Criteria**:
- [ ] `faculty_moonlight_stats` view created
- [ ] `admin_moonlight_overview` view created
- [ ] `available_moonlight_nights` view created
- [ ] All views tested with sample data
- [ ] Performance acceptable (<100ms)

**Files**:
- `database/migrations/004-dashboard-views.sql`

**SQL Example**:
```sql
CREATE VIEW faculty_moonlight_stats AS
SELECT 
  f.id,
  f.name,
  COUNT(DISTINCT mr.id) AS total_requests,
  COUNT(DISTINCT ma.id) AS total_assigned,
  -- etc
FROM faculty f
LEFT JOIN moonlighting_requests mr ON ...
LEFT JOIN moonlighting_assignments ma ON ...
GROUP BY f.id;
```

---

### Phase 2.3: Frontend Integration

#### Task 2.3.1: Create Unified Navigation
**Priority**: High  
**Estimate**: 3 hours

**Description**:
- Design combined sidebar navigation
- Add moonlighting section
- Update dashboard to show both systems
- Ensure mobile responsive

**Acceptance Criteria**:
- [ ] Navigation includes both vacation and moonlighting
- [ ] Clear section separation
- [ ] Active page indication
- [ ] Mobile menu works
- [ ] Consistent styling

**Files**:
- `integration/dashboard.html`
- `integration/shared/navigation.js`

**Notes**:
- Use existing PCCM Schedule navigation as base
- Add new items: "Moonlighting Requests", "Moonlighting Schedule"
- Maintain current design system

---

#### Task 2.3.2: Build Moonlighting Request Interface
**Priority**: High  
**Estimate**: 6 hours  
**Dependencies**: Task 2.2.2

**Description**:
- Create calendar view for available nights
- Add request submission form
- Show current requests
- Display assignment status
- Add cancellation capability

**Acceptance Criteria**:
- [ ] Calendar shows available nights
- [ ] Can submit requests with priority
- [ ] Can view own requests
- [ ] Can cancel unassigned requests
- [ ] Real-time status updates
- [ ] Mobile friendly

**Files**:
- `integration/moonlighting/request.html`
- `integration/moonlighting/request.js`

**Features**:
- Calendar highlighting: available (green), requested (yellow), assigned (blue)
- Priority selection (1-5)
- Notes field for special requests
- Conflict warnings

---

#### Task 2.3.3: Build Admin Moonlighting Management
**Priority**: High  
**Estimate**: 6 hours  
**Dependencies**: Task 2.3.2

**Description**:
- Create admin view of all requests
- Show coverage gaps
- Manual assignment interface
- Bulk operations
- Reports and exports

**Acceptance Criteria**:
- [ ] View all requests by night
- [ ] See coverage gaps highlighted
- [ ] Can manually assign faculty
- [ ] Can run auto-assignment algorithm
- [ ] Can export schedule
- [ ] Conflict detection works

**Files**:
- `integration/admin/moonlighting.html`
- `integration/admin/moonlighting-admin.js`

**Features**:
- Night-by-night grid view
- Filter by faculty, date range, status
- Drag-and-drop assignment
- One-click conflict resolution

---

#### Task 2.3.4: Update Dashboard Stats
**Priority**: Medium  
**Estimate**: 2 hours  
**Dependencies**: Tasks 2.2.3, 2.3.1

**Description**:
- Add moonlighting stats cards
- Show upcoming assignments
- Display request status
- Add quick actions

**Acceptance Criteria**:
- [ ] Stats cards show moonlighting data
- [ ] Upcoming assignments listed
- [ ] Quick "request a night" button
- [ ] Visual consistency with existing design

**Files**:
- `integration/dashboard.html` (modify stats section)

**Stats to show**:
- Moonlighting shifts this month
- Pending requests
- Total assignments this year
- Next scheduled shift

---

### Phase 2.4: Optimization Algorithm

#### Task 2.4.1: Design Algorithm Requirements
**Priority**: High  
**Estimate**: 3 hours

**Description**:
- Define optimization objectives
- List all constraints
- Determine fairness metrics
- Plan algorithm approach

**Acceptance Criteria**:
- [ ] Objectives ranked by priority
- [ ] Hard constraints documented
- [ ] Soft constraints documented
- [ ] Fairness definition agreed upon
- [ ] Algorithm approach selected

**Files**:
- `docs/ALGORITHM_SPECIFICATION.md`

**Objectives** (example):
1. Maximize coverage (all nights staffed)
2. Maximize request satisfaction
3. Minimize max shifts per person (fairness)
4. Respect seniority/experience

**Constraints**:
- Hard: Min/max staff per night, max shifts per month
- Soft: Preference priority, consecutive nights, weekends

---

#### Task 2.4.2: Implement Assignment Algorithm
**Priority**: High  
**Estimate**: 8 hours  
**Dependencies**: Task 2.4.1

**Description**:
- Implement constraint solver
- Add fairness distribution
- Handle edge cases
- Create test scenarios

**Acceptance Criteria**:
- [ ] Algorithm runs successfully
- [ ] All hard constraints respected
- [ ] Fair distribution verified
- [ ] Edge cases handled
- [ ] Performance acceptable (<5 seconds)
- [ ] Comprehensive tests pass

**Files**:
- `integration/algorithms/moonlighting-optimizer.py`
- `tests/algorithm-tests.py`

**Approach**:
```python
# Using PuLP or OR-Tools
# 1. Load requests and constraints
# 2. Define decision variables
# 3. Set up objective function
# 4. Add constraints
# 5. Solve and return assignments
```

---

#### Task 2.4.3: Create Algorithm API Endpoint
**Priority**: Medium  
**Estimate**: 4 hours  
**Dependencies**: Task 2.4.2

**Description**:
- Create Supabase Edge Function or Python endpoint
- Accept requests and constraints
- Run algorithm
- Return assignments
- Handle errors

**Acceptance Criteria**:
- [ ] Endpoint accessible via HTTP
- [ ] Input validation works
- [ ] Algorithm executes successfully
- [ ] Returns JSON assignments
- [ ] Error handling robust

**Files**:
- `backend/moonlighting-optimizer-api.py`
- `database/functions/run_optimizer.sql`

**Notes**:
- Consider Supabase Edge Functions (TypeScript/Deno)
- Or: Simple Python API (Flask/FastAPI)
- Or: Database function if algorithm simple enough

---

### Phase 2.5: Testing & Validation

#### Task 2.5.1: Unit Tests for Algorithm
**Priority**: High  
**Estimate**: 4 hours  
**Dependencies**: Task 2.4.2

**Description**:
- Test algorithm with various scenarios
- Test constraint violations
- Test fairness metrics
- Test performance with realistic data

**Acceptance Criteria**:
- [ ] >90% code coverage
- [ ] All constraint scenarios tested
- [ ] Fairness verified in tests
- [ ] Performance benchmarks met
- [ ] Edge cases covered

**Files**:
- `tests/test_moonlighting_algorithm.py`
- `tests/fixtures/test_scenarios.json`

**Test Scenarios**:
1. More requests than slots
2. Fewer requests than slots
3. Conflicting preferences
4. Seniority tie-breaking
5. Maximum shifts reached

---

#### Task 2.5.2: Integration Tests
**Priority**: High  
**Estimate**: 4 hours  
**Dependencies**: Phase 2.3 complete

**Description**:
- Test complete user workflows
- Test admin workflows
- Verify data consistency
- Test edge cases

**Acceptance Criteria**:
- [ ] Faculty can submit requests
- [ ] Admin can review/assign
- [ ] Algorithm produces valid assignments
- [ ] Database constraints respected
- [ ] No data corruption

**Files**:
- `tests/integration/test_moonlighting_workflow.js`

**Workflows to test**:
1. Faculty submits request → Admin runs algorithm → Faculty sees assignment
2. Faculty cancels request → Admin re-runs algorithm
3. Multiple faculty request same night → Fair resolution

---

#### Task 2.5.3: User Acceptance Testing
**Priority**: High  
**Estimate**: Variable

**Description**:
- Create UAT checklist
- Recruit beta testers
- Collect feedback
- Fix critical issues

**Acceptance Criteria**:
- [ ] UAT checklist completed
- [ ] 5+ faculty test the system
- [ ] Critical bugs fixed
- [ ] Feedback incorporated
- [ ] System accepted by users

**Files**:
- `tests/UAT_CHECKLIST.md`
- `tests/BETA_FEEDBACK.md`

---

### Phase 2.6: Documentation & Deployment

#### Task 2.6.1: Write User Documentation
**Priority**: Medium  
**Estimate**: 4 hours

**Description**:
- How to request moonlighting shifts
- How assignments work
- FAQs
- Troubleshooting guide

**Acceptance Criteria**:
- [ ] Complete user guide
- [ ] Screenshots included
- [ ] FAQs comprehensive
- [ ] Accessible to non-technical users

**Files**:
- `docs/MOONLIGHTING_USER_GUIDE.md`

---

#### Task 2.6.2: Write Admin Documentation
**Priority**: Medium  
**Estimate**: 3 hours

**Description**:
- How to manage requests
- How to run algorithm
- Manual assignment process
- Reporting and exports

**Acceptance Criteria**:
- [ ] Complete admin guide
- [ ] All features documented
- [ ] Screenshots included
- [ ] Troubleshooting section

**Files**:
- `docs/MOONLIGHTING_ADMIN_GUIDE.md`

---

#### Task 2.6.3: Deployment to Production
**Priority**: High  
**Estimate**: 4 hours  
**Dependencies**: All Phase 2.5 tasks complete

**Description**:
- Backup production database
- Run migration scripts on production
- Deploy frontend to GitHub Pages
- Deploy backend (if separate)
- Verify everything works

**Acceptance Criteria**:
- [ ] Production backup created
- [ ] Migrations run successfully
- [ ] Frontend deployed
- [ ] Backend deployed (if applicable)
- [ ] Smoke tests pass
- [ ] Rollback plan ready

**Files**:
- `scripts/deploy-to-production.sh`
- `DEPLOYMENT_CHECKLIST.md`

**Critical Steps**:
1. Announce maintenance window
2. Backup database
3. Run migrations
4. Deploy new code
5. Verify critical paths
6. Monitor for issues

---

## 📊 Stage 3: Clinical Schedule Automation (FUTURE)

### Phase 3.1: Planning

#### Task 3.1.1: Define Clinical Schedule Requirements
**Priority**: Medium (Future)  
**Estimate**: 8 hours

**Description**:
- Weekly inpatient service requirements
- Rotation rules
- Coverage constraints
- Integration with Stages 1 & 2

**Files**:
- `docs/STAGE_3_CLINICAL_SCHEDULE.md`

---

#### Task 3.1.2: Design Clinical Schedule Algorithm
**Priority**: Medium (Future)  
**Estimate**: 12 hours

**Description**:
- Multi-week scheduling algorithm
- Consider vacation and moonlighting
- Fair rotation
- Subspecialty coverage

---

### Phase 3.2: Implementation
*(Tasks to be defined during Stage 3 planning)*

---

## 🔌 Stage 4: QGenda Integration (FUTURE)

### Phase 4.1: QGenda API Research

#### Task 4.1.1: Study QGenda API Documentation
**Priority**: Low (Future)  
**Estimate**: 6 hours

**Description**:
- Review QGenda API capabilities
- Understand authentication
- Map data structures
- Plan integration points

**Files**:
- `docs/QGENDA_API_NOTES.md`

---

#### Task 4.1.2: Build Export Function
**Priority**: Low (Future)  
**Estimate**: 8 hours

**Description**:
- Create CSV export matching QGenda format
- Or API push to QGenda
- Schedule data
- Assignment data

**Files**:
- `scripts/export-to-qgenda.py`

---

## 🏷️ Labels for GitHub Project

Create these labels in your repository:

- `stage-1` - Current MVP (green)
- `stage-2` - Moonlighting (blue)
- `stage-3` - Clinical Schedule (yellow)
- `stage-4` - QGenda (orange)
- `priority-high` - Critical path (red)
- `priority-medium` - Important (orange)
- `priority-low` - Nice to have (gray)
- `type-frontend` - UI work (purple)
- `type-backend` - Database/API (teal)
- `type-algorithm` - Optimization (pink)
- `type-docs` - Documentation (white)
- `type-testing` - QA work (lime)
- `blocked` - Can't proceed (red)

---

## 📅 Milestones

### Milestone 1: Stage 2 Planning Complete
- All Phase 2.1 tasks done
- Database schema finalized
- Ready to implement

### Milestone 2: Stage 2 Database Ready
- All Phase 2.2 tasks done
- Test database operational
- Ready for frontend work

### Milestone 3: Stage 2 MVP
- Core moonlighting features working
- Faculty can request shifts
- Admin can assign manually

### Milestone 4: Stage 2 Algorithm Complete
- Auto-assignment working
- Fair distribution verified
- Production ready

### Milestone 5: Stage 2 Production
- Deployed to production
- Documentation complete
- Users trained

---

## 📈 Progress Tracking

Use this template for weekly updates:

```markdown
## Week of [Date]

### Completed ✅
- Task 2.1.1: Reviewed both systems
- Task 2.1.2: Designed unified schema

### In Progress 🚧
- Task 2.2.1: Setting up test database (80%)
- Task 2.3.1: Building navigation (30%)

### Blocked 🚫
- Task 2.4.2: Waiting for business rules sign-off

### Next Week 📅
- Complete test database setup
- Start moonlighting request interface
- Review algorithm requirements
```

---

## 🎯 Quick Reference: Critical Path

**Must be done in this order:**

1. Task 2.1.2 (Database Design)
2. Task 2.2.1 (Test Database)
3. Task 2.2.2 (Run Migrations)
4. Task 2.3.2 (Request Interface)
5. Task 2.4.2 (Algorithm)
6. Task 2.5.2 (Integration Tests)
7. Task 2.6.3 (Deploy to Production)

---

**Last Updated**: November 21, 2025  
**Total Tasks**: 35+  
**Current Focus**: Stage 2 Planning & Architecture
