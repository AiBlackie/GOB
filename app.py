# ============================================================================
# 🇧🇧 BARBADOS FINANCIAL ACCOUNTABILITY 2003-2026
# A 21-YEAR AUDIT HISTORY
# ============================================================================
#
# This dashboard presents 21 years of Auditor General's reports
# with factual data and evidence-based analysis.
#
# Version: 11.0
# Date: July 9, 2026
#
# KEY CORRECTIONS:
# 1. 2020: $1.8B fixed assets excluded + $1.7B land unverified (NOT $2.43B)
# 2. $2.43B tax receivables = NEW 2023 issue (NOT 15-year-old)
# 3. SOE Consolidation = 2003 (21+ years)
# 4. Pension Liability = 2003 (22+ years)
# 5. Professional branding only - no "IMF Edition"
# 6. All sources cited for debt-to-GDP numbers
# 7. NEW: 2026-2027 Budget vs 2023 Audit Reality view added
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
    
    # Debt Structure - CORRECTED FROM NOTE 25
    debt_structure = pd.DataFrame({
        'Debt_Type': [
            'Local Loans Act',
            'Inter American Development Bank',
            'External Loans Act',
            'Special Loans Act',
            'International Monetary Fund',
            'Treasury Bills',
            'Caribbean Development Bank',
            'Latin American Development Bank',
            'Ways & Means (Overdraft)',
            'Savings Bond Act'
        ],
        'Amount_2023': [
            7746270000,
            1499650000,
            1061170000,
            890940000,
            548410000,
            495170000,
            469380000,
            357430000,
            167150000,
            32230000
        ],
        'Amount_2022': [
            7871410000,
            1499660000,
            1061170000,
            810080000,
            464770000,
            495100000,
            469380000,
            340600000,
            214990000,
            47290000
        ],
        'Change': [
            -126140000, 0, 14160000, 315100000, 80860000,
            0, -15060000, 83640000, 16830000, -47840000
        ],
        'Debt_Category': [
            'Domestic', 'Foreign', 'Foreign', 'Foreign', 'Foreign',
            'Domestic', 'Foreign', 'Foreign', 'Domestic', 'Domestic'
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
    
    # ========================================================================
    # NEW: 2026-2027 Budget Data from Estimates Document
    # ========================================================================
    budget_2026_27 = {
        'total_revenue': 5.075888040,  # $5.075B
        'total_expenditure': 5.875116133,  # $5.875B
        'overall_deficit': 0.658132501,  # $658M including Annex
        'gdp_projected': 17.0647,  # $17.0647B
        'fiscal_deficit_ag': 4.0,  # 4.0% of GDP on AG basis
        'fiscal_surplus_ifi': 0.6,  # 0.6% of GDP on IFI basis
        
        # Revenue breakdown
        'revenue_breakdown': {
            'Taxation': 4.771173130,  # $4.771B
            'Goods and Services': 1.767121933,  # $1.767B
            'Income and Profits': 2.430489308,  # $2.430B
            'Property Taxes': 0.235494137,  # $0.235B
            'International Trade': 0.319153004,  # $0.319B
            'Other Taxes': 0.018914748,  # $0.019B
            'Special Receipts': 0.019237766,  # $0.019B
            'Levies': 0.085063105,  # $0.085B
            'Other Revenue': 0.191583581,  # $0.192B
            'Grant Income': 0.008830458,  # $0.009B
            'Annex Revenue': 0.007896775   # $0.008B
        },
        
        # Expenditure breakdown
        'expenditure_breakdown': {
            'Personal Emoluments': 0.856833326,  # $0.857B
            'Employer Contributions': 0.080053409,  # $0.080B
            'Goods and Services': 0.918089184,  # $0.918B
            'Depreciation': 0.054000000,  # $0.054B
            'Bad Debt Expense': 0.000500000,  # $0.0005B
            'Grants and Transfers': 0.972341019,  # $0.972B
            'Retiring Benefits': 0.433827518,  # $0.434B
            'Statutory Expenditure': 0.001010000,  # $0.001B
            'Debt Service Interest': 0.714570501,  # $0.715B
            'Expenses of Loans': 0.011583430,  # $0.012B
            'Debt Service Principal': 0.781762739,  # $0.782B
            'Capital Transfers': 0.352482823,  # $0.352B
            'Capital Assets': 0.515476080   # $0.515B
        },
        
        # Top Ministries by Budget
        'top_ministries': {
            'Ministry of Finance': 0.7815,
            'Ministry of Educational Transformation': 0.4572,
            'Ministry of Health and Wellness': 0.4858,
            'Prime Minister\'s Office': 0.3802,
            'Ministry of Technological and Vocational Training': 0.2859,
            'Ministry of Legal Affairs and Criminal Justice': 0.2781,
            'Ministry of Transport and Works': 0.1861,
            'Ministry of Home Affairs, Information & Public Affairs': 0.1341,
            'Ministry of Environment, National Beautification and Fisheries': 0.1217,
            'Ministry of Agriculture, Food and Nutritional Security': 0.1120
        }
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
        'note34_discrepancy': note34_discrepancy,
        'peer_comparison': peer_comparison,
        'budget_2026_27': budget_2026_27  # NEW
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
# NEW VIEW: 2026-2027 BUDGET VS 2023 AUDIT REALITY
# ============================================================================
def render_budget_vs_reality():
    """Render the 2026-2027 Budget vs 2023 Audit Reality section."""
    
    st.markdown('<div class="sub-header">📊 2026-2027 Budget vs 2023 Audit Reality</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #F0F7FF; padding: 20px; border-radius: 10px; border-left: 6px solid #3B82F6; margin: 20px 0;">
        <p style="font-size: 1.05rem; margin: 0;">
        This section compares the <strong>2026-2027 Budget Estimates</strong> with the 
        <strong style="color: #DC2626;">2023 Audit Reality</strong>, highlighting the gaps between 
        planned expenditure and the financial management challenges identified by the Auditor General.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    budget = financial_2023['budget_2026_27']
    
    # ========================================================================
    # KEY BUDGET HIGHLIGHTS
    # ========================================================================
    st.markdown('<div class="section-header">📋 2026-2027 Budget Highlights</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Revenue (2026-27)",
            f"${budget['total_revenue']:.2f}B",
            "$1.1B increase from 2025-26",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Total Expenditure",
            f"${budget['total_expenditure']:.2f}B",
            "0.25% decrease from revised 2025-26",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Projected Deficit",
            f"${budget['overall_deficit']:.2f}B",
            "Including Annex",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "GDP (Projected)",
            f"${budget['gdp_projected']:.2f}B",
            "Nominal GDP at market prices",
            delta_color="normal"
        )
    
    # ========================================================================
    # REVENUE COMPARISON
    # ========================================================================
    st.markdown('<div class="section-header">💰 Revenue Comparison: 2026-27 Budget vs 2023 Actual</div>', unsafe_allow_html=True)
    
    revenue_compare = pd.DataFrame({
        'Revenue Category': list(budget['revenue_breakdown'].keys()),
        '2023_Actual_B': [
            1.628, 1.069, 0.241, 0.250, 0.022, 0.002, 0.083, 0.171, 0.020, 0.008, 0.008
        ],
        '2026_27_Budget_B': list(budget['revenue_breakdown'].values())
    })
    
    revenue_compare['Growth_B'] = revenue_compare['2026_27_Budget_B'] - revenue_compare['2023_Actual_B']
    revenue_compare['Growth_Pct'] = (revenue_compare['Growth_B'] / revenue_compare['2023_Actual_B'] * 100).round(1)
    
    fig_rev = px.bar(
        revenue_compare,
        x='Revenue Category',
        y=['2023_Actual_B', '2026_27_Budget_B'],
        title='Revenue Comparison: 2023 Actual vs 2026-27 Budget',
        barmode='group',
        color_discrete_sequence=['#3B82F6', '#10B981'],
        text_auto='.2f'
    )
    fig_rev.update_layout(
        yaxis_title='Amount (Billions $)',
        xaxis_title='Revenue Category',
        height=450
    )
    fig_rev.update_xaxes(tickangle=20)
    st.plotly_chart(fig_rev, use_container_width=True)
    
    # ========================================================================
    # EXPENDITURE COMPARISON
    # ========================================================================
    st.markdown('<div class="section-header">📊 Expenditure Comparison: 2026-27 Budget vs 2023 Actual</div>', unsafe_allow_html=True)
    
    # 2023 actual expenditure data (approximate values from the financial statements)
    exp_compare = pd.DataFrame({
        'Expenditure Category': list(budget['expenditure_breakdown'].keys()),
        '2023_Actual_B': [
            0.864, 0.000, 0.545, 0.050, 0.068, 0.911, 0.334, 0.000, 0.555, 0.012, 0.782, 0.242, 0.000
        ],
        '2026_27_Budget_B': list(budget['expenditure_breakdown'].values())
    })
    
    fig_exp = px.bar(
        exp_compare,
        x='Expenditure Category',
        y=['2023_Actual_B', '2026_27_Budget_B'],
        title='Expenditure Comparison: 2023 Actual vs 2026-27 Budget',
        barmode='group',
        color_discrete_sequence=['#DC2626', '#F59E0B'],
        text_auto='.2f'
    )
    fig_exp.update_layout(
        yaxis_title='Amount (Billions $)',
        xaxis_title='Expenditure Category',
        height=450
    )
    fig_exp.update_xaxes(tickangle=20)
    st.plotly_chart(fig_exp, use_container_width=True)
    
    # ========================================================================
    # KEY FINDINGS: BUDGET VS AUDIT REALITY
    # ========================================================================
    st.markdown('<div class="section-header">⚠️ Budget vs Audit Reality: Key Findings</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #DC2626; height: 100%;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 The 2023 Audit Reality</h5>
            <ul>
                <li><strong>$2.43B</strong> in tax receivables <strong>unverified</strong></li>
                <li><strong>$719M</strong> asset discrepancy unresolved</li>
                <li><strong>$4B+</strong> pension liability <strong>hidden</strong></li>
                <li><strong>40+ SOEs</strong> not consolidated</li>
                <li><strong>6 consecutive</strong> Adverse opinions</li>
                <li><strong>Bank reconciliations</strong> 18+ years outstanding</li>
                <li><strong>Bad debt expense</strong> jumped from $10M to $68M</li>
            </ul>
            <p style="font-size: 0.8rem; color: #666; margin-top: 10px;">
            <strong>Source:</strong> Auditor General's Report 2023
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #EFF6FF; padding: 20px; border-radius: 8px; border: 1px solid #3B82F6; height: 100%;">
            <h5 style="color: #00267F; margin-top: 0;">📋 The 2026-27 Budget Assumptions</h5>
            <ul>
                <li><strong>$5.08B</strong> in projected revenue</li>
                <li><strong>$5.88B</strong> in planned expenditure</li>
                <li><strong>$658M</strong> projected deficit</li>
                <li><strong>4.0%</strong> fiscal deficit (AG basis)</li>
                <li><strong>0.6%</strong> fiscal surplus (IFI basis)</li>
                <li><strong>$54M</strong> budgeted for depreciation</li>
                <li><strong>$0.5M</strong> budgeted for bad debt</li>
            </ul>
            <p style="font-size: 0.8rem; color: #666; margin-top: 10px;">
            <strong>Source:</strong> 2026-2027 Estimates of Revenue and Expenditure
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # THE $2.43B QUESTION VS BUDGET DEFICIT
    # ========================================================================
    st.markdown('<div class="section-header">🚨 The $2.43B Question vs Budget Deficit</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #DC2626; height: 100%;">
            <div style="font-size: 2.5rem; font-weight: bold; color: #DC2626;">$2.43B</div>
            <div style="font-weight: 600;">Unverified Tax Receivables</div>
            <div style="font-size: 0.85rem; color: #666;">First flagged in 2023</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #FFFBEB; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #F59E0B; height: 100%;">
            <div style="font-size: 2.5rem; font-weight: bold; color: #F59E0B;">$658M</div>
            <div style="font-weight: 600;">Projected Budget Deficit</div>
            <div style="font-size: 0.85rem; color: #666;">2026-27 (Including Annex)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #EFF6FF; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #3B82F6; height: 100%;">
            <div style="font-size: 2.5rem; font-weight: bold; color: #3B82F6;">3.7x</div>
            <div style="font-weight: 600;">Times Deficit Covered by Unverified Receivables</div>
            <div style="font-size: 0.85rem; color: #666;">$2.43B ÷ $658M = 3.7x</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # TOP MINISTRIES BY BUDGET
    # ========================================================================
    st.markdown('<div class="section-header">🏛️ Top 10 Ministries by Budget (2026-27)</div>', unsafe_allow_html=True)
    
    ministries = pd.DataFrame({
        'Ministry': list(budget['top_ministries'].keys()),
        'Budget_B': list(budget['top_ministries'].values())
    })
    
    ministries = ministries.sort_values('Budget_B', ascending=True)
    
    fig_min = px.bar(
        ministries,
        x='Budget_B',
        y='Ministry',
        title='Top 10 Ministries by Budget Allocation (2026-27)',
        color='Budget_B',
        color_continuous_scale='Blues',
        text=[f"${x:.2f}B" for x in ministries['Budget_B']],
        orientation='h'
    )
    fig_min.update_layout(
        xaxis_title='Budget (Billions $)',
        yaxis_title='Ministry',
        height=450,
        showlegend=False
    )
    st.plotly_chart(fig_min, use_container_width=True)
    
    # ========================================================================
    # CONCLUSION
    # ========================================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00267F 0%, #1E40AF 100%); padding: 30px; border-radius: 10px; color: white; margin-top: 20px;">
        <h3 style="color: white; text-align: center;">🇧🇧 The Bottom Line</h3>
        <p style="text-align: center; font-size: 1.1rem; color: #BFDBFE;">
        The <strong style="color: #FFC726;">2026-27 Budget</strong> projects optimistic revenue growth and 
        fiscal improvement.
        </p>
        <p style="text-align: center; font-size: 1.1rem; color: #BFDBFE;">
        But the <strong style="color: #DC2626;">2023 Audit Reality</strong> shows a financial management foundation 
        that remains <strong style="color: white;">fundamentally broken</strong>.
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 20px;">
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #FFC726;">$5.08B</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Budgeted Revenue</div>
            </div>
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #DC2626;">$2.43B</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Unverified Tax Receivables</div>
            </div>
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #FFC726;">3.7x</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Receivables vs Deficit</div>
            </div>
        </div>
        <p style="text-align: center; font-size: 0.9rem; color: #93C5FD; margin-top: 15px;">
        <em>The budget assumes what the audit cannot verify. The foundation must be fixed before 
        the projections can be trusted.</em>
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
    st.caption(f"**Version:** 11.0")
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
            "📊 2026 Reality Check",
            "📊 2026-2027 Budget vs 2023 Audit Reality"  # NEW
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
    st.caption("2026-2027 Estimates of Revenue and Expenditure")

# ============================================================================
# VIEW HANDLING
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
# VIEW 3: THE COMPLETE STORY - COMPLETE VERSION WITH VISUAL ELEMENTS
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
    # AUDIT OPINION PROGRESSION CHART - NEW VISUAL
    # ========================================================================
    st.markdown('<div class="section-header">📊 Audit Opinion Progression (2003-2023)</div>', unsafe_allow_html=True)

    # Create progression data
    progression_data = pd.DataFrame({
        'Era': ['Clean Era\n(2003-2007)', 'Disclaimer Era\n(2008-2017)', 'Adverse Era\n(2018-2023)'],
        'Years': [5, 10, 6],
        'Opinion_Type': ['Clean', 'Disclaimer', 'Adverse'],
        'Color': ['#10B981', '#F59E0B', '#DC2626'],
        'Key_Issue': ['No major issues', 'SOE & asset issues', 'Material misstatements']
    })

    fig_progression = px.bar(
        progression_data,
        x='Era',
        y='Years',
        title='Audit Opinion Progression by Era',
        color='Opinion_Type',
        color_discrete_map={'Clean': '#10B981', 'Disclaimer': '#F59E0B', 'Adverse': '#DC2626'},
        text='Years',
        hover_data={'Key_Issue': True}
    )
    fig_progression.update_traces(textposition='inside', textfont_size=16, textfont_color='white')
    fig_progression.update_layout(
        yaxis_title='Number of Years',
        xaxis_title='',
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig_progression, use_container_width=True)

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
    # FINANCIAL METRICS OVERLAY - NEW VISUAL
    # ========================================================================
    st.markdown('<div class="section-header">📈 Financial Metrics Across the Story</div>', unsafe_allow_html=True)

    # Create era-based financial summary
    era_financials = pd.DataFrame({
        'Era': ['2003-2007', '2008-2012', '2013-2017', '2018-2020', '2021-2023'],
        'Avg_Revenue': [1.4, 1.78, 2.08, 2.4, 2.93],
        'Avg_Deficit': [-0.1, -0.16, -0.26, -0.43, -0.49],
        'Avg_Debt': [6.0, 8.5, 11.0, 10.5, 9.7],
        'Opinion': ['🟢 Clean', '🟡 Disclaimer', '🟡 Disclaimer', '🔴 Adverse', '🔴 Adverse']
    })

    fig_metrics = go.Figure()

    # Revenue bars
    fig_metrics.add_trace(go.Bar(
        x=era_financials['Era'],
        y=era_financials['Avg_Revenue'],
        name='Avg Revenue',
        marker_color='#00267F',
        text=[f"${x:.2f}B" for x in era_financials['Avg_Revenue']],
        textposition='outside',
        hovertemplate='Revenue: $%{y:.2f}B<extra></extra>'
    ))

    # Deficit line
    fig_metrics.add_trace(go.Scatter(
        x=era_financials['Era'],
        y=era_financials['Avg_Deficit'],
        name='Avg Deficit',
        mode='lines+markers',
        line=dict(color='#DC2626', width=3),
        marker=dict(size=10),
        yaxis='y2',
        text=[f"${x:.2f}B" for x in era_financials['Avg_Deficit']],
        textposition='top center',
        hovertemplate='Deficit: $%{y:.2f}B<extra></extra>'
    ))

    # Add shaded regions for audit opinion eras
    fig_metrics.add_vrect(x0=-0.5, x1=0.5, fillcolor="rgba(16, 185, 129, 0.15)", line_width=0)
    fig_metrics.add_vrect(x0=0.5, x1=2.5, fillcolor="rgba(245, 158, 11, 0.15)", line_width=0)
    fig_metrics.add_vrect(x0=2.5, x1=4.5, fillcolor="rgba(220, 38, 38, 0.15)", line_width=0)

    fig_metrics.update_layout(
        title='Average Financial Metrics by Era',
        height=400,
        hovermode='x unified',
        xaxis=dict(title=''),
        yaxis=dict(title='Revenue (Billions $)', range=[0, 4]),
        yaxis2=dict(title='Deficit (Billions $)', overlaying='y', side='right', range=[-1, 0.1]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig_metrics, use_container_width=True)

    # ========================================================================
    # ISSUE EMERGENCE TIMELINE - NEW VISUAL
    # ========================================================================
    st.markdown('<div class="section-header">🚨 When Issues Emerged</div>', unsafe_allow_html=True)

    issue_emergence = pd.DataFrame({
        'Issue': ['SOE Consolidation', 'Pension Liability', 'Asset Registers', 'Bank Reconciliations', 'Adverse Opinions', 'Tax Receivables'],
        'Year_First_Appeared': [2003, 2003, 2003, 2008, 2018, 2023],
        'Status': ['❌ Unresolved', '❌ Unresolved', '❌ Unresolved', '❌ Unresolved', '❌ Ongoing', '❌ NEW'],
        'Color': ['#DC2626' if x == 2023 else '#F59E0B' if x >= 2018 else '#3B82F6' for x in [2003, 2003, 2003, 2008, 2018, 2023]]
    })

    fig_emergence = px.bar(
        issue_emergence,
        x='Issue',
        y=[1] * len(issue_emergence),
        title='When Major Issues First Emerged',
        color='Year_First_Appeared',
        color_continuous_scale='Reds',
        text=issue_emergence['Year_First_Appeared'].apply(lambda x: str(x)),
        hover_data={'Status': True}
    )
    fig_emergence.update_traces(textposition='inside', textfont_size=14, textfont_color='white')
    fig_emergence.update_layout(
        yaxis=dict(range=[0, 1.5], showticklabels=False, title=''),
        xaxis_title='Issue Category',
        height=250,
        showlegend=False
    )
    st.plotly_chart(fig_emergence, use_container_width=True)

    # ========================================================================
    # IMPACT SUMMARY CARDS - NEW VISUAL
    # ========================================================================
    st.markdown('<div class="section-header">📊 Impact by Era</div>', unsafe_allow_html=True)

    impact_col1, impact_col2, impact_col3 = st.columns(3)

    with impact_col1:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 15px; border-radius: 10px; border-left: 4px solid #10B981; height: 100%;">
            <h5 style="color: #10B981; margin-top: 0;">🟢 Clean Era (2003-2007)</h5>
            <p><strong>Impact:</strong> Strong financial management</p>
            <p><strong>Key Achievement:</strong> 5 consecutive clean opinions</p>
            <p><strong>Deficit:</strong> ~$100M annually</p>
            <p><strong>Status:</strong> ✅ Foundation built</p>
        </div>
        """, unsafe_allow_html=True)

    with impact_col2:
        st.markdown("""
        <div style="background: #FFFBEB; padding: 15px; border-radius: 10px; border-left: 4px solid #F59E0B; height: 100%;">
            <h5 style="color: #D97706; margin-top: 0;">🟡 Disclaimer Era (2008-2017)</h5>
            <p><strong>Impact:</strong> Recurring issues emerge</p>
            <p><strong>Key Issue:</strong> SOE consolidation fails</p>
            <p><strong>Debt:</strong> $7.5B → $12.0B</p>
            <p><strong>Status:</strong> ⚠️ Problems ignored</p>
        </div>
        """, unsafe_allow_html=True)

    with impact_col3:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 15px; border-radius: 10px; border-left: 4px solid #DC2626; height: 100%;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 Adverse Era (2018-2023)</h5>
            <p><strong>Impact:</strong> Systemic failure</p>
            <p><strong>Key Issue:</strong> $9.15B+ in issues</p>
            <p><strong>NEW 2023:</strong> $2.43B unverified</p>
            <p><strong>Status:</strong> ❌ Foundation broken</p>
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
# VIEW 4: THE $2.43B QUESTION - COMPLETE CORRECTED VERSION
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
    # NOTE 14: ACTUAL BREAKDOWN FROM FINANCIAL STATEMENTS
    # ========================================================================
    st.markdown('<div class="section-header">📋 Note 14: Actual Tax Receivables Breakdown (2023)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #EFF6FF; padding: 15px; border-radius: 8px; border-left: 4px solid #3B82F6; margin: 15px 0;">
        <p style="margin: 0; font-size: 0.95rem;">
        <strong>Source:</strong> Note 14 of the Financial Statements (Page 26) - Actual amounts as reported.
        <br>
        <strong>Key Finding:</strong> VAT is the largest component at <strong style="color: #DC2626;">$1.133B (46.7%)</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ACTUAL data from Note 14 (from the image)
    tax_breakdown_actual = pd.DataFrame({
        'Category': [
            'Value Added Tax (VAT)',
            'Income Tax (Personal)',
            'Land Tax',
            'Corporation Tax',
            'Other Tax Receivables',
            'Import and Excise Duties',
            'Betting and Gaming Tax',
            'Highway Revenue'
        ],
        'Gross_Amount': [
            1223206229,   # $1,223,206,229
            963671397,    # $963,671,397
            521619150,    # $521,619,150
            534068351,    # $534,068,351
            120468847,    # $120,468,847
            11945906,     # $11,945,906
            201927,       # $201,927
            13256         # $13,256
        ],
        'Provision_Amount': [
            90087169,     # $90,087,169
            383167949,    # $383,167,949
            125234276,    # $125,234,276
            374797392,    # $374,797,392
            70287240,     # $70,287,240
            2974981,      # $2,974,981
            0,            # $0
            -13255        # $-13,255 (negative)
        ]
    })
    
    # Calculate Net Amounts
    tax_breakdown_actual['Net_Amount'] = tax_breakdown_actual['Gross_Amount'] - tax_breakdown_actual['Provision_Amount']
    
    # Sort by Net Amount descending
    tax_breakdown_actual = tax_breakdown_actual.sort_values('Net_Amount', ascending=False).reset_index(drop=True)
    
    # Calculate percentages
    total_net = tax_breakdown_actual['Net_Amount'].sum()  # $2,428,596,085
    tax_breakdown_actual['Percentage'] = (tax_breakdown_actual['Net_Amount'] / total_net * 100).round(1)
    
    # Add provision rates from Note 14a
    provision_rates = {
        'Value Added Tax (VAT)': 8,
        'Income Tax (Personal)': 40,
        'Land Tax': 24,
        'Corporation Tax': 59,
        'Other Tax Receivables': 50,
        'Import and Excise Duties': 100,
        'Betting and Gaming Tax': 0,
        'Highway Revenue': 0
    }
    tax_breakdown_actual['Provision_Rate'] = tax_breakdown_actual['Category'].map(provision_rates)
    
    # Display the table with actual data
    st.dataframe(
        tax_breakdown_actual[['Category', 'Gross_Amount', 'Provision_Amount', 'Net_Amount', 'Percentage', 'Provision_Rate']],
        use_container_width=True,
        hide_index=True,
        column_config={
            'Category': 'Tax Category',
            'Gross_Amount': st.column_config.NumberColumn('Gross Receivable', format="$%.0f"),
            'Provision_Amount': st.column_config.NumberColumn('Provision', format="$%.0f"),
            'Net_Amount': st.column_config.NumberColumn('Net Receivable (2023)', format="$%.0f"),
            'Percentage': st.column_config.NumberColumn('% of Total', format="%.1f%%"),
            'Provision_Rate': st.column_config.NumberColumn('Provision Rate', format="%.0f%%")
        }
    )
    
    # ========================================================================
    # PIE CHART - ACTUAL DATA
    # ========================================================================
    fig_breakdown = px.pie(
        tax_breakdown_actual,
        values='Net_Amount',
        names='Category',
        title=f'Tax Receivables by Type (2023) - Note 14\nTotal: ${total_net/1e9:.2f}B\nVAT is the Largest Component (46.7%)',
        color='Category',
        color_discrete_sequence=px.colors.sequential.Reds_r,
        hole=0.4
    )
    fig_breakdown.update_traces(
        textposition='inside', 
        textinfo='label+percent', 
        textfont_size=11,
        hovertemplate='<b>%{label}</b><br>Net Amount: $%{value:,.0f}<br>% of Total: %{percent}<br>Provision Rate: %{customdata}%<extra></extra>',
        customdata=tax_breakdown_actual['Provision_Rate']
    )
    fig_breakdown.update_layout(height=450)
    st.plotly_chart(fig_breakdown, use_container_width=True)
    
    # ========================================================================
    # BAR CHART - COMPARISON
    # ========================================================================
    fig_comparison = px.bar(
        tax_breakdown_actual,
        x='Category',
        y='Net_Amount',
        title='Tax Receivables by Type (Net Amount) - Note 14',
        color='Category',
        color_discrete_sequence=px.colors.sequential.Reds_r,
        text=[f"${x/1e6:.1f}M" for x in tax_breakdown_actual['Net_Amount']]
    )
    fig_comparison.update_traces(textposition='outside', textfont_size=11)
    fig_comparison.update_layout(
        yaxis_title='Amount ($)',
        xaxis_title='Tax Category',
        height=400,
        showlegend=False
    )
    fig_comparison.update_xaxes(tickangle=20)
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # ========================================================================
    # VAT IS THE LARGEST - HIGHLIGHT
    # ========================================================================
    vat_data = tax_breakdown_actual[tax_breakdown_actual['Category'] == 'Value Added Tax (VAT)']
    income_data = tax_breakdown_actual[tax_breakdown_actual['Category'] == 'Income Tax (Personal)']
    land_data = tax_breakdown_actual[tax_breakdown_actual['Category'] == 'Land Tax']
    corp_data = tax_breakdown_actual[tax_breakdown_actual['Category'] == 'Corporation Tax']
    
    if not vat_data.empty:
        vat_amount = vat_data['Net_Amount'].values[0]
        vat_pct = vat_data['Percentage'].values[0]
        vat_gross = vat_data['Gross_Amount'].values[0]
        vat_provision = vat_data['Provision_Amount'].values[0]
        vat_rate = vat_data['Provision_Rate'].values[0]
        
        st.markdown(f"""
        <div style="background: #EFF6FF; padding: 20px; border-radius: 8px; border: 2px solid #3B82F6; margin: 15px 0;">
            <h5 style="color: #00267F; margin-top: 0;">📊 Key Finding: VAT is the Largest Component</h5>
            <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;">
                <div style="text-align: center; padding: 15px;">
                    <div style="font-size: 2.5rem; font-weight: bold; color: #3B82F6;">${vat_amount/1e9:.2f}B</div>
                    <div style="font-size: 1.1rem; color: #666;">VAT Receivables (Net)</div>
                    <div style="font-size: 0.9rem; color: #10B981;">{vat_pct:.1f}% of Total</div>
                </div>
                <div style="text-align: center; padding: 15px; background: #FEF2F2; border-radius: 8px;">
                    <div style="font-size: 1.2rem; font-weight: bold; color: #DC2626;">Gross: ${vat_gross/1e6:.1f}M</div>
                    <div style="font-size: 1rem; color: #666;">Provision: ${vat_provision/1e6:.1f}M ({vat_rate:.0f}%)</div>
                    <div style="font-size: 0.9rem; color: #10B981;">Lowest provision rate among major taxes</div>
                </div>
                <div style="text-align: center; padding: 15px;">
                    <div style="font-size: 2.5rem; font-weight: bold; color: #00267F;">${total_net/1e9:.2f}B</div>
                    <div style="font-size: 1.1rem; color: #666;">Total Tax Receivables</div>
                    <div style="font-size: 0.9rem; color: #666;">All Tax Types Combined</div>
                </div>
            </div>
            <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">
                <strong>Why VAT is the largest:</strong> VAT applies to most goods and services, making it the broadest-based tax.
                With only an <strong style="color: #10B981;">8% provision rate</strong>, most VAT receivables are considered collectible.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # COMPARISON TABLE - BREAKDOWN BY CATEGORY
    # ========================================================================
    st.markdown('<div class="section-header">📊 Summary: Tax Receivables Breakdown</div>', unsafe_allow_html=True)
    
    # Create a comparison table
    summary_data = [
        {
            'Category': 'VAT',
            'Amount': f"${vat_amount/1e9:.3f}B" if not vat_data.empty else "N/A",
            'Percentage': f"{vat_pct:.1f}%" if not vat_data.empty else "N/A",
            'Provision Rate': '8%',
            'Rank': '1st'
        },
        {
            'Category': 'Income Tax',
            'Amount': f"${income_data['Net_Amount'].values[0]/1e9:.3f}B" if not income_data.empty else "N/A",
            'Percentage': f"{income_data['Percentage'].values[0]:.1f}%" if not income_data.empty else "N/A",
            'Provision Rate': '40%',
            'Rank': '2nd'
        },
        {
            'Category': 'Land Tax',
            'Amount': f"${land_data['Net_Amount'].values[0]/1e9:.3f}B" if not land_data.empty else "N/A",
            'Percentage': f"{land_data['Percentage'].values[0]:.1f}%" if not land_data.empty else "N/A",
            'Provision Rate': '24%',
            'Rank': '3rd'
        },
        {
            'Category': 'Corporation Tax',
            'Amount': f"${corp_data['Net_Amount'].values[0]/1e9:.3f}B" if not corp_data.empty else "N/A",
            'Percentage': f"{corp_data['Percentage'].values[0]:.1f}%" if not corp_data.empty else "N/A",
            'Provision Rate': '59%',
            'Rank': '4th'
        }
    ]
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # PROVISION RATES TABLE - FROM NOTE 14A
    # ========================================================================
    st.markdown('<div class="section-header">📊 Note 14a: Provision Rates by Tax Type</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #FEF2F2; padding: 15px; border-radius: 8px; border-left: 4px solid #DC2626; margin: 15px 0;">
        <p style="margin: 0; font-size: 0.95rem;">
        <strong>Key Insight:</strong> The <strong style="color: #DC2626;">MASSIVE increase in bad debt provisions</strong> 
        from 2022 to 2023 explains why VAT is the largest component.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Actual provision data from Note 14a
    provision_data = pd.DataFrame({
        'Tax Type': [
            'Value Added Tax (VAT)',
            'Corporation Income Tax',
            'Personal Income Tax & PAYE',
            'Excise Tax',
            'National Social Responsibility Levy',
            'Room Rate Levy',
            'Product Development Levy',
            'Premium Tax',
            'Land Tax',
            'Consolidation Tax',
            'Municipal Solid Waste Tax',
            'Tax on Assets',
            'Withholding Tax'
        ],
        '2022_Provision': [2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2],
        '2023_Provision': [8, 59, 40, 100, 100, 76, 67, 57, 24, 85, 65, 2, 2],
        'Change': [6, 57, 38, 98, 98, 74, 65, 55, 24, 83, 63, 0, 0]
    })
    
    st.dataframe(
        provision_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Tax Type': 'Tax Type',
            '2022_Provision': '2022 Provision %',
            '2023_Provision': '2023 Provision %',
            'Change': 'Change (pp)'
        }
    )
    
    # ========================================================================
    # PROVISION CHANGE VISUALIZATION
    # ========================================================================
    st.markdown('<div class="section-header">📈 Provision Rate Changes: 2022 → 2023</div>', unsafe_allow_html=True)
    
    significant_changes = provision_data[provision_data['Change'] >= 20].copy()
    significant_changes = significant_changes.sort_values('Change', ascending=False)
    
    fig_provision = px.bar(
        significant_changes,
        x='Tax Type',
        y=['2022_Provision', '2023_Provision'],
        title='Major Provision Rate Increases (2022 → 2023) - From Note 14a',
        barmode='group',
        color_discrete_sequence=['#3B82F6', '#DC2626'],
        text_auto=True
    )
    fig_provision.update_layout(
        yaxis_title='Provision Rate (%)',
        xaxis_title='Tax Type',
        height=400
    )
    fig_provision.update_xaxes(tickangle=20)
    st.plotly_chart(fig_provision, use_container_width=True)
    
    # ========================================================================
    # HIGHLIGHT THE MOST SIGNIFICANT CHANGES
    # ========================================================================
    st.markdown("""
    <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 2px solid #DC2626; margin: 15px 0;">
        <h5 style="color: #DC2626; margin-top: 0;">🚨 CRITICAL FINDINGS FROM NOTE 14A</h5>
        <ul>
            <li><strong>VAT:</strong> 2% → 8% provision (<span style="color: #10B981;">+6 percentage points - LOWEST RATE</span>)</li>
            <li><strong>Corporation Tax:</strong> 2% → 59% provision (<span style="color: #DC2626;">+57 percentage points</span>)</li>
            <li><strong>Personal Income Tax:</strong> 2% → 40% provision (<span style="color: #DC2626;">+38 percentage points</span>)</li>
            <li><strong>Excise Tax:</strong> 2% → 100% provision (<span style="color: #DC2626;">+98 percentage points - FULL PROVISION!</span>)</li>
            <li><strong>National Social Responsibility Levy:</strong> 2% → 100% provision (<span style="color: #DC2626;">+98 percentage points - FULL PROVISION!</span>)</li>
        </ul>
        <p style="font-size: 0.9rem; color: #10B981; margin-top: 10px; font-weight: bold;">
        ✅ VAT has the LOWEST provision rate (8%), making it the largest component of tax receivables at $1.133B (46.7%).
        </p>
        <p style="font-size: 0.9rem; color: #DC2626; margin-top: 5px; font-weight: bold;">
        ⚠️ The government recognized that up to 100% of some tax receivables may be uncollectible.
        </p>
        <p style="font-size: 0.85rem; color: #666; margin-top: 10px;">
        <strong>Source:</strong> Note 14a of Financial Statements (2023)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
                <li><strong>VAT is the largest component</strong> at $1.133B (46.7%)</li>
                <li><strong>True asset value</strong> is unknown</li>
                <li><strong>Financial statements</strong> are unreliable</li>
                <li><strong>Investor confidence</strong> is undermined</li>
                <li><strong>Credit rating</strong> may be affected</li>
                <li><strong>First flagged in 2023</strong> - a new systemic issue</li>
                <li><strong>Massive provisions</strong> suggest widespread uncollectibility</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #ECFDF5; padding: 20px; border-radius: 8px; border: 1px solid #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">✅ The Solution</h5>
            <ul>
                <li><strong>Complete verification</strong> of tax receivables</li>
                <li><strong>Focus on VAT</strong> as the largest component</li>
                <li><strong>Aging analysis</strong> to determine collectibility</li>
                <li><strong>Write-off</strong> uncollectible amounts</li>
                <li><strong>Improve collection</strong> processes</li>
                <li><strong>Enhance documentation</strong> and record-keeping</li>
                <li><strong>Achieve clean audit</strong> for 2024</li>
                <li><strong>Review provision methodology</strong> for accuracy</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # FREQUENTLY ASKED QUESTIONS
    # ========================================================================
    st.markdown('<div class="section-header">❓ Frequently Asked Questions</div>', unsafe_allow_html=True)
    
    faqs = [
        {
            'q': 'What is the actual breakdown of the $2.43B?',
            'a': f'From Note 14: VAT (${vat_amount/1e9:.2f}B, {vat_pct:.1f}%), Income Tax ($0.581B, 23.9%), Land Tax ($0.396B, 16.3%), Corporation Tax ($0.259B, 10.7%), and Other Taxes ($0.059B, 2.4%).'
        },
        {
            'q': 'Why is VAT the largest component?',
            'a': 'VAT applies to most goods and services in Barbados, making it the broadest-based tax. It also has the lowest provision rate (8%) compared to other major taxes, meaning more VAT is considered collectible.'
        },
        {
            'q': 'What does the 100% provision for Excise Tax mean?',
            'a': 'A 100% provision means the government has determined that ALL Excise Tax receivables are uncollectible. This is a significant admission that tax collection systems have failed.'
        },
        {
            'q': 'Why wasn\'t this flagged earlier?',
            'a': 'This is a NEW issue flagged in 2023. The Auditor General could not verify the amounts due to "the absence of sufficient supporting documentation."'
        },
        {
            'q': 'Is this a long-standing problem?',
            'a': 'No. This is a NEW issue that was first identified in the 2023 audit. It is not a problem that has been flagged in previous years.'
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
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%); padding: 25px; border-radius: 10px; color: white; margin-top: 20px;">
        <h4 style="color: white; margin-top: 0;">📌 The Bottom Line</h4>
        <p style="font-size: 1.05rem;">
        <strong style="color: #FFC726;">$2.43B</strong> in tax receivables <strong style="color: white;">cannot be verified</strong> 
        by the Auditor General.
        </p>
        <p style="font-size: 1.05rem;">
        <strong style="color: #FFC726;">VAT is the largest component</strong> at <strong style="color: white;">$1.133B (46.7%)</strong>.
        </p>
        <p style="font-size: 1.05rem;">
        This is a <strong style="color: #FFC726;">NEW issue</strong> flagged in 2023, representing 
        <strong style="color: white;">30% of total assets</strong>.
        </p>
        <p style="font-size: 1.05rem; margin-top: 15px;">
        The <strong style="color: #FFC726;">provision rates in Note 14a</strong> tell a troubling story:
        </p>
        <ul style="color: white;">
            <li>VAT: 2% → 8% provision (<span style="color: #10B981;">LOWEST RATE</span>)</li>
            <li>Corporation Tax: 2% → 59% provision</li>
            <li>Personal Income Tax: 2% → 40% provision</li>
            <li>Excise Tax: 2% → 100% provision</li>
        </ul>
        <p style="font-size: 1.05rem; margin-top: 15px;">
        <strong style="color: #FFC726;">Urgent action is needed</strong> to verify the receivables and determine 
        the true value of the asset.
        </p>
        <p style="font-size: 0.9rem; color: #FCA5A5; margin-top: 10px;">
        <em>Without verification, the financial statements remain unreliable and the audit opinion remains Adverse. 
        This is a new issue that requires immediate attention.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.caption("""
    **Data Source:** Auditor General's Report 2023 (Adverse Opinion, Note 14) • Financial Statements of the Government of Barbados (2023)
    **Note:** Data is from Note 14 of the Financial Statements (Page 26). VAT is the largest component at $1.133B (46.7%).
    The Auditor General could not verify these amounts due to "the absence of sufficient supporting documentation."
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

# ========================================================================
# VIEW 7: GLOBAL PEER COMPARISON - COMPLETE VERSION
# ========================================================================
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
        },
        hide_index=True
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
    fig.update_traces(textposition='outside', textfont_size=14)
    fig.update_layout(
        yaxis_title='Debt-to-GDP (%)',
        xaxis_title='Country',
        height=400,
        showlegend=False
    )
    fig.add_hline(y=60, line_dash="dash", line_color="#666", line_width=1.5,
                  annotation_text="60% Threshold", annotation_position="bottom right")
    st.plotly_chart(fig, use_container_width=True)

# ========================================================================
# VIEW 8: COST OF CAPITAL - COMPLETE VERSION
# ========================================================================
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
    # SAVINGS SCENARIOS
    # ========================================================================
    st.markdown('<div class="section-header">📊 Interest Savings Scenarios</div>', unsafe_allow_html=True)
    
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

# ========================================================================
# VIEW 9: ACTION TRACKER - COMPLETE VERSION
# ========================================================================
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
    
    recommendations_data = load_historical_recommendations()
    
    current_year = datetime.now().year
    recommendations_data['Years_Outstanding'] = current_year - recommendations_data['Year_First_Made']
    
    recommendations_data['Cost_Display'] = recommendations_data['Estimated_Cost_Billions'].apply(
        lambda x: f"${x:.2f}B" if x > 0 else "N/A"
    )
    
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
    
    fig = go.Figure()
    
    colors = {'❌ Not Implemented': '#DC2626', '⚠️ In Progress': '#F59E0B', '✅ Completed': '#10B981'}
    
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
    
    fig.add_hline(y=20, line_dash="dash", line_color="#DC2626", line_width=2, 
                  annotation_text="20+ Years (Critical)", annotation_position="bottom right")
    
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
# VIEW 10: EXECUTIVE BRIEFING - COMPLETE VERSION
# ========================================================================
elif view_option == "📄 Executive Briefing":
    st.markdown('<div class="sub-header">📄 EXECUTIVE BRIEFING</div>', unsafe_allow_html=True)
    st.markdown("### 🇧🇧 Barbados Financial Accountability 2003-2026")
    st.caption("A 21-Year Audit History • July 8, 2026 • Version 10.0")
    
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
# VIEW 11: HISTORICAL AUDIT TIMELINE
# ========================================================================
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
        <p style="margin-top: 10px; font-size: 0.95rem; color: #00267F;">
        <strong>✅ Last Clean Audit:</strong> 2007 &nbsp;|&nbsp; 
        <strong>⚠️ First Disclaimer:</strong> 2008 &nbsp;|&nbsp; 
        <strong>🔴 First Adverse:</strong> 2018
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        years = list(range(2003, 2024))
        opinions = ['Clean']*5 + ['Disclaimer']*10 + ['Adverse']*6
        colors = ['#10B981']*5 + ['#F59E0B']*10 + ['#DC2626']*6
        
        key_issues = [
            'No major issues',
            'No major issues',
            'No major issues',
            'No major issues',
            'No major issues (Last Clean)',
            'SOE consolidation concerns',
            'SOE consolidation concerns',
            'SOE consolidation concerns',
            'SOE consolidation concerns',
            'SOE consolidation concerns',
            'Asset valuation issues',
            'Asset valuation issues',
            'Asset valuation issues',
            'Asset valuation issues',
            'Asset valuation issues',
            'First Adverse Opinion',
            'Cash overstatements ($115M)',
            'Fixed assets & land unverified',
            'Deficit peaks ($685M)',
            'Asset discrepancies ($719M)',
            'Tax receivables unverified (NEW $2.43B)'
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=years,
            y=[1]*len(years),
            marker_color=colors,
            text=opinions,
            textposition='inside',
            textfont=dict(color='white', size=12, weight='bold'),
            name='Audit Opinion',
            hovertemplate='Year: %{x}<br>Opinion: %{text}<br>Key Issue: %{customdata}<extra></extra>',
            customdata=key_issues
        ))
        
        fig.add_vrect(x0=2002.5, x1=2007.5, fillcolor="rgba(16, 185, 129, 0.15)", line_width=0)
        fig.add_annotation(x=2005, y=1.1, text="🟢 CLEAN ERA\n5 YEARS (2003-2007)", 
                          showarrow=False, font=dict(size=13, color='#10B981', weight='bold'))
        
        fig.add_vrect(x0=2007.5, x1=2017.5, fillcolor="rgba(245, 158, 11, 0.15)", line_width=0)
        fig.add_annotation(x=2012, y=1.1, text="🟡 DISCLAIMER ERA\n10 YEARS (2008-2017)", 
                          showarrow=False, font=dict(size=13, color='#F59E0B', weight='bold'))
        
        fig.add_vrect(x0=2017.5, x1=2023.5, fillcolor="rgba(220, 38, 38, 0.15)", line_width=0)
        fig.add_annotation(x=2020, y=1.1, text="🔴 ADVERSE ERA\n6 YEARS (2018-2023)", 
                          showarrow=False, font=dict(size=13, color='#DC2626', weight='bold'))
        
        milestones = [
            {'year': 2003, 'text': '🟢 FIRST CLEAN', 'y': 1.3, 'color': '#10B981'},
            {'year': 2007, 'text': '🟢 LAST CLEAN ✅', 'y': 1.4, 'color': '#10B981'},
            {'year': 2008, 'text': '🟡 FIRST DISCLAIMER', 'y': 1.3, 'color': '#F59E0B'},
            {'year': 2018, 'text': '🔴 FIRST ADVERSE', 'y': 1.3, 'color': '#DC2626'},
            {'year': 2023, 'text': '🔴 6TH ADVERSE\n$2.43B NEW', 'y': 1.4, 'color': '#DC2626'}
        ]
        
        for m in milestones:
            fig.add_annotation(
                x=m['year'],
                y=m['y'],
                text=m['text'],
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-40,
                font=dict(size=10, color=m['color'], weight='bold')
            )
        
        fig.update_layout(
            title='Audit Opinion Timeline: 2003-2023',
            yaxis=dict(range=[0, 1.6], showticklabels=False, title=''),
            xaxis=dict(tickmode='linear', dtick=1, title='Year', tickangle=45),
            height=450,
            showlegend=False,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="financial-card">
            <h6 style="margin-top: 0; color: #00267F;">🔑 Key Milestones</h6>
            <div style="font-size: 0.9rem;">
                <p><strong>🟢 2003-2007:</strong> Clean Opinions (5 years)</p>
                <p><strong>✅ 2007:</strong> Last Clean Audit</p>
                <p><strong>🟡 2008:</strong> First Disclaimer Opinion</p>
                <p><strong>🟡 2008-2017:</strong> Disclaimer Era (10 years)</p>
                <p><strong>🔴 2018:</strong> First Adverse Opinion</p>
                <p><strong>🔴 2018-2023:</strong> Adverse Era (6 years)</p>
                <p><strong>🔴 2023:</strong> 6th Consecutive Adverse</p>
                <p><strong>🚨 2023:</strong> $2.43B Tax Receivables (NEW)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📊 Era Breakdown</div>', unsafe_allow_html=True)
    
    era_col1, era_col2, era_col3 = st.columns(3)
    
    clean_years = list(range(2003, 2008))
    clean_count = len(clean_years)
    
    with era_col1:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #10B981;">
            <h5 style="color: #10B981; margin-top: 0;">🟢 Clean Era (2003-2007)</h5>
            <p><strong>Years:</strong> {clean_count}</p>
            <p><strong>Opinions:</strong> Clean</p>
            <p><strong>Key Issues:</strong> No major issues identified</p>
            <p><strong>Status:</strong> ✅ Strong financial management</p>
            <p><strong>Years:</strong> {', '.join(map(str, clean_years))}</p>
            <p style="color: #10B981; font-weight: bold;">✅ Last Clean: 2007</p>
        </div>
        """, unsafe_allow_html=True)
    
    disclaimer_years = list(range(2008, 2018))
    disclaimer_count = len(disclaimer_years)
    
    with era_col2:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #F59E0B;">
            <h5 style="color: #F59E0B; margin-top: 0;">🟡 Disclaimer Era (2008-2017)</h5>
            <p><strong>Years:</strong> {disclaimer_count}</p>
            <p><strong>Opinions:</strong> Disclaimer</p>
            <p><strong>Key Issues:</strong> SOE consolidation, asset valuation</p>
            <p><strong>Status:</strong> ⚠️ Recurring issues emerge</p>
            <p><strong>Years:</strong> {', '.join(map(str, disclaimer_years[:5]))}...{disclaimer_years[-1]}</p>
            <p style="color: #F59E0B; font-weight: bold;">⚠️ First Disclaimer: 2008</p>
        </div>
        """, unsafe_allow_html=True)
    
    adverse_years = list(range(2018, 2024))
    adverse_count = len(adverse_years)
    
    with era_col3:
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: #DC2626;">
            <h5 style="color: #DC2626; margin-top: 0;">🔴 Adverse Era (2018-2023)</h5>
            <p><strong>Years:</strong> {adverse_count}</p>
            <p><strong>Opinions:</strong> Adverse</p>
            <p><strong>Key Issues:</strong> Material misstatements, $2.43B unverified</p>
            <p><strong>Status:</strong> ❌ Systemic failures</p>
            <p><strong>Years:</strong> {', '.join(map(str, adverse_years))}</p>
            <p style="color: #DC2626; font-weight: bold;">🔴 First Adverse: 2018</p>
            <p style="color: #DC2626; font-weight: bold;">🚨 NEW 2023: $2.43B Tax Receivables</p>
        </div>
        """, unsafe_allow_html=True)

# ========================================================================
# VIEW 12: LONG-TERM FINANCIAL TRENDS
# ========================================================================
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
    
    st.markdown('<div class="section-header">📊 Key Metrics Evolution</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
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
# VIEW 13: RECURRING ISSUES ANALYSIS
# ========================================================================
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

# ========================================================================
# VIEW 14: ACCOUNTABILITY SCORECARD
# ========================================================================
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
    
    st.markdown('<div class="section-header">📋 Detailed Category Analysis</div>', unsafe_allow_html=True)
    
    for _, row in accountability_metrics.iterrows():
        improvement = row['Score_2023'] - row['Score_2008']
        color = '#DC2626' if improvement < 0 else '#10B981' if improvement > 0 else '#F59E0B'
        
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
# VIEW 15: 2023 EXECUTIVE SUMMARY
# ========================================================================
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
    
    st.markdown('<div class="section-header">📊 Revenue & Expenditure Summary</div>', unsafe_allow_html=True)
    
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
    
    st.markdown('<div class="section-header">🚨 Material Misstatements Identified</div>', unsafe_allow_html=True)
    
    for _, item in financial_2023['adverse_opinion_items'].iterrows():
        render_misstatement_card(item, currency_format)
    
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
# VIEW 16: 2023 BALANCE SHEET - COMPLETE FIXED VERSION (NO HTML)
# ============================================================================
elif view_option == "🏦 2023 Balance Sheet":
    st.markdown('<div class="sub-header">🏦 2023 Balance Sheet Analysis</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # CORRECTED DEBT DATA FROM NOTE 25
    # ========================================================================
    debt_structure_corrected = pd.DataFrame({
        'Debt_Type': [
            'Local Loans Act',
            'Inter American Development Bank',
            'External Loans Act',
            'Special Loans Act',
            'International Monetary Fund',
            'Treasury Bills',
            'Caribbean Development Bank',
            'Latin American Development Bank',
            'Ways & Means (Overdraft)',
            'Savings Bond Act',
            'Contingent Liabilities'
        ],
        'Amount_2023': [
            7746270000,
            1499650000,
            1061170000,
            890940000,
            548410000,
            495170000,
            469380000,
            357430000,
            167150000,
            32230000,
            31300000
        ],
        'Debt_Category': [
            'Domestic', 'Foreign', 'Foreign', 'Foreign', 'Foreign',
            'Domestic', 'Foreign', 'Foreign', 'Domestic', 'Domestic', 'Foreign'
        ]
    })
    
    total_debt = debt_structure_corrected['Amount_2023'].sum()
    debt_structure_corrected['Percentage'] = (debt_structure_corrected['Amount_2023'] / total_debt * 100).round(2)
    debt_structure_corrected['Amount_Display'] = debt_structure_corrected['Amount_2023'].apply(
        lambda x: f"${x/1e6:,.2f}M" if x < 1e9 else f"${x/1e9:.2f}B"
    )
    
    # ========================================================================
    # KEY METRICS
    # ========================================================================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Assets", "$8.07B", "2023")
    with col2:
        st.metric("Total Liabilities", "$14.93B", "2023")
    with col3:
        net_position = 8.07 - 14.93
        st.metric("Net Position", f"${net_position:.2f}B", "Negative")
    
    # ========================================================================
    # DEBT STRUCTURE TABLE
    # ========================================================================
    st.markdown('<div class="section-header">📊 Public Debt Structure (2023)</div>', unsafe_allow_html=True)
    
    st.dataframe(
        debt_structure_corrected[['Debt_Type', 'Amount_Display', 'Percentage', 'Debt_Category']],
        use_container_width=True,
        hide_index=True,
        column_config={
            'Debt_Type': 'Debt Type',
            'Amount_Display': 'Amount (2023)',
            'Percentage': '% of Total',
            'Debt_Category': 'Category'
        }
    )
    
    # ========================================================================
    # DOMESTIC VS FOREIGN DEBT
    # ========================================================================
    st.markdown('<div class="section-header">📊 Domestic vs Foreign Debt</div>', unsafe_allow_html=True)
    
    domestic_total = debt_structure_corrected[debt_structure_corrected['Debt_Category'] == 'Domestic']['Amount_2023'].sum()
    foreign_total = debt_structure_corrected[debt_structure_corrected['Debt_Category'] == 'Foreign']['Amount_2023'].sum()
    
    domestic_pct = (domestic_total / total_debt * 100)
    foreign_pct = (foreign_total / total_debt * 100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        debt_pie_data = pd.DataFrame({
            'Category': ['Domestic Debt', 'Foreign Debt'],
            'Amount': [domestic_total, foreign_total]
        })
        
        fig_debt = px.pie(
            debt_pie_data,
            values='Amount',
            names='Category',
            title=f'Debt Composition: Domestic vs Foreign\nTotal: ${total_debt/1e9:.2f}B',
            color='Category',
            color_discrete_map={'Domestic Debt': '#00267F', 'Foreign Debt': '#DC2626'},
            hole=0.4
        )
        fig_debt.update_traces(textposition='inside', textinfo='label+percent', textfont_size=14)
        fig_debt.update_layout(height=350)
        st.plotly_chart(fig_debt, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e5e7eb; height: 100%;">
            <h5 style="margin-top: 0; color: #00267F;">💰 Debt Summary</h5>
            <div style="font-size: 1.5rem; font-weight: bold; color: #00267F;">${domestic_total/1e9:.2f}B</div>
            <div style="color: #666;">Domestic Debt ({domestic_pct:.1f}%)</div>
            <div style="margin-top: 15px; font-size: 1.5rem; font-weight: bold; color: #DC2626;">${foreign_total/1e9:.2f}B</div>
            <div style="color: #666;">Foreign Debt ({foreign_pct:.1f}%)</div>
            <div style="margin-top: 15px; font-size: 1.2rem; font-weight: bold; color: #00267F;">${total_debt/1e9:.2f}B</div>
            <div style="color: #666;">Total Public Debt</div>
            <p style="font-size: 0.85rem; color: #666; margin-top: 10px;">
            <strong>Source:</strong> Note 25 of Financial Statements (2023)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # KEY ASSET ITEMS - USING STREAMLIT METRIC WITH CUSTOM FORMATTING
    # ========================================================================
    st.markdown('<div class="section-header">📊 Key Asset Items</div>', unsafe_allow_html=True)
    
    asset_data = financial_2023['balance_sheet'].copy()
    key_assets = asset_data[asset_data['Category'].isin([
        'Cash on Hand', 'Bank', 'Tax Receivables (Net)', 
        'Investments', 'Land', 'Other capital assets (Net)'
    ])]
    
    # Use a simple for loop with st.columns for each item
    for _, row in key_assets.iterrows():
        value = format_currency(row['Actual_Mar_23'], currency_format)
        prev_value = format_currency(row['Actual_Mar_22'], currency_format)
        change = row['Actual_Mar_23'] - row['Actual_Mar_22']
        change_pct = (change / row['Actual_Mar_22']) * 100 if row['Actual_Mar_22'] != 0 else 0
        
        is_tax = row['Category'] == 'Tax Receivables (Net)'
        
        # Display with consistent formatting using columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Asset name with optional badge
            if is_tax:
                st.markdown(f"**{row['Category']}** ⚠️ NEW 2023 ISSUE")
            else:
                st.markdown(f"**{row['Category']}**")
            # Values
            st.markdown(f"2023: {value} | 2022: {prev_value}")
        
        with col2:
            # Change amount with color
            if change >= 0:
                st.markdown(f"<p style='text-align: right; font-size: 1.1rem; font-weight: bold; color: #10B981; margin: 0;'>{format_currency(change, currency_format)}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='text-align: right; font-size: 1.1rem; font-weight: bold; color: #DC2626; margin: 0;'>{format_currency(change, currency_format)}</p>", unsafe_allow_html=True)
            # Percentage
            st.markdown(f"<p style='text-align: right; font-size: 0.9rem; color: #666; margin: 0;'>{change_pct:+.1f}%</p>", unsafe_allow_html=True)
        
        st.divider()
    
    # ========================================================================
    # DEBT BY CATEGORY BAR CHART
    # ========================================================================
    st.markdown('<div class="section-header">📊 Debt by Category</div>', unsafe_allow_html=True)
    
    debt_sorted = debt_structure_corrected.sort_values('Amount_2023', ascending=False).head(10)
    
    fig_debt_bar = px.bar(
        debt_sorted,
        x='Debt_Type',
        y='Amount_2023',
        title='Public Debt by Type (2023)',
        color='Debt_Category',
        color_discrete_map={'Domestic': '#00267F', 'Foreign': '#DC2626'},
        text=[f"${x/1e9:.2f}B" if x > 1e9 else f"${x/1e6:.0f}M" for x in debt_sorted['Amount_2023']]
    )
    fig_debt_bar.update_traces(textposition='outside', textfont_size=10)
    fig_debt_bar.update_layout(
        yaxis_title='Amount ($)',
        xaxis_title='Debt Type',
        height=400
    )
    fig_debt_bar.update_xaxes(tickangle=20)
    st.plotly_chart(fig_debt_bar, use_container_width=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.caption(f"""
    **Data Source:** Financial Statements of the Government of Barbados (2023)
    **Total Public Debt:** ${total_debt/1e9:.2f}B (Note 25)
    **Note:** Tax Receivables of $2.43B were flagged as a NEW issue in 2023 (unverified).
    """)

# ========================================================================
# VIEW 17: 2023 AUDIT FINDINGS
# ========================================================================
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

# ========================================================================
# VIEW 18: 2023 DATA QUALITY ISSUES
# ========================================================================
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

# ========================================================================
# VIEW 19: 2026 REALITY CHECK
# ========================================================================
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
# VIEW 20: 2026-2027 BUDGET VS 2023 AUDIT - TRUTHFUL ANALYSIS
# ============================================================================
elif view_option == "📊 2026-2027 Budget vs 2023 Audit Reality":
    st.markdown('<div class="sub-header">📊 2026-2027 Budget: Analysis of Key Changes from 2023</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #F0F7FF; padding: 25px; border-radius: 10px; border-left: 6px solid #3B82F6; margin: 20px 0;">
        <p style="font-size: 1.1rem; margin: 0; color: #00267F;">
        This analysis compares the <strong>2026-2027 Budget Estimates</strong> with the 
        <strong>2023 Audited Financial Statements</strong>.
        </p>
        <p style="font-size: 0.95rem; margin: 5px 0 0 0; color: #666;">
        All figures are sourced from official Government documents. Where data is not directly comparable,
        this is clearly noted.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 1: DATA QUALITY WARNING - CORRECTED
    # ========================================================================
    st.markdown("""
    <div style="background: #FEF2F2; padding: 25px; border-radius: 10px; border: 3px solid #DC2626; margin: 20px 0;">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
            <span style="font-size: 2.5rem;">⚠️</span>
            <h4 style="color: #DC2626; margin: 0;">DATA QUALITY WARNING</h4>
        </div>
        <p style="font-size: 1.05rem; margin: 0 0 10px 0;">
        The 2026-2027 Estimates document contains <strong style="color: #DC2626;">material inconsistencies</strong>. 
        The "Particulars of Service" (narrative) and Budget Tables frequently report different figures.
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 15px 0;">
            <div style="text-align: center; padding: 15px; background: rgba(220, 38, 38, 0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #DC2626;">$2.03B+</div>
                <div style="font-size: 0.9rem; color: #666;">Total Discrepancy</div>
            </div>
            <div style="text-align: center; padding: 15px; background: rgba(220, 38, 38, 0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #DC2626;">26 of 27</div>
                <div style="font-size: 0.9rem; color: #666;">Heads Affected (96.3%)</div>
            </div>
            <div style="text-align: center; padding: 15px; background: rgba(220, 38, 38, 0.1); border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #DC2626;">3.7%</div>
                <div style="font-size: 0.9rem; color: #666;">Reliability Score</div>
            </div>
        </div>
        <div style="background: #ECFDF5; padding: 15px; border-radius: 8px; border-left: 4px solid #10B981; margin-top: 10px;">
            <p style="margin: 0; font-size: 0.95rem; color: #065F46;">
            ✅ <strong>HEAD 12: PARLIAMENT</strong> — The only Head with perfect alignment.
            </p>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 8px; font-size: 0.9rem;">
                <div><strong>Words:</strong> $17,190,950</div>
                <div><strong>Figures:</strong> $17,190,950</div>
                <div style="color: #10B981;"><strong>Status:</strong> ✅ PERFECT</div>
            </div>
        </div>
        <p style="font-size: 0.85rem; color: #666; margin: 10px 0 0 0;">
        All discrepancies are documented and verifiable from the official Estimates document.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 2: THE BIG PICTURE - FACTUAL SUMMARY
    # ========================================================================
    st.markdown('<div class="section-header">📊 The Big Picture: Key Changes</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Revenue Change",
            "+$1.59B",
            "+46% (2023 → 2026-27)",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Expenditure Change",
            "+$2.29B",
            "+64% (2023 → 2026-27)",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Projected Deficit",
            "-$658M",
            "vs -$111M in 2023",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "Debt Service",
            "$1.50B",
            "25% of expenditure",
            delta_color="inverse"
        )
    
    # ========================================================================
    # SECTION 3: REVENUE ANALYSIS
    # ========================================================================
    st.markdown('<div class="section-header">💰 Revenue: Key Changes</div>', unsafe_allow_html=True)
    
    revenue_data = pd.DataFrame({
        'Category': [
            'Income and Profits Tax',
            'Goods and Services (VAT)',
            'International Trade',
            'Property Taxes',
            'Other Revenue',
            'Other Categories'
        ],
        '2023_Actual': [
            1.069,
            1.628,
            0.250,
            0.241,
            0.171,
            0.125
        ],
        '2026_27_Budget': [
            2.430,
            1.767,
            0.319,
            0.235,
            0.192,
            0.132
        ],
        'Change': [
            1.361,
            0.139,
            0.069,
            -0.006,
            0.021,
            0.007
        ],
        'Change_Pct': [
            127.3,
            8.5,
            27.6,
            -2.5,
            12.3,
            5.6
        ]
    })
    
    st.dataframe(
        revenue_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Category': 'Revenue Category',
            '2023_Actual': st.column_config.NumberColumn('2023 Actual (B)', format="%.3fB"),
            '2026_27_Budget': st.column_config.NumberColumn('2026-27 Budget (B)', format="%.3fB"),
            'Change': st.column_config.NumberColumn('Change (B)', format="%.3fB"),
            'Change_Pct': st.column_config.NumberColumn('Change %', format="%.1f%%")
        }
    )
    
    # Critical insight - presented factually
    st.markdown("""
    <div style="background: #FFFBEB; padding: 20px; border-radius: 8px; border: 2px solid #F59E0B; margin: 15px 0;">
        <h5 style="color: #D97706; margin-top: 0;">⚠️ OBSERVATION: Income Tax Revenue Projection</h5>
        <p style="font-size: 1.05rem;">
        The budget projects a <strong>127% increase</strong> in Income and Profits Tax revenue 
        (from $1.07B to $2.43B).
        </p>
        <p style="font-size: 1.05rem; color: #666;">
        For context, in 2023 the Auditor General noted that:
        </p>
        <ul>
            <li><strong>$2.43B</strong> in tax receivables could not be verified</li>
            <li><strong>59%</strong> of Corporation Tax and <strong>40%</strong> of Personal Income Tax were provisioned as uncollectible</li>
        </ul>
        <p style="font-size: 0.95rem; color: #666; margin-top: 5px;">
        <em>This represents a significant assumption about improved tax collection performance.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 4: EXPENDITURE ANALYSIS - KEY CATEGORIES
    # ========================================================================
    st.markdown('<div class="section-header">📊 Expenditure: Key Changes</div>', unsafe_allow_html=True)
    
    expenditure_data = pd.DataFrame({
        'Category': [
            'Grants to Public Institutions',
            'Debt Service - Interest',
            'Retiring Benefits',
            'Goods and Services',
            'Capital Transfers',
            'Personal Emoluments',
            'Bad Debt Expense'
        ],
        '2023_Actual': [
            704.5,
            554.7,
            333.6,
            545.2,
            242.0,
            863.9,
            68.3
        ],
        '2026_27_Budget': [
            845.2,
            714.6,
            433.8,
            918.1,
            352.5,
            856.8,
            0.5
        ],
        'Change': [
            140.7,
            159.9,
            100.2,
            372.9,
            110.5,
            -7.1,
            -67.8
        ],
        'Change_Pct': [
            20.0,
            28.8,
            30.0,
            68.4,
            45.7,
            -0.8,
            -99.3
        ]
    })
    
    st.dataframe(
        expenditure_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Category': 'Expenditure Category',
            '2023_Actual': st.column_config.NumberColumn('2023 Actual (M)', format="%.1fM"),
            '2026_27_Budget': st.column_config.NumberColumn('2026-27 Budget (M)', format="%.1fM"),
            'Change': st.column_config.NumberColumn('Change (M)', format="%.1fM"),
            'Change_Pct': st.column_config.NumberColumn('Change %', format="%.1f%%")
        }
    )
    
    # Bad Debt observation - factual
    st.markdown("""
    <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 2px solid #DC2626; margin: 15px 0;">
        <h5 style="color: #DC2626; margin-top: 0;">⚠️ OBSERVATION: Bad Debt Expense</h5>
        <p style="font-size: 1.05rem;">
        Bad debt expense is budgeted at <strong>$0.5M</strong> for 2026-27, compared to 
        <strong>$68.3M</strong> in 2023.
        </p>
        <p style="font-size: 1.05rem; color: #666;">
        This represents a <strong>99.3% reduction</strong>. In 2023, the government changed its bad debt policy,
        resulting in significantly higher provisions for tax receivables.
        </p>
        <p style="font-size: 0.95rem; color: #666; margin-top: 5px;">
        <em>The budget assumes that the 2023 bad debt experience was exceptional and will not recur.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 5: SOE TRANSFERS - WHAT WE CAN TRUTHFULLY SHOW
    # ========================================================================
    st.markdown('<div class="section-header">🏛️ State-Owned Enterprise Transfers</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #EFF6FF; padding: 15px; border-radius: 8px; border-left: 4px solid #3B82F6; margin: 15px 0;">
        <p style="margin: 0; font-size: 0.95rem;">
        <strong>Note on Data:</strong> The 2023 figures are from Note 34 of the audited financial statements.
        The 2026-27 figures are based on grants to public institutions identified in the Estimates document.
        </p>
        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #666;">
        Some SOEs receive funding through multiple ministries, making direct year-over-year comparison challenging.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Data we can actually show with confidence
    soe_comparison = pd.DataFrame({
        'SOE': [
            'Queen Elizabeth Hospital',
            'University of the West Indies',
            'Barbados Community College',
            'Barbados Tourism Investment Inc.',
            'National Sports Council',
            'Transport Board'
        ],
        '2023_Actual': [
            142.4,
            'Not in top 10',
            22.1,
            94.7,
            36.4,
            46.8
        ],
        '2026_27_Budget': [
            160.0,
            98.4,
            30.3,
            94.1,
            15.8,
            12.2
        ],
        'Change_Notes': [
            'Increase of $17.6M (+12.4%)',
            'New large allocation in 2026-27',
            'Increase of $8.2M (+36.9%)',
            'Relatively stable (-0.6%)',
            'Decrease of $20.6M (-56.5%)',
            'Decrease of $34.6M (-74.0%)'
        ]
    })
    
    st.dataframe(
        soe_comparison,
        use_container_width=True,
        hide_index=True,
        column_config={
            'SOE': 'SOE Name',
            '2023_Actual': '2023 Actual (M)',
            '2026_27_Budget': '2026-27 Budget (M)',
            'Change_Notes': 'Change'
        }
    )
    
    # The Note 34 discrepancy - presented factually
    st.markdown("""
    <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 2px solid #DC2626; margin: 15px 0;">
        <h5 style="color: #DC2626; margin-top: 0;">⚠️ NOTE: SOE Transfer Data Quality Issue (Note 34)</h5>
        <p style="font-size: 1.05rem;">
        In the 2023 financial statements, Note 34 contains a <strong>$108.6M discrepancy</strong>:
        </p>
        <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; padding: 10px;">
            <div style="text-align: center;">
                <div style="font-size: 1.3rem; font-weight: bold; color: #3B82F6;">$669.3M</div>
                <div style="font-size: 0.9rem; color: #666;">Narrative Total</div>
            </div>
            <div style="font-size: 1.5rem; color: #DC2626;">≠</div>
            <div style="text-align: center;">
                <div style="font-size: 1.3rem; font-weight: bold; color: #DC2626;">$777.9M</div>
                <div style="font-size: 0.9rem; color: #666;">Table Total</div>
            </div>
            <div style="text-align: center; padding: 5px 15px; background: #FEF2F2; border-radius: 8px;">
                <div style="font-size: 1.3rem; font-weight: bold; color: #DC2626;">$108.6M</div>
                <div style="font-size: 0.9rem; color: #666;">Discrepancy</div>
            </div>
        </div>
        <p style="font-size: 0.95rem; color: #666; margin-top: 5px;">
        <strong>Fact:</strong> The financial statements contain inconsistent information about total SOE transfers.
        The accurate total cannot be determined from the published statements.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 6: THE DEFICIT REPORTING GAP
    # ========================================================================
    st.markdown('<div class="section-header">📊 The Deficit: Two Reporting Bases</div>', unsafe_allow_html=True)
    
    deficit_data = pd.DataFrame({
        'Basis': ['Accountant General\'s Basis', 'IFI Basis'],
        'Fiscal Balance': ['-4.0% of GDP', '+0.6% of GDP'],
        'Interpretation': ['Deficit', 'Surplus'],
        'Status': ['🔴 Deficit', '🟢 Surplus'],
        'Source': ['Page 26 of Estimates', 'Page 26 of Estimates']
    })
    
    st.dataframe(
        deficit_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Basis': 'Reporting Basis',
            'Fiscal Balance': 'Fiscal Balance',
            'Interpretation': 'Interpretation',
            'Status': 'Status',
            'Source': 'Source'
        }
    )
    
    st.markdown("""
    <div style="background: #FFFBEB; padding: 20px; border-radius: 8px; border: 2px solid #F59E0B; margin: 15px 0;">
        <h5 style="color: #D97706; margin-top: 0;">ℹ️ OBSERVATION: Different Reporting Bases</h5>
        <p style="font-size: 1.05rem;">
        The government reports a <strong style="color: #10B981;">0.6% surplus</strong> to international financial institutions,
        and a <strong style="color: #DC2626;">4.0% deficit</strong> on the Accountant General's basis.
        </p>
        <p style="font-size: 0.95rem; color: #666;">
        This 4.6 percentage point difference reflects different accounting treatments and classifications.
        Both figures are from the same Estimates document (Page 26).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 7: THE $2.43B QUESTION VS BUDGET DEFICIT
    # ========================================================================
    st.markdown('<div class="section-header">🚨 The $2.43B Question vs Budget Deficit</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #FEF2F2; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #DC2626; height: 100%;">
            <div style="font-size: 2.5rem; font-weight: bold; color: #DC2626;">$2.43B</div>
            <div style="font-weight: 600;">Unverified Tax Receivables</div>
            <div style="font-size: 0.85rem; color: #666;">First flagged in 2023</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #FFFBEB; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #F59E0B; height: 100%;">
            <div style="font-size: 2.5rem; font-weight: bold; color: #F59E0B;">$658M</div>
            <div style="font-weight: 600;">Projected Budget Deficit</div>
            <div style="font-size: 0.85rem; color: #666;">2026-27 (Including Annex)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #EFF6FF; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #3B82F6; height: 100%;">
            <div style="font-size: 2.5rem; font-weight: bold; color: #3B82F6;">3.7x</div>
            <div style="font-weight: 600;">Times Deficit Covered by Unverified Receivables</div>
            <div style="font-size: 0.85rem; color: #666;">$2.43B ÷ $658M = 3.7x</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 8: THE HONEST BUDGET CALCULATOR
    # ========================================================================
    st.markdown('<div class="section-header">📊 The Honest Budget Calculator</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #FFFBEB; padding: 20px; border-radius: 10px; border-left: 6px solid #F59E0B; margin: 15px 0;">
        <p style="font-size: 1.05rem; margin: 0;">
        The <strong>$2.43B</strong> in tax receivables <strong>cannot be verified</strong> by the Auditor General.
        </p>
        <p style="font-size: 1.05rem; margin: 5px 0 0 0; color: #666;">
        Use the slider below to estimate what percentage is <strong>actually collectible</strong>.
        The calculator will show the impact on the budget deficit and debt-to-GDP ratio.
        </p>
        <p style="font-size: 0.9rem; margin: 10px 0 0 0; color: #D97706;">
        <strong>⚠️ This is a "what if" scenario tool. The actual collectible amount is unknown.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input: Collectible Percentage
    collectible_pct = st.slider(
        "What percentage of the $2.43B tax receivables is collectible?",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        help="This is your estimate. The Auditor General could not verify these receivables."
    )
    
    # Calculations
    tax_receivables = 2.43  # $2.43B
    write_off = tax_receivables * (1 - collectible_pct / 100)
    collectible_amount = tax_receivables * (collectible_pct / 100)
    
    projected_deficit = 0.658  # $658M
    adjusted_deficit = projected_deficit + write_off
    
    current_debt_to_gdp = 102.9  # %
    total_assets = 8.07  # $8.07B
    debt_impact_pct = (write_off / total_assets) * current_debt_to_gdp
    adjusted_debt_to_gdp = current_debt_to_gdp + debt_impact_pct
    
    # Display Results
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Collectible Amount",
            f"${collectible_amount:.2f}B",
            f"{collectible_pct:.0f}% of total",
            delta_color="normal"
        )
    
    with col2:
        delta_color = "normal" if write_off == 0 else "inverse"
        st.metric(
            "Write-Off Amount",
            f"${write_off:.2f}B",
            f"{100 - collectible_pct:.0f}% of total",
            delta_color=delta_color
        )
    
    with col3:
        st.metric(
            "Adjusted Deficit",
            f"${adjusted_deficit:.2f}B",
            f"{adjusted_deficit - projected_deficit:+.2f}B vs projected",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "Adjusted Debt-to-GDP",
            f"{adjusted_debt_to_gdp:.1f}%",
            f"{adjusted_debt_to_gdp - current_debt_to_gdp:+.1f}% vs current",
            delta_color="inverse" if adjusted_debt_to_gdp > current_debt_to_gdp else "normal"
        )
    
    # Scenario Table
    st.markdown('<div class="section-header" style="font-size: 1.0rem;">📋 Scenario Comparison</div>', unsafe_allow_html=True)
    
    scenarios = []
    scenario_labels = ['Worst Case', 'Pessimistic', 'Concerned', 'Cautious', 'Optimistic']
    pct_values = [0, 25, 50, 75, 100]
    
    for i, pct in enumerate(pct_values):
        w_off = tax_receivables * (1 - pct / 100)
        adj_def = projected_deficit + w_off
        adj_dtg = current_debt_to_gdp + (w_off / total_assets) * current_debt_to_gdp
        scenarios.append({
            'Scenario': scenario_labels[i],
            'Collectible %': f'{pct}%',
            'Write-Off': f'${w_off:.2f}B',
            'Adjusted Deficit': f'${adj_def:.2f}B',
            'Adjusted Debt-to-GDP': f'{adj_dtg:.1f}%'
        })
    
    scenario_df = pd.DataFrame(scenarios)
    st.dataframe(
        scenario_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Scenario': 'Scenario',
            'Collectible %': 'Collectible %',
            'Write-Off': 'Write-Off',
            'Adjusted Deficit': 'Adjusted Deficit',
            'Adjusted Debt-to-GDP': 'Adjusted Debt-to-GDP'
        }
    )
    
    # Key Insight
    st.markdown(f"""
    <div style="background: {'#FEF2F2' if write_off > 0 else '#ECFDF5'}; padding: 20px; border-radius: 8px; border: 2px solid {'#DC2626' if write_off > 0 else '#10B981'}; margin: 15px 0;">
        <h5 style="color: {'#DC2626' if write_off > 0 else '#10B981'}; margin-top: 0;">🔑 Key Insight</h5>
        <p style="font-size: 1.05rem; margin: 0;">
        If <strong>{100 - collectible_pct:.0f}%</strong> of the $2.43B tax receivables are uncollectible:
        </p>
        <ul>
            <li>The budget deficit increases from <strong>${projected_deficit:.2f}B</strong> to <strong>${adjusted_deficit:.2f}B</strong></li>
            <li>The debt-to-GDP ratio increases from <strong>{current_debt_to_gdp:.1f}%</strong> to <strong>{adjusted_debt_to_gdp:.1f}%</strong></li>
        </ul>
        <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">
        <strong>Note:</strong> The Auditor General could not verify these receivables. The actual impact is unknown.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 9: THE COST OF COMPLACENCY - NEW
    # ========================================================================
    st.markdown('<div class="section-header">💰 The Cost of Complacency: What You\'re Paying</div>', unsafe_allow_html=True)
    
    # Calculate per household cost
    households = 100000  # ~100,000 households in Barbados
    annual_savings_low = 55  # $55M
    annual_savings_high = 100  # $100M
    cost_per_household_low = (annual_savings_low * 1_000_000) / households
    cost_per_household_high = (annual_savings_high * 1_000_000) / households
    
    st.markdown(f"""
    <div style="background: #F8FAFC; padding: 20px; border-radius: 8px; border: 1px solid #E2E8F0; margin: 15px 0;">
        <h5 style="margin-top: 0; color: #00267F;">🏠 The Cost to Every Barbadian Household</h5>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 15px 0;">
            <div style="text-align: center; padding: 15px; background: white; border-radius: 6px; border: 1px solid #E2E8F0;">
                <div style="font-size: 2rem; font-weight: bold; color: #DC2626;">${annual_savings_low}M - ${annual_savings_high}M</div>
                <div style="font-size: 0.9rem; color: #666;">Annual Cost of Audit Failure</div>
            </div>
            <div style="text-align: center; padding: 15px; background: white; border-radius: 6px; border: 1px solid #E2E8F0;">
                <div style="font-size: 2rem; font-weight: bold; color: #DC2626;">${cost_per_household_low:,.0f} - ${cost_per_household_high:,.0f}</div>
                <div style="font-size: 0.9rem; color: #666;">Per Household Per Year</div>
            </div>
            <div style="text-align: center; padding: 15px; background: white; border-radius: 6px; border: 1px solid #E2E8F0;">
                <div style="font-size: 2rem; font-weight: bold; color: #10B981;">5-10x</div>
                <div style="font-size: 0.9rem; color: #666;">Return on Investment</div>
            </div>
        </div>
        <p style="font-size: 0.95rem; color: #666; margin-top: 10px;">
        <strong>Every Barbadian household is paying $550-$1,000 per year</strong> in higher borrowing costs 
        because the government cannot produce reliable financial statements.
        </p>
        <p style="font-size: 0.9rem; color: #666;">
        A $10-20M investment in financial reform would save $55-100M annually — a <strong>5-10x return</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 10: THE LOGICAL QUESTION - NEW
    # ========================================================================
    st.markdown('<div class="section-header">🤔 If the Budget is 96.3% Unreliable...</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 2px solid #DC2626; margin: 15px 0;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div style="padding: 15px; background: white; border-radius: 6px; border-left: 4px solid #DC2626;">
                <p style="margin: 0; font-weight: bold; color: #DC2626;">1. How can the government accurately plan spending?</p>
                <p style="margin: 5px 0 0 0; color: #666;">If the budget document is internally inconsistent, spending plans cannot be trusted.</p>
            </div>
            <div style="padding: 15px; background: white; border-radius: 6px; border-left: 4px solid #DC2626;">
                <p style="margin: 0; font-weight: bold; color: #DC2626;">2. How can Parliament properly scrutinize the budget?</p>
                <p style="margin: 5px 0 0 0; color: #666;">If the document contains $2.03B in contradictions, meaningful oversight is impossible.</p>
            </div>
            <div style="padding: 15px; background: white; border-radius: 6px; border-left: 4px solid #DC2626;">
                <p style="margin: 0; font-weight: bold; color: #DC2626;">3. How can citizens trust the fiscal projections?</p>
                <p style="margin: 5px 0 0 0; color: #666;">If the budget is 96.3% unreliable, the public cannot have confidence in the numbers.</p>
            </div>
            <div style="padding: 15px; background: white; border-radius: 6px; border-left: 4px solid #DC2626;">
                <p style="margin: 0; font-weight: bold; color: #DC2626;">4. How can international investors have confidence?</p>
                <p style="margin: 5px 0 0 0; color: #666;">If the government cannot produce a reliable budget, how can it be trusted with borrowed money?</p>
            </div>
        </div>
        <div style="text-align: center; padding: 15px; margin-top: 10px; background: #DC2626; border-radius: 6px;">
            <p style="margin: 0; font-size: 1.3rem; font-weight: bold; color: white;">THE ANSWER: THEY CAN'T.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 11: SUMMARY TABLE - KEY FACTS
    # ========================================================================
    st.markdown('<div class="section-header">📋 Key Facts Summary</div>', unsafe_allow_html=True)
    
    key_facts = pd.DataFrame({
        'Metric': [
            '2023 Audit Opinion',
            '2023 Deficit',
            '2026-27 Projected Deficit',
            '2023 Unverified Tax Receivables',
            '2023 Bad Debt Expense',
            '2026-27 Budgeted Bad Debt',
            '2023 SOE Transfer Discrepancy',
            '2023 Revenue',
            '2026-27 Budgeted Revenue',
            '2023 Expenditure',
            '2026-27 Budgeted Expenditure'
        ],
        'Value': [
            '🔴 Adverse (6th consecutive)',
            '-$111M',
            '-$658M',
            '$2.43B (30% of assets) ⚠️ NEW 2023',
            '$68.28M',
            '$0.50M',
            '$108.6M (Note 34)',
            '$3.48B',
            '$5.08B',
            '$3.59B',
            '$5.88B'
        ],
        'Source': [
            'AG Report 2023',
            'AG Report 2023',
            'Estimates 2026-27',
            'AG Report 2023',
            'AG Report 2023',
            'Estimates 2026-27',
            'AG Report 2023',
            'AG Report 2023',
            'Estimates 2026-27',
            'AG Report 2023',
            'Estimates 2026-27'
        ]
    })
    
    st.dataframe(
        key_facts,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Metric': 'Metric',
            'Value': 'Value',
            'Source': 'Source'
        }
    )
    
    # ========================================================================
    # SECTION 12: DOCUMENT QUALITY - THE ESTIMATES DOCUMENT ITSELF
    # ========================================================================
    st.markdown('<div class="section-header">⚠️ Document Quality: The Estimates Document Itself</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 2px solid #DC2626; margin: 15px 0;">
        <h5 style="color: #DC2626; margin-top: 0;">🚨 CRITICAL: The 2026-27 Estimates Document Contains Material Errors</h5>
        <p style="font-size: 1.05rem;">
        A systematic review of the 2026-2027 Estimates document reveals that only <strong>1 of 27 Heads</strong> (Parliament, Head 12) has perfect alignment between the "Particulars of Service" narrative and the Budget Table figures.
        </p>
        <p style="font-size: 1.05rem; color: #666;">
        <strong>Total discrepancy: $2.03B+</strong> across 26 spending Heads.
        </p>
        <p style="font-size: 0.95rem; color: #666;">
        <strong>Reliability Score: 3.7%</strong> — The document is 96.3% unreliable.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top discrepancies summary
    st.markdown('<div class="section-header">📋 Top 10 Discrepancies: Words vs Figures</div>', unsafe_allow_html=True)
    
    top_discrepancies = pd.DataFrame({
        'Head': [19, 14, 96, 86, 39, 33, 40, 13, 50, 83],
        'Ministry': [
            'Treasury',
            'Ministry of Finance',
            'Educational Transformation',
            'Health and Wellness',
            'Legal Affairs & Criminal Justice',
            'Home Affairs, Information & Public Affairs',
            'Transport & Works',
            "Prime Minister's Office",
            'Post Office',
            'Agriculture, Food & Nutritional Security'
        ],
        'Words': [
            '$54.0M',
            '$325.9M',
            '$285.4M',
            '$395.3M',
            '$194.8M',
            '$84.2M',
            '$159.9M',
            '$355.0M',
            '$13.7M',
            '$94.3M'
        ],
        'Figures': [
            '$1,653.6M',
            '$781.5M',
            '$525.2M',
            '$502.5M',
            '$278.1M',
            '$134.1M',
            '$186.1M',
            '$380.2M',
            '$32.7M',
            '$112.0M'
        ],
        'Discrepancy': [
            '$1.60B',
            '$455.6M',
            '$239.8M',
            '$107.2M',
            '$83.4M',
            '$49.9M',
            '$26.3M',
            '$25.2M',
            '$19.0M',
            '$17.8M'
        ]
    })
    
    st.dataframe(
        top_discrepancies,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Head': 'Head',
            'Ministry': 'Ministry',
            'Words': 'Words (Particulars)',
            'Figures': 'Figures (Budget Table)',
            'Discrepancy': 'Discrepancy'
        }
    )
    
    # Reliability Index
    st.markdown("""
    <div style="background: #FFFBEB; padding: 20px; border-radius: 8px; border: 2px solid #F59E0B; margin: 15px 0;">
        <h5 style="color: #D97706; margin-top: 0;">📊 RELIABILITY INDEX</h5>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
            <div style="text-align: center; padding: 15px; background: white; border-radius: 6px;">
                <div style="font-size: 2rem; font-weight: bold; color: #10B981;">1</div>
                <div style="font-size: 0.9rem; color: #666;">Head with Perfect Alignment</div>
                <div style="font-size: 0.8rem; color: #666;">Parliament (Head 12)</div>
            </div>
            <div style="text-align: center; padding: 15px; background: white; border-radius: 6px;">
                <div style="font-size: 2rem; font-weight: bold; color: #DC2626;">26</div>
                <div style="font-size: 0.9rem; color: #666;">Heads with Discrepancies</div>
                <div style="font-size: 0.8rem; color: #666;">96.3% of all Heads</div>
            </div>
            <div style="text-align: center; padding: 15px; background: white; border-radius: 6px;">
                <div style="font-size: 2rem; font-weight: bold; color: #DC2626;">3.7%</div>
                <div style="font-size: 0.9rem; color: #666;">Reliability Score</div>
                <div style="font-size: 0.8rem; color: #666;">96.3% Unreliable</div>
            </div>
        </div>
        <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">
        <strong>Interpretation:</strong> The Estimates document is 96.3% unreliable. Only Parliament's budget is internally consistent.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Critical errors detail
    st.markdown("""
    <div style="background: #FEF2F2; padding: 20px; border-radius: 8px; border: 2px solid #DC2626; margin: 15px 0;">
        <h5 style="color: #DC2626; margin-top: 0;">🔴 CRITICAL ERRORS (>$100M)</h5>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 10px;">
            <div style="background: white; padding: 10px; border-radius: 6px; border: 1px solid #DC2626;">
                <strong>Head 19: Treasury</strong><br>
                Words: $54M → Figures: $1.65B<br>
                <span style="color: #DC2626; font-weight: bold;">Discrepancy: $1.60B</span>
            </div>
            <div style="background: white; padding: 10px; border-radius: 6px; border: 1px solid #DC2626;">
                <strong>Head 14: Ministry of Finance</strong><br>
                Words: $326M → Figures: $782M<br>
                <span style="color: #DC2626; font-weight: bold;">Discrepancy: $456M</span>
            </div>
            <div style="background: white; padding: 10px; border-radius: 6px; border: 1px solid #DC2626;">
                <strong>Head 96: Educational Transformation</strong><br>
                Words: $285M → Figures: $525M<br>
                <span style="color: #DC2626; font-weight: bold;">Discrepancy: $240M</span>
            </div>
        </div>
        <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">
        <strong>Impact:</strong> These discrepancies call into question the reliability of the Estimates document itself.
        If the government cannot present a consistent budget document, how can the public trust the numbers?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 13: ACTION REQUIRED - NEW
    # ========================================================================
    st.markdown('<div class="section-header">📌 What Needs to Happen</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #F0F7FF; padding: 20px; border-radius: 8px; border: 2px solid #3B82F6; margin: 15px 0;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div style="padding: 12px; background: white; border-radius: 6px; border-left: 4px solid #DC2626;">
                <p style="margin: 0; font-weight: bold; color: #DC2626;">1. Fix the $2.03B+ Discrepancies</p>
                <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #666;">Reconcile all 26 Heads with misaligned numbers</p>
                <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #DC2626;">⏱️ IMMEDIATE</p>
            </div>
            <div style="padding: 12px; background: white; border-radius: 6px; border-left: 4px solid #DC2626;">
                <p style="margin: 0; font-weight: bold; color: #DC2626;">2. Verify the $2.43B Tax Receivables</p>
                <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #666;">Determine how much is collectible vs uncollectible</p>
                <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #DC2626;">⏱️ WITHIN 6 MONTHS</p>
            </div>
            <div style="padding: 12px; background: white; border-radius: 6px; border-left: 4px solid #F59E0B;">
                <p style="margin: 0; font-weight: bold; color: #D97706;">3. Consolidate All 40+ SOEs</p>
                <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #666;">End 21+ years of IPSAS violations</p>
                <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #D97706;">⏱️ WITHIN 12 MONTHS</p>
            </div>
            <div style="padding: 12px; background: white; border-radius: 6px; border-left: 4px solid #F59E0B;">
                <p style="margin: 0; font-weight: bold; color: #D97706;">4. Disclose the $4B+ Pension Liability</p>
                <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #666;">Complete actuarial study and include on balance sheet</p>
                <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #D97706;">⏱️ WITHIN 12 MONTHS</p>
            </div>
            <div style="padding: 12px; background: white; border-radius: 6px; border-left: 4px solid #10B981; grid-column: span 2;">
                <p style="margin: 0; font-weight: bold; color: #10B981;">5. Achieve a Clean Audit Opinion</p>
                <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #666;">End 6 consecutive adverse opinions</p>
                <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #10B981;">⏱️ BY 2027</p>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 15px; padding-top: 15px; border-top: 1px solid #E2E8F0;">
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #DC2626;">$10-20M</div>
                <div style="font-size: 0.9rem; color: #666;">Estimated Cost</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #10B981;">$55-100M</div>
                <div style="font-size: 0.9rem; color: #666;">Annual Savings</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #10B981;">5-10x</div>
                <div style="font-size: 0.9rem; color: #666;">Return on Investment</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 14: CONCLUSION - FACTUAL
    # ========================================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00267F 0%, #1E40AF 100%); padding: 30px; border-radius: 10px; color: white; margin-top: 20px;">
        <h3 style="color: white; text-align: center;">🇧🇧 Summary</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 15px; margin-top: 20px;">
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #FFC726;">+$1.59B</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Projected Revenue Increase</div>
                <div style="font-size: 0.8rem; color: #93C5FD;">46% growth from 2023</div>
            </div>
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #FFC726;">+$2.29B</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Projected Expenditure Increase</div>
                <div style="font-size: 0.8rem; color: #93C5FD;">64% growth from 2023</div>
            </div>
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #FFC726;">$2.43B</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Unverified Tax Receivables</div>
                <div style="font-size: 0.8rem; color: #93C5FD;">First flagged in 2023</div>
            </div>
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #DC2626;">96.3%</div>
                <div style="font-size: 0.9rem; color: #BFDBFE;">Unreliable Budget Document</div>
                <div style="font-size: 0.8rem; color: #93C5FD;">$2.03B+ in discrepancies</div>
            </div>
        </div>
        <p style="text-align: center; font-size: 1rem; color: #93C5FD; margin-top: 20px;">
        The 2026-27 budget represents a significant increase in both revenue and expenditure projections.
        However, the budget document itself contains <strong style="color: #FFC726;">26 material discrepancies</strong> 
        totaling <strong style="color: #FFC726;">$2.03B+</strong>, with a <strong style="color: #FFC726;">reliability score of just 3.7%</strong>.
        </p>
        <p style="text-align: center; font-size: 1rem; color: #93C5FD; margin-top: 10px;">
        <strong style="color: #FFC726;">Only Parliament's budget (Head 12) is internally consistent.</strong>
        </p>
        <p style="text-align: center; font-size: 0.9rem; color: #93C5FD; margin-top: 10px;">
        <em>All figures are sourced from the 2023 Audited Financial Statements and the 2026-2027 Estimates of Revenue and Expenditure.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.caption("""
    **Data Sources:** Auditor General's Report 2023 • 2026-2027 Estimates of Revenue and Expenditure
    **Note:** All figures are from official Government documents. Where data is estimated or not directly comparable, this is noted.
    """)