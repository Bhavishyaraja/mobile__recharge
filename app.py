"""
Mobile Recharge Calculator
Built with Python & Streamlit
========================================
A beginner-friendly web application demonstrating Object-Oriented Programming (OOP)
to calculate mobile recharge costs, GST (18%), per-day value, and total breakdown.
"""

import re
import datetime
import streamlit as st


# ==============================================================================
# 1. CORE OOP MODEL (MobileRecharge Class)
# ==============================================================================
class MobileRecharge:
    """
    Represents a Mobile Recharge plan with tax calculations and plan specifications.

    Attributes:
        mobile_number (str): 10-digit mobile phone number.
        plan_amount (float): Base price of the recharge plan in INR (₹).
        plan_validity (int): Plan validity in calendar days.
        data_per_day (float): Daily high-speed data allowance in GB.
        talktime (float): Talktime allowance in minutes (0 indicates unlimited voice).
        gst_rate (float): Goods & Services Tax percentage (default: 18.0%).
    """

    def __init__(
        self,
        mobile_number: str,
        plan_amount: float,
        plan_validity: int,
        data_per_day: float,
        talktime: float,
        gst_rate: float = 18.0,
    ):
        self.mobile_number = str(mobile_number).strip()
        self.plan_amount = float(plan_amount)
        self.plan_validity = int(plan_validity)
        self.data_per_day = float(data_per_day)
        self.talktime = float(talktime)
        self.gst_rate = float(gst_rate)

    def calculate_gst(self) -> float:
        """
        Calculate Goods & Services Tax (GST).
        Formula: GST = plan_amount * gst_rate / 100
        """
        return (self.plan_amount * self.gst_rate) / 100.0

    def calculate_total_amount(self) -> float:
        """
        Calculate final payable price.
        Formula: final_price = plan_amount + GST
        """
        return self.plan_amount + self.calculate_gst()

    def display_plan_details(self) -> dict:
        """
        Compile and return a structured dictionary containing all plan details,
        calculated taxes, total cost, and derived statistics (per-day cost, total data).
        """
        gst = self.calculate_gst()
        total = self.calculate_total_amount()
        total_data = self.data_per_day * self.plan_validity
        cost_per_day = (total / self.plan_validity) if self.plan_validity > 0 else 0.0

        talktime_label = (
            "Unlimited Calls"
            if self.talktime == 0 or self.talktime >= 9999
            else f"{self.talktime:g} Minutes"
        )

        return {
            "mobile_number": self.mobile_number,
            "plan_amount": round(self.plan_amount, 2),
            "gst_rate": self.gst_rate,
            "gst_amount": round(gst, 2),
            "total_amount": round(total, 2),
            "plan_validity": self.plan_validity,
            "data_per_day": self.data_per_day,
            "total_data": round(total_data, 2),
            "talktime": self.talktime,
            "talktime_label": talktime_label,
            "cost_per_day": round(cost_per_day, 2),
        }

    def __str__(self) -> str:
        """Friendly string representation of the recharge object."""
        details = self.display_plan_details()
        return (
            f"MobileRecharge(Number={details['mobile_number']}, "
            f"Base=₹{details['plan_amount']}, GST=₹{details['gst_amount']}, "
            f"Total=₹{details['total_amount']}, Validity={details['plan_validity']}d)"
        )


# ==============================================================================
# 2. VALIDATION HELPERS
# ==============================================================================
def sanitize_mobile_number(raw_number: str) -> str:
    """Strip spaces, dashes, parentheses and country code prefixes (+91 or 91)."""
    clean = re.sub(r"[^\d]", "", str(raw_number))
    if clean.startswith("91") and len(clean) == 12:
        clean = clean[2:]
    elif clean.startswith("0") and len(clean) == 11:
        clean = clean[1:]
    return clean


def validate_inputs(
    mobile: str, amount: float, validity: int, data: float, talktime: float
) -> tuple[bool, list[str]]:
    """Validate all user inputs and return status and error messages."""
    errors = []

    # Mobile validation
    clean_mobile = sanitize_mobile_number(mobile)
    if not clean_mobile:
        errors.append("Phone number is required.")
    elif len(clean_mobile) != 10:
        errors.append(f"Phone number must be exactly 10 digits (got {len(clean_mobile)}).")
    elif clean_mobile[0] not in "6789":
        errors.append("Standard mobile numbers usually start with digits 6, 7, 8, or 9.")

    # Plan amount validation
    if amount <= 0:
        errors.append("Plan amount must be greater than ₹0.")
    elif amount > 50000:
        errors.append("Plan amount exceeds maximum limit (₹50,000).")

    # Validity validation
    if validity <= 0:
        errors.append("Plan validity must be at least 1 day.")
    elif validity > 730:
        errors.append("Plan validity cannot exceed 730 days (2 years).")

    # Data validation
    if data < 0:
        errors.append("Daily data cannot be negative.")

    # Talktime validation
    if talktime < 0:
        errors.append("Talktime cannot be negative.")

    return len(errors) == 0, errors


# ==============================================================================
# 3. POPULAR PLAN PRESETS FOR ONE-CLICK SELECTION
# ==============================================================================
PRESET_PLANS = {
    "🌟 Daily Saver (₹239)": {
        "amount": 239.0,
        "validity": 28,
        "data": 1.5,
        "talktime": 0.0,
        "desc": "28 Days • 1.5 GB/day • Unlimited Calls",
    },
    "🔥 Binge Hero (₹299)": {
        "amount": 299.0,
        "validity": 28,
        "data": 2.0,
        "talktime": 0.0,
        "desc": "28 Days • 2.0 GB/day • Unlimited Calls + Weekend Rollover",
    },
    "🚀 Quarterly Power (₹666)": {
        "amount": 666.0,
        "validity": 70,
        "data": 1.5,
        "talktime": 0.0,
        "desc": "70 Days • 1.5 GB/day • Unlimited Calls",
    },
    "💎 Long Term Saver (₹719)": {
        "amount": 719.0,
        "validity": 84,
        "data": 1.5,
        "talktime": 0.0,
        "desc": "84 Days • 1.5 GB/day • Unlimited Voice & 100 SMS/day",
    },
    "👑 Annual Mega Saver (₹2999)": {
        "amount": 2999.0,
        "validity": 365,
        "data": 2.5,
        "talktime": 0.0,
        "desc": "365 Days • 2.5 GB/day • 365d Non-stop Unlimited",
    },
    "📞 Pure Talktime Top-Up (₹100)": {
        "amount": 100.0,
        "validity": 28,
        "data": 0.0,
        "talktime": 81.75,
        "desc": "28 Days • No Data • 81.75 Mins Talktime balance",
    },
}


# ==============================================================================
# 4. STREAMLIT APPLICATION MAIN FUNCTION
# ==============================================================================
def main():
    # Page configuration
    st.set_page_config(
        page_title="Mobile Recharge Calculator",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for modern styling, clean glassmorphism, responsive cards, and typography
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        /* Gradient Hero Banner */
        .hero-container {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
            border-radius: 18px;
            padding: 30px 26px;
            color: white;
            margin-bottom: 22px;
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.35);
        }
        .hero-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.22);
            backdrop-filter: blur(8px);
            padding: 5px 12px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.6px;
            margin-bottom: 10px;
            border: 1px solid rgba(255, 255, 255, 0.35);
        }
        .hero-title {
            font-size: 32px;
            font-weight: 800;
            margin: 0 0 6px 0;
            color: #ffffff;
            letter-spacing: -0.5px;
        }
        .hero-subtitle {
            font-size: 15px;
            opacity: 0.94;
            margin: 0;
            max-width: 680px;
            line-height: 1.5;
        }

        /* Result Highlight Card */
        .highlight-card {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 24px;
            color: white;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }
        .highlight-label {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: #94a3b8;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .highlight-price {
            font-size: 44px;
            font-weight: 800;
            color: #38bdf8;
            line-height: 1.1;
            margin-bottom: 8px;
        }
        .highlight-subtext {
            font-size: 14px;
            color: #cbd5e1;
        }

        /* Metric pill boxes */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
            gap: 10px;
            margin-top: 16px;
        }
        .metric-pill {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            padding: 10px 12px;
            text-align: center;
        }
        .metric-pill-label {
            font-size: 11px;
            color: #94a3b8;
            text-transform: uppercase;
            font-weight: 600;
        }
        .metric-pill-val {
            font-size: 16px;
            font-weight: 700;
            color: #f8fafc;
            margin-top: 3px;
        }

        /* Invoice / Receipt Card */
        .receipt-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 22px;
            color: #1e293b;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        }
        .receipt-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 9px 0;
            border-bottom: 1px dashed #e2e8f0;
            font-size: 14px;
        }
        .receipt-row:last-child {
            border-bottom: none;
        }
        .receipt-bold {
            font-weight: 700;
            color: #0f172a;
        }
        .receipt-total-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 0 6px 0;
            border-top: 2px solid #0f172a;
            margin-top: 8px;
            font-size: 18px;
            font-weight: 800;
            color: #0f172a;
        }

        /* Badges */
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 6px;
        }
        .badge-blue { background: #dbeafe; color: #1e40af; }
        .badge-green { background: #dcfce7; color: #166534; }
        .badge-purple { background: #f3e8ff; color: #6b21a8; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------------------
    # SIDEBAR: OPERATOR & CONFIGURATION
    # --------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### 📡 Telecom Operator")
        operator = st.selectbox(
            "Select your network provider:",
            ["Jio 🔵", "Airtel 🔴", "Vi (Vodafone Idea) 🟡", "BSNL 🟢", "Other Telecom 🌐"],
            index=0,
        )

        st.markdown("---")
        st.markdown("### ⚡ Quick Presets")
        st.caption("Pick a popular plan to auto-fill fields:")

        preset_choice = st.selectbox(
            "Choose a plan template:",
            ["-- Custom Plan (Manual Input) --"] + list(PRESET_PLANS.keys()),
            index=1,  # Default to Daily Saver
        )

        st.markdown("---")
        st.markdown("### ⚙️ Tax Settings")
        tax_rate = st.slider(
            "GST Rate (%)",
            min_value=0.0,
            max_value=28.0,
            value=18.0,
            step=0.5,
            help="Standard Telecom Services GST rate in India is 18%.",
        )

        st.markdown("---")
        st.markdown(
            """
            <div style="font-size: 12px; color: #64748b; line-height: 1.6;">
                <b>💡 Beginner Python Tip:</b><br>
                The <code>MobileRecharge</code> class encapsulates plan parameters
                and performs formula-based calculations cleanly with type safety.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------------------------
    # HERO HEADER
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <div class="hero-container">
            <span class="hero-badge">⚡ PYTHON STREAMLIT PROJECT</span>
            <h1 class="hero-title">Mobile Recharge Calculator</h1>
            <p class="hero-subtitle">
                Calculate accurate mobile recharge costs including GST (18%), per-day value analysis,
                and complete breakdown using object-oriented Python.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Determine preset values
    if preset_choice in PRESET_PLANS:
        preset_data = PRESET_PLANS[preset_choice]
        default_amount = preset_data["amount"]
        default_validity = preset_data["validity"]
        default_data = preset_data["data"]
        default_talktime = preset_data["talktime"]
    else:
        default_amount = 299.0
        default_validity = 28
        default_data = 1.5
        default_talktime = 0.0

    # --------------------------------------------------------------------------
    # TWO-COLUMN RESPONSIVE LAYOUT
    # --------------------------------------------------------------------------
    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("### 📝 Enter Plan Details")
        st.caption("Provide your mobile number and recharge specifications below.")

        with st.container(border=True):
            # 1. Phone number
            mobile_input = st.text_input(
                "📞 Mobile Number (10 digits)",
                value="9876543210",
                max_chars=14,
                help="Enter a 10-digit mobile number. Prefixes like +91 or leading 0 are automatically handled.",
            )

            # 2. Plan Amount & Validity
            c1, c2 = st.columns(2)
            with c1:
                plan_amount_input = st.number_input(
                    "💰 Plan Base Amount (₹)",
                    min_value=1.0,
                    max_value=50000.0,
                    value=float(default_amount),
                    step=10.0,
                    format="%.2f",
                    help="Base recharge plan price before GST.",
                )
            with c2:
                plan_validity_input = st.number_input(
                    "📅 Validity (Days)",
                    min_value=1,
                    max_value=730,
                    value=int(default_validity),
                    step=1,
                    help="Total duration of the recharge pack in days.",
                )

            # 3. Daily Data & Talktime
            c3, c4 = st.columns(2)
            with c3:
                data_per_day_input = st.number_input(
                    "🌐 Daily Data (GB/day)",
                    min_value=0.0,
                    max_value=20.0,
                    value=float(default_data),
                    step=0.5,
                    format="%.1f",
                    help="Daily high-speed data limit in GB. Enter 0 for voice-only packs.",
                )
            with c4:
                is_unlimited_talk = st.checkbox(
                    "Unlimited Voice Calls",
                    value=(default_talktime == 0.0),
                    help="Check if plan offers unlimited domestic voice calls.",
                )

                if is_unlimited_talk:
                    talktime_input = 0.0
                    st.info("📞 Unlimited Voice Active")
                else:
                    talktime_input = st.number_input(
                        "⏱️ Talktime (Minutes)",
                        min_value=0.0,
                        max_value=10000.0,
                        value=float(default_talktime if default_talktime > 0 else 100.0),
                        step=10.0,
                        format="%.1f",
                        help="Dedicated talktime balance in minutes.",
                    )

            calculate_btn = st.button(
                "🚀 Calculate Recharge & Taxes", type="primary", use_container_width=True
            )

    # --------------------------------------------------------------------------
    # RESULTS & DISPLAY
    # --------------------------------------------------------------------------
    is_valid, validation_errors = validate_inputs(
        mobile=mobile_input,
        amount=plan_amount_input,
        validity=plan_validity_input,
        data=data_per_day_input,
        talktime=talktime_input,
    )

    with col_result:
        if not is_valid:
            st.markdown("### ⚠️ Validation Issues")
            for err in validation_errors:
                st.error(f"• {err}")
            st.info("👉 Please update the input fields on the left to calculate.")
        else:
            # Instantiate our MobileRecharge class
            recharge = MobileRecharge(
                mobile_number=sanitize_mobile_number(mobile_input),
                plan_amount=plan_amount_input,
                plan_validity=plan_validity_input,
                data_per_day=data_per_day_input,
                talktime=talktime_input,
                gst_rate=tax_rate,
            )

            # Retrieve structured calculations using OOP methods
            gst_val = recharge.calculate_gst()
            total_val = recharge.calculate_total_amount()
            details = recharge.display_plan_details()

            st.markdown("### 📊 Calculation Summary")

            # Hero Highlight Card for Total
            clean_num = details["mobile_number"]
            formatted_num = f"+91 {clean_num[:5]} {clean_num[5:]}" if len(clean_num) == 10 else clean_num
            st.markdown(
                f"""
                <div class="highlight-card">
                    <div class="highlight-label">Total Payable Amount (with {details['gst_rate']}% GST)</div>
                    <div class="highlight-price">₹{details['total_amount']:,.2f}</div>
                    <div class="highlight-subtext">
                        📱 <b>{formatted_num}</b> &nbsp;|&nbsp; 📶 <b>{operator.split()[0]}</b> &nbsp;|&nbsp;
                        ⏱️ <b>{details['plan_validity']} Days Validity</b>
                    </div>
                    <div class="metric-grid">
                        <div class="metric-pill">
                            <div class="metric-pill-label">Base Plan</div>
                            <div class="metric-pill-val">₹{details['plan_amount']:,.2f}</div>
                        </div>
                        <div class="metric-pill">
                            <div class="metric-pill-label">GST ({details['gst_rate']}%)</div>
                            <div class="metric-pill-val">+₹{details['gst_amount']:,.2f}</div>
                        </div>
                        <div class="metric-pill">
                            <div class="metric-pill-label">Total Data</div>
                            <div class="metric-pill-val">{details['total_data']} GB</div>
                        </div>
                        <div class="metric-pill">
                            <div class="metric-pill-label">Per Day Cost</div>
                            <div class="metric-pill-val">₹{details['cost_per_day']}/d</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Tabs for Receipt, Plan Details Breakdown, and Visual Analytics
            tab_receipt, tab_breakdown, tab_code = st.tabs(
                ["🧾 Tax Invoice Receipt", "🔍 Detailed Breakdown", "💡 Python OOP Code"]
            )

            with tab_receipt:
                now_str = datetime.datetime.now().strftime("%d-%b-%Y %I:%M %p")
                invoice_id = f"RCHG-{abs(hash(details['mobile_number'] + str(details['total_amount']))) % 1000000:06d}"

                st.markdown(
                    f"""
                    <div class="receipt-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                            <div>
                                <span class="badge badge-blue">{operator}</span>
                                <span class="badge badge-green">Recharge Invoice</span>
                            </div>
                            <span style="font-size:12px; color:#64748b;">Ref: <b>#{invoice_id}</b></span>
                        </div>
                        <div style="font-size:12px; color:#64748b; margin-bottom:14px;">
                            Date: {now_str}
                        </div>
                        <div class="receipt-row">
                            <span>Target Mobile Number</span>
                            <span class="receipt-bold">{formatted_num}</span>
                        </div>
                        <div class="receipt-row">
                            <span>Recharge Plan Base Price</span>
                            <span class="receipt-bold">₹{details['plan_amount']:.2f}</span>
                        </div>
                        <div class="receipt-row">
                            <span>GST ({details['gst_rate']}%)</span>
                            <span class="receipt-bold">+ ₹{details['gst_amount']:.2f}</span>
                        </div>
                        <div class="receipt-row">
                            <span>Validity Period</span>
                            <span>{details['plan_validity']} Days</span>
                        </div>
                        <div class="receipt-row">
                            <span>High-Speed Data Allowance</span>
                            <span>{details['data_per_day']} GB/day ({details['total_data']} GB Total)</span>
                        </div>
                        <div class="receipt-row">
                            <span>Voice Calling Allowance</span>
                            <span>{details['talktime_label']}</span>
                        </div>
                        <div class="receipt-total-row">
                            <span>Total Payable</span>
                            <span style="color:#2563eb;">₹{details['total_amount']:.2f}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Downloadable Receipt File
                receipt_text = f"""==================================================
              MOBILE RECHARGE INVOICE
==================================================
Invoice Ref:   #{invoice_id}
Date & Time:   {now_str}
Operator:      {operator}
Mobile Number: {formatted_num}
--------------------------------------------------
Base Plan Price:      ₹{details['plan_amount']:.2f}
GST Rate:             {details['gst_rate']}%
GST Amount:           ₹{details['gst_amount']:.2f}
--------------------------------------------------
TOTAL PAYABLE:        ₹{details['total_amount']:.2f}
--------------------------------------------------
Plan Validity:        {details['plan_validity']} Days
Daily Data Allowance: {details['data_per_day']} GB/day
Total High-Speed Data:{details['total_data']} GB
Talktime Allowance:   {details['talktime_label']}
Effective Cost / Day: ₹{details['cost_per_day']:.2f} / day
==================================================
Generated via Mobile Recharge Calculator (Streamlit)
"""
                st.download_button(
                    label="📥 Download Receipt (.txt)",
                    data=receipt_text,
                    file_name=f"Recharge_Receipt_{details['mobile_number']}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

            with tab_breakdown:
                st.write("##### 📈 Cost & Value Analysis")
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    st.metric("Base Price", f"₹{details['plan_amount']:.2f}")
                    st.metric("Effective Cost / Day", f"₹{details['cost_per_day']:.2f}")
                with col_b2:
                    st.metric("GST Added", f"₹{details['gst_amount']:.2f}", delta=f"{details['gst_rate']}%")
                    st.metric("Total Data Pack", f"{details['total_data']} GB")

                # Progress bar showing Base Price vs GST proportion
                base_percent = (details["plan_amount"] / details["total_amount"]) * 100
                st.caption(f"Cost Breakdown: Base Plan ({base_percent:.1f}%) | GST ({100-base_percent:.1f}%)")
                st.progress(base_percent / 100.0)

            with tab_code:
                st.write("##### 🐍 How the OOP Python Code Runs Behind This:")
                st.code(
                    f"""# 1. Instantiate the MobileRecharge class
recharge = MobileRecharge(
    mobile_number="{details['mobile_number']}",
    plan_amount={details['plan_amount']},
    plan_validity={details['plan_validity']},
    data_per_day={details['data_per_day']},
    talktime={details['talktime']},
    gst_rate={details['gst_rate']}
)

# 2. Call methods
gst = recharge.calculate_gst()               # Returns {details['gst_amount']}
total = recharge.calculate_total_amount()   # Returns {details['total_amount']}
details = recharge.display_plan_details()   # Returns complete dictionary
""",
                    language="python",
                )

    # --------------------------------------------------------------------------
    # FOOTER & EDUCATIONAL GUIDE
    # --------------------------------------------------------------------------
    st.markdown("---")
    with st.expander("📚 Beginner's Guide: Understanding the Python OOP Architecture"):
        st.markdown(
            """
            ### What is Object-Oriented Programming (OOP) here?
            1. **Class (`MobileRecharge`)**: A blueprint that bundles together recharge data (attributes) and calculations (methods).
            2. **Attributes**:
               - `mobile_number`: The phone number receiving the recharge.
               - `plan_amount`: Base cost of the plan.
               - `plan_validity`: Number of days the plan lasts.
               - `data_per_day`: Daily data allocation in GB.
               - `talktime`: Voice minutes or unlimited indicator.
               - `gst_rate`: Tax percentage (default: 18%).
            3. **Methods**:
               - `calculate_gst()`: `plan_amount * gst_rate / 100`
               - `calculate_total_amount()`: `plan_amount + GST`
               - `display_plan_details()`: Bundles all information into a structured Python dictionary.

            ### Running Locally:
            ```bash
            streamlit run app.py
            ```
            """
        )

    st.markdown(
        """
        <div style="text-align:center; padding: 20px 0; color: #94a3b8; font-size: 13px;">
            Made with ❤️ using <b>Python</b> & <b>Streamlit</b> • Ready for Streamlit Community Cloud
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
