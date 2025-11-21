# 🗄️ Database

Database schemas, migrations, and test data.

## Structure

```
database/
├── current-schema/         # Production schemas (reference)
│   ├── pccm-schedule.sql
│   └── moonlighter.sql
├── migrations/             # Integration migration scripts
│   ├── 001-merge-faculty-tables.sql
│   ├── 002-add-moonlighting-tables.sql
│   └── 003-create-unified-views.sql
└── test-data/              # Sample data for testing
    ├── faculty.sql
    ├── moonlighting-nights.sql
    └── moonlighting-requests.sql
```

## Migration Strategy

### Development
1. Test migrations in test Supabase project
2. Verify all data loads correctly
3. Test RLS policies
4. Check performance

### Production
1. **BACKUP FIRST** (critical!)
2. Run migrations during maintenance window
3. Verify data integrity
4. Test critical paths
5. Monitor for issues

## Running Migrations

```sql
-- In Supabase SQL Editor
-- Or via psql:
psql $DATABASE_URL < migrations/001-merge-faculty-tables.sql
```

## Test Data

```bash
# Load test data
psql $DATABASE_URL < test-data/faculty.sql
psql $DATABASE_URL < test-data/moonlighting-nights.sql
```

## Important Notes

- 🔒 Always backup before migrations
- 🧪 Test in development first
- 📝 Document schema changes
- ⚡ Check query performance
- 🔐 Verify RLS policies
