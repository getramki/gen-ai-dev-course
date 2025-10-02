# Part 2: MCP Integration with FastMCP

## Overview
This module extends Part 1 agents with FastMCP tool integration for advanced profit optimization, constraint management, and resource access. Each agent gains specialized tools while maintaining profit maximization objectives.

## Key Features
- **FastMCP Servers**: Specialized tool servers for each domain
- **Enhanced Agents**: Part 1 agents extended with MCP capabilities
- **Profit Optimization**: Advanced margin analysis and cost optimization
- **Constraint Management**: Automated validation and enforcement
- **Resource Integration**: Database access and persistent state

## Architecture

### FastMCP Servers
1. **Construction Server** (Port 8000)
   - Budget tracking and utilization
   - ROI projection and analysis
   - Supplier performance analytics
   - Cost calculation with constraints

2. **Cement Server** (Port 8001)
   - Optimal margin calculation
   - Pricing strategy analysis
   - Inventory availability checking
   - Competitive response strategies

3. **Steel Server** (Port 8002)
   - Inventory carrying cost analysis
   - Grade-based pricing optimization
   - Market positioning analysis
   - Bulk discount strategies

### Enhanced Agents
- **EnhancedPurchaseAgent**: Extends Part 1 with MCP cost optimization
- **EnhancedCementAgent**: Extends Part 1 with MCP margin analysis
- **EnhancedSteelAgent**: Extends Part 1 with MCP inventory optimization

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start FastMCP Servers**
   ```bash
   # Terminal 1 - Construction Server
   python fastmcp_servers/construction_server.py --port 8000

   # Terminal 2 - Cement Server  
   python fastmcp_servers/cement_server.py --port 8001
   
   # Terminal 3 - Steel Server
   python fastmcp_servers/steel_server.py --port 8002
   ```

3. **Run Enhanced Demo**
   ```bash
   python demo.py
   ```

## MCP Tools Available

### Construction Tools
- `calculate_total_cost`: Cost analysis with constraint validation
- `track_budget_utilization`: Budget monitoring and alerts
- `analyze_supplier_performance`: Historical performance analysis
- `calculate_roi_projection`: Investment return calculations
- `create_project`: Project setup and tracking

### Cement Tools
- `calculate_optimal_margin`: Margin optimization with competition
- `analyze_pricing_strategy`: Market-based pricing strategies
- `check_inventory_availability`: Stock levels and carrying costs
- `calculate_competitive_response`: Dynamic competitive positioning
- `record_sale`: Transaction recording and tracking

### Steel Tools
- `calculate_inventory_carrying_cost`: Storage and handling costs
- `optimize_grade_pricing`: Grade-specific pricing optimization
- `calculate_bulk_discount_strategy`: Volume-based pricing
- `analyze_market_positioning`: Competitive market analysis
- `calculate_delivery_cost_impact`: Logistics cost integration

## Enhanced Capabilities

### Profit Optimization
- **Dynamic Pricing**: Real-time price adjustments based on market conditions
- **Margin Analysis**: Advanced margin calculations with cost factors
- **Inventory Optimization**: Carrying cost integration in pricing decisions
- **Competitive Intelligence**: Market positioning and response strategies

### Constraint Management
- **Automated Validation**: Real-time constraint checking via MCP
- **Violation Handling**: Automatic adjustments and alerts
- **Approval Workflows**: Threshold-based human intervention
- **Audit Trails**: Complete transaction and decision logging

### Resource Integration
- **Database Access**: Persistent storage for projects, inventory, sales
- **Historical Analysis**: Performance trends and supplier analytics
- **Market Data**: Competitive intelligence and positioning
- **Cost Modeling**: Advanced cost calculation with multiple factors

## Demo Scenarios

### Enhanced Procurement
- Purchase agent uses MCP tools for budget optimization
- Real-time ROI analysis and supplier performance evaluation
- Automated constraint validation and approval workflows

### Advanced Margin Optimization
- Cement agent leverages MCP for competitive positioning
- Dynamic pricing based on inventory levels and market conditions
- Automated margin optimization within human-set constraints

### Inventory-Driven Pricing
- Steel agent uses MCP for carrying cost integration
- Grade-specific optimization with market positioning
- Bulk discount strategies with profit protection

## Business Value

### For Construction Company
- **Cost Reduction**: Advanced procurement optimization
- **Risk Management**: Budget tracking and ROI analysis
- **Supplier Intelligence**: Performance-based decision making

### For Cement Company
- **Margin Maximization**: Dynamic pricing optimization
- **Market Leadership**: Competitive positioning strategies
- **Inventory Efficiency**: Cost-aware pricing decisions

### For Steel Company
- **Profit Optimization**: Grade and volume-based strategies
- **Market Positioning**: Competitive intelligence integration
- **Cost Management**: Comprehensive cost factor analysis

## Next Steps
- Part 3: A2A communication for inter-agent negotiation
- Part 4: Local deployment with Docker containers
- Part 5: Cloud deployment on AgentCore/EKS

## Troubleshooting

### Common Issues
1. **MCP Server Connection**: Ensure servers are running on correct ports
2. **Database Initialization**: Check SQLite database creation
3. **Tool Timeouts**: Verify network connectivity and server responsiveness
4. **Constraint Violations**: Review human-set limits in constraints_manager.py

### Debug Mode
Enable detailed logging by setting environment variable:
```bash
export MCP_DEBUG=1
python demo.py
```