# 🚀 PCCM Integration Plan

**Complete 4-Stage Roadmap for Faculty Scheduling System**

---

## 📊 System Overview

The PCCM Faculty Scheduling System will evolve through four stages, each building on the previous to create a comprehensive, automated scheduling solution.

### Vision
A fully integrated system that:
- ✅ Fairly allocates vacation time using economic points
- ✅ Schedules moonlighting shifts based on faculty preferences
- ✅ Automates weekly clinical service assignments
- ✅ Exports seamlessly to QGenda enterprise system

---

## 🎯 Stage 1: Time-Off Scheduler (COMPLETE) ✅

### Status: PRODUCTION
**Repository**: [PCCMSchedule](https://github.com/kbenfield-716ths/PCCMSchedule)

### Features Implemented
- ✅ Point-based vacation allocation system
- ✅ Faculty authentication and profiles
- ✅ Week selection interface (Available/Unavailable/Requested)
- ✅ Real-time points tracking
- ✅ Admin panel for faculty management
- ✅ Draft priority system (holiday coverage)
- ✅ Modern, responsive UI
- ✅ Mobile-friendly design

### Key Technologies
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Backend**: Supabase (PostgreSQL + Auth)
- **Hosting**: GitHub Pages (free)
- **Database**: Supabase free tier

### Business Logic
- Points = 100 × Clinical Effort % × Rank Multiplier
- Week costs: Regular (5), Summer (7), Spring Break (12), Major Holidays (15)
- Volunteer bonuses for working high-demand weeks
- Draft priority based on previous year's holiday coverage

---

## 🚧 Stage 2: Moonlighting Integration (IN PROGRESS)

### Goal
Add moonlighting shift scheduling where faculty REQUEST nights they WANT to work (opposite of vacation requests).

### New Features
1. **Moonlighting Request Interface**
   - Calendar view of available nights
   - Faculty can request specific nights
   - Priority levels for requests
   - Request tracking and status

2. **Assignment Algorithm**
   - Auto-assign based on requests and constraints
   - Fair distribution across faculty
   - Respect maximum shifts per person
   - Handle conflicts (multiple requests, one slot)

3. **Admin Tools**
   - Review all requests
   - Manual assignment override
   - Coverage gap visualization
   - Export assignments

4. **Integration with Stage 1**
   - Unified authentication
   - Single dashboard showing both vacation and moonlighting
   - Shared faculty database
   - Combined reporting

### Technical Architecture

#### Database Changes
```sql
-- New tables
CREATE TABLE moonlighting_nights (
  id UUID PRIMARY KEY,
  night_date DATE NOT NULL,
  min_staff INTEGER DEFAULT 1,
  max_staff INTEGER DEFAULT 2,
  night_type VARCHAR(50), -- weekday, weekend, holiday
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE moonlighting_requests (
  id UUID PRIMARY KEY,
  faculty_id UUID REFERENCES faculty(id),
  night_id UUID REFERENCES moonlighting_nights(id),
  priority INTEGER DEFAULT 3, -- 1=highest, 5=lowest
  notes TEXT,
  status VARCHAR(20), -- pending, assigned, denied
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE moonlighting_assignments (
  id UUID PRIMARY KEY,
  faculty_id UUID REFERENCES faculty(id),
  night_id UUID REFERENCES moonlighting_nights(id),
  assigned_by UUID REFERENCES faculty(id), -- admin who assigned
  assigned_at TIMESTAMP DEFAULT NOW(),
  method VARCHAR(20) -- auto, manual
);
```

#### Frontend Structure
```
integration/
├── index.html              # Unified login
├── dashboard.html          # Combined dashboard
├── vacation/
│   ├── weeks.html         # Week selection (Stage 1)
│   └── schedule.html      # Final vacation schedule
├── moonlighting/
│   ├── request.html       # Request shifts
│   ├── my-shifts.html     # View assignments
│   └── calendar.html      # Calendar view
├── admin/
│   ├── overview.html      # Combined admin dashboard
│   ├── vacation-admin.html
│   └── moonlighting-admin.html
└── shared/
    ├── navigation.js      # Unified nav
    └── api.js            # Supabase helpers
```

#### Algorithm Approach
```python
# Constraint Satisfaction Problem using PuLP or OR-Tools

def optimize_moonlighting_assignments(requests, nights, faculty_data):
    \"\"\"
    Objectives:
    1. Maximize coverage (staff all nights)
    2. Maximize request satisfaction
    3. Minimize max shifts per person (fairness)
    4. Respect priority preferences
    
    Constraints:
    - Hard: min_staff <= assigned <= max_staff per night
    - Hard: max_shifts_per_month per faculty
    - Soft: Respect priority levels
    - Soft: Avoid consecutive nights
    - Soft: Balance weekends vs weekdays
    \"\"\"
    
    # Decision variables: x[faculty][night] = 0 or 1
    # Objective function: weighted sum of goals
    # Return: Dict of assignments
```

### Development Phases

#### Phase 2.1: Planning (2 weeks)
- [ ] Review and compare both existing systems
- [ ] Design unified database schema
- [ ] Define moonlighting business rules
- [ ] Create wireframes for new UI

#### Phase 2.2: Database (1 week)
- [ ] Create test Supabase project
- [ ] Implement migrations
- [ ] Set up RLS policies
- [ ] Create views for dashboard

#### Phase 2.3: Frontend (3 weeks)
- [ ] Unified navigation
- [ ] Moonlighting request interface
- [ ] Admin moonlighting panel
- [ ] Update dashboard with moonlighting stats

#### Phase 2.4: Algorithm (2 weeks)
- [ ] Design optimization algorithm
- [ ] Implement in Python
- [ ] Create API endpoint
- [ ] Test with sample data

#### Phase 2.5: Testing (2 weeks)
- [ ] Unit tests for algorithm
- [ ] Integration tests
- [ ] User acceptance testing
- [ ] Performance optimization

#### Phase 2.6: Deployment (1 week)
- [ ] Documentation
- [ ] Production migration
- [ ] Training materials
- [ ] Launch

**Total Stage 2 Timeline**: ~11 weeks

---

## 📅 Stage 3: Clinical Schedule Automation (FUTURE)

### Goal
Automate the weekly inpatient clinical service schedule, considering vacation and moonlighting assignments.

### New Features
1. **Weekly Service Schedule**
   - 52-week rotation
   - Multiple service types (consult, ICU, floor)
   - Subspecialty coverage
   - Call schedules

2. **Smart Scheduling**
   - Considers vacation blocks (from Stage 1)
   - Considers moonlighting assignments (from Stage 2)
   - Fair rotation over time
   - Subspecialty distribution
   - Educational goals (fellows, residents)

3. **Conflict Detection**
   - Can't schedule if on vacation
   - Balance with moonlighting load
   - Avoid overloading any faculty
   - Maintain minimum competency requirements

4. **Multi-Week Optimization**
   - Look ahead several months
   - Optimize for fairness and coverage
   - Handle last-minute changes
   - Swap capability

### Technical Challenges
- Much more complex constraints
- Longer time horizons (52 weeks vs 30 nights)
- More service types
- Integration with academic schedules
- Fellow/resident coordination

### Algorithm Requirements
- Multi-objective optimization
- Constraint propagation
- Heuristic search (genetic algorithms?)
- Real-time re-optimization
- "What-if" scenario planning

**Estimated Timeline**: 4-6 months

---

## 🔌 Stage 4: QGenda Integration (FUTURE)

### Goal
Seamless integration with QGenda enterprise scheduling system for deployment across the health system.

### Features
1. **Bi-Directional Sync**
   - Push schedules to QGenda
   - Pull external assignments
   - Handle conflicts
   - Maintain audit trail

2. **Export Capabilities**
   - CSV export in QGenda format
   - Direct API integration
   - Scheduled automatic exports
   - Manual export on demand

3. **Import Capabilities**
   - Import external shifts
   - Import time-off requests from QGenda
   - Sync faculty data
   - Handle data conflicts

4. **Administrative Dashboard**
   - View discrepancies
   - Resolve conflicts
   - Audit trail of all changes
   - Reporting across both systems

### Technical Requirements
- QGenda API credentials
- OAuth authentication
- Webhook support for real-time updates
- Data mapping between systems
- Error handling and retry logic
- Comprehensive logging

### Integration Points
```
PCCM System          QGenda
===========          ======
Vacation     -----> Time Off
Moonlighting -----> Night Shifts
Clinical     -----> Service Assignments
Faculty      <---> Staff Data
```

**Estimated Timeline**: 3-4 months

---

## 🗺️ Overall Timeline

```
Stage 1: Complete ✅ (Already in production)
Stage 2: 11 weeks (Q1 2026)
Stage 3: 4-6 months (Q2-Q3 2026)
Stage 4: 3-4 months (Q4 2026)

Total: ~12-16 months for complete system
```

---

## 🎯 Success Metrics

### Stage 2 Success Criteria
- [ ] Faculty can request moonlighting shifts
- [ ] Algorithm produces fair assignments
- [ ] 90%+ request satisfaction rate
- [ ] < 5 seconds assignment time
- [ ] Zero ongoing costs maintained
- [ ] 95%+ user satisfaction

### Stage 3 Success Criteria
- [ ] Automated weekly schedules
- [ ] Fair distribution verified
- [ ] Handles 52-week rotation
- [ ] Integrates all three components
- [ ] Reduces admin time by 80%

### Stage 4 Success Criteria
- [ ] Seamless QGenda integration
- [ ] Real-time sync working
- [ ] Zero data discrepancies
- [ ] Enterprise-ready
- [ ] Adopted system-wide

---

## 💰 Cost Structure

### Current (Stage 1)
- **Hosting**: $0 (GitHub Pages)
- **Database**: $0 (Supabase free tier)
- **Development**: $0 (self-built)
- **Total Monthly**: $0

### Stage 2 (Projected)
- **Hosting**: $0 (same)
- **Database**: $0 (within free tier limits)
- **Algorithm Compute**: $0-10/month (occasional runs)
- **Total Monthly**: ~$0-10

### Stage 3 (Projected)
- **Hosting**: $0-25 (may need Vercel/Netlify pro)
- **Database**: $25 (may exceed free tier)
- **Compute**: $10-20 (more frequent algorithm runs)
- **Total Monthly**: ~$35-70

### Stage 4 (Projected)
- **All Stage 3 costs**: $35-70
- **QGenda API**: $0 (if included in enterprise)
- **Premium hosting**: $25 (for reliability)
- **Total Monthly**: ~$60-95

**Note**: These are conservative estimates. Focus on maintaining $0 cost through Stage 2.

---

## 🔧 Technical Stack Evolution

### Stage 1 & 2
- Frontend: Vanilla HTML/CSS/JS
- Backend: Supabase (serverless)
- Hosting: GitHub Pages
- Algorithm: Python (run on-demand)

### Stage 3 & 4 (Potential upgrades)
- Frontend: Consider React/Vue for complexity
- Backend: May need dedicated API server
- Hosting: Vercel/Netlify/AWS
- Algorithm: Containerized microservice
- CI/CD: GitHub Actions

---

## 🎓 Key Learnings & Principles

### From Stage 1
1. **Simplicity works**: Vanilla JS sufficient for Stage 1
2. **Zero cost is possible**: Free tiers cover a lot
3. **Mobile-first**: Medical professionals need mobile access
4. **User-centered**: Simple, intuitive interfaces matter
5. **Documentation**: Essential for handoff and maintenance

### For Stage 2+
1. **Algorithm != LLM**: Use proper optimization libraries
2. **Test thoroughly**: Complex logic needs comprehensive tests
3. **Plan for scale**: Design for growth from the start
4. **Iterative approach**: Build, test, refine, repeat
5. **User feedback**: Beta test with real faculty early

---

## 📞 Next Steps

### Immediate (This Week)
1. Review PROJECT_TASKS.md in detail
2. Set up GitHub Project board
3. Review both production systems
4. Start database schema design

### Short Term (This Month)
1. Complete Phase 2.1 (Planning)
2. Set up test environment
3. Create initial wireframes
4. Define all business rules

### Medium Term (Next 3 Months)
1. Complete database implementation
2. Build core UI
3. Implement algorithm
4. Begin testing

---

**Last Updated**: November 21, 2025  
**Current Stage**: 2 (In Progress)  
**Document Version**: 1.0
