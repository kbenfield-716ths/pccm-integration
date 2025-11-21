# 🧪 Testing Guide

## Local Testing Setup

### Prerequisites
- Python 3.7+ installed
- Git installed
- Web browser (Chrome/Firefox recommended)
- Code editor (VS Code recommended)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/kbenfield-716ths/pccm-integration.git
   cd pccm-integration
   ```

2. **Start local server**
   ```bash
   python3 scripts/local-test-server.py
   ```

3. **Open in browser**
   ```
   http://localhost:8000
   ```

4. **Test your changes**
   - Make changes to files in `integration/` folder
   - Refresh browser to see changes
   - Check browser console for errors (F12)

---

## Testing Checklist

### Before Every Commit
- [ ] Code runs without JavaScript errors
- [ ] All links work
- [ ] Mobile view looks correct
- [ ] Forms submit successfully
- [ ] Database queries work
- [ ] No console errors

### Before Deploying to Production
- [ ] All features tested
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Mobile testing (phone and tablet)
- [ ] All edge cases covered
- [ ] Performance acceptable
- [ ] Backup created
- [ ] Rollback plan ready

---

## Test Scenarios

### Scenario 1: Faculty Request Moonlighting Shift
**Steps:**
1. Login as faculty
2. Navigate to "Moonlighting Requests"
3. Select an available night
4. Submit request
5. Verify request appears in "My Requests"

**Expected:**
- Request submitted successfully
- Confirmation message shown
- Request visible in list
- Database updated

---

### Scenario 2: Admin Runs Auto-Assignment
**Steps:**
1. Login as admin
2. Navigate to "Admin > Moonlighting"
3. Review all requests
4. Click "Run Auto-Assignment"
5. Review proposed assignments
6. Accept or modify

**Expected:**
- Algorithm completes successfully
- Fair distribution achieved
- All constraints respected
- Assignments can be modified
- Faculty notified

---

### Scenario 3: Conflict Resolution
**Steps:**
1. Multiple faculty request same night
2. Admin runs algorithm
3. System chooses based on fairness
4. Other requests marked as unassigned

**Expected:**
- Fair selection made
- Clear communication to all faculty
- Unassigned faculty can request other nights

---

## Browser Console Testing

### Check for Errors
1. Open browser console (F12)
2. Click "Console" tab
3. Look for red errors
4. Fix any errors before committing

### Common Issues
- **CORS errors**: Check Supabase configuration
- **401 Unauthorized**: Check authentication
- **404 Not Found**: Check file paths
- **Syntax errors**: Check JavaScript code

---

## Database Testing

### Test Queries in Supabase
1. Open Supabase dashboard
2. Go to SQL Editor
3. Test your queries
4. Verify results

### Test RLS Policies
```sql
-- Test as specific user
SET request.jwt.claims.sub = 'user-id-here';

-- Try to access data
SELECT * FROM moonlighting_requests;

-- Should only see own data (non-admin)
```

---

## Performance Testing

### Page Load Time
- Target: < 2 seconds
- Tool: Browser DevTools > Network tab

### Database Query Time
- Target: < 100ms for dashboard queries
- Tool: Supabase dashboard > Database > Performance

### Algorithm Execution Time
- Target: < 5 seconds for full month
- Tool: Console timing or backend logs

---

## Mobile Testing

### Responsive Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Test On
- [ ] iPhone (Safari)
- [ ] Android (Chrome)
- [ ] iPad (Safari)

### Check
- [ ] Navigation menu works
- [ ] Forms are usable
- [ ] Text is readable
- [ ] Buttons are tap-friendly
- [ ] No horizontal scrolling

---

## Integration Testing

### Test Complete Workflows

**Workflow 1: New Faculty Onboarding**
1. Admin adds faculty to database
2. Faculty receives invite
3. Faculty sets password
4. Faculty accesses dashboard
5. Faculty can submit requests

**Workflow 2: Monthly Scheduling Cycle**
1. Admin opens request window
2. Faculty submit requests
3. Request window closes
4. Admin reviews requests
5. Admin runs algorithm
6. Assignments finalized
7. Faculty see assignments
8. Export to QGenda (future)

---

## Automated Testing (Future)

### Unit Tests
```python
# Example test structure
def test_algorithm_fairness():
    requests = load_test_requests()
    assignments = run_algorithm(requests)
    assert distribution_is_fair(assignments)
```

### Integration Tests
```javascript
// Example test structure
describe('Moonlighting Request Flow', () => {
  it('should allow faculty to submit request', async () => {
    // Test implementation
  });
});
```

---

## Bug Reporting

When you find a bug:

1. **Document it**
   - What were you doing?
   - What happened?
   - What should have happened?
   - Screenshot if relevant

2. **Check console**
   - Any JavaScript errors?
   - Any failed network requests?

3. **Create GitHub Issue**
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment (browser, device)

---

## Test Data

Use the provided test data scripts:

```bash
# Load test faculty
psql $DATABASE_URL < database/test-data/faculty.sql

# Load test moonlighting nights
psql $DATABASE_URL < database/test-data/moonlighting-nights.sql

# Load test requests
psql $DATABASE_URL < database/test-data/moonlighting-requests.sql
```

---

## Troubleshooting

### Issue: Pages won't load
**Solution**: Check that local server is running on correct port

### Issue: Database connection fails
**Solution**: Verify Supabase credentials in code

### Issue: Changes not showing
**Solution**: Hard refresh browser (Ctrl+Shift+R)

### Issue: Algorithm takes too long
**Solution**: Reduce test data size or optimize constraints

---

**Remember**: Test early, test often, test thoroughly! 🚀