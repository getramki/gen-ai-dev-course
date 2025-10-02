# Business Rules and Constraints

## Profit Maximization Framework

### Purchase Agent (Construction Company)
- **Objective**: Minimize total procurement cost while meeting quality requirements
- **Constraints**:
  - Maximum budget per project: $500K
  - Quality thresholds: Grade A materials minimum
  - Delivery timeline: Within 30 days
  - Supplier diversity: Minimum 2 suppliers per material type

### Cement Sales Agent
- **Objective**: Maximize revenue and margin per sale
- **Constraints**:
  - Minimum margin: 15%
  - Maximum discount: 20% from list price
  - Inventory levels: Cannot oversell current stock
  - Credit terms: Net 30 days maximum

### Steel Sales Agent
- **Objective**: Maximize profit while managing inventory costs
- **Constraints**:
  - Minimum margin: 12%
  - Maximum discount: 25% for bulk orders (>100 tons)
  - Storage costs: $5/ton/month
  - Quality grades: A, B, C with different pricing

## Negotiation Cycle Management

### Cycle Structure
1. **Round 1**: Initial offers (no constraints)
2. **Round 2**: Counter-offers (10% adjustment limit)
3. **Round 3**: Competitive bidding (5% adjustment limit)
4. **Round 4**: Final offers (2% adjustment limit)
5. **Round 5**: Best and final (1% adjustment or auto-accept)

### Termination Conditions
- Maximum 5 cycles reached → Auto-finalize best available
- Mutual agreement reached → Immediate contract generation
- Budget exceeded → Reject and seek alternatives
- No improvement in 2 consecutive rounds → Auto-finalize

### Auto-Finalization Rules
- Purchase Agent: Accept lowest total cost within budget
- Sales Agents: Accept highest margin offer above minimum threshold
- Tie-breaking: Favor existing business relationships

## A2A Communication Elements

### Agent Card Structure
```json
{
  "agent_id": "cement_sales_001",
  "company": "ABC Cement Co",
  "capabilities": ["bulk_pricing", "quality_grades", "delivery"],
  "constraints": {
    "min_margin": 0.15,
    "max_discount": 0.20,
    "payment_terms": "net_30"
  },
  "pricing_authority": "manager_approval_required"
}
```

### Task Definition
```json
{
  "task_id": "procurement_2024_001",
  "type": "RFQ",
  "materials": ["cement", "steel"],
  "quantities": {"cement": "500_tons", "steel": "200_tons"},
  "budget": 100000,
  "deadline": "2024-02-15",
  "quality_requirements": "grade_a_minimum"
}
```

### Message Structure
```json
{
  "message_id": "msg_001",
  "task_id": "procurement_2024_001",
  "cycle": 1,
  "parts": {
    "header": {"from": "purchase_agent", "to": "cement_sales"},
    "body": {"quote_request": {...}},
    "constraints": {"max_price": 200, "delivery_by": "2024-02-15"}
  }
}
```

### Artifacts Management
- **Quotes**: Structured pricing with terms
- **Contracts**: Auto-generated from accepted quotes
- **Specifications**: Technical requirements
- **Approvals**: Human sign-off records

## Human Override Mechanisms

### Approval Thresholds
- Purchase Agent: >$50K requires manager approval
- Sales Agents: >20% discount requires director approval
- Contract changes: Legal review for terms modification

### Emergency Stops
- Market volatility: Pause negotiations if price swings >10%
- Compliance issues: Halt if regulatory requirements not met
- Budget overrun: Stop if projected costs exceed approved budget

### Manual Interventions
- Price ceiling enforcement
- Supplier blacklist management
- Quality standard updates
- Payment term modifications