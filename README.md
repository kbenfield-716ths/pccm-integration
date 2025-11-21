# PCCM Integration Workspace

🚀 **Integration repository for combining PCCM Schedule and Moonlighter systems**

This repository provides a safe workspace for integrating the vacation/time-off scheduling system with the moonlighting shift scheduler.

## 📋 Repository Purpose

This integration workspace allows you to:
- ✅ Safely combine features from both systems
- ✅ Test integration changes without affecting production
- ✅ Track all modifications with version control
- ✅ Maintain clear separation between production and development
- ✅ Collaborate effectively with detailed task tracking

## 🏗️ Repository Structure

```
pccm-integration/
├── README.md                          # This file
├── PROJECT_TASKS.md                   # Complete checklist for GitHub Projects
├── INTEGRATION_PLAN.md                # Full 4-stage integration roadmap
├── TESTING_GUIDE.md                   # How to test locally
│
├── docs/                              # All documentation
│   ├── STAGE_1_CURRENT_STATE.md
│   ├── STAGE_2_MOONLIGHTING.md
│   ├── STAGE_3_CLINICAL_SCHEDULE.md
│   ├── STAGE_4_QGENDA.md
│   ├── HOW_POINTS_ARE_CALCULATED.md
│   └── DEPLOYMENT_GUIDE.md
│
├── production/                        # Current working systems
│   ├── pccm-schedule/                # Production vacation scheduler
│   └── moonlighter/                  # Production moonlighting scheduler
│
├── integration/                       # Work-in-progress integration
│   ├── index.html                    # Combined login
│   ├── dashboard.html                # Unified dashboard
│   ├── vacation/                     # Vacation scheduling module
│   ├── moonlighting/                 # Moonlighting module
│   └── shared/                       # Shared components
│
├── database/
│   ├── current-schema/               # Production schemas
│   ├── migrations/                   # Integration migrations
│   └── test-data/                    # Sample data for testing
│
├── scripts/
│   ├── local-test-server.py          # Simple HTTP server for testing
│   ├── deploy-to-production.sh       # Deployment script
│   └── backup-production.sh          # Backup script
│
└── tests/
    ├── integration-tests.md          # Test scenarios
    └── user-acceptance-tests.md      # UAT checklist
```

## 🎯 Current Status: Stage 2 Planning

**Stage 1 (COMPLETE)**: Time-off scheduler with economic points ✅
**Stage 2 (IN PROGRESS)**: Moonlighting integration 🚧
**Stage 3 (PLANNED)**: Clinical schedule automation 📅
**Stage 4 (PLANNED)**: QGenda integration 🔌

## 🚀 Quick Start

### For Integration Work

1. **Clone the repository**
   ```bash
   git clone https://github.com/kbenfield-716ths/pccm-integration.git
   cd pccm-integration
   ```

2. **Review the task list**
   ```bash
   cat PROJECT_TASKS.md
   ```

3. **Start working in the integration folder**
   ```bash
   cd integration/
   # Make your changes here
   ```

4. **Test locally**
   ```bash
   python3 scripts/local-test-server.py
   # Open http://localhost:8000 in browser
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```

### For Creating GitHub Project

1. Go to your repository → **Projects** tab
2. Click **New Project**
3. Choose **Board** view
4. Use **PROJECT_TASKS.md** to create your task cards
5. Organize by Stage/Phase

## 📚 Key Documents

- **[PROJECT_TASKS.md](./PROJECT_TASKS.md)** - Complete task checklist (use this for GitHub Projects)
- **[INTEGRATION_PLAN.md](./INTEGRATION_PLAN.md)** - Full 4-stage roadmap
- **[TESTING_GUIDE.md](./TESTING_GUIDE.md)** - How to test your changes

## 🔗 Related Repositories

- **Production Vacation Scheduler**: [PCCMSchedule](https://github.com/kbenfield-716ths/PCCMSchedule)
- **Production Moonlighter**: [moonlighter-web](https://github.com/kbenfield-716ths/moonlighter-web)

## ⚠️ Important Notes

1. **Never edit production repos directly** - Always work in this integration repo first
2. **Test thoroughly** - Use the testing guide before deploying
3. **Keep production separate** - The `production/` folder is read-only reference
4. **Document everything** - Update docs as you make changes
5. **Commit frequently** - Small, focused commits are easier to track

## 🛠️ Workflow

```
1. Read PROJECT_TASKS.md
   ↓
2. Pick a task
   ↓
3. Work in integration/ folder
   ↓
4. Test locally
   ↓
5. Commit to this repo
   ↓
6. When ready: Deploy to production repos
```

## 📞 Questions?

Refer to the detailed documentation in the `docs/` folder, or check the task notes in `PROJECT_TASKS.md`.

---

**Last Updated**: November 21, 2025  
**Current Phase**: Stage 2 Development  
**Status**: Active Development 🚧
