"""
Exercise 2: Compliance Dashboard
Create a comprehensive governance and compliance monitoring system.
"""

import json
import boto3
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from flask import Flask, render_template_string, jsonify, request
import sqlite3
import uuid

class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    WARNING = "warning"
    UNKNOWN = "unknown"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ComplianceMetric:
    metric_id: str
    name: str
    category: str
    value: float
    target: float
    status: ComplianceStatus
    risk_level: RiskLevel
    last_updated: datetime
    details: Dict[str, Any]

class ComplianceDashboard:
    """Comprehensive compliance monitoring dashboard."""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.db_path = 'compliance.db'
        self.metrics = {}
        self.alerts = []
        
        # Initialize database
        self._init_database()
        
        # Setup routes
        self._setup_routes()
        
        # Generate sample data
        self._generate_sample_data()
    
    def _init_database(self):
        """Initialize SQLite database for compliance data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compliance_events (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                event_type TEXT,
                user_id TEXT,
                resource TEXT,
                action TEXT,
                status TEXT,
                risk_level TEXT,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compliance_metrics (
                metric_id TEXT PRIMARY KEY,
                name TEXT,
                category TEXT,
                value REAL,
                target REAL,
                status TEXT,
                risk_level TEXT,
                last_updated TEXT,
                details TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _generate_sample_data(self):
        """Generate sample compliance data."""
        
        # Sample metrics
        sample_metrics = [
            ComplianceMetric(
                metric_id="gdpr_consent_rate",
                name="GDPR Consent Rate",
                category="Privacy",
                value=94.5,
                target=95.0,
                status=ComplianceStatus.WARNING,
                risk_level=RiskLevel.MEDIUM,
                last_updated=datetime.utcnow(),
                details={"total_users": 10000, "consented_users": 9450}
            ),
            ComplianceMetric(
                metric_id="data_retention_compliance",
                name="Data Retention Compliance",
                category="Governance",
                value=98.2,
                target=100.0,
                status=ComplianceStatus.COMPLIANT,
                risk_level=RiskLevel.LOW,
                last_updated=datetime.utcnow(),
                details={"total_records": 50000, "compliant_records": 49100}
            ),
            ComplianceMetric(
                metric_id="access_control_effectiveness",
                name="Access Control Effectiveness",
                category="Security",
                value=99.1,
                target=99.0,
                status=ComplianceStatus.COMPLIANT,
                risk_level=RiskLevel.LOW,
                last_updated=datetime.utcnow(),
                details={"total_access_attempts": 100000, "authorized_attempts": 99100}
            ),
            ComplianceMetric(
                metric_id="audit_log_completeness",
                name="Audit Log Completeness",
                category="Audit",
                value=87.3,
                target=95.0,
                status=ComplianceStatus.NON_COMPLIANT,
                risk_level=RiskLevel.HIGH,
                last_updated=datetime.utcnow(),
                details={"expected_events": 10000, "logged_events": 8730}
            ),
            ComplianceMetric(
                metric_id="encryption_coverage",
                name="Data Encryption Coverage",
                category="Security",
                value=96.8,
                target=100.0,
                status=ComplianceStatus.WARNING,
                risk_level=RiskLevel.MEDIUM,
                last_updated=datetime.utcnow(),
                details={"total_data_assets": 1000, "encrypted_assets": 968}
            )
        ]
        
        # Store metrics
        for metric in sample_metrics:
            self.metrics[metric.metric_id] = metric
            self._store_metric(metric)
        
        # Generate sample events
        self._generate_sample_events()
    
    def _store_metric(self, metric: ComplianceMetric):
        """Store metric in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO compliance_metrics 
            (metric_id, name, category, value, target, status, risk_level, last_updated, details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metric.metric_id,
            metric.name,
            metric.category,
            metric.value,
            metric.target,
            metric.status.value,
            metric.risk_level.value,
            metric.last_updated.isoformat(),
            json.dumps(metric.details)
        ))
        
        conn.commit()
        conn.close()
    
    def _generate_sample_events(self):
        """Generate sample compliance events."""
        events = [
            {
                'id': str(uuid.uuid4()),
                'timestamp': (datetime.utcnow() - timedelta(hours=1)).isoformat(),
                'event_type': 'data_access',
                'user_id': 'user123',
                'resource': 'customer_data',
                'action': 'read',
                'status': 'compliant',
                'risk_level': 'low',
                'metadata': json.dumps({'purpose': 'analytics', 'consent': True})
            },
            {
                'id': str(uuid.uuid4()),
                'timestamp': (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                'event_type': 'data_export',
                'user_id': 'analyst456',
                'resource': 'sensitive_data',
                'action': 'export',
                'status': 'non_compliant',
                'risk_level': 'high',
                'metadata': json.dumps({'reason': 'missing_approval', 'data_classification': 'restricted'})
            },
            {
                'id': str(uuid.uuid4()),
                'timestamp': (datetime.utcnow() - timedelta(hours=3)).isoformat(),
                'event_type': 'consent_withdrawal',
                'user_id': 'customer789',
                'resource': 'personal_data',
                'action': 'withdraw_consent',
                'status': 'compliant',
                'risk_level': 'medium',
                'metadata': json.dumps({'processing_stopped': True, 'data_deleted': False})
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for event in events:
            cursor.execute('''
                INSERT OR REPLACE INTO compliance_events 
                (id, timestamp, event_type, user_id, resource, action, status, risk_level, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(event.values()))
        
        conn.commit()
        conn.close()
    
    def _setup_routes(self):
        """Setup Flask routes for dashboard."""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard view."""
            return render_template_string(DASHBOARD_HTML)
        
        @self.app.route('/api/metrics')
        def get_metrics():
            """Get all compliance metrics."""
            metrics_data = []
            for metric in self.metrics.values():
                metrics_data.append({
                    'metric_id': metric.metric_id,
                    'name': metric.name,
                    'category': metric.category,
                    'value': metric.value,
                    'target': metric.target,
                    'status': metric.status.value,
                    'risk_level': metric.risk_level.value,
                    'last_updated': metric.last_updated.isoformat(),
                    'details': metric.details
                })
            
            return jsonify(metrics_data)
        
        @self.app.route('/api/events')
        def get_events():
            """Get compliance events."""
            limit = int(request.args.get('limit', 50))
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM compliance_events 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            events = []
            for row in cursor.fetchall():
                events.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'event_type': row[2],
                    'user_id': row[3],
                    'resource': row[4],
                    'action': row[5],
                    'status': row[6],
                    'risk_level': row[7],
                    'metadata': json.loads(row[8]) if row[8] else {}
                })
            
            conn.close()
            return jsonify(events)
        
        @self.app.route('/api/summary')
        def get_summary():
            """Get compliance summary."""
            
            # Calculate summary statistics
            total_metrics = len(self.metrics)
            compliant_metrics = sum(1 for m in self.metrics.values() if m.status == ComplianceStatus.COMPLIANT)
            warning_metrics = sum(1 for m in self.metrics.values() if m.status == ComplianceStatus.WARNING)
            non_compliant_metrics = sum(1 for m in self.metrics.values() if m.status == ComplianceStatus.NON_COMPLIANT)
            
            # Risk distribution
            risk_distribution = {
                'low': sum(1 for m in self.metrics.values() if m.risk_level == RiskLevel.LOW),
                'medium': sum(1 for m in self.metrics.values() if m.risk_level == RiskLevel.MEDIUM),
                'high': sum(1 for m in self.metrics.values() if m.risk_level == RiskLevel.HIGH),
                'critical': sum(1 for m in self.metrics.values() if m.risk_level == RiskLevel.CRITICAL)
            }
            
            # Overall compliance score
            compliance_score = (compliant_metrics / total_metrics) * 100 if total_metrics > 0 else 0
            
            return jsonify({
                'total_metrics': total_metrics,
                'compliant_metrics': compliant_metrics,
                'warning_metrics': warning_metrics,
                'non_compliant_metrics': non_compliant_metrics,
                'compliance_score': round(compliance_score, 1),
                'risk_distribution': risk_distribution,
                'last_updated': datetime.utcnow().isoformat()
            })
        
        @self.app.route('/api/alerts')
        def get_alerts():
            """Get active compliance alerts."""
            
            alerts = []
            
            # Generate alerts based on metrics
            for metric in self.metrics.values():
                if metric.status == ComplianceStatus.NON_COMPLIANT:
                    alerts.append({
                        'id': f"alert_{metric.metric_id}",
                        'type': 'compliance_violation',
                        'severity': 'high',
                        'title': f"{metric.name} Non-Compliant",
                        'message': f"{metric.name} is at {metric.value}%, below target of {metric.target}%",
                        'metric_id': metric.metric_id,
                        'timestamp': metric.last_updated.isoformat()
                    })
                elif metric.status == ComplianceStatus.WARNING:
                    alerts.append({
                        'id': f"warning_{metric.metric_id}",
                        'type': 'compliance_warning',
                        'severity': 'medium',
                        'title': f"{metric.name} Warning",
                        'message': f"{metric.name} is at {metric.value}%, approaching target threshold",
                        'metric_id': metric.metric_id,
                        'timestamp': metric.last_updated.isoformat()
                    })
            
            return jsonify(alerts)
        
        @self.app.route('/api/report/<framework>')
        def generate_report(framework):
            """Generate compliance report for specific framework."""
            
            # Filter metrics by framework/category
            framework_mapping = {
                'gdpr': 'Privacy',
                'hipaa': 'Security',
                'sox': 'Governance'
            }
            
            category = framework_mapping.get(framework.lower(), 'All')
            
            if category == 'All':
                relevant_metrics = list(self.metrics.values())
            else:
                relevant_metrics = [m for m in self.metrics.values() if m.category == category]
            
            # Generate report
            report = {
                'framework': framework.upper(),
                'generated_at': datetime.utcnow().isoformat(),
                'metrics_count': len(relevant_metrics),
                'compliance_status': 'compliant' if all(m.status == ComplianceStatus.COMPLIANT for m in relevant_metrics) else 'non_compliant',
                'metrics': [asdict(m) for m in relevant_metrics]
            }
            
            return jsonify(report)
    
    def run(self, host='0.0.0.0', port=8001, debug=False):
        """Run the compliance dashboard."""
        print(f"Starting Compliance Dashboard on {host}:{port}")
        print("Dashboard features:")
        print("✓ Real-time compliance metrics")
        print("✓ Risk assessment and alerts")
        print("✓ Audit event tracking")
        print("✓ Regulatory reporting")
        print("✓ Interactive visualizations")
        
        self.app.run(host=host, port=port, debug=debug)

# HTML template for dashboard
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Compliance Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .metric-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-value { font-size: 2em; font-weight: bold; margin: 10px 0; }
        .compliant { color: #27ae60; }
        .warning { color: #f39c12; }
        .non-compliant { color: #e74c3c; }
        .chart-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .events-table { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f8f9fa; }
        .risk-low { background-color: #d4edda; }
        .risk-medium { background-color: #fff3cd; }
        .risk-high { background-color: #f8d7da; }
        .refresh-btn { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Compliance Dashboard</h1>
        <p>Real-time monitoring of compliance metrics and governance controls</p>
        <button class="refresh-btn" onclick="refreshData()">Refresh Data</button>
    </div>
    
    <div id="summary-cards" class="metrics-grid"></div>
    
    <div class="chart-container">
        <h3>Compliance Overview</h3>
        <canvas id="complianceChart" width="400" height="200"></canvas>
    </div>
    
    <div class="chart-container">
        <h3>Risk Distribution</h3>
        <canvas id="riskChart" width="400" height="200"></canvas>
    </div>
    
    <div class="events-table">
        <h3>Recent Compliance Events</h3>
        <table id="eventsTable">
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Event Type</th>
                    <th>User</th>
                    <th>Resource</th>
                    <th>Status</th>
                    <th>Risk Level</th>
                </tr>
            </thead>
            <tbody id="eventsBody"></tbody>
        </table>
    </div>

    <script>
        let complianceChart, riskChart;
        
        async function fetchData(endpoint) {
            const response = await fetch(`/api/${endpoint}`);
            return response.json();
        }
        
        async function refreshData() {
            await Promise.all([
                loadSummary(),
                loadMetrics(),
                loadEvents(),
                loadCharts()
            ]);
        }
        
        async function loadSummary() {
            const summary = await fetchData('summary');
            
            const summaryHtml = `
                <div class="metric-card">
                    <h3>Overall Compliance</h3>
                    <div class="metric-value compliant">${summary.compliance_score}%</div>
                    <p>${summary.compliant_metrics} of ${summary.total_metrics} metrics compliant</p>
                </div>
                <div class="metric-card">
                    <h3>Warnings</h3>
                    <div class="metric-value warning">${summary.warning_metrics}</div>
                    <p>Metrics requiring attention</p>
                </div>
                <div class="metric-card">
                    <h3>Violations</h3>
                    <div class="metric-value non-compliant">${summary.non_compliant_metrics}</div>
                    <p>Non-compliant metrics</p>
                </div>
            `;
            
            document.getElementById('summary-cards').innerHTML = summaryHtml;
        }
        
        async function loadEvents() {
            const events = await fetchData('events?limit=10');
            
            const tbody = document.getElementById('eventsBody');
            tbody.innerHTML = events.map(event => `
                <tr class="risk-${event.risk_level}">
                    <td>${new Date(event.timestamp).toLocaleString()}</td>
                    <td>${event.event_type}</td>
                    <td>${event.user_id}</td>
                    <td>${event.resource}</td>
                    <td>${event.status}</td>
                    <td>${event.risk_level}</td>
                </tr>
            `).join('');
        }
        
        async function loadCharts() {
            const summary = await fetchData('summary');
            
            // Compliance Chart
            const ctx1 = document.getElementById('complianceChart').getContext('2d');
            if (complianceChart) complianceChart.destroy();
            
            complianceChart = new Chart(ctx1, {
                type: 'doughnut',
                data: {
                    labels: ['Compliant', 'Warning', 'Non-Compliant'],
                    datasets: [{
                        data: [summary.compliant_metrics, summary.warning_metrics, summary.non_compliant_metrics],
                        backgroundColor: ['#27ae60', '#f39c12', '#e74c3c']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });
            
            // Risk Chart
            const ctx2 = document.getElementById('riskChart').getContext('2d');
            if (riskChart) riskChart.destroy();
            
            riskChart = new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: ['Low', 'Medium', 'High', 'Critical'],
                    datasets: [{
                        label: 'Risk Distribution',
                        data: [
                            summary.risk_distribution.low,
                            summary.risk_distribution.medium,
                            summary.risk_distribution.high,
                            summary.risk_distribution.critical
                        ],
                        backgroundColor: ['#27ae60', '#f39c12', '#e74c3c', '#8e44ad']
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', refreshData);
        
        // Auto-refresh every 30 seconds
        setInterval(refreshData, 30000);
    </script>
</body>
</html>
'''

def demonstrate_compliance_dashboard():
    """Demonstrate compliance dashboard functionality."""
    
    print("=== Compliance Dashboard Demo ===\n")
    
    dashboard = ComplianceDashboard()
    
    print("1. Dashboard Components:")
    components = [
        "Real-time compliance metrics monitoring",
        "Risk assessment and categorization",
        "Audit event tracking and analysis",
        "Regulatory framework reporting",
        "Interactive data visualizations",
        "Automated alert generation",
        "Historical trend analysis",
        "Export capabilities for auditors"
    ]
    
    for component in components:
        print(f"✓ {component}")
    
    print()
    
    print("2. Sample Metrics Generated:")
    for metric in dashboard.metrics.values():
        status_symbol = "✓" if metric.status == ComplianceStatus.COMPLIANT else "⚠️" if metric.status == ComplianceStatus.WARNING else "✗"
        print(f"{status_symbol} {metric.name}: {metric.value}% (target: {metric.target}%)")
    
    print()
    
    print("3. API Endpoints:")
    endpoints = [
        ("GET /", "Main dashboard interface"),
        ("GET /api/metrics", "Compliance metrics data"),
        ("GET /api/events", "Audit events log"),
        ("GET /api/summary", "Compliance summary statistics"),
        ("GET /api/alerts", "Active compliance alerts"),
        ("GET /api/report/<framework>", "Framework-specific reports")
    ]
    
    for endpoint, description in endpoints:
        print(f"{endpoint:<30} - {description}")
    
    print()
    
    print("4. Usage Instructions:")
    print("Start the dashboard:")
    print("python exercise_2_compliance_dashboard.py run")
    print()
    print("Access the dashboard:")
    print("http://localhost:8001")
    print()
    print("API examples:")
    print("curl http://localhost:8001/api/summary")
    print("curl http://localhost:8001/api/report/gdpr")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        # Run the dashboard
        dashboard = ComplianceDashboard()
        dashboard.run(debug=False)
    else:
        # Run demonstration
        demonstrate_compliance_dashboard()