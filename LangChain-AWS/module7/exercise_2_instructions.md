# Exercise 2: Compliance Dashboard

## Objective
Create a comprehensive governance and compliance monitoring system with real-time dashboards, automated reporting, and regulatory framework support.

## Time Estimate
15 minutes

## Prerequisites
- Completed Exercise 1
- Basic understanding of compliance frameworks
- Web browser for dashboard access

## Step-by-Step Instructions

### Step 1: Understand the Dashboard Architecture
1. **Review dashboard components**:
   - Real-time compliance metrics monitoring
   - Risk assessment and categorization
   - Audit event tracking and analysis
   - Regulatory framework reporting (GDPR, HIPAA, SOX)
   - Interactive data visualizations
   - Automated alert generation

2. **Examine the data model**:
   - **ComplianceMetric**: Individual compliance measurements
   - **ComplianceStatus**: Compliant, Warning, Non-Compliant
   - **RiskLevel**: Low, Medium, High, Critical
   - **Events**: Audit trail of compliance-related activities

### Step 2: Run the Dashboard Demo
```bash
cd module7
python exercise_2_compliance_dashboard.py
```

**Expected Output**:
- Dashboard components overview
- Sample metrics with status indicators
- Available API endpoints
- Usage instructions

### Step 3: Start the Compliance Dashboard
```bash
python exercise_2_compliance_dashboard.py run
```

The dashboard will start on `http://localhost:8001` with:
- Interactive web interface
- Real-time data updates
- SQLite database for persistence
- RESTful API endpoints

### Step 4: Explore the Web Dashboard
1. **Open the dashboard** in your browser:
   ```
   http://localhost:8001
   ```

2. **Review the main sections**:
   - **Summary Cards**: Overall compliance score, warnings, violations
   - **Compliance Overview Chart**: Doughnut chart showing metric distribution
   - **Risk Distribution Chart**: Bar chart showing risk levels
   - **Recent Events Table**: Latest compliance events with risk indicators

3. **Test auto-refresh**: The dashboard updates every 30 seconds automatically

### Step 5: Test API Endpoints
1. **Get compliance summary**:
   ```bash
   curl http://localhost:8001/api/summary
   ```

2. **Get all metrics**:
   ```bash
   curl http://localhost:8001/api/metrics
   ```

3. **Get recent events**:
   ```bash
   curl http://localhost:8001/api/events?limit=10
   ```

4. **Get active alerts**:
   ```bash
   curl http://localhost:8001/api/alerts
   ```

5. **Generate framework-specific reports**:
   ```bash
   # GDPR report
   curl http://localhost:8001/api/report/gdpr
   
   # HIPAA report
   curl http://localhost:8001/api/report/hipaa
   
   # SOX report
   curl http://localhost:8001/api/report/sox
   ```

### Step 6: Analyze Compliance Metrics
1. **Review sample metrics**:
   - **GDPR Consent Rate**: 94.5% (Warning - below 95% target)
   - **Data Retention Compliance**: 98.2% (Compliant)
   - **Access Control Effectiveness**: 99.1% (Compliant)
   - **Audit Log Completeness**: 87.3% (Non-Compliant - high risk)
   - **Encryption Coverage**: 96.8% (Warning)

2. **Understand risk levels**:
   - **Low**: Metrics meeting or exceeding targets
   - **Medium**: Metrics approaching thresholds
   - **High**: Metrics below acceptable levels
   - **Critical**: Metrics requiring immediate attention

### Step 7: Monitor Compliance Events
1. **Review event types**:
   - **data_access**: User accessing sensitive data
   - **data_export**: Data being exported from systems
   - **consent_withdrawal**: Users withdrawing consent
   - **policy_violation**: Violations of compliance policies

2. **Analyze event patterns**:
   - Check for unusual access patterns
   - Monitor high-risk activities
   - Track compliance violations
   - Review user behavior trends

### Step 8: Generate Regulatory Reports
1. **GDPR Compliance Report**:
   ```bash
   curl -s http://localhost:8001/api/report/gdpr | jq '.'
   ```

2. **HIPAA Security Report**:
   ```bash
   curl -s http://localhost:8001/api/report/hipaa | jq '.'
   ```

3. **SOX Governance Report**:
   ```bash
   curl -s http://localhost:8001/api/report/sox | jq '.'
   ```

### Step 9: Customize the Dashboard (Optional)
1. **Add new metrics**:
   ```python
   new_metric = ComplianceMetric(
       metric_id="pci_compliance_score",
       name="PCI DSS Compliance Score",
       category="Security",
       value=92.5,
       target=95.0,
       status=ComplianceStatus.WARNING,
       risk_level=RiskLevel.MEDIUM,
       last_updated=datetime.utcnow(),
       details={"card_data_encrypted": True, "network_segmented": False}
   )
   
   dashboard.metrics[new_metric.metric_id] = new_metric
   dashboard._store_metric(new_metric)
   ```

2. **Add custom alerts**:
   ```python
   def check_custom_alerts(self):
       alerts = []
       
       # Check for data breach indicators
       recent_events = self._get_recent_events(hours=24)
       failed_access_count = sum(1 for e in recent_events 
                               if e['status'] == 'non_compliant' 
                               and e['event_type'] == 'data_access')
       
       if failed_access_count > 10:
           alerts.append({
               'type': 'security_incident',
               'severity': 'critical',
               'message': f'Potential data breach: {failed_access_count} failed access attempts'
           })
       
       return alerts
   ```

3. **Add new visualizations**:
   ```javascript
   // Trend chart for compliance over time
   const trendChart = new Chart(ctx, {
       type: 'line',
       data: {
           labels: timeLabels,
           datasets: [{
               label: 'Compliance Score',
               data: complianceScores,
               borderColor: '#3498db',
               fill: false
           }]
       }
   });
   ```

## Expected Output

### Dashboard Summary API Response
```json
{
  "total_metrics": 5,
  "compliant_metrics": 2,
  "warning_metrics": 2,
  "non_compliant_metrics": 1,
  "compliance_score": 40.0,
  "risk_distribution": {
    "low": 2,
    "medium": 2,
    "high": 1,
    "critical": 0
  },
  "last_updated": "2024-01-15T10:30:00.000Z"
}
```

### Compliance Events Response
```json
[
  {
    "id": "event-123",
    "timestamp": "2024-01-15T09:30:00.000Z",
    "event_type": "data_access",
    "user_id": "user123",
    "resource": "customer_data",
    "action": "read",
    "status": "compliant",
    "risk_level": "low",
    "metadata": {
      "purpose": "analytics",
      "consent": true
    }
  }
]
```

### GDPR Report Response
```json
{
  "framework": "GDPR",
  "generated_at": "2024-01-15T10:30:00.000Z",
  "metrics_count": 1,
  "compliance_status": "non_compliant",
  "metrics": [
    {
      "metric_id": "gdpr_consent_rate",
      "name": "GDPR Consent Rate",
      "category": "Privacy",
      "value": 94.5,
      "target": 95.0,
      "status": "warning"
    }
  ]
}
```

## Common Issues and Solutions

### Issue 1: Dashboard Not Loading
**Problem**: Web dashboard shows blank page or errors
**Solution**: 
- Check that the server is running on port 8001
- Verify no firewall blocking the port
- Check browser console for JavaScript errors
- Ensure Chart.js CDN is accessible

### Issue 2: Database Errors
**Problem**: SQLite database errors or missing data
**Solution**:
- Check file permissions for compliance.db
- Verify SQLite is installed
- Delete compliance.db to regenerate sample data
- Check disk space availability

### Issue 3: API Endpoints Not Responding
**Problem**: API calls return 404 or 500 errors
**Solution**:
- Verify Flask server is running
- Check endpoint URLs are correct
- Review server logs for error messages
- Ensure JSON responses are properly formatted

### Issue 4: Charts Not Displaying
**Problem**: Dashboard shows empty chart areas
**Solution**:
- Check Chart.js library is loaded
- Verify data format matches chart expectations
- Check browser developer tools for errors
- Ensure canvas elements have proper dimensions

## Challenge Extensions

### Extension 1: Real-time Alerts
Add real-time alerting with WebSockets:
```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    emit('status', {'msg': 'Connected to compliance monitoring'})

def send_alert(alert):
    socketio.emit('compliance_alert', alert)
```

### Extension 2: Advanced Analytics
Add trend analysis and predictive compliance:
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

class ComplianceAnalytics:
    def predict_compliance_trend(self, metric_history):
        df = pd.DataFrame(metric_history)
        X = df[['timestamp']].values
        y = df['value'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict next 30 days
        future_dates = pd.date_range(start=df['timestamp'].max(), periods=30)
        predictions = model.predict(future_dates.values.reshape(-1, 1))
        
        return predictions
```

### Extension 3: Integration with External Systems
Add integration with compliance management systems:
```python
class ComplianceIntegration:
    def sync_with_grc_system(self, grc_api_url, api_key):
        # Sync metrics with external GRC system
        headers = {'Authorization': f'Bearer {api_key}'}
        
        for metric in self.metrics.values():
            payload = {
                'metric_name': metric.name,
                'value': metric.value,
                'status': metric.status.value,
                'timestamp': metric.last_updated.isoformat()
            }
            
            requests.post(f'{grc_api_url}/metrics', 
                         json=payload, headers=headers)
```

### Extension 4: Automated Remediation
Add automated compliance remediation:
```python
class AutoRemediation:
    def __init__(self):
        self.remediation_rules = {
            'gdpr_consent_rate': self.fix_consent_issues,
            'encryption_coverage': self.enable_encryption,
            'access_control_effectiveness': self.review_access_controls
        }
    
    def auto_remediate(self, metric_id):
        if metric_id in self.remediation_rules:
            return self.remediation_rules[metric_id]()
        return None
    
    def fix_consent_issues(self):
        # Automated consent collection workflow
        return {'action': 'consent_campaign_initiated'}
```

## Completion Checklist
- [ ] Compliance dashboard runs successfully
- [ ] Web interface displays all components
- [ ] API endpoints return correct data
- [ ] Charts and visualizations work
- [ ] Sample metrics and events generated
- [ ] Regulatory reports can be generated
- [ ] Real-time updates function properly
- [ ] Database persistence works correctly

## Learning Outcomes
After completing this exercise, you will understand:
- Compliance monitoring system architecture
- Real-time dashboard development with Flask
- Data visualization with Chart.js
- Regulatory framework reporting
- Risk assessment and categorization
- Audit trail management
- Automated alert generation
- Database design for compliance data

## Next Steps
- Integrate with real compliance data sources
- Add more regulatory frameworks (PCI DSS, ISO 27001)
- Implement automated remediation workflows
- Add advanced analytics and trend prediction
- Create mobile-responsive dashboard
- Integrate with enterprise GRC systems
- Add role-based dashboard access
- Implement data export for auditors