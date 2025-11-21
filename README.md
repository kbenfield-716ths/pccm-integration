# PCCM Integration Workspace

🚀 **Migrate PCCM Vacation Scheduler INTO your existing Fly.io Moonlighting deployment**

---

## 📋 What's Happening

**Current State**:
- ✅ **Moonlighting**: Working on Fly.io (FastAPI + SQLite)
- 📦 **Vacation Scheduling**: On GitHub Pages + Supabase

**Goal**:
- ✅ **Everything on Fly.io** (one deployment)
- ✅ **Single SQLite database** (no more Supabase!)
- ✅ **No RLS headaches** (simple SQL)
- ✅ **Unified login** (one authentication system)

---

## 🎯 Why This Approach

### Eliminate Supabase Because:
- ❌ RLS is frustrating and overcomplicated
- ❌ Split architecture (2 systems to manage)
- ❌ Auth friction (user_id sync, password resets)
- ❌ Can't easily migrate to UVA hosting

### Use Fly.io Because:
- ✅ You already have it working!
- ✅ Simple SQLite (you own the data)
- ✅ Single deployment (~$3/month)
- ✅ Easy to move to UVA later
- ✅ No RLS complexity

---

## 🏗️ Architecture

```
Fly.io Container (~$3/month)
├── FastAPI Backend
│   ├── Moonlighting API (existing)
│   └── Vacation API (new)
├── SQLite Database
│   ├── faculty (extended)
│   ├── moonlight_* tables (existing)
│   └── vacation_* tables (new)
└── Static Files
    ├── Moonlighting pages (existing)
    └── Vacation pages (new)
```

---

## 📚 Key Documents

- **[PROJECT_TASKS.md](./PROJECT_TASKS.md)** - 20 tasks, ~15 hours total
- **[INTEGRATION_PLAN.md](./INTEGRATION_PLAN.md)** - Complete technical plan
- **[QUICK_START.md](./QUICK_START.md)** - Get started immediately

---

## 🚀 Quick Start

### 1. Clone This Repo
```bash
git clone https://github.com/kbenfield-716ths/pccm-integration.git
cd pccm-integration
```

### 2. Read the Plan
```bash
cat QUICK_START.md
cat INTEGRATION_PLAN.md
```

### 3. Start First Task
**Task 1.1: Extend Faculty Model**
- Add vacation fields to existing Faculty model
- ~30 minutes
- No breaking changes

---

## 📊 Timeline

- **Day 1**: Database extension (3 hours)
- **Day 2**: API endpoints (4 hours)
- **Days 3-4**: Frontend (6 hours)
- **Day 5**: Deployment (2 hours)

**Total**: ~15 hours over 5 days

---

## 📁 Repository Structure

```
pccm-integration/
├── README.md                  # This file
├── QUICK_START.md             # Get started guide
├── PROJECT_TASKS.md           # 20 detailed tasks
├── INTEGRATION_PLAN.md        # Technical architecture
│
├── integration/               # Your workspace
│   ├── backend/              # Python FastAPI code
│   └── frontend/             # HTML/CSS/JS
│
├── production/               # Reference copies
│   ├── moonlighter/         # Current Fly.io system
│   └── pccm-schedule/       # Current Supabase system
│
└── scripts/                  # Migration utilities
    ├── export_from_supabase.py
    └── import_to_sqlite.py
```

---

## ✅ Final Result

After migration, you'll have:

- ✅ **Single login** for both systems
- ✅ **Unified dashboard** showing moonlighting + vacation
- ✅ **One database** (SQLite on Fly.io)
- ✅ **No Supabase** (eliminated!)
- ✅ **Easy to migrate** to UVA hosting
- ✅ **Cost**: ~$3/month total

---

## 🔗 Your Repositories

- **This Integration Repo**: [pccm-integration](https://github.com/kbenfield-716ths/pccm-integration)
- **Moonlighter (Fly.io)**: [moonlighter-web](https://github.com/kbenfield-716ths/moonlighter-web)
- **PCCM Schedule (Supabase)**: [PCCMSchedule](https://github.com/kbenfield-716ths/PCCMSchedule)

---

## 📞 Getting Help

- **Tasks**: See [PROJECT_TASKS.md](./PROJECT_TASKS.md)
- **Architecture**: See [INTEGRATION_PLAN.md](./INTEGRATION_PLAN.md)
- **Start Here**: See [QUICK_START.md](./QUICK_START.md)

---

**Ready to consolidate everything? Start with QUICK_START.md! 🚀**

---

**Last Updated**: November 21, 2025  
**Status**: Ready for Development  
**Timeline**: ~15 hours over 5 days
