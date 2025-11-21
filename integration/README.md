# 🚧 Integration Workspace

This is where you build and test the integrated system.

## Structure

```
integration/
├── index.html              # Combined login page
├── dashboard.html          # Unified dashboard
├── vacation/               # Vacation scheduling module
│   ├── weeks.html
│   └── schedule.html
├── moonlighting/           # Moonlighting module
│   ├── request.html
│   ├── my-shifts.html
│   └── calendar.html
├── admin/                  # Admin interfaces
│   ├── overview.html
│   ├── vacation-admin.html
│   └── moonlighting-admin.html
└── shared/                 # Shared components
    ├── navigation.js
    ├── api.js
    └── styles.css
```

## Getting Started

1. Copy files from `production/` as starting points
2. Modify and enhance for integration
3. Test locally using `scripts/local-test-server.py`
4. Commit changes frequently
5. When ready, deploy to production repos

## Important Notes

- ⚠️ This is the **development workspace** only
- ✅ All changes should be tested here first
- 🚫 Never edit production repos directly
- 📝 Document all significant changes
- 🧪 Test on multiple devices/browsers

## Testing

```bash
# From repository root
python3 scripts/local-test-server.py

# Then open:
http://localhost:8000
```
