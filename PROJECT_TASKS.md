# 📋 REVISED: PCCM Integration Project Tasks

**Migration: PCCM Schedule (Supabase) → Moonlighter (Fly.io)**

**Goal**: Consolidate both systems into your existing Fly.io deployment, eliminating Supabase and RLS complexity.

---

## 🎯 Overview

**Current State**:
- Moonlighting scheduler: ✅ Working on Fly.io with SQLite
- Vacation scheduler: 📦 On GitHub Pages + Supabase

**End Goal**:
- Everything: ✅ On Fly.io with SQLite
- One database, one deployment, one login

**Timeline**: ~15 hours over 5 days

---

## Phase 1: Database Extension (Day 1 - 3 hours)

### Task 1.1: Extend Faculty Model
**Priority**: High  
**Estimate**: 30 minutes

**Description**:
Add vacation/points fields to your existing Faculty model in `backend/models.py`

**Files to Modify**:
- `backend/models.py`

**Changes**:
```python
class Faculty(Base):
    # Existing fields
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    password_hash = Column(String)
    availability_dates = Column(Text)  # Existing moonlighting
    
    # ADD these new fields
    rank = Column(String)  # assistant, associate, full
    clinical_effort_pct = Column(Integer)
    base_points = Column(Integer)
    is_admin = Column(Boolean, default=False)
    password_changed = Column(Boolean, default=False)
    registered = Column(Boolean, default=True)
    active = Column(Boolean, default=True)
```

**Acceptance Criteria**:
- [ ] Faculty model includes all vacation fields
- [ ] No breaking changes to existing moonlighting code
- [ ] Model compiles without errors

---

### Task 1.2: Create Vacation Tables
**Priority**: High  
**Estimate**: 1 hour

**Description**:
Add VacationWeek and VacationRequest models

**Files to Create/Modify**:
- `backend/models.py` (add new models)

**New Models**:
```python
class VacationWeek(Base):
    __tablename__ = "vacation_weeks"
    
    id = Column(String, primary_key=True)
    week_number = Column(Integer, nullable=False)
    label = Column(String)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    week_type = Column(String)  # regular, summer, spring_break, thanksgiving, christmas
    point_cost_off = Column(Integer)
    point_reward_work = Column(Integer)
    min_staff_required = Column(Integer, default=5)
    year = Column(Integer)

class VacationRequest(Base):
    __tablename__ = "vacation_requests"
    
    id = Column(String, primary_key=True)
    faculty_id = Column(String, ForeignKey('faculty.id'))
    week_id = Column(String, ForeignKey('vacation_weeks.id'))
    status = Column(String)  # unavailable, available, requested
    points_spent = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    faculty = relationship("Faculty")
    week = relationship("VacationWeek")
```

**Acceptance Criteria**:
- [ ] Both models defined correctly
- [ ] Foreign keys properly set
- [ ] Relationships working

---

### Task 1.3: Create Migration Script
**Priority**: High  
**Estimate**: 45 minutes

**Description**:
Script to add new columns and tables to existing SQLite database

**Files to Create**:
- `backend/migrations/add_vacation_tables.py`

**Script**:
```python
from sqlalchemy import create_engine, text
from backend.models import Base, VacationWeek, VacationRequest

def migrate():
    engine = create_engine('sqlite:////data/moonlighter.db')
    
    # Add columns to faculty table
    with engine.connect() as conn:
        try:
            conn.execute(text(\"ALTER TABLE faculty ADD COLUMN rank TEXT\"))
            conn.execute(text(\"ALTER TABLE faculty ADD COLUMN clinical_effort_pct INTEGER\"))
            conn.execute(text(\"ALTER TABLE faculty ADD COLUMN base_points INTEGER\"))
            conn.execute(text(\"ALTER TABLE faculty ADD COLUMN is_admin BOOLEAN DEFAULT 0\"))
            print(\"✅ Added columns to faculty table\")
        except Exception as e:
            print(f\"⚠️  Columns may already exist: {e}\")
    
    # Create new tables
    VacationWeek.__table__.create(engine, checkfirst=True)
    VacationRequest.__table__.create(engine, checkfirst=True)
    print(\"✅ Created vacation tables\")

if __name__ == \"__main__\":
    migrate()
```

**Acceptance Criteria**:
- [ ] Script runs without errors
- [ ] New columns added to faculty
- [ ] New tables created
- [ ] Idempotent (can run multiple times)

---

### Task 1.4: Export Data from Supabase
**Priority**: High  
**Estimate**: 30 minutes

**Description**:
Export all data from Supabase as CSV files

**Steps**:
1. Login to Supabase dashboard
2. Go to Table Editor
3. Export each table:
   - faculty → `faculty_export.csv`
   - weeks → `weeks_export.csv`
   - points_ledger → `points_export.csv`

**Acceptance Criteria**:
- [ ] All CSVs downloaded
- [ ] Data looks correct
- [ ] No missing rows

---

### Task 1.5: Create Import Script
**Priority**: High  
**Estimate**: 30 minutes

**Description**:
Script to import Supabase CSV data into SQLite

**Files to Create**:
- `scripts/import_from_supabase.py`

**Script**:
```python
import csv
from backend.database import SessionLocal
from backend.models import Faculty, VacationWeek, VacationRequest

def import_faculty():
    db = SessionLocal()
    
    with open('faculty_export.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Update existing or create new
            faculty = db.query(Faculty).filter(Faculty.id == row['faculty_id']).first()
            if not faculty:
                faculty = Faculty(id=row['faculty_id'])
                db.add(faculty)
            
            faculty.name = row['name']
            faculty.email = row['email']
            faculty.rank = row['rank']
            faculty.clinical_effort_pct = int(row['clinical_effort_pct'])
            faculty.base_points = int(row['base_points'])
            faculty.password_hash = \"PCCM2025!\"
        
        db.commit()
        print(f\"✅ Imported faculty\")

# Similar functions for weeks and requests...
```

**Acceptance Criteria**:
- [ ] Imports faculty data
- [ ] Imports week data
- [ ] Imports requests
- [ ] Handles duplicates gracefully

---

## Phase 2: Backend API (Day 2 - 4 hours)

### Task 2.1: Add Vacation API Endpoints
**Priority**: High  
**Estimate**: 2 hours

**Description**:
Add vacation-related routes to existing FastAPI app

**Files to Modify**:
- `backend/app.py`

**New Endpoints**:
```python
@app.get(\"/api/vacation/weeks\")
def get_vacation_weeks(year: int = 2026):
    # Return all weeks for year

@app.get(\"/api/vacation/my-requests\")
def get_my_requests(faculty_id: str):
    # Return faculty's requests

@app.post(\"/api/vacation/request\")
def submit_request(faculty_id: str, week_id: str, status: str):
    # Submit or update request

@app.get(\"/api/vacation/points\")
def get_points_balance(faculty_id: str):
    # Calculate current balance

@app.post(\"/api/vacation/generate-weeks\")
def generate_weeks(year: int, start_date: str):
    # Admin: Generate 52 weeks
```

**Acceptance Criteria**:
- [ ] All endpoints working
- [ ] Returns correct data
- [ ] Proper error handling
- [ ] Tests pass

---

### Task 2.2: Add Points Calculation Logic
**Priority**: High  
**Estimate**: 1 hour

**Description**:
Implement points calculation business logic

**Logic**:
```python
def calculate_base_points(clinical_effort_pct: int, rank: str) -> int:
    multipliers = {
        'assistant': 1.0,
        'associate': 1.75,
        'full': 2.5
    }
    return int(100 * (clinical_effort_pct / 100) * multipliers[rank])

def calculate_current_balance(faculty_id: str, db: Session) -> dict:
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    requests = db.query(VacationRequest).filter(
        VacationRequest.faculty_id == faculty_id
    ).all()
    
    base = faculty.base_points
    spent = sum(r.points_spent for r in requests)
    balance = base + spent
    
    return {\"base\": base, \"spent\": spent, \"balance\": balance}
```

**Acceptance Criteria**:
- [ ] Points calculation matches PCCM rules
- [ ] Handles all edge cases
- [ ] Returns correct balances

---

### Task 2.3: Test API Locally
**Priority**: High  
**Estimate**: 1 hour

**Description**:
Test all new endpoints locally

**Commands**:
```bash
# Start local server
uvicorn backend.app:app --reload

# Test endpoints
curl http://localhost:8000/api/vacation/weeks?year=2026
curl http://localhost:8000/api/vacation/points?faculty_id=001
```

**Acceptance Criteria**:
- [ ] All endpoints respond
- [ ] Data is correct
- [ ] No errors in logs

---

## Phase 3: Frontend Integration (Days 3-4 - 6 hours)

### Task 3.1: Create vacation.html
**Priority**: High  
**Estimate**: 3 hours

**Description**:
Create new vacation week selection page

**Files to Create**:
- `static/vacation.html`
- Copy style from existing moonlighting pages

**Features**:
- Grid of 52 weeks
- Status selection (unavailable/available/requested)
- Real-time points display
- Color coding by week type
- Mobile responsive

**Acceptance Criteria**:
- [ ] Page loads correctly
- [ ] Can select weeks
- [ ] Points update in real-time
- [ ] Matches existing design style

---

### Task 3.2: Update Dashboard
**Priority**: High  
**Estimate**: 2 hours

**Description**:
Add vacation stats and navigation to existing dashboard

**Files to Modify**:
- `static/dashboard.html` (or index.html)

**Changes**:
```html
<!-- Add to navigation -->
<li class=\"nav-item\">
  <a href=\"/vacation\" class=\"nav-link\">
    <span class=\"nav-icon\">🌴</span>
    <span>Vacation Weeks</span>
  </a>
</li>

<!-- Add stat card -->
<div class=\"stat-card\">
  <div class=\"stat-header\">
    <span>Available Points</span>
    <span class=\"stat-icon\">💎</span>
  </div>
  <div class=\"stat-value\" id=\"vacationPoints\">--</div>
</div>
```

**Acceptance Criteria**:
- [ ] Navigation includes vacation link
- [ ] Stats show points balance
- [ ] Design consistent

---

### Task 3.3: Update Admin Panel
**Priority**: Medium  
**Estimate**: 1 hour

**Description**:
Add vacation management to admin panel

**Files to Modify**:
- `static/Admin.html`

**New Features**:
- View all requests
- Generate weeks button
- Faculty points overview
- Export schedule

**Acceptance Criteria**:
- [ ] Admin can view all requests
- [ ] Can generate weeks
- [ ] Can see points report

---

## Phase 4: Testing & Deployment (Day 5 - 2 hours)

### Task 4.1: Local Testing
**Priority**: High  
**Estimate**: 30 minutes

**Description**:
Comprehensive local testing

**Test Scenarios**:
1. Faculty logs in
2. Views vacation weeks
3. Selects unavailable/available
4. Points update correctly
5. Requests save to database
6. Admin can view all requests

**Acceptance Criteria**:
- [ ] All scenarios pass
- [ ] No console errors
- [ ] Data persists

---

### Task 4.2: Deploy to Fly.io
**Priority**: High  
**Estimate**: 30 minutes

**Description**:
Deploy updated application

**Commands**:
```bash
# SSH into Fly.io
fly ssh console

# Run migration
python backend/migrations/add_vacation_tables.py

# Exit and deploy
exit
fly deploy

# Monitor logs
fly logs --tail
```

**Acceptance Criteria**:
- [ ] Deployment successful
- [ ] Migration ran
- [ ] App accessible
- [ ] No errors in logs

---

### Task 4.3: Import Production Data
**Priority**: High  
**Estimate**: 30 minutes

**Description**:
Import data from Supabase to Fly.io

**Steps**:
```bash
# Copy CSVs to Fly.io
fly ssh console
# Upload files via SCP or paste

# Run import
python scripts/import_from_supabase.py

# Verify
sqlite3 /data/moonlighter.db
SELECT COUNT(*) FROM vacation_weeks;
SELECT COUNT(*) FROM vacation_requests;
```

**Acceptance Criteria**:
- [ ] All data imported
- [ ] No duplicates
- [ ] Data looks correct

---

### Task 4.4: End-to-End Testing
**Priority**: High  
**Estimate**: 30 minutes

**Description**:
Test complete workflow in production

**Test Flow**:
1. Login as faculty
2. Navigate to vacation page
3. Select weeks
4. Check points
5. Navigate to moonlighting
6. Verify both systems work
7. Logout and login as admin
8. Verify admin can see everything

**Acceptance Criteria**:
- [ ] Complete workflow works
- [ ] Both systems functional
- [ ] No errors
- [ ] Performance acceptable

---

## Phase 5: Cleanup & Documentation (Optional)

### Task 5.1: Shut Down Supabase
**Priority**: Low  
**Estimate**: 15 minutes

**Description**:
Once everything is working, shut down Supabase project

**Steps**:
1. Download final backup
2. Pause project
3. Delete project (after confirmation period)

**Acceptance Criteria**:
- [ ] Backup saved
- [ ] Supabase project paused/deleted
- [ ] No ongoing costs

---

### Task 5.2: Update Documentation
**Priority**: Low  
**Estimate**: 30 minutes

**Description**:
Update README and docs to reflect new architecture

**Files to Update**:
- README.md
- DEPLOYMENT.md
- User guide

**Acceptance Criteria**:
- [ ] Documentation accurate
- [ ] Architecture diagram updated
- [ ] Deployment steps correct

---

## 📊 Summary

**Total Tasks**: 20  
**Total Time**: ~15 hours  
**Timeline**: 5 days  
**Result**: Single Fly.io deployment with everything

---

## 🎯 Critical Path

Must complete in order:
1. Task 1.2 (Vacation Tables)
2. Task 1.3 (Migration Script)
3. Task 2.1 (API Endpoints)
4. Task 3.1 (vacation.html)
5. Task 4.2 (Deploy)

---

## 🏷️ Labels

- `phase-1` - Database (blue)
- `phase-2` - Backend API (green)
- `phase-3` - Frontend (purple)
- `phase-4` - Deployment (orange)
- `priority-high` - Critical (red)
- `priority-medium` - Important (yellow)
- `priority-low` - Nice to have (gray)

---

**Start Here**: Task 1.1 - Extend Faculty Model  
**End Goal**: Everything on Fly.io, Supabase gone!

**Last Updated**: November 21, 2025  
**Status**: Ready to start 🚀
