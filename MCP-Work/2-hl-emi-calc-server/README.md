# Home Loan EMI Calculator MCP Server

An MCP server that provides home loan EMI calculation functionality.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### With MCP Inspector

1. Install dependencies and run with MCP Inspector:
```bash
pip install fastmcp
npx @modelcontextprotocol/inspector python server.py
```

2. Open the inspector in your browser and test the tool

### Direct Usage

```bash
python server.py
```

## Tool

- `calculate_home_loan_emi`: Calculate EMI, total amount, and interest for a home loan
  - Parameters:
    - `principal` (number): Loan amount
    - `annual_rate` (number): Annual interest rate as percentage
    - `tenure_years` (integer): Loan tenure in years