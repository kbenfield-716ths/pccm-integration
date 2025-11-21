# 🚀 REVISED: PCCM Integration Plan - Fly.io Consolidation

**Goal**: Migrate the PCCM vacation scheduling system INTO your existing Fly.io moonlighting deployment, eliminating Supabase entirely.

---

## 🎯 Why This Approach is Better

### Current Pain Points (Supabase)
- ❌ **RLS Complexity**: Row Level Security is frustrating and overcomplicated
- ❌ **Split Architecture**: GitHub Pages + Supabase = two systems to manage
- ❌ **Auth Friction**: user_id sync, password resets, registration flow issues
- ❌ **Limited Control**: Can't easily migrate or self-host
- ❌ **Debugging Hell**: RLS policies hide real issues

### Fly.io Benefits
- ✅ **Single Deployment**: One Docker container, one command to deploy
- ✅ **Simple SQLite**: No RLS, straightforward SQL, you own the file
- ✅ **Full Control**: Easy to backup, migrate, or move to UVA hosting
- ✅ **Already Working**: You have moonlighting running successfully
- ✅ **Cost**: ~$3/month vs managing two free tiers
- ✅ **Future Proof**: Easy to move to UVA infrastructure

### Security Reality
- These are **internal trusted faculty** members
- You're managing **preferences**, not PHI/PII
- Simple password auth is **sufficient**
- Most breaches come from complexity, not simplicity

---

## 📊 Current State

### What You Have on Fly.io (moonlighter-web)
- ✅ FastAPI backend
- ✅ SQLite database with persistence
- ✅ Python optimization algorithm (PuLP)
- ✅ PWA with service workers and caching
- ✅ Beautiful UI
- ✅ Faculty authentication
- ✅ Admin panel
- ✅ Working deployment

### What You Have on Supabase (PCCMSchedule)
- 📦 Vacation week selection (Available/Unavailable/Requested)
- 📦 Points system (base points, costs, volunteer bonuses)
- 📦 Draft priority system
- 📦 Faculty profiles
- 📦 Admin panel
- 📦 Modern UI design

---

## 🏗️ New Architecture

```
┌─────────────────────────────────────────┐
│   Fly.io Container (~$3/month)          │
│                                         │
│   ├── FastAPI Backend (Python)         │
│   │   ├── /api/moonlight/*             │
│   │   ├── /api/vacation/*  ← NEW       │
│   │   ├── /api/faculty/*               │
│   │   └── /api/admin/*                 │
│   │                                     │
│   ├── SQLite Database (persistent)     │
│   │   ├── faculty (unified)            │
│   │   ├── moonlight_signups            │
│   │   ├── moonlight_assignments        │
│   │   ├── vacation_weeks    ← NEW      │
│   │   ├── vacation_requests ← NEW      │
│   │   └── points_ledger     ← NEW      │
│   │                                     │
│   ├── Static Files (served by FastAPI) │
│   │   ├── index.html (login)           │
│   │   ├── dashboard.html               │
│   │   ├── moonlighting.html            │
│   │   ├── vacation.html     ← NEW      │
│   │   └── admin.html                   │
│   │                                     │
│   └── Algorithms                        │
│       ├── moonlight_optimizer.py       │
│       └── vacation_optimizer.py ← NEW  │
└─────────────────────────────────────────┘
```

---

## 📋 Migration Plan

### Phase 1: Extend Moonlighter Database (Day 1: 3 hours)

**Task 1.1**: Add Vacation Tables to SQLite

```python
# backend/models.py (extend existing file)

class Faculty(Base):
    \"\"\"Extended to include vacation/points data\"\"\"
    __tablename__ = "faculty"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    password_hash = Column(String)
    
    # Existing moonlighting fields
    availability_dates = Column(Text)  # JSON array
    
    # NEW: Vacation/points fields
    rank = Column(String)  # assistant, associate, full
    clinical_effort_pct = Column(Integer)
    base_points = Column(Integer)
    is_admin = Column(Boolean, default=False)
    password_changed = Column(Boolean, default=False)
    registered = Column(Boolean, default=True)
    active = Column(Boolean, default=True)

class VacationWeek(Base):
    \"\"\"52 weeks for vacation scheduling\"\"\"
    __tablename__ = "vacation_weeks"
    
    id = Column(String, primary_key=True)
    week_number = Column(Integer, nullable=False)
    label = Column(String)  # "Week 1 (Jul 7)"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    week_type = Column(String)  # regular, summer, spring_break, thanksgiving, christmas
    point_cost_off = Column(Integer)  # Cost to take week off
    point_reward_work = Column(Integer)  # Bonus for volunteering
    min_staff_required = Column(Integer, default=5)
    year = Column(Integer)

class VacationRequest(Base):
    \"\"\"Faculty requests for weeks off/available\"\"\"
    __tablename__ = "vacation_requests"
    
    id = Column(String, primary_key=True)
    faculty_id = Column(String, ForeignKey('faculty.id'))
    week_id = Column(String, ForeignKey('vacation_weeks.id'))
    status = Column(String)  # unavailable, available, requested
    points_spent = Column(Integer)  # Negative for off, positive for volunteer
    created_at = Column(DateTime, default=datetime.utcnow)
    
    faculty = relationship("Faculty")
    week = relationship("VacationWeek")
```

**Task 1.2**: Create Migration Script

```python
# backend/migrations/add_vacation_tables.py

from sqlalchemy import create_engine
from backend.models import Base, Faculty, VacationWeek, VacationRequest

def migrate():
    engine = create_engine('sqlite:////data/moonlighter.db')
    
    # Add new columns to faculty table
    with engine.connect() as conn:
        conn.execute(text(\"\"\"
            ALTER TABLE faculty ADD COLUMN rank TEXT;
            ALTER TABLE faculty ADD COLUMN clinical_effort_pct INTEGER;
            ALTER TABLE faculty ADD COLUMN base_points INTEGER;
            ALTER TABLE faculty ADD COLUMN is_admin BOOLEAN DEFAULT 0;
        \"\"\"))
    
    # Create new tables
    VacationWeek.__table__.create(engine, checkfirst=True)
    VacationRequest.__table__.create(engine, checkfirst=True)
    
    print("✅ Migration complete!")

if __name__ == "__main__":
    migrate()
```

**Task 1.3**: Import Existing Faculty Data

```python
# scripts/import_from_supabase.py

import csv
from backend.database import SessionLocal
from backend.models import Faculty

def import_faculty():
    \"\"\"Import faculty from Supabase CSV export\"\"\"
    db = SessionLocal()
    
    with open('faculty_export.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            faculty = Faculty(
                id=row['faculty_id'],
                name=row['name'],
                email=row['email'],
                rank=row['rank'],
                clinical_effort_pct=int(row['clinical_effort_pct']),
                base_points=int(row['base_points']),
                is_admin=row.get('is_admin', 'false').lower() == 'true',
                password_hash="PCCM2025!"  # Default password
            )
            db.add(faculty)
        
        db.commit()
        print(f"✅ Imported {reader.line_num} faculty members")

if __name__ == "__main__":
    import_faculty()
```

---

### Phase 2: Add Vacation API Endpoints (Day 2: 4 hours)

**Task 2.1**: Add Vacation Routes to FastAPI

```python
# backend/app.py (extend existing file)

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Faculty, VacationWeek, VacationRequest
from typing import List

# ... existing moonlighting routes ...

# NEW: Vacation Routes

@app.get("/api/vacation/weeks")
def get_vacation_weeks(year: int = 2026, db: Session = Depends(get_db)):
    \"\"\"Get all vacation weeks for a year\"\"\"
    weeks = db.query(VacationWeek).filter(VacationWeek.year == year).all()
    return weeks

@app.get("/api/vacation/my-requests")
def get_my_requests(faculty_id: str, db: Session = Depends(get_db)):
    \"\"\"Get faculty's vacation requests\"\"\"
    requests = db.query(VacationRequest).filter(
        VacationRequest.faculty_id == faculty_id
    ).all()
    return requests

@app.post("/api/vacation/request")
def submit_request(
    faculty_id: str,
    week_id: str, 
    status: str,  # unavailable, available, requested
    db: Session = Depends(get_db)
):
    \"\"\"Submit or update vacation request\"\"\"
    
    # Check if request exists
    request = db.query(VacationRequest).filter(
        VacationRequest.faculty_id == faculty_id,
        VacationRequest.week_id == week_id
    ).first()
    
    week = db.query(VacationWeek).filter(VacationWeek.id == week_id).first()
    
    # Calculate points
    if status == "unavailable":
        points = -week.point_cost_off
    elif status == "available":
        points = week.point_reward_work
    else:  # requested
        points = -week.point_cost_off
    
    if request:
        request.status = status
        request.points_spent = points
    else:
        request = VacationRequest(
            faculty_id=faculty_id,
            week_id=week_id,
            status=status,
            points_spent=points
        )
        db.add(request)
    
    db.commit()
    return {"success": True, "points": points}

@app.get("/api/vacation/points")
def get_points_balance(faculty_id: str, db: Session = Depends(get_db)):
    \"\"\"Calculate current points balance\"\"\"
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    requests = db.query(VacationRequest).filter(
        VacationRequest.faculty_id == faculty_id
    ).all()
    
    spent = sum(r.points_spent for r in requests)
    balance = faculty.base_points + spent
    
    return {
        "base_points": faculty.base_points,
        "spent": spent,
        "balance": balance
    }

@app.post("/api/vacation/generate-weeks")
def generate_weeks(year: int, start_date: str, db: Session = Depends(get_db)):
    \"\"\"Admin: Generate 52 weeks for scheduling year\"\"\"
    from datetime import datetime, timedelta
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    weeks = []
    
    for i in range(52):
        week_start = start + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)
        
        # Determine week type and costs
        week_type = "regular"
        cost_off = 5
        reward_work = 0
        
        # Add logic for summer, holidays, etc.
        month = week_start.month
        if month in [6, 7, 8]:
            week_type = "summer"
            cost_off = 7
            reward_work = 5
        
        week = VacationWeek(
            week_number=i + 1,
            label=f"Week {i+1} ({week_start.strftime('%b %d')})",
            start_date=week_start.date(),
            end_date=week_end.date(),
            week_type=week_type,
            point_cost_off=cost_off,
            point_reward_work=reward_work,
            year=year
        )
        weeks.append(week)
        db.add(week)
    
    db.commit()
    return {"success": True, "weeks_created": 52}
```

---

### Phase 3: Update Frontend (Day 3-4: 6 hours)

**Task 3.1**: Add Vacation Section to Dashboard

```html
<!-- Update existing dashboard.html -->

<!-- Add to navigation -->
<li class="nav-item">
  <a href="/vacation" class="nav-link">
    <span class="nav-icon">🌴</span>
    <span>Vacation Weeks</span>
  </a>
</li>

<!-- Add to dashboard stats -->
<div class="stat-card">
  <div class="stat-header">
    <span class="stat-label">Available Points</span>
    <span class="stat-icon">💎</span>
  </div>
  <div class="stat-value" id="vacationPoints">--</div>
  <div class="stat-subtitle">Current balance</div>
</div>
```

**Task 3.2**: Create vacation.html

```html
<!-- vacation.html - similar to existing signup.html style -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Vacation Weeks - PCCM Scheduler</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <div class="container">
    <h1>Select Your Weeks</h1>
    
    <div class="points-display">
      <strong>Available Points:</strong> <span id="points-balance">--</span>
    </div>
    
    <div id="weeks-grid" class="weeks-grid">
      <!-- Populated by JavaScript -->
    </div>
  </div>
  
  <script>
    async function loadWeeks() {
      const response = await fetch('/api/vacation/weeks?year=2026');
      const weeks = await response.json();
      
      const grid = document.getElementById('weeks-grid');
      weeks.forEach(week => {
        const card = createWeekCard(week);
        grid.appendChild(card);
      });
    }
    
    function createWeekCard(week) {
      const card = document.createElement('div');
      card.className = 'week-card';
      card.innerHTML = `
        <div class="week-label">${week.label}</div>
        <div class="week-type">${week.week_type}</div>
        <div class="week-cost">Cost: ${week.point_cost_off} pts</div>
        <select onchange="updateRequest('${week.id}', this.value)">
          <option value="">No Selection</option>
          <option value="unavailable">Unavailable (-${week.point_cost_off})</option>
          <option value="available">Available (+${week.point_reward_work})</option>
          <option value="requested">Requested (-${week.point_cost_off})</option>
        </select>
      `;
      return card;
    }
    
    async function updateRequest(weekId, status) {
      const facultyId = localStorage.getItem('faculty_id');
      await fetch('/api/vacation/request', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({faculty_id: facultyId, week_id: weekId, status})
      });
      updatePointsDisplay();
    }
    
    async function updatePointsDisplay() {
      const facultyId = localStorage.getItem('faculty_id');
      const response = await fetch(`/api/vacation/points?faculty_id=${facultyId}`);
      const data = await response.json();
      document.getElementById('points-balance').textContent = data.balance;
    }
    
    loadWeeks();
    updatePointsDisplay();
  </script>
</body>
</html>
```

---

### Phase 4: Deployment (Day 5: 2 hours)

**Task 4.1**: Update Dockerfile (if needed)

```dockerfile
# Your existing Dockerfile should work
# Just ensure requirements.txt includes any new dependencies
```

**Task 4.2**: Deploy to Fly.io

```bash
# Run migration
fly ssh console
python backend/migrations/add_vacation_tables.py
exit

# Deploy updated app
fly deploy

# Test
curl https://your-app.fly.dev/api/vacation/weeks?year=2026
```

**Task 4.3**: Import Data

```bash
# Export from Supabase (via dashboard)
# Download: faculty, weeks, requests as CSV

# Upload to Fly.io
fly ssh console
# Upload files, run import script
python scripts/import_from_supabase.py
```

---

## ✅ Final Result

### What You'll Have
- ✅ **Single Deployment**: Everything on Fly.io
- ✅ **Unified Database**: SQLite with all data
- ✅ **No Supabase**: Completely eliminated
- ✅ **No RLS Headaches**: Simple SQL queries
- ✅ **Easy to Migrate**: To UVA or anywhere
- ✅ **One Login**: Shared authentication
- ✅ **Combined Dashboard**: Moonlighting + Vacation
- ✅ **Cost**: ~$3/month total

### User Experience
1. Login once
2. See combined dashboard
3. Navigate between Moonlighting and Vacation
4. All data in one place
5. Fast, simple, reliable

---

## 🎯 Timeline

- **Day 1**: Database extension (3 hours)
- **Day 2**: API endpoints (4 hours)
- **Day 3-4**: Frontend integration (6 hours)
- **Day 5**: Deployment & testing (2 hours)

**Total**: ~15 hours over 5 days

---

## 📝 Migration Checklist

- [ ] Backup Supabase data (CSV exports)
- [ ] Extend SQLite schema
- [ ] Run migration script
- [ ] Import faculty data
- [ ] Add vacation API routes
- [ ] Create vacation.html
- [ ] Update dashboard navigation
- [ ] Test locally
- [ ] Deploy to Fly.io
- [ ] Import week data
- [ ] Test end-to-end
- [ ] Shut down Supabase (save money!)

---

**Ready to start? Which phase would you like me to help you with first?** 🚀
