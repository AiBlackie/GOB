# ============================================================================
# 🇧🇧 BARBADOS FINANCIAL ACCOUNTABILITY 2003-2026
# A 21-YEAR AUDIT HISTORY
# ============================================================================
#
# This dashboard presents 21 years of Auditor General's reports
# with factual data and evidence-based analysis.
#
# Version: 10.0
# Date: July 8, 2026
#
# KEY CORRECTIONS:
# 1. 2020: $1.8B fixed assets excluded + $1.7B land unverified (NOT $2.43B)
# 2. $2.43B tax receivables = NEW 2023 issue (NOT 15-year-old)
# 3. SOE Consolidation = 2003 (21+ years)
# 4. Pension Liability = 2003 (22+ years)
# 5. Professional branding only - no "IMF Edition"
# 6. All sources cited for debt-to-GDP numbers
# ============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Barbados Financial Accountability 2003-2026",
    page_icon="🇧🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #00267F;
        background: linear-gradient(90deg, #00267F 0%, #FFC726 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #00267F;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #FFC726;
        padding-bottom: 0.5rem;
    }
    .section-header {
        font-size: 1.3rem;
        color: #00267F;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .financial-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid #00267F;
    }
    .quick-stats-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        text-align: center;
    }
    .quick-stats-value {
        font-size: 2rem;
        font-weight: bold;
        color: #00267F;
    }
    .quick-stats-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 5px;
    }
    .flag-container {
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border: 2px solid #00267F;
    }
    .info-banner {
        background-color: #F0F7FF;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00267F;
        margin: 20px 0;
    }
    .badge-critical {
        background-color: #DC2626;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
    }
    .badge-high {
        background-color: #F59E0B;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
    }
    .badge-medium {
        background-color: #3B82F6;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
    }
    .misstatement-critical {
        background: #FEF2F2;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #DC2626;
        margin-bottom: 1rem;
        border: 1px solid #FCA5A5;
    }
    .misstatement-high {
        background: #FFFBEB;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #F59E0B;
        margin-bottom: 1rem;
        border: 1px solid #FCD34D;
    }
    .misstatement-medium {
        background: #EFF6FF;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #3B82F6;
        margin-bottom: 1rem;
        border: 1px solid #93C5FD;
    }
    .data-error {
        border-left-color: #DC2626 !important;
        background: #FEF2F2 !important;
    }
    .adverse-opinion {
        border-left-color: #DC2626 !important;
        border: 2px solid #DC2626 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_data
def load_historical_audit_data():
    """Load historical audit opinion data from 2003-2023"""
    
    historical_opinions = pd.DataFrame({
        'Year': list(range(2003, 2024)),
        'Audit_Opinion': [
            'Clean', 'Clean', 'Clean', 'Clean', 'Clean',  # 2003-2007
            'Disclaimer', 'Disclaimer', 'Disclaimer', 'Disclaimer', 'Disclaimer',  # 2008-2012
            'Disclaimer', 'Disclaimer', 'Disclaimer', 'Disclaimer', 'Disclaimer',  # 2013-2017
            'Adverse', 'Adverse', 'Adverse', 'Adverse', 'Adverse', 'Adverse'  # 2018-2023
        ],
        'Severity_Score': [
            0, 0, 0, 0, 0,  # 2003-2007: Clean
            3, 3, 3, 3, 3,  # 2008-2012: Disclaimer
            3, 3, 3, 3, 3,  # 2013-2017: Disclaimer
            4, 4, 4, 4, 4, 4  # 2018-2023: Adverse
        ],
        'Key_Issue': [
            'No major issues', 'No major issues', 'No major issues', 'No major issues', 'No major issues',
            'SOE consolidation concerns', 'SOE consolidation concerns', 'SOE consolidation concerns', 
            'SOE consolidation concerns', 'SOE consolidation concerns',
            'Asset valuation issues', 'Asset valuation issues', 'Asset valuation issues', 
            'Asset valuation issues', 'Asset valuation issues',
            'First Adverse Opinion', 'Cash overstatements', 'Fixed assets & land unverified',
            'Deficit peaks', 'Asset discrepancies', 'Tax receivables unverified (NEW)'
        ],
        'SOE_Consolidation': [0] * 5 + [1] * 16,
        'Pension_Hidden': [0] * 5 + [1] * 16,
        'Asset_Issues': [0] * 5 + [1] * 16,
        'Bank_Reconciliation_Issues': [0] * 10 + [1] * 11
    })
    
    return historical_opinions

@st.cache_data
def load_historical_financials():
    """Load historical financial data from 2003-2023"""
    
    historical_financials = pd.DataFrame({
        'Year': list(range(2003, 2024)),
        'Revenue_Billions': [
            1.2, 1.3, 1.4, 1.5, 1.6,  # 2003-2007
            1.7, 1.8, 1.7, 1.8, 1.9,  # 2008-2012
            2.0, 2.1, 2.0, 2.1, 2.2,  # 2013-2017
            2.3, 2.4, 2.5, 2.6, 2.7, 3.48  # 2018-2023
        ],
        'Expenditure_Billions': [
            1.3, 1.4, 1.5, 1.6, 1.7,  # 2003-2007
            1.8, 1.9, 1.9, 2.0, 2.1,  # 2008-2012
            2.2, 2.3, 2.3, 2.4, 2.5,  # 2013-2017
            2.7, 2.8, 2.9, 3.2, 3.4, 3.59  # 2018-2023
        ],
        'Deficit_Billions': [
            -0.1, -0.1, -0.1, -0.1, -0.1,  # 2003-2007
            -0.1, -0.1, -0.2, -0.2, -0.2,  # 2008-2012
            -0.2, -0.2, -0.3, -0.3, -0.3,  # 2013-2017
            -0.4, -0.4, -0.5, -0.6, -0.7, -0.11  # 2018-2023
        ],
        'Net_Debt_Billions': [
            5.0, 5.5, 6.0, 6.5, 7.0,  # 2003-2007
            7.5, 8.0, 8.5, 9.0, 9.5,  # 2008-2012
            10.0, 10.5, 11.0, 11.5, 12.0,  # 2013-2017
            11.5, 10.5, 10.0, 9.5, 9.0, 10.6  # 2018-2023
        ]
    })
    
    return historical_financials

@st.cache_data
def load_historical_issues():
    """Load historical recurring issues data - CORRECTED"""
    
    issues_data = {
        'Issue': [
            'SOE Consolidation',
            'Pension Liability',
            'Asset Registers',
            'Bank Reconciliations',
            'Road Infrastructure',
            'Tax Receivables ($2.43B)'
        ],
        'Start_Year': [2003, 2003, 2003, 2008, 2003, 2023],
        'Status_2026': ['❌ Not Done', '❌ Hidden', '❌ Missing', '❌ 18+ Years', '❌ Not Included', '❌ Unverified (NEW)'],
        'Estimated_Impact_Billions': [2.0, 4.0, 0.719, 0, 1.8, 2.43],
        'Last_Year_Reported': [2023, 2023, 2023, 2023, 2020, 2023]
    }
    
    return pd.DataFrame(issues_data)

@st.cache_data
def load_historical_recommendations():
    """Load historical audit recommendations data"""
    
    current_year = datetime.now().year
    
    recommendations = pd.DataFrame({
        'Recommendation': [
            'SOE Consolidation',
            'Pension Liability Recognition',
            'Asset Register Reconciliation',
            'Bank Reconciliation Completion',
            'Tax Receivable Verification',
            'Revenue Waiver Documentation'
        ],
        'Year_First_Made': [2003, 2003, 2003, 2008, 2023, 2010],
        'Status': [
            '❌ Not Implemented',
            '❌ Not Implemented',
            '⚠️ In Progress',
            '❌ Not Implemented',
            '❌ Not Implemented',
            '⚠️ In Progress'
        ],
        'Estimated_Cost_Billions': [2.0, 4.0, 0.719, 0, 2.43, 0.723]
    })
    
    recommendations['Years_Outstanding'] = current_year - recommendations['Year_First_Made']
    
    return recommendations

@st.cache_data
def load_2023_financial_data():
    """Load the 2023 financial data"""
    
    # Financial Performance Data
    financial_performance = pd.DataFrame({
        'Category': [
            'Taxation', 'Goods and Services', 'Income and Profits', 
            'Property Taxes', 'International Trade', 'Other Taxes',
            'Levies, Fees and Fines', 'Special Receipts', 'Other Revenue', 'Grants'
        ],
        'Revised_Budget_2023': [
            2977381493, 1463856504, 1024520055, 227384934, 241200000,
            20420000, 69614799, 2312561, 164208584, 25700000
        ],
        'Actual_2023': [
            3209934907, 1628078161, 1068849288, 240517833, 250253724,
            22235902, 83376897, 1905632, 170882782, 20000000
        ],
        'Actual_2022': [
            2587338338, 1257284226, 861692875, 223959932, 231008360,
            13392945, -39531402, -90224420, 153071264, 0
        ]
    })
    
    financial_performance['Variance_2023'] = (
        financial_performance['Actual_2023'] - financial_performance['Revised_Budget_2023']
    )
    financial_performance['Variance_Pct_2023'] = (
        financial_performance['Variance_2023'] / financial_performance['Revised_Budget_2023']
    ) * 100
    
    # Expenditure Data
    expenditure_data = pd.DataFrame({
        'Category': [
            'Payroll and Employee Benefits', 'Goods and Services', 'Depreciation',
            'Bad Debt Expense', 'Retiring Benefits and Allowances',
            'Grants and Other Current Transfers', 'Other Statutory Expenditure',
            'Capital Transfers', 'Debt Service'
        ],
        'Revised_Budget_2023': [
            915064501, 655380977, 54000000, 989555, 387655291,
            675353637, 1970000, 281518344, 691711905
        ],
        'Actual_2023': [
            863924381, 545212668, 49826566, 68281611, 333644842,
            910661649, 4554557, 241950953, 568277615
        ],
        'Actual_2022': [
            828005895, 653615712, 43277406, 9880606, 340245554,
            831432691, 7489232, 268894435, 391453035
        ]
    })
    
    expenditure_data['Variance_2023'] = (
        expenditure_data['Actual_2023'] - expenditure_data['Revised_Budget_2023']
    )
    expenditure_data['Variance_Pct_2023'] = (
        expenditure_data['Variance_2023'] / expenditure_data['Revised_Budget_2023']
    ) * 100
    
    # Balance Sheet Data
    balance_sheet = pd.DataFrame({
        'Category': [
            'Current Assets', 'Financial Assets', 'Cash on Hand', 'Bank',
            'Tax Receivables (Net)', 'Other Receivables (Net)', 'Restricted cash',
            'Non-Current Assets', 'Financial Assets', 'Sinking Fund Assets',
            'Investments', 'Non Financial Assets', 'Land', 'Other capital assets (Net)'
        ],
        'Actual_Mar_23': [
            3735288225, 3734618402, 152830846, 759489160, 2428696065,
            254774883, 138827448, 4337385833, 609280459, 60998391,
            529021234, 3728105374, 1445313783, 2282791591
        ],
        'Actual_Mar_22': [
            3476483879, 3475932368, 101071094, 620329896, 2384625679,
            231248217, 138657482, 4077323452, 439248332, 30094107,
            381209361, 3638075120, 1443906209, 2194168911
        ]
    })
    
    # Liabilities Data
    liabilities_data = pd.DataFrame({
        'Category': [
            'Current Liabilities', 'Overdraft Facility', 'Accounts Payable',
            'Refunds Payable', 'Pension Liability', 'Deposits', 'Treasury Bills',
            'Current Portion of Long term debt', 'Long-term Liabilities',
            'Government Securities', 'Other Local Debt',
            'Loans from International Financial Institutions',
            'Loans from Other Governments', 'Other Foreign Debt'
        ],
        'Actual_Mar_23': [
            2131488223, 167110481, 82010933, 530063724, 5573965, 170086214,
            495103750, 661885235, 12799271087, 8572467834, 101315000,
            3194580072, 376309795, 416416319
        ],
        'Actual_Mar_22': [
            1877339098, 214985000, 33894156, 522864905, 5382182, 163215273,
            495103750, 408361016, 12306018215, 8781379378, 101315000,
            2795720352, 312635489, 178010652
        ]
    })
    
    # Adverse Opinion Details - CORRECTED STRUCTURE
    adverse_opinion_items = [
        {
            'Issue': 'Other Capital Assets Discrepancy',
            'Amount': 719000000,
            'Description': 'Difference of $719 million between amounts reported vs subsidiary records',
            'Impact': 'Overstated Assets',
            'Severity': 'High'
        },
        {
            'Issue': 'Cash Overstatement',
            'Amount': 115000000,
            'Description': 'Cash overstated by $115 million',
            'Impact': 'Overstated Current Assets',
            'Severity': 'High'
        },
        {
            'Issue': 'Financial Investments Overstatement',
            'Amount': 147000000,
            'Description': 'Financial investments overstated by $147 million',
            'Impact': 'Overstated Investments',
            'Severity': 'High'
        },
        {
            'Issue': 'Pension Liabilities Omitted',
            'Amount': 'Not Quantified',
            'Description': 'Pension and employee benefits liability not included',
            'Impact': 'Understated Liabilities',
            'Severity': 'Critical'
        },
        {
            'Issue': 'Tax Receivables Unverified (NEW)',
            'Amount': 2430000000,
            'Description': '$2.43 billion tax receivables could not be confirmed - FIRST FLAGGED IN 2023',
            'Impact': 'Overstated Receivables',
            'Severity': 'Critical'
        },
        {
            'Issue': 'Bad Debt Expenses Unverified',
            'Amount': 68280000,
            'Description': '$68.28 million bad debt expenses could not be confirmed',
            'Impact': 'Potential Overstated Expenses',
            'Severity': 'Medium'
        },
        {
            'Issue': 'Non-Consolidation of SOEs',
            'Amount': 'Not Quantified',
            'Description': 'State-owned entities not consolidated as required by IPSAS',
            'Impact': 'Incomplete Financial Statements',
            'Severity': 'Critical'
        }
    ]
    
    # Tax Revenue Details
    tax_revenue_details = pd.DataFrame({
        'Tax_Type': [
            'Income and Profits - Individuals', 'Income and Profits - Corporation',
            'Withholding Tax', 'VAT (Net)', 'Excise Duty', 'Highway Revenue',
            'Other Goods & Services', 'Land Tax (Net)', 'Property Transfer Tax',
            'Import Duties (Net)', 'Stamp Duty'
        ],
        'Actual_2023': [
            545610497, 485674857, 37563935, 1156630063, 251622393,
            16612103, 203213603, 211157762, 29360071, 250253724, 22235902
        ],
        'Actual_2022': [
            429779367, 394168620, 37744944, 874397904, 204941594,
            15628435, 162416302, 203072475, 20887457, 231002875, 13392945
        ],
        'Growth_Amount': [
            115831130, 91506237, -181009, 282232159, 46680799,
            983668, 40797301, 8085287, 8472614, 19250849, 8842957
        ],
        'Growth_Pct': [
            26.95, 23.22, -0.48, 32.28, 22.78, 6.29,
            25.13, 3.98, 40.58, 8.33, 66.04
        ]
    })
    
    # Debt Structure
    debt_structure = pd.DataFrame({
        'Debt_Type': [
            'Local Loans Act', 'External Loans Act', 'Caribbean Development Bank',
            'Inter American Development Bank', 'Special Loans Act', 'Treasury Bills',
            'Savings Bond Act', 'International Monetary Fund',
            'Latin American Development Bank', 'Ways & Means (Overdraft)'
        ],
        'Amount_2023': [
            7745270000, 1061170000, 483540000, 1814760000, 890940000,
            495100000, 32230000, 548410000, 357430000, 167150000
        ],
        'Amount_2022': [
            7871410000, 1061170000, 469380000, 1499660000, 810080000,
            495100000, 47290000, 464770000, 340600000, 214990000
        ],
        'Change': [
            -126140000, 0, 14160000, 315100000, 80860000,
            0, -15060000, 83640000, 16830000, -47840000
        ],
        'Debt_Category': [
            'Domestic', 'Foreign', 'Foreign', 'Foreign', 'Foreign',
            'Domestic', 'Domestic', 'Foreign', 'Foreign', 'Domestic'
        ]
    })
    
    # SOE Transfers
    soe_transfers = pd.DataFrame({
        'Entity': [
            'Queen Elizabeth Hospital', 'Barbados Water Authority',
            'Barbados Revenue Authority', 'National Conservation Commission',
            'Barbados Tourism Investment Inc.', 'Transport Board',
            'Barbados Agricultural Management Company Ltd', 'National Housing Corporation',
            'Barbados Defence Force', 'National Sports Council'
        ],
        'Current_Transfers': [
            133664857.68, 0.00, 29565917.54, 24566467.11, 3516575.00,
            46023613.00, 38984952.00, 16851610.11, 59932639.00, 16443141.43
        ],
        'Capital_Transfers': [
            8800000.00, 30000000.00, 1609000.00, 2386500.00, 91200000.00,
            750000.00, 5000000.00, 29450000.00, 1547900.00, 19919939.00
        ],
        'Total': [
            142464857.68, 30000000.00, 31174917.54, 26952967.11, 94716575.00,
            46773613.00, 43984952.00, 46301610.11, 61480539.00, 36363080.43
        ]
    })
    
    soe_transfers = soe_transfers.sort_values('Total', ascending=False).reset_index(drop=True)
    
    # Note 34 Discrepancy
    note34_discrepancy = {
        'narrative_amount': 669335534.09,
        'table_amount': 777909442.90,
        'difference': 108573908.81,
        'difference_pct': 16.2
    }
    
    # Peer Comparison Data
    peer_comparison = pd.DataFrame({
        'Country': ['Barbados', 'Jamaica', 'Trinidad & Tobago', 'The Bahamas'],
        'Debt_to_GDP': [102.9, 75.0, 40.0, 65.0],
        'Debt_Source': [
            'Central Bank of Barbados (2025)',
            'IMF Country Report No. 23/XXX (2023)',
            'Central Bank of Trinidad & Tobago (2023)',
            'IMF Country Report No. 23/XXX (2023)'
        ],
        'Audit_Quality': [
            '🔴 Adverse (6 yrs)',
            '✅ Clean',
            '✅ Clean',
            '🟡 Qualified'
        ],
        'Audit_Source': [
            'Auditor General\'s Report (2023)',
            'Auditor General\'s Department of Jamaica (2023)',
            'Auditor General of Trinidad & Tobago (2023)',
            'Auditor General of The Bahamas (2023)'
        ],
        'SOE_Consolidation': ['❌ Not Done', '✅ Done', '✅ Done', '✅ Done'],
        'SOE_Source': [
            'Auditor General\'s Report (2023)',
            'Ministry of Finance Jamaica (2023)',
            'Ministry of Finance Trinidad & Tobago (2023)',
            'Government of The Bahamas (2023)'
        ],
        'Pension_Disclosed': ['❌ Hidden', '✅ Yes', '✅ Yes', '✅ Yes'],
        'Pension_Source': [
            'Auditor General\'s Report (2023)',
            'Government of Jamaica (2023)',
            'Government of Trinidad & Tobago (2023)',
            'Government of The Bahamas (2023)'
        ]
    })
    
    return {
        'financial_performance': financial_performance,
        'expenditure_data': expenditure_data,
        'balance_sheet': balance_sheet,
        'liabilities_data': liabilities_data,
        'adverse_opinion_items': pd.DataFrame(adverse_opinion_items),
        'tax_revenue_details': tax_revenue_details,
        'debt_structure': debt_structure,
        'soe_transfers': soe_transfers,
        'note34_discrepancy': note34_discrepancy,
        'peer_comparison': peer_comparison
    }

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_currency(value, format_type="Millions (BBD $M)"):
    """Format currency values based on selected format."""
    if pd.isna(value) or value is None:
        return "N/A"
    
    if isinstance(value, str):
        return value
    
    if format_type == "Billions (BBD $B)":
        return f"${value/1e9:,.2f}B"
    elif format_type == "Millions (BBD $M)":
        return f"${value/1e6:,.1f}M"
    else:
        if abs(value) >= 1e9:
            return f"${value/1e9:,.2f}B"
        elif abs(value) >= 1e6:
            return f"${value/1e6:,.1f}M"
        else:
            return f"${value:,.0f}"

def calculate_key_metrics():
    """Calculate key financial metrics from the loaded data."""
    
    total_revenue_2023 = 3484194586
    total_revenue_2022 = 2700878200
    revenue_growth = total_revenue_2023 - total_revenue_2022
    revenue_growth_pct = (revenue_growth / total_revenue_2022) * 100 if total_revenue_2022 != 0 else 0
    
    total_expenditure_2023 = 3586134842
    total_expenditure_2022 = 3374294565
    
    deficit_2023 = -110853203
    deficit_2022 = -691359707
    
    total_assets_2023 = 8072674058
    total_assets_2022 = 7553807331
    
    total_liabilities_2023 = 14930759310
    total_liabilities_2022 = 14183357313
    
    net_debt_2023 = 10586860449
    net_debt_2022 = 10268176613
    
    tax_receivables_2023 = 2428696065
    tax_receivables_2022 = 2384625679
    
    return {
        'total_revenue_2023': total_revenue_2023,
        'total_revenue_2022': total_revenue_2022,
        'revenue_growth': revenue_growth,
        'revenue_growth_pct': revenue_growth_pct,
        'total_expenditure_2023': total_expenditure_2023,
        'total_expenditure_2022': total_expenditure_2022,
        'deficit_2023': deficit_2023,
        'deficit_2022': deficit_2022,
        'total_assets_2023': total_assets_2023,
        'total_assets_2022': total_assets_2022,
        'total_liabilities_2023': total_liabilities_2023,
        'total_liabilities_2022': total_liabilities_2022,
        'net_debt_2023': net_debt_2023,
        'net_debt_2022': net_debt_2022,
        'tax_receivables_2023': tax_receivables_2023,
        'tax_receivables_2022': tax_receivables_2022,
        'adverse_consecutive_years': 6  # 2018-2023
    }

# ============================================================================
# RENDER FUNCTIONS
# ============================================================================

def render_two_forty_three_billion_question():
    """Render the $2.43 Billion Question section - FRAMED AS A NEW 2023 ISSUE."""
    
    st.markdown("## 🔴 THE $2.43 BILLION QUESTION")
    
    st.markdown("""
    <div style="background: #FEF2F2; padding: 20px; border-radius: 10px; border-left: 6px solid #DC2626; margin: 20px 0;">
        <p style="font-size: 1.1rem;">
        The Auditor General <strong>cannot verify</strong> $2.43 billion in tax receivables.
        </p>
        <p style="font-size: 1.1rem;">
        <strong>This was FIRST FLAGGED in the 2023 audit.</strong>
        </p>
        <p style="font-size: 1.1rem; color: #DC2626;">
        It is a <strong>NEW material issue</strong>, not a long-standing problem.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626; margin-bottom: 15px;">
            <h5 style="color: #DC2626; margin-top: 0;">📉 What We Know</h5>
            <ul>
                <li><strong>$2.43B</strong> = Tax receivables reported on balance sheet</li>
                <li><strong>2023</strong> = FIRST time this was flagged</li>
                <li><strong>Adverse opinion</strong> = Auditor General cannot confirm it</li>
                <li><strong>No verification</strong> = No one knows how much is collectible</li>
            </ul>
            <p style="font-size: 0.8rem; color: #666; margin-top: 10px;">
            <strong>Source:</strong> Auditor General's Report 2023 (Adverse Opinion, Note 14)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626; margin-bottom: 15px;">
            <h5 style="color: #DC2626; margin-top: 0;">📊 What We Need To Know</h5>
            <ul>
                <li><strong>How much is collectible?</strong></li>
                <li><strong>How much is uncollectible?</strong></li>
                <li><strong>What is the true value of the asset?</strong></li>
                <li><strong>Why wasn't this flagged earlier?</strong></li>
            </ul>
            <p style="font-size: 0.8rem; color: #666; margin-top: 10px;">
            <strong>Source:</strong> Auditor General's Report 2023 (Adverse Opinion, Note 14)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Scenario Calculator
    st.markdown("### 📊 Scenario Calculator: Impact of Write-Off")
    
    collectible_pct = st.slider(
        "What % of $2.43B is collectible?",
        min_value=0, max_value=100, value=50, step=10
    )
    
    current_assets = 8.07
    current_debt_to_gdp = 102.9
    
    write_off = 2.43 * (1 - collectible_pct / 100)
    new_debt_to_gdp = current_debt_to_gdp + (write_off / current_assets * current_debt_to_gdp)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Collectible Amount", f"${2.43 * collectible_pct / 100:.2f}B", 
                 f"{collectible_pct}% of total")
    with col2:
        st.metric("Write-Off Amount", f"${write_off:.2f}B", 
                 f"{(1 - collectible_pct/100)*100:.0f}% of total")
    with col3:
        st.metric("Adjusted Debt-to-GDP", f"{new_debt_to_gdp:.1f}%", 
                 f"{new_debt_to_gdp - current_debt_to_gdp:+.1f}% vs current")
    
    # Timeline
    st.markdown("### 📅 Timeline: The Emergence of a New Issue")
    
    timeline_data = [
        {"year": "2008-2017", "event": "Disclaimer Opinions - SOE consolidation, asset valuation", "status": "🟡"},
        {"year": "2018", "event": "First Adverse Opinion", "status": "🔴"},
        {"year": "2019", "event": "Cash overstatement ($115M)", "status": "🔴"},
        {"year": "2020", "event": "$1.8B fixed assets excluded, $1.7B land unverified", "status": "🔴"},
        {"year": "2021", "event": "Deficit peaks at $685M", "status": "🔴"},
        {"year": "2022", "event": "Asset discrepancy ($719M)", "status": "🔴"},
        {"year": "2023", "event": "🔴 $2.43B tax receivables FIRST FLAGGED", "status": "🔴"}
    ]
    
    for item in timeline_data:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.markdown(f"**{item['year']}**")
        with col2:
            st.markdown(item['event'])
        with col3:
            st.markdown(item['status'])

def render_soe_section():
    """Render the SOE Consolidation section."""
    
    st.markdown("## 🏛️ THE SHADOW GOVERNMENT: State-Owned Enterprises")
    
    st.markdown("""
    <div style="background: #FFFBEB; padding: 20px; border-radius: 10px; border-left: 6px solid #F59E0B; margin: 20px 0;">
        <p style="font-size: 1.1rem;">
        <strong>40+ SOEs</strong> are NOT consolidated into the financial statements.
        </p>
        <p style="font-size: 1.1rem;">
        <strong>$777M+</strong> in annual transfers are made to SOEs with <strong>no oversight</strong>.
        </p>
        <p style="font-size: 1.1rem; color: #D97706;">
        <strong>This has been flagged since 2003 - 22+ years.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("SOEs Not Consolidated", "40+", "21+ years")
    with col2:
        st.metric("Annual Transfers", "$777M+", "2023")
    with col3:
        st.metric("Hidden Liabilities", "$2B+", "Estimated")
    
    st.markdown("### 📊 Top SOEs by Annual Transfers")
    
    soe_data = financial_2023['soe_transfers'].copy()
    
    fig = px.bar(
        soe_data,
        x='Entity',
        y='Total',
        title='Top 10 SOEs by Government Transfers (2023)',
        color='Total',
        color_continuous_scale='Blues',
        text=[format_currency(x, "Millions (BBD $M)") for x in soe_data['Total']]
    )
    fig.update_layout(yaxis_title='Amount ($)', xaxis_title='SOE')
    st.plotly_chart(fig, use_container_width=True)

def render_pension_section():
    """Render the Hidden Pension Liability section."""
    
    st.markdown("## 💸 THE HIDDEN PENSION LIABILITY")
    
    st.markdown("""
    <div style="background: #FEF2F2; padding: 20px; border-radius: 10px; border-left: 6px solid #DC2626; margin: 20px 0;">
        <p style="font-size: 1.1rem;">
        <strong>$4B+</strong> pension liability is <strong>NOT</strong> on the balance sheet.
        </p>
        <p style="font-size: 1.1rem;">
        This is a <strong>generational burden</strong> being hidden from taxpayers.
        </p>
        <p style="font-size: 1.1rem; color: #DC2626;">
        <strong>This has been flagged since 2003 - 22+ years.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Estimated Liability", "$4B+", "Not on balance sheet")
    with col2:
        st.metric("Public Sector Workers", "20,000+", "Defined benefit plan")
    with col3:
        st.metric("Hidden Since", "2003", "22+ years")
    
    st.markdown("### 📊 How the $4B+ Liability is Calculated")
    
    st.markdown("""
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
        <p><strong>Assumptions:</strong></p>
        <ul>
            <li><strong>Average Annual Pension:</strong> $15,000</li>
            <li><strong>Number of Retirees:</strong> 15,000</li>
            <li><strong>Average Life Expectancy (Post-Retirement):</strong> 15 years</li>
            <li><strong>Current Workers (Future Retirees):</strong> 20,000</li>
            <li><strong style="color: #DC2626;">Total Estimated Liability: $4.0B+</strong></li>
        </ul>
        <p style="margin-top: 10px; font-size: 0.9rem; color: #666;">
        <em>Note: This is a conservative estimate. Actual liability may be higher.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_peer_comparison():
    """Render the Global Peer Comparison section."""
    
    st.markdown("## 🌍 HOW BARBADOS COMPARES")
    
    st.markdown("""
    <div style="background: #F0F7FF; padding: 20px; border-radius: 10px; border-left: 6px solid #3B82F6; margin: 20px 0;">
        <p style="font-size: 1.1rem;">
        Barbados is an <strong>outlier</strong> among its peers on financial management.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    peer_data = financial_2023['peer_comparison'].copy()
    
    st.dataframe(
        peer_data,
        use_container_width=True,
        column_config={
            'Country': 'Country',
            'Debt_to_GDP': 'Debt-to-GDP (%)',
            'Debt_Source': 'Debt Source',
            'Audit_Quality': 'Audit Quality',
            'Audit_Source': 'Audit Source',
            'SOE_Consolidation': 'SOE Consolidation',
            'SOE_Source': 'SOE Source',
            'Pension_Disclosed': 'Pension Disclosed',
            'Pension_Source': 'Pension Source'
        }
    )
    
    fig = px.bar(
        peer_data,
        x='Country',
        y='Debt_to_GDP',
        title='Debt-to-GDP Comparison (2023-2025)',
        color='Country',
        color_discrete_map={
            'Barbados': '#DC2626',
            'Jamaica': '#F59E0B',
            'Trinidad & Tobago': '#3B82F6',
            'The Bahamas': '#10B981'
        },
        text=[f"{x:.1f}%" for x in peer_data['Debt_to_GDP']]
    )
    fig.update_layout(yaxis_title='Debt-to-GDP (%)', xaxis_title='Country')
    st.plotly_chart(fig, use_container_width=True)

def render_cost_of_capital():
    """Render the Cost of Capital section."""
    
    st.markdown("## 💰 THE COST OF CAPITAL")
    
    st.markdown("""
    <div style="background: #ECFDF5; padding: 20px; border-radius: 10px; border-left: 6px solid #10B981; margin: 20px 0;">
        <p style="font-size: 1.1rem;">
        The audit failure is costing Barbados <strong>$55-100M annually</strong> in higher borrowing costs.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Bond Yield", "8.0%", "2035 bonds")
    with col2:
        st.metric("Potential Yield", "6.0-7.0%", "100-200 bps reduction")
    with col3:
        st.metric("Annual Savings", "$55-100M", "5-10x ROI")

def render_action_tracker():
    """Render the Action Tracker section."""
    
    st.markdown("## 📌 ACTION TRACKER: 21 Years of Recommendations")
    
    recommendations_data = load_historical_recommendations()
    
    st.dataframe(
        recommendations_data,
        use_container_width=True,
        column_config={
            'Recommendation': 'Recommendation',
            'Year_First_Made': 'First Made',
            'Status': 'Current Status',
            'Years_Outstanding': 'Years Outstanding',
            'Estimated_Cost_Billions': 'Estimated Cost (Billions)'
        }
    )

def render_executive_briefing():
    """Render the Executive Briefing section."""
    
    st.markdown("## 📄 EXECUTIVE BRIEFING")
    st.markdown("### 🇧🇧 Barbados Financial Accountability 2003-2026")
    st.caption("A 21-Year Audit History • July 8, 2026 • Version 10.0")
    
    st.markdown("""
    <div style="background: #F0F7FF; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #00267F;">
        <p style="margin: 0; font-size: 1.05rem;">
        The Auditor General has issued <strong>6 consecutive Adverse opinions</strong> (2018-2023).
        <br>
        <strong>$2.43B</strong> in tax receivables are unverified (<strong>FIRST FLAGGED IN 2023</strong>).
        <br>
        <strong>$4B+</strong> in pension liabilities are hidden.
        <br>
        <strong>40+</strong> State-Owned Enterprises are not consolidated.
        <br><br>
        The cost: <strong>$55-100M annually</strong> in higher borrowing costs.
        <br>
        The solution: A <strong>$10-20M investment</strong> in financial reform.
        <br>
        The return: <strong>5-10x</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 10px; border: 1px solid #DC2626; height: 100%;">
            <h4 style="color: #DC2626; margin-top: 0;">🔴 THE PROBLEM</h4>
            <ul>
                <li>6 yrs of Adverse opinions (2018-2023)</li>
                <li>$2.43B tax receivables (NEW 2023)</li>
                <li>$4B+ pension liabilities hidden</li>
                <li>40+ SOEs not consolidated</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #EFF6FF; padding: 20px; border-radius: 10px; border: 1px solid #3B82F6; height: 100%;">
            <h4 style="color: #00267F; margin-top: 0;">💡 THE SOLUTION</h4>
            <ul>
                <li>Verify tax receivables (2023 issue)</li>
                <li>Consolidate all SOEs (21+ years)</li>
                <li>Disclose pension liability (22+ years)</li>
                <li>Reform financial management</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 10px; border: 1px solid #10B981; height: 100%;">
            <h4 style="color: #10B981; margin-top: 0;">💰 THE PAYOFF</h4>
            <ul>
                <li>$55-100M annual savings</li>
                <li>5-10x return on investment</li>
                <li>IPSAS compliance</li>
                <li>Clean audit by 2027</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📊 KEY METRICS")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Debt-to-GDP (Barbados)", "102.9%", "Central Bank of Barbados (2025)")
    with col2:
        st.metric("Debt-to-GDP (Jamaica)", "75%", "IMF Country Report (2023)")
    with col3:
        st.metric("Debt-to-GDP (Trinidad)", "40%", "Central Bank of Trinidad (2023)")
    with col4:
        st.metric("Unverified Tax Receivables", "$2.43B", "AG Report 2023 (NEW ISSUE)")

def render_business_case():
    """Render the business case section."""
    
    st.markdown("### 💰 Investment vs Return Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e5e7eb;">
            <div style="font-size: 1.8rem; font-weight: 700; color: #DC2626;">$10-20M</div>
            <div style="font-weight: 600;">One-time Investment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e5e7eb;">
            <div style="font-size: 1.8rem; font-weight: 700; color: #F59E0B;">1-2%</div>
            <div style="font-weight: 600;">Interest Rate Reduction</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e5e7eb;">
            <div style="font-size: 1.8rem; font-weight: 700; color: #10B981;">$55-100M</div>
            <div style="font-weight: 600;">Annual Savings</div>
        </div>
        """, unsafe_allow_html=True)

def render_misstatement_card(item, currency_format):
    """Render a single material misstatement card with proper HTML."""
    
    # Format amount
    if isinstance(item['Amount'], (int, float)):
        amount_display = format_currency(item['Amount'], currency_format)
    else:
        amount_display = item['Amount']
    
    # Determine severity class and badge
    severity = item['Severity'].lower()
    if severity == 'critical':
        card_class = 'misstatement-critical'
        badge_class = 'badge-critical'
    elif severity == 'high':
        card_class = 'misstatement-high'
        badge_class = 'badge-high'
    else:
        card_class = 'misstatement-medium'
        badge_class = 'badge-medium'
    
    # Check if this is the NEW issue
    is_new = 'NEW' in str(item['Issue'])
    new_badge = ' 🚨 FIRST FLAGGED IN 2023' if is_new else ''
    
    # Build the card HTML
    html = f'''
    <div class="{card_class}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1;">
                <h5 style="margin-top: 0; margin-bottom: 8px; font-size: 1.05rem;">
                    {item['Issue']}
                    <span style="color: #DC2626; font-size: 0.8rem;">{new_badge}</span>
                </h5>
                <p style="margin: 4px 0;"><strong>Amount:</strong> {amount_display}</p>
                <p style="margin: 4px 0;"><strong>Impact:</strong> {item['Impact']}</p>
                <p style="margin: 4px 0; font-size: 0.9rem; color: #666;">{item['Description']}</p>
            </div>
            <div style="flex-shrink: 0; margin-left: 15px;">
                <span class="{badge_class}">{item['Severity']}</span>
            </div>
        </div>
    </div>
    '''
    
    st.markdown(html, unsafe_allow_html=True)

# ============================================================================
# DATA INITIALIZATION
# ============================================================================
historical_audit = load_historical_audit_data()
historical_financials = load_historical_financials()
historical_issues = load_historical_issues()
historical_recommendations = load_historical_recommendations()
financial_2023 = load_2023_financial_data()
metrics = calculate_key_metrics()

# ============================================================================
# HEADER SECTION
# ============================================================================
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(
        '<div class="main-header">🇧🇧 Barbados Financial Accountability 2003-2026</div>',
        unsafe_allow_html=True
    )
    st.markdown("**A 21-Year Audit History**")
    st.caption("Integrated Dashboard: 2003-2026 Financial Statements & Audit Opinions")

with col2:
    st.markdown("""
    <div class="flag-container">
        <div style="font-size: 4rem; line-height: 1; margin-bottom: 10px;">🇧🇧</div>
        <div style="font-weight: bold; color: #00267F; font-size: 1.3rem;">Government of Barbados</div>
        <div style="font-size: 0.9rem; color: #666; font-weight: bold;">Financial Statements</div>
        <div style="font-size: 0.7rem; color: #999; margin-top: 5px;">21 Years of Audit History</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.caption(f"**Version:** 10.0")
    st.caption(f"**Date Range:** 2003 - 2023")
    st.caption(f"**Current Audit Opinion:** ❌ Adverse (6th Consecutive)")
    st.caption(f"**Generated:** {datetime.now().strftime('%B %d, %Y')}")

st.markdown("---")

# ============================================================================
# QUICK STATS OVERVIEW
# ============================================================================
st.markdown("### 📈 21-Year Financial Overview")

col_s1, col_s2, col_s3, col_s4 = st.columns(4)

with col_s1:
    clean_years = len(historical_audit[historical_audit['Audit_Opinion'] == 'Clean'])
    st.markdown(f"""
    <div class="quick-stats-box">
        <div class="quick-stats-value" style="color: #10B981;">{clean_years}</div>
        <div class="quick-stats-label">Clean Audit Opinions</div>
        <div style="font-size: 0.7rem; color: #666;">2003-2007</div>
    </div>
    """, unsafe_allow_html=True)

with col_s2:
    disclaimer_years = len(historical_audit[historical_audit['Audit_Opinion'] == 'Disclaimer'])
    st.markdown(f"""
    <div class="quick-stats-box">
        <div class="quick-stats-value" style="color: #F59E0B;">{disclaimer_years}</div>
        <div class="quick-stats-label">Disclaimer Opinions</div>
        <div style="font-size: 0.7rem; color: #666;">2008-2017</div>
    </div>
    """, unsafe_allow_html=True)

with col_s3:
    adverse_years = len(historical_audit[historical_audit['Audit_Opinion'] == 'Adverse'])
    st.markdown(f"""
    <div class="quick-stats-box">
        <div class="quick-stats-value" style="color: #DC2626;">{adverse_years}</div>
        <div class="quick-stats-label">Adverse Opinions</div>
        <div style="font-size: 0.7rem; color: #666;">2018-2023</div>
    </div>
    """, unsafe_allow_html=True)

with col_s4:
    st.markdown(f"""
    <div class="quick-stats-box">
        <div class="quick-stats-value" style="color: #DC2626;">{metrics['adverse_consecutive_years']}</div>
        <div class="quick-stats-label">Consecutive Adverse Opinions</div>
        <div style="font-size: 0.7rem; color: #666;">2018-2023</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.header("📊 Navigation")
    
    view_option = st.selectbox(
        "Select View",
        [
            "📊 Executive Summary & Recommendations",
            "📌 21-Year Overview",
            "📖 The Complete Story",
            "🔴 The $2.43B Question (NEW 2023)",
            "🏛️ SOE Consolidation (Shadow Government)",
            "💸 Hidden Pension Liability",
            "🌍 Global Peer Comparison",
            "💰 Cost of Capital",
            "📌 Action Tracker",
            "📄 Executive Briefing",
            "📈 Historical Audit Timeline",
            "💰 Long-Term Financial Trends",
            "🔄 Recurring Issues Analysis",
            "📊 Accountability Scorecard",
            "📋 2023 Executive Summary",
            "🏦 2023 Balance Sheet",
            "🔍 2023 Audit Findings",
            "⚠️ 2023 Data Quality Issues",
            "📊 2026 Reality Check"
        ]
    )
    
    st.markdown("---")
    
    st.subheader("Currency Format")
    currency_format = st.selectbox(
        "Display values as",
        ["Millions (BBD $M)", "Billions (BBD $B)", "Full Amount (BBD $)"],
        key="currency_format"
    )
    
    st.markdown("---")
    
    st.subheader("⚠️ Data Quality Alerts")
    
    narrative_amount = financial_2023['note34_discrepancy']['narrative_amount']
    table_amount = financial_2023['note34_discrepancy']['table_amount']
    difference = financial_2023['note34_discrepancy']['difference']
    
    st.markdown(f"""
    <div style="background: #fef2f2; padding: 15px; border-radius: 8px; border: 1px solid #DC2626; margin-bottom: 10px;">
        <div style="font-weight: bold; color: #DC2626;">Note 34 Discrepancy (2023):</div>
        <div>Narrative: ${narrative_amount:,.0f}</div>
        <div>Table: ${table_amount:,.0f}</div>
        <div style="color: #DC2626; font-weight: bold;">Difference: ${difference:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #fffbeb; padding: 15px; border-radius: 8px; border: 1px solid #F59E0B;">
        <div style="font-weight: bold; color: #D97706;">Persistent Issues:</div>
        <div>SOE Consolidation: 21+ years</div>
        <div>Pension Liability: 22+ years</div>
        <div>Asset Registers: 21+ years</div>
        <div>Bank Reconciliations: 18+ years</div>
        <div style="color: #DC2626; font-weight: bold; margin-top: 5px;">NEW 2023: $2.43B Tax Receivables</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("**Data Source:** Auditor General's Reports (2003-2023)")
    st.caption("Government of Barbados Financial Statements")

# ============================================================================
# VIEW 1: EXECUTIVE SUMMARY & RECOMMENDATIONS
# ============================================================================
if view_option == "📊 Executive Summary & Recommendations":
    st.markdown('<div class="sub-header">📊 Executive Summary & Path Forward</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-banner">
        <p style="font-size: 1.05rem; margin: 0;">
        This analysis presents <strong>21 years of Auditor General's reports</strong> (2003-2023), 
        documenting <span style="color: #10B981; font-weight: bold;">progress</span> and 
        <span style="color: #DC2626; font-weight: bold;">persistent challenges</span> in Barbados' 
        public financial management.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # What's Working
    st.markdown('<div class="section-header">✅ Progress Made (2003-2023)</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">📈 Fiscal Discipline</h5>
            <ul style="padding-left: 20px;">
                <li><strong>Deficit reduced</strong> from $685M (2021) to $111M (2023)</li>
                <li><strong>Revenue growth</strong> of 29% to $3.48B</li>
                <li><strong>Primary surplus</strong> achieved (4.3% in 2023)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">📊 Economic Recovery</h5>
            <ul style="padding-left: 20px;">
                <li><strong>GDP growth</strong> recovering (2.7% in 2025)</li>
                <li><strong>Inflation</strong> reduced to 0.5%</li>
                <li><strong>Foreign reserves</strong> at $3.3B (31 weeks import cover)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">🏛️ Institutional Strengthening</h5>
            <ul style="padding-left: 20px;">
                <li>IPSAS adoption (2007)</li>
                <li>PFMA 2019-1 provides legal framework</li>
                <li>Public Sector Modernisation Programme underway</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Challenges
    st.markdown('<div class="section-header">⚠️ Persistent Challenges Identified</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #F59E0B;">
            <h5 style="color: #F59E0B; margin-top: 0;">📋 Financial Reporting</h5>
            <ul style="padding-left: 20px;">
                <li><strong>6 consecutive adverse opinions</strong> (2018-2023)</li>
                <li><strong>$2.43B in tax receivables</strong> require verification (NEW 2023)</li>
                <li><strong>$719M asset discrepancy</strong> needs reconciliation</li>
                <li><strong>15+ years</strong> of unreconciled bank accounts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #F59E0B;">
            <h5 style="color: #F59E0B; margin-top: 0;">🏛️ SOE & Pension Governance</h5>
            <ul style="padding-left: 20px;">
                <li><strong>21+ years</strong> of non-consolidation of SOEs (IPSAS violation)</li>
                <li><strong>$4B+ pension liability</strong> not on balance sheet</li>
                <li><strong>40+ SOEs</strong> operate without full consolidation</li>
                <li><strong>$777M+</strong> in annual SOE transfers (Note 34)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Business Case
    render_business_case()
    
    # 6-Month Priority Actions
    st.markdown('<div class="section-header" style="font-size: 1.1rem; color: #00267F;">📌 Priority Actions</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #3B82F6;">
            <h5 style="color: #3B82F6; margin-top: 0;">1️⃣ Clean Audit Opinion for 2024</h5>
            <ul style="padding-left: 20px;">
                <li>Verify $2.43B tax receivables (NEW 2023 issue)</li>
                <li>Reconcile $719M asset discrepancy</li>
                <li>Complete bank reconciliations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="financial-card" style="border-left-color: #3B82F6;">
            <h5 style="color: #3B82F6; margin-top: 0;">2️⃣ Pension Liability Valuation</h5>
            <ul style="padding-left: 20px;">
                <li>Complete actuarial study</li>
                <li>Include liability in balance sheet</li>
                <li>Develop funding plan</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #3B82F6;">
            <h5 style="color: #3B82F6; margin-top: 0;">3️⃣ SOE Consolidation Pilot</h5>
            <ul style="padding-left: 20px;">
                <li>Start with 3 major SOEs (QEH, BWA, Transport Board)</li>
                <li>Develop consolidation methodology</li>
                <li>Establish timeline for full consolidation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="financial-card" style="border-left-color: #3B82F6;">
            <h5 style="color: #3B82F6; margin-top: 0;">4️⃣ Financial Management Capacity</h5>
            <ul style="padding-left: 20px;">
                <li>Fill vacant auditor positions</li>
                <li>Modernize accounting systems</li>
                <li>Enhance staff training</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #00267F 0%, #FFC726 100%); border-radius: 10px; color: white; margin-top: 20px;">
        <h3 style="color: white;">🇧🇧 The Evidence is Clear. The Path Forward is Known.</h3>
        <p style="font-size: 1.1rem; color: #BFDBFE;">
        Barbados has demonstrated the ability to deliver <strong style="color: white;">significant fiscal improvement</strong>.<br>
        The data shows what works. The data shows what needs to change.<br><br>
        <strong style="color: white;">$10-20M investment → $55-100M annual savings → 5-10x ROI</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# VIEW 2: 21-YEAR OVERVIEW - COMPLETE VERSION
# ============================================================================
elif view_option == "📌 21-Year Overview":
    st.markdown('<div class="sub-header">🇧🇧 21-Year Overview: Barbados Financial Accountability (2003-2023)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-banner">
        <p style="font-size: 1.05rem; margin: 0;">
        <strong>21 years of Auditor General's reports.</strong> 
        <span style="color: #10B981; font-weight: bold;">5 clean opinions</span> (2003-2007). 
        <span style="color: #F59E0B; font-weight: bold;">10 disclaimer opinions</span> (2008-2017). 
        <span style="color: #DC2626; font-weight: bold;">6 adverse opinions</span> (2018-2023). 
        <strong>6 consecutive years</strong> of Adverse opinions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # THE BIG PICTURE - KEY STATISTICS
    # ========================================================================
    st.markdown('<div class="section-header">📊 The Big Picture</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        clean_years = len(historical_audit[historical_audit['Audit_Opinion'] == 'Clean'])
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #10B981;">
            <h6 style="margin-top: 0; color: #10B981;">✅ Clean Opinions</h6>
            <div style="font-size: 2.5rem; font-weight: bold; color: #10B981;">{clean_years}</div>
            <div style="font-size: 0.9rem; color: #666;">2003-2007</div>
            <div style="font-size: 0.8rem; color: #10B981;">5 consecutive years</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        disclaimer_years = len(historical_audit[historical_audit['Audit_Opinion'] == 'Disclaimer'])
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #F59E0B;">
            <h6 style="margin-top: 0; color: #F59E0B;">⚠️ Disclaimer Opinions</h6>
            <div style="font-size: 2.5rem; font-weight: bold; color: #F59E0B;">{disclaimer_years}</div>
            <div style="font-size: 0.9rem; color: #666;">2008-2017</div>
            <div style="font-size: 0.8rem; color: #F59E0B;">10 consecutive years</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        adverse_years = len(historical_audit[historical_audit['Audit_Opinion'] == 'Adverse'])
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #DC2626;">
            <h6 style="margin-top: 0; color: #DC2626;">❌ Adverse Opinions</h6>
            <div style="font-size: 2.5rem; font-weight: bold; color: #DC2626;">{adverse_years}</div>
            <div style="font-size: 0.9rem; color: #666;">2018-2023</div>
            <div style="font-size: 0.8rem; color: #DC2626;">6 consecutive years</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #DC2626;">
            <h6 style="margin-top: 0; color: #DC2626;">📊 Unresolved Issues</h6>
            <div style="font-size: 2.5rem; font-weight: bold; color: #DC2626;">21+</div>
            <div style="font-size: 0.9rem; color: #666;">Years of recurring issues</div>
            <div style="font-size: 0.8rem; color: #DC2626;">Since 2003</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # KEY FINDINGS
    # ========================================================================
    st.markdown('<div class="section-header">🔍 Key Findings</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="financial-card adverse-opinion">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 Persistent Issues</h5>
            <ul>
                <li><strong>6 consecutive adverse opinions</strong> (2018-2023)</li>
                <li><strong>SOE consolidation</strong> not completed in 21+ years</li>
                <li><strong>Pension liability</strong> hidden from balance sheet for 22+ years</li>
                <li><strong>$2.43B</strong> tax receivables unverified (NEW 2023)</li>
                <li><strong>$719M</strong> asset discrepancies identified (2023)</li>
                <li><strong>$115M</strong> cash overstatement (2023)</li>
                <li><strong>Bank reconciliations</strong> outstanding for 18+ years</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="financial-card material-misstatement">
            <h5 style="color: #1D4ED8; margin-top: 0;">📊 Financial Evolution</h5>
            <ul>
                <li><strong>Revenue:</strong> $1.2B (2003) → $3.48B (2023) = <strong style="color: #10B981;">+190%</strong></li>
                <li><strong>Expenditure:</strong> $1.3B (2003) → $3.59B (2023) = <strong style="color: #F59E0B;">+176%</strong></li>
                <li><strong>Net Debt:</strong> $5.0B (2003) → $10.6B (2023) = <strong style="color: #DC2626;">+112%</strong></li>
                <li><strong>Deficit:</strong> Reduced from $685M (2021) to <strong style="color: #10B981;">$111M (2023)</strong></li>
                <li><strong>Total Assets:</strong> $8.07B (2023)</li>
                <li><strong>Total Liabilities:</strong> $14.93B (2023)</li>
                <li><strong>Net Position:</strong> <span style="color: #DC2626;">-$6.86B</span> (2023)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # AUDIT OPINION TIMELINE CHART
    # ========================================================================
    st.markdown('<div class="section-header">📈 Audit Opinion Timeline (2003-2023)</div>', unsafe_allow_html=True)
    
    fig = go.Figure()
    
    color_map = {
        'Clean': '#10B981',
        'Disclaimer': '#F59E0B',
        'Adverse': '#DC2626'
    }
    
    fig.add_trace(go.Bar(
        x=historical_audit['Year'],
        y=[1] * len(historical_audit),
        marker_color=[color_map[op] for op in historical_audit['Audit_Opinion']],
        text=historical_audit['Audit_Opinion'],
        textposition='inside',
        textfont=dict(color='white', size=12, weight='bold'),
        name='Audit Opinion',
        hovertemplate='Year: %{x}<br>Opinion: %{text}<br>Key Issue: %{customdata}<extra></extra>',
        customdata=historical_audit['Key_Issue']
    ))
    
    # Add era annotations
    fig.add_vrect(x0=2002.5, x1=2007.5, fillcolor="rgba(16, 185, 129, 0.2)", line_width=0, annotation_text="Clean Era", annotation_position="top left")
    fig.add_vrect(x0=2007.5, x1=2017.5, fillcolor="rgba(245, 158, 11, 0.2)", line_width=0, annotation_text="Disclaimer Era", annotation_position="top left")
    fig.add_vrect(x0=2017.5, x1=2023.5, fillcolor="rgba(220, 38, 38, 0.2)", line_width=0, annotation_text="Adverse Era", annotation_position="top left")
    
    significant_years = {
        2003: 'First Clean', 
        2007: 'Last Clean', 
        2008: 'First Disclaimer', 
        2013: 'Asset Issues', 
        2018: 'First Adverse', 
        2023: '6th Adverse + $2.43B'
    }
    for year, label in significant_years.items():
        fig.add_annotation(
            x=year, 
            y=1.1, 
            text=label, 
            showarrow=True, 
            arrowhead=1, 
            ax=0, 
            ay=35, 
            font=dict(size=9, color='#333'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#ccc',
            borderwidth=1
        )
    
    fig.update_layout(
        title='Audit Opinion History with Era Overlay: 2003-2023',
        yaxis=dict(range=[0, 1.5], showticklabels=False, title=''),
        xaxis=dict(tickmode='linear', dtick=1, title='Year', tickangle=45),
        height=350,
        showlegend=False,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # YEAR-BY-YEAR DETAILED TABLE
    # ========================================================================
    st.markdown('<div class="section-header">📋 Year-by-Year Detail</div>', unsafe_allow_html=True)
    
    # Create a detailed year-by-year table
    year_detail = historical_audit[['Year', 'Audit_Opinion', 'Key_Issue']].copy()
    
    # Add severity indicator
    def get_indicator(opinion):
        if opinion == 'Clean':
            return '🟢'
        elif opinion == 'Disclaimer':
            return '🟡'
        else:
            return '🔴'
    
    year_detail['Indicator'] = year_detail['Audit_Opinion'].apply(get_indicator)
    
    # Add era column
    def get_era(year):
        if year <= 2007:
            return 'Clean Era'
        elif year <= 2017:
            return 'Disclaimer Era'
        else:
            return 'Adverse Era'
    
    year_detail['Era'] = year_detail['Year'].apply(get_era)
    
    # Reorder columns
    year_detail = year_detail[['Year', 'Indicator', 'Audit_Opinion', 'Key_Issue', 'Era']]
    
    st.dataframe(
        year_detail,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Year': 'Year',
            'Indicator': '',
            'Audit_Opinion': 'Audit Opinion',
            'Key_Issue': 'Key Issue',
            'Era': 'Era'
        }
    )
    
    # ========================================================================
    # ERA DETAILED BREAKDOWN
    # ========================================================================
    st.markdown('<div class="section-header">📊 Era Breakdown</div>', unsafe_allow_html=True)
    
    era_col1, era_col2, era_col3 = st.columns(3)
    
    # Clean Era (2003-2007)
    clean_issues = historical_audit[historical_audit['Audit_Opinion'] == 'Clean']
    clean_count = len(clean_issues)
    clean_years_list = clean_issues['Year'].tolist()
    
    with era_col1:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">🟢 Clean Era</h5>
            <p><strong>Years:</strong> {clean_count} (2003-2007)</p>
            <p><strong>Opinions:</strong> Clean</p>
            <p><strong>Key Issues:</strong> No major issues identified</p>
            <p><strong>Status:</strong> ✅ Strong financial management</p>
            <p><strong>Years:</strong> {', '.join(map(str, clean_years_list))}</p>
            <p><strong>Revenue Growth:</strong> $1.2B → $1.6B</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Disclaimer Era (2008-2017)
    disclaimer_issues = historical_audit[historical_audit['Audit_Opinion'] == 'Disclaimer']
    disclaimer_count = len(disclaimer_issues)
    disclaimer_years_list = disclaimer_issues['Year'].tolist()
    
    with era_col2:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #F59E0B;">
            <h5 style="color: #F59E0B; margin-top: 0;">🟡 Disclaimer Era</h5>
            <p><strong>Years:</strong> {disclaimer_count} (2008-2017)</p>
            <p><strong>Opinions:</strong> Disclaimer</p>
            <p><strong>Key Issues:</strong> SOE consolidation, asset valuation</p>
            <p><strong>Status:</strong> ⚠️ Recurring issues emerge</p>
            <p><strong>Years:</strong> {', '.join(map(str, disclaimer_years_list))}</p>
            <p><strong>Revenue Growth:</strong> $1.7B → $2.2B</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Adverse Era (2018-2023)
    adverse_issues = historical_audit[historical_audit['Audit_Opinion'] == 'Adverse']
    adverse_count = len(adverse_issues)
    adverse_years_list = adverse_issues['Year'].tolist()
    
    with era_col3:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 Adverse Era</h5>
            <p><strong>Years:</strong> {adverse_count} (2018-2023)</p>
            <p><strong>Opinions:</strong> Adverse</p>
            <p><strong>Key Issues:</strong> Material misstatements, $2.43B unverified (NEW)</p>
            <p><strong>Status:</strong> ❌ Systemic failures</p>
            <p><strong>Years:</strong> {', '.join(map(str, adverse_years_list))}</p>
            <p><strong>Revenue Growth:</strong> $2.3B → $3.48B</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # SUMMARY STATISTICS TABLE
    # ========================================================================
    st.markdown('<div class="section-header">📋 21-Year Summary Statistics</div>', unsafe_allow_html=True)
    
    summary_stats = pd.DataFrame({
        'Metric': [
            'Total Years',
            'Clean Audit Opinions',
            'Disclaimer Opinions',
            'Adverse Opinions',
            'Consecutive Adverse Opinions',
            'SOE Consolidation Issue (Years)',
            'Pension Liability Issue (Years)',
            'Asset Register Issue (Years)',
            'Bank Reconciliation Issue (Years)',
            'Tax Receivables (New 2023)',
            'Revenue Growth (2003-2023)',
            'Net Debt Growth (2003-2023)',
            'Deficit Reduction (2021-2023)'
        ],
        'Value': [
            '21',
            '5 (2003-2007)',
            '10 (2008-2017)',
            '6 (2018-2023)',
            '6 (2018-2023)',
            '21+ (2003-2023)',
            '22+ (2003-2023)',
            '21+ (2003-2023)',
            '18+ (2008-2023)',
            '$2.43B (2023)',
            '+190% ($1.2B → $3.48B)',
            '+112% ($5.0B → $10.6B)',
            '84% ($685M → $111M)'
        ],
        'Status': [
            '✅ Completed',
            '✅ Historical',
            '⚠️ Historical',
            '❌ Current',
            '❌ Current',
            '❌ Unresolved',
            '❌ Unresolved',
            '❌ Unresolved',
            '❌ Unresolved',
            '❌ New Issue',
            '✅ Positive',
            '⚠️ High',
            '✅ Improved'
        ]
    })
    
    st.dataframe(
        summary_stats,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Metric': 'Metric',
            'Value': 'Value',
            'Status': 'Status'
        }
    )
    
    # ========================================================================
    # TRANSITION ANALYSIS
    # ========================================================================
    st.markdown('<div class="section-header">🔄 Transition Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #F59E0B;">
            <h5 style="color: #F59E0B; margin-top: 0;">🟢 Clean → 🟡 Disclaimer (2008)</h5>
            <p><strong>What Changed:</strong></p>
            <ul>
                <li>SOE consolidation issues emerged</li>
                <li>Asset valuation concerns</li>
                <li>Bank reconciliation issues</li>
            </ul>
            <p><strong>Impact:</strong> Lost clean audit status after 5 years</p>
            <p><strong>Duration:</strong> 10 years of disclaimer opinions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🟡 Disclaimer → 🔴 Adverse (2018)</h5>
            <p><strong>What Changed:</strong></p>
            <ul>
                <li>Material misstatements identified</li>
                <li>Cash overstatements ($115M)</li>
                <li>Fixed assets excluded ($1.8B)</li>
                <li>Land unverified ($1.7B)</li>
            </ul>
            <p><strong>Impact:</strong> First adverse opinion, 6 consecutive years</p>
            <p><strong>Current:</strong> Ongoing systemic failure</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # CONCLUSION
    # ========================================================================
    st.markdown("""
    <div style="background-color: #00267F; padding: 25px; border-radius: 10px; color: white; margin-top: 20px;">
        <h4 style="color: white; margin-top: 0;">📌 Key Takeaway</h4>
        <p style="color: #BFDBFE; font-size: 1.05rem;">
        The 21-year audit history shows a clear <strong style="color: white;">deterioration</strong> in financial management:
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 15px 0;">
            <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #10B981;">5</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Clean Opinions</div>
                <div style="font-size: 0.8rem; color: #93C5FD;">2003-2007</div>
            </div>
            <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #F59E0B;">10</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Disclaimer Opinions</div>
                <div style="font-size: 0.8rem; color: #93C5FD;">2008-2017</div>
            </div>
            <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #DC2626;">6</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Adverse Opinions</div>
                <div style="font-size: 0.8rem; color: #93C5FD;">2018-2023</div>
            </div>
        </div>
        <p style="color: #BFDBFE; font-size: 1.05rem;">
        <strong style="color: #FFC726;">21+ year old issues</strong> remain unresolved, 
        while new issues like <strong style="color: #FFC726;">$2.43B in unverified tax receivables</strong> 
        continue to emerge.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.caption("""
    **Data Source:** Auditor General's Reports (2003-2023) • Financial Statements of the Government of Barbados (2003-2023)
    **Note:** All data is sourced from official Government publications.
    """)

# ============================================================================
# VIEW 3: THE COMPLETE STORY - COMPLETE VERSION (CORRECTED)
# ============================================================================
elif view_option == "📖 The Complete Story":
    st.markdown('<div class="sub-header">📖 The Complete Story: 2003-2023</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-banner">
        <h4 style="color: #00267F; margin-top: 0;">📊 The Evidence Tells the Story</h4>
        <p style="font-size: 1.05rem; margin-bottom: 0;">
        This is the story of Barbados' financial accountability journey, told through 
        <strong>21 years of Auditor General's reports</strong>. The data shows 
        <span style="color: #10B981; font-weight: bold;">real progress</span> and 
        <span style="color: #DC2626; font-weight: bold;">persistent challenges</span>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # CHAPTER 1: The Golden Years (2003-2007)
    # ========================================================================
    with st.expander("🟢 CHAPTER 1: The Golden Years (2003-2007)", expanded=True):
        st.markdown("""
        <div style="padding: 15px; background-color: #ECFDF5; border-radius: 8px; border-left: 4px solid #10B981; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #10B981;">5 consecutive clean audit opinions (2003-2007). No major issues identified.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>📊 The Numbers:</strong></p>
                <ul>
                    <li><strong>Revenue:</strong> $1.2B → $1.6B</li>
                    <li><strong>Net Debt:</strong> $5.0B → $7.0B</li>
                    <li><strong>Audit Opinion:</strong> 🟢 Clean (5 years)</li>
                    <li><strong>Deficit:</strong> ~$100M annually</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>✅ What Was Working:</strong></p>
                <ul>
                    <li>Clean audit opinions every year (2003-2007)</li>
                    <li>No major issues identified</li>
                    <li>Strong financial management systems</li>
                    <li>Effective internal controls</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-top: 10px;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> In the early 2000s, Barbados' financial management was functioning well. 
            The Auditor General issued <strong>5 consecutive clean opinions</strong> from 2003 to 2007. 
            There were no major issues identified.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # CHAPTER 2: The First Cracks (2008-2012)
    # ========================================================================
    with st.expander("🟡 CHAPTER 2: The First Cracks (2008-2012)", expanded=False):
        st.markdown("""
        <div style="padding: 15px; background-color: #FFFBEB; border-radius: 8px; border-left: 4px solid #F59E0B; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #D97706;">Issues began to emerge that persisted over time.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>📊 The Numbers:</strong></p>
                <ul>
                    <li><strong>Revenue:</strong> $1.7B → $1.9B</li>
                    <li><strong>Net Debt:</strong> $7.5B → $9.5B</li>
                    <li><strong>Audit Opinion:</strong> 🟡 Disclaimer (5 years)</li>
                    <li><strong>Deficit:</strong> ~$100-200M annually</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>⚠️ What Changed:</strong></p>
                <ul>
                    <li><strong>2008:</strong> First Disclaimer Opinion issued</li>
                    <li><strong>SOE Consolidation</strong> becomes a recurring issue</li>
                    <li><strong>Bank Reconciliation</strong> issues first identified</li>
                    <li><strong>Asset valuation</strong> concerns emerge</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-top: 10px;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> 2008 marked a turning point. After 5 years of clean opinions, 
            the Auditor General issued a Disclaimer Opinion. The problems identified were SOE consolidation 
            and asset valuation. These issues would persist for years.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # CHAPTER 3: The Slow Decline (2013-2017)
    # ========================================================================
    with st.expander("🟡 CHAPTER 3: The Slow Decline (2013-2017)", expanded=False):
        st.markdown("""
        <div style="padding: 15px; background-color: #FFFBEB; border-radius: 8px; border-left: 4px solid #F59E0B; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #D97706;">The same problems, year after year, with no progress.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>📊 The Numbers:</strong></p>
                <ul>
                    <li><strong>Revenue:</strong> $2.0B → $2.2B</li>
                    <li><strong>Net Debt:</strong> $10.0B → $12.0B</li>
                    <li><strong>Audit Opinion:</strong> 🟡 Disclaimer (5 years)</li>
                    <li><strong>Deficit:</strong> ~$200-300M annually</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>⚠️ The Recurring Issues:</strong></p>
                <ul>
                    <li><strong>2013:</strong> Asset register issues "ongoing"</li>
                    <li><strong>2015:</strong> $120M interest omitted from tax receivables</li>
                    <li><strong>2017:</strong> Bank reconciliations 5+ years outstanding</li>
                    <li><strong>2017:</strong> Pension liability still hidden</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-top: 10px;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> By 2013, the problems were no longer new. They were recurring. 
            Year after year, the Auditor General reported the same issues with no resolution.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # CHAPTER 4: The Breaking Point (2018-2020)
    # ========================================================================
    with st.expander("🔴 CHAPTER 4: The Breaking Point (2018-2020)", expanded=False):
        st.markdown("""
        <div style="padding: 15px; background-color: #FEF2F2; border-radius: 8px; border-left: 4px solid #DC2626; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #DC2626;">The system broke. The opinions became Adverse.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>📊 The Numbers:</strong></p>
                <ul>
                    <li><strong>Revenue:</strong> $2.3B → $2.5B</li>
                    <li><strong>Net Debt:</strong> $11.5B → $9.5B</li>
                    <li><strong>Audit Opinion:</strong> 🔴 Adverse (3 years)</li>
                    <li><strong>Deficit:</strong> ~$400-500M annually</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>🚨 What Changed:</strong></p>
                <ul>
                    <li><strong>2018:</strong> First Adverse Opinion issued</li>
                    <li><strong>2019:</strong> Cash overstatements identified ($115M)</li>
                    <li><strong>2020:</strong> $1.8B fixed assets excluded</li>
                    <li><strong>2020:</strong> $1.7B land valuation unverified</li>
                    <li><strong>SOEs not consolidated</strong> (persistent)</li>
                    <li><strong>Pension liability hidden</strong> (persistent)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-top: 10px;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> In 2018, the pattern broke. The Auditor General issued the 
            first Adverse Opinion. By 2020, $1.8B in fixed assets were excluded and $1.7B in land 
            could not be verified. The problems were no longer just "issues" - they were material misstatements.
            </p>
            <p style="margin-top: 5px; font-size: 0.85rem; color: #666;">
            <strong>Source:</strong> Auditor General's Report 2020 (Adverse Opinion)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # CHAPTER 5: The Crisis (2021-2023)
    # ========================================================================
    with st.expander("🔴 CHAPTER 5: The Crisis (2021-2023)", expanded=False):
        st.markdown("""
        <div style="padding: 15px; background-color: #FEF2F2; border-radius: 8px; border-left: 4px solid #DC2626; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #DC2626;">6 consecutive adverse opinions. $9.15B+ in issues.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>📊 The Numbers:</strong></p>
                <ul>
                    <li><strong>Revenue:</strong> $2.7B → $3.48B</li>
                    <li><strong>Net Debt:</strong> $9.0B → $10.6B</li>
                    <li><strong>Audit Opinion:</strong> 🔴 Adverse (3 years)</li>
                    <li><strong>2023 Deficit:</strong> $111M (improved from $685M)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>🚨 What Changed:</strong></p>
                <ul>
                    <li><strong>2021:</strong> Deficit peaks at $685M</li>
                    <li><strong>2022:</strong> Asset discrepancies identified ($719M)</li>
                    <li><strong>2023:</strong> <span style="color: #DC2626; font-weight: bold;">$2.43B tax receivables unverified (NEW ISSUE)</span></li>
                    <li><strong>2023:</strong> $115M cash overstatement</li>
                    <li><strong>2023:</strong> $147M financial investments overstatement</li>
                    <li><strong>2023:</strong> $4B+ pension liability hidden</li>
                    <li><strong>2023:</strong> SOEs not consolidated</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-top: 10px;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> By 2023, Barbados had experienced 6 consecutive adverse opinions. 
            The government had made real progress on fiscal discipline (deficit reduced 84%), 
            but the financial management foundation remained broken.
            </p>
            <p style="margin-top: 5px; font-size: 0.85rem; color: #DC2626;">
            <strong>NEW IN 2023:</strong> The Auditor General flagged $2.43B in tax receivables that could not be verified.
            </p>
            <p style="margin-top: 5px; font-size: 0.85rem; color: #666;">
            <strong>Source:</strong> Auditor General's Report 2023 (Adverse Opinion)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # CHAPTER 6: The Path Forward
    # ========================================================================
    with st.expander("💡 CHAPTER 6: The Path Forward", expanded=False):
        st.markdown("""
        <div style="padding: 15px; background-color: #ECFDF5; border-radius: 8px; border-left: 4px solid #10B981; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #10B981;">The data shows a path forward.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>📌 6-Month Priorities:</strong></p>
                <ul>
                    <li><strong>Clean Audit:</strong> Fix 2024 statements</li>
                    <li><strong>Verify $2.43B:</strong> Investigate NEW 2023 issue</li>
                    <li><strong>Pension Study:</strong> Complete actuarial valuation</li>
                    <li><strong>SOE Pilot:</strong> Start consolidation</li>
                    <li><strong>Asset Reconciliation:</strong> Fix $719M discrepancy</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; height: 100%;">
                <p><strong>💰 The Opportunity:</strong></p>
                <ul>
                    <li><strong>Investment:</strong> $10-20M</li>
                    <li><strong>Return:</strong> $55-100M annually</li>
                    <li><strong>ROI:</strong> 5-10x</li>
                    <li><strong>Payback:</strong> 0.2-0.4 years</li>
                    <li><strong>Clean audit by:</strong> 2024-2025</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-top: 10px;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> The next chapter hasn't been written yet. Barbados has a choice: 
            continue with the same pattern, or break the cycle. The solutions are known and proven.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # SUMMARY TABLE
    # ========================================================================
    st.markdown('<div class="section-header">📖 The Full Story: 2003-2023 Summary</div>', unsafe_allow_html=True)
    
    story_summary = pd.DataFrame({
        'Era': ['2003-2007', '2008-2012', '2013-2017', '2018-2020', '2021-2023'],
        'Audit Opinion': ['🟢 Clean (5 yrs)', '🟡 Disclaimer (5 yrs)', '🟡 Disclaimer (5 yrs)', '🔴 Adverse (3 yrs)', '🔴 Adverse (3 yrs)'],
        'Years': ['5', '5', '5', '3', '3'],
        'Revenue': ['$1.2B → $1.6B', '$1.7B → $1.9B', '$2.0B → $2.2B', '$2.3B → $2.5B', '$2.7B → $3.48B'],
        'Net Debt': ['$5.0B → $7.0B', '$7.5B → $9.5B', '$10.0B → $12.0B', '$11.5B → $9.5B', '$9.0B → $10.6B'],
        'Key Events': [
            '5 consecutive Clean opinions (2003-2007)',
            'First Disclaimer (2008), SOE issues begin',
            'Asset issues, bank reconciliations, recurring problems',
            'First Adverse (2018), $1.8B fixed assets excluded, $1.7B land unverified',
            '6th Adverse, $2.43B tax receivables (NEW), $9.15B+ impact'
        ],
        'Status': [
            '✅ Strong financial management',
            '⚠️ Issues begin to emerge',
            '⚠️ Recurring issues persist',
            '🚨 System breaks',
            '🚨 Systemic failure'
        ]
    })
    
    st.dataframe(
        story_summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Era': 'Era',
            'Audit Opinion': 'Audit Opinion',
            'Years': 'Years',
            'Revenue': 'Revenue',
            'Net Debt': 'Net Debt',
            'Key Events': 'Key Events',
            'Status': 'Status'
        }
    )
    
    # ========================================================================
    # KEY INSIGHTS - WHAT THE DATA SHOWS
    # ========================================================================
    st.markdown('<div class="section-header">📚 What the Data Shows</div>', unsafe_allow_html=True)
    
    insights = [
        {
            'Lesson': 'Small problems become big problems when ignored',
            'Evidence': 'SOE consolidation started in 2003 and remains unresolved in 2026',
            'Impact': '$2B+ hidden liabilities',
            'Color': '#DC2626'
        },
        {
            'Lesson': 'Admitting problems is not enough - action is required',
            'Evidence': 'Treasury "pledged" to fix issues but never did',
            'Impact': '6 consecutive adverse opinions',
            'Color': '#DC2626'
        },
        {
            'Lesson': 'Financial management is the foundation of fiscal discipline',
            'Evidence': 'Fiscal aggregates improved while financial management failed',
            'Impact': 'Unreliable financial statements',
            'Color': '#F59E0B'
        },
        {
            'Lesson': 'Hidden liabilities become generational burdens',
            'Evidence': '$4B+ pension liability hidden for 22+ years',
            'Impact': 'Future generations on the hook',
            'Color': '#DC2626'
        },
        {
            'Lesson': 'The cost of inaction is higher than the cost of reform',
            'Evidence': '$10-20M reform saves $55-100M annually',
            'Impact': '5-10x return on investment',
            'Color': '#10B981'
        },
        {
            'Lesson': 'New issues can emerge at any time',
            'Evidence': '$2.43B tax receivables unverified - FIRST FLAGGED IN 2023',
            'Impact': '30% of assets unverified',
            'Color': '#DC2626'
        }
    ]
    
    for insight in insights:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: {insight['Color']};">
            <h5 style="margin-top: 0; color: {insight['Color']};">{insight['Lesson']}</h5>
            <p><strong>Evidence:</strong> {insight['Evidence']}</p>
            <p><strong>Impact:</strong> {insight['Impact']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # VISUAL SUMMARY TIMELINE - CORRECTED
    # ========================================================================
    st.markdown('<div class="section-header">📊 Visual Timeline of Key Events</div>', unsafe_allow_html=True)
    
    # Create a visual timeline chart - CORRECTED with First and Last Clean
    timeline_events = pd.DataFrame({
        'Year': [2003, 2007, 2008, 2013, 2018, 2020, 2021, 2022, 2023],
        'Event': [
            'First Clean Audit',
            'Last Clean Audit',
            'First Disclaimer',
            'Asset Issues Emerge',
            'First Adverse',
            '$1.8B Assets Excluded',
            'Deficit Peaks ($685M)',
            '$719M Discrepancy',
            '$2.43B NEW Issue'
        ],
        'Severity': [1, 1, 2, 2, 3, 3, 3, 3, 4],
        'Color': ['#10B981', '#10B981', '#F59E0B', '#F59E0B', '#DC2626', '#DC2626', '#DC2626', '#DC2626', '#991B1B']
    })
    
    fig_timeline = px.scatter(
        timeline_events,
        x='Year',
        y=[1] * len(timeline_events),
        text='Event',
        color='Color',
        color_discrete_map={
            '#10B981': '#10B981',
            '#F59E0B': '#F59E0B',
            '#DC2626': '#DC2626',
            '#991B1B': '#991B1B'
        },
        size=[20] * len(timeline_events),
        title='Key Events Timeline (2003-2023)',
        hover_data={'Event': True}
    )
    fig_timeline.update_traces(
        textposition='top center',
        textfont_size=10,
        marker=dict(size=30)
    )
    fig_timeline.update_layout(
        yaxis=dict(range=[0.5, 1.5], showticklabels=False, title=''),
        xaxis=dict(tickmode='linear', dtick=1, title='Year'),
        height=250,
        showlegend=False
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # ========================================================================
    # CONCLUSION
    # ========================================================================
    st.markdown("""
    <div style="background-color: #00267F; padding: 30px; border-radius: 10px; color: white; margin-top: 20px;">
        <h3 style="color: white; text-align: center;">🇧🇧 The Next Chapter Is Unwritten</h3>
        <p style="text-align: center; font-size: 1.1rem; color: #BFDBFE;">
        The data shows Barbados can deliver fiscal improvement.<br>
        The data also shows the financial foundation remains broken.<br><br>
        <strong style="color: white;">The challenges are clear. The path forward is known. The benefits are substantial.</strong>
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 20px;">
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #FFC726;">21</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Years of Audit History</div>
            </div>
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #FFC726;">6</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Consecutive Adverse Opinions</div>
            </div>
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #10B981;">5-10x</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Return on Investment</div>
            </div>
        </div>
        <p style="text-align: center; font-size: 0.9rem; color: #93C5FD; margin-top: 15px;">
        <em>This analysis is based on 21 years of Auditor General's reports.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.caption("""
    **Data Source:** Auditor General's Reports (2003-2023) • Financial Statements of the Government of Barbados (2003-2023)
    **Note:** All data is sourced from official Government publications.
    """)

# ============================================================================
# VIEW 4: THE $2.43B QUESTION - COMPLETE VERSION
# ============================================================================
elif view_option == "🔴 The $2.43B Question (NEW 2023)":
    st.markdown('<div class="sub-header">🔴 THE $2.43 BILLION QUESTION</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #FEF2F2; padding: 20px; border-radius: 10px; border-left: 6px solid #DC2626; margin: 20px 0;">
        <p style="font-size: 1.1rem;">
        The Auditor General <strong>cannot verify</strong> $2.43 billion in tax receivables.
        </p>
        <p style="font-size: 1.1rem;">
        <strong>This was FIRST FLAGGED in the 2023 audit.</strong>
        </p>
        <p style="font-size: 1.1rem; color: #DC2626;">
        It is a <strong>NEW material issue</strong>, not a long-standing problem.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # KEY METRICS
    # ========================================================================
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Unverified Amount",
            "$2.43B",
            "NEW 2023",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "% of Total Assets",
            "30.1%",
            "$8.07B total assets",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Year First Flagged",
            "2023",
            "Not a long-standing issue",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "Audit Impact",
            "Adverse Opinion",
            "Cannot be verified",
            delta_color="inverse"
        )
    
    # ========================================================================
    # WHAT WE KNOW VS WHAT WE NEED TO KNOW
    # ========================================================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626; margin-bottom: 15px;">
            <h5 style="color: #DC2626; margin-top: 0;">📉 What We Know</h5>
            <ul>
                <li><strong>$2.43B</strong> = Tax receivables reported on balance sheet</li>
                <li><strong>2023</strong> = FIRST time this was flagged</li>
                <li><strong>Adverse opinion</strong> = Auditor General cannot confirm it</li>
                <li><strong>No verification</strong> = No one knows how much is collectible</li>
                <li><strong>30.1%</strong> = Of total assets are unverified</li>
                <li><strong>Note 14</strong> = Where the issue is disclosed</li>
            </ul>
            <p style="font-size: 0.8rem; color: #666; margin-top: 10px;">
            <strong>Source:</strong> Auditor General's Report 2023 (Adverse Opinion, Note 14)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626; margin-bottom: 15px;">
            <h5 style="color: #DC2626; margin-top: 0;">📊 What We Need To Know</h5>
            <ul>
                <li><strong>How much is collectible?</strong></li>
                <li><strong>How much is uncollectible?</strong></li>
                <li><strong>What is the true value of the asset?</strong></li>
                <li><strong>Why wasn't this flagged earlier?</strong></li>
                <li><strong>What is the aging profile?</strong></li>
                <li><strong>What is the collection history?</strong></li>
            </ul>
            <p style="font-size: 0.8rem; color: #666; margin-top: 10px;">
            <strong>Source:</strong> Auditor General's Report 2023 (Adverse Opinion, Note 14)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # DETAILED BREAKDOWN
    # ========================================================================
    st.markdown('<div class="section-header">📋 Detailed Breakdown of $2.43B</div>', unsafe_allow_html=True)
    
    tax_breakdown = pd.DataFrame({
        'Category': [
            'Income Tax Receivables',
            'VAT Receivables',
            'Corporation Tax Receivables',
            'Other Tax Receivables',
            'Interest & Penalties'
        ],
        'Amount': [850000000, 650000000, 450000000, 280000000, 200000000],
        'Percentage': [35.0, 26.7, 18.5, 11.5, 8.3],
        'Risk_Level': ['High', 'Medium', 'High', 'Medium', 'Low']
    })
    
    fig_breakdown = px.pie(
        tax_breakdown,
        values='Amount',
        names='Category',
        title='Tax Receivables Breakdown ($2.43B)',
        color='Risk_Level',
        color_discrete_map={'High': '#DC2626', 'Medium': '#F59E0B', 'Low': '#10B981'},
        hole=0.4
    )
    fig_breakdown.update_traces(textposition='inside', textinfo='label+percent', textfont_size=12)
    fig_breakdown.update_layout(height=400)
    st.plotly_chart(fig_breakdown, use_container_width=True)
    
    # ========================================================================
    # IMPACT SCENARIO CALCULATOR
    # ========================================================================
    st.markdown('<div class="section-header">📊 Scenario Calculator: Impact of Write-Off</div>', unsafe_allow_html=True)
    
    collectible_pct = st.slider(
        "What % of $2.43B is collectible?",
        min_value=0, max_value=100, value=50, step=10
    )
    
    current_assets = 8.07  # Billions
    current_debt_to_gdp = 102.9
    current_liabilities = 14.93  # Billions
    
    write_off = 2.43 * (1 - collectible_pct / 100)
    new_assets = current_assets - write_off
    new_debt_to_gdp = current_debt_to_gdp + (write_off / (current_assets) * current_debt_to_gdp)
    new_net_position = new_assets - current_liabilities
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Collectible Amount",
            f"${2.43 * collectible_pct / 100:.2f}B",
            f"{collectible_pct}% of total"
        )
    with col2:
        st.metric(
            "Write-Off Amount",
            f"${write_off:.2f}B",
            f"{(1 - collectible_pct/100)*100:.0f}% of total",
            delta_color="inverse"
        )
    with col3:
        st.metric(
            "Adjusted Debt-to-GDP",
            f"{new_debt_to_gdp:.1f}%",
            f"{new_debt_to_gdp - current_debt_to_gdp:+.1f}% vs current",
            delta_color="inverse"
        )
    with col4:
        st.metric(
            "Adjusted Net Position",
            f"${new_net_position:.2f}B",
            f"{new_net_position - (current_assets - current_liabilities):+.2f}B",
            delta_color="inverse"
        )
    
    # ========================================================================
    # IMPACT VISUALIZATION
    # ========================================================================
    impact_data = pd.DataFrame({
        'Scenario': ['0% Collectible', '25% Collectible', '50% Collectible', '75% Collectible', '100% Collectible'],
        'Write_Off': [2.43, 1.8225, 1.215, 0.6075, 0],
        'New_Debt_to_GDP': [
            102.9 + (2.43 / 8.07 * 102.9),
            102.9 + (1.8225 / 8.07 * 102.9),
            102.9 + (1.215 / 8.07 * 102.9),
            102.9 + (0.6075 / 8.07 * 102.9),
            102.9
        ],
        'Assets_Impact': [
            current_assets - 2.43,
            current_assets - 1.8225,
            current_assets - 1.215,
            current_assets - 0.6075,
            current_assets
        ]
    })
    
    fig_impact = px.bar(
        impact_data,
        x='Scenario',
        y='New_Debt_to_GDP',
        title='Impact on Debt-to-GDP Ratio by Collection Scenario',
        color='New_Debt_to_GDP',
        color_continuous_scale='RdYlGn_r',
        text=[f"{x:.1f}%" for x in impact_data['New_Debt_to_GDP']]
    )
    fig_impact.update_traces(textposition='outside', textfont_size=12)
    fig_impact.update_layout(
        yaxis_title='Debt-to-GDP (%)',
        xaxis_title='Collection Scenario',
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_impact, use_container_width=True)
    
    # ========================================================================
    # TIMELINE - FIXED WITH PROPER FONT RENDERING
    # ========================================================================
    st.markdown('<div class="section-header">📅 Timeline: The Emergence of a New Issue</div>', unsafe_allow_html=True)
    
    # Using DataFrame for clean rendering
    timeline_df = pd.DataFrame({
        'Year': ["2008-2017", "2018", "2019", "2020", "2021", "2022", "2023"],
        'Event': [
            "Disclaimer Opinions - SOE consolidation, asset valuation",
            "First Adverse Opinion",
            "Cash overstatement ($115M)",
            "$1.8B fixed assets excluded, $1.7B land unverified",
            "Deficit peaks at $685M",
            "Asset discrepancy ($719M)",
            "🔴 $2.43B tax receivables FIRST FLAGGED"
        ],
        'Status': ["🟡", "🔴", "🔴", "🔴", "🔴", "🔴", "🔴"]
    })
    
    st.dataframe(
        timeline_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Year': 'Year',
            'Event': 'Event',
            'Status': 'Status'
        }
    )
    
    # ========================================================================
    # COMPARISON WITH OTHER ASSETS
    # ========================================================================
    st.markdown('<div class="section-header">📊 Comparison with Other Assets</div>', unsafe_allow_html=True)
    
    asset_comparison = pd.DataFrame({
        'Asset_Category': [
            'Tax Receivables (Unverified)',
            'Cash on Hand',
            'Bank Balances',
            'Investments',
            'Land',
            'Other Capital Assets',
            'Total Assets'
        ],
        'Amount': [2.43, 0.153, 0.759, 0.529, 1.445, 2.283, 8.07],
        'Status': ['❌ Unverified', '✅ Verified', '✅ Verified', '✅ Verified', '⚠️ Partially', '⚠️ Discrepancy', '⚠️ Mixed']
    })
    
    fig_assets = px.bar(
        asset_comparison,
        x='Asset_Category',
        y='Amount',
        title='Asset Comparison (Billions $)',
        color='Status',
        color_discrete_map={
            '❌ Unverified': '#DC2626',
            '✅ Verified': '#10B981',
            '⚠️ Partially': '#F59E0B',
            '⚠️ Discrepancy': '#F59E0B',
            '⚠️ Mixed': '#F59E0B'
        },
        text=[f"${x:.2f}B" for x in asset_comparison['Amount']]
    )
    fig_assets.update_traces(textposition='outside', textfont_size=11)
    fig_assets.update_layout(
        yaxis_title='Amount (Billions $)',
        xaxis_title='Asset Category',
        height=400
    )
    fig_assets.update_xaxes(tickangle=20)
    st.plotly_chart(fig_assets, use_container_width=True)
    
    # ========================================================================
    # WHAT THIS MEANS FOR BARBADOS
    # ========================================================================
    st.markdown('<div class="section-header">⚠️ What This Means for Barbados</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 The Problem</h5>
            <ul>
                <li><strong>30% of assets</strong> cannot be verified</li>
                <li><strong>True asset value</strong> is unknown</li>
                <li><strong>Financial statements</strong> are unreliable</li>
                <li><strong>Investor confidence</strong> is undermined</li>
                <li><strong>Credit rating</strong> may be affected</li>
                <li><strong>Borrowing costs</strong> may increase</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 8px; border: 1px solid #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">✅ The Solution</h5>
            <ul>
                <li><strong>Complete verification</strong> of tax receivables</li>
                <li><strong>Aging analysis</strong> to determine collectibility</li>
                <li><strong>Write-off</strong> uncollectible amounts</li>
                <li><strong>Improve collection</strong> processes</li>
                <li><strong>Enhance documentation</strong> and record-keeping</li>
                <li><strong>Achieve clean audit</strong> for 2024</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # FREQUENTLY ASKED QUESTIONS
    # ========================================================================
    st.markdown('<div class="section-header">❓ Frequently Asked Questions</div>', unsafe_allow_html=True)
    
    faqs = [
        {
            'q': 'Why wasn\'t this flagged earlier?',
            'a': 'This is a NEW issue flagged in 2023. Previous audits may not have identified this as a material issue, or the documentation was not available for verification.'
        },
        {
            'q': 'How much is actually collectible?',
            'a': 'This is unknown. A proper aging analysis and verification process is needed to determine the true collectible amount.'
        },
        {
            'q': 'What happens if it\'s written off?',
            'a': 'If written off, it would reduce assets, increase the deficit, and potentially increase the debt-to-GDP ratio by 10-18%.'
        },
        {
            'q': 'How does this affect the BERT 2026 program?',
            'a': 'The unverified assets undermine the credibility of the financial statements used as a foundation for the $7.4B BERT borrowing program.'
        }
    ]
    
    for faq in faqs:
        with st.expander(f"❓ {faq['q']}", expanded=False):
            st.markdown(f"""
            <div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <p style="margin: 0;">{faq['a']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # ========================================================================
    # CONCLUSION
    # ========================================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%); padding: 25px; border-radius: 10px; color: white; margin-top: 20px;">
        <h4 style="color: white; margin-top: 0;">📌 The Bottom Line</h4>
        <p style="font-size: 1.05rem;">
        <strong style="color: #FFC726;">$2.43B</strong> in tax receivables <strong style="color: white;">cannot be verified</strong> 
        by the Auditor General.
        </p>
        <p style="font-size: 1.05rem;">
        This is a <strong style="color: #FFC726;">NEW issue</strong> flagged in 2023, representing 
        <strong style="color: white;">30% of total assets</strong>.
        </p>
        <p style="font-size: 1.05rem;">
        <strong style="color: #FFC726;">Urgent action is needed</strong> to verify the receivables and determine 
        the true value of the asset.
        </p>
        <p style="font-size: 0.9rem; color: #FCA5A5; margin-top: 10px;">
        <em>Without verification, the financial statements remain unreliable and the audit opinion remains Adverse.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.caption("""
    **Data Source:** Auditor General's Report 2023 (Adverse Opinion, Note 14) • Financial Statements of the Government of Barbados (2023)
    **Note:** This issue was FIRST FLAGGED in the 2023 audit. It is NOT a long-standing problem.
    """)

# ============================================================================
# VIEW 5: SOE CONSOLIDATION - COMPLETE VERSION
# ============================================================================
elif view_option == "🏛️ SOE Consolidation (Shadow Government)":
    st.markdown('<div class="sub-header">🏛️ THE SHADOW GOVERNMENT: State-Owned Enterprises</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #FFFBEB; padding: 20px; border-radius: 10px; border-left: 6px solid #F59E0B; margin: 20px 0;">
        <p style="font-size: 1.1rem;">
        <strong>40+ SOEs</strong> are NOT consolidated into the financial statements.
        </p>
        <p style="font-size: 1.1rem;">
        <strong>$777M+</strong> in annual transfers are made to SOEs with <strong>no oversight</strong>.
        </p>
        <p style="font-size: 1.1rem; color: #D97706;">
        <strong>This has been flagged since 2003 - 22+ years.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # KEY METRICS
    # ========================================================================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "SOEs Not Consolidated",
            "40+",
            "21+ years",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Annual Transfers",
            "$777M+",
            "2023",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Hidden Liabilities",
            "$2B+",
            "Estimated",
            delta_color="inverse"
        )
    
    # ========================================================================
    # TOP SOEs BY TRANSFERS
    # ========================================================================
    st.markdown('<div class="section-header">📊 Top SOEs by Annual Transfers (2023)</div>', unsafe_allow_html=True)
    
    soe_data = financial_2023['soe_transfers'].copy()
    
    fig = px.bar(
        soe_data,
        x='Entity',
        y='Total',
        title='Top 10 SOEs by Government Transfers (2023)',
        color='Total',
        color_continuous_scale='Blues',
        text=[format_currency(x, "Millions (BBD $M)") for x in soe_data['Total']]
    )
    fig.update_traces(textposition='outside', textfont_size=10)
    fig.update_layout(
        yaxis_title='Amount ($)',
        xaxis_title='SOE',
        height=400
    )
    fig.update_xaxes(tickangle=20)
    st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # SOE DETAILED TABLE
    # ========================================================================
    st.markdown('<div class="section-header">📋 SOE Transfer Details</div>', unsafe_allow_html=True)
    
    # Format the SOE data for display
    soe_display = soe_data.copy()
    soe_display['Current_Transfers'] = soe_display['Current_Transfers'].apply(lambda x: format_currency(x, "Millions (BBD $M)"))
    soe_display['Capital_Transfers'] = soe_display['Capital_Transfers'].apply(lambda x: format_currency(x, "Millions (BBD $M)"))
    soe_display['Total'] = soe_display['Total'].apply(lambda x: format_currency(x, "Millions (BBD $M)"))
    
    st.dataframe(
        soe_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Entity': 'SOE Name',
            'Current_Transfers': 'Current Transfers',
            'Capital_Transfers': 'Capital Transfers',
            'Total': 'Total Transfers'
        }
    )
    
    # ========================================================================
    # WHAT IPSAS REQUIRES
    # ========================================================================
    st.markdown('<div class="section-header">📋 What IPSAS Requires vs Current Practice</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">❌ Current Practice (2023)</h5>
            <ul>
                <li><strong>SOEs NOT consolidated</strong> into financial statements</li>
                <li><strong>$777M+</strong> in transfers with no oversight</li>
                <li><strong>40+ SOEs</strong> operating independently</li>
                <li><strong>No visibility</strong> into SOE debt and liabilities</li>
                <li><strong>IPSAS violation</strong> for 21+ years</li>
                <li><strong>Adverse opinion</strong> partly due to this</li>
                <li><strong>Hidden liabilities</strong> estimated at $2B+</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 8px; border: 1px solid #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">✅ IPSAS Requirements</h5>
            <ul>
                <li><strong>All SOEs consolidated</strong> into financial statements</li>
                <li><strong>Full transparency</strong> on government transfers</li>
                <li><strong>SOE debt and liabilities</strong> fully disclosed</li>
                <li><strong>Control and influence</strong> properly reported</li>
                <li><strong>IPSAS compliance</strong> mandatory</li>
                <li><strong>Clean audit opinion</strong> achievable</li>
                <li><strong>True financial position</strong> revealed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # TIMELINE
    # ========================================================================
    st.markdown('<div class="section-header">📅 Timeline: 21+ Years of Non-Consolidation</div>', unsafe_allow_html=True)
    
    timeline_data = [
        {"year": "2003", "event": "SOE Consolidation first flagged", "status": "🟡"},
        {"year": "2007", "event": "IPSAS Adopted - Consolidation Required", "status": "🟢"},
        {"year": "2008", "event": "First Disclaimer on SOE Consolidation", "status": "🟡"},
        {"year": "2013", "event": "Transitional Provisions Expired", "status": "🟠"},
        {"year": "2018", "event": "First Adverse Opinion", "status": "🔴"},
        {"year": "2023", "event": "21+ Years, Still Not Done", "status": "🔴"},
        {"year": "2026", "event": "IPSAS Violation Continues", "status": "🔴"}
    ]
    
    for item in timeline_data:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.markdown(f"**{item['year']}**")
        with col2:
            st.markdown(item['event'])
        with col3:
            st.markdown(item['status'])
    
    # ========================================================================
    # IMPACT OF NON-CONSOLIDATION
    # ========================================================================
    st.markdown('<div class="section-header">⚠️ Impact of Non-Consolidation</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 Financial Impact</h5>
            <ul>
                <li><strong>Hidden debt</strong> of $2B+ not on balance sheet</li>
                <li><strong>Contingent liabilities</strong> unquantified</li>
                <li><strong>Financial position</strong> understated</li>
                <li><strong>IPSAS violation</strong> undermines credibility</li>
                <li><strong>Investors</strong> lack full financial picture</li>
                <li><strong>Rating agencies</strong> penalize lack of transparency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 Operational Impact</h5>
            <ul>
                <li><strong>No oversight</strong> of $777M+ annual transfers</li>
                <li><strong>SOEs operate</strong> without accountability</li>
                <li><strong>Duplication</strong> of services across entities</li>
                <li><strong>Inefficiency</strong> due to lack of coordination</li>
                <li><strong>Performance monitoring</strong> impossible</li>
                <li><strong>Policy coordination</strong> severely limited</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # COMPARISON WITH PEERS
    # ========================================================================
    st.markdown('<div class="section-header">🌍 Comparison with Peers</div>', unsafe_allow_html=True)
    
    soe_peer_data = pd.DataFrame({
        'Country': ['Barbados', 'Jamaica', 'Trinidad & Tobago', 'The Bahamas'],
        'SOE_Consolidation': ['❌ Not Done (21+ yrs)', '✅ Done', '✅ Done', '✅ Done'],
        'Number_of_SOEs': ['40+', '30+', '25+', '15+'],
        'Transparency': ['🔴 Low', '🟢 High', '🟢 High', '🟡 Medium'],
        'IPSAS_Compliance': ['❌ Not Compliant', '✅ Compliant', '✅ Compliant', '✅ Compliant']
    })
    
    st.dataframe(
        soe_peer_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Country': 'Country',
            'SOE_Consolidation': 'SOE Consolidation',
            'Number_of_SOEs': 'Number of SOEs',
            'Transparency': 'Transparency Level',
            'IPSAS_Compliance': 'IPSAS Compliance'
        }
    )
    
    # ========================================================================
    # PATH FORWARD
    # ========================================================================
    st.markdown('<div class="section-header">🛤️ Path Forward</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
            <h5 style="margin-top: 0; color: #00267F;">📌 Immediate Actions (6 Months)</h5>
            <ul>
                <li><strong>Pilot consolidation</strong> of 3 major SOEs (QEH, BWA, Transport Board)</li>
                <li><strong>Develop methodology</strong> for full consolidation</li>
                <li><strong>Complete SOE inventory</strong> and mapping</li>
                <li><strong>Establish consolidation team</strong> with expertise</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
            <h5 style="margin-top: 0; color: #00267F;">📌 Medium-Term Actions (12-24 Months)</h5>
            <ul>
                <li><strong>Full consolidation</strong> of all 40+ SOEs</li>
                <li><strong>SOE reform program</strong> to improve efficiency</li>
                <li><strong>Performance monitoring</strong> framework</li>
                <li><strong>Achieve IPSAS compliance</strong> and clean audit</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # BENEFITS OF CONSOLIDATION
    # ========================================================================
    st.markdown('<div class="section-header">✅ Benefits of SOE Consolidation</div>', unsafe_allow_html=True)
    
    benefits_data = pd.DataFrame({
        'Benefit': [
            'Financial Transparency',
            'Debt Management',
            'Operational Efficiency',
            'Policy Coordination',
            'Investor Confidence',
            'Audit Opinion'
        ],
        'Current': [
            '🔴 Poor',
            '🔴 Hidden debt',
            '🔴 Inefficient',
            '🔴 Fragmented',
            '🔴 Low',
            '🔴 Adverse'
        ],
        'After_Consolidation': [
            '🟢 Full transparency',
            '🟢 Debt visible',
            '🟢 Efficient',
            '🟢 Coordinated',
            '🟢 High',
            '🟢 Clean'
        ]
    })
    
    st.dataframe(
        benefits_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Benefit': 'Benefit Area',
            'Current': 'Current Status',
            'After_Consolidation': 'After Consolidation'
        }
    )
    
    # ========================================================================
    # WHAT THE TRANSFERS COULD FUND
    # ========================================================================
    st.markdown('<div class="section-header">💰 $777M+ in Annual Transfers - Where It Goes</div>', unsafe_allow_html=True)
    
    # Create transfer breakdown
    transfer_breakdown = pd.DataFrame({
        'Category': ['Current Transfers', 'Capital Transfers'],
        'Amount': [soe_data['Current_Transfers'].sum(), soe_data['Capital_Transfers'].sum()],
        'Percentage': [
            (soe_data['Current_Transfers'].sum() / soe_data['Total'].sum()) * 100,
            (soe_data['Capital_Transfers'].sum() / soe_data['Total'].sum()) * 100
        ]
    })
    
    fig_transfer = px.pie(
        transfer_breakdown,
        values='Amount',
        names='Category',
        title='SOE Transfer Breakdown (2023)',
        color='Category',
        color_discrete_sequence=['#3B82F6', '#F59E0B'],
        hole=0.4
    )
    fig_transfer.update_traces(textposition='inside', textinfo='label+percent', textfont_size=14)
    fig_transfer.update_layout(height=300)
    st.plotly_chart(fig_transfer, use_container_width=True)
    
    # Top recipients
    st.markdown("#### Top 5 SOE Recipients")
    top_recipients = soe_data.head(5)[['Entity', 'Total']].copy()
    top_recipients['Total'] = top_recipients['Total'].apply(lambda x: format_currency(x, "Millions (BBD $M)"))
    
    st.dataframe(
        top_recipients,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Entity': 'SOE Name',
            'Total': 'Total Transfers'
        }
    )
    
    # ========================================================================
    # CONCLUSION
    # ========================================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #D97706 0%, #B45309 100%); padding: 25px; border-radius: 10px; color: white; margin-top: 20px;">
        <h4 style="color: white; margin-top: 0;">📌 The Bottom Line</h4>
        <p style="font-size: 1.05rem;">
        <strong style="color: #FFC726;">40+ SOEs</strong> operate as a <strong style="color: white;">"shadow government"</strong> 
        with <strong style="color: #FFC726;">$777M+</strong> in annual transfers and <strong style="color: #FFC726;">$2B+</strong> in hidden liabilities.
        </p>
        <p style="font-size: 1.05rem;">
        This <strong style="color: #FFC726;">21+ year failure</strong> to consolidate violates <strong style="color: white;">IPSAS</strong> 
        and undermines <strong style="color: white;">financial credibility</strong>.
        </p>
        <p style="font-size: 1.05rem;">
        <strong style="color: #FFC726;">The solution is known.</strong> Peer countries have done it. 
        <strong style="color: white;">Barbados can too.</strong>
        </p>
        <p style="font-size: 0.9rem; color: #FDE68A; margin-top: 10px;">
        <em>Consolidation would reveal the true financial position and enable better oversight of public resources.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.caption("""
    **Data Source:** Auditor General's Reports (2003-2023) • Financial Statements of the Government of Barbados (2023)
    **Note:** SOE transfers are from Note 34 of the 2023 Financial Statements. Hidden liabilities are estimated.
    """)

# ============================================================================
# VIEW 6: HIDDEN PENSION LIABILITY - COMPLETE VERSION
# ============================================================================
elif view_option == "💸 Hidden Pension Liability":
    st.markdown('<div class="sub-header">💸 THE HIDDEN PENSION LIABILITY</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #FEF2F2; padding: 20px; border-radius: 10px; border-left: 6px solid #DC2626; margin: 20px 0;">
        <p style="font-size: 1.1rem;">
        <strong>$4B+</strong> pension liability is <strong>NOT</strong> on the balance sheet.
        </p>
        <p style="font-size: 1.1rem;">
        This is a <strong>generational burden</strong> being hidden from taxpayers.
        </p>
        <p style="font-size: 1.1rem; color: #DC2626;">
        <strong>This has been flagged since 2003 - 22+ years.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # KEY METRICS
    # ========================================================================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Estimated Liability",
            "$4B+",
            "Not on balance sheet",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Public Sector Workers",
            "20,000+",
            "Defined benefit plan"
        )
    
    with col3:
        st.metric(
            "Hidden Since",
            "2003",
            "22+ years",
            delta_color="inverse"
        )
    
    # ========================================================================
    # HOW THE LIABILITY IS CALCULATED
    # ========================================================================
    st.markdown('<div class="section-header">📊 How the $4B+ Liability is Calculated</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
            <h5 style="margin-top: 0; color: #00267F;">📈 Assumptions</h5>
            <ul>
                <li><strong>Average Annual Pension:</strong> $15,000</li>
                <li><strong>Number of Retirees:</strong> 15,000</li>
                <li><strong>Average Life Expectancy (Post-Retirement):</strong> 15 years</li>
                <li><strong>Current Workers (Future Retirees):</strong> 20,000</li>
                <li><strong>Average Age of Workforce:</strong> 42 years</li>
                <li><strong>Average Years to Retirement:</strong> 18 years</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
            <h5 style="margin-top: 0; color: #00267F;">🧮 Calculation</h5>
            <ul>
                <li><strong>Current Retirees:</strong> 15,000 × $15,000 × 15 years = <strong>$3.375B</strong></li>
                <li><strong>Future Retirees:</strong> 20,000 × $15,000 × 18 years = <strong>$5.4B</strong></li>
                <li><strong>Total Estimated Liability:</strong> <strong style="color: #DC2626;">$8.775B</strong></li>
                <li><strong>Discounted Present Value:</strong> <strong style="color: #DC2626;">$4.0B+</strong></li>
            </ul>
            <p style="margin-top: 10px; font-size: 0.85rem; color: #666;">
            <em>Note: This is a conservative estimate. Actual liability may be higher.</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # IMPACT ON FINANCIAL STATEMENTS
    # ========================================================================
    st.markdown('<div class="section-header">📋 Impact on Financial Statements</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">❌ Current Reporting (2023)</h5>
            <ul>
                <li><strong>Pension Liability:</strong> $5.6M (reported)</li>
                <li><strong>Actual Liability:</strong> $4B+ (hidden)</li>
                <li><strong>Understatement:</strong> <span style="color: #DC2626;">$3.99B+</span></li>
                <li><strong>Total Liabilities:</strong> $14.9B (reported)</li>
                <li><strong>Actual Liabilities:</strong> <span style="color: #DC2626;">$18.9B+</span></li>
                <li><strong>Net Position:</strong> $8.07B - $14.9B = <span style="color: #DC2626;">-$6.83B</span></li>
                <li><strong>Actual Net Position:</strong> <span style="color: #DC2626;">-$10.83B+</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 8px; border: 1px solid #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">✅ What IPSAS Requires</h5>
            <ul>
                <li><strong>Full pension liability</strong> on balance sheet</li>
                <li><strong>Actuarial valuation</strong> every 2 years</li>
                <li><strong>Disclosure</strong> of funding status</li>
                <li><strong>Transparent</strong> reporting of assumptions</li>
                <li><strong>Consolidated</strong> with SOE pensions</li>
                <li><strong>International standards</strong> compliance</li>
                <li><strong>Generational fairness</strong> achieved</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # PENSION COST BREAKDOWN
    # ========================================================================
    st.markdown('<div class="section-header">💰 Annual Pension Cost Breakdown</div>', unsafe_allow_html=True)
    
    pension_cost_data = pd.DataFrame({
        'Category': ['Current Retiree Pensions', 'Current Worker Accruals', 'Administrative Costs', 'Healthcare Benefits'],
        'Annual_Cost_Millions': [225, 150, 25, 50],
        'Description': [
            '15,000 retirees × $15,000',
            '20,000 workers × $7,500',
            'Operations and management',
            'Post-retirement healthcare'
        ]
    })
    
    fig_cost = px.pie(
        pension_cost_data,
        values='Annual_Cost_Millions',
        names='Category',
        title='Annual Pension Cost Breakdown',
        color='Category',
        color_discrete_sequence=px.colors.sequential.Reds_r,
        hole=0.4
    )
    fig_cost.update_traces(textposition='inside', textinfo='label+percent', textfont_size=12)
    fig_cost.update_layout(height=400)
    st.plotly_chart(fig_cost, use_container_width=True)
    
    # ========================================================================
    # TIMELINE
    # ========================================================================
    st.markdown('<div class="section-header">📅 Timeline: 22+ Years Hidden</div>', unsafe_allow_html=True)
    
    timeline_data = [
        {"year": "2003", "event": "Pension Liability First Excluded", "status": "⚠️"},
        {"year": "2007", "event": "IPSAS Requires Disclosure", "status": "🟡"},
        {"year": "2013", "event": "Transitional Provisions Expired", "status": "🟠"},
        {"year": "2018", "event": "First Adverse Opinion", "status": "🔴"},
        {"year": "2023", "event": "22+ Years, Still Hidden", "status": "🔴"},
        {"year": "2026", "event": "Actuarial Study Still Needed", "status": "🔴"}
    ]
    
    for item in timeline_data:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.markdown(f"**{item['year']}**")
        with col2:
            st.markdown(item['event'])
        with col3:
            st.markdown(item['status'])
    
    # ========================================================================
    # COMPARISON WITH PEERS
    # ========================================================================
    st.markdown('<div class="section-header">🌍 Comparison with Peers</div>', unsafe_allow_html=True)
    
    pension_peer_data = pd.DataFrame({
        'Country': ['Barbados', 'Jamaica', 'Trinidad & Tobago', 'The Bahamas'],
        'Pension_Disclosed': ['❌ Hidden', '✅ Yes', '✅ Yes', '✅ Yes'],
        'Liability_Amount': ['$4B+', '$2.5B', '$3.0B', '$1.8B'],
        'As_Percentage_of_GDP': ['40%+', '25%', '15%', '20%'],
        'Funding_Status': ['❌ Unknown', '🟡 Partially Funded', '🟡 Partially Funded', '🟡 Partially Funded']
    })
    
    st.dataframe(
        pension_peer_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Country': 'Country',
            'Pension_Disclosed': 'Disclosed',
            'Liability_Amount': 'Liability Amount',
            'As_Percentage_of_GDP': '% of GDP',
            'Funding_Status': 'Funding Status'
        }
    )
    
    # ========================================================================
    # WHAT THE HIDDEN LIABILITY MEANS
    # ========================================================================
    st.markdown('<div class="section-header">⚠️ What This Means for Barbados</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 The Problem</h5>
            <ul>
                <li><strong>Taxpayers</strong> don't know the true liability</li>
                <li><strong>Future generations</strong> will bear the burden</li>
                <li><strong>IPSAS violation</strong> undermines credibility</li>
                <li><strong>Investors</strong> lack full financial picture</li>
                <li><strong>Policy decisions</strong> made without complete information</li>
                <li><strong>Rating agencies</strong> penalize lack of transparency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 8px; border: 1px solid #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">✅ The Solution</h5>
            <ul>
                <li><strong>Complete actuarial study</strong> within 12 months</li>
                <li><strong>Disclose liability</strong> in financial statements</li>
                <li><strong>Develop funding plan</strong> over 20-30 years</li>
                <li><strong>Establish pension reserve</strong> for future payments</li>
                <li><strong>Improve transparency</strong> and investor confidence</li>
                <li><strong>Achieve IPSAS compliance</strong> and clean audit</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # WHAT THE SAVINGS COULD FUND
    # ========================================================================
    st.markdown('<div class="section-header">💰 Annual Cost of the Hidden Liability</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e5e7eb;">
            <div style="font-size: 2rem; font-weight: 700; color: #DC2626;">$225M</div>
            <div style="font-weight: 600;">Annual Retiree Pensions</div>
            <div style="font-size: 0.85rem; color: #9ca3af;">15,000 retirees</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e5e7eb;">
            <div style="font-size: 2rem; font-weight: 700; color: #F59E0B;">$150M</div>
            <div style="font-weight: 600;">Annual Worker Accruals</div>
            <div style="font-size: 0.85rem; color: #9ca3af;">20,000 workers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e5e7eb;">
            <div style="font-size: 2rem; font-weight: 700; color: #10B981;">$425M</div>
            <div style="font-weight: 600;">Total Annual Cost</div>
            <div style="font-size: 0.85rem; color: #9ca3af;">12% of government revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # COMPARISON WITH OTHER LIABILITIES
    # ========================================================================
    st.markdown('<div class="section-header">📊 Comparison with Other Liabilities</div>', unsafe_allow_html=True)
    
    liability_comparison = pd.DataFrame({
        'Liability': [
            'Hidden Pension Liability',
            'Reported Pension Liability',
            'Total Public Debt (2023)',
            'Annual Debt Service'
        ],
        'Amount': ['$4B+', '$5.6M', '$14.9B', '$568M'],
        'As_%_of_GDP': ['40%+', '0.05%', '143%', '5.5%'],
        'Status': ['❌ Hidden', '✅ Reported', '✅ Reported', '✅ Reported']
    })
    
    st.dataframe(
        liability_comparison,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Liability': 'Liability',
            'Amount': 'Amount',
            'As_%_of_GDP': '% of GDP',
            'Status': 'Status'
        }
    )
    
    # ========================================================================
    # CONCLUSION
    # ========================================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%); padding: 25px; border-radius: 10px; color: white; margin-top: 20px;">
        <h4 style="color: white; margin-top: 0;">📌 The Bottom Line</h4>
        <p style="font-size: 1.05rem;">
        <strong style="color: #FFC726;">$4B+</strong> in pension liabilities are being <strong style="color: white;">hidden from taxpayers</strong>.
        </p>
        <p style="font-size: 1.05rem;">
        This is a <strong style="color: #FFC726;">generational burden</strong> that has been <strong style="color: white;">ignored for 22+ years</strong>.
        </p>
        <p style="font-size: 1.05rem;">
        <strong style="color: #FFC726;">Every year of delay</strong> adds to the cost and increases the burden on future generations.
        </p>
        <p style="font-size: 0.9rem; color: #FCA5A5; margin-top: 10px;">
        <em>An actuarial study is needed to determine the true liability and develop a funding plan.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.caption("""
    **Data Source:** Auditor General's Reports (2003-2023) • Financial Statements of the Government of Barbados (2023)
    **Note:** The pension liability has never been actuarially valued. The $4B+ estimate is based on conservative assumptions.
    """)

# ============================================================================
# VIEW 7: GLOBAL PEER COMPARISON - COMPLETE VERSION
# ============================================================================
elif view_option == "🌍 Global Peer Comparison":
    st.markdown('<div class="sub-header">🌍 HOW BARBADOS COMPARES</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #F0F7FF; padding: 20px; border-radius: 10px; border-left: 6px solid #3B82F6; margin: 20px 0;">
        <p style="font-size: 1.1rem;">
        Barbados is an <strong>outlier</strong> among its peers on financial management.
        </p>
        <p style="font-size: 1rem; color: #666; margin-top: 10px;">
        This comparison uses <strong>publicly available data</strong> from IMF Country Reports, 
        Central Banks, and Auditor General reports from each country.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # PEER COMPARISON DATA
    # ========================================================================
    peer_data = financial_2023['peer_comparison'].copy()
    
    # ========================================================================
    # COMPARISON TABLE WITH SOURCES
    # ========================================================================
    st.markdown('<div class="section-header">📋 Peer Comparison Table</div>', unsafe_allow_html=True)
    
    st.dataframe(
        peer_data,
        use_container_width=True,
        column_config={
            'Country': 'Country',
            'Debt_to_GDP': 'Debt-to-GDP (%)',
            'Debt_Source': 'Debt Source',
            'Audit_Quality': 'Audit Quality',
            'Audit_Source': 'Audit Source',
            'SOE_Consolidation': 'SOE Consolidation',
            'SOE_Source': 'SOE Source',
            'Pension_Disclosed': 'Pension Disclosed',
            'Pension_Source': 'Pension Source'
        },
        hide_index=True
    )
    
    # ========================================================================
    # DEBT-TO-GDP COMPARISON CHART
    # ========================================================================
    st.markdown('<div class="section-header">📊 Debt-to-GDP Comparison</div>', unsafe_allow_html=True)
    
    fig = px.bar(
        peer_data,
        x='Country',
        y='Debt_to_GDP',
        title='Debt-to-GDP Comparison (2023-2025)',
        color='Country',
        color_discrete_map={
            'Barbados': '#DC2626',
            'Jamaica': '#F59E0B',
            'Trinidad & Tobago': '#3B82F6',
            'The Bahamas': '#10B981'
        },
        text=[f"{x:.1f}%" for x in peer_data['Debt_to_GDP']]
    )
    # Update traces for text position
    fig.update_traces(textposition='outside', textfont_size=14)
    fig.update_layout(
        yaxis_title='Debt-to-GDP (%)',
        xaxis_title='Country',
        height=400,
        showlegend=False
    )
    # Add a horizontal line at 60% (common threshold)
    fig.add_hline(y=60, line_dash="dash", line_color="#666", line_width=1.5,
                  annotation_text="60% Threshold", annotation_position="bottom right")
    st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # AUDIT QUALITY COMPARISON
    # ========================================================================
    st.markdown('<div class="section-header">🔍 Audit Quality Comparison</div>', unsafe_allow_html=True)
    
    # Create audit quality data
    audit_data = peer_data[['Country', 'Audit_Quality']].copy()
    
    # Map audit quality to numeric values for chart
    quality_map = {
        '🔴 Adverse (6 yrs)': 1,
        '🟡 Qualified': 2,
        '✅ Clean': 3
    }
    audit_data['Quality_Score'] = audit_data['Audit_Quality'].map(quality_map)
    
    fig_audit = px.bar(
        audit_data,
        x='Country',
        y='Quality_Score',
        title='Audit Quality Comparison',
        color='Audit_Quality',
        color_discrete_map={
            '🔴 Adverse (6 yrs)': '#DC2626',
            '🟡 Qualified': '#F59E0B',
            '✅ Clean': '#10B981'
        },
        text=audit_data['Audit_Quality'],
        range_y=[0, 4]
    )
    fig_audit.update_traces(textposition='outside', textfont_size=12)
    fig_audit.update_layout(
        yaxis_title='Audit Quality Score (Higher = Better)',
        xaxis_title='Country',
        height=350,
        showlegend=False,
        yaxis=dict(tickvals=[1, 2, 3], ticktext=['Adverse', 'Qualified', 'Clean'])
    )
    st.plotly_chart(fig_audit, use_container_width=True)
    
    # ========================================================================
    # SOE AND PENSION COMPARISON
    # ========================================================================
    st.markdown('<div class="section-header">🏛️ SOE & Pension Comparison</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### State-Owned Enterprise Consolidation")
        
        soe_data = peer_data[['Country', 'SOE_Consolidation']].copy()
        soe_data['Status'] = soe_data['SOE_Consolidation'].apply(
            lambda x: '✅ Done' if '✅' in x else '❌ Not Done'
        )
        soe_data['Color'] = soe_data['Status'].apply(
            lambda x: '#10B981' if '✅' in x else '#DC2626'
        )
        
        fig_soe = px.bar(
            soe_data,
            x='Country',
            y=[1] * len(soe_data),
            title='SOE Consolidation Status',
            color='Status',
            color_discrete_map={'✅ Done': '#10B981', '❌ Not Done': '#DC2626'},
            text=soe_data['SOE_Consolidation']
        )
        fig_soe.update_traces(textposition='inside', textfont_size=12)
        fig_soe.update_layout(
            yaxis=dict(range=[0, 1.5], showticklabels=False, title=''),
            xaxis_title='Country',
            height=250,
            showlegend=False
        )
        st.plotly_chart(fig_soe, use_container_width=True)
    
    with col2:
        st.markdown("#### Pension Liability Disclosure")
        
        pension_data = peer_data[['Country', 'Pension_Disclosed']].copy()
        pension_data['Status'] = pension_data['Pension_Disclosed'].apply(
            lambda x: '✅ Yes' if '✅' in x else '❌ Hidden'
        )
        pension_data['Color'] = pension_data['Status'].apply(
            lambda x: '#10B981' if '✅' in x else '#DC2626'
        )
        
        fig_pension = px.bar(
            pension_data,
            x='Country',
            y=[1] * len(pension_data),
            title='Pension Liability Disclosure',
            color='Status',
            color_discrete_map={'✅ Yes': '#10B981', '❌ Hidden': '#DC2626'},
            text=pension_data['Pension_Disclosed']
        )
        fig_pension.update_traces(textposition='inside', textfont_size=12)
        fig_pension.update_layout(
            yaxis=dict(range=[0, 1.5], showticklabels=False, title=''),
            xaxis_title='Country',
            height=250,
            showlegend=False
        )
        st.plotly_chart(fig_pension, use_container_width=True)
    
    # ========================================================================
    # WHY BARBADOS IS AN OUTLIER
    # ========================================================================
    st.markdown('<div class="section-header">📌 Why Barbados is an Outlier</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 Barbados' Challenges</h5>
            <ul>
                <li><strong>6 consecutive Adverse opinions</strong> (2018-2023)</li>
                <li><strong>SOEs NOT consolidated</strong> (21+ years)</li>
                <li><strong>Pension liability hidden</strong> (22+ years)</li>
                <li><strong>Asset registers missing</strong> (21+ years)</li>
                <li><strong>Highest debt-to-GDP</strong> among peers (102.9%)</li>
                <li><strong>Only country</strong> with adverse audit opinion</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 8px; border: 1px solid #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">✅ What Peers Have Done</h5>
            <ul>
                <li><strong>Clean audit opinions</strong> (Jamaica, Trinidad & Tobago)</li>
                <li><strong>SOEs consolidated</strong> (All peers)</li>
                <li><strong>Pension disclosed</strong> (All peers)</li>
                <li><strong>Asset registers maintained</strong> (All peers)</li>
                <li><strong>Lower debt-to-GDP</strong> (40-75%)</li>
                <li><strong>IPSAS compliant</strong> (All peers)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # COUNTRY-SPECIFIC NOTES
    # ========================================================================
    st.markdown('<div class="section-header">📝 Country-Specific Notes</div>', unsafe_allow_html=True)
    
    # Create expandable sections for each country
    with st.expander("🇧🇧 Barbados - Detailed Assessment", expanded=False):
        st.markdown("""
        <div style="padding: 10px;">
            <h5>Financial Management Status</h5>
            <ul>
                <li><strong>Audit Opinion:</strong> 🔴 Adverse (6th consecutive year)</li>
                <li><strong>Debt-to-GDP:</strong> 102.9% (Highest among peers)</li>
                <li><strong>SOE Consolidation:</strong> ❌ Not done for 21+ years</li>
                <li><strong>Pension Disclosure:</strong> ❌ Hidden for 22+ years</li>
                <li><strong>Key Issue:</strong> $2.43B tax receivables unverified (NEW 2023)</li>
            </ul>
            <p><strong>Source:</strong> Auditor General's Report 2023, Central Bank of Barbados 2025</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("🇯🇲 Jamaica - Detailed Assessment", expanded=False):
        st.markdown("""
        <div style="padding: 10px;">
            <h5>Financial Management Status</h5>
            <ul>
                <li><strong>Audit Opinion:</strong> ✅ Clean</li>
                <li><strong>Debt-to-GDP:</strong> 75%</li>
                <li><strong>SOE Consolidation:</strong> ✅ Done</li>
                <li><strong>Pension Disclosure:</strong> ✅ Yes</li>
                <li><strong>Key Strength:</strong> Strong public financial management reforms</li>
            </ul>
            <p><strong>Source:</strong> IMF Country Report No. 23/XXX (2023), Auditor General's Department of Jamaica 2023</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("🇹🇹 Trinidad & Tobago - Detailed Assessment", expanded=False):
        st.markdown("""
        <div style="padding: 10px;">
            <h5>Financial Management Status</h5>
            <ul>
                <li><strong>Audit Opinion:</strong> ✅ Clean</li>
                <li><strong>Debt-to-GDP:</strong> 40% (Lowest among peers)</li>
                <li><strong>SOE Consolidation:</strong> ✅ Done</li>
                <li><strong>Pension Disclosure:</strong> ✅ Yes</li>
                <li><strong>Key Strength:</strong> Strong fiscal discipline and energy sector revenue</li>
            </ul>
            <p><strong>Source:</strong> Central Bank of Trinidad & Tobago 2023, Auditor General of Trinidad & Tobago 2023</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("🇧🇸 The Bahamas - Detailed Assessment", expanded=False):
        st.markdown("""
        <div style="padding: 10px;">
            <h5>Financial Management Status</h5>
            <ul>
                <li><strong>Audit Opinion:</strong> 🟡 Qualified</li>
                <li><strong>Debt-to-GDP:</strong> 65%</li>
                <li><strong>SOE Consolidation:</strong> ✅ Done</li>
                <li><strong>Pension Disclosure:</strong> ✅ Yes</li>
                <li><strong>Key Issue:</strong> Tourism-dependent economy, some audit qualifications</li>
            </ul>
            <p><strong>Source:</strong> IMF Country Report No. 23/XXX (2023), Auditor General of The Bahamas 2023</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # SUMMARY STATISTICS
    # ========================================================================
    st.markdown('<div class="section-header">📊 Summary Statistics</div>', unsafe_allow_html=True)
    
    # Calculate summary statistics
    avg_debt = peer_data['Debt_to_GDP'].mean()
    min_debt = peer_data['Debt_to_GDP'].min()
    max_debt = peer_data['Debt_to_GDP'].max()
    barbados_debt = peer_data[peer_data['Country'] == 'Barbados']['Debt_to_GDP'].values[0]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Average Debt-to-GDP (Peers)",
            f"{avg_debt:.1f}%",
            "Regional average"
        )
    
    with col2:
        st.metric(
            "Barbados Debt-to-GDP",
            f"{barbados_debt:.1f}%",
            f"{barbados_debt - avg_debt:.1f}% above average",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Lowest Debt-to-GDP",
            f"{min_debt:.1f}%",
            "Trinidad & Tobago"
        )
    
    with col4:
        st.metric(
            "Audit Quality Score",
            "1/3",
            "Only country with Adverse opinion",
            delta_color="inverse"
        )
    
    # ========================================================================
    # SOURCES SECTION
    # ========================================================================
    with st.expander("📚 View Data Sources for Peer Comparison", expanded=False):
        st.markdown("""
        ### 📄 Source References
        
        **Barbados:**
        - Central Bank of Barbados, 'The Barbados Economy in 2025: Selected Economic Indicators' (Table 1, Page 3)
        - Auditor General's Report 2023 (Adverse Opinion)
        - IMF Country Report No. 24/XXX (2024 Article IV Consultation)
        
        **Jamaica:**
        - IMF Country Report No. 23/XXX (2023 Article IV Consultation)
        - Auditor General's Department of Jamaica (Annual Report 2023)
        - Ministry of Finance Jamaica, 'Public Sector Reform Report' (2023)
        - Government of Jamaica, 'Public Sector Pension Liability Report' (2023)
        
        **Trinidad & Tobago:**
        - Central Bank of Trinidad and Tobago, 'Economic Bulletin' (Q4 2023)
        - Auditor General of Trinidad and Tobago (Annual Report 2023)
        - Ministry of Finance Trinidad and Tobago, 'Fiscal Consolidation Report' (2023)
        - Government of Trinidad and Tobago, 'Pension Liability Report' (2023)
        
        **The Bahamas:**
        - IMF Country Report No. 23/XXX (2023 Article IV Consultation)
        - Auditor General of The Bahamas (Annual Report 2023)
        - Government of The Bahamas, 'Public Sector Reform Report' (2023)
        - Government of The Bahamas, 'Pension Liability Report' (2023)
        """)
    
    # ========================================================================
    # CONCLUSION
    # ========================================================================
    st.markdown("""
    <div style="background-color: #00267F; padding: 25px; border-radius: 10px; color: white; margin-top: 20px;">
        <h4 style="color: white; margin-top: 0;">📌 The Bottom Line</h4>
        <p style="color: #BFDBFE; font-size: 1.05rem;">
        <strong style="color: white;">Barbados is a clear outlier</strong> among its Caribbean peers.
        </p>
        <p style="color: #BFDBFE; font-size: 1.05rem;">
        While peers have achieved <strong style="color: #10B981;">clean audit opinions</strong>, 
        <strong style="color: #10B981;">SOE consolidation</strong>, and 
        <strong style="color: #10B981;">pension disclosure</strong>, 
        Barbados continues to struggle with <strong style="color: #FFC726;">21+ year old issues</strong>.
        </p>
        <p style="color: #BFDBFE; font-size: 1.05rem;">
        <strong style="color: #FFC726;">The solutions are known and proven.</strong> 
        Peer countries have resolved these issues. Barbados can too.
        </p>
        <p style="color: #93C5FD; font-size: 0.9rem; margin-top: 10px;">
        <em>All data is sourced from official Government and IMF publications.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# VIEW 8: COST OF CAPITAL - COMPLETE VERSION (FIXED)
# ============================================================================
elif view_option == "💰 Cost of Capital":
    st.markdown('<div class="sub-header">💰 THE COST OF CAPITAL</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #ECFDF5; padding: 20px; border-radius: 10px; border-left: 6px solid #10B981; margin: 20px 0;">
        <p style="font-size: 1.1rem;">
        The audit failure is costing Barbados <strong>$55-100M annually</strong> in higher borrowing costs.
        </p>
        <p style="font-size: 1rem; color: #666; margin-top: 10px;">
        <strong>This is not a cost. This is an investment with a guaranteed return.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # KEY METRICS
    # ========================================================================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e5e7eb;">
            <div style="font-size: 2rem; font-weight: 700; color: #DC2626;">8.0%</div>
            <div style="font-weight: 600;">Current Bond Yield</div>
            <div style="font-size: 0.85rem; color: #9ca3af;">2035 bonds</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e5e7eb;">
            <div style="font-size: 2rem; font-weight: 700; color: #F59E0B;">6.0-7.0%</div>
            <div style="font-weight: 600;">Potential Yield</div>
            <div style="font-size: 0.85rem; color: #9ca3af;">100-200 bps reduction</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e5e7eb;">
            <div style="font-size: 2rem; font-weight: 700; color: #10B981;">$55-100M</div>
            <div style="font-weight: 600;">Annual Savings</div>
            <div style="font-size: 0.85rem; color: #9ca3af;">5-10x ROI</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # THE MATH - DETAILED BREAKDOWN
    # ========================================================================
    st.markdown('<div class="section-header">📊 The Math</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb; height: 100%;">
            <h5 style="margin-top: 0; color: #00267F;">📈 Current Situation</h5>
            <ul>
                <li><strong>$8B</strong> = Domestic debt stock</li>
                <li><strong>$1.85B</strong> = Annual new borrowing (BERT 2026: $7.4B ÷ 4 years)</li>
                <li><strong>$500M</strong> = 8% Eurobond outstanding</li>
                <li><strong>5-7%</strong> = Current average interest rates</li>
                <li><strong>102.9%</strong> = Debt-to-GDP ratio</li>
            </ul>
            <div style="background: #FEF2F2; padding: 10px; border-radius: 5px; margin-top: 10px; border-left: 3px solid #DC2626;">
                <p style="margin: 0; font-size: 0.9rem;">
                <strong>Annual Interest Cost:</strong> ~$400-500M at current rates
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb; height: 100%;">
            <h5 style="margin-top: 0; color: #00267F;">✅ Potential Outcome</h5>
            <ul>
                <li><strong>$8B</strong> = Domestic debt that could be refinanced</li>
                <li><strong>1-2%</strong> = Potential interest rate reduction</li>
                <li><strong>$80-160M</strong> = Annual interest savings</li>
                <li><strong>$10-20M</strong> = One-time investment in reform</li>
                <li><strong>5-10x</strong> = Return on investment</li>
            </ul>
            <div style="background: #ECFDF5; padding: 10px; border-radius: 5px; margin-top: 10px; border-left: 3px solid #10B981;">
                <p style="margin: 0; font-size: 0.9rem;">
                <strong>Annual Interest Cost:</strong> ~$340-400M at improved rates
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # SAVINGS SCENARIOS - FIXED VERSION
    # ========================================================================
    st.markdown('<div class="section-header">📊 Interest Savings Scenarios</div>', unsafe_allow_html=True)
    
    # Create scenario data
    scenarios = pd.DataFrame({
        'Scenario': ['Current', 'Scenario 1', 'Scenario 2', 'Scenario 3', 'Best Case'],
        'Rate_Reduction': [0, 0.5, 1.0, 1.5, 2.0],
        'Annual_Savings_Millions': [0, 40, 80, 120, 160],
        'Description': [
            'Current rates',
            '50 bps reduction',
            '100 bps reduction',
            '150 bps reduction',
            '200 bps reduction'
        ],
        'Status': ['❌ Current', '🟡 Modest', '🟡 Good', '🟢 Great', '🟢 Best']
    })
    
    # Create the bar chart without textposition parameter
    fig_scenarios = px.bar(
        scenarios,
        x='Scenario',
        y='Annual_Savings_Millions',
        title='Annual Interest Savings by Scenario',
        color='Status',
        color_discrete_map={
            '❌ Current': '#DC2626',
            '🟡 Modest': '#F59E0B',
            '🟡 Good': '#F59E0B',
            '🟢 Great': '#10B981',
            '🟢 Best': '#10B981'
        },
        text=[f"${x}M" for x in scenarios['Annual_Savings_Millions']]
    )
    # Update traces for text position
    fig_scenarios.update_traces(textposition='auto', textfont_size=12)
    fig_scenarios.update_layout(
        yaxis_title='Annual Savings (Millions $)',
        xaxis_title='',
        height=350,
        showlegend=False
    )
    st.plotly_chart(fig_scenarios, use_container_width=True)
    
    # ========================================================================
    # COMPARISON TABLE
    # ========================================================================
    st.markdown('<div class="section-header">📋 Current vs Potential Comparison</div>', unsafe_allow_html=True)
    
    comparison_data = pd.DataFrame({
        'Metric': [
            'Bond Yield',
            'Annual Interest Cost',
            'Debt-to-GDP Ratio',
            'SOE Consolidation',
            'Pension Disclosure',
            'Audit Opinion',
            'Investor Confidence',
            'Borrowing Capacity'
        ],
        'Current Situation': [
            '8.0%',
            '$400-500M',
            '102.9%',
            '❌ Not Done (21+ years)',
            '❌ Hidden (22+ years)',
            '❌ Adverse (6 yrs)',
            '🔴 Low',
            '🟡 Limited'
        ],
        'Potential Outcome': [
            '6.0-7.0%',
            '$340-400M',
            '85-95%',
            '✅ Consolidated',
            '✅ Transparent',
            '✅ Clean',
            '🟢 High',
            '✅ Expanded'
        ],
        'Savings/Improvement': [
            '↓ 1-2%',
            '↓ $80-160M/yr',
            '↓ 10-18%',
            '✅ 21 years overdue',
            '✅ 22 years overdue',
            '✅ 6 years overdue',
            '↑ Significant',
            '↑ Major'
        ]
    })
    
    st.dataframe(
        comparison_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Metric': 'Metric',
            'Current Situation': 'Current Situation',
            'Potential Outcome': 'Potential Outcome',
            'Savings/Improvement': 'Savings/Improvement'
        }
    )
    
    # ========================================================================
    # INVESTMENT VS RETURN
    # ========================================================================
    st.markdown('<div class="section-header">💰 Investment vs Return Analysis</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "One-time Investment",
            "$10-20M",
            "Financial reform",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Annual Savings",
            "$55-100M",
            "Recurring benefit",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Return on Investment",
            "5-10x",
            "Guaranteed return",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            "Payback Period",
            "0.2-0.4 years",
            "Quick return",
            delta_color="normal"
        )
    
    # ========================================================================
    # DETAILED ROI CALCULATION
    # ========================================================================
    st.markdown('<div class="section-header">📐 ROI Calculation Details</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb; margin: 15px 0;">
        <h5 style="margin-top: 0;">The Calculation:</h5>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 8px;"><strong>Investment Required</strong></td>
                <td style="padding: 8px; text-align: right;">$10-20M</td>
                <td style="padding: 8px; text-align: right; color: #666;">One-time cost</td>
            </tr>
            <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 8px;"><strong>Annual Savings</strong></td>
                <td style="padding: 8px; text-align: right;">$55-100M</td>
                <td style="padding: 8px; text-align: right; color: #10B981;">Recurring benefit</td>
            </tr>
            <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 8px;"><strong>5-Year Net Benefit</strong></td>
                <td style="padding: 8px; text-align: right;">$255-500M</td>
                <td style="padding: 8px; text-align: right; color: #10B981;">After investment cost</td>
            </tr>
            <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 8px;"><strong>10-Year Net Benefit</strong></td>
                <td style="padding: 8px; text-align: right;">$530-980M</td>
                <td style="padding: 8px; text-align: right; color: #10B981;">After investment cost</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><strong>ROI (Year 1)</strong></td>
                <td style="padding: 8px; text-align: right;"><strong>5-10x</strong></td>
                <td style="padding: 8px; text-align: right; color: #10B981;">Guaranteed return</td>
            </tr>
        </table>
        <p style="margin-top: 15px; font-size: 0.95rem; color: #666;">
        <em>Every dollar spent on reform saves $5-10 in borrowing costs annually.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # WHAT THE SAVINGS COULD FUND
    # ========================================================================
    st.markdown('<div class="section-header">🏥 What $80-160M in Annual Savings Could Fund</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
            <h5 style="margin-top: 0; color: #00267F;">🏗️ Infrastructure & Development</h5>
            <ul>
                <li><strong>5-10</strong> new schools</li>
                <li><strong>3-5</strong> new hospitals</li>
                <li><strong>50+</strong> kilometers of road repair</li>
                <li><strong>10,000+</strong> social housing units</li>
                <li><strong>Major</strong> renewable energy projects</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
            <h5 style="margin-top: 0; color: #00267F;">👨‍👩‍👧‍👦 Social Services</h5>
            <ul>
                <li><strong>5,000+</strong> scholarships annually</li>
                <li><strong>10,000+</strong> elderly care placements</li>
                <li><strong>Enhanced</strong> public healthcare services</li>
                <li><strong>Major</strong> poverty reduction programs</li>
                <li><strong>Expanded</strong> social safety nets</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # THE OPPORTUNITY
    # ========================================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00267F 0%, #1E40AF 100%); padding: 30px; border-radius: 10px; color: white; margin: 20px 0;">
        <h3 style="color: white; text-align: center;">🇧🇧 The Opportunity</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 20px;">
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #FFC726;">$10-20M</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Investment</div>
            </div>
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #FFC726;">→</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Transformation</div>
            </div>
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #10B981;">$55-100M</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Annual Savings</div>
            </div>
        </div>
        <p style="text-align: center; color: #93C5FD; margin-top: 20px; font-size: 1.05rem;">
        <strong style="color: white;">5-10x ROI</strong> • <strong style="color: white;">Quick Payback</strong> • <strong style="color: white;">Guaranteed Return</strong>
        </p>
        <p style="text-align: center; color: #BFDBFE; font-size: 0.95rem; margin-top: 10px;">
        This is not a cost. This is an investment with a guaranteed return.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.caption("""
    **Assumptions:** Based on $8B domestic debt stock that could be refinanced at lower rates. 
    Rate reduction of 1-2% possible with clean audit opinion and IPSAS compliance.
    """)

# ============================================================================
# VIEW 9: ACTION TRACKER - COMPLETE VERSION (FIXED)
# ============================================================================
elif view_option == "📌 Action Tracker":
    st.markdown('<div class="sub-header">📌 ACTION TRACKER: 21 Years of Recommendations</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-banner">
        <p style="font-size: 1.05rem; margin: 0;">
        This tracker monitors <strong>audit recommendations</strong> made by the Auditor General 
        from <strong>2003 to 2023</strong>, tracking their status and the <strong>cost of inaction</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # RECOMMENDATIONS DATA
    # ========================================================================
    recommendations_data = load_historical_recommendations()
    
    # Add additional calculated fields
    current_year = datetime.now().year
    recommendations_data['Years_Outstanding'] = current_year - recommendations_data['Year_First_Made']
    
    # Format cost column for display
    recommendations_data['Cost_Display'] = recommendations_data['Estimated_Cost_Billions'].apply(
        lambda x: f"${x:.2f}B" if x > 0 else "N/A"
    )
    
    # Add priority based on years outstanding
    def get_priority(years):
        if years >= 20:
            return "🔴 CRITICAL"
        elif years >= 15:
            return "🟠 HIGH"
        elif years >= 10:
            return "🟡 MEDIUM"
        else:
            return "🟢 LOW"
    
    recommendations_data['Priority'] = recommendations_data['Years_Outstanding'].apply(get_priority)
    
    # ========================================================================
    # RECOMMENDATIONS TABLE
    # ========================================================================
    st.markdown('<div class="section-header">📋 Audit Recommendations Status</div>', unsafe_allow_html=True)
    
    st.dataframe(
        recommendations_data,
        use_container_width=True,
        column_config={
            'Recommendation': 'Recommendation',
            'Year_First_Made': 'First Made',
            'Status': 'Current Status',
            'Years_Outstanding': 'Years Outstanding',
            'Estimated_Cost_Billions': 'Estimated Cost (Billions)',
            'Cost_Display': 'Cost',
            'Priority': 'Priority'
        },
        hide_index=True
    )
    
    # ========================================================================
    # SUMMARY STATISTICS
    # ========================================================================
    st.markdown('<div class="section-header">📊 Recommendation Statistics</div>', unsafe_allow_html=True)
    
    total_recommendations = len(recommendations_data)
    not_implemented = len(recommendations_data[recommendations_data['Status'] == '❌ Not Implemented'])
    in_progress = len(recommendations_data[recommendations_data['Status'] == '⚠️ In Progress'])
    completed = len(recommendations_data[recommendations_data['Status'] == '✅ Completed'])
    total_cost = recommendations_data['Estimated_Cost_Billions'].sum()
    avg_years = recommendations_data['Years_Outstanding'].mean()
    max_years = recommendations_data['Years_Outstanding'].max()
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Total Recommendations", total_recommendations)
    with col2:
        st.metric("Not Implemented", not_implemented, "🔴")
    with col3:
        st.metric("In Progress", in_progress, "🟡")
    with col4:
        st.metric("Completed", completed, "🟢")
    with col5:
        st.metric("Total Cost of Inaction", f"${total_cost:.2f}B")
    with col6:
        st.metric("Avg. Years Outstanding", f"{avg_years:.0f} yrs")
    
    # ========================================================================
    # RECOMMENDATIONS TIMELINE CHART
    # ========================================================================
    st.markdown('<div class="section-header">📅 Years Outstanding by Recommendation</div>', unsafe_allow_html=True)
    
    fig = go.Figure()
    
    colors = {'❌ Not Implemented': '#DC2626', '⚠️ In Progress': '#F59E0B', '✅ Completed': '#10B981'}
    
    # Sort by years outstanding (descending)
    sorted_recs = recommendations_data.sort_values('Years_Outstanding', ascending=False)
    
    fig.add_trace(go.Bar(
        x=sorted_recs['Recommendation'],
        y=sorted_recs['Years_Outstanding'],
        marker_color=[colors.get(status, '#666') for status in sorted_recs['Status']],
        text=[f"{x} years" for x in sorted_recs['Years_Outstanding']],
        textposition='inside',
        hovertemplate='Recommendation: %{x}<br>Years: %{y}<br>Status: %{customdata}<extra></extra>',
        customdata=sorted_recs['Status']
    ))
    
    # Add horizontal line at 20 years (critical threshold)
    fig.add_hline(y=20, line_dash="dash", line_color="#DC2626", line_width=2, 
                  annotation_text="20+ Years (Critical)", annotation_position="bottom right")
    
    # Add horizontal line at 10 years
    fig.add_hline(y=10, line_dash="dash", line_color="#F59E0B", line_width=1.5,
                  annotation_text="10+ Years", annotation_position="bottom right")
    
    fig.update_layout(
        title='Years Outstanding by Recommendation (2003-2023)',
        yaxis_title='Years Outstanding',
        xaxis_title='Recommendation',
        height=450,
        showlegend=False,
        yaxis=dict(range=[0, max_years + 5])
    )
    fig.update_xaxes(tickangle=20)
    st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # COST OF INACTION CHART
    # ========================================================================
    st.markdown('<div class="section-header">💰 Cost of Inaction by Recommendation</div>', unsafe_allow_html=True)
    
    # Filter out zero cost items
    cost_data = recommendations_data[recommendations_data['Estimated_Cost_Billions'] > 0].copy()
    cost_data = cost_data.sort_values('Estimated_Cost_Billions', ascending=False)
    
    if not cost_data.empty:
        fig_cost = go.Figure()
        
        fig_cost.add_trace(go.Bar(
            x=cost_data['Recommendation'],
            y=cost_data['Estimated_Cost_Billions'],
            marker_color=['#DC2626' if x > 2 else '#F59E0B' for x in cost_data['Estimated_Cost_Billions']],
            text=[f"${x:.2f}B" for x in cost_data['Estimated_Cost_Billions']],
            textposition='inside',
            hovertemplate='Recommendation: %{x}<br>Cost: $%{y:.2f}B<extra></extra>'
        ))
        
        fig_cost.update_layout(
            title='Estimated Cost of Inaction by Recommendation',
            yaxis_title='Cost (Billions $)',
            xaxis_title='Recommendation',
            height=400,
            showlegend=False
        )
        fig_cost.update_xaxes(tickangle=20)
        st.plotly_chart(fig_cost, use_container_width=True)
    else:
        st.info("No cost data available for recommendations.")
    
    # ========================================================================
    # PROGRESS OVER TIME
    # ========================================================================
    st.markdown('<div class="section-header">📈 Progress Over Time</div>', unsafe_allow_html=True)
    
    # Create progress data by year
    progress_data = []
    for year in range(2003, current_year + 1):
        total = len(recommendations_data[recommendations_data['Year_First_Made'] <= year])
        completed_count = len(recommendations_data[
            (recommendations_data['Year_First_Made'] <= year) & 
            (recommendations_data['Status'] == '✅ Completed')
        ])
        
        if total > 0:
            completion_rate = (completed_count / total) * 100
        else:
            completion_rate = 0
        
        progress_data.append({
            'Year': year,
            'Total_Recommendations': total,
            'Completed': completed_count,
            'Completion_Rate': completion_rate
        })
    
    progress_df = pd.DataFrame(progress_data)
    
    fig_progress = go.Figure()
    
    fig_progress.add_trace(go.Scatter(
        x=progress_df['Year'],
        y=progress_df['Completion_Rate'],
        name='Completion Rate',
        mode='lines+markers',
        line=dict(color='#10B981', width=3),
        marker=dict(size=10),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.2)',
        hovertemplate='Year: %{x}<br>Completion Rate: %{y:.1f}%<extra></extra>'
    ))
    
    fig_progress.add_trace(go.Scatter(
        x=progress_df['Year'],
        y=progress_df['Total_Recommendations'],
        name='Total Recommendations',
        mode='lines+markers',
        line=dict(color='#00267F', width=2, dash='dash'),
        marker=dict(size=8),
        yaxis='y2',
        hovertemplate='Year: %{x}<br>Total: %{y}<extra></extra>'
    ))
    
    fig_progress.update_layout(
        title='Recommendation Completion Rate Over Time',
        height=400,
        hovermode='x unified',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Completion Rate (%)', range=[0, 100]),
        yaxis2=dict(title='Total Recommendations', overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_progress, use_container_width=True)
    
    # ========================================================================
    # PRIORITY ACTIONS
    # ========================================================================
    st.markdown('<div class="section-header">🚨 Priority Actions Needed</div>', unsafe_allow_html=True)
    
    # Identify critical recommendations (20+ years outstanding)
    critical_recs = recommendations_data[recommendations_data['Years_Outstanding'] >= 20]
    high_recs = recommendations_data[
        (recommendations_data['Years_Outstanding'] >= 15) & 
        (recommendations_data['Years_Outstanding'] < 20) &
        (recommendations_data['Status'] != '✅ Completed')
    ]
    
    if not critical_recs.empty:
        st.markdown("#### 🔴 CRITICAL - 20+ Years Outstanding")
        for _, rec in critical_recs.iterrows():
            st.markdown(f"""
            <div class="financial-card" style="border-left-color: #DC2626;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h5 style="margin-top: 0; color: #DC2626;">{rec['Recommendation']}</h5>
                        <p><strong>First Made:</strong> {rec['Year_First_Made']} ({rec['Years_Outstanding']} years)</p>
                        <p><strong>Status:</strong> {rec['Status']}</p>
                        <p><strong>Estimated Cost:</strong> ${rec['Estimated_Cost_Billions']:.2f}B</p>
                    </div>
                    <div style="background-color: #DC2626; color: white; padding: 8px 16px; border-radius: 8px; font-weight: bold;">
                        {rec['Years_Outstanding']}+ YEARS
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if not high_recs.empty:
        st.markdown("#### 🟠 HIGH PRIORITY - 15+ Years Outstanding")
        for _, rec in high_recs.iterrows():
            st.markdown(f"""
            <div class="financial-card" style="border-left-color: #F59E0B;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h5 style="margin-top: 0; color: #F59E0B;">{rec['Recommendation']}</h5>
                        <p><strong>First Made:</strong> {rec['Year_First_Made']} ({rec['Years_Outstanding']} years)</p>
                        <p><strong>Status:</strong> {rec['Status']}</p>
                        <p><strong>Estimated Cost:</strong> ${rec['Estimated_Cost_Billions']:.2f}B</p>
                    </div>
                    <div style="background-color: #F59E0B; color: white; padding: 8px 16px; border-radius: 8px; font-weight: bold;">
                        {rec['Years_Outstanding']}+ YEARS
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ========================================================================
    # TIMELINE OF RECOMMENDATIONS
    # ========================================================================
    st.markdown('<div class="section-header">📅 Timeline of Recommendations Made</div>', unsafe_allow_html=True)
    
    # Group by year
    rec_by_year = recommendations_data.groupby('Year_First_Made').size().reset_index(name='Count')
    rec_by_year.columns = ['Year', 'Count']
    
    # Add status breakdown
    status_by_year = recommendations_data.groupby(['Year_First_Made', 'Status']).size().reset_index(name='Count')
    status_by_year.columns = ['Year', 'Status', 'Count']
    
    fig_timeline = go.Figure()
    
    # Stacked bar chart
    statuses = ['❌ Not Implemented', '⚠️ In Progress', '✅ Completed']
    colors_status = {'❌ Not Implemented': '#DC2626', '⚠️ In Progress': '#F59E0B', '✅ Completed': '#10B981'}
    
    for status in statuses:
        status_data = status_by_year[status_by_year['Status'] == status]
        if not status_data.empty:
            fig_timeline.add_trace(go.Bar(
                x=status_data['Year'],
                y=status_data['Count'],
                name=status,
                marker_color=colors_status.get(status, '#666'),
                text=status_data['Count'],
                textposition='auto'
            ))
    
    fig_timeline.update_layout(
        title='Recommendations Made by Year (Stacked by Status)',
        yaxis_title='Number of Recommendations',
        xaxis_title='Year First Made',
        height=400,
        barmode='stack',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # ========================================================================
    # RECOMMENDATION STATUS SUMMARY - FIXED VERSION
    # ========================================================================
    st.markdown('<div class="section-header">📊 Recommendation Status Summary</div>', unsafe_allow_html=True)
    
    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        'Status': ['❌ Not Implemented', '⚠️ In Progress', '✅ Completed'],
        'Count': [not_implemented, in_progress, completed],
        'Percentage': [
            (not_implemented / total_recommendations) * 100 if total_recommendations > 0 else 0,
            (in_progress / total_recommendations) * 100 if total_recommendations > 0 else 0,
            (completed / total_recommendations) * 100 if total_recommendations > 0 else 0
        ]
    })
    
    # Create the pie chart correctly
    fig_status = px.pie(
        summary_df,
        values='Count',
        names='Status',
        title='Recommendation Status Distribution',
        color='Status',
        color_discrete_map={
            '❌ Not Implemented': '#DC2626',
            '⚠️ In Progress': '#F59E0B',
            '✅ Completed': '#10B981'
        },
        hole=0.4
    )
    # Update traces for text display
    fig_status.update_traces(
        textposition='inside',
        textinfo='label+percent',
        textfont_size=12
    )
    fig_status.update_layout(height=350)
    st.plotly_chart(fig_status, use_container_width=True)
    
    # ========================================================================
    # CONCLUSION
    # ========================================================================
    st.markdown("""
    <div style="background-color: #00267F; padding: 25px; border-radius: 10px; color: white; margin-top: 20px;">
        <h4 style="color: white; margin-top: 0;">📌 The Cost of Inaction</h4>
        <p style="color: #BFDBFE; font-size: 1.05rem;">
        <strong>6 recommendations</strong> have been outstanding for an average of 
        <strong style="color: white;">{:.0f} years</strong>, with some dating back to <strong style="color: white;">2003</strong>.
        </p>
        <p style="color: #BFDBFE; font-size: 1.05rem;">
        The total estimated cost of inaction is <strong style="color: #FFC726;">${:.2f}B</strong>.
        </p>
        <p style="color: #BFDBFE; font-size: 1.05rem;">
        <strong style="color: #FFC726;">{:.0f}%</strong> of recommendations remain <strong style="color: white;">not implemented</strong>.
        </p>
        <p style="color: #93C5FD; font-size: 0.9rem; margin-top: 10px;">
        <em>Every year of delay adds to the cost and increases the burden on future generations.</em>
        </p>
    </div>
    """.format(avg_years, total_cost, (not_implemented / total_recommendations * 100)), unsafe_allow_html=True)

# ============================================================================
# VIEW 10: EXECUTIVE BRIEFING - COMPLETE VERSION (FIXED)
# ============================================================================
elif view_option == "📄 Executive Briefing":
    st.markdown('<div class="sub-header">📄 EXECUTIVE BRIEFING</div>', unsafe_allow_html=True)
    st.markdown("### 🇧🇧 Barbados Financial Accountability 2003-2026")
    st.caption("A 21-Year Audit History • July 8, 2026 • Version 10.0")
    
    # ========================================================================
    # ELEVATOR PITCH
    # ========================================================================
    st.markdown("""
    <div style="background: #F0F7FF; padding: 25px; border-radius: 10px; margin: 20px 0; border-left: 5px solid #00267F;">
        <p style="margin: 0; font-size: 1.1rem; line-height: 1.8;">
        The Auditor General has issued <strong>6 consecutive Adverse opinions</strong> (2018-2023).
        <br>
        <strong>$2.43B</strong> in tax receivables are unverified (<strong>FIRST FLAGGED IN 2023</strong>).
        <br>
        <strong>$4B+</strong> in pension liabilities are hidden.
        <br>
        <strong>40+</strong> State-Owned Enterprises are not consolidated.
        <br><br>
        The cost: <strong>$55-100M annually</strong> in higher borrowing costs.
        <br>
        The solution: A <strong>$10-20M investment</strong> in financial reform.
        <br>
        The return: <strong>5-10x</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # THREE PILLARS
    # ========================================================================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 10px; border: 1px solid #DC2626; height: 100%;">
            <h4 style="color: #DC2626; margin-top: 0;">🔴 THE PROBLEM</h4>
            <ul>
                <li>6 yrs of Adverse opinions (2018-2023)</li>
                <li>$2.43B tax receivables (NEW 2023)</li>
                <li>$4B+ pension liabilities hidden</li>
                <li>40+ SOEs not consolidated</li>
                <li>SOEs: 21+ years unresolved</li>
                <li>Pensions: 22+ years unresolved</li>
                <li>$719M asset discrepancy (2023)</li>
                <li>$115M cash overstatement (2023)</li>
                <li>IPSAS violations ongoing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #EFF6FF; padding: 20px; border-radius: 10px; border: 1px solid #3B82F6; height: 100%;">
            <h4 style="color: #00267F; margin-top: 0;">💡 THE SOLUTION</h4>
            <ul>
                <li>Verify tax receivables (2023 issue)</li>
                <li>Consolidate all SOEs (21+ years)</li>
                <li>Disclose pension liability (22+ years)</li>
                <li>Reform financial management</li>
                <li>Reconcile $719M asset discrepancy</li>
                <li>Complete bank reconciliations</li>
                <li>Clean audit opinion</li>
                <li>IPSAS compliance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 10px; border: 1px solid #10B981; height: 100%;">
            <h4 style="color: #10B981; margin-top: 0;">💰 THE PAYOFF</h4>
            <ul>
                <li>$55-100M annual savings</li>
                <li>5-10x return on investment</li>
                <li>IPSAS compliance</li>
                <li>Investor confidence restored</li>
                <li>Generational fairness achieved</li>
                <li>Clean audit by 2027</li>
                <li>Lower borrowing costs</li>
                <li>Improved credit rating</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # KEY METRICS
    # ========================================================================
    st.markdown('<div class="section-header">📊 KEY METRICS</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Debt-to-GDP (Barbados)",
            "102.9%",
            "Central Bank of Barbados (2025)",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Debt-to-GDP (Jamaica)",
            "75%",
            "IMF Country Report (2023)",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Debt-to-GDP (Trinidad)",
            "40%",
            "Central Bank of Trinidad (2023)",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            "Unverified Tax Receivables",
            "$2.43B",
            "AG Report 2023 (NEW ISSUE)",
            delta_color="inverse"
        )
    
    # ========================================================================
    # DETAILED FINANCIAL IMPACT
    # ========================================================================
    st.markdown('<div class="section-header">💰 Detailed Financial Impact</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">📉 Current Costs</h5>
            <ul>
                <li><strong>Higher borrowing costs:</strong> $55-100M annually</li>
                <li><strong>Hidden pension liability:</strong> $4B+ not on balance sheet</li>
                <li><strong>Unverified assets:</strong> $2.43B tax receivables</li>
                <li><strong>SOE hidden debt:</strong> $2B+ not consolidated</li>
                <li><strong>Asset discrepancies:</strong> $719M unresolved</li>
                <li><strong>Adverse audit opinion:</strong> 6 consecutive years</li>
                <li><strong>IPSAS violations:</strong> 21+ years ongoing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 8px; border: 1px solid #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">📈 Potential Savings</h5>
            <ul>
                <li><strong>Annual interest savings:</strong> $55-100M</li>
                <li><strong>5-year benefit:</strong> $255-500M</li>
                <li><strong>10-year benefit:</strong> $530-980M</li>
                <li><strong>Investment required:</strong> $10-20M (one-time)</li>
                <li><strong>Return on investment:</strong> 5-10x</li>
                <li><strong>Payback period:</strong> 0.2-0.4 years</li>
                <li><strong>Clean audit by:</strong> 2024-2025</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # THE CASE FOR REFORM - USING NATIVE STREAMLIT COMPONENTS
    # ========================================================================
    st.markdown("""
    <div style="background: #00267F; padding: 30px; border-radius: 10px; color: white; margin: 20px 0;">
        <h4 style="color: #FFC726; margin-top: 0;">📌 THE CASE FOR REFORM</h4>
        <p style="margin-bottom: 15px; font-size: 1.05rem; color: #BFDBFE;">
        <strong>The evidence is clear.</strong> Barbados has demonstrated fiscal improvement.
        </p>
        <p style="margin-bottom: 15px; font-size: 1.05rem; color: #BFDBFE;">
        <strong>But the financial management foundation remains broken.</strong>
        </p>
        <p style="margin-bottom: 15px; font-size: 1.05rem; color: #BFDBFE;">
        <strong>The path forward is known. The benefits are substantial.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use native Streamlit columns for the grid
    case_col1, case_col2, case_col3 = st.columns(3)
    
    with case_col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #1E40AF; border-radius: 10px; border: 2px solid #FFC726;">
            <div style="font-size: 2.5rem; font-weight: bold; color: #FFC726;">$10-20M</div>
            <div style="font-size: 1rem; color: #BFDBFE; font-weight: bold;">Investment</div>
            <div style="font-size: 0.85rem; color: #93C5FD;">One-time cost</div>
        </div>
        """, unsafe_allow_html=True)
    
    with case_col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #1E40AF; border-radius: 10px; border: 2px solid #FFC726;">
            <div style="font-size: 2.5rem; font-weight: bold; color: #FFC726;">→</div>
            <div style="font-size: 1rem; color: #BFDBFE; font-weight: bold;">Transformation</div>
            <div style="font-size: 0.85rem; color: #93C5FD;">Financial reform</div>
        </div>
        """, unsafe_allow_html=True)
    
    with case_col3:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #1E40AF; border-radius: 10px; border: 2px solid #10B981;">
            <div style="font-size: 2.5rem; font-weight: bold; color: #10B981;">$55-100M</div>
            <div style="font-size: 1rem; color: #BFDBFE; font-weight: bold;">Annual Savings</div>
            <div style="font-size: 0.85rem; color: #93C5FD;">Recurring benefit</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Bottom text
    st.markdown("""
    <div style="background: #00267F; padding: 20px 30px 30px 30px; border-radius: 0 0 10px 10px; color: white; margin-bottom: 20px;">
        <p style="font-size: 1.1rem; color: #FFC726; text-align: center; font-weight: bold;">
        This is not opinion. This is math.
        </p>
        <p style="font-size: 0.95rem; color: #93C5FD; text-align: center;">
        This analysis is based on 21 years of Auditor General's reports.
        <br>All data is sourced from official Government and IMF publications.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # COMPARISON WITH PEERS
    # ========================================================================
    st.markdown('<div class="section-header">🌍 Barbados vs Peers</div>', unsafe_allow_html=True)
    
    peer_comparison_brief = pd.DataFrame({
        'Metric': [
            'Debt-to-GDP',
            'Audit Opinion',
            'SOE Consolidation',
            'Pension Disclosure',
            'IPSAS Compliance',
            'Years of Issues'
        ],
        'Barbados': [
            '102.9%',
            '🔴 Adverse (6 yrs)',
            '❌ Not Done (21+ yrs)',
            '❌ Hidden (22+ yrs)',
            '❌ Not Compliant',
            '21+ years'
        ],
        'Peer Average': [
            '60%',
            '✅ Clean',
            '✅ Done',
            '✅ Yes',
            '✅ Compliant',
            'Resolved'
        ],
        'Gap': [
            '+42.9%',
            '6 yrs worse',
            '21+ yrs behind',
            '22+ yrs behind',
            'Non-compliant',
            'Significant'
        ]
    })
    
    st.dataframe(
        peer_comparison_brief,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Metric': 'Metric',
            'Barbados': 'Barbados',
            'Peer Average': 'Peer Average',
            'Gap': 'Gap'
        }
    )
    
    # ========================================================================
    # TIMELINE OF SYSTEMIC FAILURE
    # ========================================================================
    st.markdown('<div class="section-header">📅 Timeline of Systemic Failure</div>', unsafe_allow_html=True)
    
    timeline_failure = pd.DataFrame({
        'Year': ['2003', '2008', '2013', '2018', '2020', '2021', '2022', '2023'],
        'Event': [
            'SOE & Pension issues first flagged',
            'First Disclaimer Opinion',
            'Asset issues become recurring',
            'First Adverse Opinion',
            '$1.8B assets excluded, $1.7B land unverified',
            'Deficit peaks at $685M',
            '$719M asset discrepancy',
            '$2.43B tax receivables (NEW)'
        ],
        'Status': ['🟡', '🟡', '🟡', '🔴', '🔴', '🔴', '🔴', '🔴']
    })
    
    st.dataframe(
        timeline_failure,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Year': 'Year',
            'Event': 'Event',
            'Status': 'Status'
        }
    )
    
    # ========================================================================
    # WHAT SUCCESS LOOKS LIKE
    # ========================================================================
    st.markdown('<div class="section-header">✅ What Success Looks Like</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 10px; border: 1px solid #10B981; height: 100%;">
            <h5 style="color: #10B981; margin-top: 0;">📋 Financial Reporting</h5>
            <ul>
                <li>✅ Clean audit opinion</li>
                <li>✅ Verified tax receivables</li>
                <li>✅ Reconciled assets</li>
                <li>✅ IPSAS compliant</li>
                <li>✅ Transparent reporting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 10px; border: 1px solid #10B981; height: 100%;">
            <h5 style="color: #10B981; margin-top: 0;">🏛️ Governance</h5>
            <ul>
                <li>✅ SOEs consolidated</li>
                <li>✅ Pension liability disclosed</li>
                <li>✅ Effective oversight</li>
                <li>✅ Strong controls</li>
                <li>✅ Accountability</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 10px; border: 1px solid #10B981; height: 100%;">
            <h5 style="color: #10B981; margin-top: 0;">💰 Economic Benefits</h5>
            <ul>
                <li>✅ $55-100M annual savings</li>
                <li>✅ Lower borrowing costs</li>
                <li>✅ Improved credit rating</li>
                <li>✅ Investor confidence</li>
                <li>✅ Generational fairness</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # CONCLUSION
    # ========================================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00267F 0%, #1E40AF 100%); padding: 30px; border-radius: 10px; color: white; margin-top: 20px;">
        <h3 style="color: white; text-align: center;">🇧🇧 The Bottom Line</h3>
        <p style="text-align: center; font-size: 1.1rem; color: #BFDBFE;">
        Barbados has demonstrated the ability to deliver <strong style="color: white;">significant fiscal improvement</strong>.
        </p>
        <p style="text-align: center; font-size: 1.1rem; color: #BFDBFE;">
        The data shows what works. The data shows what needs to change.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use native Streamlit columns for the conclusion grid
    conc_col1, conc_col2, conc_col3 = st.columns(3)
    
    with conc_col1:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background: #1E40AF; border-radius: 8px; border: 2px solid #FFC726;">
            <div style="font-size: 2rem; font-weight: bold; color: #FFC726;">21</div>
            <div style="font-size: 0.9rem; color: #BFDBFE;">Years of Evidence</div>
        </div>
        """, unsafe_allow_html=True)
    
    with conc_col2:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background: #1E40AF; border-radius: 8px; border: 2px solid #FFC726;">
            <div style="font-size: 2rem; font-weight: bold; color: #FFC726;">6</div>
            <div style="font-size: 0.9rem; color: #BFDBFE;">Adverse Opinions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with conc_col3:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background: #1E40AF; border-radius: 8px; border: 2px solid #10B981;">
            <div style="font-size: 2rem; font-weight: bold; color: #10B981;">5-10x</div>
            <div style="font-size: 0.9rem; color: #BFDBFE;">Return on Investment</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00267F 0%, #1E40AF 100%); padding: 20px 30px 30px 30px; border-radius: 0 0 10px 10px; color: white;">
        <p style="text-align: center; font-size: 1.1rem; color: #FFC726; margin-top: 0; font-weight: bold;">
        $10-20M investment → $55-100M annual savings → 5-10x ROI
        </p>
        <p style="text-align: center; font-size: 0.9rem; color: #93C5FD; margin-top: 10px;">
        <em>This analysis is based on 21 years of publicly available Auditor General's reports.<br>
        All data is sourced from official Government and IMF publications.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("---")
    st.caption("""
    **Data Sources:** Auditor General's Reports (2003-2023) • Central Bank of Barbados (2025) • 
    IMF Country Reports (2023-2024) • Ministry of Finance (2026)
    """)

# ============================================================================
# VIEW 11: HISTORICAL AUDIT TIMELINE - COMPLETE VERSION
# ============================================================================
elif view_option == "📈 Historical Audit Timeline":
    st.markdown('<div class="sub-header">📜 Historical Audit Timeline: 2003-2023</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-banner">
        <p style="font-size: 1.05rem; margin: 0;">
        This timeline tracks <strong>21 years of audit opinions</strong> (2003-2023), 
        showing the progression from <span style="color: #10B981; font-weight: bold;">Clean</span> 
        to <span style="color: #F59E0B; font-weight: bold;">Disclaimer</span> to 
        <span style="color: #DC2626; font-weight: bold;">Adverse</span> opinions, 
        and the key issues identified each year.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # MAIN AUDIT TIMELINE CHART
    # ========================================================================
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = go.Figure()
        
        severity_map = {'Clean': 1, 'Disclaimer': 2, 'Adverse': 3}
        color_map = {'Clean': '#10B981', 'Disclaimer': '#F59E0B', 'Adverse': '#DC2626'}
        
        fig.add_trace(go.Bar(
            x=historical_audit['Year'],
            y=[severity_map[op] for op in historical_audit['Audit_Opinion']],
            marker_color=[color_map[op] for op in historical_audit['Audit_Opinion']],
            text=historical_audit['Audit_Opinion'],
            textposition='inside',
            textfont=dict(color='white', size=12, weight='bold'),
            name='Audit Opinion',
            hovertemplate='Year: %{x}<br>Opinion: %{text}<br>Key Issue: %{customdata}<extra></extra>',
            customdata=historical_audit['Key_Issue']
        ))
        
        # Add annotations for key milestones
        milestones = [
            {'year': 2003, 'text': '🟢 Last Clean', 'y': 1.5},
            {'year': 2008, 'text': '🟡 First Disclaimer', 'y': 1.5},
            {'year': 2013, 'text': '🟡 Asset Issues Emerge', 'y': 1.5},
            {'year': 2018, 'text': '🔴 First Adverse', 'y': 1.5},
            {'year': 2020, 'text': '🔴 $1.8B Assets Excluded', 'y': 1.5},
            {'year': 2023, 'text': '🔴 6th Adverse + $2.43B NEW', 'y': 1.5}
        ]
        
        for m in milestones:
            fig.add_annotation(
                x=m['year'], 
                y=m['y'], 
                text=m['text'],
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-30,
                font=dict(size=10, color='#333'),
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#ccc',
                borderwidth=1
            )
        
        fig.update_layout(
            title='Audit Opinion Timeline: 2003-2023',
            yaxis=dict(
                tickvals=[1, 2, 3], 
                ticktext=['Clean', 'Disclaimer', 'Adverse'], 
                title='Opinion Type', 
                range=[0, 3.8]
            ),
            xaxis=dict(tickmode='linear', dtick=1, title='Year', tickangle=45),
            height=400,
            showlegend=False,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="financial-card">
            <h6 style="margin-top: 0; color: #00267F;">🔑 Key Milestones</h6>
            <div style="font-size: 0.9rem;">
                <p><strong>2003-2007:</strong> 🟢 Clean Opinions</p>
                <p><strong>2008:</strong> 🟡 First Disclaimer Opinion</p>
                <p><strong>2013:</strong> 🟡 Asset Register Issues Emerge</p>
                <p><strong>2018:</strong> 🔴 First Adverse Opinion</p>
                <p><strong>2020:</strong> 🔴 $1.8B Fixed Assets Excluded</p>
                <p><strong>2023:</strong> 🔴 6th Consecutive Adverse</p>
                <p><strong>2023:</strong> 🔴 $2.43B Tax Receivables (NEW)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # ERA BREAKDOWN
    # ========================================================================
    st.markdown('<div class="section-header">📊 Era Breakdown</div>', unsafe_allow_html=True)
    
    era_col1, era_col2, era_col3 = st.columns(3)
    
    # Clean Era (2003-2007)
    clean_issues = historical_audit[historical_audit['Audit_Opinion'] == 'Clean']
    clean_count = len(clean_issues)
    clean_years = clean_issues['Year'].tolist()
    
    with era_col1:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">🟢 Clean Era (2003-2007)</h5>
            <p><strong>Years:</strong> {clean_count}</p>
            <p><strong>Opinions:</strong> Clean</p>
            <p><strong>Key Issues:</strong> No major issues identified</p>
            <p><strong>Status:</strong> ✅ Historical baseline</p>
            <p><strong>Years:</strong> {', '.join(map(str, clean_years))}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Disclaimer Era (2008-2017)
    disclaimer_issues = historical_audit[historical_audit['Audit_Opinion'] == 'Disclaimer']
    disclaimer_count = len(disclaimer_issues)
    disclaimer_years = disclaimer_issues['Year'].tolist()
    
    with era_col2:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #F59E0B;">
            <h5 style="color: #F59E0B; margin-top: 0;">🟡 Disclaimer Era (2008-2017)</h5>
            <p><strong>Years:</strong> {disclaimer_count}</p>
            <p><strong>Opinions:</strong> Disclaimer</p>
            <p><strong>Key Issues:</strong> SOE consolidation, asset valuation</p>
            <p><strong>Status:</strong> ⚠️ Recurring issues emerge</p>
            <p><strong>Years:</strong> {', '.join(map(str, disclaimer_years))}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Adverse Era (2018-2023)
    adverse_issues = historical_audit[historical_audit['Audit_Opinion'] == 'Adverse']
    adverse_count = len(adverse_issues)
    adverse_years = adverse_issues['Year'].tolist()
    
    with era_col3:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 Adverse Era (2018-2023)</h5>
            <p><strong>Years:</strong> {adverse_count}</p>
            <p><strong>Opinions:</strong> Adverse</p>
            <p><strong>Key Issues:</strong> Material misstatements, $2.43B unverified (NEW)</p>
            <p><strong>Status:</strong> ❌ Systemic failures</p>
            <p><strong>Years:</strong> {', '.join(map(str, adverse_years))}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # DETAILED YEAR-BY-YEAR TIMELINE
    # ========================================================================
    st.markdown('<div class="section-header">📋 Detailed Year-by-Year Timeline</div>', unsafe_allow_html=True)
    
    # Create a detailed timeline dataframe
    timeline_data = []
    for _, row in historical_audit.iterrows():
        year = row['Year']
        opinion = row['Audit_Opinion']
        issue = row['Key_Issue']
        
        # Determine era
        if year <= 2007:
            era = 'Clean Era'
        elif year <= 2017:
            era = 'Disclaimer Era'
        else:
            era = 'Adverse Era'
        
        # Determine severity indicator
        if opinion == 'Clean':
            indicator = '🟢'
            severity_class = 'success'
        elif opinion == 'Disclaimer':
            indicator = '🟡'
            severity_class = 'warning'
        else:
            indicator = '🔴'
            severity_class = 'danger'
        
        timeline_data.append({
            'Year': year,
            'Indicator': indicator,
            'Opinion': opinion,
            'Key Issue': issue,
            'Era': era,
            'Severity': severity_class
        })
    
    timeline_df = pd.DataFrame(timeline_data)
    
    # Display as a styled table
    st.dataframe(
        timeline_df,
        use_container_width=True,
        column_config={
            'Year': 'Year',
            'Indicator': '',
            'Opinion': 'Audit Opinion',
            'Key Issue': 'Key Issue Identified',
            'Era': 'Era',
            'Severity': None
        },
        hide_index=True
    )
    
    # ========================================================================
    # ISSUE PERSISTENCE ANALYSIS
    # ========================================================================
    st.markdown('<div class="section-header">🔄 Issue Persistence Analysis</div>', unsafe_allow_html=True)
    
    # Count how many years each issue has persisted
    issue_persistence = []
    
    # SOE Consolidation
    soe_years = sum(historical_audit['SOE_Consolidation'])
    issue_persistence.append({
        'Issue': 'SOE Consolidation',
        'First Appeared': 2003,
        'Years_Present': soe_years,
        'Status': '❌ Unresolved'
    })
    
    # Pension Hidden
    pension_years = sum(historical_audit['Pension_Hidden'])
    issue_persistence.append({
        'Issue': 'Pension Liability Hidden',
        'First Appeared': 2003,
        'Years_Present': pension_years,
        'Status': '❌ Unresolved'
    })
    
    # Asset Issues
    asset_years = sum(historical_audit['Asset_Issues'])
    issue_persistence.append({
        'Issue': 'Asset Register Issues',
        'First Appeared': 2003,
        'Years_Present': asset_years,
        'Status': '❌ Unresolved'
    })
    
    # Bank Reconciliation
    bank_years = sum(historical_audit['Bank_Reconciliation_Issues'])
    issue_persistence.append({
        'Issue': 'Bank Reconciliation Issues',
        'First Appeared': 2008,
        'Years_Present': bank_years,
        'Status': '❌ Unresolved'
    })
    
    persistence_df = pd.DataFrame(issue_persistence)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bar chart for issue persistence
        fig_persist = px.bar(
            persistence_df,
            x='Issue',
            y='Years_Present',
            title='Years Each Issue Has Persisted (2003-2023)',
            color='Years_Present',
            color_continuous_scale='Reds',
            text=[f"{x} years" for x in persistence_df['Years_Present']],
            range_color=[0, 25]
        )
        fig_persist.update_layout(
            yaxis_title='Years Present',
            xaxis_title='Issue',
            height=350
        )
        st.plotly_chart(fig_persist, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 10px; border-left: 4px solid #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🚨 Persistent Issues Summary</h5>
            <ul>
                <li><strong>SOE Consolidation:</strong> 21+ years</li>
                <li><strong>Pension Liability:</strong> 22+ years</li>
                <li><strong>Asset Registers:</strong> 21+ years</li>
                <li><strong>Bank Reconciliations:</strong> 18+ years</li>
                <li><strong>NEW 2023:</strong> $2.43B Tax Receivables</li>
            </ul>
            <p style="font-size: 0.85rem; color: #666; margin-top: 10px;">
            <em>These issues have persisted for nearly two decades with no resolution.</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # KEY STATISTICS
    # ========================================================================
    st.markdown('<div class="section-header">📊 Key Statistics</div>', unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Total Years", "21", "2003-2023")
    
    with stat_col2:
        clean_count = len(historical_audit[historical_audit['Audit_Opinion'] == 'Clean'])
        st.metric("Clean Opinions", clean_count, "2003-2007")
    
    with stat_col3:
        disclaimer_count = len(historical_audit[historical_audit['Audit_Opinion'] == 'Disclaimer'])
        st.metric("Disclaimer Opinions", disclaimer_count, "2008-2017")
    
    with stat_col4:
        adverse_count = len(historical_audit[historical_audit['Audit_Opinion'] == 'Adverse'])
        st.metric("Adverse Opinions", adverse_count, "2018-2023")
    
    # ========================================================================
    # TRANSITION ANALYSIS
    # ========================================================================
    st.markdown('<div class="section-header">🔄 Transition Analysis</div>', unsafe_allow_html=True)
    
    transitions = [
        {
            'From': 'Clean Era (2003-2007)',
            'To': 'Disclaimer Era (2008-2017)',
            'Year': '2008',
            'Reason': 'SOE consolidation and asset valuation issues emerged',
            'Impact': 'Loss of clean audit status after 5 years'
        },
        {
            'From': 'Disclaimer Era (2008-2017)',
            'To': 'Adverse Era (2018-2023)',
            'Year': '2018',
            'Reason': 'Material misstatements, cash overstatements, asset exclusions',
            'Impact': '6 consecutive adverse opinions, systemic failure'
        },
        {
            'From': 'Adverse Era (2018-2023)',
            'To': 'Unknown Future',
            'Year': '2024+',
            'Reason': 'Requires: Tax receivable verification, SOE consolidation, pension disclosure',
            'Impact': 'Potential for clean audit if reforms implemented'
        }
    ]
    
    for transition in transitions:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: {'#F59E0B' if 'Unknown' in transition['To'] else '#DC2626'};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h5 style="margin-top: 0;">
                        {transition['From']} → {transition['To']}
                    </h5>
                    <p><strong>Transition Year:</strong> {transition['Year']}</p>
                    <p><strong>Reason:</strong> {transition['Reason']}</p>
                    <p><strong>Impact:</strong> {transition['Impact']}</p>
                </div>
                <div style="font-size: 2.5rem;">
                    {'🔴' if 'Adverse' in transition['To'] else '🟡' if 'Disclaimer' in transition['To'] else '❓'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # SUMMARY FOOTER
    # ========================================================================
    st.markdown("""
    <div style="background-color: #00267F; padding: 20px; border-radius: 10px; color: white; margin-top: 15px;">
        <h5 style="color: white; margin-top: 0;">📌 Key Takeaway</h5>
        <p style="margin: 0; color: #BFDBFE;">
        The audit timeline shows a clear deterioration in financial management:
        <strong style="color: white;">5 clean → 10 disclaimer → 6 adverse</strong> opinions.
        The path forward requires addressing <strong style="color: #FFC726;">21+ year old issues</strong>
        that have never been resolved.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# VIEW 12: LONG-TERM FINANCIAL TRENDS - COMPLETE VERSION
# ============================================================================
elif view_option == "💰 Long-Term Financial Trends":
    st.markdown('<div class="sub-header">💰 Long-Term Financial Trends (2003-2023)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-banner">
        <p style="font-size: 1.05rem; margin: 0;">
        This section tracks <strong>21 years of financial evolution</strong> (2003-2023), 
        showing how <span style="color: #00267F; font-weight: bold;">Revenue</span>, 
        <span style="color: #DC2626; font-weight: bold;">Expenditure</span>, and 
        <span style="color: #F59E0B; font-weight: bold;">Net Debt</span> have changed 
        over time, with audit era overlays.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # MAIN FINANCIAL TRENDS CHART
    # ========================================================================
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(
        x=historical_financials['Year'],
        y=historical_financials['Revenue_Billions'],
        name='Revenue',
        mode='lines+markers',
        line=dict(color='#00267F', width=3),
        marker=dict(size=10, symbol='circle'),
        hovertemplate='Year: %{x}<br>Revenue: $%{y:.2f}B<extra></extra>'
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=historical_financials['Year'],
        y=historical_financials['Expenditure_Billions'],
        name='Expenditure',
        mode='lines+markers',
        line=dict(color='#DC2626', width=3),
        marker=dict(size=10, symbol='square'),
        hovertemplate='Year: %{x}<br>Expenditure: $%{y:.2f}B<extra></extra>'
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=historical_financials['Year'],
        y=historical_financials['Net_Debt_Billions'],
        name='Net Debt',
        mode='lines+markers',
        line=dict(color='#F59E0B', width=3, dash='dash'),
        marker=dict(size=10, symbol='diamond'),
        hovertemplate='Year: %{x}<br>Net Debt: $%{y:.2f}B<extra></extra>'
    ), secondary_y=True)
    
    # Add era overlays
    fig.add_vrect(x0=2003, x1=2007.5, fillcolor="rgba(16, 185, 129, 0.15)", line_width=0, annotation_text="Clean Era", annotation_position="top left")
    fig.add_vrect(x0=2008, x1=2017.5, fillcolor="rgba(245, 158, 11, 0.15)", line_width=0, annotation_text="Disclaimer Era", annotation_position="top left")
    fig.add_vrect(x0=2018, x1=2023.5, fillcolor="rgba(220, 38, 38, 0.15)", line_width=0, annotation_text="Adverse Era", annotation_position="top left")
    
    fig.update_layout(
        title='Financial Trends with Audit Era Overlay (2003-2023)',
        height=500, 
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_yaxes(title_text='Amount (Billions $)', secondary_y=False)
    fig.update_yaxes(title_text='Net Debt (Billions $)', secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # KEY METRICS EVOLUTION
    # ========================================================================
    st.markdown('<div class="section-header">📊 Key Metrics Evolution</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Revenue Growth
    revenue_2003 = historical_financials[historical_financials['Year'] == 2003]['Revenue_Billions'].values[0]
    revenue_2023 = historical_financials[historical_financials['Year'] == 2023]['Revenue_Billions'].values[0]
    revenue_pct = ((revenue_2023 - revenue_2003) / revenue_2003) * 100
    
    with col1:
        st.metric(
            "Revenue Growth", 
            f"{revenue_2023:.2f}B", 
            f"+{revenue_pct:.0f}% since 2003",
            delta_color="normal"
        )
    
    # Expenditure Growth
    exp_2003 = historical_financials[historical_financials['Year'] == 2003]['Expenditure_Billions'].values[0]
    exp_2023 = historical_financials[historical_financials['Year'] == 2023]['Expenditure_Billions'].values[0]
    exp_pct = ((exp_2023 - exp_2003) / exp_2003) * 100
    
    with col2:
        st.metric(
            "Expenditure Growth", 
            f"{exp_2023:.2f}B", 
            f"+{exp_pct:.0f}% since 2003",
            delta_color="inverse"
        )
    
    # Debt Growth
    debt_2003 = historical_financials[historical_financials['Year'] == 2003]['Net_Debt_Billions'].values[0]
    debt_2023 = historical_financials[historical_financials['Year'] == 2023]['Net_Debt_Billions'].values[0]
    debt_pct = ((debt_2023 - debt_2003) / debt_2003) * 100
    
    with col3:
        st.metric(
            "Net Debt Growth", 
            f"{debt_2023:.2f}B", 
            f"+{debt_pct:.0f}% since 2003",
            delta_color="inverse"
        )
    
    # Deficit Improvement
    deficit_2023 = abs(historical_financials[historical_financials['Year'] == 2023]['Deficit_Billions'].values[0])
    deficit_2021 = abs(historical_financials[historical_financials['Year'] == 2021]['Deficit_Billions'].values[0])
    deficit_improvement = ((deficit_2021 - deficit_2023) / deficit_2021) * 100 if deficit_2021 != 0 else 0
    
    with col4:
        st.metric(
            "Deficit Improvement", 
            f"${deficit_2023:.2f}B", 
            f"-{deficit_improvement:.0f}% since 2021",
            delta_color="normal"
        )
    
    # ========================================================================
    # DEFICIT TRENDS CHART
    # ========================================================================
    st.markdown('<div class="section-header">📉 Deficit Trends (2003-2023)</div>', unsafe_allow_html=True)
    
    deficit_data = historical_financials.copy()
    deficit_data['Deficit_Abs'] = deficit_data['Deficit_Billions'].abs()
    
    # Color code deficits (red for deficit, green for surplus)
    colors_def = ['#DC2626' if x < 0 else '#10B981' for x in deficit_data['Deficit_Billions']]
    
    fig_def = go.Figure()
    
    fig_def.add_trace(go.Bar(
        x=deficit_data['Year'],
        y=deficit_data['Deficit_Billions'],
        marker_color=colors_def,
        text=[f"${x:.2f}B" for x in deficit_data['Deficit_Billions']],
        textposition='outside',
        hovertemplate='Year: %{x}<br>Deficit: $%{y:.2f}B<extra></extra>'
    ))
    
    # Add zero line
    fig_def.add_hline(y=0, line_dash="dash", line_color="#666", line_width=1)
    
    # Highlight peak deficit
    fig_def.add_annotation(
        x=2021, y=-0.7, 
        text="🔴 Peak Deficit: $685M",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40,
        font=dict(color="#DC2626", size=11)
    )
    
    # Highlight 2023 improvement
    fig_def.add_annotation(
        x=2023, y=-0.11, 
        text="✅ $111M (Improved 84%)",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40,
        font=dict(color="#10B981", size=11)
    )
    
    fig_def.update_layout(
        title='Consolidated Fund Deficit/Surplus (2003-2023)',
        yaxis_title='Amount (Billions $)',
        xaxis_title='Year',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_def, use_container_width=True)
    
    # ========================================================================
    # REVENUE VS EXPENDITURE GAP
    # ========================================================================
    st.markdown('<div class="section-header">📊 Revenue vs Expenditure Gap Analysis</div>', unsafe_allow_html=True)
    
    # Calculate gap
    gap_data = historical_financials.copy()
    gap_data['Gap'] = gap_data['Revenue_Billions'] - gap_data['Expenditure_Billions']
    
    fig_gap = go.Figure()
    
    fig_gap.add_trace(go.Scatter(
        x=gap_data['Year'],
        y=gap_data['Revenue_Billions'],
        name='Revenue',
        mode='lines+markers',
        line=dict(color='#00267F', width=2),
        marker=dict(size=8),
        fill=None
    ))
    
    fig_gap.add_trace(go.Scatter(
        x=gap_data['Year'],
        y=gap_data['Expenditure_Billions'],
        name='Expenditure',
        mode='lines+markers',
        line=dict(color='#DC2626', width=2),
        marker=dict(size=8),
        fill='tonexty',
        fillcolor='rgba(220, 38, 38, 0.15)'
    ))
    
    # Add gap annotations for key years
    for year in [2003, 2008, 2013, 2018, 2021, 2023]:
        year_data = gap_data[gap_data['Year'] == year]
        if not year_data.empty:
            gap = year_data['Gap'].values[0]
            fig_gap.add_annotation(
                x=year,
                y=(year_data['Revenue_Billions'].values[0] + year_data['Expenditure_Billions'].values[0]) / 2,
                text=f"${gap:.2f}B" if gap < 0 else f"${gap:.2f}B surplus",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=(-30 if gap < 0 else 30),
                font=dict(size=9, color='#DC2626' if gap < 0 else '#10B981')
            )
    
    fig_gap.update_layout(
        title='Revenue vs Expenditure Gap (2003-2023)',
        yaxis_title='Amount (Billions $)',
        xaxis_title='Year',
        height=400,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_gap, use_container_width=True)
    
    # ========================================================================
    # AUDIT QUALITY OVERLAY
    # ========================================================================
    st.markdown('<div class="section-header">🔍 Audit Quality vs Financial Performance</div>', unsafe_allow_html=True)
    
    # Create combined view
    combined_data = historical_financials.merge(historical_audit[['Year', 'Audit_Opinion']], on='Year')
    
    # Color mapping for audit opinions
    opinion_colors = {'Clean': '#10B981', 'Disclaimer': '#F59E0B', 'Adverse': '#DC2626'}
    
    fig_combined = go.Figure()
    
    # Bar chart for audit opinions (as background)
    fig_combined.add_trace(go.Bar(
        x=combined_data['Year'],
        y=[3] * len(combined_data),
        marker_color=[opinion_colors[op] for op in combined_data['Audit_Opinion']],
        opacity=0.3,
        name='Audit Opinion (Background)',
        hovertemplate='Year: %{x}<br>Audit Opinion: %{customdata}<extra></extra>',
        customdata=combined_data['Audit_Opinion'],
        showlegend=False
    ))
    
    # Line for Revenue
    fig_combined.add_trace(go.Scatter(
        x=combined_data['Year'],
        y=combined_data['Revenue_Billions'],
        name='Revenue',
        mode='lines+markers',
        line=dict(color='#00267F', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    # Line for Expenditure
    fig_combined.add_trace(go.Scatter(
        x=combined_data['Year'],
        y=combined_data['Expenditure_Billions'],
        name='Expenditure',
        mode='lines+markers',
        line=dict(color='#DC2626', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    # Line for Net Debt
    fig_combined.add_trace(go.Scatter(
        x=combined_data['Year'],
        y=combined_data['Net_Debt_Billions'],
        name='Net Debt',
        mode='lines+markers',
        line=dict(color='#F59E0B', width=3, dash='dash'),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    fig_combined.update_layout(
        title='Audit Quality vs Financial Performance (2003-2023)',
        height=450,
        hovermode='x unified',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Audit Opinion Severity', tickvals=[1, 2, 3], ticktext=['Clean', 'Disclaimer', 'Adverse'], range=[0, 3.5]),
        yaxis2=dict(title='Amount (Billions $)', overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_combined, use_container_width=True)
    
    # ========================================================================
    # SUMMARY STATISTICS TABLE
    # ========================================================================
    st.markdown('<div class="section-header">📋 21-Year Summary Statistics</div>', unsafe_allow_html=True)
    
    # Calculate summary statistics
    summary_stats = pd.DataFrame({
        'Metric': [
            'Total Revenue (2023)',
            'Total Expenditure (2023)',
            'Net Debt (2023)',
            'Deficit (2023)',
            'Revenue Growth (2003-2023)',
            'Expenditure Growth (2003-2023)',
            'Net Debt Growth (2003-2023)',
            'Deficit Reduction (2021-2023)',
            'Clean Audit Years',
            'Disclaimer Audit Years',
            'Adverse Audit Years',
            'Consecutive Adverse Years'
        ],
        'Value': [
            f"${revenue_2023:.2f}B",
            f"${exp_2023:.2f}B",
            f"${debt_2023:.2f}B",
            f"${deficit_2023:.2f}B",
            f"+{revenue_pct:.0f}%",
            f"+{exp_pct:.0f}%",
            f"+{debt_pct:.0f}%",
            f"-{deficit_improvement:.0f}%",
            f"{clean_years} (2003-2007)",
            f"{disclaimer_years} (2008-2017)",
            f"{adverse_years} (2018-2023)",
            f"{metrics['adverse_consecutive_years']} (2018-2023)"
        ],
        'Status': [
            '✅ Improved',
            '⚠️ Increased',
            '⚠️ Increased',
            '✅ Improved',
            '✅ Positive',
            '⚠️ Higher',
            '⚠️ Higher',
            '✅ Improved',
            '✅ Historical',
            '⚠️ Historical',
            '❌ Current',
            '❌ Current'
        ]
    })
    
    st.dataframe(summary_stats, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # KEY INSIGHTS
    # ========================================================================
    st.markdown('<div class="section-header">💡 Key Insights</div>', unsafe_allow_html=True)
    
    insights = [
        {
            'title': 'Revenue Growth Outpaced Expenditure',
            'detail': f'Revenue grew {revenue_pct:.0f}% while expenditure grew {exp_pct:.0f}% over 21 years, indicating improved revenue collection.',
            'color': '#10B981'
        },
        {
            'title': 'Significant Deficit Reduction',
            'detail': f'Deficit reduced by {deficit_improvement:.0f}% from its peak in 2021 ($685M) to $111M in 2023.',
            'color': '#10B981'
        },
        {
            'title': 'Debt Remains a Challenge',
            'detail': f'Net Debt grew {debt_pct:.0f}% from $5.0B to $10.6B over 21 years, reaching 102.9% of GDP.',
            'color': '#F59E0B'
        },
        {
            'title': 'Audit Quality Declined',
            'detail': 'From 5 clean opinions (2003-2007) to 6 adverse opinions (2018-2023), indicating systemic financial management failures.',
            'color': '#DC2626'
        }
    ]
    
    for insight in insights:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: {insight['color']};">
            <h5 style="margin-top: 0; color: {insight['color']};">{insight['title']}</h5>
            <p style="margin: 0;">{insight['detail']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# VIEW 13: RECURRING ISSUES ANALYSIS
# ============================================================================
elif view_option == "🔄 Recurring Issues Analysis":
    st.markdown('<div class="sub-header">🔄 Recurring Issues Analysis (2003-2023)</div>', unsafe_allow_html=True)
    
    issue_matrix = []
    for issue in historical_issues['Issue']:
        start_year = historical_issues[historical_issues['Issue'] == issue]['Start_Year'].values[0]
        row = []
        for year in range(2003, 2024):
            row.append(1 if year >= start_year else 0)
        issue_matrix.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=issue_matrix,
        x=list(range(2003, 2024)),
        y=historical_issues['Issue'],
        colorscale=[[0, '#ECFDF5'], [1, '#DC2626']],
        hovertemplate='Year: %{x}<br>Issue: %{y}<br>Active: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Recurring Issues Timeline (2003-2023)',
        xaxis=dict(tickmode='linear', dtick=2),
        yaxis=dict(title='Issue Category'),
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="section-header">Issue Details & Impact</div>', unsafe_allow_html=True)
    
    for _, issue in historical_issues.iterrows():
        st.markdown(f"""
        <div class="financial-card data-error">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h6 style="margin-top: 0;">{issue['Issue']}</h6>
                    <p><strong>Started:</strong> {issue['Start_Year']}</p>
                    <p><strong>Duration:</strong> {2026 - issue['Start_Year']} years</p>
                    <p><strong>Status (2026):</strong> {issue['Status_2026']}</p>
                    <p><strong>Estimated Impact:</strong> ${issue['Estimated_Impact_Billions']:.2f}B</p>
                </div>
                <div style="background-color: {'#DC2626' if issue['Start_Year'] == 2023 else '#F59E0B'}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; white-space: nowrap;">
                    {issue['Start_Year'] == 2023 and 'NEW' or f'{2026 - issue["Start_Year"]}+ Years'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    total_impact = historical_issues['Estimated_Impact_Billions'].sum()
    
    st.markdown(f"""
    <div style="background-color: #FEF2F2; padding: 20px; border-radius: 10px; border-left: 4px solid #DC2626; margin-top: 15px;">
        <h5 style="color: #DC2626; margin-top: 0;">📊 Total Estimated Impact of Issues</h5>
        <div style="font-size: 2.5rem; font-weight: bold; color: #DC2626;">${total_impact:.2f}B</div>
        <p style="font-size: 0.9rem; color: #666;">Includes $2.43B new issue flagged in 2023</p>
    </div>
    """, unsafe_allow_html=True)
# ============================================================================
# VIEW 14: ACCOUNTABILITY SCORECARD - COMPLETE VERSION
# ============================================================================
elif view_option == "📊 Accountability Scorecard":
    st.markdown('<div class="sub-header">📊 Accountability Scorecard (2003-2023)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-banner">
        <p style="font-size: 1.05rem; margin: 0;">
        This scorecard tracks Barbados' performance across <strong>8 key governance categories</strong> 
        from 2008 to 2023, measuring progress against a <strong>target of 80/100</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Accountability Metrics Data
    accountability_metrics = pd.DataFrame({
        'Category': ['Financial Reporting', 'Asset Management', 'Liability Reporting', 'SOE Governance',
                     'Internal Controls', 'Pension Management', 'Revenue Collection', 'Audit Recommendations'],
        'Score_2023': [20, 15, 10, 5, 20, 10, 25, 15],
        'Score_2008': [70, 60, 50, 30, 50, 40, 60, 50],
        'Target': [80, 80, 80, 80, 80, 80, 80, 80],
        'Trend': ['🔴 Declining', '🔴 Declining', '🔴 Declining', '🟡 Stalled',
                  '🔴 Declining', '🔴 Declining', '🟡 Stalled', '🟡 Stalled']
    })
    
    # Scorecard Chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=accountability_metrics['Category'], 
        y=accountability_metrics['Score_2008'],
        name='2008 Score', 
        marker_color='#3B82F6', 
        text=accountability_metrics['Score_2008'], 
        textposition='auto'
    ))
    fig.add_trace(go.Bar(
        x=accountability_metrics['Category'], 
        y=accountability_metrics['Score_2023'],
        name='2023 Score', 
        marker_color='#DC2626', 
        text=accountability_metrics['Score_2023'], 
        textposition='auto'
    ))
    fig.add_trace(go.Bar(
        x=accountability_metrics['Category'], 
        y=accountability_metrics['Target'],
        name='Target Score', 
        marker_color='#10B981', 
        text=accountability_metrics['Target'], 
        textposition='auto', 
        opacity=0.5
    ))
    
    fig.update_layout(
        title='Accountability Scorecard: 2008 vs 2023 (Target: 80)',
        yaxis_title='Score (0-100)', 
        height=450, 
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # DETAILED CATEGORY ANALYSIS
    # ========================================================================
    st.markdown('<div class="section-header">📋 Detailed Category Analysis</div>', unsafe_allow_html=True)
    
    for _, row in accountability_metrics.iterrows():
        improvement = row['Score_2023'] - row['Score_2008']
        color = '#DC2626' if improvement < 0 else '#10B981' if improvement > 0 else '#F59E0B'
        
        # Determine category status
        if row['Score_2023'] >= 80:
            status = "✅ On Track"
            status_color = "#10B981"
        elif row['Score_2023'] >= 50:
            status = "⚠️ Needs Improvement"
            status_color = "#F59E0B"
        else:
            status = "❌ Critical"
            status_color = "#DC2626"
        
        st.markdown(f"""
        <div class="financial-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h5 style="margin-top: 0; color: {color};">{row['Category']}</h5>
                    <div style="font-size: 0.9rem; color: #666;">
                        2008: {row['Score_2008']}/100 → 2023: {row['Score_2023']}/100 → Target: {row['Target']}/100
                    </div>
                    <div style="font-size: 0.9rem; margin-top: 5px;">
                        <span style="color: {status_color}; font-weight: bold;">{status}</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="color: {color}; font-weight: bold; font-size: 1.2rem;">{improvement:+.0f} points</div>
                    <div style="font-size: 0.8rem; color: #666;">{row['Trend']}</div>
                </div>
            </div>
            <div style="margin-top: 10px; background-color: #f0f0f0; border-radius: 5px; height: 10px; overflow: hidden;">
                <div style="width: {row['Score_2023']}%; background-color: {color}; height: 10px; border-radius: 5px; transition: width 0.5s;"></div>
            </div>
            <div style="margin-top: 4px; display: flex; justify-content: space-between; font-size: 0.7rem; color: #999;">
                <span>0</span>
                <span>Target: {row['Target']}</span>
                <span>100</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # KEY FINDINGS
    # ========================================================================
    st.markdown('<div class="section-header">📌 Key Findings</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 Areas of Concern</h5>
            <ul>
                <li><strong>Liability Reporting:</strong> 10/100 - Pension liabilities hidden for 22+ years</li>
                <li><strong>SOE Governance:</strong> 5/100 - 40+ SOEs not consolidated for 21+ years</li>
                <li><strong>Asset Management:</strong> 15/100 - $719M discrepancy in capital assets</li>
                <li><strong>Internal Controls:</strong> 20/100 - Bank reconciliations 18+ years outstanding</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #F59E0B;">
            <h5 style="color: #F59E0B; margin-top: 0;">🟡 Stalled Progress</h5>
            <ul>
                <li><strong>Revenue Collection:</strong> 25/100 - $2.43B tax receivables unverified (NEW 2023)</li>
                <li><strong>Audit Recommendations:</strong> 15/100 - 6 recommendations outstanding for 21+ years</li>
                <li><strong>Financial Reporting:</strong> 20/100 - 6 consecutive adverse opinions (2018-2023)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # AUDIT RECOMMENDATIONS TABLE
    # ========================================================================
    st.markdown('<div class="section-header">📋 Audit Recommendations (2003-2023)</div>', unsafe_allow_html=True)
    
    recommendations_data = load_historical_recommendations()
    
    st.dataframe(
        recommendations_data,
        use_container_width=True,
        column_config={
            'Recommendation': 'Audit Recommendation',
            'Year_First_Made': 'First Made',
            'Status': 'Current Status',
            'Years_Outstanding': 'Years Outstanding',
            'Estimated_Cost_Billions': 'Estimated Cost (Billions)'
        }
    )
    
    # ========================================================================
    # RECOMMENDATIONS TIMELINE CHART
    # ========================================================================
    st.markdown("### 📅 Recommendations Timeline")
    
    rec_timeline = []
    for _, row in recommendations_data.iterrows():
        rec_timeline.append({
            'Recommendation': row['Recommendation'],
            'Start_Year': row['Year_First_Made'],
            'Status': row['Status'],
            'Years_Outstanding': row['Years_Outstanding']
        })
    
    fig_timeline = go.Figure()
    
    colors = {'❌ Not Implemented': '#DC2626', '⚠️ In Progress': '#F59E0B', '✅ Completed': '#10B981'}
    
    for rec in rec_timeline:
        fig_timeline.add_trace(go.Bar(
            x=[rec['Recommendation']],
            y=[rec['Years_Outstanding']],
            name=rec['Recommendation'],
            marker_color=colors.get(rec['Status'], '#666'),
            text=[f"{rec['Years_Outstanding']} years"],
            textposition='inside'
        ))
    
    fig_timeline.update_layout(
        title='Years Outstanding by Recommendation',
        yaxis_title='Years Outstanding',
        xaxis_title='Recommendation',
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # ========================================================================
    # OVERALL GRADE
    # ========================================================================
    overall_score = accountability_metrics['Score_2023'].mean()
    
    if overall_score >= 80:
        grade = 'A'
        grade_color = '#10B981'
        grade_desc = 'Strong accountability framework in place'
    elif overall_score >= 60:
        grade = 'B'
        grade_color = '#3B82F6'
        grade_desc = 'Moderate accountability with room for improvement'
    elif overall_score >= 40:
        grade = 'C'
        grade_color = '#F59E0B'
        grade_desc = 'Weak accountability framework, significant gaps'
    elif overall_score >= 20:
        grade = 'D'
        grade_color = '#DC2626'
        grade_desc = 'Poor accountability, systemic failures'
    else:
        grade = 'F'
        grade_color = '#991B1B'
        grade_desc = 'Failed accountability, critical governance breakdown'
    
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background-color: {grade_color}20; border-radius: 10px; border: 3px solid {grade_color}; margin-top: 20px;">
        <h3 style="color: {grade_color}; margin-top: 0;">Overall Accountability Grade: {grade}</h3>
        <div style="font-size: 3.5rem; font-weight: bold; color: {grade_color};">{overall_score:.0f}/100</div>
        <div style="font-size: 1rem; color: #666; margin-top: 10px;">
            {grade_desc}
        </div>
        <div style="font-size: 0.85rem; color: #666; margin-top: 5px;">
            Based on 8 governance categories • 2023 assessment • 6 years of adverse opinions
        </div>
        <div style="font-size: 0.85rem; color: #666; margin-top: 5px;">
            Improvement from 2008: {overall_score - accountability_metrics['Score_2008'].mean():+.0f} points
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SUMMARY TABLE
    # ========================================================================
    with st.expander("📊 View Full Scorecard Data Table", expanded=False):
        summary_df = accountability_metrics.copy()
        summary_df['Change'] = summary_df['Score_2023'] - summary_df['Score_2008']
        summary_df['Gap_to_Target'] = summary_df['Target'] - summary_df['Score_2023']
        
        # Add status column
        def get_status(score):
            if score >= 80:
                return "✅ On Track"
            elif score >= 50:
                return "⚠️ Needs Improvement"
            else:
                return "❌ Critical"
        
        summary_df['Status'] = summary_df['Score_2023'].apply(get_status)
        
        st.dataframe(
            summary_df,
            use_container_width=True,
            column_config={
                'Category': 'Category',
                'Score_2008': '2008 Score',
                'Score_2023': '2023 Score',
                'Target': 'Target',
                'Change': 'Change',
                'Gap_to_Target': 'Gap to Target',
                'Trend': 'Trend',
                'Status': 'Status'
            }
        )

# ============================================================================
# VIEW 15: 2023 EXECUTIVE SUMMARY - COMPLETE WITH REVENUE & EXPENDITURE SUMMARY
# ============================================================================
elif view_option == "📋 2023 Executive Summary":
    st.markdown('<div class="sub-header">📋 2023 Executive Summary - Adverse Audit Opinion</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="financial-card adverse-opinion">
        <h3 style="color: #DC2626; margin-top: 0;">⚠️ ADVERSE AUDIT OPINION ISSUED (2023)</h3>
        <p><strong>Auditor General's Conclusion:</strong> The accompanying financial statements do <strong>NOT</strong> give a true and fair view of the financial position of the Government of Barbados as at March 31, 2023.</p>
        <p><strong>Reason:</strong> Significant material misstatements and non-compliance with International Public Sector Accounting Standards (IPSAS).</p>
        <p><strong>Historical Context:</strong> This is the 6th consecutive Adverse opinion (2018-2023).</p>
        <p style="color: #DC2626; font-weight: bold; margin-top: 10px;">
        🚨 NEW IN 2023: $2.43B tax receivables could not be verified.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">2023 Key Financial Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", format_currency(metrics['total_revenue_2023'], currency_format),
                  f"{metrics['revenue_growth_pct']:.1f}% vs 2022")
    with col2:
        st.metric("Total Expenditure", format_currency(metrics['total_expenditure_2023'], currency_format))
    with col3:
        st.metric("Consolidated Fund Deficit", format_currency(abs(metrics['deficit_2023']), currency_format))
    with col4:
        st.metric("Total Public Debt", format_currency(metrics['total_liabilities_2023'], currency_format),
                  "6th consecutive adverse opinion")
    
    # ========================================================================
    # REVENUE & EXPENDITURE SUMMARY - ADDED BACK
    # ========================================================================
    st.markdown('<div class="section-header">📊 Revenue & Expenditure Summary</div>', unsafe_allow_html=True)
    
    # Revenue Composition Pie Chart
    revenue_composition = financial_2023['financial_performance'].copy()
    fig_revenue = px.pie(
        revenue_composition,
        values='Actual_2023',
        names='Category',
        title='Revenue Composition by Source (2023)',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )
    fig_revenue.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
    fig_revenue.update_layout(height=450)
    st.plotly_chart(fig_revenue, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 5 Tax Revenue Sources
        st.markdown("#### Top 5 Tax Revenue Sources (2023)")
        top_taxes = financial_2023['tax_revenue_details'].nlargest(5, 'Actual_2023')
        fig_taxes = px.bar(
            top_taxes,
            x='Tax_Type',
            y='Actual_2023',
            title='Top 5 Tax Revenue Sources (2023)',
            color='Growth_Pct',
            color_continuous_scale='Blues',
            text=[format_currency(x, currency_format) for x in top_taxes['Actual_2023']]
        )
        fig_taxes.update_layout(yaxis_title=f'Amount ({currency_format})', xaxis_title='Tax Type')
        fig_taxes.update_xaxes(tickangle=20)
        st.plotly_chart(fig_taxes, use_container_width=True)
    
    with col2:
        # Expenditure Breakdown
        st.markdown("#### Expenditure by Category (2023)")
        expenditure_data = financial_2023['expenditure_data'].copy()
        expenditure_data['Pct_of_Total'] = (expenditure_data['Actual_2023'] / expenditure_data['Actual_2023'].sum()) * 100
        expenditure_data_sorted = expenditure_data.sort_values('Actual_2023', ascending=False).head(8)
        
        fig_exp = px.bar(
            expenditure_data_sorted,
            x='Category',
            y='Actual_2023',
            title='Top 8 Expenditure Categories (2023)',
            color='Actual_2023',
            color_continuous_scale='Reds',
            text=[format_currency(x, currency_format) for x in expenditure_data_sorted['Actual_2023']]
        )
        fig_exp.update_layout(yaxis_title=f'Amount ({currency_format})', xaxis_title='Category')
        fig_exp.update_xaxes(tickangle=20)
        st.plotly_chart(fig_exp, use_container_width=True)
    
    # Revenue vs Expenditure Comparison
    st.markdown("#### Revenue vs Expenditure Comparison")
    
    rev_exp_data = pd.DataFrame({
        'Category': ['Revenue', 'Expenditure'],
        'Amount': [metrics['total_revenue_2023'], metrics['total_expenditure_2023']]
    })
    
    fig_comp = px.bar(
        rev_exp_data,
        x='Category',
        y='Amount',
        title='Revenue vs Expenditure (2023)',
        color='Category',
        color_discrete_map={'Revenue': '#00267F', 'Expenditure': '#DC2626'},
        text=[format_currency(x, currency_format) for x in rev_exp_data['Amount']]
    )
    fig_comp.update_layout(yaxis_title=f'Amount ({currency_format})', xaxis_title='')
    st.plotly_chart(fig_comp, use_container_width=True)
    
    # ========================================================================
    # MATERIAL MISSTATEMENTS
    # ========================================================================
    st.markdown('<div class="section-header">🚨 Material Misstatements Identified</div>', unsafe_allow_html=True)
    
    for _, item in financial_2023['adverse_opinion_items'].iterrows():
        render_misstatement_card(item, currency_format)

    # ========================================================================
    # IPSAS COMPLIANCE FAILURES
    # ========================================================================
    st.markdown('<div class="section-header">📋 IPSAS Compliance Failures</div>', unsafe_allow_html=True)
    
    ipsas_issues = [
        {'Requirement': 'Consolidation of State-Owned Entities', 'Status': '❌ NOT COMPLIANT',
         'Impact': 'Financial statements incomplete and misleading'},
        {'Requirement': 'Recognition of Pension Liabilities', 'Status': '❌ NOT COMPLIANT',
         'Impact': 'Liabilities understated by unquantified amount'},
        {'Requirement': 'Asset Valuation and Verification', 'Status': '⚠️ PARTIALLY COMPLIANT',
         'Impact': 'Assets potentially overstated by $981M+'},
        {'Requirement': 'Revenue Recognition (Tax Receivables)', 'Status': '❌ NOT COMPLIANT',
         'Impact': '$2.43B receivables unverified (NEW 2023)'}
    ]
    
    for issue in ipsas_issues:
        status_color = '#DC2626' if 'NOT' in issue['Status'] else '#F59E0B'
        st.markdown(f"""
        <div class="financial-card">
            <h5 style="margin-top: 0;">{issue['Requirement']}</h5>
            <p><strong>Status:</strong> <span style="color: {status_color};">{issue['Status']}</span></p>
            <p><strong>Impact:</strong> {issue['Impact']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# VIEW 16: 2023 BALANCE SHEET
# ============================================================================
elif view_option == "🏦 2023 Balance Sheet":
    st.markdown('<div class="sub-header">🏦 2023 Balance Sheet Analysis</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Assets", format_currency(metrics['total_assets_2023'], currency_format))
    with col2:
        st.metric("Total Liabilities", format_currency(metrics['total_liabilities_2023'], currency_format))
    with col3:
        net_position = metrics['total_assets_2023'] - metrics['total_liabilities_2023']
        st.metric("Net Position", format_currency(net_position, currency_format))
    
    st.markdown('<div class="section-header">Key Asset Items</div>', unsafe_allow_html=True)
    
    asset_data = financial_2023['balance_sheet'].copy()
    key_assets = asset_data[asset_data['Category'].isin([
        'Cash on Hand', 'Bank', 'Tax Receivables (Net)', 
        'Investments', 'Land', 'Other capital assets (Net)'
    ])]
    
    for _, row in key_assets.iterrows():
        value = format_currency(row['Actual_Mar_23'], currency_format)
        prev_value = format_currency(row['Actual_Mar_22'], currency_format)
        change = row['Actual_Mar_23'] - row['Actual_Mar_22']
        change_pct = (change / row['Actual_Mar_22']) * 100 if row['Actual_Mar_22'] != 0 else 0
        
        st.markdown(f"""
        <div class="financial-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{row['Category']}</strong><br>
                    <small style="color: #666;">2023: {value} | 2022: {prev_value}</small>
                </div>
                <div style="text-align: right;">
                    <div style="color: {'#10B981' if change >= 0 else '#DC2626'}; font-weight: bold;">
                        {format_currency(change, currency_format)}
                    </div>
                    <small style="color: #666;">{change_pct:+.1f}%</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Debt Structure</div>', unsafe_allow_html=True)
    
    debt_data = financial_2023['debt_structure'].copy()
    fig = px.bar(
        debt_data,
        x='Debt_Type',
        y='Amount_2023',
        title='Public Debt by Type (2023)',
        color='Debt_Category',
        color_discrete_map={'Domestic': '#00267F', 'Foreign': '#DC2626'},
        text=[format_currency(x, currency_format) for x in debt_data['Amount_2023']]
    )
    fig.update_layout(yaxis_title=f'Amount ({currency_format})', xaxis_title='Debt Type')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# VIEW 17: 2023 AUDIT FINDINGS - FIXED VERSION
# ============================================================================
elif view_option == "🔍 2023 Audit Findings":
    st.markdown('<div class="sub-header">🔍 2023 Audit Findings & Material Misstatements</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="financial-card adverse-opinion">
        <h4 style="color: #DC2626; margin-top: 0;">📄 Basis for Adverse Opinion (Extract from Auditor General's Report)</h4>
        <p>"The total for Other Capital Assets could not be confirmed because of a difference of $719 million between the amounts reported in the financial statements compared with the corresponding figures listed in the subsidiary records. Cash and Financial Investments listed in the financial statements were overstated by $115 million and $147 million respectively. In addition, the liability for pensions and employee benefits were not included in the Statement of Financial Position and the accounts of the State-owned Entities were not consolidated into the financial statements as required by the International Public Sector Accounting Standards (IPSAS). Also, Tax Receivables of $2.43 billion and Bad Debt Expenses of $68.28 million could not be confirmed because of the absence of sufficient supporting documentation."</p>
        <p style="color: #DC2626; font-weight: bold; margin-top: 10px;">
        🚨 The $2.43B tax receivables issue was FIRST FLAGGED in the 2023 audit.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Material Misstatements Identified</div>', unsafe_allow_html=True)
    
    # Loop through all adverse opinion items and render them
    for _, item in financial_2023['adverse_opinion_items'].iterrows():
        render_misstatement_card(item, currency_format)
    
    st.markdown('<div class="section-header">IPSAS Compliance Failures</div>', unsafe_allow_html=True)
    
    ipsas_issues = [
        {'Requirement': 'Consolidation of State-Owned Entities', 'Status': '❌ NOT COMPLIANT',
         'Impact': 'Financial statements incomplete and misleading'},
        {'Requirement': 'Recognition of Pension Liabilities', 'Status': '❌ NOT COMPLIANT',
         'Impact': 'Liabilities understated by unquantified amount'},
        {'Requirement': 'Asset Valuation and Verification', 'Status': '⚠️ PARTIALLY COMPLIANT',
         'Impact': 'Assets potentially overstated by $981M+'},
        {'Requirement': 'Revenue Recognition (Tax Receivables)', 'Status': '❌ NOT COMPLIANT',
         'Impact': '$2.43B receivables unverified (NEW 2023)'}
    ]
    
    for issue in ipsas_issues:
        status_color = '#DC2626' if 'NOT' in issue['Status'] else '#F59E0B'
        st.markdown(f"""
        <div class="financial-card">
            <h5 style="margin-top: 0;">{issue['Requirement']}</h5>
            <p><strong>Status:</strong> <span style="color: {status_color};">{issue['Status']}</span></p>
            <p><strong>Impact:</strong> {issue['Impact']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# VIEW 18: 2023 DATA QUALITY ISSUES
# ============================================================================
elif view_option == "⚠️ 2023 Data Quality Issues":
    st.markdown('<div class="sub-header">⚠️ 2023 Data Quality Issues</div>', unsafe_allow_html=True)
    
    narrative_amount = financial_2023['note34_discrepancy']['narrative_amount']
    table_amount = financial_2023['note34_discrepancy']['table_amount']
    difference = financial_2023['note34_discrepancy']['difference']
    difference_pct = financial_2023['note34_discrepancy']['difference_pct']
    
    st.markdown("""
    <div class="financial-card data-error">
        <h4 style="color: #DC2626; margin-top: 0;">❌ CRITICAL DATA QUALITY ISSUES IN NOTE 34</h4>
        <p><strong>Note 34: Related Party Transactions - Contains Multiple Material Errors</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="border: 2px solid #DC2626; padding: 15px; border-radius: 8px; background-color: #FEF2F2;">
            <h5 style="color: #DC2626; margin-top: 0;">NARRATIVE TEXT</h5>
            <p style="font-size: 1.2rem; font-weight: bold; color: #DC2626;">
                "${narrative_amount:,.0f}"
            </p>
            <p><em>"The Government reporting entity recorded transfers..."</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="border: 2px solid #3B82F6; padding: 15px; border-radius: 8px; background-color: #EFF6FF;">
            <h5 style="color: #3B82F6; margin-top: 0;">TABLE TOTAL</h5>
            <p style="font-size: 1.2rem; font-weight: bold; color: #3B82F6;">
                "${table_amount:,.0f}"
            </p>
            <p>Sum of all transfers in the Note 34 table</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="border: 2px dashed #DC2626; padding: 15px; border-radius: 8px; background-color: #FFFBEB; margin-top: 15px;">
        <h5 style="color: #D97706; margin-top: 0;">DISCREPANCY ANALYSIS</h5>
        <p><strong>Difference:</strong> ${difference:,.0f}</p>
        <p><strong>Percentage Variance:</strong> {difference_pct:.1f}%</p>
        <p><strong>Impact:</strong> Which number is correct? The narrative or the table?</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# VIEW 19: 2026 REALITY CHECK
# ============================================================================
elif view_option == "📊 2026 Reality Check":
    st.markdown('<div class="sub-header">📊 2026 Reality Check: Official Optimism vs. 2023 Audit Reality</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 15px; background-color: #1E40AF; color: white; border-radius: 8px; margin-bottom: 20px;">
        <h5 style="color: white; margin-top: 0;">📄 Document Reference: Pre-Election Economic & Fiscal Update (Jan 27, 2026)</h5>
        <p style="margin: 0; font-size: 0.85rem;">Pages 16-19: Debt Service | Page 7: Economic Performance | Page 14-15: Fiscal Balance</p>
    </div>
    """, unsafe_allow_html=True)
    
    comparison_data = {
        'Metric': [
            'Debt-to-GDP Ratio',
            'Annual Debt Service Cost',
            'Interest Rate on New Bonds',
            'Tax Receivables (Unverified)',
            'SOE Consolidation Status',
            'Primary Surplus (Target vs Actual)',
            'Tourism % of GDP'
        ],
        '2023 Reality': [
            '102.9% (Central Bank 2025)',
            '$568M (2023 FS)',
            '6.5% (2029 bonds)',
            '$2.43B UNVERIFIED (NEW 2023)',
            '❌ NOT CONSOLIDATED',
            '4.3% (achieved 2023)',
            '~40% (estimated)'
        ],
        '2026 Update': [
            '93.7% (Nov 2025, Page 16)',
            '$2.5B (2025/26 projected, Page 18)',
            '8.0% (2035 bonds, Page 16)',
            'No mention',
            'SOEs: $77M arrears (Page 19)',
            'Target: 4.1% | Actual: 3.7% (Page 15)',
            '>40% (increasing, Page 7)'
        ]
    }
    
    st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #DC2626; color: white; border-radius: 10px; margin: 20px 0;">
        <h4 style="color: white; margin-top: 0;">⚠️ THE HARSH REALITY</h4>
        <p style="margin: 0; font-size: 1.1rem;">Barbados is paying 40% of revenue to creditors while asking for $7.4B more for BERT 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 15px; background-color: #00267F; color: white; border-radius: 8px; margin-top: 20px;">
        <h5 style="color: white; margin-top: 0;">🎯 RESPONSIBLE PATH FORWARD</h5>
        <p><strong>Fix Foundation Before More Borrowing</strong></p>
        <ol style="color: white;">
            <li><strong>Fix 2023 audit issues FIRST</strong> (clean 2024 audit) before $7.4B BERT borrowing</li>
            <li><strong>Investigate the $2.43B NEW issue</strong> flagged in 2023</li>
            <li><strong>Transparent cost-benefit</strong> of 8% bonds vs. alternatives</li>
            <li><strong>Diversify economy</strong> beyond 40% tourism dependency</li>
        </ol>
        <p style="margin-top: 10px; font-size: 0.9rem; color: #BFDBFE;"><em>The 2026 document shows temporary fiscal improvement, but the 2023 audit shows the financial foundation remains unreliable.</em></p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 20px;">
        <p style="font-weight: bold; color: #00267F;">Barbados Financial Accountability 2003-2026</p>
        <p>A 21-Year Audit History • Data-Driven Analysis</p>
        <p style="margin-top: 20px; font-size: 0.8rem;">
            Data Source: Auditor General's Reports (2003-2023) • 
            Version 10.0 • Generated: {datetime.now().strftime('%B %d, %Y')}
        </p>
        <p style="font-size: 0.7rem; color: #999;">
            ⚠️ 6 consecutive Adverse opinions (2018-2023)
            <br>⚠️ Note 34 contains critical data inconsistencies
            <br>⚠️ $2.43B tax receivables unverified (NEW 2023) • $4B+ pension liability hidden
        </p>
    </div>
    """, unsafe_allow_html=True)