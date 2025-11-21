# 📦 Production Systems (Reference Only)

**⚠️ READ ONLY - Do not edit files here!**

This directory contains reference copies of the current production systems.

## Current Production Repositories

### PCCM Schedule (Vacation System)
**Repository**: [kbenfield-716ths/PCCMSchedule](https://github.com/kbenfield-716ths/PCCMSchedule)  
**URL**: https://kbenfield-716ths.github.io/PCCMSchedule/  
**Status**: ✅ Production

**Key Files**:
- index.html - Login page
- dashboard.html - Main dashboard
- weeks.html - Week selection
- admin.html - Admin panel

### Moonlighter (Shift Scheduling)
**Repository**: [kbenfield-716ths/moonlighter-web](https://github.com/kbenfield-716ths/moonlighter-web)  
**URL**: https://kbenfield-716ths.github.io/moonlighter-web/  
**Status**: ✅ Production

**Key Files**:
- index.html - Login/dashboard
- signup.html - Shift signup
- Admin.html - Admin interface
- backend/ - Python optimization

## Purpose

These files serve as:
1. 📚 Reference for current features
2. 🔍 Comparison during integration
3. 💾 Backup of working code
4. 📖 Documentation of existing behavior

## Usage

```bash
# Copy a file to integration workspace
cp production/pccm-schedule/dashboard.html integration/dashboard.html

# Then modify the copy in integration/
```

## Important Reminders

- 🚫 **Never edit files in production/ folder**
- ✅ Always copy to `integration/` first
- 🔄 Keep this folder in sync with production repos
- 📝 Document any significant differences

## Updating Reference Files

Periodically refresh from production:

```bash
# Pull latest from production repos
cd production/pccm-schedule
git pull origin main

cd ../moonlighter
git pull origin main
```
