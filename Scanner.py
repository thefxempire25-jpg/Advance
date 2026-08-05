import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Surgeon DOM & Scanner Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# AUTHENTICATION GATE (MATCHED APP COLOR THEME)
# ==========================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
        <style>
        .stApp {
            background-color: #0d1117;
            color: #f1f5f9;
            font-family: 'Inter', sans-serif;
        }
        .login-container {
            max-width: 420px;
            margin: 80px auto;
            background: #161b22;
            color: #f1f5f9;
            padding: 40px;
            border-radius: 8px;
            border: 1px solid #21262d;
            border-top: 4px solid #DC143C;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            text-align: center;
        }
        .login-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 25px;
            color: #06B6D4;
        }
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #DC143C 0%, #900C3F 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            padding: 10px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #06B6D4 0%, #38BDF8 100%);
            color: #0d1117;
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="login-container">
                <div class="login-title">🔐 Surgeon Access Gate</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email_input = st.text_input("Email Address", placeholder="name@example.com")
            key_input = st.text_input("Access Key / Password", type="password", placeholder="Enter secret access key")
            submit_btn = st.form_submit_button("LOGIN")
            
            if submit_btn:
                MASTER_KEY = "SURGEON2026"
                if key_input == MASTER_KEY:
                    st.session_state.authenticated = True
                    st.success("Access Granted! Loading Workstation...")
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.error("Invalid Access Key. Please check your credentials.")
    
    st.stop()

# ==========================================
# CUSTOM CRIMSON-CYAN THEME (MAIN APP)
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #21262d;
    }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .metric-card-crimson { border-left: 4px solid #DC143C; }
    .metric-card-skyblue { border-left: 4px solid #38BDF8; }
    .metric-card-cyan { border-left: 4px solid #06B6D4; }
    
    .card-label {
        font-size: 11px;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .card-value {
        font-size: 22px;
        font-weight: bold;
        margin-top: 5px;
    }
    .card-value.cyan { color: #06B6D4; }
    .card-value.skyblue { color: #38BDF8; }
    .card-value.crimson { color: #DC143C; }

    .stButton>button {
        background: linear-gradient(135deg, #DC143C 0%, #900C3F 100%);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #06B6D4 0%, #38BDF8 100%);
        color: #0d1117;
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if 'account_equity' not in st.session_state:
    st.session_state.account_equity = 100000.0
if 'active_trade' not in st.session_state:
    st.session_state.active_trade = None

# ==========================================
# QUANTITATIVE INDICATORS
# ==========================================
def calculate_atr(df, period=14):
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def calculate_roc(df, period=5):
    return ((df['Close'] - df['Close'].shift(period)) / df['Close'].shift(period)) * 100

def get_market_data(ticker_symbol, timeframe='1d', period='60d'):
    try:
        data = yf.download(ticker_symbol, period=period, interval=timeframe, progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except Exception:
        return None

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.markdown("<h2 style='color: #06B6D4;'>⚡ SURGEON DOM</h2>", unsafe_allow_html=True)
st.sidebar.caption("Surgical Market Microstructure Engine")

if st.sidebar.button("🔒 Logout / Lock Workspace"):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🛡️ Account Risk Controls")
account_balance = st.sidebar.number_input("Account Balance ($)", value=100000.0, step=5000.0)
risk_pct = st.sidebar.slider("Max Risk Per Trade (%)", min_value=0.1, max_value=1.0, value=0.3, step=0.05) / 100.0
max_risk_usd = account_balance * risk_pct

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Execution Parameters")
atr_multiplier = st.sidebar.slider("ATR Multiplier (Stop Distance)", 0.5, 3.0, 1.25, 0.05)
rr_ratio = st.sidebar.slider("Risk-to-Reward Ratio (RR)", 1.0, 5.0, 3.0, 0.5)

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
    <div class="metric-card metric-card-crimson">
        <div class="card-label">Hard Risk Limit (0.3%)</div>
        <div class="card-value crimson">${max_risk_usd:,.2f}</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# TOP HEADER & METRIC CARDS
# ==========================================
col_h1, col_h2, col_h3, col_h4 = st.columns(4)

with col_h1:
    st.markdown(f"""
        <div class="metric-card metric-card-cyan">
            <div class="card-label">Account Balance</div>
            <div class="card-value cyan">${account_balance:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown(f"""
        <div class="metric-card metric-card-skyblue">
            <div class="card-label">Weekly Target (+4%)</div>
            <div class="card-value skyblue">${account_balance * 0.04:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col_h3:
    st.markdown(f"""
        <div class="metric-card metric-card-crimson">
            <div class="card-label">Max Risk Per Trade</div>
            <div class="card-value crimson">${max_risk_usd:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col_h4:
    st.markdown(f"""
        <div class="metric-card metric-card-cyan">
            <div class="card-label">Monthly Target (+10%)</div>
            <div class="card-value cyan">${account_balance * 0.10:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# NAVIGATION TABS
# ==========================================
tab1, tab2 = st.tabs(["📡 Triage Scanner Grid", "🔪 Surgical DOM Simulator"])

watchlist = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "Gold (XAU/USD)": "GC=F",
    "S&P 500 Futures": "ES=F",
    "Bitcoin": "BTC-USD"
}

# ==========================================
# TAB 1: TRIAGE SCANNER
# ==========================================
with tab1:
    col_dxy, col_macro = st.columns([1, 2])
    
    dxy_df = get_market_data("DX-Y.NYB", timeframe="1d", period="30d")
    dxy_bias = "NEUTRAL"
    dxy_roc = 0.0
    
    if dxy_df is not None and not dxy_df.empty:
        dxy_df['ROC'] = calculate_roc(dxy_df, period=5)
        dxy_roc = dxy_df['ROC'].iloc[-1]
        if dxy_roc > 0.2:
            dxy_bias = "BULLISH (USD STRONG)"
        elif dxy_roc < -0.2:
            dxy_bias = "BEARISH (USD WEAK)"
            
    with col_dxy:
        st.markdown(f"""
            <div class="metric-card metric-card-skyblue">
                <div class="card-label">DXY Macro Direction</div>
                <div class="card-value skyblue">{dxy_bias}</div>
                <div style="font-size: 12px; color: #8b949e; margin-top:5px;">5D Momentum ROC: <b style="color:#06B6D4">{dxy_roc:.2f}%</b></div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_macro:
        st.markdown("""
            <div class="metric-card metric-card-cyan">
                <div class="card-label">Surgical Macro Rulebook</div>
                <div style="font-size: 13px; color: #f1f5f9; margin-top:5px;">
                    When DXY is <b style="color:#38BDF8">BULLISH</b>, look for short cuts on EUR/USD, GBP/USD, and Gold.<br>
                    Execute cuts only when <b style="color:#06B6D4">ATR Volatility</b> confirms liquidity voids are open.
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Multi-Timeframe Triage Grid")
    
    grid_data = []
    for name, ticker in watchlist.items():
        df = get_market_data(ticker, timeframe="1d", period="60d")
        if df is not None and len(df) > 20:
            df['ATR_5'] = calculate_atr(df, 5)
            df['ATR_20'] = calculate_atr(df, 20)
            df['ROC'] = calculate_roc(df, 5)
            
            latest_price = df['Close'].iloc[-1]
            atr_5 = df['ATR_5'].iloc[-1]
            atr_20 = df['ATR_20'].iloc[-1]
            roc = df['ROC'].iloc[-1]
            
            vol_status = "HIGH" if atr_5 > (atr_20 * 0.85) else "LOW (CHOP)"
            
            score = 0.0
            if vol_status == "HIGH": score += 0.35
            if abs(roc) > 0.5: score += 0.35
            
            aligned = False
            if "USD=X" in ticker or ticker == "GC=F":
                if (dxy_bias.startswith("BULLISH") and roc < 0) or (dxy_bias.startswith("BEARISH") and roc > 0):
                    score += 0.30
                    aligned = True
            else:
                score += 0.20
            
            action = "OPEN DOM 🟢" if score >= 0.70 else "MUTED 🔴"
            
            grid_data.append({
                "Asset": name,
                "Price": f"{latest_price:,.4f}",
                "ATR (5D)": f"{atr_5:.4f}",
                "Volatility Gate": vol_status,
                "Momentum (ROC)": f"{roc:.2f}%",
                "DXY Aligned": "YES" if aligned else "NO",
                "Confluence Score": round(score, 2),
                "Status": action
            })
            
    grid_df = pd.DataFrame(grid_data)
    
    def style_grid(val):
        if val == "OPEN DOM 🟢":
            return 'color: #06B6D4; font-weight: bold;'
        elif val == "MUTED 🔴":
            return 'color: #DC143C;'
        elif val == "HIGH":
            return 'color: #38BDF8;'
        return ''

    st.dataframe(grid_df.style.map(style_grid), use_container_width=True)

# ==========================================
# TAB 2: SURGICAL DOM SIMULATOR
# ==========================================
with tab2:
    selected_asset_name = st.selectbox("Select Asset to Trade on DOM", list(watchlist.keys()))
    selected_ticker = watchlist[selected_asset_name]
    
    asset_df = get_market_data(selected_ticker, timeframe="5m", period="5d")
    
    if asset_df is not None and not asset_df.empty:
        current_price = float(asset_df['Close'].iloc[-1])
        asset_df['ATR'] = calculate_atr(asset_df, 14)
        current_atr = float(asset_df['ATR'].iloc[-1]) if not pd.isna(asset_df['ATR'].iloc[-1]) else (current_price * 0.002)
    else:
        current_price = 1.0850
        current_atr = 0.0015

    col_dom, col_calc = st.columns([2, 1])
    
    stop_dist_pts = current_atr * atr_multiplier
    target_dist_pts = stop_dist_pts * rr_ratio
    point_value = 100000.0 if "USD=X" in selected_ticker else (50.0 if "ES=F" in selected_ticker else 1.0)
    lot_size = max_risk_usd / (stop_dist_pts * point_value)
    
    with col_calc:
        st.markdown("""
            <div class="metric-card metric-card-cyan">
                <div class="card-label">Dynamic Sizing Panel</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.metric("Live Market Price", f"{current_price:,.5f}")
        st.metric("5-Min ATR Volatility", f"{current_atr:,.5f}")
        
        st.markdown("---")
        st.write(f"**Stop-Loss Distance:** `{stop_dist_pts:.5f} pts` ({stop_dist_pts*10000:.1f} ticks)")
        st.write(f"**Take-Profit Distance:** `{target_dist_pts:.5f} pts` ({target_dist_pts*10000:.1f} ticks)")
        
        st.markdown("---")
        st.markdown(f"**Calculated Lot Size:** <b style='color:#06B6D4'>{lot_size:.2f} Lots</b>", unsafe_allow_html=True)
        st.markdown(f"**Max Dollar Risk:** <b style='color:#DC143C'>${max_risk_usd:,.2f}</b>", unsafe_allow_html=True)
        st.markdown(f"**Target Reward:** <b style='color:#38BDF8'>${max_risk_usd * rr_ratio:,.2f}</b>", unsafe_allow_html=True)
        
        trade_dir = st.radio("Execution Direction", ["SHORT (Fill Void Down)", "LONG (Fill Void Up)"])
        
        if trade_dir.startswith("SHORT"):
            entry_p = current_price
            sl_p = entry_p + stop_dist_pts
            tp_p = entry_p - target_dist_pts
        else:
            entry_p = current_price
            sl_p = entry_p - stop_dist_pts
            tp_p = entry_p + target_dist_pts
            
        if st.button("🔥 EXECUTE SURGICAL CUT", use_container_width=True):
            st.session_state.active_trade = {
                "asset": selected_asset_name,
                "direction": trade_dir,
                "entry": entry_p,
                "sl": sl_p,
                "tp": tp_p,
                "lots": lot_size,
                "risk": max_risk_usd
            }
            st.success("Surgical Cut Executed into Simulated DOM Order Book!")

    with col_dom:
        st.subheader("Level 2 Depth of Market Ladder")
        
        tick_step = current_atr * 0.2
        levels = 10
        prices = [current_price + (i * tick_step) for i in range(levels, -levels - 1, -1)]
        
        dom_rows = []
        np.random.seed(42)
        
        for p in prices:
            p_rounded = round(p, 5)
            bid_vol = 0
            ask_vol = 0
            is_void = False
            is_wall = False
            
            diff_ticks = round((p - current_price) / tick_step)
            
            if diff_ticks in [2, 3, 4] or diff_ticks in [-2, -3, -4]:
                is_void = True
                vol = np.random.randint(1, 8)
            elif diff_ticks in [6, -6]:
                is_wall = True
                vol = np.random.randint(250, 500)
            else:
                vol = np.random.randint(30, 120)
                
            if p > current_price:
                ask_vol = vol
            elif p < current_price:
                bid_vol = vol
                
            tag = ""
            if abs(p - entry_p) < (tick_step / 2): tag = "📍 ENTRY"
            elif abs(p - sl_p) < (tick_step / 2): tag = "🛑 STOP LOSS"
            elif abs(p - tp_p) < (tick_step / 2): tag = "🎯 TAKE PROFIT"
            elif is_void: tag = "⚡ VOID"
            elif is_wall: tag = "🧱 LIQUIDITY WALL"

            dom_rows.append({
                "Bid Vol (Buyers)": bid_vol if bid_vol > 0 else "",
                "Price Level": f"{p_rounded:.5f}",
                "Ask Vol (Sellers)": ask_vol if ask_vol > 0 else "",
                "Structure Marker": tag
            })
            
        dom_table = pd.DataFrame(dom_rows)
        
        def style_dom_row(row):
            marker = row["Structure Marker"]
            if "STOP LOSS" in marker:
                return ['background-color: rgba(220, 20, 60, 0.4); color: white; font-weight: bold;'] * len(row)
            elif "TAKE PROFIT" in marker:
                return ['background-color: rgba(6, 182, 212, 0.4); color: white; font-weight: bold;'] * len(row)
            elif "ENTRY" in marker:
                return ['background-color: rgba(56, 189, 248, 0.4); color: white; font-weight: bold;'] * len(row)
            elif "VOID" in marker:
                return ['background-color: rgba(6, 182, 212, 0.15); color: #06B6D4;'] * len(row)
            elif "WALL" in marker:
                return ['background-color: rgba(220, 20, 60, 0.15); color: #DC143C;'] * len(row)
            return [''] * len(row)

        st.dataframe(dom_table.style.apply(style_dom_row, axis=1), use_container_width=True, height=500)