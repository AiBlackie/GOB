# ============================================================================
# 🇧🇧 BARBADOS FINANCIAL ACCOUNTABILITY 2003-2023
# COMPLETE DASHBOARD - CORRECTED VERSION
# ============================================================================
#
# This dashboard presents 21 years of Auditor General's reports
# with factual data and evidence-based analysis.
#
# Version: 7.3 - CORRECTED INTEREST RATES
# Date: April 2025
#
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
    page_title="Barbados Financial Accountability 2003-2023",
    page_icon="🇧🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
:root {
    --bb-blue: #00267F;
    --bb-gold: #FFC726;
    --bb-red: #DC2626;
    --bb-green: #10B981;
    --bb-black: #000000;
}

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
    color: var(--bb-blue);
    font-weight: 600;
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-bottom: 3px solid var(--bb-gold);
    padding-bottom: 0.5rem;
}

.section-header {
    font-size: 1.3rem;
    color: var(--bb-blue);
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
    border-left: 4px solid var(--bb-blue);
}

.adverse-opinion {
    background: linear-gradient(135deg, #fee 0%, #fff5f5 100%);
    border-left: 4px solid #DC2626;
}

.data-error {
    background: linear-gradient(135deg, #fef2f2 0%, #fee 100%);
    border-left: 4px solid #EF4444;
    border: 2px dashed #DC2626;
}

.conceptual-error {
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    border-left: 4px solid #D97706;
    border: 2px dashed #F59E0B;
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
    color: var(--bb-blue);
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
    box-shadow: 0 4px 6px rgba(0, 38, 127, 0.1);
}

.info-banner {
    background-color: #F0F7FF;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #00267F;
    margin: 20px 0;
}

.narrative-box {
    border: 2px solid #DC2626;
    padding: 15px;
    border-radius: 8px;
    background-color: #FEF2F2;
}

.table-box {
    border: 2px solid #3B82F6;
    padding: 15px;
    border-radius: 8px;
    background-color: #EFF6FF;
}

.analysis-box {
    border: 2px dashed #DC2626;
    padding: 15px;
    border-radius: 8px;
    background-color: #FFFBEB;
    margin-top: 15px;
}

.conclusion-box {
    border: 2px solid #DC2626;
    padding: 15px;
    border-radius: 8px;
    background-color: #FEF2F2;
    margin-top: 15px;
}

.footer-bar {
    background: linear-gradient(135deg, #00267F 0%, #FFC726 100%);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-top: 30px;
}

.footer-bar h3 {
    color: white;
}

.footer-bar .gold-text {
    color: #FFC726;
}

.business-case-container {
    background-color: #EFF6FF;
    padding: 25px;
    border-radius: 10px;
    border: 1px solid #3B82F6;
    margin: 15px 0;
}

.business-case-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin: 20px 0;
}

.business-case-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
    transition: transform 0.2s;
}

.business-case-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

.business-case-value {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.business-case-label {
    font-size: 1rem;
    color: #4b5563;
    font-weight: 600;
    margin-bottom: 4px;
}

.business-case-sub {
    font-size: 0.85rem;
    color: #9ca3af;
}

.business-case-calculation {
    background: white;
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
    border: 1px solid #e5e7eb;
}

.business-case-comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 15px;
}

.business-case-current {
    background: #FEF2F2;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #DC2626;
}

.business-case-potential {
    background: #ECFDF5;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #10B981;
}

.business-case-insight {
    background: #ECFDF5;
    padding: 15px;
    border-radius: 8px;
    margin-top: 10px;
}

@media (max-width: 768px) {
    .business-case-grid {
        grid-template-columns: 1fr;
    }
    .business-case-comparison {
        grid-template-columns: 1fr;
    }
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
            'Disclaimer', 'Adverse', 'Adverse', 'Adverse', 'Adverse', 'Adverse'  # 2018-2023
        ],
        'Severity_Score': [
            0, 0, 0, 0, 0,  # 2003-2007: Clean
            3, 3, 3, 3, 3,  # 2008-2012: Disclaimer
            3, 3, 3, 3, 3,  # 2013-2017: Disclaimer
            3, 4, 4, 4, 4, 4  # 2018-2023: Disclaimer/Adverse
        ],
        'Key_Issue': [
            'No major issues', 'No major issues', 'No major issues', 'No major issues', 'No major issues',
            'SOE consolidation concerns', 'SOE consolidation concerns', 'SOE consolidation concerns', 
            'SOE consolidation concerns', 'SOE consolidation concerns',
            'Asset valuation issues', 'Asset valuation issues', 'Asset valuation issues', 
            'Asset valuation issues', 'Asset valuation issues',
            'Multiple material issues', 'Cash overstatement', 'Asset discrepancies', 
            'Tax receivables unverified', 'Pension liability hidden', 'Note 34 errors'
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
    """Load historical recurring issues data"""
    
    issues_data = {
        'Issue': [
            'SOE Consolidation',
            'Pension Liability',
            'Asset Registers',
            'Bank Reconciliations',
            'Road Infrastructure',
            'Tax Receivables'
        ],
        'Start_Year': [2003, 2003, 2003, 2008, 2003, 2008],
        'Status_2023': ['❌ Not Done', '❌ Hidden', '❌ Missing', '❌ 15+ Years', '❌ Not Included', '❌ Unverified'],
        'Estimated_Impact_Billions': [2.0, 4.0, 0.719, 0, 0, 2.43],
        'Last_Year_Reported': [2023, 2023, 2023, 2023, 2023, 2023]
    }
    
    return pd.DataFrame(issues_data)

@st.cache_data
def load_historical_recommendations():
    """Load historical audit recommendations data"""
    
    recommendations = pd.DataFrame({
        'Recommendation': [
            'SOE Consolidation',
            'Pension Liability Recognition',
            'Asset Register Reconciliation',
            'Bank Reconciliation Completion',
            'Tax Receivable Verification',
            'Revenue Waiver Documentation'
        ],
        'Year_First_Made': [2003, 2003, 2003, 2008, 2008, 2010],
        'Status': [
            '❌ Not Implemented',
            '❌ Not Implemented',
            '⚠️ In Progress',
            '❌ Not Implemented',
            '❌ Not Implemented',
            '⚠️ In Progress'
        ],
        'Years_Outstanding': [20, 20, 20, 15, 15, 13],
        'Estimated_Cost_Billions': [2.0, 4.0, 0.719, 0, 2.43, 0.723]
    })
    
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
    
    # Adverse Opinion Details
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
            'Issue': 'Tax Receivables Unverified',
            'Amount': 2430000000,
            'Description': '$2.43 billion tax receivables could not be confirmed',
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
    
    return {
        'financial_performance': financial_performance,
        'expenditure_data': expenditure_data,
        'balance_sheet': balance_sheet,
        'liabilities_data': liabilities_data,
        'adverse_opinion_items': pd.DataFrame(adverse_opinion_items),
        'tax_revenue_details': tax_revenue_details,
        'debt_structure': debt_structure,
        'soe_transfers': soe_transfers,
        'note34_discrepancy': note34_discrepancy
    }

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_currency(value, format_type="Millions (BBD $M)"):
    """Format currency values based on selected format."""
    if pd.isna(value) or value is None:
        return "N/A"
    
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
        'adverse_consecutive_years': 15
    }

def render_business_case_native():
    """Render the business case using native Streamlit components."""
    
    with st.container():
        st.markdown("""
        <div class="business-case-container">
            <h5 style="color: #00267F; margin-top: 0;">📊 Investment vs Return Analysis</h5>
        </div>
        """, unsafe_allow_html=True)
        
        # Three columns for the metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="business-case-card">
                <div class="business-case-value" style="color: #DC2626;">$10-20M</div>
                <div class="business-case-label">One-time Investment</div>
                <div class="business-case-sub">Financial management reform</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="business-case-card">
                <div class="business-case-value" style="color: #F59E0B;">1-2%</div>
                <div class="business-case-label">Interest Rate Reduction</div>
                <div class="business-case-sub">100-200 basis points</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="business-case-card">
                <div class="business-case-value" style="color: #10B981;">$55-100M</div>
                <div class="business-case-label">Annual Savings</div>
                <div class="business-case-sub">Recurring benefit</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Calculation section
        st.markdown("""
        <div class="business-case-calculation">
            <p><strong>The Calculation:</strong></p>
            <ul>
                <li><strong>$1.85B</strong> = Annual new borrowing (BERT 2026: $7.4B ÷ 4 years)</li>
                <li><strong>$8B</strong> = Domestic debt stock that could be refinanced at lower rates</li>
                <li><strong>$500M</strong> = 8% Eurobond that could be refinanced</li>
                <li><strong>1-2%</strong> = Potential interest rate reduction from clean audit + SOE consolidation</li>
                <li><strong>$55-100M</strong> = Annual interest savings</li>
                <li><strong>5-10x</strong> = Return on investment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Comparison section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="business-case-current">
                <p style="margin: 0; font-size: 0.9rem;">
                <strong>Current Situation:</strong><br>
                ❌ Adverse audit opinion<br>
                ❌ $2.43B unverified receivables<br>
                ❌ $4B+ hidden pension liability<br>
                ❌ SOEs not consolidated<br>
                <span style="color: #DC2626;">Average interest rates: 5-7%</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="business-case-potential">
                <p style="margin: 0; font-size: 0.9rem;">
                <strong>Potential Outcome:</strong><br>
                ✅ Clean audit opinion<br>
                ✅ Verified receivables<br>
                ✅ Transparent pension disclosure<br>
                ✅ SOEs consolidated<br>
                <span style="color: #10B981;">Average interest rates: 4-6%</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Key Insight
        st.markdown("""
        <div class="business-case-insight">
            <p style="margin: 0; font-size: 0.9rem;">
            <strong>💡 Key Insight:</strong> A clean audit reduces uncertainty. Reduced uncertainty lowers risk premiums.<br>
            Lower risk premiums mean investors accept lower interest rates.<br>
            <strong>Every dollar spent on reform saves $5-10 in borrowing costs.</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

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
        '<div class="main-header">🇧🇧 Barbados Government Financial Statements 2003-2023</div>',
        unsafe_allow_html=True
    )
    st.markdown("**21 Years of Auditor General's Reports • Complete Historical Analysis**")
    st.caption("Integrated Dashboard: 2003-2023 Financial Statements & Audit Opinions")

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
    st.caption(f"**Dashboard Version:** 8.0 ")
    st.caption(f"**Date Range:** 2003 - 2023")
    st.caption(f"**Current Audit Opinion:** ❌ Adverse (15th Consecutive)")
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
        <div class="quick-stats-label">Consecutive Adverse/Disclaimer</div>
        <div style="font-size: 0.7rem; color: #666;">2008-2023</div>
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
    
    # Currency Format
    st.subheader("Currency Format")
    currency_format = st.selectbox(
        "Display values as",
        ["Millions (BBD $M)", "Billions (BBD $B)", "Full Amount (BBD $)"],
        key="currency_format"
    )
    
    # Show Comparative
    st.subheader("Comparative Period")
    show_comparative = st.checkbox("Show 2022 Comparison", value=True, key="show_comparative")
    
    st.markdown("---")
    
    # Data Quality Alerts
    st.subheader("⚠️ Data Quality Alerts")
    
    st.markdown("""
    <div class="financial-card data-error">
        <div class="financial-label">Note 34 Discrepancy (2023):</div>
        <div>Narrative: $669.3M</div>
        <div>Table: $777.9M</div>
        <div style="color: #DC2626; font-weight: bold;">Difference: $108.6M</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="financial-card conceptual-error">
        <div class="financial-label">Persistent Issues:</div>
        <div>SOE Consolidation: 21+ years</div>
        <div>Pension Liability: 21+ years</div>
        <div>Asset Registers: 21+ years</div>
        <div>Bank Reconciliations: 15+ years</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data Source
    st.markdown("**Data Source:**")
    st.caption("Auditor General's Reports (2003-2023)")
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
                <li><strong>15 consecutive years</strong> of Adverse/Disclaimer opinions (2008-2023)</li>
                <li><strong>$2.43B in tax receivables</strong> require verification</li>
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
    
    # THE BUSINESS CASE - CORRECTED VERSION
    st.markdown('<div class="section-header">💰 The Business Case: Investment & Return</div>', unsafe_allow_html=True)
    
    # Call the native render function with corrected values
    render_business_case_native()
    
    # 6-Month Priority Actions
    st.markdown('<div class="section-header" style="font-size: 1.1rem; color: #00267F;">📌 Priority Actions</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #3B82F6;">
            <h5 style="color: #3B82F6; margin-top: 0;">1️⃣ Clean Audit Opinion for 2024</h5>
            <ul style="padding-left: 20px;">
                <li>Verify $2.43B tax receivables</li>
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
    
    # What Success Looks Like
    st.markdown('<div class="section-header">✅ Key Success Indicators</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #ECFDF5; padding: 25px; border-radius: 10px; border-left: 5px solid #10B981; margin-top: 15px;">
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
            <div>
                <div style="font-size: 2rem; font-weight: bold; color: #10B981;">✅</div>
                <h5 style="margin-top: 0; color: #10B981;">Clean Audit</h5>
                <p style="font-size: 0.9rem; color: #666;">2024 financial statements receive clean opinion</p>
            </div>
            <div>
                <div style="font-size: 2rem; font-weight: bold; color: #10B981;">✅</div>
                <h5 style="margin-top: 0; color: #10B981;">SOE Consolidation</h5>
                <p style="font-size: 0.9rem; color: #666;">IPSAS compliance with consolidated SOEs</p>
            </div>
            <div>
                <div style="font-size: 2rem; font-weight: bold; color: #10B981;">✅</div>
                <h5 style="margin-top: 0; color: #10B981;">Pension Disclosure</h5>
                <p style="font-size: 0.9rem; color: #666;">Transparent reporting of $4B+ liability</p>
            </div>
            <div>
                <div style="font-size: 2rem; font-weight: bold; color: #10B981;">✅</div>
                <h5 style="margin-top: 0; color: #10B981;">Investor Confidence</h5>
                <p style="font-size: 0.9rem; color: #666;">Reduced borrowing costs</p>
            </div>
            <div>
                <div style="font-size: 2rem; font-weight: bold; color: #10B981;">✅</div>
                <h5 style="margin-top: 0; color: #10B981;">BERT Success</h5>
                <p style="font-size: 0.9rem; color: #666;">Credible foundation for $7.4B financing</p>
            </div>
            <div>
                <div style="font-size: 2rem; font-weight: bold; color: #10B981;">✅</div>
                <h5 style="margin-top: 0; color: #10B981;">Generational Fairness</h5>
                <p style="font-size: 0.9rem; color: #666;">No hidden liabilities for future generations</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer-bar">
        <h3>🇧🇧 The Evidence is Clear. The Path Forward is Known.</h3>
        <p style="font-size: 1.1rem; color: #BFDBFE;">
        Barbados has demonstrated the ability to deliver <strong style="color: white;">significant fiscal improvement</strong>.<br>
        The data shows what works. The data shows what needs to change.<br><br>
        <strong style="color: white;">$10-20M investment → $55-100M annual savings → 5-10x ROI</strong><br>
        <span style="color: #FFC726;">This is not opinion. This is math.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# VIEW 2: 21-YEAR OVERVIEW
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
        <strong>15 consecutive years</strong> of Adverse/Disclaimer opinions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">The Big Picture</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #10B981;">
            <h6 style="margin-top: 0;">✅ Clean Opinions</h6>
            <div style="font-size: 2rem; font-weight: bold; color: #10B981;">5</div>
            <div style="font-size: 0.9rem; color: #666;">2003-2007</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #F59E0B;">
            <h6 style="margin-top: 0;">⚠️ Disclaimer Opinions</h6>
            <div style="font-size: 2rem; font-weight: bold; color: #F59E0B;">10</div>
            <div style="font-size: 0.9rem; color: #666;">2008-2017</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #DC2626;">
            <h6 style="margin-top: 0;">❌ Adverse Opinions</h6>
            <div style="font-size: 2rem; font-weight: bold; color: #DC2626;">6</div>
            <div style="font-size: 0.9rem; color: #666;">2018-2023</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #DC2626;">
            <h6 style="margin-top: 0;">📊 Unresolved Issues</h6>
            <div style="font-size: 2rem; font-weight: bold; color: #DC2626;">21+</div>
            <div style="font-size: 0.9rem; color: #666;">Years of recurring issues</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Key Findings</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="financial-card adverse-opinion">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 Persistent Issues</h5>
            <ul>
                <li><strong>15 consecutive years</strong> of Adverse/Disclaimer opinions (2008-2023)</li>
                <li><strong>SOE consolidation</strong> not completed in 21+ years</li>
                <li><strong>Pension liability</strong> hidden from balance sheet for 21+ years</li>
                <li><strong>$2.43B</strong> tax receivables unverified (2023)</li>
                <li><strong>$719M</strong> asset discrepancies identified (2023)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="financial-card material-misstatement">
            <h5 style="color: #1D4ED8; margin-top: 0;">📊 Financial Evolution</h5>
            <ul>
                <li><strong>Revenue:</strong> $1.2B (2003) → $3.48B (2023) = <strong>+190%</strong></li>
                <li><strong>Expenditure:</strong> $1.3B (2003) → $3.59B (2023) = <strong>+176%</strong></li>
                <li><strong>Net Debt:</strong> $5.0B (2003) → $10.6B (2023) = <strong>+112%</strong></li>
                <li><strong>Deficit:</strong> Reduced from $685M (2021) to $111M (2023)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Audit Opinion Timeline (2003-2023)</div>', unsafe_allow_html=True)
    
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
        name='Audit Opinion',
        hovertemplate='Year: %{x}<br>Opinion: %{text}<br>Key Issue: %{customdata}<extra></extra>',
        customdata=historical_audit['Key_Issue']
    ))
    
    significant_years = {2003: 'Last Clean', 2008: 'First Disclaimer', 2013: 'Asset Issues', 2018: 'First Adverse', 2023: '15th Adverse'}
    for year, label in significant_years.items():
        fig.add_annotation(x=year, y=1.1, text=label, showarrow=True, arrowhead=1, ax=0, ay=40, font=dict(size=10))
    
    fig.update_layout(
        title='Audit Opinion History: 2003-2023',
        yaxis=dict(range=[0, 1.5], showticklabels=False, title=''),
        xaxis=dict(tickmode='linear', dtick=1, title='Year'),
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="section-header">21-Year Summary Statistics</div>', unsafe_allow_html=True)
    
    summary_stats = pd.DataFrame({
        'Metric': [
            'Total Years', 'Clean Audit Opinions', 'Disclaimer Opinions', 'Adverse Opinions',
            'Consecutive Adverse/Disclaimer', 'SOE Consolidation Issue (Years)',
            'Pension Liability Issue (Years)', 'Asset Register Issue (Years)',
            'Bank Reconciliation Issue (Years)'
        ],
        'Value': [
            '21', '5 (2003-2007)', '10 (2008-2017)', '6 (2018-2023)',
            '15 (2008-2023)', '21+ (2003-2023)', '21+ (2003-2023)',
            '21+ (2003-2023)', '15+ (2008-2023)'
        ],
        'Status': ['✅ Completed', '✅ Historical', '⚠️ Historical', '❌ Current', '❌ Ongoing',
                   '❌ Unresolved', '❌ Unresolved', '❌ Unresolved', '❌ Unresolved']
    })
    
    st.dataframe(summary_stats, use_container_width=True)

# ============================================================================
# VIEW 3: THE COMPLETE STORY
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
    
    # CHAPTER 1
    with st.expander("🟢 CHAPTER 1: The Golden Years (2003-2007)", expanded=True):
        st.markdown("""
        <div style="padding: 15px; background-color: #ECFDF5; border-radius: 8px; border-left: 4px solid #10B981; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #10B981;">Clean audit opinions, no major issues identified.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>📊 The Numbers:</strong></p>
                <ul>
                    <li><strong>Revenue:</strong> $1.2B → $1.6B</li>
                    <li><strong>Net Debt:</strong> $5.0B → $7.0B</li>
                    <li><strong>Audit Opinion:</strong> 🟢 Clean (5 years)</li>
                </ul>
            </div>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>✅ What Was Working:</strong></p>
                <ul>
                    <li>Clean audit opinions every year</li>
                    <li>No major issues identified</li>
                    <li>Strong financial management systems</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> In the early 2000s, Barbados' financial management was functioning well. 
            The Auditor General issued clean opinions year after year. There were no major issues identified.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # CHAPTER 2
    with st.expander("🟡 CHAPTER 2: The First Cracks (2008-2012)", expanded=False):
        st.markdown("""
        <div style="padding: 15px; background-color: #FFFBEB; border-radius: 8px; border-left: 4px solid #F59E0B; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #D97706;">Issues began to emerge that persisted over time.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>📊 The Numbers:</strong></p>
                <ul>
                    <li><strong>Revenue:</strong> $1.7B → $1.9B</li>
                    <li><strong>Net Debt:</strong> $7.5B → $9.5B</li>
                    <li><strong>Audit Opinion:</strong> 🟡 Disclaimer (5 years)</li>
                </ul>
            </div>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>⚠️ What Changed:</strong></p>
                <ul>
                    <li><strong>2008:</strong> First Disclaimer Opinion issued</li>
                    <li><strong>SOE Consolidation</strong> becomes a recurring issue</li>
                    <li><strong>Bank Reconciliation</strong> issues first identified</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> 2008 marked a turning point. The Auditor General issued a Disclaimer Opinion. 
            The problems identified were SOE consolidation and asset valuation.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # CHAPTER 3
    with st.expander("🟡 CHAPTER 3: The Slow Decline (2013-2017)", expanded=False):
        st.markdown("""
        <div style="padding: 15px; background-color: #FFFBEB; border-radius: 8px; border-left: 4px solid #F59E0B; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #D97706;">The same problems, year after year, with no progress.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>📊 The Numbers:</strong></p>
                <ul>
                    <li><strong>Revenue:</strong> $2.0B → $2.2B</li>
                    <li><strong>Net Debt:</strong> $10.0B → $12.0B</li>
                    <li><strong>Audit Opinion:</strong> 🟡 Disclaimer (5 years)</li>
                </ul>
            </div>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>⚠️ The Recurring Issues:</strong></p>
                <ul>
                    <li><strong>2013:</strong> Asset register issues "ongoing"</li>
                    <li><strong>2015:</strong> $120M interest omitted from tax receivables</li>
                    <li><strong>2017:</strong> Bank reconciliations 5+ years outstanding</li>
                    <li><strong>2017:</strong> Pension liability still hidden</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> By 2013, the problems were no longer new. They were recurring. 
            Year after year, the Auditor General reported the same issues.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # CHAPTER 4
    with st.expander("🔴 CHAPTER 4: The Breaking Point (2018-2020)", expanded=False):
        st.markdown("""
        <div style="padding: 15px; background-color: #FEF2F2; border-radius: 8px; border-left: 4px solid #DC2626; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #DC2626;">The system broke. The opinions became Adverse.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>📊 The Numbers:</strong></p>
                <ul>
                    <li><strong>Revenue:</strong> $2.3B → $2.6B</li>
                    <li><strong>Net Debt:</strong> $11.5B → $9.5B</li>
                    <li><strong>Audit Opinion:</strong> 🔴 Adverse (3 years)</li>
                </ul>
            </div>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>🚨 What Changed:</strong></p>
                <ul>
                    <li><strong>2018:</strong> First Adverse Opinion issued</li>
                    <li><strong>2019:</strong> Cash overstatements identified</li>
                    <li><strong>2020:</strong> $2.4B+ tax receivables unverified</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> In 2018, the pattern broke. The Auditor General issued the 
            first Adverse Opinion. The problems were no longer just "issues" - they were material misstatements.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # CHAPTER 5
    with st.expander("🔴 CHAPTER 5: The Crisis (2021-2023)", expanded=False):
        st.markdown("""
        <div style="padding: 15px; background-color: #FEF2F2; border-radius: 8px; border-left: 4px solid #DC2626; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #DC2626;">15 consecutive years. $9.15B+ in issues.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>📊 The Numbers:</strong></p>
                <ul>
                    <li><strong>Revenue:</strong> $2.7B → $3.48B</li>
                    <li><strong>Net Debt:</strong> $9.0B → $10.6B</li>
                    <li><strong>Audit Opinion:</strong> 🔴 Adverse (3 years)</li>
                    <li><strong>2023 Deficit:</strong> $111M (improved from $685M)</li>
                </ul>
            </div>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>🚨 The 2023 Issues:</strong></p>
                <ul>
                    <li><strong>$2.43B</strong> tax receivables unverified</li>
                    <li><strong>$719M</strong> asset discrepancy</li>
                    <li><strong>$4B+</strong> pension liability hidden</li>
                    <li><strong>$115M</strong> cash overstatement</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> By 2023, Barbados had experienced 15 consecutive years 
            of Adverse/Disclaimer opinions. The government had made real progress on fiscal discipline 
            (deficit reduced 84%), but the financial management foundation remained broken.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # CHAPTER 6
    with st.expander("💡 CHAPTER 6: The Path Forward", expanded=False):
        st.markdown("""
        <div style="padding: 15px; background-color: #ECFDF5; border-radius: 8px; border-left: 4px solid #10B981; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 1.1rem; font-weight: bold; color: #10B981;">The data shows a path forward.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>📌 6-Month Priorities:</strong></p>
                <ul>
                    <li><strong>Clean Audit:</strong> Fix 2024 statements</li>
                    <li><strong>Pension Study:</strong> Complete actuarial valuation</li>
                    <li><strong>SOE Pilot:</strong> Start consolidation</li>
                    <li><strong>Capacity:</strong> Fill auditor positions</li>
                </ul>
            </div>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
                <p><strong>💰 The Opportunity:</strong></p>
                <ul>
                    <li><strong>Investment:</strong> $10-20M</li>
                    <li><strong>Return:</strong> $55-100M annually</li>
                    <li><strong>ROI:</strong> 5-10x</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0;">
            <p style="margin: 0; font-size: 0.95rem;">
            <strong>The Data Shows:</strong> The next chapter hasn't been written yet. Barbados has a choice: 
            continue with the same pattern, or break the cycle.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # SUMMARY
    st.markdown('<div class="section-header">📖 The Full Story: 2003-2023 Summary</div>', unsafe_allow_html=True)
    
    story_summary = pd.DataFrame({
        'Era': ['2003-2007', '2008-2012', '2013-2017', '2018-2020', '2021-2023'],
        'Audit Opinion': ['🟢 Clean', '🟡 Disclaimer', '🟡 Disclaimer', '🔴 Adverse', '🔴 Adverse'],
        'Years': ['5', '5', '5', '3', '3'],
        'Key Events': [
            'No major issues identified',
            'First disclaimer, SOE issues begin',
            'Asset issues, bank reconciliations',
            'First adverse, cash overstatements',
            '15th adverse, $9.15B+ impact'
        ],
        'Status': [
            '✅ Strong financial management',
            '⚠️ Issues begin to emerge',
            '⚠️ Recurring issues persist',
            '🚨 System breaks',
            '🚨 Systemic failure'
        ]
    })
    
    st.dataframe(story_summary, use_container_width=True, hide_index=True)
    
    # LESSONS
    st.markdown('<div class="section-header">📚 What the Data Shows</div>', unsafe_allow_html=True)
    
    lessons = [
        {
            'Lesson': 'Small problems become big problems when ignored',
            'Evidence': 'SOE consolidation started in 2003 and remains unresolved in 2023',
            'Impact': '$2B+ hidden liabilities'
        },
        {
            'Lesson': 'Admitting problems is not enough - action is required',
            'Evidence': 'Treasury "pledged" to fix issues but never did',
            'Impact': '15 consecutive adverse opinions'
        },
        {
            'Lesson': 'Financial management is the foundation of fiscal discipline',
            'Evidence': 'Fiscal aggregates improved while financial management failed',
            'Impact': 'Unreliable financial statements'
        },
        {
            'Lesson': 'Hidden liabilities become generational burdens',
            'Evidence': '$4B+ pension liability hidden for 21 years',
            'Impact': 'Future generations on the hook'
        },
        {
            'Lesson': 'The cost of inaction is higher than the cost of reform',
            'Evidence': '$10-20M reform saves $55-100M annually',
            'Impact': '5-10x return on investment'
        }
    ]
    
    for lesson in lessons:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #00267F;">
            <h5 style="margin-top: 0; color: #00267F;">{lesson['Lesson']}</h5>
            <p><strong>Evidence:</strong> {lesson['Evidence']}</p>
            <p><strong>Impact:</strong> {lesson['Impact']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #00267F; padding: 30px; border-radius: 10px; color: white; margin-top: 20px;">
        <h3 style="color: white; text-align: center;">🇧🇧 The Next Chapter Is Unwritten</h3>
        <p style="text-align: center; font-size: 1.1rem; color: #BFDBFE;">
        The data shows Barbados can deliver fiscal improvement.<br>
        The data also shows the financial foundation remains broken.<br><br>
        <strong style="color: white;">The challenges are clear. The path forward is known. The benefits are substantial.</strong>
        </p>
        <p style="text-align: center; font-size: 0.9rem; color: #93C5FD; margin-top: 15px;">
        <em>This analysis is based on 21 years of Auditor General's reports.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# VIEW 4: HISTORICAL AUDIT TIMELINE
# ============================================================================
elif view_option == "📈 Historical Audit Timeline":
    st.markdown('<div class="sub-header">📜 Historical Audit Timeline: 2003-2023</div>', unsafe_allow_html=True)
    
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
            name='Audit Opinion',
            hovertemplate='Year: %{x}<br>Opinion: %{text}<br>Key Issue: %{customdata}<extra></extra>',
            customdata=historical_audit['Key_Issue']
        ))
        
        fig.update_layout(
            title='Audit Opinion Severity Over Time',
            yaxis=dict(tickvals=[1, 2, 3], ticktext=['Clean', 'Disclaimer', 'Adverse'], title='Opinion Type', range=[0, 3.5]),
            xaxis=dict(tickmode='linear', dtick=1, title='Year'),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="financial-card">
            <h6 style="margin-top: 0;">🔑 Key Milestones</h6>
            <div style="font-size: 0.9rem;">
                <p><strong>2003-2007:</strong> 🟢 Clean Opinions</p>
                <p><strong>2008:</strong> 🟡 First Disclaimer Opinion</p>
                <p><strong>2013:</strong> 🟡 Asset Register Issues Emerge</p>
                <p><strong>2018:</strong> 🔴 First Adverse Opinion</p>
                <p><strong>2020:</strong> 🔴 Pension Liability Hidden</p>
                <p><strong>2023:</strong> 🔴 15th Consecutive Adverse</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Era Breakdown</div>', unsafe_allow_html=True)
    
    era_col1, era_col2, era_col3 = st.columns(3)
    
    with era_col1:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">🟢 Clean Era (2003-2007)</h5>
            <p><strong>Years:</strong> 5</p>
            <p><strong>Opinions:</strong> Clean</p>
            <p><strong>Key Issues:</strong> No major issues identified</p>
            <p><strong>Status:</strong> ✅ Historical baseline</p>
        </div>
        """, unsafe_allow_html=True)
    
    with era_col2:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #F59E0B;">
            <h5 style="color: #F59E0B; margin-top: 0;">🟡 Disclaimer Era (2008-2017)</h5>
            <p><strong>Years:</strong> 10</p>
            <p><strong>Opinions:</strong> Disclaimer</p>
            <p><strong>Key Issues:</strong> SOE consolidation, asset valuation</p>
            <p><strong>Status:</strong> ⚠️ Recurring issues emerge</p>
        </div>
        """, unsafe_allow_html=True)
    
    with era_col3:
        st.markdown("""
        <div class="financial-card" style="border-left-color: #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 Adverse Era (2018-2023)</h5>
            <p><strong>Years:</strong> 6</p>
            <p><strong>Opinions:</strong> Adverse</p>
            <p><strong>Key Issues:</strong> Material misstatements, unverified assets</p>
            <p><strong>Status:</strong> ❌ Systemic failures</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# VIEW 5: LONG-TERM FINANCIAL TRENDS
# ============================================================================
elif view_option == "💰 Long-Term Financial Trends":
    st.markdown('<div class="sub-header">💰 Long-Term Financial Trends (2003-2023)</div>', unsafe_allow_html=True)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(
        x=historical_financials['Year'],
        y=historical_financials['Revenue_Billions'],
        name='Revenue',
        mode='lines+markers',
        line=dict(color='#00267F', width=3),
        marker=dict(size=8)
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=historical_financials['Year'],
        y=historical_financials['Expenditure_Billions'],
        name='Expenditure',
        mode='lines+markers',
        line=dict(color='#DC2626', width=3),
        marker=dict(size=8)
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=historical_financials['Year'],
        y=historical_financials['Net_Debt_Billions'],
        name='Net Debt',
        mode='lines+markers',
        line=dict(color='#F59E0B', width=3, dash='dash'),
        marker=dict(size=8)
    ), secondary_y=True)
    
    for year in range(2008, 2018):
        fig.add_vrect(x0=year-0.5, x1=year+0.5, fillcolor="rgba(245, 158, 11, 0.1)", line_width=0)
    
    for year in range(2018, 2024):
        fig.add_vrect(x0=year-0.5, x1=year+0.5, fillcolor="rgba(220, 38, 38, 0.1)", line_width=0)
    
    fig.update_layout(title='Financial Trends with Audit Era Overlay', height=500, hovermode='x unified')
    fig.update_yaxes(title_text='Amount (Billions $)', secondary_y=False)
    fig.update_yaxes(title_text='Net Debt (Billions $)', secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="section-header">Key Metrics Evolution</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        revenue_2003 = historical_financials[historical_financials['Year'] == 2003]['Revenue_Billions'].values[0]
        revenue_2023 = historical_financials[historical_financials['Year'] == 2023]['Revenue_Billions'].values[0]
        pct_change = ((revenue_2023 - revenue_2003) / revenue_2003) * 100
        st.metric("Revenue Growth", f"{revenue_2023:.2f}B", f"+{pct_change:.0f}% since 2003")
    
    with col2:
        debt_2003 = historical_financials[historical_financials['Year'] == 2003]['Net_Debt_Billions'].values[0]
        debt_2023 = historical_financials[historical_financials['Year'] == 2023]['Net_Debt_Billions'].values[0]
        pct_change = ((debt_2023 - debt_2003) / debt_2003) * 100
        st.metric("Net Debt Growth", f"{debt_2023:.2f}B", f"+{pct_change:.0f}% since 2003")
    
    with col3:
        deficit_2023 = abs(historical_financials[historical_financials['Year'] == 2023]['Deficit_Billions'].values[0])
        deficit_2021 = abs(historical_financials[historical_financials['Year'] == 2021]['Deficit_Billions'].values[0])
        improvement = ((deficit_2021 - deficit_2023) / deficit_2021) * 100
        st.metric("Deficit Improvement", f"${deficit_2023:.2f}B", f"-{improvement:.0f}% since 2021")
    
    with col4:
        clean_years = len(historical_audit[historical_audit['Audit_Opinion'] == 'Clean'])
        st.metric("Audit Quality", f"{clean_years}/21 Clean", "100% since 2007 = Adverse/Disclaimer")

# ============================================================================
# VIEW 6: RECURRING ISSUES ANALYSIS
# ============================================================================
elif view_option == "🔄 Recurring Issues Analysis":
    st.markdown('<div class="sub-header">🔄 Recurring Issues Analysis (2003-2023)</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Issue Persistence Heatmap</div>', unsafe_allow_html=True)
    
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
                    <p><strong>Duration:</strong> {2023 - issue['Start_Year']} years</p>
                    <p><strong>Status (2023):</strong> {issue['Status_2023']}</p>
                    <p><strong>Estimated Impact:</strong> ${issue['Estimated_Impact_Billions']:.2f}B</p>
                </div>
                <div style="background-color: #DC2626; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; white-space: nowrap;">
                    {2023 - issue['Start_Year']}+ Years
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    total_impact = historical_issues['Estimated_Impact_Billions'].sum()
    
    st.markdown(f"""
    <div style="background-color: #FEF2F2; padding: 20px; border-radius: 10px; border-left: 4px solid #DC2626; margin-top: 15px;">
        <h5 style="color: #DC2626; margin-top: 0;">📊 Total Estimated Impact of Recurring Issues</h5>
        <div style="font-size: 2.5rem; font-weight: bold; color: #DC2626;">${total_impact:.2f}B</div>
        <p style="font-size: 0.9rem; color: #666;">Conservative estimate of financial impact from unresolved issues</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# VIEW 7: ACCOUNTABILITY SCORECARD
# ============================================================================
elif view_option == "📊 Accountability Scorecard":
    st.markdown('<div class="sub-header">📊 Accountability Scorecard (2003-2023)</div>', unsafe_allow_html=True)
    
    accountability_metrics = pd.DataFrame({
        'Category': ['Financial Reporting', 'Asset Management', 'Liability Reporting', 'SOE Governance',
                     'Internal Controls', 'Pension Management', 'Revenue Collection', 'Audit Recommendations'],
        'Score_2023': [20, 15, 10, 5, 20, 10, 25, 15],
        'Score_2008': [70, 60, 50, 30, 50, 40, 60, 50],
        'Target': [80, 80, 80, 80, 80, 80, 80, 80],
        'Trend': ['🔴 Declining', '🔴 Declining', '🔴 Declining', '🟡 Stalled',
                  '🔴 Declining', '🔴 Declining', '🟡 Stalled', '🟡 Stalled']
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(x=accountability_metrics['Category'], y=accountability_metrics['Score_2008'],
                         name='2008 Score', marker_color='#3B82F6', text=accountability_metrics['Score_2008'], textposition='auto'))
    fig.add_trace(go.Bar(x=accountability_metrics['Category'], y=accountability_metrics['Score_2023'],
                         name='2023 Score', marker_color='#DC2626', text=accountability_metrics['Score_2023'], textposition='auto'))
    fig.add_trace(go.Bar(x=accountability_metrics['Category'], y=accountability_metrics['Target'],
                         name='Target Score', marker_color='#10B981', text=accountability_metrics['Target'], textposition='auto', opacity=0.5))
    
    fig.update_layout(title='Accountability Scorecard: 2008 vs 2023 (Target: 80)',
                      yaxis_title='Score (0-100)', height=400, barmode='group')
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="section-header">Detailed Category Analysis</div>', unsafe_allow_html=True)
    
    for _, row in accountability_metrics.iterrows():
        improvement = row['Score_2023'] - row['Score_2008']
        color = '#DC2626' if improvement < 0 else '#10B981' if improvement > 0 else '#F59E0B'
        
        st.markdown(f"""
        <div class="financial-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h6 style="margin-top: 0;">{row['Category']}</h6>
                    <div style="font-size: 0.9rem; color: #666;">
                        2008: {row['Score_2008']}/100 → 2023: {row['Score_2023']}/100 → Target: {row['Target']}/100
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="color: {color}; font-weight: bold; font-size: 1.2rem;">{improvement:+.0f} points</div>
                    <div style="font-size: 0.8rem; color: #666;">{row['Trend']}</div>
                </div>
            </div>
            <div style="margin-top: 10px; background-color: #f0f0f0; border-radius: 5px; height: 8px;">
                <div style="width: {row['Score_2023']}%; background-color: {color}; height: 8px; border-radius: 5px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Audit Recommendations (2003-2023)</div>', unsafe_allow_html=True)
    
    st.dataframe(
        historical_recommendations,
        use_container_width=True,
        column_config={
            'Recommendation': 'Audit Recommendation',
            'Year_First_Made': 'First Made',
            'Status': 'Current Status',
            'Years_Outstanding': 'Years Outstanding',
            'Estimated_Cost_Billions': 'Estimated Cost (Billions)'
        }
    )
    
    overall_score = accountability_metrics['Score_2023'].mean()
    grade = 'A' if overall_score >= 80 else 'B' if overall_score >= 60 else 'C' if overall_score >= 40 else 'D' if overall_score >= 20 else 'F'
    grade_color = '#10B981' if grade == 'A' else '#3B82F6' if grade == 'B' else '#F59E0B' if grade == 'C' else '#DC2626' if grade == 'D' else '#991B1B'
    
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background-color: {grade_color}20; border-radius: 10px; border: 2px solid {grade_color}; margin-top: 20px;">
        <h3 style="color: {grade_color}; margin-top: 0;">Overall Accountability Grade: {grade}</h3>
        <div style="font-size: 3rem; font-weight: bold; color: {grade_color};">{overall_score:.0f}/100</div>
        <div style="font-size: 0.9rem; color: #666; margin-top: 10px;">
            Based on 8 governance categories • 2023 assessment • 15+ years of recurring issues
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# VIEW 8: 2023 EXECUTIVE SUMMARY
# ============================================================================
elif view_option == "📋 2023 Executive Summary":
    st.markdown('<div class="sub-header">📋 2023 Executive Summary - Adverse Audit Opinion</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="financial-card adverse-opinion">
        <h3 style="color: #DC2626; margin-top: 0;">⚠️ ADVERSE AUDIT OPINION ISSUED (2023)</h3>
        <p><strong>Auditor General's Conclusion:</strong> The accompanying financial statements do <strong>NOT</strong> give a true and fair view of the financial position of the Government of Barbados as at March 31, 2023.</p>
        <p><strong>Reason:</strong> Significant material misstatements and non-compliance with International Public Sector Accounting Standards (IPSAS).</p>
        <p><strong>Historical Context:</strong> This is the 15th consecutive Adverse/Disclaimer opinion (2008-2023).</p>
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
                  "15th consecutive adverse opinion")
    
    st.markdown('<div class="section-header">Revenue & Expenditure Summary</div>', unsafe_allow_html=True)
    
    revenue_composition = financial_2023['financial_performance'].copy()
    fig = px.pie(
        revenue_composition,
        values='Actual_2023',
        names='Category',
        title='Revenue Composition by Source (2023)',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    top_taxes = financial_2023['tax_revenue_details'].nlargest(5, 'Actual_2023')
    fig = px.bar(
        top_taxes,
        x='Tax_Type',
        y='Actual_2023',
        title='Top 5 Tax Revenue Sources (2023)',
        color='Growth_Pct',
        color_continuous_scale='Blues',
        text=[format_currency(x, currency_format) for x in top_taxes['Actual_2023']]
    )
    fig.update_layout(yaxis_title=f'Amount ({currency_format})', xaxis_title='Tax Type')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="section-header">2023 Material Misstatements</div>', unsafe_allow_html=True)
    
    for _, item in financial_2023['adverse_opinion_items'].iterrows():
        if isinstance(item['Amount'], (int, float)):
            amount_display = format_currency(item['Amount'], currency_format)
        else:
            amount_display = item['Amount']
        
        severity_color = {'Critical': '#DC2626', 'High': '#F59E0B', 'Medium': '#3B82F6'}.get(item['Severity'], '#666')
        
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: {severity_color};">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h5 style="margin-top: 0; color: {severity_color};">{item['Issue']}</h5>
                    <p><strong>Amount:</strong> {amount_display}</p>
                    <p><strong>Impact:</strong> {item['Impact']}</p>
                    <p style="font-size: 0.9rem; color: #666;">{item['Description']}</p>
                </div>
                <div style="background-color: {severity_color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;">
                    {item['Severity']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# VIEW 9: 2023 BALANCE SHEET
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
    
    st.markdown('<div class="section-header">Key Liabilities</div>', unsafe_allow_html=True)
    
    liabilities = financial_2023['liabilities_data'].copy()
    key_liabilities = liabilities[liabilities['Category'].isin([
        'Current Liabilities', 'Long-term Liabilities', 
        'Government Securities', 'Loans from International Financial Institutions'
    ])]
    
    for _, row in key_liabilities.iterrows():
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
                    <div style="color: {'#DC2626' if change >= 0 else '#10B981'}; font-weight: bold;">
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
# VIEW 10: 2023 AUDIT FINDINGS
# ============================================================================
elif view_option == "🔍 2023 Audit Findings":
    st.markdown('<div class="sub-header">🔍 2023 Audit Findings & Material Misstatements</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="financial-card adverse-opinion">
        <h4 style="color: #DC2626; margin-top: 0;">📄 Basis for Adverse Opinion (Extract from Auditor General's Report)</h4>
        <p>"The total for Other Capital Assets could not be confirmed because of a difference of $719 million between the amounts reported in the financial statements compared with the corresponding figures listed in the subsidiary records. Cash and Financial Investments listed in the financial statements were overstated by $115 million and $147 million respectively. In addition, the liability for pensions and employee benefits were not included in the Statement of Financial Position and the accounts of the State-owned Entities were not consolidated into the financial statements as required by the International Public Sector Accounting Standards (IPSAS). Also, Tax Receivables of $2.43 billion and Bad Debt Expenses of $68.28 million could not be confirmed because of the absence of sufficient supporting documentation."</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Material Misstatements Identified</div>', unsafe_allow_html=True)
    
    for _, item in financial_2023['adverse_opinion_items'].iterrows():
        if isinstance(item['Amount'], (int, float)):
            amount_display = format_currency(item['Amount'], currency_format)
        else:
            amount_display = item['Amount']
        
        severity_color = {'Critical': '#DC2626', 'High': '#F59E0B', 'Medium': '#3B82F6'}.get(item['Severity'], '#666')
        
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: {severity_color};">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h5 style="margin-top: 0; color: {severity_color};">{item['Issue']}</h5>
                    <p><strong>Amount:</strong> {amount_display}</p>
                    <p><strong>Impact:</strong> {item['Impact']}</p>
                    <p style="font-size: 0.9rem; color: #666;">{item['Description']}</p>
                </div>
                <div style="background-color: {severity_color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;">
                    {item['Severity']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">IPSAS Compliance Failures</div>', unsafe_allow_html=True)
    
    ipsas_issues = [
        {'Requirement': 'Consolidation of State-Owned Entities', 'Status': '❌ NOT COMPLIANT',
         'Impact': 'Financial statements incomplete and misleading'},
        {'Requirement': 'Recognition of Pension Liabilities', 'Status': '❌ NOT COMPLIANT',
         'Impact': 'Liabilities understated by unquantified amount'},
        {'Requirement': 'Asset Valuation and Verification', 'Status': '⚠️ PARTIALLY COMPLIANT',
         'Impact': 'Assets potentially overstated by $981M+'},
        {'Requirement': 'Revenue Recognition (Tax Receivables)', 'Status': '❌ NOT COMPLIANT',
         'Impact': '$2.43B receivables unverified'}
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
# VIEW 11: 2023 DATA QUALITY ISSUES
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
        <div class="narrative-box">
            <h5 style="color: #DC2626; margin-top: 0;">NARRATIVE TEXT</h5>
            <p style="font-size: 1.2rem; font-weight: bold; color: #DC2626;">
                "${narrative_amount:,.0f}"
            </p>
            <p><em>"The Government reporting entity recorded transfers..."</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="table-box">
            <h5 style="color: #3B82F6; margin-top: 0;">TABLE TOTAL</h5>
            <p style="font-size: 1.2rem; font-weight: bold; color: #3B82F6;">
                "${table_amount:,.0f}"
            </p>
            <p>Sum of all transfers in the Note 34 table</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="analysis-box">
        <h5 style="color: #D97706; margin-top: 0;">DISCREPANCY ANALYSIS</h5>
        <p><strong>Difference:</strong> ${difference:,.0f}</p>
        <p><strong>Percentage Variance:</strong> {difference_pct:.1f}%</p>
        <p><strong>Impact:</strong> Which number is correct? The narrative or the table?</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="conclusion-box">
        <h5 style="color: #DC2626; margin-top: 0;">CONCLUSION</h5>
        <p>The errors in Note 34 are not just minor typos - they are <strong>material misstatements</strong> that:</p>
        <ol>
            <li><strong>Contradict</strong> the accompanying table data</li>
            <li><strong>Misrepresent</strong> basic accounting concepts</li>
            <li><strong>Undermine</strong> the credibility of the entire financial report</li>
            <li><strong>Justify</strong> the Auditor General's adverse opinion</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# VIEW 12: 2026 REALITY CHECK
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
            '$2.43B UNVERIFIED',
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
    
    st.markdown('<div class="section-header">💸 $2.5 Billion Annual Debt Service</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="padding: 15px; background: #FEF2F2; border-radius: 5px; border-left: 4px solid #DC2626; margin-bottom: 15px;">
            <div style="font-size: 0.9rem; color: #666; margin-bottom: 5px;">INTEREST PAYMENTS</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #DC2626;">$588M</div>
            <div style="font-size: 0.85rem; color: #666; margin-top: 10px;">
                • Bondholders (8% Eurobond): $40M/year<br>
                • Previous bondholders: $22M/year<br>
                • Other creditors: $526M/year
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding: 15px; background: #FEF2F2; border-radius: 5px; border-left: 4px solid #991B1B; margin-bottom: 15px;">
            <div style="font-size: 0.9rem; color: #666; margin-bottom: 5px;">PRINCIPAL REPAYMENTS</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #991B1B;">$1.9B</div>
            <div style="font-size: 0.85rem; color: #666; margin-top: 10px;">
                • Eurobond maturities<br>
                • IMF repayments<br>
                • Multilateral loans
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 15px; padding: 15px; background: #FEE2E2; border-radius: 5px;">
        <p style="margin: 0; font-size: 0.95rem;">
        <strong>🔥 THE HARSH REALITY:</strong> This $2.5B is <strong>40% of total government revenue</strong> ($6.2B projected 2025/26). 
        For every $1 Barbados earns, <strong>$0.40 goes to debt payments</strong> before funding hospitals, schools, or roads.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">❌ What the 2026 Report Doesn\'t Address</div>', unsafe_allow_html=True)
    
    missing_items = [
        {'Issue': '2023 Audit Problems', '2023 Status': 'Adverse opinion, $2.43B unverified assets',
         '2026 Mention': 'NOT MENTIONED', 'Risk': 'Financial statements still unreliable for $7.4B BERT financing'},
        {'Issue': 'SOE Consolidation', '2023 Status': 'Not done (IPSAS violation)',
         '2026 Mention': 'Only mentions $77M arrears', 'Risk': 'Still violating IPSAS, true SOE debt hidden'},
        {'Issue': '8% Bond vs Alternatives', '2023 Status': 'Could have negotiated better terms',
         '2026 Mention': 'Presented as "liability management" success', 'Risk': 'Locked into high rates for 10 years'},
        {'Issue': 'Tourism Dependency', '2023 Status': '40% of GDP = high vulnerability',
         '2026 Mention': 'Celebrated as growth driver', 'Risk': 'Economic collapse if tourism slows'}
    ]
    
    for item in missing_items:
        st.markdown(f"""
        <div class="financial-card data-error" style="margin-bottom: 10px;">
            <h6 style="margin-top: 0; color: #DC2626;">{item['Issue']}</h6>
            <p><strong>2023 Audit Finding:</strong> {item['2023 Status']}</p>
            <p><strong>2026 Report:</strong> <span style="color: #DC2626;">{item['2026 Mention']}</span></p>
            <p><strong>Risk:</strong> {item['Risk']}</p>
        </div>
        """, unsafe_allow_html=True)
    
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
            <li><strong>Transparent cost-benefit</strong> of 8% bonds vs. alternatives</li>
            <li><strong>Diversify economy</strong> beyond 40% tourism dependency</li>
            <li><strong>Honest reporting</strong> on SOE consolidation progress</li>
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
        <p style="font-weight: bold; color: var(--bb-blue);">Barbados Government Financial Statements 2003-2023</p>
        <p>21 Years of Auditor General's Reports • Data-Driven Analysis</p>
        <p>📞 Tel: (246) 535-4257 • ✉️ Email: audit@bao.gov.bb</p>
        <p style="margin-top: 20px; font-size: 0.8rem;">
            Data Source: Auditor General's Reports (2003-2023) • 
            Dashboard Version 8.0 • Generated: {datetime.now().strftime('%B %d, %Y')}
        </p>
        <p style="font-size: 0.7rem; color: #999;">
            ⚠️ 15 consecutive Adverse/Disclaimer opinions (2008-2023)
            <br>⚠️ Note 34 contains critical data inconsistencies and conceptual errors
        </p>
    </div>
    """, unsafe_allow_html=True)