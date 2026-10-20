# 📱 Mobile Recharge Calculator

A beginner-friendly Python web application built with **Streamlit** and **Object-Oriented Programming (OOP)**. It allows users to calculate mobile recharge plan costs, compute applicable Goods & Services Tax (GST at 18%), evaluate effective per-day cost, view total high-speed data, and generate downloadable digital tax invoices.

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌟 Features

- **Object-Oriented Architecture**: Clean `MobileRecharge` class encapsulating plan attributes, tax calculations, and plan summaries.
- **Accurate Tax Calculations**:
  - **GST Calculation**: $\text{GST} = \frac{\text{plan\_amount} \times \text{gst\_rate}}{100}$ (default rate: 18%)
  - **Total Payable Amount**: $\text{Final Price} = \text{plan\_amount} + \text{GST}$
- **Full Input Validation**:
  - Validates 10-digit mobile numbers with prefix cleaning (`+91`, `0`).
  - Checks positive plan amounts, valid days, daily data allowances, and talktime.
- **Popular Plan Presets**:
  - One-click autofill for popular plans: Daily Saver (₹239), Binge Hero (₹299), Quarterly Pack (₹666), Long Term Saver (₹719), Annual Mega Saver (₹2999), and Talktime Top-Up (₹100).
- **Telecom Operator Selection**: Support for Jio, Airtel, Vi, BSNL, and custom networks.
- **Instant Key Metrics & Analytics**:
  - Base plan price vs. GST breakdown
  - Effective per-day cost ($\frac{\text{Total}}{\text{Validity}}$)
  - Total high-speed data volume over the entire validity cycle
  - Interactive proportion visualizer
- **Digital Tax Invoice & Receipt**:
  - Professional tax invoice summary with unique reference numbers and timestamps.
  - One-click `.txt` receipt download.
- **Interactive Python OOP Code Viewer**:
  - Live preview explaining how the Python OOP code executes in the background.

---

## 🏗️ Python Class Structure (`MobileRecharge`)

The core business logic is encapsulated in the `MobileRecharge` class located in [`app.py`](file:///e:/mobile_recharge/app.py):

```python
class MobileRecharge:
    def __init__(
        self,
        mobile_number: str,
        plan_amount: float,
        plan_validity: int,
        data_per_day: float,
        talktime: float,
        gst_rate: float = 18.0
    ):
        self.mobile_number = mobile_number
        self.plan_amount = plan_amount
        self.plan_validity = plan_validity
        self.data_per_day = data_per_day
        self.talktime = talktime
        self.gst_rate = gst_rate

    def calculate_gst(self) -> float:
        """Calculate GST as plan_amount * gst_rate / 100."""
        return (self.plan_amount * self.gst_rate) / 100.0

    def calculate_total_amount(self) -> float:
        """Calculate final payable amount as plan_amount + GST."""
        return self.plan_amount + self.calculate_gst()

    def display_plan_details(self) -> dict:
        """Return a structured dictionary containing all plan details."""
        gst = self.calculate_gst()
        total = self.calculate_total_amount()
        total_data = self.data_per_day * self.plan_validity
        cost_per_day = (total / self.plan_validity) if self.plan_validity > 0 else 0.0

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
            "cost_per_day": round(cost_per_day, 2)
        }
```

---

## 📁 Repository Structure

```plaintext
mobile_recharge/
│
├── app.py                   # Main Streamlit web application & MobileRecharge class
├── requirements.txt         # Required Python packages (Streamlit)
├── test_mobile_recharge.py  # Unit test suite for verification
├── .gitignore               # Git ignore rules for Python & environments
└── README.md                # Project documentation and deployment guide
```

---

## 🚀 Local Setup & Installation

### 1. Prerequisites
- [Python 3.9 or higher](https://www.python.org/downloads/)
- `pip` (Python package installer)
- Git (optional, for cloning)

### 2. Clone or Download the Project
```bash
git clone https://github.com/<your-username>/mobile-recharge-calculator.git
cd mobile-recharge-calculator
```

### 3. (Optional) Create a Virtual Environment
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
streamlit run app.py
```
*(Alternatively: `python -m streamlit run app.py`)*

The web app will automatically open in your default browser at `http://localhost:8501`.

---

## 🧪 Running Unit Tests

Run the included automated unit tests to verify the calculations:
```bash
python test_mobile_recharge.py
```

Expected output:
```plaintext
Ran 5 tests in 0.000s
OK
```

---

## ☁️ Deployment to Streamlit Community Cloud from GitHub

This repository is pre-configured and 100% ready for deployment to **[Streamlit Community Cloud](https://streamlit.io/cloud)**.

### Step 1: Initialize Git and Push to GitHub
1. Open your terminal in the project directory:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Mobile Recharge Calculator"
   ```
2. Create a new public repository on [GitHub](https://github.com/new) (e.g., `mobile-recharge-calculator`).
3. Link your remote repository and push:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/mobile-recharge-calculator.git
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Community Cloud
1. Visit **[share.streamlit.io](https://share.streamlit.io/)** and sign in with your GitHub account.
2. Click the **"New app"** button.
3. Fill in the deployment details:
   - **Repository**: `<your-username>/mobile-recharge-calculator`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **"Deploy!"**.
5. Within 1–2 minutes, Streamlit will install `requirements.txt` and launch your live public web app with a shareable URL (e.g., `https://<your-app-name>.streamlit.app`).

---

## 💡 Educational Concepts Demonstrated

1. **Class and Object Creation**:
   - `class MobileRecharge:` creates a blueprint.
   - `recharge = MobileRecharge(...)` instantiates the class into an object with individual state.
2. **Encapsulation**:
   - Bundling state (`plan_amount`, `gst_rate`) together with related methods (`calculate_gst`, `calculate_total_amount`).
3. **Type Hinting & Docstrings**:
   - Code is clean, maintainable, and self-documenting with Python standard typing.
4. **Separation of Concerns**:
   - Core computational logic is decoupled from UI presentation, enabling seamless unit testing.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
