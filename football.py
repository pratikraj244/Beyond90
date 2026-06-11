

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import datetime as dt
import pydeck as pdk
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
def pil_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_str

#img = Image.open(r"C:\Users\Pratik\OneDrive\Pictures\Screenshots\beyond90logo.png")
img = Image.open("images/beyond90logo.png")

# Option 2: Or simpler - just use st.image directly
img_base64 = pil_to_base64(img)

st.set_page_config(
    page_title="Beyond90",
    layout = "wide",
    initial_sidebar_state="expanded"   # ← always start expanded
    
)
# Then immediately hide the collapse button
st.markdown("""
<style>
/* Hide native buttons on both states */
[data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="collapsedControl"]        { display: none !important; }

/* Custom toggle — mobile only */
#menu-toggle {
    display: none;
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 999999;
    background: #2e2e2e;
    border: 1.5px solid #3CDC54;
    border-radius: 8px;
    color: white;
    font-size: 20px;
    width: 38px;
    height: 38px;
    cursor: pointer;
    align-items: center;
    justify-content: center;
}

@media (max-width: 767px) {
    #menu-toggle { display: flex !important; }
}
</style>

<button id="menu-toggle" onclick="toggleSidebar()" title="Toggle menu">☰</button>

<script>
function toggleSidebar() {
    const doc = window.parent.document;

    // Try the collapse button first (sidebar is open)
    let btn = doc.querySelector('[data-testid="stSidebarCollapseButton"] button');

    // If not found, try the expand button (sidebar is closed)
    if (!btn) {
        btn = doc.querySelector('[data-testid="collapsedControl"] button');
    }

    if (btn) {
        // Temporarily un-hide whichever button exists, click it, re-hide
        const parent = btn.closest('[data-testid="stSidebarCollapseButton"]') 
                     || btn.closest('[data-testid="collapsedControl"]');
        if (parent) {
            parent.style.cssText = "display:block!important;visibility:visible!important;opacity:1!important;";
            btn.click();
            setTimeout(() => { parent.style.cssText = "display:none!important;"; }, 100);
        } else {
            btn.click();
        }
    }
}
</script>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@media (max-width: 767px) {
    /* Sidebar slides in/out */
    section[data-testid="stSidebar"] {
        position: fixed !important;
        z-index: 9998 !important;
        height: 100vh !important;
        transform: translateX(0%);
        transition: transform 0.3s ease;
    }

    /* Push main content left so sidebar doesn't cover it */
    .main .block-container {
        padding-left: 1rem !important;
    }
}

/* Desktop — always visible, no toggle button */
@media (min-width: 768px) {
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    [data-testid="collapsedControl"]        { display: none !important; }
    #custom-toggle                          { display: none !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Main sidebar container */
    section[data-testid="stSidebar"] > div {
        padding: 0rem !important;
    }
    
    /* Option menu container */
    .st-emotion-cache-1cypcdb {
        width: 200% !important;
        padding: 0 !important;
        margin: 0 !important;
        background-color: #2b2b2b;
        border-radius: 0px;
    }
    
    /* Menu items */
    .st-emotion-cache-1wbqy5l {
        width: 100% !important;
        margin: 0 !important;
        text-align: left !important;
        padding-left: 10px !important;
        padding: 15px 15px !important;
        box-sizing: border-box !important;
    }
    
    /* Selected menu item */
    .st-emotion-cache-ffhzg2 {
        width: 100% !important;
        margin: 0 !important;
        text-align: left !important;
        padding-left: 10px !important
    }
    
    /* Remove gaps between items */
    ul[role="menu"] {
        gap: 0 !important;
    }
</style>
""", unsafe_allow_html=True)
OPTIONS = ["HOME", "INSIGHTS", "PREDICTIONS"]
st.markdown("""<style>[data-testid="stSidebar"] {
        background-color: #2e2e2e !important;
    }</style>""",unsafe_allow_html=True)
with st.sidebar:
   selected = option_menu(
        menu_title=None,
        options = ["HOME","INSIGHTS","PREDICTIONS"],
        icons=["house", "bar-chart", "robot"],
        menu_icon="cast",
        default_index=1,
        styles={
            "container": {
                "padding": "0",
                "margin": "0",
                "width": "100%",
                "background-color": "#2e2e2e",
                "border-radius": "0px"
            },
            "nav-link": {
                "width": "100%",
                "margin": "0",
                "margin-left": "5px",
                "text-align": "left",
                "padding": "16px 16px",
                "font-size": "16px",
                "text-align": "left",
                "color": "white",
            },
            "nav-link-selected": {
                "width": "100%",
                "margin": "0",
                "padding": "16px 16px",
                "background-color": "transparent",
                "color": "#3CDC54",
                "font-weight": "bold",
                "border-radius": "0",
            }
            
        }
   )

st.markdown("""
<style>
/* Ensure sidebar toggle button is always visible */
[data-testid="collapsedControl"] {
    display: block !important;
    visibility: visible !important;
}

/* Prevent sidebar from fully disappearing on collapse */
[data-testid="stSidebar"][aria-expanded="false"] {
    min-width: 0px !important;
    width: 0px !important;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
            /* Remove all default Streamlit spacing */
        .stApp header {
            display: none;
        }
        .block-container {
            padding-top: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 90% !important;
        }
        .main > div {
            padding-top: 0rem !important;
        }
        .hero-image2 {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 73vw;  /* Full viewport width */
            margin-left: 5;  /* Center and expand to full width */
            margin-right: 5;
            margin-top: 55px;
            position: relative;
            left: 0;
            right: 0;
        }
        .hero-image2 img {
            width: 100%;  /* Full width of the container */
            height: auto;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)









if selected == "HOME":
    st.markdown(f"""
    <div class="hero-image2">
        <img src="data:image/png;base64,{img_base64}" />
    </div>
    """, unsafe_allow_html=True)

    st.header("  ")
    col1, col2 = st.columns(2)
    with col1:
        st.header("TOP 14 QUALIFIED TEAMS")
        data1 = pd.read_csv("data/results.csv")
        data2 = pd.read_csv("data/former_names.csv")
        data3 = pd.read_csv("data/goalscorers.csv")
        data4 = pd.read_csv("data/shootouts.csv")
        data1["home_team_agg"] = data1["home_score"] - data1["away_score"]
        data1["away_team_agg"] = data1["away_score"] - data1["home_score"]
        data1["total_score"] = data1["home_score"] + data1["away_score"]
        def func(x):
          if x > 0:
            return "Won"
          elif x < 0:
            return "Loss"
          else:
            return "Tied"
        data1["home_team_status"] = data1["home_team_agg"].apply(func)
        data1["away_team_status"] = data1["away_team_agg"].apply(func)
        data11_fq = data1[data1["tournament"] == 'FIFA World Cup qualification']
        data11_fq['date'] = pd.to_datetime(data11_fq['date'], dayfirst=True, errors='coerce')
        data11_fq["year"] = data11_fq['date'].dt.year
        data11_fq = data11_fq[data11_fq["year"] >= 2023]



        data11_fq_esp_home = data11_fq[(data11_fq['home_team'] == 'Spain')]
        esp_h_len = len(data11_fq_esp_home["home_team_status"])
        esp_h_win = len(data11_fq_esp_home[data11_fq_esp_home["home_team_status"] == "Won"])
        esp_h_win_per = int((esp_h_win/esp_h_len)*100)

        data11_fq_esp_away = data11_fq[(data11_fq['away_team'] == 'Spain')]
        esp_aw_len = len(data11_fq_esp_away["away_team_status"])
        esp_aw_win = len(data11_fq_esp_away[data11_fq_esp_away["away_team_status"] == "Won"])
        esp_aw_win_per = int((esp_aw_win/esp_aw_len)*100)

        esp_total_win_per = (esp_h_win_per + esp_aw_win_per)/2

        esp_match = len(data11_fq_esp_home["home_team_status"]) + len(data11_fq_esp_away["away_team_status"])

        data11_fq_arg_home = data11_fq[(data11_fq['home_team'] == 'Argentina')]
        arg__h_len = len(data11_fq_arg_home["home_team_status"])
        arg_h_win = len(data11_fq_arg_home[data11_fq_arg_home["home_team_status"] == "Won"])
        arg_h_win_per = int((arg_h_win/arg__h_len)*100)

        data11_fq_arg_away = data11_fq[(data11_fq['away_team'] == 'Argentina')]
        arg_aw_len = len(data11_fq_arg_away["away_team_status"])
        arg_aw_win = len(data11_fq_arg_away[data11_fq_arg_away["away_team_status"] == "Won"])
        arg_aw_win_per = int((arg_aw_win/arg_aw_len)*100)

        arg_total_win_per = (arg_h_win_per + arg_aw_win_per)/2

        arg_match = len(data11_fq_arg_home["home_team_status"]) + len(data11_fq_arg_away["away_team_status"])

        data11_fq_fra_home = data11_fq[(data11_fq['home_team'] == 'France')]
        fra__h_len = len(data11_fq_fra_home["home_team_status"])
        fra_h_win = len(data11_fq_fra_home[data11_fq_fra_home["home_team_status"] == "Won"])
        fra_h_win_per = int((fra_h_win/fra__h_len)*100)

        data11_fq_fra_away = data11_fq[(data11_fq['away_team'] == 'France')]
        fra_aw_len = len(data11_fq_fra_away["away_team_status"])
        fra_aw_win = len(data11_fq_fra_away[data11_fq_fra_away["away_team_status"] == "Won"])
        fra_aw_win_per = int((fra_aw_win/fra_aw_len)*100)

        fra_total_win_per = (fra_h_win_per + fra_aw_win_per)/2

        fra_match = len(data11_fq_fra_home["home_team_status"]) + len(data11_fq_fra_away["away_team_status"])

        data11_fq_eng_home = data11_fq[(data11_fq['home_team'] == 'England')]
        eng_h_len = len(data11_fq_eng_home["home_team_status"])
        eng_h_win = len(data11_fq_eng_home[data11_fq_eng_home["home_team_status"] == "Won"])
        eng_h_win_per = int((eng_h_win / eng_h_len) * 100)

        # === England (ENG) - Away performance ===
        data11_fq_eng_away = data11_fq[(data11_fq['away_team'] == 'England')]
        eng_aw_len = len(data11_fq_eng_away["away_team_status"])
        eng_aw_win = len(data11_fq_eng_away[data11_fq_eng_away["away_team_status"] == "Won"])
        eng_aw_win_per = int((eng_aw_win / eng_aw_len) * 100)

        # === Combined average win percentage ===
        eng_total_win_per = (eng_h_win_per + eng_aw_win_per) / 2

        eng_match = len(data11_fq_eng_home["home_team_status"]) + len(data11_fq_eng_away["away_team_status"])

        data11_fq_bra_home = data11_fq[(data11_fq['home_team'] == 'Brazil')]
        bra_h_len = len(data11_fq_bra_home["home_team_status"])
        bra_h_win = len(data11_fq_bra_home[data11_fq_bra_home["home_team_status"] == "Won"])
        bra_h_win_per = int((bra_h_win / bra_h_len) * 100)

        # For Brazil as AWAY team
        data11_fq_bra_away = data11_fq[(data11_fq['away_team'] == 'Brazil')]
        bra_aw_len = len(data11_fq_bra_away["away_team_status"])
        bra_aw_win = len(data11_fq_bra_away[data11_fq_bra_away["away_team_status"] == "Won"])
        bra_aw_win_per = int((bra_aw_win / bra_aw_len) * 100)

        # Average win percentage (home + away)
        bra_total_win_per = (bra_h_win_per + bra_aw_win_per) / 2

        bra_match = len(data11_fq_bra_home["home_team_status"]) + len(data11_fq_bra_away["away_team_status"])

        data11_fq_por_home = data11_fq[(data11_fq['home_team'] == 'Portugal')]
        por_h_len = len(data11_fq_por_home["home_team_status"])
        por_h_win = len(data11_fq_por_home[data11_fq_por_home["home_team_status"] == "Won"])
        por_h_win_per = int((por_h_win / por_h_len) * 100)

        # Portugal (POR) - Away matches
        data11_fq_por_away = data11_fq[(data11_fq['away_team'] == 'Portugal')]
        por_aw_len = len(data11_fq_por_away["away_team_status"])
        por_aw_win = len(data11_fq_por_away[data11_fq_por_away["away_team_status"] == "Won"])
        por_aw_win_per = int((por_aw_win / por_aw_len) * 100)

        # Overall win percentage (simple average of home and away)
        por_total_win_per = (por_h_win_per + por_aw_win_per) / 2

        por_match = len(data11_fq_por_home["home_team_status"]) + len(data11_fq_por_away["away_team_status"])

        data11_fq_ned_home = data11_fq[(data11_fq['home_team'] == 'Netherlands')]
        ned_h_len = len(data11_fq_ned_home["home_team_status"])
        ned_h_win = len(data11_fq_ned_home[data11_fq_ned_home["home_team_status"] == "Won"])
        ned_h_win_per = int((ned_h_win / ned_h_len) * 100)

        # Netherlands (NED) - Away matches
        data11_fq_ned_away = data11_fq[(data11_fq['away_team'] == 'Netherlands')]
        ned_aw_len = len(data11_fq_ned_away["away_team_status"])
        ned_aw_win = len(data11_fq_ned_away[data11_fq_ned_away["away_team_status"] == "Won"])
        ned_aw_win_per = int((ned_aw_win / ned_aw_len) * 100)

        # Average win percentage (home + away)
        ned_total_win_per = (ned_h_win_per + ned_aw_win_per) / 2

        ned_match = len(data11_fq_ned_home["home_team_status"]) + len(data11_fq_ned_away["away_team_status"])


        data11_fq_bel_home = data11_fq[(data11_fq['home_team'] == 'Belgium')]
        bel_h_len = len(data11_fq_bel_home["home_team_status"])
        bel_h_win = len(data11_fq_bel_home[data11_fq_bel_home["home_team_status"] == "Won"])
        bel_h_win_per = int((bel_h_win / bel_h_len) * 100)

        data11_fq_bel_away = data11_fq[(data11_fq['away_team'] == 'Belgium')]
        bel_aw_len = len(data11_fq_bel_away["away_team_status"])
        bel_aw_win = len(data11_fq_bel_away[data11_fq_bel_away["away_team_status"] == "Won"])
        bel_aw_win_per = int((bel_aw_win / bel_aw_len) * 100)

        bel_total_win_per = (bel_h_win_per + bel_aw_win_per) / 2

        bel_match = len(data11_fq_bel_home["home_team_status"]) + len(data11_fq_bel_away["away_team_status"])


        data11_fq_ger_home = data11_fq[(data11_fq['home_team'] == 'Germany')]
        ger_h_len = len(data11_fq_ger_home["home_team_status"])
        ger_h_win = len(data11_fq_ger_home[data11_fq_ger_home["home_team_status"] == "Won"])
        ger_h_win_per = int((ger_h_win / ger_h_len) * 100)

        # Filter for Germany as away team
        data11_fq_ger_away = data11_fq[(data11_fq['away_team'] == 'Germany')]
        ger_aw_len = len(data11_fq_ger_away["away_team_status"])
        ger_aw_win = len(data11_fq_ger_away[data11_fq_ger_away["away_team_status"] == "Won"])
        ger_aw_win_per = int((ger_aw_win / ger_aw_len) * 100)

        # Average win percentage (home + away)
        ger_total_win_per = (ger_h_win_per + ger_aw_win_per) / 2

        ger_match = len(data11_fq_ger_home["home_team_status"]) + len(data11_fq_ger_away["away_team_status"])


        data11_fq_cro_home = data11_fq[(data11_fq['home_team'] == 'Croatia')]
        cro_h_len = len(data11_fq_cro_home["home_team_status"])
        cro_h_win = len(data11_fq_cro_home[data11_fq_cro_home["home_team_status"] == "Won"])
        cro_h_win_per = int((cro_h_win / cro_h_len) * 100)

        # Filter for Croatia as away team
        data11_fq_cro_away = data11_fq[(data11_fq['away_team'] == 'Croatia')]
        cro_aw_len = len(data11_fq_cro_away["away_team_status"])
        cro_aw_win = len(data11_fq_cro_away[data11_fq_cro_away["away_team_status"] == "Won"])
        cro_aw_win_per = int((cro_aw_win / cro_aw_len) * 100)

        # Average win percentage (home + away)
        cro_total_win_per = (cro_h_win_per + cro_aw_win_per) / 2



        cro_match = len(data11_fq_cro_home["home_team_status"]) + len(data11_fq_cro_away["away_team_status"])


        data11_fq_mor_home = data11_fq[(data11_fq['home_team'] == 'Morocco')]
        mor_h_len = len(data11_fq_mor_home["home_team_status"])
        mor_h_win = len(data11_fq_mor_home[data11_fq_mor_home["home_team_status"] == "Won"])
        mor_h_win_per = int((mor_h_win / mor_h_len) * 100) if mor_h_len > 0 else 0

        # For Morocco as AWAY team
        data11_fq_mor_away = data11_fq[(data11_fq['away_team'] == 'Morocco')]
        mor_aw_len = len(data11_fq_mor_away["away_team_status"])
        mor_aw_win = len(data11_fq_mor_away[data11_fq_mor_away["away_team_status"] == "Won"])
        mor_aw_win_per = int((mor_aw_win / mor_aw_len) * 100) if mor_aw_len > 0 else 0

        # Average win percentage (home + away)
        mor_total_win_per = (mor_h_win_per + mor_aw_win_per) / 2


        mor_match = len(data11_fq_mor_home["home_team_status"]) + len(data11_fq_mor_away["away_team_status"])


        data11_fq_col_home = data11_fq[(data11_fq['home_team'] == 'Colombia')]
        col_h_len = len(data11_fq_col_home["home_team_status"])
        col_h_win = len(data11_fq_col_home[data11_fq_col_home["home_team_status"] == "Won"])
        col_h_win_per = int((col_h_win / col_h_len) * 100) if col_h_len > 0 else 0

        # Colombia - Away matches
        data11_fq_col_away = data11_fq[(data11_fq['away_team'] == 'Colombia')]
        col_aw_len = len(data11_fq_col_away["away_team_status"])
        col_aw_win = len(data11_fq_col_away[data11_fq_col_away["away_team_status"] == "Won"])
        col_aw_win_per = int((col_aw_win / col_aw_len) * 100) if col_aw_len > 0 else 0

        # Average win percentage (home + away)
        col_total_win_per = (col_h_win_per + col_aw_win_per) / 2


        col_match = len(data11_fq_col_home["home_team_status"]) + len(data11_fq_col_away["away_team_status"])


        data11_fq_uru_home = data11_fq[(data11_fq['home_team'] == 'Uruguay')]
        uru_h_len = len(data11_fq_uru_home["home_team_status"])
        uru_h_win = len(data11_fq_uru_home[data11_fq_uru_home["home_team_status"] == "Won"])
        uru_h_win_per = int((uru_h_win / uru_h_len) * 100)

        data11_fq_uru_away = data11_fq[(data11_fq['away_team'] == 'Uruguay')]
        uru_aw_len = len(data11_fq_uru_away["away_team_status"])
        uru_aw_win = len(data11_fq_uru_away[data11_fq_uru_away["away_team_status"] == "Won"])
        uru_aw_win_per = int((uru_aw_win / uru_aw_len) * 100)

        uru_total_win_per = (uru_h_win_per + uru_aw_win_per) / 2


        uru_match = len(data11_fq_uru_home["home_team_status"]) + len(data11_fq_uru_away["away_team_status"])


        data11_fq_sen_home = data11_fq[(data11_fq['home_team'] == 'Senegal')]
        sen_h_len = len(data11_fq_sen_home["home_team_status"])
        sen_h_win = len(data11_fq_sen_home[data11_fq_sen_home["home_team_status"] == "Won"])
        sen_h_win_per = int((sen_h_win / sen_h_len) * 100)

        data11_fq_sen_away = data11_fq[(data11_fq['away_team'] == 'Senegal')]
        sen_aw_len = len(data11_fq_sen_away["away_team_status"])
        sen_aw_win = len(data11_fq_sen_away[data11_fq_sen_away["away_team_status"] == "Won"])
        sen_aw_win_per = int((sen_aw_win / sen_aw_len) * 100)

        sen_total_win_per = (sen_h_win_per + sen_aw_win_per) / 2


        sen_match = len(data11_fq_sen_home["home_team_status"]) + len(data11_fq_sen_away["away_team_status"])


        win_rate = pd.DataFrame({
            'Country': ['Spain', 'Argentina', 'France', 'England', 'Brazil', 'Portugal', 'Netherlands', 'Belgium', 'Germany', 'Croatia', 'Morocco', 'Colombia', 'Uruguay', 'Senegal'],
            'Win_Rate': [esp_total_win_per, arg_total_win_per, fra_total_win_per, eng_total_win_per, bra_total_win_per, por_total_win_per, ned_total_win_per, bel_total_win_per, ger_total_win_per, cro_total_win_per, mor_total_win_per, col_total_win_per, uru_total_win_per, sen_total_win_per]
        })
        plot = px.bar(win_rate, x='Country', y='Win_Rate', 
                  color='Win_Rate',
                  color_continuous_scale=['#FFFF00', '#008000'])

        #win_rate = win_rate.sort_values(by='Win_Rate', ascending=False).reset_index(drop=True)

        country1_data1 = pd.DataFrame({
        "Country": win_rate["Country"],
        "Win_Rate": win_rate["Win_Rate"],
        "latitudes": [40.4637,
        -38.4161,
        46.2276,
        52.3555,
        -14.2350,
        39.3999,
        52.1326,
        50.5039,
        51.1657,
        45.1000,
        31.7917,
        4.5709,
        -32.5228,
        14.4974],

        "longitudes": [-3.7492,
        -63.6167,
        2.2137,
        -1.1743,
        -51.9253,
        -8.2245,
        5.2913,
        4.4699,
        10.4515,
        15.2000,
        -7.0926,
        -74.2973,
        -55.7658,
        -14.4524]})


        pred_min, pred_max = country1_data1["Win_Rate"].min(), country1_data1["Win_Rate"].max()
        country1_data1["color_r"] = ((country1_data1["Win_Rate"] - pred_min) / (pred_max - pred_min) * 255).astype(int)  # Red intensity
        country1_data1["color_g"] = (155 - country1_data1["color_r"]).astype(int)  # Green intensity
        country1_data1["color_b"] = 180  # Keep blue constant
        country1_data1["color_a"] = 230
        layer = pdk.Layer(
            "ColumnLayer",
            data=country1_data1,
            get_position=['longitudes','latitudes'],
            get_elevation = "Win_Rate",
            elevation_scale= 14800,
            radius=292000,
            get_fill_color=["color_r", "color_g", "color_b", "color_a"],
            #elevation_range="AQI",
            pickable=True,
            extruded=True,
            auto_highlight=True
        )
        vi = pdk.ViewState(latitude=country1_data1["latitudes"].mean(),longitude= country1_data1["longitudes"].mean(),zoom=4,pitch=30)
        xyz = pdk.Deck(layers=[layer],initial_view_state=vi)

        countries_matches = pd.DataFrame({
            'Country': ['Spain', 'Argentina', 'France', 'England', 'Brazil', 'Portugal', 'Netherlands', 'Belgium', 'Germany', 'Croatia', 'Morocco', 'Colombia', 'Uruguay', 'Senegal'],
            'Matches_Played': [esp_match, arg_match, fra_match, eng_match, bra_match, por_match, ned_match, bel_match, ger_match, cro_match, mor_match, col_match, uru_match, sen_match]
        })
        country2_data2 = pd.DataFrame({
        "Country": countries_matches["Country"],
        "Total_matches": countries_matches["Matches_Played"],
        "Win_Rate": win_rate["Win_Rate"],
        "latitudes": [40.4637,
        -38.4161,
        46.2276,
        52.3555,
        -14.2350,
        39.3999,
        52.1326,
        50.5039,
        51.1657,
        45.1000,
        31.7917,
        4.5709,
        -32.5228,
        14.4974],

        "longitudes": [-3.7492,
        -63.6167,
        2.2137,
        -1.1743,
        -51.9253,
        -8.2245,
        5.2913,
        4.4699,
        10.4515,
        15.2000,
        -7.0926,
        -74.2973,
        -55.7658,
        -14.4524]})
        plot2 = px.bar(country2_data2,x = 'Country',y = "Win_Rate",color='Total_matches',
                  color_continuous_scale=["#D9FF00", '#008000'])
        plot2.update_layout(height = 500,margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(plot2,use_container_width=False)
        st.write("Here win rates of the top 14 countries are stated along with the number of matches played by them in FIFA WC 2026 Qualifiers. The darker shades in the graph shows more number of matches played. South American teams have played the most matches, than of europe and african teams.")
        pred_min, pred_max = country2_data2["Total_matches"].min(), country2_data2["Total_matches"].max()
        country2_data2["color_r"] = ((country2_data2["Total_matches"] - pred_min) / (pred_max - pred_min) * 255).astype(int)  # Red intensity
        country2_data2["color_g"] = (155 - country2_data2["color_r"]).astype(int)  # Green intensity
        country2_data2["color_b"] = 180  # Keep blue constant
        country2_data2["color_a"] = 230
        layer = pdk.Layer(
            "ColumnLayer",
            data=country2_data2,
            get_position=['longitudes','latitudes'],
            get_elevation = "Total_matches",
            elevation_scale= 84800,
            radius=292000,
            get_fill_color=["color_r", "color_g", "color_b", "color_a"],
            #elevation_range="AQI",
            pickable=True,
            extruded=True,
            auto_highlight=True 
        )
        vi = pdk.ViewState(latitude=country2_data2["latitudes"].mean(),longitude= country2_data2["longitudes"].mean(),zoom=4,pitch=30)
        xyz1 = pdk.Deck(layers=[layer],initial_view_state=vi)
    fifa_score = pd.read_csv("data/fifa_2014-2022_scorers.csv")

    with col2:
        st.header("WORLD CUP INSIGHTS")
        st.markdown("""
        <style>
        /* Style the selectbox label */
        .stSelectbox label {
            color: #FFFFFF !important;
            font-size: 18px !important;
            font-weight: bold !important;
        }
        
        /* Style the selectbox container*/
        div[data-baseweb="select"] > div {
            background-color: #008000 !important;
          
        }
                    
        /* Target the select widget container */
        .stSelectbox div[data-baseweb="select"] {
            background-color: #008000 !important;
            border-radius: 10px !important;
            border: 2px solid #4CAF50 !important;
        }            
        
        /* Style the selected value */
        .stSelectbox div[data-baseweb="select"] div {
            font-weight: bold !important;
            font-size: 16px !important;
        }
        
        /* Style dropdown menu items */
        div[role="listbox"] div {
            background-color: #e8f5e9 !important;
            color: #1B5E20 !important;
            font-size: 14px !important;
        }
        
        /* The actual list item Streamlit renders */
    li[role="option"]:hover {
        background-color: #008000 !important;
        color: white !important;
    }
        

        </style>
    """, unsafe_allow_html=True)
        st.markdown("""
        <style>
        /* This will highlight dropdown options in red - helps identify the right selector */
        div[role="option"] {
            background-color: red !important;
        }
        </style>
    """, unsafe_allow_html=True)

        drop = st.selectbox(label="Year",options=["2014","2018","2022"])
        if drop == "2014":
            col3, col4 = st.columns(2)

            fifa_score['Date'] = pd.to_datetime(fifa_score['Date'], dayfirst=True, errors='coerce')
            fifa_score['year'] = fifa_score['Date'].dt.year
            fifa_score_14 = fifa_score[fifa_score["year"] == 2014]
            
            a = fifa_score_14["Scored team"].value_counts()
            a1 = pd.DataFrame({"country":a.index,"goals":a.values})
            countries_scored_14 = pd.DataFrame({
                'country': a1["country"],
                'goals': a1["goals"],
            "latitudes": [
                52.520008,    # Berlin, Germany
                52.367573,    # Amsterdam, Netherlands
                4.7110,      # Bogotá, Colombia
              -15.793889,    # Brasília, Brazil
                48.856614,    # Paris, France
              -34.603722,    # Buenos Aires, Argentina
                36.737232,    # Algiers, Algeria
                46.948090,    # Bern, Switzerland
              -33.448890,    # Santiago, Chile
                45.815010,    # Zagreb, Croatia
                50.850450,    # Brussels, Belgium
                38.907192,    # Washington, D.C., United States
                9.928069,    # San José, Costa Rica
                19.432608,    # Mexico City, Mexico
                43.856259,    # Sarajevo, Bosnia and Herzegovina
                40.416775,    # Madrid, Spain
              -34.901113,    # Montevideo, Uruguay
                6.827623,    # Yamoussoukro, Ivory Coast (official capital)
                5.603717,    # Accra, Ghana
                38.722252,    # Lisbon, Portugal
                -0.180653,    # Quito, Ecuador
                37.566535,    # Seoul, South Korea
                37.983810,    # Athens, Greece
              -35.280937,    # Canberra, Australia
                9.057850,    # Abuja, Nigeria
                51.507351,    # London, England (United Kingdom)
                35.689487,    # Tokyo, Japan
                41.902782,    # Rome, Italy
                55.755826,    # Moscow, Russia
                14.072275,    # Tegucigalpa, Honduras
                3.848033,    # Yaoundé, Cameroon
                35.689197,    # Tehran, Iran
            ],

            "longitudes": [
                13.404954,    # Berlin
                  4.904139,    # Amsterdam
                -74.072092,    # Bogotá
                -47.882778,    # Brasília
                  2.352222,    # Paris
                -58.381592,    # Buenos Aires
                  3.086472,    # Algiers
                  7.447447,    # Bern
                -70.669265,    # Santiago
                15.981919,    # Zagreb
                  4.348780,    # Brussels
                -77.036871,    # Washington, D.C.
                -84.090725,    # San José
                -99.133209,    # Mexico City
                18.413076,    # Sarajevo
                -3.703790,     # Madrid
                -56.164532,    # Montevideo
                -5.289344,    # Yamoussoukro
                  0.187000,    # Accra
                -9.139337,    # Lisbon
                -78.467834,    # Quito
                126.977969,    # Seoul
                23.727539,    # Athens
                149.130009,    # Canberra
                  7.495080,    # Abuja
                -0.127758,    # London
                139.691711,    # Tokyo
                12.496366,    # Rome
                37.617300,    # Moscow
                -87.192070,    # Tegucigalpa
                11.502075,    # Yaoundé
                51.388973     # Tehran
            ]})
            pred_min, pred_max = countries_scored_14["goals"].min(), countries_scored_14["goals"].max()
            countries_scored_14["color_r"] = ((countries_scored_14["goals"] - pred_min) / (pred_max - pred_min) * 255).astype(int)  # Red intensity
            countries_scored_14["color_g"] = (155 - countries_scored_14["color_r"]).astype(int)  # Green intensity
            countries_scored_14["color_b"] = 180  # Keep blue constant
            countries_scored_14["color_a"] = 230
            layer = pdk.Layer(
                "ColumnLayer",
                data=countries_scored_14,
                get_position=['longitudes','latitudes'],
                get_elevation = "goals",
                elevation_scale= 84800,
                radius = 90000,
                get_fill_color=["color_r", "color_g", "color_b", "color_a"],
                #elevation_range="AQI",
                pickable=True,
                extruded=True,
                auto_highlight=True
            )
            vi = pdk.ViewState(latitude=countries_scored_14["latitudes"].mean(),longitude= countries_scored_14["longitudes"].mean(),zoom=4,pitch=30)
            xyz2 = pdk.Deck(layers=[layer],initial_view_state=vi)
            xyz2.to_html("pred_map.html")
            fifa_14_own_goal = fifa_score_14[fifa_score_14["Own goal"] == True]
            fifa_score_14_only_goal = fifa_score_14.copy()
            country = []
            for i in fifa_score_14_only_goal["Scored team"]:
              country.append(i)
            country1 = list(set(country))
            # AFC (Asian Football Confederation – Asia)
            afc = [
                'Australia',
                'Iran',
                'Japan',
                'South Korea'
            ]

            # CAF (Confédération Africaine de Football – Africa)
            caf = [
                'Algeria',
                'Cameroon',
                'Ghana',
                'Ivory Coast',
                'Nigeria'
            ]

            # CONCACAF (North, Central America and Caribbean)
            concacaf = [
                'Costa Rica',
                'Honduras',
                'Mexico',
                'United States'
            ]

            # CONMEBOL (South America)
            conmebol = [
                'Argentina',
                'Brazil',
                'Chile',
                'Colombia',
                'Ecuador',
                'Uruguay'
            ]

            # UEFA (Europe)
            uefa = [
                'Belgium',
                'Bosnia and Herzegovina',
                'Croatia',
                'England',
                'France',
                'Germany',
                'Greece',
                'Italy',
                'Netherlands',
                'Portugal',
                'Russia',
                'Spain',
                'Switzerland'
            ]
            fifa_rankings_july_2014 = {
                'Switzerland': 8,
                'Algeria': 36,
                'Japan': 47,
                'Mexico': 19,
                'Portugal': 3,
                'Chile': 14,
                'Germany': 2,
                'Argentina': 6,
                'Iran': 37,
                'Uruguay': 5,
                'England': 11,
                'Netherlands': 15,
                'Cameroon': 50,
                'Ghana': 43,  # Approximate from consistent sources; exact CAF/April 2014 placement
                'Belgium': 12,
                'Australia': 59,
                'Honduras': 33,  # From May close but April consistent around 33
                'Italy': 9,
                'Costa Rica': 34,
                'Spain': 1,
                'South Korea': 57,  # Consistent with AFC rankings
                'Croatia': 18,
                'Bosnia and Herzegovina': 25,
                'Ecuador': 26,
                'Russia': 22,
                'United States': 13,
                'Colombia': 4,
                'Nigeria': 44,
                'Greece': 10,
                'Brazil': 6,  # Tied at 6 with Argentina in some lists, but exact placement 6
                'Ivory Coast': 21,
                'France': 16
            }
            def rank(team_name):
              return fifa_rankings_july_2014.get(team_name, 0)
            fifa_score_14_only_goal["rank"] = fifa_score_14_only_goal["Scored team"].apply(rank)
            def get_continent(team_name):
              if team_name in afc:
                return "AFC"
              elif team_name in caf:
                return "CAF"
              elif team_name in concacaf:
                return "CONCACAF"
              elif team_name in conmebol:
                return "CONMEBOL"
              elif team_name in uefa:
                return "UEFA"
              else:
                return "Other" # Handle cases where a team might not be in any defined list

            fifa_score_14_only_goal["Continent"] = fifa_score_14_only_goal["Scored team"].apply(get_continent)
            def home_res(row):
              if row['Home team'] == row['Scored team']:
                return True
              else:
                return False
            def away_res(row):
              if row['Away team'] == row['Scored team']:
                return True
              else:
                return False
            fifa_score_14_only_goal["Home_res"] = fifa_score_14_only_goal.apply(home_res, axis=1)
            fifa_score_14_only_goal["Away_res"] = fifa_score_14_only_goal.apply(away_res, axis=1)



            home_score = fifa_score_14_only_goal.groupby(['Date', 'Scored team','rank'])['Away_res'].count()
            temp_df = home_score.reset_index()
            home_score1 = pd.DataFrame({"Date":temp_df["Date"],"Scored_team":temp_df["Scored team"],"goals":temp_df["Away_res"],"rank":temp_df["rank"]})
            cc = fifa_score_14_only_goal["Continent"].value_counts()
            continent = pd.DataFrame({"continent":cc.index,"goals":cc.values})
            import plotly.express as px
            pie = px.pie(continent, values='goals', names='continent', title='Continent Goals', 
                  color='goals',
                  color_discrete_sequence=["#ABEFA1", '#008000', "#82E1A9", '#006400',"#5FE85F"])
            ss = fifa_score_14_only_goal['Player'].value_counts()
            player_scores = pd.DataFrame({"player":ss.index,"goals":ss.values})
            ff14 = fifa_score_14_only_goal['Scored team'].value_counts()
            fifa_14_scored = pd.DataFrame({"country":ff14.index,"goals":ff14.values})
            scored_country_14 = pd.DataFrame({
            "country": fifa_14_scored["country"],
            "goals": fifa_14_scored["goals"],

            "latitudes": [
                52.5200,     # Berlin, Germany
                52.3676,     # Amsterdam, Netherlands
                4.7110,     # Bogotá, Colombia
              -15.7939,     # Brasília, Brazil
                48.8566,     # Paris, France
              -34.6037,     # Buenos Aires, Argentina
                46.9480,     # Bern, Switzerland
                36.7525,     # Algiers, Algeria
                50.8503,     # Brussels, Belgium
              -33.4489,     # Santiago, Chile
                45.8150,     # Zagreb, Croatia
                38.9072,     # Washington, D.C., United States
                19.4326,     # Mexico City, Mexico
                9.9281,     # San José, Costa Rica
                6.8276,     # Yamoussoukro, Ivory Coast (official capital)
                43.8563,     # Sarajevo, Bosnia and Herzegovina
              -34.9011,     # Montevideo, Uruguay
                40.4168,     # Madrid, Spain
                5.6037,     # Accra, Ghana
              -35.2809,     # Canberra, Australia
                37.5665,     # Seoul, South Korea
                9.0579,     # Abuja, Nigeria
                37.9838,     # Athens, Greece
                -0.1807,     # Quito, Ecuador
                38.7223,     # Lisbon, Portugal
                35.6762,     # Tokyo, Japan
                41.9028,     # Rome, Italy
                51.5074,     # London, England (United Kingdom)
                55.7558,     # Moscow, Russia
                14.0723,     # Tegucigalpa, Honduras
                3.8480,     # Yaoundé, Cameroon
                35.6892      # Tehran, Iran
            ],

            "longitudes": [
                13.4050,     # Berlin
                4.9041,     # Amsterdam
              -74.0721,     # Bogotá
              -47.8825,     # Brasília
                2.3522,     # Paris
              -58.3816,     # Buenos Aires
                7.4474,     # Bern
                3.0420,     # Algiers
                4.3517,     # Brussels
              -70.6693,     # Santiago
                15.9819,     # Zagreb
              -77.0369,     # Washington, D.C.
              -99.1332,     # Mexico City
              -84.0907,     # San José
                -5.2893,     # Yamoussoukro
                18.4131,     # Sarajevo
              -56.1645,     # Montevideo
                -3.7038,     # Madrid
                -0.1870,     # Accra
              149.1300,     # Canberra
              126.9780,     # Seoul
                7.4951,     # Abuja
                23.7275,     # Athens
              -78.4678,     # Quito
                -9.1393,     # Lisbon
              139.6503,     # Tokyo
                12.4964,     # Rome
                -0.1278,     # London
                37.6173,     # Moscow
              -87.1928,     # Tegucigalpa
                11.5021,     # Yaoundé
                51.3890      # Tehran
            ]})
            pred_min, pred_max = scored_country_14["goals"].min(), scored_country_14["goals"].max()
            scored_country_14["color_r"] = ((scored_country_14["goals"] - pred_min) / (pred_max - pred_min) * 255).astype(int)  # Red intensity
            scored_country_14["color_g"] = (155 - scored_country_14["color_r"]).astype(int)  # Green intensity
            scored_country_14["color_b"] = 180  # Keep blue constant
            scored_country_14["color_a"] = 230
            layer = pdk.Layer(
                "ColumnLayer",
                data=scored_country_14,
                get_position=['longitudes','latitudes'],
                get_elevation = "goals",
                elevation_scale= 84800,
                radius = 90000,
                get_fill_color=["color_r", "color_g", "color_b", "color_a"],
                #elevation_range="AQI",
                pickable=True,
                extruded=True,
                auto_highlight=True
            )
            vi = pdk.ViewState(latitude=scored_country_14["latitudes"].mean(),longitude= scored_country_14["longitudes"].mean(),zoom=4,pitch=30)
            xyz3 = pdk.Deck(layers=[layer],initial_view_state=vi)
            # {"Country": "{country}\nGoals: {goals}"}
            xyz3.to_html("pred_map.html")
            ps = fifa_score_14_only_goal["Position"].value_counts()
            position_score = pd.DataFrame({"position":ps.index,"goals":ps.values})
            import matplotlib.pyplot as plt
            import plotly.express as px
            bar = px.area(position_score, x="position", y="goals",title='Position wise Goals',color_discrete_sequence=['green'])
            with col3:
              st.subheader("Goals scored")
              st.pydeck_chart(xyz3)
            with col4:
              pie.update_layout(height=250,margin=dict(t=60, b=0, l=0, r=0))
              st.plotly_chart(pie,use_container_width=False)
              bar.update_layout(height = 300,margin=dict(t=90, b=0, l=0, r=0))
              st.plotly_chart(bar,use_container_width=False)
        if drop == "2018":
            col6, col7 = st.columns(2)
            fifa_score['Date'] = pd.to_datetime(fifa_score['Date'], dayfirst=True, errors='coerce')
            fifa_score['year'] = fifa_score['Date'].dt.year
            fifa_score_18 = fifa_score[fifa_score["year"] == 2018]
            fifa_score_18["Minute"].mean()
            ff = fifa_score_18["Scored team"].value_counts()
            fifa_18_scored = pd.DataFrame({"country":ff.index,"goals":ff.values})
            scored_country_18 = pd.DataFrame({
            "country": fifa_18_scored["country"],
            "goals": fifa_18_scored["goals"],
            "latitudes":[
                50.8503,     # Brussels, Belgium
                45.8150,     # Zagreb, Croatia
                48.8566,     # Paris, France
                51.5074,     # London, England (United Kingdom)
                55.7558,     # Moscow, Russia
                -15.7939,    # Brasília, Brazil
                -34.9011,    # Montevideo, Uruguay
                40.4168,     # Madrid, Spain
                38.7223,     # Lisbon, Portugal
                35.6762,     # Tokyo, Japan
                59.3293,     # Stockholm, Sweden
                -34.6037,    # Buenos Aires, Argentina
                4.7110,      # Bogotá, Colombia
                46.9480,     # Bern, Switzerland
                36.8065,     # Tunis, Tunisia
                14.6937,     # Dakar, Senegal
                55.6761,     # Copenhagen, Denmark
                19.4326,     # Mexico City, Mexico
                37.5665,     # Seoul, South Korea
                9.0579,      # Abuja, Nigeria
                44.7866,     # Belgrade, Serbia
                -35.2809,    # Canberra, Australia
                35.6892,     # Tehran, Iran
                64.1466,     # Reykjavík, Iceland
                30.0444,     # Cairo, Egypt
                52.2297,     # Warsaw, Poland
                52.5200,     # Berlin, Germany
                8.9833,      # Panama City, Panama
                24.7136,     # Riyadh, Saudi Arabia
                34.0209,     # Rabat, Morocco
                -12.0464,    # Lima, Peru
                9.9281       # San José, Costa Rica
            ],

            "longitudes": [
                4.3517,     # Brussels
                15.9819,     # Zagreb
                2.3522,     # Paris
                -0.1278,     # London
                37.6173,     # Moscow
              -47.8828,     # Brasília
              -56.1645,     # Montevideo
                -3.7038,     # Madrid
                -9.1393,     # Lisbon
              139.6503,     # Tokyo
                18.0686,     # Stockholm
              -58.3816,     # Buenos Aires
              -74.0721,     # Bogotá
                7.4474,     # Bern
                10.1815,     # Tunis
              -17.4441,     # Dakar
                12.5683,     # Copenhagen
              -99.1332,     # Mexico City
              126.9780,     # Seoul
                7.4951,     # Abuja
                20.4489,     # Belgrade
              149.1310,     # Canberra
                51.3890,     # Tehran
              -21.9426,     # Reykjavík
                31.2357,     # Cairo
                21.0122,     # Warsaw
                13.4050,     # Berlin
              -79.5197,     # Panama City
                46.6753,     # Riyadh
                -6.8416,     # Rabat
              -77.0428,     # Lima
              -84.0908      # San José
            ]})
            pred_min, pred_max = scored_country_18["goals"].min(), scored_country_18["goals"].max()
            scored_country_18["color_r"] = ((scored_country_18["goals"] - pred_min) / (pred_max - pred_min) * 255).astype(int)  # Red intensity
            scored_country_18["color_g"] = (155 - scored_country_18["color_r"]).astype(int)  # Green intensity
            scored_country_18["color_b"] = 180  # Keep blue constant
            scored_country_18["color_a"] = 230
            layer = pdk.Layer(
                "ColumnLayer",
                data=scored_country_18,
                get_position=['longitudes','latitudes'],
                get_elevation = "goals",
                elevation_scale= 84800,
                radius = 90000,
                get_fill_color=["color_r", "color_g", "color_b", "color_a"],
                #elevation_range="AQI",
                pickable=True,
                extruded=True,
                auto_highlight=True
            )
            vi = pdk.ViewState(latitude=scored_country_18["latitudes"].mean(),longitude= scored_country_18["longitudes"].mean(),zoom=4,pitch=30)
            xyz4 = pdk.Deck(layers=[layer],initial_view_state=vi)
            xyz4.to_html("pred_map.html")
            fifa_18_own_goal = fifa_score_18[fifa_score_18["Own goal"] == True]
            fifa_score_18_only_goal = fifa_score_18.copy()
            country2 = []
            for i in fifa_score_18_only_goal["Scored team"]:
              country2.append(i)
            country3 = list(set(country2))
            africa = [
                'Nigeria',
                'Morocco',
                'Egypt',
                'Senegal',
                'Tunisia'
            ]

            asia = [
                'Saudi Arabia',
                'Iran',
                'South Korea',
                'Australia',      # AFC member in football
                'Japan'
            ]

            europe = [
                'Croatia',
                'Portugal',
                'Spain',
                'Denmark',
                'Belgium',
                'Iceland',
                'Germany',
                'England',
                'Sweden',
                'Poland',
                'Russia',
                'Switzerland',
                'Serbia',
                'France'
            ]

            north_america = [
                'Panama',
                'Costa Rica',
                'Mexico'
            ]

            south_america = [
                'Uruguay',
                'Colombia',
                'Peru',
                'Brazil',
                'Argentina'
            ]

            # Countries not present in the list but worth noting for context:
            # Oceania → none in your list (Australia is classified under Asia/AFC in football)
            fifa_rankings_june_2018 = {
                'Russia': 70,
                'Spain': 10,
                'Senegal': 27,
                'Saudi Arabia': 67,
                'Costa Rica': 31,
                'Nigeria': 48,
                'Iceland': 22,
                'Argentina': 5,
                'Peru': 11,
                'Australia': 36,
                'Belgium': 3,
                'Mexico': 15,
                'Sweden': 24,
                'Iran': 37,
                'Serbia': 35,
                'Colombia': 16,
                'Brazil': 2,
                'South Korea': 57,
                'Portugal': 4,
                'England': 12,
                'Tunisia': 21,
                'Croatia': 20,
                'Uruguay': 14,
                'Japan': 61,
                'Egypt': 45,
                'Poland': 8,
                'France': 7,
                'Switzerland': 6,
                'Germany': 1,
                'Panama': 55,
                'Denmark': 12,   # Tied with England at 12
                'Morocco': 41
            }
            def rank(team_name):
              return fifa_rankings_june_2018.get(team_name, 0)
            fifa_score_18_only_goal["rank"] = fifa_score_18_only_goal["Scored team"].apply(rank)
            def get_continent(team_name):
              if team_name in asia:
                return "AFC"
              elif team_name in africa:
                return "CAF"
              elif team_name in south_america:
                return "CONCACAF"
              elif team_name in north_america:
                return "CONMEBOL"
              elif team_name in europe:
                return "UEFA"
              else:
                return "Other" # Handle cases where a team might not be in any defined list

            fifa_score_18_only_goal["Continent"] = fifa_score_18_only_goal["Scored team"].apply(get_continent)
            def home_res(row):
              if row['Home team'] == row['Scored team']:
                return True
              else:
                return False
            def away_res(row):
              if row['Away team'] == row['Scored team']:
                return True
              else:
                return False
            fifa_score_18_only_goal["Home_res"] = fifa_score_18_only_goal.apply(home_res, axis=1)
            fifa_score_18_only_goal["Away_res"] = fifa_score_18_only_goal.apply(away_res, axis=1)
            home_score10 = fifa_score_18_only_goal.groupby(['Date', 'Scored team','rank'])['Away_res'].count()
            temp_df1 = home_score10.reset_index()
            home_score12 = pd.DataFrame({"Date":temp_df1["Date"],"Scored_team":temp_df1["Scored team"],"goals":temp_df1["Away_res"],"rank":temp_df1["rank"]})
            sg = fifa_score_18_only_goal['Scored team'].value_counts()
            sg1 = pd.DataFrame({"country":sg.index,"goals":sg.values})
            true_goals_18 = pd.DataFrame({
            "country": sg1["country"],
            "goals": sg1["goals"],

            "latitudes": [
                50.8503,    # Brussels, Belgium
                45.8150,    # Zagreb, Croatia
                48.8566,    # Paris, France
                51.5074,    # London, England (United Kingdom)
                55.7558,    # Moscow, Russia
              -15.7939,    # Brasília, Brazil
                40.4168,    # Madrid, Spain
                38.7223,    # Lisbon, Portugal
              -34.6037,    # Buenos Aires, Argentina
                4.7110,    # Bogotá, Colombia
                35.6762,    # Tokyo, Japan
              -34.9011,    # Montevideo, Uruguay
                36.8065,    # Tunis, Tunisia
                59.3293,    # Stockholm, Sweden
                46.9480,    # Bern, Switzerland
                19.4326,    # Mexico City, Mexico
                14.7167,    # Dakar, Senegal
                9.0579,    # Abuja, Nigeria
                37.5665,    # Seoul, South Korea
                55.6761,    # Copenhagen, Denmark
                44.7866,    # Belgrade, Serbia
              -35.2809,    # Canberra, Australia
                64.1466,    # Reykjavík, Iceland
                52.2297,    # Warsaw, Poland
                30.0444,    # Cairo, Egypt
                52.5200,    # Berlin, Germany
                34.0209,    # Rabat, Morocco
                24.7136,    # Riyadh, Saudi Arabia
              -12.0464,    # Lima, Peru
                8.9833,    # Panama City, Panama
                35.6892,    # Tehran, Iran
                9.9281     # San José, Costa Rica
            ],

            "longitudes": [
                4.3517,    # Brussels
                15.9819,    # Zagreb
                2.3522,    # Paris
                -0.1278,    # London
                37.6173,    # Moscow
              -47.8828,    # Brasília
                -3.7038,    # Madrid
                -9.1393,    # Lisbon
              -58.3816,    # Buenos Aires
              -74.0721,    # Bogotá
              139.6503,    # Tokyo
              -56.1645,    # Montevideo
                10.1815,    # Tunis
                18.0686,    # Stockholm
                7.4474,    # Bern
              -99.1332,    # Mexico City
              -17.4677,    # Dakar
                7.4951,    # Abuja
              126.9780,    # Seoul
                12.5683,    # Copenhagen
                20.4489,    # Belgrade
              149.1300,    # Canberra
              -21.9426,    # Reykjavík
                21.0122,    # Warsaw
                31.2357,    # Cairo
                13.4050,    # Berlin
                -6.8416,    # Rabat
                46.6753,    # Riyadh
              -77.0428,    # Lima
              -79.5199,    # Panama City
                51.3890,    # Tehran
              -84.0907     # San José
            ]})
            pred_min, pred_max = true_goals_18["goals"].min(), true_goals_18["goals"].max()
            true_goals_18["color_r"] = ((true_goals_18["goals"] - pred_min) / (pred_max - pred_min) * 255).astype(int)  # Red intensity
            true_goals_18["color_g"] = (155 - true_goals_18["color_r"]).astype(int)  # Green intensity
            true_goals_18["color_b"] = 180  # Keep blue constant
            true_goals_18["color_a"] = 230
            layer = pdk.Layer(
                "ColumnLayer",
                data=true_goals_18,
                get_position=['longitudes','latitudes'],
                get_elevation = "goals",
                elevation_scale= 84800,
                radius = 90000,
                get_fill_color=["color_r", "color_g", "color_b", "color_a"],
                #elevation_range="AQI",
                pickable=True,
                extruded=True,
                auto_highlight=True
            )
            vi = pdk.ViewState(latitude=true_goals_18["latitudes"].mean(),longitude= true_goals_18["longitudes"].mean(),zoom=4,pitch=30)
            xyz5 = pdk.Deck(layers=[layer],initial_view_state=vi)
            xyz5.to_html("pred_map.html")
            
            cc1 = fifa_score_18_only_goal["Continent"].value_counts()
            continent1 = pd.DataFrame({"continent":cc1.index,"goals":cc1.values})
            pie1 = px.pie(continent1, values='goals', names='continent', title='Continent Goals', 
                  color='goals',
                  color_discrete_sequence=["#ABEFA1", '#008000', "#82E1A9", '#006400',"#5FE85F"])
            
            ps1 = fifa_score_18_only_goal["Position"].value_counts()
            position1 = pd.DataFrame({"position":ps1.index,"goals":ps1.values})
            bar1 = px.area(position1, x="position", y="goals",color_discrete_sequence=['green'])
            with col6:
              st.subheader("Goals scored")
              xyz5
            with col7:
              pie1.update_layout(height=250,margin=dict(t=60, b=0, l=0, r=0))
              st.plotly_chart(pie1,use_container_width=False)
              bar1.update_layout(height = 300,margin=dict(t=90, b=0, l=0, r=0))
              st.plotly_chart(bar1,use_container_width=False)
        if drop == "2022":
            col8, col9 = st.columns(2)
            fifa_score['Date'] = pd.to_datetime(fifa_score['Date'], dayfirst=True, errors='coerce')
            fifa_score['year'] = fifa_score['Date'].dt.year
            fifa_score_22 = fifa_score[fifa_score["year"] == 2022]
            fifa_score_22["Minute"].mean()
            ff22 = fifa_score_22["Scored team"].value_counts()
            fifa_22_scored = pd.DataFrame({"country":ff22.index,"goals":ff22.values})
            scored_country_22 = pd.DataFrame({
            "country": fifa_22_scored["country"],
            "goals": fifa_22_scored["goals"],
            "latitudes": [
                48.8566,     # Paris, France
                -34.6037,    # Buenos Aires, Argentina
                51.5074,     # London, England (United Kingdom)
                38.7223,     # Lisbon, Portugal
                52.3676,     # Amsterdam, Netherlands
                40.4168,     # Madrid, Spain
                -15.7939,    # Brasília, Brazil
                45.8150,     # Zagreb, Croatia
                34.0209,     # Rabat, Morocco
                52.5200,     # Berlin, Germany
                35.6762,     # Tokyo, Japan
                46.9480,     # Bern, Switzerland
                5.6037,      # Accra, Ghana
                14.7167,     # Dakar, Senegal
                37.5665,     # Seoul, South Korea
                44.7866,     # Belgrade, Serbia
                35.6892,     # Tehran, Iran
                -35.2809,    # Canberra, Australia
                -0.1807,     # Quito, Ecuador
                3.8480,      # Yaoundé, Cameroon
                9.9281,      # San José, Costa Rica
                52.2297,     # Warsaw, Poland
                24.7136,     # Riyadh, Saudi Arabia
                38.9072,     # Washington, D.C., United States
                -34.9011,    # Montevideo, Uruguay
                19.4326,     # Mexico City, Mexico
                45.4215,     # Ottawa, Canada
                51.4816,     # Cardiff, Wales (United Kingdom)
                50.8503,     # Brussels, Belgium
                25.2769,     # Doha, Qatar
                55.6761,     # Copenhagen, Denmark
                36.8065      # Tunis, Tunisia
            ],

            "longitudes": [
                2.3522,     # Paris
                -58.3816,    # Buenos Aires
                -0.1278,    # London
                -9.1393,    # Lisbon
                4.9041,     # Amsterdam
                -3.7038,    # Madrid
                -47.8828,    # Brasília
                15.9819,     # Zagreb
                -6.8416,     # Rabat
                13.4050,     # Berlin
              139.6503,     # Tokyo
                7.4474,     # Bern
                -0.1870,     # Accra
              -17.4677,     # Dakar
              126.9780,     # Seoul
                20.4489,     # Belgrade
                51.3889,     # Tehran
              149.1300,     # Canberra
              -78.4678,     # Quito
                11.5021,     # Yaoundé
              -84.0907,     # San José
                21.0122,     # Warsaw
                46.6753,     # Riyadh
              -77.0369,     # Washington, D.C.
              -56.1645,     # Montevideo
              -99.1332,     # Mexico City
              -75.6972,     # Ottawa
                -3.1791,     # Cardiff
                4.3517,     # Brussels
                51.5200,     # Doha
                12.5683,     # Copenhagen
                10.1815      # Tunis
            ]})
            pred_min, pred_max = scored_country_22["goals"].min(), scored_country_22["goals"].max()
            scored_country_22["color_r"] = ((scored_country_22["goals"] - pred_min) / (pred_max - pred_min) * 255).astype(int)  # Red intensity
            scored_country_22["color_g"] = (155 - scored_country_22["color_r"]).astype(int)  # Green intensity
            scored_country_22["color_b"] = 180  # Keep blue constant
            scored_country_22["color_a"] = 230
            layer = pdk.Layer(
                "ColumnLayer",
                data=scored_country_22,
                get_position=['longitudes','latitudes'],
                get_elevation = "goals",
                elevation_scale= 84800,
                radius = 90000,
                get_fill_color=["color_r", "color_g", "color_b", "color_a"],
                #elevation_range="AQI",
                pickable=True,
                extruded=True,
                auto_highlight=True
            )
            vi = pdk.ViewState(latitude=scored_country_22["latitudes"].mean(),longitude= scored_country_22["longitudes"].mean(),zoom=4,pitch=30)
            xyz5 = pdk.Deck(layers=[layer],initial_view_state=vi)
            xyz5.to_html("pred_map.html")
            fifa_score_22["Position"].value_counts()
            fifa_22_own_goal = fifa_score_22[fifa_score_22["Own goal"] == True]
            fifa_score_22_only_goal = fifa_score_22.copy()
            sg10 = fifa_score_22_only_goal['Scored team'].value_counts()
            sg11 = pd.DataFrame({"country":sg10.index,"goals":sg10.values})
            true_goals_22 = pd.DataFrame({
            "country": sg11["country"],
            "goals": sg11["goals"],

            "latitudes": [
                48.8566,     # Paris, France
                -34.6037,    # Buenos Aires, Argentina
                51.5074,     # London, England
                38.7223,     # Lisbon, Portugal
                52.3676,     # Amsterdam, Netherlands
                40.4168,     # Madrid, Spain
                -15.7939,    # Brasília, Brazil
                45.8150,     # Zagreb, Croatia
                34.0209,     # Rabat, Morocco
                52.5200,     # Berlin, Germany
                35.6762,     # Tokyo, Japan
                46.9481,     # Bern, Switzerland
                5.6037,      # Accra, Ghana
                14.7167,     # Dakar, Senegal
                37.5665,     # Seoul, South Korea
                44.7866,     # Belgrade, Serbia
                -0.1807,     # Quito, Ecuador
                35.6892,     # Tehran, Iran
                3.8480,      # Yaoundé, Cameroon
                9.9281,      # San José, Costa Rica
                38.9072,     # Washington, D.C., United States
                52.2297,     # Warsaw, Poland
                24.7136,     # Riyadh, Saudi Arabia
                -35.2809,    # Canberra, Australia
                -34.9011,    # Montevideo, Uruguay
                19.4326,     # Mexico City, Mexico
                50.8503,     # Brussels, Belgium
                51.4816,     # Cardiff, Wales
                45.4215,     # Ottawa, Canada
                55.6761,     # Copenhagen, Denmark
                25.2854,     # Doha, Qatar
                36.8065      # Tunis, Tunisia
            ],

            "longitudes": [
                2.3522,     # Paris
                -58.3816,    # Buenos Aires
                0.1278,     # London
                9.1393,     # Lisbon
                4.9041,     # Amsterdam
                -3.7038,     # Madrid
                -47.8828,    # Brasília
                15.9819,     # Zagreb
                -6.8416,     # Rabat
                13.4050,     # Berlin
              139.6503,     # Tokyo
                7.4474,     # Bern
                -0.1870,     # Accra
              -17.4677,     # Dakar
              126.9780,     # Seoul
                20.4489,     # Belgrade
              -78.4678,     # Quito
                51.3890,     # Tehran
                11.5021,     # Yaoundé
              -84.0907,     # San José
              -77.0369,     # Washington, D.C.
                21.0122,     # Warsaw
                46.6753,     # Riyadh
              149.1300,     # Canberra
              -56.1645,     # Montevideo
              -99.1332,     # Mexico City
                4.3517,     # Brussels
                -3.1791,     # Cardiff
              -75.6972,     # Ottawa
                12.5683,     # Copenhagen
                51.5310,     # Doha
                10.1815      # Tunis
            ]})
            pred_min, pred_max = true_goals_22["goals"].min(),true_goals_22["goals"].max()
            true_goals_22["color_r"] = ((true_goals_22["goals"] - pred_min) / (pred_max - pred_min) * 255).astype(int)  # Red intensity
            true_goals_22["color_g"] = (155 - true_goals_22["color_r"]).astype(int)  # Green intensity
            true_goals_22["color_b"] = 180  # Keep blue constant
            true_goals_22["color_a"] = 230
            layer = pdk.Layer(
                "ColumnLayer",
                data=true_goals_22,
                get_position=['longitudes','latitudes'],
                get_elevation = "goals",
                elevation_scale= 84800,
                radius = 90000,
                get_fill_color=["color_r", "color_g", "color_b", "color_a"],
                #elevation_range="AQI",
                pickable=True,
                extruded=True,
                auto_highlight=True
            )
            vi = pdk.ViewState(latitude=true_goals_22["latitudes"].mean(),longitude= true_goals_22["longitudes"].mean(),zoom=4,pitch=30)
            xyz6 = pdk.Deck(layers=[layer],initial_view_state=vi)
            xyz6.to_html("pred_map.html")

            country4 = []
            for i in fifa_score_22_only_goal["Scored team"]:
              country4.append(i)
            country6 = list(set(country4))
            # UEFA - Europe
            europe = [
                'Croatia',
                'Portugal',
                'Spain',
                'Belgium',
                'Denmark',
                'Germany',
                'England',
                'Netherlands',
                'Switzerland',
                'Serbia',
                'Wales',
                'France',
                'Poland'
            ]

            # AFC - Asia
            asia = [
                'Saudi Arabia',
                'Iran',
                'South Korea',
                'Australia',
                'Japan',
                'Qatar'
            ]

            # CAF - Africa
            africa = [
                'Ghana',
                'Morocco',
                'Cameroon',
                'Tunisia',
                'Senegal'
            ]

            # CONMEBOL - South America
            south_america = [
                'Uruguay',
                'Ecuador',
                'Brazil',
                'Argentina'
            ]

            # CONCACAF - North & Central America / Caribbean
            concacaf = [
                'Costa Rica',
                'Mexico',
                'Canada',
                'United States'
            ]
            pre_2022_wc_rankings = {
                'Spain': 7,
                'Senegal': 18,
                'Saudi Arabia': 51,
                'Costa Rica': 31,
                'Cameroon': 43,
                'Argentina': 3,
                'Australia': 38,
                'Belgium': 2,
                'Mexico': 13,
                'Ecuador': 44,
                'Iran': 20,
                'Serbia': 21,
                'South Korea': 28,
                'Brazil': 1,
                'Qatar': 50,
                'Portugal': 9,
                'England': 5,
                'Tunisia': 30,
                'Croatia': 12,
                'Uruguay': 14,
                'Ghana': 61,
                'Japan': 24,
                'Poland': 26,
                'France': 4,
                'Canada': 41,
                'Switzerland': 15,
                'Germany': 11,
                'Wales': 19,
                'Netherlands': 8,
                'United States': 16,
                'Denmark': 10,
                'Morocco': 22
            }
            def rank(team_name):
              return pre_2022_wc_rankings.get(team_name, 0)
            fifa_score_22_only_goal["rank"] = fifa_score_22_only_goal["Scored team"].apply(rank)
            def get_continent(team_name):
              if team_name in asia:
                return "AFC"
              elif team_name in africa:
                return "CAF"
              elif team_name in south_america:
                return "CONMEBOL"
              elif team_name in concacaf:
                return "CONCACAF"
              elif team_name in europe:
                return "UEFA"
              else:
                return "Other" # Handle cases where a team might not be in any defined list

            fifa_score_22_only_goal["Continent"] = fifa_score_22_only_goal["Scored team"].apply(get_continent)
            def home_res(row):
              if row['Home team'] == row['Scored team']:
                return True
              else:
                return False
            def away_res(row):
              if row['Away team'] == row['Scored team']:
                return True
              else:
                return False
            fifa_score_22_only_goal["Home_res"] = fifa_score_22_only_goal.apply(home_res, axis=1)
            fifa_score_22_only_goal["Away_res"] = fifa_score_22_only_goal.apply(away_res, axis=1)
            home_score20 = fifa_score_22_only_goal.groupby(['Date', 'Scored team','rank'])['Away_res'].count()
            temp_df2 = home_score20.reset_index()
            home_score22 = pd.DataFrame({"Date":temp_df2["Date"],"Scored_team":temp_df2["Scored team"],"goals":temp_df2["Away_res"],"rank":temp_df2["rank"]})
            cc2 = fifa_score_22_only_goal["Continent"].value_counts()
            continent2 = pd.DataFrame({"continent":cc2.index,"goals":cc2.values})
            pie2 = px.pie(continent2, values='goals', names='continent', title='Continent Goals', 
                  color='goals',
                  color_discrete_sequence=["#ABEFA1", '#008000', "#82E1A9", '#006400',"#5FE85F"])
      
            ps2 = fifa_score_22_only_goal["Position"].value_counts()
            position2 = pd.DataFrame({"position":ps2.index,"goals":ps2.values})
            bar2 = px.area(position2, x="position", y="goals",color_discrete_sequence=['green'])
            with col8:
              st.subheader("Goals scored")
              xyz6
            with col9:
              pie2.update_layout(height=250,margin=dict(t=60, b=0, l=0, r=0))
              st.plotly_chart(pie2,use_container_width=False)
              bar2.update_layout(height = 300,margin=dict(t=90, b=0, l=0, r=0))
              st.plotly_chart(bar2,use_container_width=False)

elif selected == "INSIGHTS":
  # SPAIN DATA


  esp_data = pd.read_csv("data/spain_stats.csv")
  col = []
  for i in esp_data.columns:
    col.append(i)
  abc1 = esp_data.groupby(["players","position"])[col].mean(numeric_only=True).round(2)
  esp_abc = pd.DataFrame({
      "position":abc1.index.get_level_values(1),
      "minutes":abc1["minutes"],
      "ratings":abc1["ratings"],
      "goals scored":abc1["goals scored"],
      "assist":abc1["assist"],
      "shots on target":abc1["shots on target"],
      "shots attempted":abc1["shots attempted"],
      "long balls":abc1["long balls"],
      "long balls completed":abc1["long balls completed"],
      "key passes":abc1["key passes"],
      "duels won":abc1["duels won"],
      "take-ons conceeded":abc1["take-ons conceeded"],
      "tackles":abc1["tackles"],
      "interceptions":abc1["interceptions"],
      "clearances":abc1["clearances"],
      "blocks":abc1["blocks"],
      "dribbles completed":abc1["dribbles completed"],
      "dribbles attempt":abc1["dribbles attempt"],
      "yellow card":abc1["yellow card"],
      "red card":abc1["red card"],
      "nationality": ["Spain"] * len(abc1)
  })
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  esp_data["traits"] = esp_data["position"].apply(func)
  total_minutes = esp_data['minutes'].sum()
  overall_rating = (esp_data['ratings'] * esp_data['minutes']).sum()
  squad_quality = overall_rating / total_minutes
  rate_std = esp_data['ratings'].std()
  esp_top11 = esp_data.nlargest(11,'minutes')
  squad_quality11 = esp_top11['ratings'].mean()

  esp_att = esp_data[esp_data['traits'] == 'ATTACK']
  total_minutes = esp_att['minutes'].sum()
  esp_att_goals = esp_att["goals scored"].sum()
  esp_att_assist = esp_att["assist"].sum()
  esp_att_cont = (esp_att["goals scored"] + esp_att["assist"]).sum()
  esp_att_shots_on_target = esp_att['shots on target'].sum()
  esp_att_shots_attempted = esp_att['shots attempted'].sum()
  esp_att_key_passes_total = esp_att['key passes'].sum()
  esp_att_dribbles_completed = esp_att['dribbles completed'].sum()
  esp_att_dribbles_attempted = esp_att['dribbles attempt'].sum()
  esp_att_rating = esp_att['ratings'].mean()
  attack_goals_90 = ((esp_att_goals / total_minutes) * 90) if total_minutes > 0 else 0
  attack_assist_90 = (esp_att_assist / total_minutes * 90) if total_minutes > 0 else 0
  attack_cont_90 = (esp_att_cont / total_minutes * 90) if total_minutes > 0 else 0
  attack_shots_90 = (esp_att_shots_on_target / total_minutes * 90) if total_minutes > 0 else 0
  attack_key_passes_90 = (esp_att_key_passes_total / total_minutes * 90) if total_minutes > 0 else 0
  attack_dribbles_90 = (esp_att_dribbles_completed / total_minutes * 90)

  esp_mid = esp_data[esp_data['traits'] == 'MIDFIELD']
  total_minutes = esp_mid['minutes'].sum()
  esp_mid_pass_acc = esp_mid['passing accuracy in %'].mean()
  esp_mid_cont = (esp_mid["goals scored"] + esp_mid["assist"]).sum()
  esp_mid_long_balls_completed = esp_mid['long balls completed'].sum()
  esp_mid_long_balls = esp_mid['long balls'].sum()
  esp_mid_key_passes_total = esp_mid['key passes'].sum()
  esp_mid_dribbles_completed = esp_mid['dribbles completed'].sum()
  esp_mid_dribbles_attempted = esp_mid['dribbles attempt'].sum()
  esp_mid_touches = esp_mid['touches'].sum()
  esp_mid_def = (esp_mid['tackles'] + esp_mid["interceptions"]).sum()
  esp_mid_tackle = esp_mid['tackles'].sum()
  esp_mid_interceptions = esp_mid['interceptions'].sum()
  esp_mid_rating = (esp_mid['ratings'].mean())
  midfield_long_balls_comp_90 = (esp_mid_long_balls_completed / total_minutes * 90) if total_minutes > 0 else 0
  midfield_long_balls_90 = (esp_mid_long_balls / total_minutes * 90) if total_minutes > 0 else 0
  midfield_cont_90 = (esp_mid_cont / total_minutes * 90) if total_minutes > 0 else 0
  midfield_touches_90 = (esp_mid_touches / total_minutes * 90) if total_minutes > 0 else 0
  midfield_def_90 = (esp_mid_def / total_minutes * 90) if total_minutes > 0 else 0
  midfield_dribbles_90 = (esp_mid_dribbles_completed / total_minutes * 90)
  midfield_key_passes_90 = (esp_mid_key_passes_total / total_minutes * 90) if total_minutes > 0 else 0
  midfield_tackle_90 = (esp_mid_tackle / total_minutes * 90) if total_minutes > 0 else 0
  midfield_interceptions_90 = (esp_mid_interceptions / total_minutes * 90) if total_minutes > 0 else 0
  midfield_pass_acc_90 = (esp_mid_pass_acc / total_minutes * 90) if total_minutes > 0 else 0

  esp_def = esp_data[esp_data['traits'] == 'DEFENCE']
  total_minutes = esp_def['minutes'].sum()
  esp_def_duels = esp_def["duels won"].sum()
  esp_def_clearances = esp_def["clearances"].sum()
  esp_def_blocks = esp_def['blocks'].sum()
  esp_def_take_ons_conceeded = esp_def['take-ons conceeded'].sum()
  esp_def_tackle = esp_def['tackles'].sum()
  esp_def_interceptions = esp_def['interceptions'].sum()
  esp_def_rating = esp_def['ratings'].mean()
  esp_def_duels_won_pct = (esp_def['duels won'].sum() /
                                (esp_def['duels won'].sum() + esp_def['take-ons conceeded'].sum() + 1e-5))
  esp_def_cards = ((esp_def['yellow card'].sum() + 2 * esp_def['red card'].sum())
                                    / (total_minutes / 90)) if total_minutes > 0 else 0
  defence_duels_90 = (esp_def_duels / total_minutes * 90) if total_minutes > 0 else 0
  defence_clearance_90 = (esp_def_clearances / total_minutes * 90) if total_minutes > 0 else 0
  defence_blocks_90 = (esp_def_blocks / total_minutes * 90) if total_minutes > 0 else 0
  defence_take_ons_conceed_90 = (esp_def_take_ons_conceeded / total_minutes * 90) if total_minutes > 0 else 0
  defence_tackle_90 = (esp_def_tackle / total_minutes * 90) if total_minutes > 0 else 0
  defence_interceptions_90 = (esp_def_interceptions / total_minutes * 90)
  total_minutes = esp_data['minutes'].sum()
  esp_matches = (esp_data["opponent"].nunique())*2
  depth_players = esp_data["players"].nunique() # unique players with no repetation
  player_min = esp_data.groupby("players")["minutes"].sum()
  depth_60 = (player_min > 60).sum()
  depth_45 = (player_min > 45).sum()
  depth_ratings = esp_data.groupby("players")["ratings"].mean()
  depth_ratings_mean = esp_data["ratings"].mean()
  depth_rate_std = depth_ratings.std()
  depth_avg_min = total_minutes / depth_players if depth_players > 0 else 0
  depth_rating_15 = esp_data.nlargest(15, 'minutes')['ratings'].mean()
  depth_index = (depth_players * depth_rating_15) / (1 + depth_rate_std)
  depth_min_pct_11 = esp_data.nlargest(11, 'minutes')['minutes'].sum() / total_minutes * 100
  depth_avg_min_per_match = depth_avg_min/esp_matches


  # ARGENTINA

  arg_data = pd.read_csv("data/argentina_stats.csv")
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  arg_data["traits"] = arg_data["position"].apply(func)
  col = []
  for i in arg_data.columns:
    col.append(i)
  abc2 = arg_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  arg_abc = pd.DataFrame({
      "position":abc2.index.get_level_values(1),
      "minutes":abc2["minutes"],
      "ratings":abc2["ratings"],
      "goals scored":abc2["goals scored"],
      "assist":abc2["assist"],
      "shots on target":abc2["shots on target"],
      "shots attempted":abc2["shots attempted"],
      "long balls":abc2["long balls"],
      "long balls completed":abc2["long balls completed"],
      "key passes":abc2["key passes"],
      "duels won":abc2["duels won"],
      "take-ons conceeded":abc2["take-ons conceeded"],
      "tackles":abc2["tackles"],
      "interceptions":abc2["interceptions"],
      "clearances":abc2["clearances"],
      "blocks":abc2["blocks"],
      "dribbles completed":abc2["dribbles completed"],
      "dribbles attempt":abc2["dribbles attempt"],
      "yellow card":abc2["yellow card"],
      "red card":abc2["red card"],
      "nationality": ["Argentina"] * len(abc2)
  })
  arg_total_minutes = arg_data['minutes'].sum()
  arg_overall_rating = (arg_data['ratings'] * arg_data['minutes']).sum()
  arg_squad_quality = arg_overall_rating / arg_total_minutes
  arg_rate_std = arg_data['ratings'].std()
  arg_top11 = arg_data.nlargest(11,'minutes')
  arg_squad_quality11 = arg_top11['ratings'].mean()

  arg_att = arg_data[arg_data['traits'] == 'ATTACK']
  arg_total_minutes = arg_att['minutes'].sum()
  arg_att_goals = arg_att["goals scored"].sum()
  arg_att_assist = arg_att["assist"].sum()
  arg_att_cont = (arg_att["goals scored"] + arg_att["assist"]).sum()
  arg_att_shots_on_target = arg_att['shots on target'].sum()
  arg_att_shots_attempted = arg_att['shots attempted'].sum()
  arg_att_key_passes_total = arg_att['key passes'].sum()
  arg_att_dribbles_completed = arg_att['dribbles completed'].sum()
  arg_att_dribbles_attempted = arg_att['dribbles attempt'].sum()
  arg_att_rating = arg_att['ratings'].mean()
  arg_attack_goals_90 = ((arg_att_goals / arg_total_minutes) * 90) if arg_total_minutes > 0 else 0
  arg_attack_assist_90 = (arg_att_assist / arg_total_minutes * 90) if arg_total_minutes > 0 else 0
  arg_attack_cont_90 = (arg_att_cont / arg_total_minutes * 90) if arg_total_minutes > 0 else 0
  arg_attack_shots_90 = (arg_att_shots_on_target / arg_total_minutes * 90) if arg_total_minutes > 0 else 0
  arg_attack_key_passes_90 = (arg_att_key_passes_total / arg_total_minutes * 90) if arg_total_minutes > 0 else 0
  arg_attack_dribbles_90 = (arg_att_dribbles_completed / arg_total_minutes * 90)

  arg_mid = arg_data[arg_data['traits'] == 'MIDFIELD']
  arg_total_minutes_1 = arg_mid['minutes'].sum()
  arg_mid_pass_acc = arg_mid['passing accuracy in %'].mean()
  arg_mid_cont = (arg_mid["goals scored"] + arg_mid["assist"]).sum()
  arg_mid_long_balls_completed = arg_mid['long balls completed'].sum()
  arg_mid_long_balls = arg_mid['long balls'].sum()
  arg_mid_key_passes_total = arg_mid['key passes'].sum()
  arg_mid_dribbles_completed = arg_mid['dribbles completed'].sum()
  arg_mid_dribbles_attempted = arg_mid['dribbles attempt'].sum()
  arg_mid_touches = arg_mid['touches'].sum()
  arg_mid_def = (arg_mid['tackles'] + arg_mid["interceptions"]).sum()
  arg_mid_tackle = arg_mid['tackles'].sum()
  arg_mid_interceptions = arg_mid['interceptions'].sum()
  arg_mid_rating = arg_mid['ratings'].mean()
  arg_midfield_long_balls_comp_90 = (arg_mid_long_balls_completed / arg_total_minutes_1 * 90) if arg_total_minutes_1 > 0 else 0
  arg_midfield_long_balls_90 = (arg_mid_long_balls / arg_total_minutes_1 * 90) if arg_total_minutes_1 > 0 else 0
  arg_midfield_cont_90 = (arg_mid_cont / arg_total_minutes_1 * 90) if arg_total_minutes_1 > 0 else 0
  arg_midfield_touches_90 = (arg_mid_touches / arg_total_minutes_1 * 90) if arg_total_minutes_1 > 0 else 0
  arg_midfield_def_90 = (arg_mid_def / arg_total_minutes_1 * 90) if arg_total_minutes_1 > 0 else 0
  arg_midfield_dribbles_90 = (arg_mid_dribbles_completed / arg_total_minutes_1 * 90)
  arg_midfield_key_passes_90 = (arg_mid_key_passes_total / arg_total_minutes_1 * 90) if arg_total_minutes_1 > 0 else 0
  arg_midfield_tackle_90 = (arg_mid_tackle / arg_total_minutes_1 * 90) if arg_total_minutes_1 > 0 else 0
  arg_midfield_interceptions_90 = (arg_mid_interceptions / arg_total_minutes_1 * 90) if arg_total_minutes_1 > 0 else 0
  arg_midfield_pass_acc_90 = (arg_mid_pass_acc / arg_total_minutes_1 * 90) if arg_total_minutes_1 > 0 else 0

  arg_def = arg_data[arg_data['traits'] == 'DEFENCE']
  arg_def_total_minutes_2 = arg_def['minutes'].sum()
  arg_def_duels = arg_def["duels won"].sum()
  arg_def_clearances = arg_def["clearances"].sum()
  arg_def_blocks = arg_def['blocks'].sum()
  arg_def_take_ons_conceeded = arg_def['take-ons conceeded'].sum()
  arg_def_tackle = arg_def['tackles'].sum()
  arg_def_interceptions = arg_def['interceptions'].sum()
  arg_def_rating = arg_def['ratings'].mean()
  arg_def_duels_won_pct = (arg_def['duels won'].sum() /
                                (arg_def['duels won'].sum() + arg_def['take-ons conceeded'].sum() + 1e-5))
  arg_def_cards = ((arg_def['yellow card'].sum() + 2 * arg_def['red card'].sum())
                                    / (arg_def_total_minutes_2 / 90)) if arg_def_total_minutes_2 > 0 else 0
  arg_defence_duels_90 = (arg_def_duels / arg_def_total_minutes_2 * 90) if arg_def_total_minutes_2 > 0 else 0
  arg_defence_clearance_90 = (arg_def_clearances / arg_def_total_minutes_2 * 90) if arg_def_total_minutes_2 > 0 else 0
  arg_defence_blocks_90 = (arg_def_blocks / arg_def_total_minutes_2 * 90) if arg_def_total_minutes_2 > 0 else 0
  arg_defence_take_ons_conceed_90 = (arg_def_take_ons_conceeded / arg_def_total_minutes_2 * 90) if arg_def_total_minutes_2 > 0 else 0
  arg_defence_tackle_90 = (arg_def_tackle / arg_def_total_minutes_2 * 90) if arg_def_total_minutes_2 > 0 else 0
  arg_defence_interceptions_90 = (arg_def_interceptions / arg_def_total_minutes_2 * 90)

  arg_total_minutes = arg_data['minutes'].sum()
  arg_depth_players = arg_data["players"].nunique() # unique players with no repetation
  arg_matches = (arg_data["opponent"].nunique())*2
  arg_player_min = arg_data.groupby("players")["minutes"].sum()
  arg_depth_60 = (arg_player_min > 60).sum()
  arg_depth_45 = (arg_player_min > 45).sum()
  arg_depth_ratings = arg_data.groupby("players")["ratings"].mean()
  arg_depth_ratings_mean = arg_data["ratings"].mean()
  arg_depth_rate_std = arg_depth_ratings.std()
  arg_depth_avg_min = arg_total_minutes / arg_depth_players if arg_depth_players > 0 else 0
  arg_depth_rating_15 = arg_data.nlargest(15, 'minutes')['ratings'].mean()
  arg_depth_index = (arg_depth_players * arg_depth_rating_15) / (1 + arg_depth_rate_std)
  arg_depth_min_pct_11 = arg_data.nlargest(11, 'minutes')['minutes'].sum() / arg_total_minutes * 100
  arg_depth_avg_min_per_match = arg_depth_avg_min/arg_matches


  # BELGIUM

  bel_data = pd.read_csv("data/Belgium_stats.csv")
  bel_data = bel_data.dropna()
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  bel_data["traits"] = bel_data["position"].apply(func)
  col = []
  for i in bel_data.columns:
    col.append(i)
  abc3 = bel_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  bel_abc = pd.DataFrame({
      "position":abc3.index.get_level_values(1),
      "minutes":abc3["minutes"],
      "ratings":abc3["ratings"],
      "goals scored":abc3["goals scored"],
      "assist":abc3["assist"],
      "shots on target":abc3["shots on target"],
      "shots attempted":abc3["shots attempted"],
      "long balls":abc3["long balls"],
      "long balls completed":abc3["long balls completed"],
      "key passes":abc3["key passes"],
      "duels won":abc3["duels won"],
      "take-ons conceeded":abc3["take-ons conceeded"],
      "tackles":abc3["tackles"],
      "interceptions":abc3["interceptions"],
      "clearances":abc3["clearances"],
      "blocks":abc3["blocks"],
      "dribbles completed":abc3["dribbles completed"],
      "dribbles attempt":abc3["dribbles attempt"],
      "yellow card":abc3["yellow card"],
      "red card":abc3["red card"],
      "nationality": ["Belgium"] * len(abc3)
  })
  bel_total_minutes = bel_data['minutes'].sum()
  bel_overall_rating = (bel_data['ratings'] * bel_data['minutes']).sum()
  bel_squad_quality = bel_overall_rating / bel_total_minutes
  bel_rate_std = bel_data['ratings'].std()
  bel_top11 = bel_data.nlargest(11,'minutes')
  bel_squad_quality11 = bel_top11['ratings'].mean()

  bel_att = bel_data[bel_data['traits'] == 'ATTACK']
  bel_total_minutes = bel_att['minutes'].sum()
  bel_att_goals = bel_att["goals scored"].sum()
  bel_att_assist = bel_att["assist"].sum()
  bel_att_cont = (bel_att["goals scored"] + bel_att["assist"]).sum()
  bel_att_shots_on_target = bel_att['shots on target'].sum()
  bel_att_shots_attempted = bel_att['shots attempted'].sum()
  bel_att_key_passes_total = bel_att['key passes'].sum()
  bel_att_dribbles_completed = bel_att['dribbles completed'].sum()
  bel_att_dribbles_attempted = bel_att['dribbles attempt'].sum()
  bel_att_rating = bel_att['ratings'].mean()
  bel_attack_goals_90 = ((bel_att_goals / bel_total_minutes) * 90) if bel_total_minutes > 0 else 0
  bel_attack_assist_90 = (bel_att_assist / bel_total_minutes * 90) if bel_total_minutes > 0 else 0
  bel_attack_cont_90 = (bel_att_cont / bel_total_minutes * 90) if bel_total_minutes > 0 else 0
  bel_attack_shots_90 = (bel_att_shots_on_target / bel_total_minutes * 90) if bel_total_minutes > 0 else 0
  bel_attack_key_passes_90 = (bel_att_key_passes_total / bel_total_minutes * 90) if bel_total_minutes > 0 else 0
  bel_attack_dribbles_90 = (bel_att_dribbles_completed / bel_total_minutes * 90)

  bel_mid = bel_data[bel_data['traits'] == 'MIDFIELD']
  bel_mid_total_minutes = bel_mid['minutes'].sum()
  bel_mid_pass_acc = bel_mid['passing accuracy in %'].mean()
  bel_mid_cont = (bel_mid["goals scored"] + bel_mid["assist"]).sum()
  bel_mid_long_balls_completed = bel_mid['long balls completed'].sum()
  bel_mid_long_balls = bel_mid['long balls'].sum()
  bel_mid_key_passes_total = bel_mid['key passes'].sum()
  bel_mid_dribbles_completed = bel_mid['dribbles completed'].sum()
  bel_mid_dribbles_attempted = bel_mid['dribbles attempt'].sum()
  bel_mid_touches = bel_mid['touches'].sum()
  bel_mid_def = (bel_mid['tackles'] + bel_mid["interceptions"]).sum()
  bel_mid_tackle = bel_mid['tackles'].sum()
  bel_mid_interceptions = bel_mid['interceptions'].sum()
  bel_mid_rating = bel_mid['ratings'].mean()
  bel_midfield_long_balls_comp_90 = (bel_mid_long_balls_completed / bel_mid_total_minutes * 90) if bel_mid_total_minutes > 0 else 0
  bel_midfield_long_balls_90 = (bel_mid_long_balls / bel_mid_total_minutes * 90) if bel_mid_total_minutes > 0 else 0
  bel_midfield_cont_90 = (bel_mid_cont / bel_mid_total_minutes * 90) if bel_mid_total_minutes > 0 else 0
  bel_midfield_touches_90 = (bel_mid_touches / bel_mid_total_minutes * 90) if bel_mid_total_minutes > 0 else 0
  bel_midfield_def_90 = (bel_mid_def / bel_mid_total_minutes * 90) if bel_mid_total_minutes > 0 else 0
  bel_midfield_dribbles_90 = (bel_mid_dribbles_completed / bel_mid_total_minutes * 90)
  bel_midfield_key_passes_90 = (bel_mid_key_passes_total / bel_mid_total_minutes * 90) if bel_mid_total_minutes > 0 else 0
  bel_midfield_tackle_90 = (bel_mid_tackle / bel_mid_total_minutes * 90) if bel_mid_total_minutes > 0 else 0
  bel_midfield_interceptions_90 = (bel_mid_interceptions / bel_mid_total_minutes * 90) if bel_mid_total_minutes > 0 else 0
  bel_midfield_pass_acc_90 = (bel_mid_pass_acc / bel_mid_total_minutes * 90) if bel_mid_total_minutes > 0 else 0

  bel_def = bel_data[bel_data['traits'] == 'DEFENCE']
  bel_def_total_minutes_2 = bel_def['minutes'].sum()
  bel_def_duels = bel_def["duels won"].sum()
  bel_def_clearances = bel_def["clearances"].sum()
  bel_def_blocks = bel_def['blocks'].sum()
  bel_def_take_ons_conceeded = bel_def['take-ons conceeded'].sum()
  bel_def_tackle = bel_def['tackles'].sum()
  bel_def_interceptions = bel_def['interceptions'].sum()
  bel_def_rating = bel_def['ratings'].mean()
  bel_def_duels_won_pct = (bel_def['duels won'].sum() /
                                (bel_def['duels won'].sum() + bel_def['take-ons conceeded'].sum() + 1e-5))
  bel_def_cards = ((bel_def['yellow card'].sum() + 2 * bel_def['red card'].sum())
                                    / (bel_def_total_minutes_2 / 90)) if bel_def_total_minutes_2 > 0 else 0

  bel_defence_duels_90 = (bel_def_duels / bel_def_total_minutes_2 * 90) if bel_def_total_minutes_2 > 0 else 0
  bel_defence_clearance_90 = (bel_def_clearances / bel_def_total_minutes_2 * 90) if bel_def_total_minutes_2 > 0 else 0
  bel_defence_blocks_90 = (bel_def_blocks / bel_def_total_minutes_2 * 90) if bel_def_total_minutes_2 > 0 else 0
  bel_defence_take_ons_conceed_90 = (bel_def_take_ons_conceeded / bel_def_total_minutes_2 * 90) if bel_def_total_minutes_2 > 0 else 0
  bel_defence_tackle_90 = (bel_def_tackle / bel_def_total_minutes_2 * 90) if bel_def_total_minutes_2 > 0 else 0
  bel_defence_interceptions_90 = (bel_def_interceptions / bel_def_total_minutes_2 * 90)

  bel_total_minutes = bel_data['minutes'].sum()
  bel_depth_players = bel_data["players"].nunique() # unique players with no repetation
  bel_matches = (bel_data["opponent"].nunique())*2
  bel_player_min = bel_data.groupby("players")["minutes"].sum()
  bel_depth_60 = (bel_player_min > 60).sum()
  bel_depth_45 = (bel_player_min > 45).sum()
  bel_depth_ratings = bel_data.groupby("players")["ratings"].mean()
  bel_depth_ratings_mean = bel_data["ratings"].mean()
  bel_depth_rate_std = bel_depth_ratings.std()
  bel_depth_avg_min = bel_total_minutes / bel_depth_players if bel_depth_players > 0 else 0
  bel_depth_rating_15 = bel_data.nlargest(15, 'minutes')['ratings'].mean()
  bel_depth_index = (bel_depth_players * bel_depth_rating_15) / (1 + bel_depth_rate_std)
  bel_depth_min_pct_11 = bel_data.nlargest(11, 'minutes')['minutes'].sum() / bel_total_minutes * 100
  bel_depth_avg_min_per_match = bel_depth_avg_min/bel_matches


  # BRAZIL


  bra_data = pd.read_csv("data/brazil_stats.csv")
  bra_data = bra_data.dropna()
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  bra_data["traits"] = bra_data["position"].apply(func)
  col = []
  for i in bra_data.columns:
    col.append(i)
  abc4 = bra_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  bra_abc = pd.DataFrame({
      "position":abc4.index.get_level_values(1),
      "minutes":abc4["minutes"],
      "ratings":abc4["ratings"],
      "goals scored":abc4["goals scored"],
      "assist":abc4["assist"],
      "shots on target":abc4["shots on target"],
      "shots attempted":abc4["shots attempted"],
      "long balls":abc4["long balls"],
      "long balls completed":abc4["long balls completed"],
      "key passes":abc4["key passes"],
      "duels won":abc4["duels won"],
      "take-ons conceeded":abc4["take-ons conceeded"],
      "tackles":abc4["tackles"],
      "interceptions":abc4["interceptions"],
      "clearances":abc4["clearances"],
      "blocks":abc4["blocks"],
      "dribbles completed":abc4["dribbles completed"],
      "dribbles attempt":abc4["dribbles attempt"],
      "yellow card":abc4["yellow card"],
      "red card":abc4["red card"],
      "nationality": ["Brazil"] * len(abc4)
  })

  bra_total_minutes = bra_data['minutes'].sum()
  bra_overall_rating = (bra_data['ratings'] * bra_data['minutes']).sum()
  bra_squad_quality = bra_overall_rating / bra_total_minutes
  bra_rate_std = bra_data['ratings'].std()
  bra_top11 = bra_data.nlargest(11,'minutes')
  bra_squad_quality11 = bra_top11['ratings'].mean()

  bra_att = bra_data[bra_data['traits'] == 'ATTACK']
  bra_total_minutes = bra_att['minutes'].sum()
  bra_att_goals = bra_att["goals scored"].sum()
  bra_att_assist = bra_att["assist"].sum()
  bra_att_cont = (bra_att["goals scored"] + bra_att["assist"]).sum()
  bra_att_shots_on_target = bra_att['shots on target'].sum()
  bra_att_shots_attempted = bra_att['shots attempted'].sum()
  bra_att_key_passes_total = bra_att['key passes'].sum()
  bra_att_dribbles_completed = bra_att['dribbles completed'].sum()
  bra_att_dribbles_attempted = bra_att['dribbles attempt'].sum()
  bra_att_rating = bra_att['ratings'].mean()
  bra_attack_goals_90 = ((bra_att_goals / bra_total_minutes) * 90) if bra_total_minutes > 0 else 0
  bra_attack_assist_90 = (bra_att_assist / bra_total_minutes * 90) if bra_total_minutes > 0 else 0
  bra_attack_cont_90 = (bra_att_cont / bra_total_minutes * 90) if bra_total_minutes > 0 else 0
  bra_attack_shots_90 = (bra_att_shots_on_target / bra_total_minutes * 90) if bra_total_minutes > 0 else 0
  bra_attack_key_passes_90 = (bra_att_key_passes_total / bra_total_minutes * 90) if bra_total_minutes > 0 else 0
  bra_attack_dribbles_90 = (bra_att_dribbles_completed / bra_total_minutes * 90)

  bra_mid = bra_data[bra_data['traits'] == 'MIDFIELD']
  bra_mid_total_minutes = bra_mid['minutes'].sum()
  bra_mid_pass_acc = bra_mid['passing accuracy in %'].mean()
  bra_mid_cont = (bra_mid["goals scored"] + bra_mid["assist"]).sum()
  bra_mid_long_balls_completed = bra_mid['long balls completed'].sum()
  bra_mid_long_balls = bra_mid['long balls'].sum()
  bra_mid_key_passes_total = bra_mid['key passes'].sum()
  bra_mid_dribbles_completed = bra_mid['dribbles completed'].sum()
  bra_mid_dribbles_attempted = bra_mid['dribbles attempt'].sum()
  bra_mid_touches = bra_mid['touches'].sum()
  bra_mid_def = (bra_mid['tackles'] + bra_mid["interceptions"]).sum()
  bra_mid_tackle = bra_mid['tackles'].sum()
  bra_mid_interceptions = bra_mid['interceptions'].sum()
  bra_mid_rating = bra_mid['ratings'].mean()
  bra_midfield_long_balls_comp_90 = (bra_mid_long_balls_completed / bra_mid_total_minutes * 90) if bra_mid_total_minutes > 0 else 0
  bra_midfield_long_balls_90 = (bra_mid_long_balls / bra_mid_total_minutes * 90) if bra_mid_total_minutes > 0 else 0
  bra_midfield_cont_90 = (bra_mid_cont / bra_mid_total_minutes * 90) if bra_mid_total_minutes > 0 else 0
  bra_midfield_touches_90 = (bra_mid_touches / bra_mid_total_minutes * 90) if bra_mid_total_minutes > 0 else 0
  bra_midfield_def_90 = (bra_mid_def / bra_mid_total_minutes * 90) if bra_mid_total_minutes > 0 else 0
  bra_midfield_dribbles_90 = (bra_mid_dribbles_completed / bra_mid_total_minutes * 90)
  bra_midfield_key_passes_90 = (bra_mid_key_passes_total / bra_mid_total_minutes * 90) if bra_mid_total_minutes > 0 else 0
  bra_midfield_tackle_90 = (bra_mid_tackle / bra_mid_total_minutes * 90) if bra_mid_total_minutes > 0 else 0
  bra_midfield_interceptions_90 = (bra_mid_interceptions / bra_mid_total_minutes * 90) if bra_mid_total_minutes > 0 else 0
  bra_midfield_pass_acc_90 = (bra_mid_pass_acc / bra_mid_total_minutes * 90) if bra_mid_total_minutes > 0 else 0

  bra_def = bra_data[bra_data['traits'] == 'DEFENCE']
  bra_def_total_minutes_2 = bra_def['minutes'].sum()
  bra_def_duels = bra_def["duels won"].sum()
  bra_def_clearances = bra_def["clearances"].sum()
  bra_def_blocks = bra_def['blocks'].sum()
  bra_def_take_ons_conceeded = bra_def['take-ons conceeded'].sum()
  bra_def_tackle = bra_def['tackles'].sum()
  bra_def_interceptions = bra_def['interceptions'].sum()
  bra_def_rating = bra_def['ratings'].mean()
  bra_def_duels_won_pct = (bra_def['duels won'].sum() /
                                (bra_def['duels won'].sum() + bra_def['take-ons conceeded'].sum() + 1e-5))
  bra_def_cards = ((bra_def['yellow card'].sum() + 2 * bra_def['red card'].sum())
                                    / (bra_def_total_minutes_2 / 90)) if bra_def_total_minutes_2 > 0 else 0

  bra_defence_duels_90 = (bra_def_duels / bra_def_total_minutes_2 * 90) if bra_def_total_minutes_2 > 0 else 0
  bra_defence_clearance_90 = (bra_def_clearances / bra_def_total_minutes_2 * 90) if bra_def_total_minutes_2 > 0 else 0
  bra_defence_blocks_90 = (bra_def_blocks / bra_def_total_minutes_2 * 90) if bra_def_total_minutes_2 > 0 else 0
  bra_defence_take_ons_conceed_90 = (bra_def_take_ons_conceeded / bra_def_total_minutes_2 * 90) if bra_def_total_minutes_2 > 0 else 0
  bra_defence_tackle_90 = (bra_def_tackle / bra_def_total_minutes_2 * 90) if bra_def_total_minutes_2 > 0 else 0
  bra_defence_interceptions_90 = (bra_def_interceptions / bra_def_total_minutes_2 * 90)

  bra_total_minutes = bra_data['minutes'].sum()
  bra_depth_players = bra_data["players"].nunique() # unique players with no repetation
  bra_matches = (bra_data["opponent"].nunique())*2
  bra_player_min = bra_data.groupby("players")["minutes"].sum()
  bra_depth_60 = (bra_player_min > 60).sum()
  bra_depth_45 = (bra_player_min > 45).sum()
  bra_depth_ratings = bra_data.groupby("players")["ratings"].mean()
  bra_depth_ratings_mean = bra_data["ratings"].mean()
  bra_depth_rate_std = bra_depth_ratings.std()
  bra_depth_avg_min = bra_total_minutes / bra_depth_players if bra_depth_players > 0 else 0
  bra_depth_rating_15 = bra_data.nlargest(15, 'minutes')['ratings'].mean()
  bra_depth_index = (bra_depth_players * bra_depth_rating_15) / (1 + bra_depth_rate_std)
  bra_depth_min_pct_11 = bra_data.nlargest(11, 'minutes')['minutes'].sum() / bra_total_minutes * 100
  bra_depth_avg_min_per_match = bra_depth_avg_min/bra_matches


  # COLOMBIA


  col_data = pd.read_csv("data/colombia_stats.csv")
  col_data = col_data.dropna()
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  col_data["traits"] = col_data["position"].apply(func)
  colo = []
  for i in col_data.columns:
    colo.append(i)
  abc5 = col_data.groupby(["players","position"])[colo[1:]].mean(numeric_only=True).round(2)
  col_abc = pd.DataFrame({
      "position":abc5.index.get_level_values(1),
      "minutes":abc5["minutes"],
      "ratings":abc5["ratings"],
      "goals scored":abc5["goals scored"],
      "assist":abc5["assist"],
      "shots on target":abc5["shots on target"],
      "shots attempted":abc5["shots attempted"],
      "long balls":abc5["long balls"],
      "long balls completed":abc5["long balls completed"],
      "key passes":abc5["key passes"],
      "duels won":abc5["duels won"],
      "take-ons conceeded":abc5["take-ons conceeded"],
      "tackles":abc5["tackles"],
      "interceptions":abc5["interceptions"],
      "clearances":abc5["clearances"],
      "blocks":abc5["blocks"],
      "dribbles completed":abc5["dribbles completed"],
      "dribbles attempt":abc5["dribbles attempt"],
      "yellow card":abc5["yellow card"],
      "red card":abc5["red card"],
      "nationality": ["Colombia"] * len(abc5)
  })

  col_total_minutes = col_data['minutes'].sum()
  col_overall_rating = (col_data['ratings'] * col_data['minutes']).sum()
  col_squad_quality = col_overall_rating / col_total_minutes
  col_rate_std = col_data['ratings'].std()
  col_top11 = col_data.nlargest(11,'minutes')
  col_squad_quality11 = col_top11['ratings'].mean()

  col_att = col_data[col_data['traits'] == 'ATTACK']
  col_total_minutes = col_att['minutes'].sum()
  col_att_goals = col_att["goals scored"].sum()
  col_att_assist = col_att["assist"].sum()
  col_att_cont = (col_att["goals scored"] + col_att["assist"]).sum()
  col_att_shots_on_target = col_att['shots on target'].sum()
  col_att_shots_attempted = col_att['shots attempted'].sum()
  col_att_key_passes_total = col_att['key passes'].sum()
  col_att_dribbles_completed = col_att['dribbles completed'].sum()
  col_att_dribbles_attempted = col_att['dribbles attempt'].sum()
  col_att_rating = col_att['ratings'].mean()
  col_attack_goals_90 = ((col_att_goals / col_total_minutes) * 90) if col_total_minutes > 0 else 0
  col_attack_assist_90 = (col_att_assist / col_total_minutes * 90) if col_total_minutes > 0 else 0
  col_attack_cont_90 = (col_att_cont / col_total_minutes * 90) if col_total_minutes > 0 else 0
  col_attack_shots_90 = (col_att_shots_on_target / col_total_minutes * 90) if col_total_minutes > 0 else 0
  col_attack_key_passes_90 = (col_att_key_passes_total / col_total_minutes * 90) if col_total_minutes > 0 else 0
  col_attack_dribbles_90 = (col_att_dribbles_completed / col_total_minutes * 90)

  col_mid = col_data[col_data['traits'] == 'MIDFIELD']
  col_mid_total_minutes = col_mid['minutes'].sum()
  col_mid_pass_acc = col_mid['passing accuracy in %'].mean()
  col_mid_cont = (col_mid["goals scored"] + col_mid["assist"]).sum()
  col_mid_long_balls_completed = col_mid['long balls completed'].sum()
  col_mid_long_balls = col_mid['long balls'].sum()
  col_mid_key_passes_total = col_mid['key passes'].sum()
  col_mid_dribbles_completed = col_mid['dribbles completed'].sum()
  col_mid_dribbles_attempted = col_mid['dribbles attempt'].sum()
  col_mid_touches = col_mid['touches'].sum()
  col_mid_def = (col_mid['tackles'] + col_mid["interceptions"]).sum()
  col_mid_tackle = col_mid['tackles'].sum()
  col_mid_interceptions = col_mid['interceptions'].sum()
  col_mid_rating = col_mid['ratings'].mean()
  col_midfield_long_balls_comp_90 = (col_mid_long_balls_completed / col_mid_total_minutes * 90) if col_mid_total_minutes > 0 else 0
  col_midfield_long_balls_90 = (col_mid_long_balls / col_mid_total_minutes * 90) if col_mid_total_minutes > 0 else 0
  col_midfield_cont_90 = (col_mid_cont / col_mid_total_minutes * 90) if col_mid_total_minutes > 0 else 0
  col_midfield_touches_90 = (col_mid_touches / col_mid_total_minutes * 90) if col_mid_total_minutes > 0 else 0
  col_midfield_def_90 = (col_mid_def / col_mid_total_minutes * 90) if col_mid_total_minutes > 0 else 0
  col_midfield_dribbles_90 = (col_mid_dribbles_completed / col_mid_total_minutes * 90)
  col_midfield_key_passes_90 = (col_mid_key_passes_total / col_mid_total_minutes * 90) if col_mid_total_minutes > 0 else 0
  col_midfield_tackle_90 = (col_mid_tackle / col_mid_total_minutes * 90) if col_mid_total_minutes > 0 else 0
  col_midfield_interceptions_90 = (col_mid_interceptions / col_mid_total_minutes * 90) if col_mid_total_minutes > 0 else 0
  col_midfield_pass_acc_90 = (col_mid_pass_acc / col_mid_total_minutes * 90) if col_mid_total_minutes > 0 else 0
  print("midfield_long_balls_comp_90",col_midfield_long_balls_comp_90)

  col_def = col_data[col_data['traits'] == 'DEFENCE']
  col_def_total_minutes_2 = col_def['minutes'].sum()
  col_def_duels = col_def["duels won"].sum()
  col_def_clearances = col_def["clearances"].sum()
  col_def_blocks = col_def['blocks'].sum()
  col_def_take_ons_conceeded = col_def['take-ons conceeded'].sum()
  col_def_tackle = col_def['tackles'].sum()
  col_def_interceptions = col_def['interceptions'].sum()
  col_def_rating = col_def['ratings'].mean()
  col_def_duels_won_pct = (col_def['duels won'].sum() /
                                (col_def['duels won'].sum() + col_def['take-ons conceeded'].sum() + 1e-5))
  col_def_cards = ((col_def['yellow card'].sum() + 2 * col_def['red card'].sum())
                                    / (col_def_total_minutes_2 / 90)) if col_def_total_minutes_2 > 0 else 0

  col_defence_duels_90 = (col_def_duels / col_def_total_minutes_2 * 90) if col_def_total_minutes_2 > 0 else 0
  col_defence_clearance_90 = (col_def_clearances / col_def_total_minutes_2 * 90) if col_def_total_minutes_2 > 0 else 0
  col_defence_blocks_90 = (col_def_blocks / col_def_total_minutes_2 * 90) if col_def_total_minutes_2 > 0 else 0
  col_defence_take_ons_conceed_90 = (col_def_take_ons_conceeded / col_def_total_minutes_2 * 90) if col_def_total_minutes_2 > 0 else 0
  col_defence_tackle_90 = (col_def_tackle / col_def_total_minutes_2 * 90) if col_def_total_minutes_2 > 0 else 0
  col_defence_interceptions_90 = (col_def_interceptions / col_def_total_minutes_2 * 90)

  col_total_minutes = col_data['minutes'].sum()
  col_depth_players = col_data["players"].nunique() # unique players with no repetation
  col_matches = (col_data["opponent"].nunique())*2
  col_player_min = col_data.groupby("players")["minutes"].sum()
  col_depth_60 = (col_player_min > 60).sum()
  col_depth_45 = (col_player_min > 45).sum()
  col_depth_ratings = col_data.groupby("players")["ratings"].mean()
  col_depth_ratings_mean = col_data["ratings"].mean()
  col_depth_rate_std = col_depth_ratings.std()
  col_depth_avg_min = col_total_minutes / col_depth_players if col_depth_players > 0 else 0
  col_depth_rating_15 = col_data.nlargest(15, 'minutes')['ratings'].mean()
  col_depth_index = (col_depth_players * col_depth_rating_15) / (1 + col_depth_rate_std)
  col_depth_min_pct_11 = col_data.nlargest(11, 'minutes')['minutes'].sum() / col_total_minutes * 100
  col_depth_avg_min_per_match = col_depth_avg_min/col_matches


  # CROATIA

  cro_data = pd.read_csv("data/croatia_stats.csv")
  cro_data = cro_data.dropna()
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  cro_data["traits"] = cro_data["position"].apply(func)
  col = []
  for i in esp_data.columns:
    col.append(i)
  abc6 = cro_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  cro_abc = pd.DataFrame({
    "position":abc6.index.get_level_values(1),
    "minutes":abc6["minutes"],
    "ratings":abc6["ratings"],
    "goals scored":abc6["goals scored"],
    "assist":abc6["assist"],
    "shots on target":abc6["shots on target"],
    "shots attempted":abc6["shots attempted"],
    "long balls":abc6["long balls"],
    "long balls completed":abc6["long balls completed"],
    "key passes":abc6["key passes"],
    "duels won":abc6["duels won"],
    "take-ons conceeded":abc6["take-ons conceeded"],
    "tackles":abc6["tackles"],
    "interceptions":abc6["interceptions"],
    "clearances":abc6["clearances"],
    "blocks":abc6["blocks"],
    "dribbles completed":abc6["dribbles completed"],
    "dribbles attempt":abc6["dribbles attempt"],
    "yellow card":abc6["yellow card"],
    "red card":abc6["red card"],
    "nationality": ["Croatia"] * len(abc6)
})
  cro_total_minutes = cro_data['minutes'].sum()
  cro_overall_rating = (cro_data['ratings'] * cro_data['minutes']).sum()
  cro_squad_quality = cro_overall_rating / cro_total_minutes
  cro_rate_std = cro_data['ratings'].std()
  cro_top11 = cro_data.nlargest(11,'minutes')
  cro_squad_quality11 = cro_top11['ratings'].mean()

  cro_att = cro_data[cro_data['traits'] == 'ATTACK']
  cro_total_minutes = cro_att['minutes'].sum()
  cro_att_goals = cro_att["goals scored"].sum()
  cro_att_assist = cro_att["assist"].sum()
  cro_att_cont = (cro_att["goals scored"] + cro_att["assist"]).sum()
  cro_att_shots_on_target = cro_att['shots on target'].sum()
  cro_att_shots_attempted = cro_att['shots attempted'].sum()
  cro_att_key_passes_total = cro_att['key passes'].sum()
  cro_att_dribbles_completed = cro_att['dribbles completed'].sum()
  cro_att_dribbles_attempted = cro_att['dribbles attempt'].sum()
  cro_att_rating = cro_att['ratings'].mean()
  cro_attack_goals_90 = ((cro_att_goals / cro_total_minutes) * 90) if cro_total_minutes > 0 else 0
  cro_attack_assist_90 = (cro_att_assist / cro_total_minutes * 90) if cro_total_minutes > 0 else 0
  cro_attack_cont_90 = (cro_att_cont / cro_total_minutes * 90) if cro_total_minutes > 0 else 0
  cro_attack_shots_90 = (cro_att_shots_on_target / cro_total_minutes * 90) if cro_total_minutes > 0 else 0
  cro_attack_key_passes_90 = (cro_att_key_passes_total / cro_total_minutes * 90) if cro_total_minutes > 0 else 0
  cro_attack_dribbles_90 = (cro_att_dribbles_completed / cro_total_minutes * 90)

  cro_mid = cro_data[cro_data['traits'] == 'MIDFIELD']
  cro_mid_total_minutes = cro_mid['minutes'].sum()
  cro_mid_pass_acc = cro_mid['passing accuracy in %'].mean()
  cro_mid_cont = (cro_mid["goals scored"] + cro_mid["assist"]).sum()
  cro_mid_long_balls_completed = cro_mid['long balls completed'].sum()
  cro_mid_long_balls = cro_mid['long balls'].sum()
  cro_mid_key_passes_total = cro_mid['key passes'].sum()
  cro_mid_dribbles_completed = cro_mid['dribbles completed'].sum()
  cro_mid_dribbles_attempted = cro_mid['dribbles attempt'].sum()
  cro_mid_touches = cro_mid['touches'].sum()
  cro_mid_def = (cro_mid['tackles'] + cro_mid["interceptions"]).sum()
  cro_mid_tackle = cro_mid['tackles'].sum()
  cro_mid_interceptions = cro_mid['interceptions'].sum()
  cro_mid_rating = cro_mid['ratings'].mean()

  cro_midfield_long_balls_comp_90 = (cro_mid_long_balls_completed / cro_mid_total_minutes * 90) if cro_mid_total_minutes > 0 else 0
  cro_midfield_long_balls_90 = (cro_mid_long_balls / cro_mid_total_minutes * 90) if cro_mid_total_minutes > 0 else 0
  cro_midfield_cont_90 = (cro_mid_cont / cro_mid_total_minutes * 90) if cro_mid_total_minutes > 0 else 0
  cro_midfield_touches_90 = (cro_mid_touches / cro_mid_total_minutes * 90) if cro_mid_total_minutes > 0 else 0
  cro_midfield_def_90 = (cro_mid_def / cro_mid_total_minutes * 90) if cro_mid_total_minutes > 0 else 0
  cro_midfield_dribbles_90 = (cro_mid_dribbles_completed / cro_mid_total_minutes * 90)
  cro_midfield_key_passes_90 = (cro_mid_key_passes_total / cro_mid_total_minutes * 90) if cro_mid_total_minutes > 0 else 0
  cro_midfield_tackle_90 = (cro_mid_tackle / cro_mid_total_minutes * 90) if cro_mid_total_minutes > 0 else 0
  cro_midfield_interceptions_90 = (cro_mid_interceptions / cro_mid_total_minutes * 90) if cro_mid_total_minutes > 0 else 0
  cro_midfield_pass_acc_90 = (cro_mid_pass_acc / cro_mid_total_minutes * 90) if cro_mid_total_minutes > 0 else 0

  cro_def = cro_data[cro_data['traits'] == 'DEFENCE']
  cro_def_total_minutes_2 = cro_def['minutes'].sum()
  cro_def_duels = cro_def["duels won"].sum()
  cro_def_clearances = cro_def["clearances"].sum()
  cro_def_blocks = cro_def['blocks'].sum()
  cro_def_take_ons_conceeded = cro_def['take-ons conceeded'].sum()
  cro_def_tackle = cro_def['tackles'].sum()
  cro_def_interceptions = cro_def['interceptions'].sum()
  cro_def_rating = cro_def['ratings'].mean()
  cro_def_duels_won_pct = (cro_def['duels won'].sum() /
                                (cro_def['duels won'].sum() + cro_def['take-ons conceeded'].sum() + 1e-5))
  cro_def_cards = ((cro_def['yellow card'].sum() + 2 * cro_def['red card'].sum())
                                    / (cro_def_total_minutes_2 / 90)) if cro_def_total_minutes_2 > 0 else 0

  cro_defence_duels_90 = (cro_def_duels / cro_def_total_minutes_2 * 90) if cro_def_total_minutes_2 > 0 else 0
  cro_defence_clearance_90 = (cro_def_clearances / cro_def_total_minutes_2 * 90) if cro_def_total_minutes_2 > 0 else 0
  cro_defence_blocks_90 = (cro_def_blocks / cro_def_total_minutes_2 * 90) if cro_def_total_minutes_2 > 0 else 0
  cro_defence_take_ons_conceed_90 = (cro_def_take_ons_conceeded / cro_def_total_minutes_2 * 90) if cro_def_total_minutes_2 > 0 else 0
  cro_defence_tackle_90 = (cro_def_tackle / cro_def_total_minutes_2 * 90) if cro_def_total_minutes_2 > 0 else 0
  cro_defence_interceptions_90 = (cro_def_interceptions / cro_def_total_minutes_2 * 90)

  cro_total_minutes = cro_data['minutes'].sum()
  cro_depth_players = cro_data["players"].nunique() # unique players with no repetation
  cro_matches = (cro_data["opponent"].nunique())*2
  cro_player_min = cro_data.groupby("players")["minutes"].sum()
  cro_depth_60 = (cro_player_min > 60).sum()
  cro_depth_45 = (cro_player_min > 45).sum()
  cro_depth_ratings = cro_data.groupby("players")["ratings"].mean()
  cro_depth_ratings_mean = cro_data["ratings"].mean()
  cro_depth_rate_std = cro_depth_ratings.std()
  cro_depth_avg_min = cro_total_minutes / cro_depth_players if cro_depth_players > 0 else 0
  cro_depth_rating_15 = cro_data.nlargest(15, 'minutes')['ratings'].mean()
  cro_depth_index = (cro_depth_players * cro_depth_rating_15) / (1 + cro_depth_rate_std)
  cro_depth_min_pct_11 = cro_data.nlargest(11, 'minutes')['minutes'].sum() / cro_total_minutes * 100
  cro_depth_avg_min_per_match = cro_depth_avg_min/cro_matches


  # DUTCH


  dut_data = pd.read_csv("data/dutch_stats.csv")
  dut_data = dut_data.dropna()
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  dut_data["traits"] = dut_data["position"].apply(func)
  col = []
  for i in esp_data.columns:
    col.append(i)
  abc7 = dut_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  dut_abc = pd.DataFrame({
      "position":abc7.index.get_level_values(1),
      "minutes":abc7["minutes"],
      "ratings":abc7["ratings"],
      "goals scored":abc7["goals scored"],
      "assist":abc7["assist"],
      "shots on target":abc7["shots on target"],
      "shots attempted":abc7["shots attempted"],
      "long balls":abc7["long balls"],
      "long balls completed":abc7["long balls completed"],
      "key passes":abc7["key passes"],
      "duels won":abc7["duels won"],
      "take-ons conceeded":abc7["take-ons conceeded"],
      "tackles":abc7["tackles"],
      "interceptions":abc7["interceptions"],
      "clearances":abc7["clearances"],
      "blocks":abc7["blocks"],
      "dribbles completed":abc7["dribbles completed"],
      "dribbles attempt":abc7["dribbles attempt"],
      "yellow card":abc7["yellow card"],
      "red card":abc7["red card"],
      "nationality": ["Netherlands"] * len(abc7)
  })
  dut_total_minutes = dut_data['minutes'].sum()
  dut_overall_rating = (dut_data['ratings'] * dut_data['minutes']).sum()
  dut_squad_quality = dut_overall_rating / dut_total_minutes
  dut_rate_std = dut_data['ratings'].std()
  dut_top11 = dut_data.nlargest(11,'minutes')
  dut_squad_quality11 = dut_top11['ratings'].mean()

  dut_att = dut_data[dut_data['traits'] == 'ATTACK']
  dut_total_minutes = dut_att['minutes'].sum()
  dut_att_goals = dut_att["goals scored"].sum()
  dut_att_assist = dut_att["assist"].sum()
  dut_att_cont = (dut_att["goals scored"] + dut_att["assist"]).sum()
  dut_att_shots_on_target = dut_att['shots on target'].sum()
  dut_att_shots_attempted = dut_att['shots attempted'].sum()
  dut_att_key_passes_total = dut_att['key passes'].sum()
  dut_att_dribbles_completed = dut_att['dribbles completed'].sum()
  dut_att_dribbles_attempted = dut_att['dribbles attempt'].sum()
  dut_att_rating = dut_att['ratings'].mean()
  dut_attack_goals_90 = ((dut_att_goals / dut_total_minutes) * 90) if dut_total_minutes > 0 else 0
  dut_attack_assist_90 = (dut_att_assist / dut_total_minutes * 90) if dut_total_minutes > 0 else 0
  dut_attack_cont_90 = (dut_att_cont / dut_total_minutes * 90) if dut_total_minutes > 0 else 0
  dut_attack_shots_90 = (dut_att_shots_on_target / dut_total_minutes * 90) if dut_total_minutes > 0 else 0
  dut_attack_key_passes_90 = (dut_att_key_passes_total / dut_total_minutes * 90) if dut_total_minutes > 0 else 0
  dut_attack_dribbles_90 = (dut_att_dribbles_completed / dut_total_minutes * 90)

  dut_mid = dut_data[dut_data['traits'] == 'MIDFIELD']
  dut_mid_total_minutes = dut_mid['minutes'].sum()
  dut_mid_pass_acc = dut_mid['passing accuracy in %'].mean()
  dut_mid_cont = (dut_mid["goals scored"] + dut_mid["assist"]).sum()
  dut_mid_long_balls_completed = dut_mid['long balls completed'].sum()
  dut_mid_long_balls = dut_mid['long balls'].sum()
  dut_mid_key_passes_total = dut_mid['key passes'].sum()
  dut_mid_dribbles_completed = dut_mid['dribbles completed'].sum()
  dut_mid_dribbles_attempted = dut_mid['dribbles attempt'].sum()
  dut_mid_touches = dut_mid['touches'].sum()
  dut_mid_def = (dut_mid['tackles'] + dut_mid["interceptions"]).sum()
  dut_mid_tackle = dut_mid['tackles'].sum()
  dut_mid_interceptions = dut_mid['interceptions'].sum()
  dut_mid_rating = dut_mid['ratings'].mean()
  dut_midfield_long_balls_comp_90 = (dut_mid_long_balls_completed / dut_mid_total_minutes * 90) if dut_mid_total_minutes > 0 else 0
  dut_midfield_long_balls_90 = (dut_mid_long_balls / dut_mid_total_minutes * 90) if dut_mid_total_minutes > 0 else 0
  dut_midfield_cont_90 = (dut_mid_cont / dut_mid_total_minutes * 90) if dut_mid_total_minutes > 0 else 0
  dut_midfield_touches_90 = (dut_mid_touches / dut_mid_total_minutes * 90) if dut_mid_total_minutes > 0 else 0
  dut_midfield_def_90 = (dut_mid_def / dut_mid_total_minutes * 90) if dut_mid_total_minutes > 0 else 0
  dut_midfield_dribbles_90 = (dut_mid_dribbles_completed / dut_mid_total_minutes * 90)
  dut_midfield_key_passes_90 = (dut_mid_key_passes_total / dut_mid_total_minutes * 90) if dut_mid_total_minutes > 0 else 0
  dut_midfield_tackle_90 = (dut_mid_tackle / dut_mid_total_minutes * 90) if dut_mid_total_minutes > 0 else 0
  dut_midfield_interceptions_90 = (dut_mid_interceptions / dut_mid_total_minutes * 90) if dut_mid_total_minutes > 0 else 0
  dut_midfield_pass_acc_90 = (dut_mid_pass_acc / dut_mid_total_minutes * 90) if dut_mid_total_minutes > 0 else 0

  dut_def = dut_data[dut_data['traits'] == 'DEFENCE']
  dut_def_total_minutes_2 = dut_def['minutes'].sum()
  dut_def_duels = dut_def["duels won"].sum()
  dut_def_clearances = dut_def["clearances"].sum()
  dut_def_blocks = dut_def['blocks'].sum()
  dut_def_take_ons_conceeded = dut_def['take-ons conceeded'].sum()
  dut_def_tackle = dut_def['tackles'].sum()
  dut_def_interceptions = dut_def['interceptions'].sum()
  dut_def_rating = dut_def['ratings'].mean()
  dut_def_duels_won_pct = (dut_def['duels won'].sum() /
                                (dut_def['duels won'].sum() + dut_def['take-ons conceeded'].sum() + 1e-5))
  dut_def_cards = ((dut_def['yellow card'].sum() + 2 * dut_def['red card'].sum())
                                    / (dut_def_total_minutes_2 / 90)) if dut_def_total_minutes_2 > 0 else 0

  dut_defence_duels_90 = (dut_def_duels / dut_def_total_minutes_2 * 90) if dut_def_total_minutes_2 > 0 else 0
  dut_defence_clearance_90 = (dut_def_clearances / dut_def_total_minutes_2 * 90) if dut_def_total_minutes_2 > 0 else 0
  dut_defence_blocks_90 = (dut_def_blocks / dut_def_total_minutes_2 * 90) if dut_def_total_minutes_2 > 0 else 0
  dut_defence_take_ons_conceed_90 = (dut_def_take_ons_conceeded / dut_def_total_minutes_2 * 90) if dut_def_total_minutes_2 > 0 else 0
  dut_defence_tackle_90 = (dut_def_tackle / dut_def_total_minutes_2 * 90) if dut_def_total_minutes_2 > 0 else 0
  dut_defence_interceptions_90 = (dut_def_interceptions / dut_def_total_minutes_2 * 90)
  dut_total_minutes = dut_data['minutes'].sum()
  dut_depth_players = dut_data["players"].nunique() # unique players with no repetation
  dut_matches = (dut_data["opponent"].nunique())*2
  dut_player_min = dut_data.groupby("players")["minutes"].sum()
  dut_depth_60 = (dut_player_min > 60).sum()
  dut_depth_45 = (dut_player_min > 45).sum()
  dut_depth_ratings = dut_data.groupby("players")["ratings"].mean()
  dut_depth_ratings_mean = dut_data["ratings"].mean()
  dut_depth_rate_std = dut_depth_ratings.std()
  dut_depth_avg_min = dut_total_minutes / dut_depth_players if dut_depth_players > 0 else 0
  dut_depth_rating_15 = dut_data.nlargest(15, 'minutes')['ratings'].mean()
  dut_depth_index = (dut_depth_players * dut_depth_rating_15) / (1 + dut_depth_rate_std)
  dut_depth_min_pct_11 = dut_data.nlargest(11, 'minutes')['minutes'].sum() / dut_total_minutes * 100
  dut_depth_avg_min_per_match = dut_depth_avg_min/dut_matches

  # FRENCH

  fra_data = pd.read_csv("data/france_stats.csv")
  fra_data = fra_data.dropna()
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  fra_data["traits"] = fra_data["position"].apply(func)
  col = []
  for i in esp_data.columns:
    col.append(i)
  abc8 = fra_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  fra_abc = pd.DataFrame({
    "position":abc8.index.get_level_values(1),
    "minutes":abc8["minutes"],
    "ratings":abc8["ratings"],
    "goals scored":abc8["goals scored"],
    "assist":abc8["assist"],
    "shots on target":abc8["shots on target"],
    "shots attempted":abc8["shots attempted"],
    "long balls":abc8["long balls"],
    "long balls completed":abc8["long balls completed"],
    "key passes":abc8["key passes"],
    "duels won":abc8["duels won"],
    "take-ons conceeded":abc8["take-ons conceeded"],
    "tackles":abc8["tackles"],
    "interceptions":abc8["interceptions"],
    "clearances":abc8["clearances"],
    "blocks":abc8["blocks"],
    "dribbles completed":abc8["dribbles completed"],
    "dribbles attempt":abc8["dribbles attempt"],
    "yellow card":abc8["yellow card"],
    "red card":abc8["red card"],
    "nationality": ["France"] * len(abc8)
})
  fra_total_minutes = fra_data['minutes'].sum()
  fra_overall_rating = (fra_data['ratings'] * fra_data['minutes']).sum()
  fra_squad_quality = fra_overall_rating / fra_total_minutes

  fra_rate_std = fra_data['ratings'].std()

  fra_top11 = fra_data.nlargest(11,'minutes')
  fra_squad_quality11 = fra_top11['ratings'].mean()

  fra_att = fra_data[fra_data['traits'] == 'ATTACK']
  fra_total_minutes = fra_att['minutes'].sum()
  fra_att_goals = fra_att["goals scored"].sum()
  fra_att_assist = fra_att["assist"].sum()
  fra_att_cont = (fra_att["goals scored"] + fra_att["assist"]).sum()
  fra_att_shots_on_target = fra_att['shots on target'].sum()
  fra_att_shots_attempted = fra_att['shots attempted'].sum()
  fra_att_key_passes_total = fra_att['key passes'].sum()
  fra_att_dribbles_completed = fra_att['dribbles completed'].sum()
  fra_att_dribbles_attempted = fra_att['dribbles attempt'].sum()
  fra_att_rating = fra_att['ratings'].mean()
  fra_attack_goals_90 = ((fra_att_goals / fra_total_minutes) * 90) if fra_total_minutes > 0 else 0
  fra_attack_assist_90 = (fra_att_assist / fra_total_minutes * 90) if fra_total_minutes > 0 else 0
  fra_attack_cont_90 = (fra_att_cont / fra_total_minutes * 90) if fra_total_minutes > 0 else 0
  fra_attack_shots_90 = (fra_att_shots_on_target / fra_total_minutes * 90) if fra_total_minutes > 0 else 0
  fra_attack_key_passes_90 = (fra_att_key_passes_total / fra_total_minutes * 90) if fra_total_minutes > 0 else 0
  fra_attack_dribbles_90 = (fra_att_dribbles_completed / fra_total_minutes * 90)

  fra_mid = fra_data[fra_data['traits'] == 'MIDFIELD']
  fra_mid_total_minutes = fra_mid['minutes'].sum()
  fra_mid_pass_acc = fra_mid['passing accuracy in %'].mean()
  fra_mid_cont = (fra_mid["goals scored"] + fra_mid["assist"]).sum()
  fra_mid_long_balls_completed = fra_mid['long balls completed'].sum()
  fra_mid_long_balls = fra_mid['long balls'].sum()
  fra_mid_key_passes_total = fra_mid['key passes'].sum()
  fra_mid_dribbles_completed = fra_mid['dribbles completed'].sum()
  fra_mid_dribbles_attempted = fra_mid['dribbles attempt'].sum()
  fra_mid_touches = fra_mid['touches'].sum()
  fra_mid_def = (fra_mid['tackles'] + fra_mid["interceptions"]).sum()
  fra_mid_tackle = fra_mid['tackles'].sum()
  fra_mid_interceptions = fra_mid['interceptions'].sum()
  fra_mid_rating = fra_mid['ratings'].mean()
  fra_midfield_long_balls_comp_90 = (fra_mid_long_balls_completed / fra_mid_total_minutes * 90) if fra_mid_total_minutes > 0 else 0
  fra_midfield_long_balls_90 = (fra_mid_long_balls / fra_mid_total_minutes * 90) if fra_mid_total_minutes > 0 else 0
  fra_midfield_cont_90 = (fra_mid_cont / fra_mid_total_minutes * 90) if fra_mid_total_minutes > 0 else 0
  fra_midfield_touches_90 = (fra_mid_touches / fra_mid_total_minutes * 90) if fra_mid_total_minutes > 0 else 0
  fra_midfield_def_90 = (fra_mid_def / fra_mid_total_minutes * 90) if fra_mid_total_minutes > 0 else 0
  fra_midfield_dribbles_90 = (fra_mid_dribbles_completed / fra_mid_total_minutes * 90)
  fra_midfield_key_passes_90 = (fra_mid_key_passes_total / fra_mid_total_minutes * 90) if fra_mid_total_minutes > 0 else 0
  fra_midfield_tackle_90 = (fra_mid_tackle / fra_mid_total_minutes * 90) if fra_mid_total_minutes > 0 else 0
  fra_midfield_interceptions_90 = (fra_mid_interceptions / fra_mid_total_minutes * 90) if fra_mid_total_minutes > 0 else 0
  fra_midfield_pass_acc_90 = (fra_mid_pass_acc / fra_mid_total_minutes * 90) if fra_mid_total_minutes > 0 else 0

  fra_def = fra_data[fra_data['traits'] == 'DEFENCE']
  fra_def_total_minutes_2 = fra_def['minutes'].sum()
  fra_def_duels = fra_def["duels won"].sum()
  fra_def_clearances = fra_def["clearances"].sum()
  fra_def_blocks = fra_def['blocks'].sum()
  fra_def_take_ons_conceeded = fra_def['take-ons conceeded'].sum()
  fra_def_tackle = fra_def['tackles'].sum()
  fra_def_interceptions = fra_def['interceptions'].sum()
  fra_def_rating = fra_def['ratings'].mean()
  fra_def_duels_won_pct = (fra_def['duels won'].sum() /
                                  (fra_def['duels won'].sum() + fra_def['take-ons conceeded'].sum() + 1e-5))
  fra_def_cards = ((fra_def['yellow card'].sum() + 2 * fra_def['red card'].sum())
                                      / (fra_def_total_minutes_2 / 90)) if fra_def_total_minutes_2 > 0 else 0

  fra_defence_duels_90 = (fra_def_duels / fra_def_total_minutes_2 * 90) if fra_def_total_minutes_2 > 0 else 0
  fra_defence_clearance_90 = (fra_def_clearances / fra_def_total_minutes_2 * 90) if fra_def_total_minutes_2 > 0 else 0
  fra_defence_blocks_90 = (fra_def_blocks / fra_def_total_minutes_2 * 90) if fra_def_total_minutes_2 > 0 else 0
  fra_defence_take_ons_conceed_90 = (fra_def_take_ons_conceeded / fra_def_total_minutes_2 * 90) if fra_def_total_minutes_2 > 0 else 0
  fra_defence_tackle_90 = (fra_def_tackle / fra_def_total_minutes_2 * 90) if fra_def_total_minutes_2 > 0 else 0
  fra_defence_interceptions_90 = (fra_def_interceptions / fra_def_total_minutes_2 * 90)
  fra_total_minutes = fra_data['minutes'].sum()
  fra_depth_players = fra_data["players"].nunique() # unique players with no repetation
  fra_matches = (fra_data["opponent"].nunique())*2
  fra_player_min = fra_data.groupby("players")["minutes"].sum()
  fra_depth_60 = (fra_player_min > 60).sum()
  fra_depth_45 = (fra_player_min > 45).sum()
  fra_depth_ratings = fra_data.groupby("players")["ratings"].mean()
  fra_depth_ratings_mean = fra_data["ratings"].mean()
  fra_depth_rate_std = fra_depth_ratings.std()
  fra_depth_avg_min = fra_total_minutes / fra_depth_players if fra_depth_players > 0 else 0
  fra_depth_rating_15 = fra_data.nlargest(15, 'minutes')['ratings'].mean()
  fra_depth_index = (fra_depth_players * fra_depth_rating_15) / (1 + fra_depth_rate_std)
  fra_depth_min_pct_11 = fra_data.nlargest(11, 'minutes')['minutes'].sum() / fra_total_minutes * 100
  fra_depth_avg_min_per_match = fra_depth_avg_min / fra_matches


  # GERMANY


  ger_data = pd.read_csv("data/Germany_stats.csv")
  
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  ger_data["traits"] = ger_data["position"].apply(func)
  col = []
  for i in esp_data.columns:
    col.append(i)
  abc9 = ger_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  ger_abc = pd.DataFrame({
    "position":abc9.index.get_level_values(1),
    "minutes":abc9["minutes"],
    "ratings":abc9["ratings"],
    "goals scored":abc9["goals scored"],
    "assist":abc9["assist"],
    "shots on target":abc9["shots on target"],
    "shots attempted":abc9["shots attempted"],
    "long balls":abc9["long balls"],
    "long balls completed":abc9["long balls completed"],
    "key passes":abc9["key passes"],
    "duels won":abc9["duels won"],
    "take-ons conceeded":abc9["take-ons conceeded"],
    "tackles":abc9["tackles"],
    "interceptions":abc9["interceptions"],
    "clearances":abc9["clearances"],
    "blocks":abc9["blocks"],
    "dribbles completed":abc9["dribbles completed"],
    "dribbles attempt":abc9["dribbles attempt"],
    "yellow card":abc9["yellow card"],
    "red card":abc9["red card"],
    "nationality": ["Germany"] * len(abc9)
})
  ger_total_minutes = ger_data['minutes'].sum()
  ger_overall_rating = (ger_data['ratings'] * ger_data['minutes']).sum()
  ger_squad_quality = ger_overall_rating / ger_total_minutes
  ger_rate_std = ger_data['ratings'].std()
  ger_top11 = ger_data.nlargest(11,'minutes')
  ger_squad_quality11 = ger_top11['ratings'].mean()

  ger_att = ger_data[ger_data['traits'] == 'ATTACK']
  ger_total_minutes = ger_att['minutes'].sum()
  ger_att_goals = ger_att["goals scored"].sum()
  ger_att_assist = ger_att["assist"].sum()
  ger_att_cont = (ger_att["goals scored"] + ger_att["assist"]).sum()
  ger_att_shots_on_target = ger_att['shots on target'].sum()
  ger_att_shots_attempted = ger_att['shots attempted'].sum()
  ger_att_key_passes_total = ger_att['key passes'].sum()
  ger_att_dribbles_completed = ger_att['dribbles completed'].sum()
  ger_att_dribbles_attempted = ger_att['dribbles attempt'].sum()
  ger_att_rating = ger_att['ratings'].mean()
  ger_attack_goals_90 = ((ger_att_goals / ger_total_minutes) * 90) if ger_total_minutes > 0 else 0
  ger_attack_assist_90 = (ger_att_assist / ger_total_minutes * 90) if ger_total_minutes > 0 else 0
  ger_attack_cont_90 = (ger_att_cont / ger_total_minutes * 90) if ger_total_minutes > 0 else 0
  ger_attack_shots_90 = (ger_att_shots_on_target / ger_total_minutes * 90) if ger_total_minutes > 0 else 0
  ger_attack_key_passes_90 = (ger_att_key_passes_total / ger_total_minutes * 90) if ger_total_minutes > 0 else 0
  ger_attack_dribbles_90 = (ger_att_dribbles_completed / ger_total_minutes * 90)

  ger_mid = ger_data[ger_data['traits'] == 'MIDFIELD']
  ger_mid_total_minutes = ger_mid['minutes'].sum()
  ger_mid_pass_acc = ger_mid['passing accuracy in %'].mean()
  ger_mid_cont = (ger_mid["goals scored"] + ger_mid["assist"]).sum()
  ger_mid_long_balls_completed = ger_mid['long balls completed'].sum()
  ger_mid_long_balls = ger_mid['long balls'].sum()
  ger_mid_key_passes_total = ger_mid['key passes'].sum()
  ger_mid_dribbles_completed = ger_mid['dribbles completed'].sum()
  ger_mid_dribbles_attempted = ger_mid['dribbles attempt'].sum()
  ger_mid_touches = ger_mid['touches'].sum()
  ger_mid_def = (ger_mid['tackles'] + ger_mid["interceptions"]).sum()
  ger_mid_tackle = ger_mid['tackles'].sum()
  ger_mid_interceptions = ger_mid['interceptions'].sum()
  ger_mid_rating = ger_mid['ratings'].mean()
  ger_midfield_long_balls_comp_90 = (ger_mid_long_balls_completed / ger_mid_total_minutes * 90) if ger_mid_total_minutes > 0 else 0
  ger_midfield_long_balls_90 = (ger_mid_long_balls / ger_mid_total_minutes * 90) if ger_mid_total_minutes > 0 else 0
  ger_midfield_cont_90 = (ger_mid_cont / ger_mid_total_minutes * 90) if ger_mid_total_minutes > 0 else 0
  ger_midfield_touches_90 = (ger_mid_touches / ger_mid_total_minutes * 90) if ger_mid_total_minutes > 0 else 0
  ger_midfield_def_90 = (ger_mid_def / ger_mid_total_minutes * 90) if ger_mid_total_minutes > 0 else 0
  ger_midfield_dribbles_90 = (ger_mid_dribbles_completed / ger_mid_total_minutes * 90)
  ger_midfield_key_passes_90 = (ger_mid_key_passes_total / ger_mid_total_minutes * 90) if ger_mid_total_minutes > 0 else 0
  ger_midfield_tackle_90 = (ger_mid_tackle / ger_mid_total_minutes * 90) if ger_mid_total_minutes > 0 else 0
  ger_midfield_interceptions_90 = (ger_mid_interceptions / ger_mid_total_minutes * 90) if ger_mid_total_minutes > 0 else 0
  ger_midfield_pass_acc_90 = (ger_mid_pass_acc / ger_mid_total_minutes * 90) if ger_mid_total_minutes > 0 else 0

  ger_def = ger_data[ger_data['traits'] == 'DEFENCE']
  ger_def_total_minutes_2 = ger_def['minutes'].sum()
  ger_def_duels = ger_def["duels won"].sum()
  ger_def_clearances = ger_def["clearances"].sum()
  ger_def_blocks = ger_def['blocks'].sum()
  ger_def_take_ons_conceeded = ger_def['take-ons conceeded'].sum()
  ger_def_tackle = ger_def['tackles'].sum()
  ger_def_interceptions = ger_def['interceptions'].sum()
  ger_def_rating = ger_def['ratings'].mean()
  ger_def_duels_won_pct = (ger_def['duels won'].sum() /
                                  (ger_def['duels won'].sum() + ger_def['take-ons conceeded'].sum() + 1e-5))
  ger_def_cards = ((ger_def['yellow card'].sum() + 2 * ger_def['red card'].sum())
                                      / (ger_def_total_minutes_2 / 90)) if ger_def_total_minutes_2 > 0 else 0

  ger_defence_duels_90 = (ger_def_duels / ger_def_total_minutes_2 * 90) if ger_def_total_minutes_2 > 0 else 0
  ger_defence_clearance_90 = (ger_def_clearances / ger_def_total_minutes_2 * 90) if ger_def_total_minutes_2 > 0 else 0
  ger_defence_blocks_90 = (ger_def_blocks / ger_def_total_minutes_2 * 90) if ger_def_total_minutes_2 > 0 else 0
  ger_defence_take_ons_conceed_90 = (ger_def_take_ons_conceeded / ger_def_total_minutes_2 * 90) if ger_def_total_minutes_2 > 0 else 0
  ger_defence_tackle_90 = (ger_def_tackle / ger_def_total_minutes_2 * 90) if ger_def_total_minutes_2 > 0 else 0
  ger_defence_interceptions_90 = (ger_def_interceptions / ger_def_total_minutes_2 * 90)
  ger_total_minutes = ger_data['minutes'].sum()
  ger_depth_players = ger_data["players"].nunique() # unique players with no repetation
  ger_matches = (ger_data["opponent"].nunique())*2
  ger_player_min = ger_data.groupby("players")["minutes"].sum()
  ger_depth_60 = (ger_player_min > 60).sum()
  ger_depth_45 = (ger_player_min > 45).sum()
  ger_depth_ratings = ger_data.groupby("players")["ratings"].mean()
  ger_depth_ratings_mean = ger_data["ratings"].mean()
  ger_depth_rate_std = ger_depth_ratings.std()
  ger_depth_avg_min = ger_total_minutes / ger_depth_players if ger_depth_players > 0 else 0
  ger_depth_rating_15 = ger_data.nlargest(15, 'minutes')['ratings'].mean()
  ger_depth_index = (ger_depth_players * ger_depth_rating_15) / (1 + ger_depth_rate_std)
  ger_depth_min_pct_11 = ger_data.nlargest(11, 'minutes')['minutes'].sum() / ger_total_minutes * 100
  ger_depth_avg_min_per_match = ger_depth_avg_min/ger_matches


  # ENGLAND


  eng_data = pd.read_csv("data/England_stats.csv")
  eng_data = eng_data.dropna()
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  eng_data["traits"] = eng_data["position"].apply(func)
  col = []
  for i in esp_data.columns:
    col.append(i)
  abc10 = eng_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  eng_abc = pd.DataFrame({
    "position":abc10.index.get_level_values(1),
    "minutes":abc10["minutes"],
    "ratings":abc10["ratings"],
    "goals scored":abc10["goals scored"],
    "assist":abc10["assist"],
    "shots on target":abc10["shots on target"],
    "shots attempted":abc10["shots attempted"],
    "long balls":abc10["long balls"],
    "long balls completed":abc10["long balls completed"],
    "key passes":abc10["key passes"],
    "duels won":abc10["duels won"],
    "take-ons conceeded":abc10["take-ons conceeded"],
    "tackles":abc10["tackles"],
    "interceptions":abc10["interceptions"],
    "clearances":abc10["clearances"],
    "blocks":abc10["blocks"],
    "dribbles completed":abc10["dribbles completed"],
    "dribbles attempt":abc10["dribbles attempt"],
    "yellow card":abc10["yellow card"],
    "red card":abc10["red card"],
    "nationality": ["England"] * len(abc10)
})
  eng_total_minutes = eng_data['minutes'].sum()
  eng_overall_rating = (eng_data['ratings'] * eng_data['minutes']).sum()
  eng_squad_quality = eng_overall_rating / eng_total_minutes
  eng_rate_std = eng_data['ratings'].std()
  eng_top11 = eng_data.nlargest(11,'minutes')
  eng_squad_quality11 = eng_top11['ratings'].mean()

  eng_att = eng_data[eng_data['traits'] == 'ATTACK']
  eng_total_minutes = eng_att['minutes'].sum()
  eng_att_goals = eng_att["goals scored"].sum()
  eng_att_assist = eng_att["assist"].sum()
  eng_att_cont = (eng_att["goals scored"] + eng_att["assist"]).sum()
  eng_att_shots_on_target = eng_att['shots on target'].sum()
  eng_att_shots_attempted = eng_att['shots attempted'].sum()
  eng_att_key_passes_total = eng_att['key passes'].sum()
  eng_att_dribbles_completed = eng_att['dribbles completed'].sum()
  eng_att_dribbles_attempted = eng_att['dribbles attempt'].sum()
  eng_att_rating = eng_att['ratings'].mean()
  eng_attack_goals_90 = ((eng_att_goals / eng_total_minutes) * 90) if eng_total_minutes > 0 else 0
  eng_attack_assist_90 = (eng_att_assist / eng_total_minutes * 90) if eng_total_minutes > 0 else 0
  eng_attack_cont_90 = (eng_att_cont / eng_total_minutes * 90) if eng_total_minutes > 0 else 0
  eng_attack_shots_90 = (eng_att_shots_on_target / eng_total_minutes * 90) if eng_total_minutes > 0 else 0
  eng_attack_key_passes_90 = (eng_att_key_passes_total / eng_total_minutes * 90) if eng_total_minutes > 0 else 0
  eng_attack_dribbles_90 = (eng_att_dribbles_completed / eng_total_minutes * 90)

  eng_mid = eng_data[eng_data['traits'] == 'MIDFIELD']
  eng_mid_total_minutes = eng_mid['minutes'].sum()
  eng_mid_pass_acc = eng_mid['passing accuracy in %'].mean()
  eng_mid_cont = (eng_mid["goals scored"] + eng_mid["assist"]).sum()
  eng_mid_long_balls_completed = eng_mid['long balls completed'].sum()
  eng_mid_long_balls = eng_mid['long balls'].sum()
  eng_mid_key_passes_total = eng_mid['key passes'].sum()
  eng_mid_dribbles_completed = eng_mid['dribbles completed'].sum()
  eng_mid_dribbles_attempted = eng_mid['dribbles attempt'].sum()
  eng_mid_touches = eng_mid['touches'].sum()
  eng_mid_def = (eng_mid['tackles'] + eng_mid["interceptions"]).sum()
  eng_mid_tackle = eng_mid['tackles'].sum()
  eng_mid_interceptions = eng_mid['interceptions'].sum()
  eng_mid_rating = eng_mid['ratings'].mean()
  eng_midfield_long_balls_comp_90 = (eng_mid_long_balls_completed / eng_mid_total_minutes * 90) if eng_mid_total_minutes > 0 else 0
  eng_midfield_long_balls_90 = (eng_mid_long_balls / eng_mid_total_minutes * 90) if eng_mid_total_minutes > 0 else 0
  eng_midfield_cont_90 = (eng_mid_cont / eng_mid_total_minutes * 90) if eng_mid_total_minutes > 0 else 0
  eng_midfield_touches_90 = (eng_mid_touches / eng_mid_total_minutes * 90) if eng_mid_total_minutes > 0 else 0
  eng_midfield_def_90 = (eng_mid_def / eng_mid_total_minutes * 90) if eng_mid_total_minutes > 0 else 0
  eng_midfield_dribbles_90 = (eng_mid_dribbles_completed / eng_mid_total_minutes * 90)
  eng_midfield_key_passes_90 = (eng_mid_key_passes_total / eng_mid_total_minutes * 90) if eng_mid_total_minutes > 0 else 0
  eng_midfield_tackle_90 = (eng_mid_tackle / eng_mid_total_minutes * 90) if eng_mid_total_minutes > 0 else 0
  eng_midfield_interceptions_90 = (eng_mid_interceptions / eng_mid_total_minutes * 90) if eng_mid_total_minutes > 0 else 0
  eng_midfield_pass_acc_90 = (eng_mid_pass_acc / eng_mid_total_minutes * 90) if eng_mid_total_minutes > 0 else 0

  eng_def = eng_data[eng_data['traits'] == 'DEFENCE']
  eng_def_total_minutes_2 = eng_def['minutes'].sum()
  eng_def_duels = eng_def["duels won"].sum()
  eng_def_clearances = eng_def["clearances"].sum()
  eng_def_blocks = eng_def['blocks'].sum()
  eng_def_take_ons_conceeded = eng_def['take-ons conceeded'].sum()
  eng_def_tackle = eng_def['tackles'].sum()
  eng_def_interceptions = eng_def['interceptions'].sum()
  eng_def_rating = eng_def['ratings'].mean()
  eng_def_duels_won_pct = (eng_def['duels won'].sum() /
                                  (eng_def['duels won'].sum() + eng_def['take-ons conceeded'].sum() + 1e-5))
  eng_def_cards = ((eng_def['yellow card'].sum() + 2 * eng_def['red card'].sum())
                                      / (eng_def_total_minutes_2 / 90)) if eng_def_total_minutes_2 > 0 else 0

  eng_defence_duels_90 = (eng_def_duels / eng_def_total_minutes_2 * 90) if eng_def_total_minutes_2 > 0 else 0
  eng_defence_clearance_90 = (eng_def_clearances / eng_def_total_minutes_2 * 90) if eng_def_total_minutes_2 > 0 else 0
  eng_defence_blocks_90 = (eng_def_blocks / eng_def_total_minutes_2 * 90) if eng_def_total_minutes_2 > 0 else 0
  eng_defence_take_ons_conceed_90 = (eng_def_take_ons_conceeded / eng_def_total_minutes_2 * 90) if eng_def_total_minutes_2 > 0 else 0
  eng_defence_tackle_90 = (eng_def_tackle / eng_def_total_minutes_2 * 90) if eng_def_total_minutes_2 > 0 else 0
  eng_defence_interceptions_90 = (eng_def_interceptions / eng_def_total_minutes_2 * 90)
  eng_total_minutes = eng_data['minutes'].sum()
  eng_depth_players = eng_data["players"].nunique() # unique players with no repetation
  eng_matches = (eng_data["opponent"].nunique())*2
  eng_player_min = eng_data.groupby("players")["minutes"].sum()
  eng_depth_60 = (eng_player_min > 60).sum()
  eng_depth_45 = (eng_player_min > 45).sum()
  eng_depth_ratings = eng_data.groupby("players")["ratings"].mean()
  eng_depth_ratings_mean = eng_data["ratings"].mean()
  eng_depth_rate_std = eng_depth_ratings.std()
  eng_depth_avg_min = eng_total_minutes / eng_depth_players if eng_depth_players > 0 else 0
  eng_depth_rating_15 = eng_data.nlargest(15, 'minutes')['ratings'].mean()
  eng_depth_index = (eng_depth_players * eng_depth_rating_15) / (1 + eng_depth_rate_std)
  eng_depth_min_pct_11 = eng_data.nlargest(11, 'minutes')['minutes'].sum() / eng_total_minutes * 100
  eng_depth_avg_min_per_match = eng_depth_avg_min/eng_matches


  # MOROCCO


  mor_data = pd.read_csv("data/Morroco_stats.csv")
  mor_data = mor_data.dropna()
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  mor_data["traits"] = mor_data["position"].apply(func)
  col = []
  for i in mor_data.columns:
    col.append(i)
  abc11 = mor_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  mor_abc = pd.DataFrame({
    "position":abc11.index.get_level_values(1),
    "minutes":abc11["minutes"],
    "ratings":abc11["ratings"],
    "goals scored":abc11["goals scored"],
    "assist":abc11["assist"],
    "shots on target":abc11["shots on target"],
    "shots attempted":abc11["shots attempted"],
    "long balls":abc11["long balls"],
    "long balls completed":abc11["long balls completed"],
    "key passes":abc11["key passes"],
    "duels won":abc11["duels won"],
    "take-ons conceeded":abc11["take-ons conceeded"],
    "tackles":abc11["tackles"],
    "interceptions":abc11["interceptions"],
    "clearances":abc11["clearances"],
    "blocks":abc11["blocks"],
    "dribbles completed":abc11["dribbles completed"],
    "dribbles attempt":abc11["dribbles attempt"],
    "yellow card":abc11["yellow card"],
    "red card":abc11["red card"],
    "nationality": ["Morocco"] * len(abc11)
})
  mor_total_minutes = mor_data['minutes'].sum()
  mor_overall_rating = (mor_data['ratings'] * mor_data['minutes']).sum()
  mor_squad_quality = mor_overall_rating / mor_total_minutes
  mor_rate_std = mor_data['ratings'].std()
  mor_top11 = mor_data.nlargest(11,'minutes')
  mor_squad_quality11 = mor_top11['ratings'].mean()

  mor_att = mor_data[mor_data['traits'] == 'ATTACK']
  mor_total_minutes = mor_att['minutes'].sum()
  mor_att_goals = mor_att["goals scored"].sum()
  mor_att_assist = mor_att["assist"].sum()
  mor_att_cont = (mor_att["goals scored"] + mor_att["assist"]).sum()
  mor_att_shots_on_target = mor_att['shots on target'].sum()
  mor_att_shots_attempted = mor_att['shots attempted'].sum()
  mor_att_key_passes_total = mor_att['key passes'].sum()
  mor_att_dribbles_completed = mor_att['dribbles completed'].sum()
  mor_att_dribbles_attempted = mor_att['dribbles attempt'].sum()
  mor_att_rating = mor_att['ratings'].mean()
  mor_attack_goals_90 = ((mor_att_goals / mor_total_minutes) * 90) if mor_total_minutes > 0 else 0
  mor_attack_assist_90 = (mor_att_assist / mor_total_minutes * 90) if mor_total_minutes > 0 else 0
  mor_attack_cont_90 = (mor_att_cont / mor_total_minutes * 90) if mor_total_minutes > 0 else 0
  mor_attack_shots_90 = (mor_att_shots_on_target / mor_total_minutes * 90) if mor_total_minutes > 0 else 0
  mor_attack_key_passes_90 = (mor_att_key_passes_total / mor_total_minutes * 90) if mor_total_minutes > 0 else 0
  mor_attack_dribbles_90 = (mor_att_dribbles_completed / mor_total_minutes * 90)

  mor_mid = mor_data[mor_data['traits'] == 'MIDFIELD']
  mor_mid_total_minutes = mor_mid['minutes'].sum()
  mor_mid_pass_acc = mor_mid['passing accuracy in %'].mean()
  mor_mid_cont = (mor_mid["goals scored"] + mor_mid["assist"]).sum()
  mor_mid_long_balls_completed = mor_mid['long balls completed'].sum()
  mor_mid_long_balls = mor_mid['long balls'].sum()
  mor_mid_key_passes_total = mor_mid['key passes'].sum()
  mor_mid_dribbles_completed = mor_mid['dribbles completed'].sum()
  mor_mid_dribbles_attempted = mor_mid['dribbles attempt'].sum()
  mor_mid_touches = mor_mid['touches'].sum()
  mor_mid_def = (mor_mid['tackles'] + mor_mid["interceptions"]).sum()
  mor_mid_tackle = mor_mid['tackles'].sum()
  mor_mid_interceptions = mor_mid['interceptions'].sum()
  mor_mid_rating = mor_mid['ratings'].mean()
  mor_midfield_long_balls_comp_90 = (mor_mid_long_balls_completed / mor_mid_total_minutes * 90) if mor_mid_total_minutes > 0 else 0
  mor_midfield_long_balls_90 = (mor_mid_long_balls / mor_mid_total_minutes * 90) if mor_mid_total_minutes > 0 else 0
  mor_midfield_cont_90 = (mor_mid_cont / mor_mid_total_minutes * 90) if mor_mid_total_minutes > 0 else 0
  mor_midfield_touches_90 = (mor_mid_touches / mor_mid_total_minutes * 90) if mor_mid_total_minutes > 0 else 0
  mor_midfield_def_90 = (mor_mid_def / mor_mid_total_minutes * 90) if mor_mid_total_minutes > 0 else 0
  mor_midfield_dribbles_90 = (mor_mid_dribbles_completed / mor_mid_total_minutes * 90)
  mor_midfield_key_passes_90 = (mor_mid_key_passes_total / mor_mid_total_minutes * 90) if mor_mid_total_minutes > 0 else 0
  mor_midfield_tackle_90 = (mor_mid_tackle / mor_mid_total_minutes * 90) if mor_mid_total_minutes > 0 else 0
  mor_midfield_interceptions_90 = (mor_mid_interceptions / mor_mid_total_minutes * 90) if mor_mid_total_minutes > 0 else 0
  mor_midfield_pass_acc_90 = (mor_mid_pass_acc / mor_mid_total_minutes * 90) if mor_mid_total_minutes > 0 else 0

  mor_def = mor_data[mor_data['traits'] == 'DEFENCE']
  mor_def_total_minutes_2 = mor_def['minutes'].sum()
  mor_def_duels = mor_def["duels won"].sum()
  mor_def_clearances = mor_def["clearances"].sum()
  mor_def_blocks = mor_def['blocks'].sum()
  mor_def_take_ons_conceeded = mor_def['take-ons conceeded'].sum()
  mor_def_tackle = mor_def['tackles'].sum()
  mor_def_interceptions = mor_def['interceptions'].sum()
  mor_def_rating = mor_def['ratings'].mean()
  mor_def_duels_won_pct = (mor_def['duels won'].sum() /
                                  (mor_def['duels won'].sum() + mor_def['take-ons conceeded'].sum() + 1e-5))
  mor_def_cards = ((mor_def['yellow card'].sum() + 2 * mor_def['red card'].sum())
                                      / (mor_def_total_minutes_2 / 90)) if mor_def_total_minutes_2 > 0 else 0

  mor_defence_duels_90 = (mor_def_duels / mor_def_total_minutes_2 * 90) if mor_def_total_minutes_2 > 0 else 0
  mor_defence_clearance_90 = (mor_def_clearances / mor_def_total_minutes_2 * 90) if mor_def_total_minutes_2 > 0 else 0
  mor_defence_blocks_90 = (mor_def_blocks / mor_def_total_minutes_2 * 90) if mor_def_total_minutes_2 > 0 else 0
  mor_defence_take_ons_conceed_90 = (mor_def_take_ons_conceeded / mor_def_total_minutes_2 * 90) if mor_def_total_minutes_2 > 0 else 0
  mor_defence_tackle_90 = (mor_def_tackle / mor_def_total_minutes_2 * 90) if mor_def_total_minutes_2 > 0 else 0
  mor_defence_interceptions_90 = (mor_def_interceptions / mor_def_total_minutes_2 * 90)

  mor_total_minutes = mor_data['minutes'].sum()
  mor_depth_players = mor_data["players"].nunique()
  mor_matches = (mor_data["opponent"].nunique())*2
  mor_player_min = mor_data.groupby("players")["minutes"].sum()
  mor_depth_60 = (mor_player_min > 60).sum()
  mor_depth_45 = (mor_player_min > 45).sum()
  mor_depth_ratings = mor_data.groupby("players")["ratings"].mean()
  mor_depth_ratings_mean = mor_data["ratings"].mean()
  mor_depth_rate_std = mor_depth_ratings.std()
  mor_depth_avg_min = mor_total_minutes / mor_depth_players if mor_depth_players > 0 else 0
  mor_depth_rating_15 = mor_data.nlargest(15, 'minutes')['ratings'].mean()
  mor_depth_index = (mor_depth_players * mor_depth_rating_15) / (1 + mor_depth_rate_std)
  mor_depth_min_pct_11 = mor_data.nlargest(11, 'minutes')['minutes'].sum() / mor_total_minutes * 100
  mor_depth_avg_min_per_match = mor_depth_avg_min / mor_matches


  # PORTUGAL


  prt_data = pd.read_csv("data/Portugal_stats.csv")
  prt_data = prt_data.dropna()
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  prt_data["traits"] = prt_data["position"].apply(func)
  col = []
  for i in esp_data.columns:
    col.append(i)
  abc12 = prt_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  prt_abc = pd.DataFrame({
    "position":abc12.index.get_level_values(1),
    "minutes":abc12["minutes"],
    "ratings":abc12["ratings"],
    "goals scored":abc12["goals scored"],
    "assist":abc12["assist"],
    "shots on target":abc12["shots on target"],
    "shots attempted":abc12["shots attempted"],
    "long balls":abc12["long balls"],
    "long balls completed":abc12["long balls completed"],
    "key passes":abc12["key passes"],
    "duels won":abc12["duels won"],
    "take-ons conceeded":abc12["take-ons conceeded"],
    "tackles":abc12["tackles"],
    "interceptions":abc12["interceptions"],
    "clearances":abc12["clearances"],
    "blocks":abc12["blocks"],
    "dribbles completed":abc12["dribbles completed"],
    "dribbles attempt":abc12["dribbles attempt"],
    "yellow card":abc12["yellow card"],
    "red card": abc12["red card"],
    "nationality": ["Portugal"] * len(abc12)
})
  prt_total_minutes = prt_data['minutes'].sum()
  prt_overall_rating = (prt_data['ratings'] * prt_data['minutes']).sum()
  prt_squad_quality = prt_overall_rating / prt_total_minutes
  prt_rate_std = prt_data['ratings'].std()
  prt_top11 = prt_data.nlargest(11,'minutes')
  prt_squad_quality11 = prt_top11['ratings'].mean()

  prt_att = prt_data[prt_data['traits'] == 'ATTACK']
  prt_total_minutes = prt_att['minutes'].sum()
  prt_att_goals = prt_att["goals scored"].sum()
  prt_att_assist = prt_att["assist"].sum()
  prt_att_cont = (prt_att["goals scored"] + prt_att["assist"]).sum()
  prt_att_shots_on_target = prt_att['shots on target'].sum()
  prt_att_shots_attempted = prt_att['shots attempted'].sum()
  prt_att_key_passes_total = prt_att['key passes'].sum()
  prt_att_dribbles_completed = prt_att['dribbles completed'].sum()
  prt_att_dribbles_attempted = prt_att['dribbles attempt'].sum()
  prt_att_rating = prt_att['ratings'].mean()
  prt_attack_goals_90 = ((prt_att_goals / prt_total_minutes) * 90) if prt_total_minutes > 0 else 0
  prt_attack_assist_90 = (prt_att_assist / prt_total_minutes * 90) if prt_total_minutes > 0 else 0
  prt_attack_cont_90 = (prt_att_cont / prt_total_minutes * 90) if prt_total_minutes > 0 else 0
  prt_attack_shots_90 = (prt_att_shots_on_target / prt_total_minutes * 90) if prt_total_minutes > 0 else 0
  prt_attack_key_passes_90 = (prt_att_key_passes_total / prt_total_minutes * 90) if prt_total_minutes > 0 else 0
  prt_attack_dribbles_90 = (prt_att_dribbles_completed / prt_total_minutes * 90)

  prt_mid = prt_data[prt_data['traits'] == 'MIDFIELD']
  prt_mid_total_minutes = prt_mid['minutes'].sum()
  prt_mid_pass_acc = prt_mid['passing accuracy in %'].mean()
  prt_mid_cont = (prt_mid["goals scored"] + prt_mid["assist"]).sum()
  prt_mid_long_balls_completed = prt_mid['long balls completed'].sum()
  prt_mid_long_balls = prt_mid['long balls'].sum()
  prt_mid_key_passes_total = prt_mid['key passes'].sum()
  prt_mid_dribbles_completed = prt_mid['dribbles completed'].sum()
  prt_mid_dribbles_attempted = prt_mid['dribbles attempt'].sum()
  prt_mid_touches = prt_mid['touches'].sum()
  prt_mid_def = (prt_mid['tackles'] + prt_mid["interceptions"]).sum()
  prt_mid_tackle = prt_mid['tackles'].sum()
  prt_mid_interceptions = prt_mid['interceptions'].sum()
  prt_mid_rating = prt_mid['ratings'].mean()
  prt_midfield_long_balls_comp_90 = (prt_mid_long_balls_completed / prt_mid_total_minutes * 90) if prt_mid_total_minutes > 0 else 0
  prt_midfield_long_balls_90 = (prt_mid_long_balls / prt_mid_total_minutes * 90) if prt_mid_total_minutes > 0 else 0
  prt_midfield_cont_90 = (prt_mid_cont / prt_mid_total_minutes * 90) if prt_mid_total_minutes > 0 else 0
  prt_midfield_touches_90 = (prt_mid_touches / prt_mid_total_minutes * 90) if prt_mid_total_minutes > 0 else 0
  prt_midfield_def_90 = (prt_mid_def / prt_mid_total_minutes * 90) if prt_mid_total_minutes > 0 else 0
  prt_midfield_dribbles_90 = (prt_mid_dribbles_completed / prt_mid_total_minutes * 90)
  prt_midfield_key_passes_90 = (prt_mid_key_passes_total / prt_mid_total_minutes * 90) if prt_mid_total_minutes > 0 else 0
  prt_midfield_tackle_90 = (prt_mid_tackle / prt_mid_total_minutes * 90) if prt_mid_total_minutes > 0 else 0
  prt_midfield_interceptions_90 = (prt_mid_interceptions / prt_mid_total_minutes * 90) if prt_mid_total_minutes > 0 else 0
  prt_midfield_pass_acc_90 = (prt_mid_pass_acc / prt_mid_total_minutes * 90) if prt_mid_total_minutes > 0 else 0

  prt_def = prt_data[prt_data['traits'] == 'DEFENCE']
  prt_def_total_minutes_2 = prt_def['minutes'].sum()
  prt_def_duels = prt_def["duels won"].sum()
  prt_def_clearances = prt_def["clearances"].sum()
  prt_def_blocks = prt_def['blocks'].sum()
  prt_def_take_ons_conceeded = prt_def['take-ons conceeded'].sum()
  prt_def_tackle = prt_def['tackles'].sum()
  prt_def_interceptions = prt_def['interceptions'].sum()
  prt_def_rating = prt_def['ratings'].mean()
  prt_def_duels_won_pct = (prt_def['duels won'].sum() /
                                  (prt_def['duels won'].sum() + prt_def['take-ons conceeded'].sum() + 1e-5))
  prt_def_cards = ((prt_def['yellow card'].sum() + 2 * prt_def['red card'].sum())
                                      / (prt_def_total_minutes_2 / 90)) if prt_def_total_minutes_2 > 0 else 0

  prt_defence_duels_90 = (prt_def_duels / prt_def_total_minutes_2 * 90) if prt_def_total_minutes_2 > 0 else 0
  prt_defence_clearance_90 = (prt_def_clearances / prt_def_total_minutes_2 * 90) if prt_def_total_minutes_2 > 0 else 0
  prt_defence_blocks_90 = (prt_def_blocks / prt_def_total_minutes_2 * 90) if prt_def_total_minutes_2 > 0 else 0
  prt_defence_take_ons_conceed_90 = (prt_def_take_ons_conceeded / prt_def_total_minutes_2 * 90) if prt_def_total_minutes_2 > 0 else 0
  prt_defence_tackle_90 = (prt_def_tackle / prt_def_total_minutes_2 * 90) if prt_def_total_minutes_2 > 0 else 0
  prt_defence_interceptions_90 = (prt_def_interceptions / prt_def_total_minutes_2 * 90)
  prt_total_minutes = prt_data['minutes'].sum()
  prt_depth_players = prt_data["players"].nunique() # unique players with no repetation
  prt_matches = (prt_data["opponent"].nunique())*2
  prt_player_min = prt_data.groupby("players")["minutes"].sum()
  prt_depth_60 = (prt_player_min > 60).sum()
  prt_depth_45 = (prt_player_min > 45).sum()
  prt_depth_ratings = prt_data.groupby("players")["ratings"].mean()
  prt_depth_ratings_mean = prt_data["ratings"].mean()
  prt_depth_rate_std = prt_depth_ratings.std()
  prt_depth_avg_min = prt_total_minutes / prt_depth_players if prt_depth_players > 0 else 0
  prt_depth_rating_15 = prt_data.nlargest(15, 'minutes')['ratings'].mean()
  prt_depth_index = (prt_depth_players * prt_depth_rating_15) / (1 + prt_depth_rate_std)
  prt_depth_min_pct_11 = prt_data.nlargest(11, 'minutes')['minutes'].sum() / prt_total_minutes * 100
  prt_depth_avg_min_per_match = prt_depth_avg_min / prt_matches


  # URUGUAY


  uru_data = pd.read_csv("data/uruguay_stats.csv")
  uru_data = uru_data.dropna()
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  uru_data["traits"] = uru_data["position"].apply(func)
  col = []
  for i in esp_data.columns:
    col.append(i)
  abc14 = uru_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  uru_abc = pd.DataFrame({
    "position":abc14.index.get_level_values(1),
    "minutes":abc14["minutes"],
    "ratings":abc14["ratings"],
    "goals scored":abc14["goals scored"],
    "assist":abc14["assist"],
    "shots on target":abc14["shots on target"],
    "shots attempted":abc14["shots attempted"],
    "long balls":abc14["long balls"],
    "long balls completed":abc14["long balls completed"],
    "key passes":abc14["key passes"],
    "duels won":abc14["duels won"],
    "take-ons conceeded":abc14["take-ons conceeded"],
    "tackles":abc14["tackles"],
    "interceptions":abc14["interceptions"],
    "clearances":abc14["clearances"],
    "blocks":abc14["blocks"],
    "dribbles completed":abc14["dribbles completed"],
    "dribbles attempt":abc14["dribbles attempt"],
    "yellow card":abc14["yellow card"],
    "red card": abc14["red card"],
    "nationality": ["Uruguay"] * len(abc14)
})
  uru_total_minutes = uru_data['minutes'].sum()
  uru_overall_rating = (uru_data['ratings'] * uru_data['minutes']).sum()
  uru_squad_quality = uru_overall_rating / uru_total_minutes
  uru_rate_std = uru_data['ratings'].std()
  uru_top11 = uru_data.nlargest(11, 'minutes')
  uru_squad_quality11 = uru_top11['ratings'].mean()

  uru_att = uru_data[uru_data['traits'] == 'ATTACK']
  uru_total_minutes = uru_att['minutes'].sum()
  uru_att_goals = uru_att["goals scored"].sum()
  uru_att_assist = uru_att["assist"].sum()
  uru_att_cont = (uru_att["goals scored"] + uru_att["assist"]).sum()
  uru_att_shots_on_target = uru_att['shots on target'].sum()
  uru_att_shots_attempted = uru_att['shots attempted'].sum()
  uru_att_key_passes_total = uru_att['key passes'].sum()
  uru_att_dribbles_completed = uru_att['dribbles completed'].sum()
  uru_att_dribbles_attempted = uru_att['dribbles attempt'].sum()
  uru_att_rating = uru_att['ratings'].mean()

  uru_attack_goals_90 = ((uru_att_goals / uru_total_minutes) * 90) if uru_total_minutes > 0 else 0
  uru_attack_assist_90 = (uru_att_assist / uru_total_minutes * 90) if uru_total_minutes > 0 else 0
  uru_attack_cont_90 = (uru_att_cont / uru_total_minutes * 90) if uru_total_minutes > 0 else 0
  uru_attack_shots_90 = (uru_att_shots_on_target / uru_total_minutes * 90) if uru_total_minutes > 0 else 0
  uru_attack_key_passes_90 = (uru_att_key_passes_total / uru_total_minutes * 90) if uru_total_minutes > 0 else 0
  uru_attack_dribbles_90 = (uru_att_dribbles_completed / uru_total_minutes * 90)

  uru_mid = uru_data[uru_data['traits'] == 'MIDFIELD']
  uru_mid_total_minutes = uru_mid['minutes'].sum()
  uru_mid_pass_acc = uru_mid['passing accuracy in %'].mean()
  uru_mid_cont = (uru_mid["goals scored"] + uru_mid["assist"]).sum()
  uru_mid_long_balls_completed = uru_mid['long balls completed'].sum()
  uru_mid_long_balls = uru_mid['long balls'].sum()
  uru_mid_key_passes_total = uru_mid['key passes'].sum()
  uru_mid_dribbles_completed = uru_mid['dribbles completed'].sum()
  uru_mid_dribbles_attempted = uru_mid['dribbles attempt'].sum()
  uru_mid_touches = uru_mid['touches'].sum()
  uru_mid_def = (uru_mid['tackles'] + uru_mid["interceptions"]).sum()
  uru_mid_tackle = uru_mid['tackles'].sum()
  uru_mid_interceptions = uru_mid['interceptions'].sum()
  uru_mid_rating = uru_mid['ratings'].mean()

  uru_midfield_long_balls_comp_90 = (uru_mid_long_balls_completed / uru_mid_total_minutes * 90) if uru_mid_total_minutes > 0 else 0
  uru_midfield_long_balls_90 = (uru_mid_long_balls / uru_mid_total_minutes * 90) if uru_mid_total_minutes > 0 else 0
  uru_midfield_cont_90 = (uru_mid_cont / uru_mid_total_minutes * 90) if uru_mid_total_minutes > 0 else 0
  uru_midfield_touches_90 = (uru_mid_touches / uru_mid_total_minutes * 90) if uru_mid_total_minutes > 0 else 0
  uru_midfield_def_90 = (uru_mid_def / uru_mid_total_minutes * 90) if uru_mid_total_minutes > 0 else 0
  uru_midfield_dribbles_90 = (uru_mid_dribbles_completed / uru_mid_total_minutes * 90)
  uru_midfield_key_passes_90 = (uru_mid_key_passes_total / uru_mid_total_minutes * 90) if uru_mid_total_minutes > 0 else 0
  uru_midfield_tackle_90 = (uru_mid_tackle / uru_mid_total_minutes * 90) if uru_mid_total_minutes > 0 else 0
  uru_midfield_interceptions_90 = (uru_mid_interceptions / uru_mid_total_minutes * 90)
  uru_midfield_pass_acc_90 = (uru_mid_pass_acc / uru_mid_total_minutes * 90) if uru_mid_total_minutes > 0 else 0

  uru_def = uru_data[uru_data['traits'] == 'DEFENCE']
  uru_def_total_minutes_2 = uru_def['minutes'].sum()
  uru_def_duels = uru_def["duels won"].sum()
  uru_def_clearances = uru_def["clearances"].sum()
  uru_def_blocks = uru_def['blocks'].sum()
  uru_def_take_ons_conceeded = uru_def['take-ons conceeded'].sum()
  uru_def_tackle = uru_def['tackles'].sum()
  uru_def_interceptions = uru_def['interceptions'].sum()
  uru_def_rating = uru_def['ratings'].mean()

  uru_def_duels_won_pct = (uru_def['duels won'].sum() /
                          (uru_def['duels won'].sum() + uru_def['take-ons conceeded'].sum() + 1e-5))
  uru_def_cards = ((uru_def['yellow card'].sum() + 2 * uru_def['red card'].sum()) /
                  (uru_def_total_minutes_2 / 90)) if uru_def_total_minutes_2 > 0 else 0

  uru_defence_duels_90 = (uru_def_duels / uru_def_total_minutes_2 * 90) if uru_def_total_minutes_2 > 0 else 0
  uru_defence_clearance_90 = (uru_def_clearances / uru_def_total_minutes_2 * 90) if uru_def_total_minutes_2 > 0 else 0
  uru_defence_blocks_90 = (uru_def_blocks / uru_def_total_minutes_2 * 90) if uru_def_total_minutes_2 > 0 else 0
  uru_defence_take_ons_conceed_90 = (uru_def_take_ons_conceeded / uru_def_total_minutes_2 * 90) if uru_def_total_minutes_2 > 0 else 0
  uru_defence_tackle_90 = (uru_def_tackle / uru_def_total_minutes_2 * 90) if uru_def_total_minutes_2 > 0 else 0
  uru_defence_interceptions_90 = (uru_def_interceptions / uru_def_total_minutes_2 * 90)

  uru_total_minutes = uru_data['minutes'].sum()
  uru_depth_players = uru_data["players"].nunique()
  uru_matches = (uru_data["opponent"].nunique()) * 2
  uru_player_min = uru_data.groupby("players")["minutes"].sum()
  uru_depth_60 = (uru_player_min > 60).sum()
  uru_depth_45 = (uru_player_min > 45).sum()
  uru_depth_ratings = uru_data.groupby("players")["ratings"].mean()
  uru_depth_ratings_mean = uru_data["ratings"].mean()
  uru_depth_rate_std = uru_depth_ratings.std()
  uru_depth_avg_min = uru_total_minutes / uru_depth_players if uru_depth_players > 0 else 0
  uru_depth_rating_15 = uru_data.nlargest(15, 'minutes')['ratings'].mean()
  uru_depth_index = (uru_depth_players * uru_depth_rating_15) / (1 + uru_depth_rate_std)
  uru_depth_min_pct_11 = uru_data.nlargest(11, 'minutes')['minutes'].sum() / uru_total_minutes * 100
  uru_depth_avg_min_per_match = uru_depth_avg_min / uru_matches


  # SENEGAL


  sen_data = pd.read_csv("data/Senegal_stats.csv")
  sen_data = sen_data.dropna()
  def func(x):
    if x == "goal keeper":
      return "KEEPER"
    elif x == "centre back" or x == "right back" or x == "left back":
      return "DEFENCE"
    elif x == "central midfielder" or x == "right midfielder" or x == "left midfielder" or x == "defensive midfielder" or x == "attacking midfielder":
      return "MIDFIELD"
    else:
      return "ATTACK"
  sen_data["traits"] = sen_data["position"].apply(func)
  col = []
  for i in esp_data.columns:
    col.append(i)
  abc13 = sen_data.groupby(["players","position"])[col[1:]].mean(numeric_only=True).round(2)
  sen_abc = pd.DataFrame({
    "position":abc13.index.get_level_values(1),
    "minutes":abc13["minutes"],
    "ratings":abc13["ratings"],
    "goals scored":abc13["goals scored"],
    "assist":abc13["assist"],
    "shots on target":abc13["shots on target"],
    "shots attempted":abc13["shots attempted"],
    "long balls":abc13["long balls"],
    "long balls completed":abc13["long balls completed"],
    "key passes":abc13["key passes"],
    "duels won":abc13["duels won"],
    "take-ons conceeded":abc13["take-ons conceeded"],
    "tackles":abc13["tackles"],
    "interceptions":abc13["interceptions"],
    "clearances":abc13["clearances"],
    "blocks":abc13["blocks"],
    "dribbles completed":abc13["dribbles completed"],
    "dribbles attempt":abc13["dribbles attempt"],
    "yellow card":abc13["yellow card"],
    "red card": abc13["red card"],
    "nationality": ["Senegal"] * len(abc13)
})
  
  sen_total_minutes = sen_data['minutes'].sum()
  sen_overall_rating = (sen_data['ratings'] * sen_data['minutes']).sum()
  sen_squad_quality = sen_overall_rating / sen_total_minutes
  sen_rate_std = sen_data['ratings'].std()
  sen_top11 = sen_data.nlargest(11, 'minutes')
  sen_squad_quality11 = sen_top11['ratings'].mean()

  sen_att = sen_data[sen_data['traits'] == 'ATTACK']
  sen_total_minutes = sen_att['minutes'].sum()
  sen_att_goals = sen_att["goals scored"].sum()
  sen_att_assist = sen_att["assist"].sum()
  sen_att_cont = (sen_att["goals scored"] + sen_att["assist"]).sum()
  sen_att_shots_on_target = sen_att['shots on target'].sum()
  sen_att_shots_attempted = sen_att['shots attempted'].sum()
  sen_att_key_passes_total = sen_att['key passes'].sum()
  sen_att_dribbles_completed = sen_att['dribbles completed'].sum()
  sen_att_dribbles_attempted = sen_att['dribbles attempt'].sum()
  sen_att_rating = sen_att['ratings'].mean()
  sen_attack_goals_90 = ((sen_att_goals / sen_total_minutes) * 90) if sen_total_minutes > 0 else 0
  sen_attack_assist_90 = (sen_att_assist / sen_total_minutes * 90) if sen_total_minutes > 0 else 0
  sen_attack_cont_90 = (sen_att_cont / sen_total_minutes * 90) if sen_total_minutes > 0 else 0
  sen_attack_shots_90 = (sen_att_shots_on_target / sen_total_minutes * 90) if sen_total_minutes > 0 else 0
  sen_attack_key_passes_90 = (sen_att_key_passes_total / sen_total_minutes * 90) if sen_total_minutes > 0 else 0
  sen_attack_dribbles_90 = (sen_att_dribbles_completed / sen_total_minutes * 90)

  sen_mid = sen_data[sen_data['traits'] == 'MIDFIELD']
  sen_mid_total_minutes = sen_mid['minutes'].sum()
  sen_mid_pass_acc = sen_mid['passing accuracy in %'].mean()
  sen_mid_cont = (sen_mid["goals scored"] + sen_mid["assist"]).sum()
  sen_mid_long_balls_completed = sen_mid['long balls completed'].sum()
  sen_mid_long_balls = sen_mid['long balls'].sum()
  sen_mid_key_passes_total = sen_mid['key passes'].sum()
  sen_mid_dribbles_completed = sen_mid['dribbles completed'].sum()
  sen_mid_dribbles_attempted = sen_mid['dribbles attempt'].sum()
  sen_mid_touches = sen_mid['touches'].sum()
  sen_mid_def = (sen_mid['tackles'] + sen_mid["interceptions"]).sum()
  sen_mid_tackle = sen_mid['tackles'].sum()
  sen_mid_interceptions = sen_mid['interceptions'].sum()
  sen_mid_rating = sen_mid['ratings'].mean()
  sen_midfield_long_balls_comp_90 = (sen_mid_long_balls_completed / sen_mid_total_minutes * 90) if sen_mid_total_minutes > 0 else 0
  sen_midfield_long_balls_90 = (sen_mid_long_balls / sen_mid_total_minutes * 90) if sen_mid_total_minutes > 0 else 0
  sen_midfield_cont_90 = (sen_mid_cont / sen_mid_total_minutes * 90) if sen_mid_total_minutes > 0 else 0
  sen_midfield_touches_90 = (sen_mid_touches / sen_mid_total_minutes * 90) if sen_mid_total_minutes > 0 else 0
  sen_midfield_def_90 = (sen_mid_def / sen_mid_total_minutes * 90) if sen_mid_total_minutes > 0 else 0
  sen_midfield_dribbles_90 = (sen_mid_dribbles_completed / sen_mid_total_minutes * 90)
  sen_midfield_key_passes_90 = (sen_mid_key_passes_total / sen_mid_total_minutes * 90) if sen_mid_total_minutes > 0 else 0
  sen_midfield_tackle_90 = (sen_mid_tackle / sen_mid_total_minutes * 90) if sen_mid_total_minutes > 0 else 0
  sen_midfield_interceptions_90 = (sen_mid_interceptions / sen_mid_total_minutes * 90) if sen_mid_total_minutes > 0 else 0
  sen_midfield_pass_acc_90 = (sen_mid_pass_acc / sen_mid_total_minutes * 90) if sen_mid_total_minutes > 0 else 0

  sen_def = sen_data[sen_data['traits'] == 'DEFENCE']
  sen_def_total_minutes_2 = sen_def['minutes'].sum()
  sen_def_duels = sen_def["duels won"].sum()
  sen_def_clearances = sen_def["clearances"].sum()
  sen_def_blocks = sen_def['blocks'].sum()
  sen_def_take_ons_conceeded = sen_def['take-ons conceeded'].sum()
  sen_def_tackle = sen_def['tackles'].sum()
  sen_def_interceptions = sen_def['interceptions'].sum()
  sen_def_rating = sen_def['ratings'].mean()
  sen_def_duels_won_pct = (sen_def['duels won'].sum() /
                          (sen_def['duels won'].sum() + sen_def['take-ons conceeded'].sum() + 1e-5))
  sen_def_cards = ((sen_def['yellow card'].sum() + 2 * sen_def['red card'].sum())
                  / (sen_def_total_minutes_2 / 90)) if sen_def_total_minutes_2 > 0 else 0

  sen_defence_duels_90 = (sen_def_duels / sen_def_total_minutes_2 * 90) if sen_def_total_minutes_2 > 0 else 0
  sen_defence_clearance_90 = (sen_def_clearances / sen_def_total_minutes_2 * 90) if sen_def_total_minutes_2 > 0 else 0
  sen_defence_blocks_90 = (sen_def_blocks / sen_def_total_minutes_2 * 90) if sen_def_total_minutes_2 > 0 else 0
  sen_defence_take_ons_conceed_90 = (sen_def_take_ons_conceeded / sen_def_total_minutes_2 * 90) if sen_def_total_minutes_2 > 0 else 0
  sen_defence_tackle_90 = (sen_def_tackle / sen_def_total_minutes_2 * 90) if sen_def_total_minutes_2 > 0 else 0
  sen_defence_interceptions_90 = (sen_def_interceptions / sen_def_total_minutes_2 * 90)

  sen_total_minutes = sen_data['minutes'].sum()
  sen_depth_players = sen_data["players"].nunique()
  sen_matches = (sen_data["opponent"].nunique()) * 2
  sen_player_min = sen_data.groupby("players")["minutes"].sum()
  sen_depth_60 = (sen_player_min > 60).sum()
  sen_depth_45 = (sen_player_min > 45).sum()
  sen_depth_ratings = sen_data.groupby("players")["ratings"].mean()
  sen_depth_ratings_mean = sen_data["ratings"].mean()
  sen_depth_rate_std = sen_depth_ratings.std()
  sen_depth_avg_min = sen_total_minutes / sen_depth_players if sen_depth_players > 0 else 0
  sen_depth_rating_15 = sen_data.nlargest(15, 'minutes')['ratings'].mean()
  sen_depth_index = (sen_depth_players * sen_depth_rating_15) / (1 + sen_depth_rate_std)
  sen_depth_min_pct_11 = sen_data.nlargest(11, 'minutes')['minutes'].sum() / sen_total_minutes * 100
  sen_depth_avg_min_per_match = sen_depth_avg_min / sen_matches

  
  # EXTRAS


  esp_mid_goals = esp_mid["goals scored"].sum()
  esp_mid_assist = esp_mid["assist"].sum()
  esp_def_goals = esp_def["goals scored"].sum()
  esp_def_assist = esp_def["assist"].sum()
  esp_def_cont = (esp_def["goals scored"] + esp_def["assist"]).sum()
  midfield_goals_90 = (esp_mid_goals / total_minutes * 90) if total_minutes > 0 else 0
  midfield_assist_90 = (esp_mid_assist / total_minutes * 90) if total_minutes > 0 else 0
  defence_goals_90 = (esp_def_goals / total_minutes * 90) if total_minutes > 0 else 0
  defence_assist_90 = (esp_def_assist / total_minutes * 90) if total_minutes > 0 else 0
  defence_cont_90 = (esp_def_cont / total_minutes * 90) if total_minutes > 0 else 0

  arg_mid_goals = arg_mid["goals scored"].sum()
  arg_mid_assist = arg_mid["assist"].sum()
  arg_def_goals = arg_def["goals scored"].sum()
  arg_def_assist = arg_def["assist"].sum()
  arg_def_cont = (arg_def["goals scored"] + arg_def["assist"]).sum()
  arg_midfield_goals_90 = (arg_mid_goals / arg_total_minutes_1 * 90) if arg_total_minutes_1 > 0 else 0
  arg_midfield_assist_90 = (arg_mid_assist / arg_total_minutes_1 * 90) if arg_total_minutes_1 > 0 else 0
  arg_defence_goals_90 = (arg_def_goals / arg_def_total_minutes_2 * 90) if arg_def_total_minutes_2 > 0 else 0
  arg_defence_assist_90 = (arg_def_assist / arg_def_total_minutes_2 * 90) if arg_def_total_minutes_2 > 0 else 0
  arg_defence_cont_90 = (arg_def_cont / arg_def_total_minutes_2 * 90) if arg_def_total_minutes_2 > 0 else 0

  bel_mid_goals = bel_mid["goals scored"].sum()
  bel_mid_assist = bel_mid["assist"].sum()
  bel_def_goals = bel_def["goals scored"].sum()
  bel_def_assist = bel_def["assist"].sum()
  bel_def_cont = (bel_def["goals scored"] + bel_def["assist"]).sum()
  bel_midfield_goals_90 = (bel_mid_goals / bel_mid_total_minutes * 90) if bel_mid_total_minutes > 0 else 0
  bel_midfield_assist_90 = (bel_mid_assist / bel_mid_total_minutes * 90) if bel_mid_total_minutes > 0 else 0
  bel_defence_goals_90 = (bel_def_goals / bel_def_total_minutes_2 * 90) if bel_def_total_minutes_2 > 0 else 0
  bel_defence_assist_90 = (bel_def_assist / bel_def_total_minutes_2 * 90) if bel_def_total_minutes_2 > 0 else 0
  bel_defence_cont_90 = (bel_def_cont / bel_def_total_minutes_2 * 90) if bel_def_total_minutes_2 > 0 else 0
  
  bra_mid_goals = bra_mid["goals scored"].sum()
  bra_mid_assist = bra_mid["assist"].sum()
  bra_def_goals = bra_def["goals scored"].sum()
  bra_def_assist = bra_def["assist"].sum()
  bra_def_cont = (bra_def["goals scored"] + bra_def["assist"]).sum()
  bra_midfield_goals_90 = (bra_mid_goals / bra_mid_total_minutes * 90) if bra_mid_total_minutes > 0 else 0
  bra_midfield_assist_90 = (bra_mid_assist / bra_mid_total_minutes * 90) if bra_mid_total_minutes > 0 else 0
  bra_defence_goals_90 = (bra_def_goals / bra_def_total_minutes_2 * 90) if bra_def_total_minutes_2 > 0 else 0
  bra_defence_assist_90 = (bra_def_assist / bra_def_total_minutes_2 * 90) if bra_def_total_minutes_2 > 0 else 0
  bra_defence_cont_90 = (bra_def_cont / bra_def_total_minutes_2 * 90) if bra_def_total_minutes_2 > 0 else 0


  col_mid_goals = col_mid["goals scored"].sum()
  col_mid_assist = col_mid["assist"].sum()
  col_def_goals = col_def["goals scored"].sum()
  col_def_assist = col_def["assist"].sum()
  col_def_cont = (col_def["goals scored"] + col_def["assist"]).sum()
  col_midfield_goals_90 = (col_mid_goals / col_mid_total_minutes * 90) if col_mid_total_minutes > 0 else 0
  col_midfield_assist_90 = (col_mid_assist / col_mid_total_minutes * 90) if col_mid_total_minutes > 0 else 0
  col_defence_goals_90 = (col_def_goals / col_def_total_minutes_2 * 90) if col_def_total_minutes_2 > 0 else 0
  col_defence_assist_90 = (col_def_assist / col_def_total_minutes_2 * 90) if col_def_total_minutes_2 > 0 else 0
  col_defence_cont_90 = (col_def_cont / col_def_total_minutes_2 * 90) if col_def_total_minutes_2 > 0 else 0

  cro_mid_goals = cro_mid["goals scored"].sum()
  cro_mid_assist = cro_mid["assist"].sum()
  cro_def_goals = cro_def["goals scored"].sum()
  cro_def_assist = cro_def["assist"].sum()
  cro_def_cont = (cro_def["goals scored"] + cro_def["assist"]).sum()
  cro_midfield_goals_90 = (cro_mid_goals / cro_mid_total_minutes * 90) if cro_mid_total_minutes > 0 else 0
  cro_midfield_assist_90 = (cro_mid_assist / cro_mid_total_minutes * 90) if cro_mid_total_minutes > 0 else 0
  cro_defence_goals_90 = (cro_def_goals / cro_def_total_minutes_2 * 90) if cro_def_total_minutes_2 > 0 else 0
  cro_defence_assist_90 = (cro_def_assist / cro_def_total_minutes_2 * 90) if cro_def_total_minutes_2 > 0 else 0
  cro_defence_cont_90 = (cro_def_cont / cro_def_total_minutes_2 * 90) if cro_def_total_minutes_2 > 0 else 0


  dut_mid_goals = dut_mid["goals scored"].sum()
  dut_mid_assist = dut_mid["assist"].sum()
  dut_def_goals = dut_def["goals scored"].sum()
  dut_def_assist = dut_def["assist"].sum()
  dut_def_cont = (dut_def["goals scored"] + dut_def["assist"]).sum()
  dut_midfield_goals_90 = (dut_mid_goals / dut_mid_total_minutes * 90) if dut_mid_total_minutes > 0 else 0
  dut_midfield_assist_90 = (dut_mid_assist / dut_mid_total_minutes * 90) if dut_mid_total_minutes > 0 else 0
  dut_defence_goals_90 = (dut_def_goals / dut_def_total_minutes_2 * 90) if dut_def_total_minutes_2 > 0 else 0
  dut_defence_assist_90 = (dut_def_assist / dut_def_total_minutes_2 * 90) if dut_def_total_minutes_2 > 0 else 0
  dut_defence_cont_90 = (dut_def_cont / dut_def_total_minutes_2 * 90) if dut_def_total_minutes_2 > 0 else 0


  fra_mid_goals = fra_mid["goals scored"].sum()
  fra_mid_assist = fra_mid["assist"].sum()
  fra_def_goals = fra_def["goals scored"].sum()
  fra_def_assist = fra_def["assist"].sum()
  fra_def_cont = (fra_def["goals scored"] + fra_def["assist"]).sum()
  fra_midfield_goals_90 = (fra_mid_goals / fra_mid_total_minutes * 90) if fra_mid_total_minutes > 0 else 0
  fra_midfield_assist_90 = (fra_mid_assist / fra_mid_total_minutes * 90) if fra_mid_total_minutes > 0 else 0
  fra_defence_goals_90 = (fra_def_goals / fra_def_total_minutes_2 * 90) if fra_def_total_minutes_2 > 0 else 0
  fra_defence_assist_90 = (fra_def_assist / fra_def_total_minutes_2 * 90) if fra_def_total_minutes_2 > 0 else 0
  fra_defence_cont_90 = (fra_def_cont / fra_def_total_minutes_2 * 90) if fra_def_total_minutes_2 > 0 else 0


  ger_mid_goals = ger_mid["goals scored"].sum()
  ger_mid_assist = ger_mid["assist"].sum()
  ger_def_goals = ger_def["goals scored"].sum()
  ger_def_assist = ger_def["assist"].sum()
  ger_def_cont = (ger_def["goals scored"] + ger_def["assist"]).sum()
  ger_midfield_goals_90 = (ger_mid_goals / ger_mid_total_minutes * 90) if ger_mid_total_minutes > 0 else 0
  ger_midfield_assist_90 = (ger_mid_assist / ger_mid_total_minutes * 90) if ger_mid_total_minutes > 0 else 0
  ger_defence_goals_90 = (ger_def_goals / ger_def_total_minutes_2 * 90) if ger_def_total_minutes_2 > 0 else 0
  ger_defence_assist_90 = (ger_def_assist / ger_def_total_minutes_2 * 90) if ger_def_total_minutes_2 > 0 else 0
  ger_defence_cont_90 = (ger_def_cont / ger_def_total_minutes_2 * 90) if ger_def_total_minutes_2 > 0 else 0

  
  eng_mid_goals = eng_mid["goals scored"].sum()
  eng_mid_assist = eng_mid["assist"].sum()
  eng_def_goals = eng_def["goals scored"].sum()
  eng_def_assist = eng_def["assist"].sum()
  eng_def_cont = (eng_def["goals scored"] + eng_def["assist"]).sum()
  eng_midfield_goals_90 = (eng_mid_goals / eng_mid_total_minutes * 90) if eng_mid_total_minutes > 0 else 0
  eng_midfield_assist_90 = (eng_mid_assist / eng_mid_total_minutes * 90) if eng_mid_total_minutes > 0 else 0
  eng_defence_goals_90 = (eng_def_goals / eng_def_total_minutes_2 * 90) if eng_def_total_minutes_2 > 0 else 0
  eng_defence_assist_90 = (eng_def_assist / eng_def_total_minutes_2 * 90) if eng_def_total_minutes_2 > 0 else 0
  eng_defence_cont_90 = (eng_def_cont / eng_def_total_minutes_2 * 90) if eng_def_total_minutes_2 > 0 else 0


  mor_mid_goals = mor_mid["goals scored"].sum()
  mor_mid_assist = mor_mid["assist"].sum()
  mor_def_goals = mor_def["goals scored"].sum()
  mor_def_assist = mor_def["assist"].sum()
  mor_def_cont = (mor_def["goals scored"] + mor_def["assist"]).sum()
  mor_midfield_goals_90 = (mor_mid_goals / mor_mid_total_minutes * 90) if mor_mid_total_minutes > 0 else 0
  mor_midfield_assist_90 = (mor_mid_assist / mor_mid_total_minutes * 90) if mor_mid_total_minutes > 0 else 0
  mor_defence_goals_90 = (mor_def_goals / mor_def_total_minutes_2 * 90) if mor_def_total_minutes_2 > 0 else 0
  mor_defence_assist_90 = (mor_def_assist / mor_def_total_minutes_2 * 90) if mor_def_total_minutes_2 > 0 else 0
  mor_defence_cont_90 = (mor_def_cont / mor_def_total_minutes_2 * 90) if mor_def_total_minutes_2 > 0 else 0


  prt_mid_goals = prt_mid["goals scored"].sum()
  prt_mid_assist = prt_mid["assist"].sum()
  prt_def_goals = prt_def["goals scored"].sum()
  prt_def_assist = prt_def["assist"].sum()
  prt_def_cont = (prt_def["goals scored"] + prt_def["assist"]).sum()
  prt_midfield_goals_90 = (prt_mid_goals / prt_mid_total_minutes * 90) if prt_mid_total_minutes > 0 else 0
  prt_midfield_assist_90 = (prt_mid_assist / prt_mid_total_minutes * 90) if prt_mid_total_minutes > 0 else 0
  prt_defence_goals_90 = (prt_def_goals / prt_def_total_minutes_2 * 90) if prt_def_total_minutes_2 > 0 else 0
  prt_defence_assist_90 = (prt_def_assist / prt_def_total_minutes_2 * 90) if prt_def_total_minutes_2 > 0 else 0
  prt_defence_cont_90 = (prt_def_cont / prt_def_total_minutes_2 * 90) if prt_def_total_minutes_2 > 0 else 0
  

  uru_mid_goals = uru_mid["goals scored"].sum()
  uru_mid_assist = uru_mid["assist"].sum()
  uru_def_goals = uru_def["goals scored"].sum()
  uru_def_assist = uru_def["assist"].sum()
  uru_def_cont = (uru_def["goals scored"] + uru_def["assist"]).sum()
  uru_midfield_goals_90 = (uru_mid_goals / uru_mid_total_minutes * 90) if uru_mid_total_minutes > 0 else 0
  uru_midfield_assist_90 = (uru_mid_assist / uru_mid_total_minutes * 90) if uru_mid_total_minutes > 0 else 0
  uru_defence_goals_90 = (uru_def_goals / uru_def_total_minutes_2 * 90) if uru_def_total_minutes_2 > 0 else 0
  uru_defence_assist_90 = (uru_def_assist / uru_def_total_minutes_2 * 90) if uru_def_total_minutes_2 > 0 else 0
  uru_defence_cont_90 = (uru_def_cont / uru_def_total_minutes_2 * 90) if uru_def_total_minutes_2 > 0 else 0


  sen_mid_goals = sen_mid["goals scored"].sum()
  sen_mid_assist = sen_mid["assist"].sum()
  sen_def_goals = sen_def["goals scored"].sum()
  sen_def_assist = sen_def["assist"].sum()
  sen_def_cont = (sen_def["goals scored"] + sen_def["assist"]).sum()
  sen_midfield_goals_90 = (sen_mid_goals / sen_mid_total_minutes * 90) if sen_mid_total_minutes > 0 else 0
  sen_midfield_assist_90 = (sen_mid_assist / sen_mid_total_minutes * 90) if sen_mid_total_minutes > 0 else 0
  sen_defence_goals_90 = (sen_def_goals / sen_def_total_minutes_2 * 90) if sen_def_total_minutes_2 > 0 else 0
  sen_defence_assist_90 = (sen_def_assist / sen_def_total_minutes_2 * 90) if sen_def_total_minutes_2 > 0 else 0
  sen_defence_cont_90 = (sen_def_cont / sen_def_total_minutes_2 * 90) if sen_def_total_minutes_2 > 0 else 0


  # FULL STATS


  full_stats = pd.DataFrame({
    "Countries": ['Spain', 'Argentina', 'France', 'England', 'Brazil', 'Portugal', 'Netherlands', 'Belgium', 'Germany', 'Croatia', 'Morocco', 'Colombia', 'Uruguay', 'Senegal'],
    "Overall Squad ratings": [(squad_quality).round(1), (arg_squad_quality).round(1), (fra_squad_quality).round(1), (eng_squad_quality).round(1), (bra_squad_quality).round(1), (prt_squad_quality).round(1), (dut_squad_quality).round(1), (bel_squad_quality).round(1), (ger_squad_quality).round(1), (cro_squad_quality).round(1), (mor_squad_quality).round(1), (col_squad_quality).round(1), (uru_squad_quality).round(1), (sen_squad_quality).round(1)],
    "Top 11 Squad ratings": [(squad_quality11).round(1), (arg_squad_quality11).round(1), (fra_squad_quality11).round(1), (eng_squad_quality11).round(1), (bra_squad_quality11).round(1), (prt_squad_quality11).round(1), (dut_squad_quality11).round(1), (bel_squad_quality11).round(1), (ger_squad_quality11).round(1), (cro_squad_quality11).round(1), (mor_squad_quality11).round(1), (col_squad_quality11).round(1), (uru_squad_quality11).round(1), (sen_squad_quality11).round(1)],
    "Squad_depth_60": [depth_60, arg_depth_60, fra_depth_60, eng_depth_60, bra_depth_60, prt_depth_60, dut_depth_60, bel_depth_60, ger_depth_60, cro_depth_60, mor_depth_60, col_depth_60, uru_depth_60, sen_depth_60],
    "Squad_depth_45": [depth_45, arg_depth_45, fra_depth_45, eng_depth_45, bra_depth_45, prt_depth_45, dut_depth_45, bel_depth_45, ger_depth_45, cro_depth_45, mor_depth_45, col_depth_45, uru_depth_45, sen_depth_45],
    "Squad_depth_avg": [np.ceil(depth_avg_min), np.ceil(arg_depth_avg_min), np.ceil(fra_depth_avg_min), np.ceil(eng_depth_avg_min), np.ceil(bra_depth_avg_min), np.ceil(prt_depth_avg_min), np.ceil(dut_depth_avg_min), np.ceil(bel_depth_avg_min), np.ceil(ger_depth_avg_min), np.ceil(cro_depth_avg_min), np.ceil(mor_depth_avg_min), np.ceil(col_depth_avg_min), np.ceil(uru_depth_avg_min), np.ceil(sen_depth_avg_min)],
    "Squad_depth_avg_per_match": [np.ceil(depth_avg_min_per_match), np.ceil(arg_depth_avg_min_per_match), np.ceil(fra_depth_avg_min_per_match), np.ceil(eng_depth_avg_min_per_match), np.ceil(bra_depth_avg_min_per_match), np.ceil(prt_depth_avg_min_per_match), np.ceil(dut_depth_avg_min_per_match), np.ceil(bel_depth_avg_min_per_match), np.ceil(ger_depth_avg_min_per_match), np.ceil(cro_depth_avg_min_per_match), np.ceil(mor_depth_avg_min_per_match), np.ceil(col_depth_avg_min_per_match), np.ceil(uru_depth_avg_min_per_match), np.ceil(sen_depth_avg_min_per_match)],
    "Squad_depth_ratings": [np.ceil(depth_ratings_mean), np.ceil(arg_depth_ratings_mean), np.ceil(fra_depth_ratings_mean), np.ceil(eng_depth_ratings_mean), np.ceil(bra_depth_ratings_mean), np.ceil(prt_depth_ratings_mean), np.ceil(dut_depth_ratings_mean), np.ceil(bel_depth_ratings_mean), np.ceil(ger_depth_ratings_mean), np.ceil(cro_depth_ratings_mean), np.ceil(mor_depth_ratings_mean), np.ceil(col_depth_ratings_mean), np.ceil(uru_depth_ratings_mean), np.ceil(sen_depth_ratings_mean)],
    "Squad_depth_rate_std": [np.ceil(depth_rate_std), np.ceil(arg_rate_std), np.ceil(fra_rate_std), np.ceil(eng_rate_std), np.ceil(bra_rate_std), np.ceil(prt_rate_std), np.ceil(dut_rate_std), np.ceil(bel_rate_std), np.ceil(ger_rate_std), np.ceil(cro_rate_std), np.ceil(mor_rate_std), np.ceil(col_rate_std), np.ceil(uru_rate_std), np.ceil(sen_rate_std)],
    "Squad_depth_rating_15": [np.ceil(depth_rating_15), np.ceil(arg_depth_rating_15), np.ceil(fra_depth_rating_15), np.ceil(eng_depth_rating_15), np.ceil(bra_depth_rating_15), np.ceil(prt_depth_rating_15), np.ceil(dut_depth_rating_15), np.ceil(bel_depth_rating_15), np.ceil(ger_depth_rating_15), np.ceil(cro_depth_rating_15), np.ceil(mor_depth_rating_15), np.ceil(col_depth_rating_15), np.ceil(uru_depth_rating_15), np.ceil(sen_depth_rating_15)],
    "Squad_depth_index": [np.ceil(depth_index), np.ceil(arg_depth_index), np.ceil(fra_depth_index), np.ceil(eng_depth_index), np.ceil(bra_depth_index), np.ceil(prt_depth_index), np.ceil(dut_depth_index), np.ceil(bel_depth_index), np.ceil(ger_depth_index), np.ceil(cro_depth_index), np.ceil(mor_depth_index), np.ceil(col_depth_index), np.ceil(uru_depth_index), np.ceil(sen_depth_index)],
    "Squad_depth_min_pct_11": [np.ceil(depth_min_pct_11), np.ceil(arg_depth_min_pct_11), np.ceil(fra_depth_min_pct_11), np.ceil(eng_depth_min_pct_11), np.ceil(bra_depth_min_pct_11), np.ceil(prt_depth_min_pct_11), np.ceil(dut_depth_min_pct_11), np.ceil(bel_depth_min_pct_11), np.ceil(ger_depth_min_pct_11), np.ceil(cro_depth_min_pct_11), np.ceil(mor_depth_min_pct_11), np.ceil(col_depth_min_pct_11), np.ceil(uru_depth_min_pct_11), np.ceil(sen_depth_min_pct_11)],
    "xg_per_90": [2.55, 1.95, 2.35, 2.10, 1.85, 2.05, 2.28, 1.85, 2.15, 1.65, 1.55, 1.45, 1.18, 1.75],

"xga_per_90": [0.85, 0.88, 0.78, 0.72, 1.15, 0.92, 0.95, 1.05, 1.25, 0.95, 0.85, 0.95, 1.05, 1.10],

"ppda": [9.8, 12.4, 10.1, 10.8, 12.7, 11.8, 9.2, 11.2, 10.4, 12.6, 12.9, 13.1, 13.8, 11.5],

    "Elo ratings":[
    1876.40,   # Spain
    1874.81,   # Argentina
    1877.32,   # France
    1825.97,   # England
    1761.16,   # Brazil
    1763.83,   # Portugal
    1757.87,   # Netherlands
    1734.71,   # Belgium (approx)
    1730.37,   # Germany
    1717.07,   # Croatia
    1755.87,   # Morocco
    1685.00,   # Colombia (approx)
    1668.50,   # Uruguay (approx)
    1678.00    # Senegal (approx)
],
    "Latitudes": [
    40.4168,   # Spain
    -34.6037,  # Argentina
    46.2276,   # France
    51.5074,   # England (United Kingdom)
    -14.2350,  # Brazil
    38.7223,   # Portugal
    52.1326,   # Netherlands
    50.5039,   # Belgium
    51.1657,   # Germany
    45.1000,   # Croatia
    31.7917,   # Morocco
    4.5709,    # Colombia
    -32.5228,  # Uruguay
    14.4974    # Senegal
],
    "Longitudes":[-3.7038, -58.3816, 2.2137, -0.1278, -51.9253, -9.1393,
              5.2913, 4.4699, 10.4515, 15.2000, -7.0926, -74.2973,
              -55.7658, -14.4524],

    "Attack Goals per 90": [attack_goals_90, arg_attack_goals_90, fra_attack_goals_90, eng_attack_goals_90, bra_attack_goals_90, prt_attack_goals_90, dut_attack_goals_90, bel_attack_goals_90, ger_attack_goals_90, cro_attack_goals_90, mor_attack_goals_90, col_attack_goals_90, uru_attack_goals_90, sen_attack_goals_90],
    "Attack Assists per 90": [attack_assist_90, arg_attack_assist_90, fra_attack_assist_90, eng_attack_assist_90, bra_attack_assist_90, prt_attack_assist_90, dut_attack_assist_90, bel_attack_assist_90, ger_attack_assist_90, cro_attack_assist_90, mor_attack_assist_90, col_attack_assist_90, uru_attack_assist_90, sen_attack_assist_90],
    "Attack Contributions per 90": [attack_cont_90, arg_attack_cont_90, fra_attack_cont_90, eng_attack_cont_90, bra_attack_cont_90, prt_attack_cont_90, dut_attack_cont_90, bel_attack_cont_90, ger_attack_cont_90, cro_attack_cont_90, mor_attack_cont_90, col_attack_cont_90, uru_attack_cont_90, sen_attack_cont_90],
    "Attack Shots per 90": [attack_shots_90, arg_attack_shots_90, fra_attack_shots_90, eng_attack_shots_90, bra_attack_shots_90, prt_attack_shots_90, dut_attack_shots_90, bel_attack_shots_90, ger_attack_shots_90, cro_attack_shots_90, mor_attack_shots_90, col_attack_shots_90, uru_attack_shots_90, sen_attack_shots_90],
    "Attack Key Passes per 90": [attack_key_passes_90, arg_attack_key_passes_90, fra_attack_key_passes_90, eng_attack_key_passes_90, bra_attack_key_passes_90, prt_attack_key_passes_90, dut_attack_key_passes_90, bel_attack_key_passes_90, ger_attack_key_passes_90, cro_attack_key_passes_90, mor_attack_key_passes_90, col_attack_key_passes_90, uru_attack_key_passes_90, sen_attack_key_passes_90],
    "Attack Dribbles per 90": [attack_dribbles_90, arg_attack_dribbles_90, fra_attack_dribbles_90, eng_attack_dribbles_90, bra_attack_dribbles_90, prt_attack_dribbles_90, dut_attack_dribbles_90, bel_attack_dribbles_90, ger_attack_dribbles_90, cro_attack_dribbles_90, mor_attack_dribbles_90, col_attack_dribbles_90, uru_attack_dribbles_90, sen_attack_dribbles_90],
    "Attack Rating": [esp_att_rating.round(2), arg_att_rating.round(2), fra_att_rating.round(2), eng_att_rating.round(2), bra_att_rating.round(2), prt_att_rating.round(2), dut_att_rating.round(2), bel_att_rating.round(2), ger_att_rating.round(2), cro_att_rating.round(2), mor_att_rating.round(2), col_att_rating.round(2), uru_att_rating.round(2), sen_att_rating.round(2)],

    "Midfield Goals per 90": [midfield_goals_90, arg_midfield_goals_90, fra_midfield_goals_90, eng_midfield_goals_90, bra_midfield_goals_90, prt_midfield_goals_90, dut_midfield_goals_90, bel_midfield_goals_90, ger_midfield_goals_90, cro_midfield_goals_90, mor_midfield_goals_90, col_midfield_goals_90, uru_midfield_goals_90, sen_midfield_goals_90],
    "Midfield Assists per 90": [midfield_assist_90, arg_midfield_assist_90, fra_midfield_assist_90, eng_midfield_assist_90, bra_midfield_assist_90, prt_midfield_assist_90, dut_midfield_assist_90, bel_midfield_assist_90, ger_midfield_assist_90, cro_midfield_assist_90, mor_midfield_assist_90, col_midfield_assist_90, uru_midfield_assist_90, sen_midfield_assist_90],
    "Midfield Contributions per 90": [midfield_cont_90, arg_midfield_cont_90, fra_midfield_cont_90, eng_midfield_cont_90, bra_midfield_cont_90, prt_midfield_cont_90, dut_midfield_cont_90, bel_midfield_cont_90, ger_midfield_cont_90, cro_midfield_cont_90, mor_midfield_cont_90, col_midfield_cont_90, uru_midfield_cont_90, sen_midfield_cont_90],
    "Midfield Touches per 90": [midfield_touches_90, arg_midfield_touches_90, fra_midfield_touches_90, eng_midfield_touches_90, bra_midfield_touches_90, prt_midfield_touches_90, dut_midfield_touches_90, bel_midfield_touches_90, ger_midfield_touches_90, cro_midfield_touches_90, mor_midfield_touches_90, col_midfield_touches_90, uru_midfield_touches_90, sen_midfield_touches_90],
    "Midfield Key Passes per 90": [midfield_key_passes_90, arg_midfield_key_passes_90, fra_midfield_key_passes_90, eng_midfield_key_passes_90, bra_midfield_key_passes_90, prt_midfield_key_passes_90, dut_midfield_key_passes_90, bel_midfield_key_passes_90, ger_midfield_key_passes_90, cro_midfield_key_passes_90, mor_midfield_key_passes_90, col_midfield_key_passes_90, uru_midfield_key_passes_90, sen_midfield_key_passes_90],
    "Midfield Dribbles per 90": [midfield_dribbles_90, arg_midfield_dribbles_90, fra_midfield_dribbles_90, eng_midfield_dribbles_90, bra_midfield_dribbles_90, prt_midfield_dribbles_90, dut_midfield_dribbles_90, bel_midfield_dribbles_90, ger_midfield_dribbles_90, cro_midfield_dribbles_90, mor_midfield_dribbles_90, col_midfield_dribbles_90, uru_midfield_dribbles_90, sen_midfield_dribbles_90],
    "Midfield Defense per 90": [midfield_def_90, arg_midfield_def_90, fra_midfield_def_90, eng_midfield_def_90, bra_midfield_def_90, prt_midfield_def_90, dut_midfield_def_90, bel_midfield_def_90, ger_midfield_def_90, cro_midfield_def_90, mor_midfield_def_90, col_midfield_def_90, uru_midfield_def_90, sen_midfield_def_90],
    "Midfield Tackles per 90": [midfield_tackle_90, arg_midfield_tackle_90, fra_midfield_tackle_90, eng_midfield_tackle_90, bra_midfield_tackle_90, prt_midfield_tackle_90, dut_midfield_tackle_90, bel_midfield_tackle_90, ger_midfield_tackle_90, cro_midfield_tackle_90, mor_midfield_tackle_90, col_midfield_tackle_90, uru_midfield_tackle_90, sen_midfield_tackle_90],
    "Midfield Interceptions per 90": [midfield_interceptions_90, arg_midfield_interceptions_90, fra_midfield_interceptions_90, eng_midfield_interceptions_90, bra_midfield_interceptions_90, prt_midfield_interceptions_90, dut_midfield_interceptions_90, bel_midfield_interceptions_90, ger_midfield_interceptions_90, cro_midfield_interceptions_90, mor_midfield_interceptions_90, col_midfield_interceptions_90, uru_midfield_interceptions_90, sen_midfield_interceptions_90],
    "Midfield Pass Accuracy": [esp_mid_pass_acc.round(2), arg_mid_pass_acc.round(2), fra_mid_pass_acc.round(2), eng_mid_pass_acc.round(2), bra_mid_pass_acc.round(2), prt_mid_pass_acc.round(2), dut_mid_pass_acc.round(2), bel_mid_pass_acc.round(2), ger_mid_pass_acc.round(2), cro_mid_pass_acc.round(2), mor_mid_pass_acc.round(2), col_mid_pass_acc.round(2), uru_mid_pass_acc.round(2), sen_mid_pass_acc.round(2)],
    "Midfield Rating": [esp_mid_rating.round(2), arg_mid_rating.round(2), fra_mid_rating.round(2), eng_mid_rating.round(2), bra_mid_rating.round(2), prt_mid_rating.round(2), dut_mid_rating.round(2), bel_mid_rating.round(2), ger_mid_rating.round(2), cro_mid_rating.round(2), mor_mid_rating.round(2), col_mid_rating.round(2), uru_mid_rating.round(2), sen_mid_rating.round(2)],

    "Defense Goals per 90": [defence_goals_90, arg_defence_goals_90, fra_defence_goals_90, eng_defence_goals_90, bra_defence_goals_90, prt_defence_goals_90, dut_defence_goals_90, bel_defence_goals_90, ger_defence_goals_90, cro_defence_goals_90, mor_defence_goals_90, col_defence_goals_90, uru_defence_goals_90, sen_defence_goals_90],
    "Defense Assists per 90": [defence_assist_90, arg_defence_assist_90, fra_defence_assist_90, eng_defence_assist_90, bra_defence_assist_90, prt_defence_assist_90, dut_defence_assist_90, bel_defence_assist_90, ger_defence_assist_90, cro_defence_assist_90, mor_defence_assist_90, col_defence_assist_90, uru_defence_assist_90, sen_defence_assist_90],
    "Defense Contributions per 90": [defence_cont_90, arg_defence_cont_90, fra_defence_cont_90, eng_defence_cont_90, bra_defence_cont_90, prt_defence_cont_90, dut_defence_cont_90, bel_defence_cont_90, ger_defence_cont_90, cro_defence_cont_90, mor_defence_cont_90, col_defence_cont_90, uru_defence_cont_90, sen_defence_cont_90],
    "Defense Duels per 90": [defence_duels_90, arg_defence_duels_90, fra_defence_duels_90, eng_defence_duels_90, bra_defence_duels_90, prt_defence_duels_90, dut_defence_duels_90, bel_defence_duels_90, ger_defence_duels_90, cro_defence_duels_90, mor_defence_duels_90, col_defence_duels_90, uru_defence_duels_90, sen_defence_duels_90],
    "Defense Clearances per 90": [defence_clearance_90, arg_defence_clearance_90, fra_defence_clearance_90, eng_defence_clearance_90, bra_defence_clearance_90, prt_defence_clearance_90, dut_defence_clearance_90, bel_defence_clearance_90, ger_defence_clearance_90, cro_defence_clearance_90, mor_defence_clearance_90, col_defence_clearance_90, uru_defence_clearance_90, sen_defence_clearance_90],
    "Defense Blocks per 90": [defence_blocks_90, arg_defence_blocks_90, fra_defence_blocks_90, eng_defence_blocks_90, bra_defence_blocks_90, prt_defence_blocks_90, dut_defence_blocks_90, bel_defence_blocks_90, ger_defence_blocks_90, cro_defence_blocks_90, mor_defence_blocks_90, col_defence_blocks_90, uru_defence_blocks_90, sen_defence_blocks_90],
    "Defense Take-ons Conceded per 90": [defence_take_ons_conceed_90, arg_defence_take_ons_conceed_90, fra_defence_take_ons_conceed_90, eng_defence_take_ons_conceed_90, bra_defence_take_ons_conceed_90, prt_defence_take_ons_conceed_90, dut_defence_take_ons_conceed_90, bel_defence_take_ons_conceed_90, ger_defence_take_ons_conceed_90, cro_defence_take_ons_conceed_90, mor_defence_take_ons_conceed_90, col_defence_take_ons_conceed_90, uru_defence_take_ons_conceed_90, sen_defence_take_ons_conceed_90],
    "Defense Tackles per 90": [defence_tackle_90, arg_defence_tackle_90, fra_defence_tackle_90, eng_defence_tackle_90, bra_defence_tackle_90, prt_defence_tackle_90, dut_defence_tackle_90, bel_defence_tackle_90, ger_defence_tackle_90, cro_defence_tackle_90, mor_defence_tackle_90, col_defence_tackle_90, uru_defence_tackle_90, sen_defence_tackle_90],
    "Defense Interceptions per 90": [defence_interceptions_90, arg_defence_interceptions_90, fra_defence_interceptions_90, eng_defence_interceptions_90, bra_defence_interceptions_90, prt_defence_interceptions_90, dut_defence_interceptions_90, bel_defence_interceptions_90, ger_defence_interceptions_90, cro_defence_interceptions_90, mor_defence_interceptions_90, col_defence_interceptions_90, uru_defence_interceptions_90, sen_defence_interceptions_90],
    "Defense Duels Won Pct": [esp_def_duels_won_pct.round(2), arg_def_duels_won_pct.round(2), fra_def_duels_won_pct.round(2), eng_def_duels_won_pct.round(2), bra_def_duels_won_pct.round(2), prt_def_duels_won_pct.round(2), dut_def_duels_won_pct.round(2), bel_def_duels_won_pct.round(2), ger_def_duels_won_pct.round(2), cro_def_duels_won_pct.round(2), mor_def_duels_won_pct.round(2), col_def_duels_won_pct.round(2), uru_def_duels_won_pct.round(2), sen_def_duels_won_pct.round(2)],
    "Defense Cards per 90": [esp_def_cards.round(2), arg_def_cards.round(2), fra_def_cards.round(2), eng_def_cards.round(2), bra_def_cards.round(2), prt_def_cards.round(2), dut_def_cards.round(2), bel_def_cards.round(2), ger_def_cards.round(2), cro_def_cards.round(2), mor_def_cards.round(2), col_def_cards.round(2), uru_def_cards.round(2), sen_def_cards.round(2)],
    "Defense Rating": [esp_def_rating.round(2), arg_def_rating.round(2), fra_def_rating.round(2), eng_def_rating.round(2), bra_def_rating.round(2), prt_def_rating.round(2), dut_def_rating.round(2), bel_def_rating.round(2), ger_def_rating.round(2), cro_def_rating.round(2), mor_def_rating.round(2), col_def_rating.round(2), uru_def_rating.round(2), sen_def_rating.round(2)]
})
  
  esp_datax = pd.read_csv("data/spain_players_stats1.csv")
  arg_datax = pd.read_csv("data/argentina_players_stats1.csv")
  bel_datax = pd.read_csv("data/belgium_players_stats1.csv")
  bra_datax = pd.read_csv("data/brazil_players_stats1.csv")
  col_datax = pd.read_csv("data/colombia_players_stats1.csv")
  cro_datax = pd.read_csv("data/croatia_players_stats1.csv")
  eng_datax = pd.read_csv("data/england_players_stats1.csv")
  fra_datax = pd.read_csv("data/france_players_stats1.csv")
  ger_datax = pd.read_csv("data/germany_players_stats1.csv")
  mor_datax = pd.read_csv("data/morroco_players_stats1.csv")
  ned_datax = pd.read_csv("data/netherlands_players_stats1.csv")
  prt_datax = pd.read_csv("data/portugal_players_stats1.csv")
  sen_datax = pd.read_csv("data/senegal_players_stats1.csv")
  uru_datax = pd.read_csv("data/uruguay_players_stats1.csv")

  
  attack = ["forward", "centre forward","left wing","right wing"]
  midfield = ["defensive midfielder", "central midfielder", "attacking midfielder", "left midfielder", "right midfielder"]
 



  def func(x):
    if x in attack:
      return "attack"
    elif x in midfield:
      return "midfield"
    else:
      return "defence"
  esp_datax["traits"] = esp_datax["position"].apply(func)
  arg_datax["traits"] = arg_datax["position"].apply(func)
  fra_datax["traits"] = fra_datax["position"].apply(func)
  bel_datax["traits"] = bel_datax["position"].apply(func)
  bra_datax["traits"] = bra_datax["position"].apply(func)
  col_datax["traits"] = col_datax["position"].apply(func)
  cro_datax["traits"] = cro_datax["position"].apply(func)
  ned_datax["traits"] = ned_datax["position"].apply(func)
  ger_datax["traits"] = ger_datax["position"].apply(func)
  prt_datax["traits"] = prt_datax["position"].apply(func)
  mor_datax["traits"] = mor_datax["position"].apply(func)
  eng_datax["traits"] = eng_datax["position"].apply(func)
  sen_datax["traits"] = sen_datax["position"].apply(func)
  uru_datax["traits"] = uru_datax["position"].apply(func)




  esp_data1 = esp_datax[esp_datax["traits"] == "attack"]
  arg_data1 = arg_datax[arg_datax["traits"] == "attack"]
  fra_data1 = fra_datax[fra_datax["traits"] == "attack"]
  bel_data1 = bel_datax[bel_datax["traits"] == "attack"]
  bra_data1 = bra_datax[bra_datax["traits"] == "attack"]
  col_data1 = col_datax[col_datax["traits"] == "attack"]
  cro_data1 = cro_datax[cro_datax["traits"] == "attack"]
  ned_data1 = ned_datax[ned_datax["traits"] == "attack"]
  ger_data1 = ger_datax[ger_datax["traits"] == "attack"]
  prt_data1 = prt_datax[prt_datax["traits"] == "attack"]
  mor_data1 = mor_datax[mor_datax["traits"] == "attack"]
  eng_data1 = eng_datax[eng_datax["traits"] == "attack"]
  sen_data1 = sen_datax[sen_datax["traits"] == "attack"]
  uru_data1 = uru_datax[uru_datax["traits"] == "attack"]



  esp_data2 = esp_datax[esp_datax["traits"] == "midfield"]
  arg_data2 = arg_datax[arg_datax["traits"] == "midfield"]
  fra_data2 = fra_datax[fra_datax["traits"] == "midfield"]
  bel_data2 = bel_datax[bel_datax["traits"] == "midfield"]
  bra_data2 = bra_datax[bra_datax["traits"] == "midfield"]
  col_data2 = col_datax[col_datax["traits"] == "midfield"]
  cro_data2 = cro_datax[cro_datax["traits"] == "midfield"]
  ned_data2 = ned_datax[ned_datax["traits"] == "midfield"]
  ger_data2 = ger_datax[ger_datax["traits"] == "midfield"]
  prt_data2 = prt_datax[prt_datax["traits"] == "midfield"]
  mor_data2 = mor_datax[mor_datax["traits"] == "midfield"]
  eng_data2 = eng_datax[eng_datax["traits"] == "midfield"]
  sen_data2 = sen_datax[sen_datax["traits"] == "midfield"]
  uru_data2 = uru_datax[uru_datax["traits"] == "midfield"]


  esp_data3 = esp_datax[esp_datax["traits"] == "defence"]
  arg_data3 = arg_datax[arg_datax["traits"] == "defence"]
  fra_data3 = fra_datax[fra_datax["traits"] == "defence"]
  bel_data3 = bel_datax[bel_datax["traits"] == "defence"]
  bra_data3 = bra_datax[bra_datax["traits"] == "defence"]
  col_data3 = col_datax[col_datax["traits"] == "defence"]
  cro_data3 = cro_datax[cro_datax["traits"] == "defence"]
  ned_data3 = ned_datax[ned_datax["traits"] == "defence"]
  ger_data3 = ger_datax[ger_datax["traits"] == "defence"]
  prt_data3 = prt_datax[prt_datax["traits"] == "defence"]
  mor_data3 = mor_datax[mor_datax["traits"] == "defence"]
  eng_data3 = eng_datax[eng_datax["traits"] == "defence"]
  sen_data3 = sen_datax[sen_datax["traits"] == "defence"]
  uru_data3 = uru_datax[uru_datax["traits"] == "defence"]



  esp_att_bar = px.bar(x = "players",y = "ratings", data_frame = esp_data1, color = "position")
  esp_att_bar.update_layout(showlegend=False)
  esp_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = esp_data1, color = "position",orientation='h')
  esp_att_h_bar.update_layout(showlegend=False)
  esp_att_line = px.line(x = "players",y = "assist", data_frame = esp_data1, color = "position",markers=True)
  esp_att_line.update_layout(showlegend=False)
  esp_fig = go.Figure()
  esp_fig.add_trace(go.Scatter(x = esp_data1["players"], y = esp_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  esp_fig.add_trace(go.Scatter(x = esp_data1["players"], y = esp_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  esp_fig.update_layout(showlegend=False)
  esp_fig1 = go.Figure()
  esp_fig1.add_trace(go.Bar(x = esp_data1["players"], y = esp_data1["dribbles completed"], name = "dribbles completed"))
  esp_fig1.add_trace(go.Bar(x = esp_data1["players"], y = esp_data1["dribbles attempt"], name = "dribbles attempted"))
  esp_fig1.update_layout(showlegend=False)
  esp_fig2 = go.Figure()
  esp_fig2.add_trace(go.Scatter(x = esp_data1["players"], y = esp_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  esp_fig2.add_trace(go.Scatter(x = esp_data1["players"], y = esp_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  esp_fig1.update_layout(showlegend=False)

  esp_mid_bar = px.bar(x = "players",y = "ratings", data_frame = esp_data2, color = "position")
  esp_mid_bar.update_layout(showlegend=False)
  esp_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = esp_data2, color = "position",orientation='h')
  esp_mid_h_bar.update_layout(showlegend=False)
  esp_mid_line = px.line(x = "players",y = "interceptions", data_frame = esp_data2, color = "position",markers=True)
  esp_mid_line.update_layout(showlegend=False)
  esp_mid_fig = go.Figure()
  esp_mid_fig.add_trace(go.Scatter(x = esp_data2["players"], y = esp_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  esp_mid_fig.add_trace(go.Scatter(x = esp_data2["players"], y = esp_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  esp_mid_fig.update_layout(showlegend=False)
  esp_mid_fig1 = go.Figure()
  esp_mid_fig1.add_trace(go.Bar(x = esp_data2["players"], y = esp_data2["dribbles completed"], name = "dribbles completed"))
  esp_mid_fig1.add_trace(go.Bar(x = esp_data2["players"], y = esp_data2["dribbles attempt"], name = "dribbles attempted"))
  esp_mid_fig1.update_layout(showlegend=False)
  esp_mid_fig2 = go.Figure()
  esp_mid_fig2.add_trace(go.Scatter(x = esp_data2["players"], y = esp_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  esp_mid_fig2.add_trace(go.Scatter(x = esp_data2["players"], y = esp_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  esp_mid_fig2.update_layout(showlegend=False)


  esp_def_bar = px.bar(x = "players",y = "ratings", data_frame = esp_data3, color = "position")
  esp_def_bar.update_layout(showlegend=False)
  esp_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = esp_data3, color = "position",orientation='h')
  esp_def_h_bar.update_layout(showlegend=False)
  esp_def_line = px.line(x = "players",y = "interceptions", data_frame = esp_data3, color = "position",markers=True)
  esp_def_line.update_layout(showlegend=False)
  esp_def_fig = go.Figure()
  esp_def_fig.add_trace(go.Scatter(x = esp_data3["players"], y = esp_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  esp_def_fig.add_trace(go.Scatter(x = esp_data3["players"], y = esp_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  esp_def_fig.update_layout(showlegend=False)
  esp_def_fig1 = go.Figure()
  esp_def_fig1.add_trace(go.Bar(x = esp_data3["players"], y = esp_data3["clearances"], name = "clearances"))
  esp_def_fig1.add_trace(go.Bar(x = esp_data3["players"], y = esp_data3["blocks"], name = "blocks"))
  esp_def_fig1.update_layout(showlegend=False)
  esp_def_fig2 = go.Figure()
  esp_def_fig2.add_trace(go.Scatter(x = esp_data3["players"], y = esp_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  esp_def_fig2.add_trace(go.Scatter(x = esp_data3["players"], y = esp_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  esp_def_fig2.update_layout(showlegend=False)


  arg_att_bar = px.bar(x = "players",y = "ratings", data_frame = arg_data1, color = "position")
  arg_att_bar.update_layout(showlegend=False)
  arg_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = arg_data1, color = "position",orientation='h')
  arg_att_h_bar.update_layout(showlegend=False)
  arg_att_line = px.line(x = "players",y = "assist", data_frame = arg_data1, color = "position",markers=True)
  arg_att_line.update_layout(showlegend=False)
  arg_fig = go.Figure()
  arg_fig.add_trace(go.Scatter(x = arg_data1["players"], y = arg_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  arg_fig.add_trace(go.Scatter(x = arg_data1["players"], y = arg_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  arg_fig.update_layout(showlegend=False)
  arg_fig1 = go.Figure()
  arg_fig1.add_trace(go.Bar(x = arg_data1["players"], y = arg_data1["dribbles completed"], name = "dribbles completed"))
  arg_fig1.add_trace(go.Bar(x = arg_data1["players"], y = arg_data1["dribbles attempt"], name = "dribbles attempted"))
  arg_fig1.update_layout(showlegend=False)
  arg_fig2 = go.Figure()
  arg_fig2.add_trace(go.Scatter(x = arg_data1["players"], y = arg_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  arg_fig2.add_trace(go.Scatter(x = arg_data1["players"], y = arg_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  arg_fig2.update_layout(showlegend=False)

  arg_mid_bar = px.bar(x = "players",y = "ratings", data_frame = arg_data2, color = "position")
  arg_mid_bar.update_layout(showlegend=False)
  arg_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = arg_data2, color = "position",orientation='h')
  arg_mid_h_bar.update_layout(showlegend=False)
  arg_mid_line = px.line(x = "players",y = "interceptions", data_frame = arg_data2, color = "position",markers=True)
  arg_mid_line.update_layout(showlegend=False)
  arg_mid_fig = go.Figure()
  arg_mid_fig.add_trace(go.Scatter(x = arg_data2["players"], y = arg_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  arg_mid_fig.add_trace(go.Scatter(x = arg_data2["players"], y = arg_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  arg_mid_fig.update_layout(showlegend=False)
  arg_mid_fig1 = go.Figure()
  arg_mid_fig1.add_trace(go.Bar(x = arg_data2["players"], y = arg_data2["dribbles completed"], name = "dribbles completed"))
  arg_mid_fig1.add_trace(go.Bar(x = arg_data2["players"], y = arg_data2["dribbles attempt"], name = "dribbles attempted"))
  arg_mid_fig1.update_layout(showlegend=False)
  arg_mid_fig2 = go.Figure()
  arg_mid_fig2.add_trace(go.Scatter(x = arg_data2["players"], y = arg_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  arg_mid_fig2.add_trace(go.Scatter(x = arg_data2["players"], y = arg_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  arg_mid_fig2.update_layout(showlegend=False)


  arg_def_bar = px.bar(x = "players",y = "ratings", data_frame = arg_data3, color = "position")
  arg_def_bar.update_layout(showlegend=False)
  arg_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = arg_data3, color = "position",orientation='h')
  arg_def_h_bar.update_layout(showlegend=False)
  arg_def_line = px.line(x = "players",y = "interceptions", data_frame = arg_data3, color = "position",markers=True)
  arg_def_line.update_layout(showlegend=False)
  arg_def_fig = go.Figure()
  arg_def_fig.add_trace(go.Scatter(x = arg_data3["players"], y = arg_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  arg_def_fig.add_trace(go.Scatter(x = arg_data3["players"], y = arg_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  arg_def_fig.update_layout(showlegend=False)
  arg_def_fig1 = go.Figure()
  arg_def_fig1.add_trace(go.Bar(x = arg_data3["players"], y = arg_data3["clearances"], name = "clearances"))
  arg_def_fig1.add_trace(go.Bar(x = arg_data3["players"], y = arg_data3["blocks"], name = "blocks"))
  arg_def_fig1.update_layout(showlegend=False)
  arg_def_fig2 = go.Figure()
  arg_def_fig2.add_trace(go.Scatter(x = arg_data3["players"], y = arg_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  arg_def_fig2.add_trace(go.Scatter(x = arg_data3["players"], y = arg_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  arg_def_fig2.update_layout(showlegend=False)


  



  bel_att_bar = px.bar(x = "players",y = "ratings", data_frame = bel_data1, color = "position")
  bel_att_bar.update_layout(showlegend=False)
  bel_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = bel_data1, color = "position",orientation='h')
  bel_att_h_bar.update_layout(showlegend=False)
  bel_att_line = px.line(x = "players",y = "assist", data_frame = bel_data1, color = "position",markers=True)
  bel_att_line.update_layout(showlegend=False)
  bel_fig = go.Figure()
  bel_fig.add_trace(go.Scatter(x = bel_data1["players"], y = bel_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  bel_fig.add_trace(go.Scatter(x = bel_data1["players"], y = bel_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  bel_fig.update_layout(showlegend=False)
  bel_fig1 = go.Figure()
  bel_fig1.add_trace(go.Bar(x = bel_data1["players"], y = bel_data1["dribbles completed"], name = "dribbles completed"))
  bel_fig1.add_trace(go.Bar(x = bel_data1["players"], y = bel_data1["dribbles attempt"], name = "dribbles attempted"))
  bel_fig1.update_layout(showlegend=False)
  bel_fig2 = go.Figure()
  bel_fig2.add_trace(go.Scatter(x = bel_data1["players"], y = bel_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  bel_fig2.add_trace(go.Scatter(x = bel_data1["players"], y = bel_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  bel_fig2.update_layout(showlegend=False)

  bel_mid_bar = px.bar(x = "players",y = "ratings", data_frame = bel_data2, color = "position")
  bel_mid_bar.update_layout(showlegend=False)
  bel_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = bel_data2, color = "position",orientation='h')
  bel_mid_h_bar.update_layout(showlegend=False)
  bel_mid_line = px.line(x = "players",y = "interceptions", data_frame = bel_data2, color = "position",markers=True)
  bel_mid_line.update_layout(showlegend=False)
  bel_mid_fig = go.Figure()
  bel_mid_fig.add_trace(go.Scatter(x = bel_data2["players"], y = bel_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  bel_mid_fig.add_trace(go.Scatter(x = bel_data2["players"], y = bel_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  bel_mid_fig.update_layout(showlegend=False)
  bel_mid_fig1 = go.Figure()
  bel_mid_fig1.add_trace(go.Bar(x = bel_data2["players"], y = bel_data2["dribbles completed"], name = "dribbles completed"))
  bel_mid_fig1.add_trace(go.Bar(x = bel_data2["players"], y = bel_data2["dribbles attempt"], name = "dribbles attempted"))
  bel_mid_fig1.update_layout(showlegend=False)
  bel_mid_fig2 = go.Figure()
  bel_mid_fig2.add_trace(go.Scatter(x = bel_data2["players"], y = bel_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  bel_mid_fig2.add_trace(go.Scatter(x = bel_data2["players"], y = bel_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  bel_mid_fig2.update_layout(showlegend=False)


  bel_def_bar = px.bar(x = "players",y = "ratings", data_frame = bel_data3, color = "position")
  bel_def_bar.update_layout(showlegend=False)
  bel_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = bel_data3, color = "position",orientation='h')
  bel_def_h_bar.update_layout(showlegend=False)
  bel_def_line = px.line(x = "players",y = "interceptions", data_frame = bel_data3, color = "position",markers=True)
  bel_def_line.update_layout(showlegend=False)
  bel_def_fig = go.Figure()
  bel_def_fig.add_trace(go.Scatter(x = bel_data3["players"], y = bel_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  bel_def_fig.add_trace(go.Scatter(x = bel_data3["players"], y = bel_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  bel_def_fig.update_layout(showlegend=False)
  bel_def_fig1 = go.Figure()
  bel_def_fig1.add_trace(go.Bar(x = bel_data3["players"], y = bel_data3["clearances"], name = "clearances"))
  bel_def_fig1.add_trace(go.Bar(x = bel_data3["players"], y = bel_data3["blocks"], name = "blocks"))
  bel_def_fig1.update_layout(showlegend=False)
  bel_def_fig2 = go.Figure()
  bel_def_fig2.add_trace(go.Scatter(x = bel_data3["players"], y = bel_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  bel_def_fig2.add_trace(go.Scatter(x = bel_data3["players"], y = bel_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  bel_def_fig2.update_layout(showlegend=False)

    
  bra_att_bar = px.bar(x = "players",y = "ratings", data_frame = bra_data1, color = "position")
  bra_att_bar.update_layout(showlegend=False)
  bra_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = bra_data1, color = "position",orientation='h')
  bra_att_h_bar.update_layout(showlegend=False)
  bra_att_line = px.line(x = "players",y = "assist", data_frame = bra_data1, color = "position",markers=True)
  bra_att_line.update_layout(showlegend=False)
  bra_fig = go.Figure()
  bra_fig.add_trace(go.Scatter(x = bra_data1["players"], y = bra_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  bra_fig.add_trace(go.Scatter(x = bra_data1["players"], y = bra_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  bra_fig.update_layout(showlegend=False)
  bra_fig1 = go.Figure()
  bra_fig1.add_trace(go.Bar(x = bra_data1["players"], y = bra_data1["dribbles completed"], name = "dribbles completed"))
  bra_fig1.add_trace(go.Bar(x = bra_data1["players"], y = bra_data1["dribbles attempt"], name = "dribbles attempted"))
  bra_fig1.update_layout(showlegend=False)
  bra_fig2 = go.Figure()
  bra_fig2.add_trace(go.Scatter(x = bra_data1["players"], y = bra_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  bra_fig2.add_trace(go.Scatter(x = bra_data1["players"], y = bra_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  bra_fig2.update_layout(showlegend=False)

  bra_mid_bar = px.bar(x = "players",y = "ratings", data_frame = bra_data2, color = "position")
  bra_mid_bar.update_layout(showlegend=False)
  bra_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = bra_data2, color = "position",orientation='h')
  bra_mid_h_bar.update_layout(showlegend=False)
  bra_mid_line = px.line(x = "players",y = "interceptions", data_frame = bra_data2, color = "position",markers=True)
  bra_mid_line.update_layout(showlegend=False)
  bra_mid_fig = go.Figure()
  bra_mid_fig.add_trace(go.Scatter(x = bra_data2["players"], y = bra_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  bra_mid_fig.add_trace(go.Scatter(x = bra_data2["players"], y = bra_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  bra_mid_fig.update_layout(showlegend=False)
  bra_mid_fig1 = go.Figure()
  bra_mid_fig1.add_trace(go.Bar(x = bra_data2["players"], y = bra_data2["dribbles completed"], name = "dribbles completed"))
  bra_mid_fig1.add_trace(go.Bar(x = bra_data2["players"], y = bra_data2["dribbles attempt"], name = "dribbles attempted"))
  bra_mid_fig1.update_layout(showlegend=False)
  bra_mid_fig2 = go.Figure()
  bra_mid_fig2.add_trace(go.Scatter(x = bra_data2["players"], y = bra_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  bra_mid_fig2.add_trace(go.Scatter(x = bra_data2["players"], y = bra_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  bra_mid_fig2.update_layout(showlegend=False)


  bra_def_bar = px.bar(x = "players",y = "ratings", data_frame = bra_data3, color = "position")
  bra_def_bar.update_layout(showlegend=False)
  bra_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = bra_data3, color = "position",orientation='h')
  bra_def_h_bar.update_layout(showlegend=False)
  bra_def_line = px.line(x = "players",y = "interceptions", data_frame = bra_data3, color = "position",markers=True)
  bra_def_line.update_layout(showlegend=False)
  bra_def_fig = go.Figure()
  bra_def_fig.add_trace(go.Scatter(x = bra_data3["players"], y = bra_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  bra_def_fig.add_trace(go.Scatter(x = bra_data3["players"], y = bra_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  bra_def_fig.update_layout(showlegend=False)
  bra_def_fig1 = go.Figure()
  bra_def_fig1.add_trace(go.Bar(x = bra_data3["players"], y = bra_data3["clearances"], name = "clearances"))
  bra_def_fig1.add_trace(go.Bar(x = bra_data3["players"], y = bra_data3["blocks"], name = "blocks"))
  bra_def_fig1.update_layout(showlegend=False)
  bra_def_fig2 = go.Figure()
  bra_def_fig2.add_trace(go.Scatter(x = bra_data3["players"], y = bra_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  bra_def_fig2.add_trace(go.Scatter(x = bra_data3["players"], y = bra_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  bra_def_fig2.update_layout(showlegend=False)
    




  col_att_bar = px.bar(x = "players",y = "ratings", data_frame = col_data1, color = "position")
  col_att_bar.update_layout(showlegend=False)
  col_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = col_data1, color = "position",orientation='h')
  col_att_h_bar.update_layout(showlegend=False)
  col_att_line = px.line(x = "players",y = "assist", data_frame = col_data1, color = "position",markers=True)
  col_att_line.update_layout(showlegend=False)
  col_fig = go.Figure()
  col_fig.add_trace(go.Scatter(x = col_data1["players"], y = col_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  col_fig.add_trace(go.Scatter(x = col_data1["players"], y = col_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  col_fig.update_layout(showlegend=False)
  col_fig1 = go.Figure()
  col_fig1.add_trace(go.Bar(x = col_data1["players"], y = col_data1["dribbles completed"], name = "dribbles completed"))
  col_fig1.add_trace(go.Bar(x = col_data1["players"], y = col_data1["dribbles attempt"], name = "dribbles attempted"))
  col_fig1.update_layout(showlegend=False)
  col_fig2 = go.Figure()
  col_fig2.add_trace(go.Scatter(x = col_data1["players"], y = col_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  col_fig2.add_trace(go.Scatter(x = col_data1["players"], y = col_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  col_fig1.update_layout(showlegend=False)

  col_mid_bar = px.bar(x = "players",y = "ratings", data_frame = col_data2, color = "position")
  col_mid_bar.update_layout(showlegend=False)
  col_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = col_data2, color = "position",orientation='h')
  col_mid_h_bar.update_layout(showlegend=False)
  col_mid_line = px.line(x = "players",y = "interceptions", data_frame = col_data2, color = "position",markers=True)
  col_mid_line.update_layout(showlegend=False)
  col_mid_fig = go.Figure()
  col_mid_fig.add_trace(go.Scatter(x = col_data2["players"], y = col_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  col_mid_fig.add_trace(go.Scatter(x = col_data2["players"], y = col_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  col_mid_fig.update_layout(showlegend=False)
  col_mid_fig1 = go.Figure()
  col_mid_fig1.add_trace(go.Bar(x = col_data2["players"], y = col_data2["dribbles completed"], name = "dribbles completed"))
  col_mid_fig1.add_trace(go.Bar(x = col_data2["players"], y = col_data2["dribbles attempt"], name = "dribbles attempted"))
  col_mid_fig1.update_layout(showlegend=False)
  col_mid_fig2 = go.Figure()
  col_mid_fig2.add_trace(go.Scatter(x = col_data2["players"], y = col_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  col_mid_fig2.add_trace(go.Scatter(x = col_data2["players"], y = col_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  col_mid_fig2.update_layout(showlegend=False)


  col_def_bar = px.bar(x = "players",y = "ratings", data_frame = col_data3, color = "position")
  col_def_bar.update_layout(showlegend=False)
  col_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = col_data3, color = "position",orientation='h')
  col_def_h_bar.update_layout(showlegend=False)
  col_def_line = px.line(x = "players",y = "interceptions", data_frame = col_data3, color = "position",markers=True)
  col_def_line.update_layout(showlegend=False)
  col_def_fig = go.Figure()
  col_def_fig.add_trace(go.Scatter(x = col_data3["players"], y = col_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  col_def_fig.add_trace(go.Scatter(x = col_data3["players"], y = col_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  col_def_fig.update_layout(showlegend=False)
  col_def_fig1 = go.Figure()
  col_def_fig1.add_trace(go.Bar(x = col_data3["players"], y = col_data3["clearances"], name = "clearances"))
  col_def_fig1.add_trace(go.Bar(x = col_data3["players"], y = col_data3["blocks"], name = "blocks"))
  col_def_fig1.update_layout(showlegend=False)
  col_def_fig2 = go.Figure()
  col_def_fig2.add_trace(go.Scatter(x = col_data3["players"], y = col_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  col_def_fig2.add_trace(go.Scatter(x = col_data3["players"], y = col_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  col_def_fig2.update_layout(showlegend=False)








  cro_att_bar = px.bar(x = "players",y = "ratings", data_frame = cro_data1, color = "position")
  cro_att_bar.update_layout(showlegend=False)
  cro_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = cro_data1, color = "position",orientation='h')
  cro_att_h_bar.update_layout(showlegend=False)
  cro_att_line = px.line(x = "players",y = "assist", data_frame = cro_data1, color = "position",markers=True)
  cro_att_line.update_layout(showlegend=False)
  cro_fig = go.Figure()
  cro_fig.add_trace(go.Scatter(x = cro_data1["players"], y = cro_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  cro_fig.add_trace(go.Scatter(x = cro_data1["players"], y = cro_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  cro_fig.update_layout(showlegend=False)
  cro_fig1 = go.Figure()
  cro_fig1.add_trace(go.Bar(x = cro_data1["players"], y = cro_data1["dribbles completed"], name = "dribbles completed"))
  cro_fig1.add_trace(go.Bar(x = cro_data1["players"], y = cro_data1["dribbles attempt"], name = "dribbles attempted"))
  cro_fig1.update_layout(showlegend=False)
  cro_fig2 = go.Figure()
  cro_fig2.add_trace(go.Scatter(x = cro_data1["players"], y = cro_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  cro_fig2.add_trace(go.Scatter(x = cro_data1["players"], y = cro_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  cro_fig2.update_layout(showlegend=False)

  cro_mid_bar = px.bar(x = "players",y = "ratings", data_frame = cro_data2, color = "position")
  cro_mid_bar.update_layout(showlegend=False)
  cro_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = cro_data2, color = "position",orientation='h')
  cro_mid_h_bar.update_layout(showlegend=False)
  cro_mid_line = px.line(x = "players",y = "interceptions", data_frame = cro_data2, color = "position",markers=True)
  cro_mid_line.update_layout(showlegend=False)
  cro_mid_fig = go.Figure()
  cro_mid_fig.add_trace(go.Scatter(x = cro_data2["players"], y = cro_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  cro_mid_fig.add_trace(go.Scatter(x = cro_data2["players"], y = cro_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  cro_mid_fig.update_layout(showlegend=False)
  cro_mid_fig1 = go.Figure()
  cro_mid_fig1.add_trace(go.Bar(x = cro_data2["players"], y = cro_data2["dribbles completed"], name = "dribbles completed"))
  cro_mid_fig1.add_trace(go.Bar(x = cro_data2["players"], y = cro_data2["dribbles attempt"], name = "dribbles attempted"))
  cro_mid_fig1.update_layout(showlegend=False)
  cro_mid_fig2 = go.Figure()
  cro_mid_fig2.add_trace(go.Scatter(x = cro_data2["players"], y = cro_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  cro_mid_fig2.add_trace(go.Scatter(x = cro_data2["players"], y = cro_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  cro_mid_fig2.update_layout(showlegend=False)


  cro_def_bar = px.bar(x = "players",y = "ratings", data_frame = cro_data3, color = "position")
  cro_def_bar.update_layout(showlegend=False)
  cro_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = cro_data3, color = "position",orientation='h')
  cro_def_h_bar.update_layout(showlegend=False)
  cro_def_line = px.line(x = "players",y = "interceptions", data_frame = cro_data3, color = "position",markers=True)
  cro_def_line.update_layout(showlegend=False)
  cro_def_fig = go.Figure()
  cro_def_fig.add_trace(go.Scatter(x = cro_data3["players"], y = cro_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  cro_def_fig.add_trace(go.Scatter(x = cro_data3["players"], y = cro_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  cro_def_fig.update_layout(showlegend=False)
  cro_def_fig1 = go.Figure()
  cro_def_fig1.add_trace(go.Bar(x = cro_data3["players"], y = cro_data3["clearances"], name = "clearances"))
  cro_def_fig1.add_trace(go.Bar(x = cro_data3["players"], y = cro_data3["blocks"], name = "blocks"))
  cro_def_fig1.update_layout(showlegend=False)
  cro_def_fig2 = go.Figure()
  cro_def_fig2.add_trace(go.Scatter(x = cro_data3["players"], y = cro_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  cro_def_fig2.add_trace(go.Scatter(x = cro_data3["players"], y = cro_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  cro_def_fig2.update_layout(showlegend=False)




  ned_att_bar = px.bar(x = "players",y = "ratings", data_frame = ned_data1, color = "position")
  ned_att_bar.update_layout(showlegend=False)
  ned_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = ned_data1, color = "position",orientation='h')
  ned_att_h_bar.update_layout(showlegend=False)
  ned_att_line = px.line(x = "players",y = "assist", data_frame = ned_data1, color = "position",markers=True)
  ned_att_line.update_layout(showlegend=False)
  ned_fig = go.Figure()
  ned_fig.add_trace(go.Scatter(x = ned_data1["players"], y = ned_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  ned_fig.add_trace(go.Scatter(x = ned_data1["players"], y = ned_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  ned_fig.update_layout(showlegend=False)
  ned_fig1 = go.Figure()
  ned_fig1.add_trace(go.Bar(x = ned_data1["players"], y = ned_data1["dribbles completed"], name = "dribbles completed"))
  ned_fig1.add_trace(go.Bar(x = ned_data1["players"], y = ned_data1["dribbles attempt"], name = "dribbles attempted"))
  ned_fig1.update_layout(showlegend=False)
  ned_fig2 = go.Figure()
  ned_fig2.add_trace(go.Scatter(x = ned_data1["players"], y = ned_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  ned_fig2.add_trace(go.Scatter(x = ned_data1["players"], y = ned_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  ned_fig2.update_layout(showlegend=False)

  ned_mid_bar = px.bar(x = "players",y = "ratings", data_frame = ned_data2, color = "position")
  ned_mid_bar.update_layout(showlegend=False)
  ned_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = ned_data2, color = "position",orientation='h')
  ned_mid_h_bar.update_layout(showlegend=False)
  ned_mid_line = px.line(x = "players",y = "interceptions", data_frame = ned_data2, color = "position",markers=True)
  ned_mid_line.update_layout(showlegend=False)
  ned_mid_fig = go.Figure()
  ned_mid_fig.add_trace(go.Scatter(x = ned_data2["players"], y = ned_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  ned_mid_fig.add_trace(go.Scatter(x = ned_data2["players"], y = ned_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  ned_mid_fig.update_layout(showlegend=False)
  ned_mid_fig1 = go.Figure()
  ned_mid_fig1.add_trace(go.Bar(x = ned_data2["players"], y = ned_data2["dribbles completed"], name = "dribbles completed"))
  ned_mid_fig1.add_trace(go.Bar(x = ned_data2["players"], y = ned_data2["dribbles attempt"], name = "dribbles attempted"))
  ned_mid_fig1.update_layout(showlegend=False)
  ned_mid_fig2 = go.Figure()
  ned_mid_fig2.add_trace(go.Scatter(x = ned_data2["players"], y = ned_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  ned_mid_fig2.add_trace(go.Scatter(x = ned_data2["players"], y = ned_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  ned_mid_fig2.update_layout(showlegend=False)


  ned_def_bar = px.bar(x = "players",y = "ratings", data_frame = ned_data3, color = "position")
  ned_def_bar.update_layout(showlegend=False)
  ned_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = ned_data3, color = "position",orientation='h')
  ned_def_h_bar.update_layout(showlegend=False)
  ned_def_line = px.line(x = "players",y = "interceptions", data_frame = ned_data3, color = "position",markers=True)
  ned_def_line.update_layout(showlegend=False)
  ned_def_fig = go.Figure()
  ned_def_fig.add_trace(go.Scatter(x = ned_data3["players"], y = ned_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  ned_def_fig.add_trace(go.Scatter(x = ned_data3["players"], y = ned_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  ned_def_fig.update_layout(showlegend=False)
  ned_def_fig1 = go.Figure()
  ned_def_fig1.add_trace(go.Bar(x = ned_data3["players"], y = ned_data3["clearances"], name = "clearances"))
  ned_def_fig1.add_trace(go.Bar(x = ned_data3["players"], y = ned_data3["blocks"], name = "blocks"))
  ned_def_fig1.update_layout(showlegend=False)
  ned_def_fig2 = go.Figure()
  ned_def_fig2.add_trace(go.Scatter(x = ned_data3["players"], y = ned_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  ned_def_fig2.add_trace(go.Scatter(x = ned_data3["players"], y = ned_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  ned_def_fig2.update_layout(showlegend=False)









  fra_att_bar = px.bar(x = "players",y = "ratings", data_frame = fra_data1, color = "position")
  fra_att_bar.update_layout(showlegend=False)
  fra_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = fra_data1, color = "position",orientation='h')
  fra_att_h_bar.update_layout(showlegend=False)
  fra_att_line = px.line(x = "players",y = "assist", data_frame = fra_data1, color = "position",markers=True)
  fra_att_line.update_layout(showlegend=False)
  fra_fig = go.Figure()
  fra_fig.add_trace(go.Scatter(x = fra_data1["players"], y = fra_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  fra_fig.add_trace(go.Scatter(x = fra_data1["players"], y = fra_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  fra_fig.update_layout(showlegend=False)
  fra_fig1 = go.Figure()
  fra_fig1.add_trace(go.Bar(x = fra_data1["players"], y = fra_data1["dribbles completed"], name = "dribbles completed"))
  fra_fig1.add_trace(go.Bar(x = fra_data1["players"], y = fra_data1["dribbles attempt"], name = "dribbles attempted"))
  fra_fig1.update_layout(showlegend=False)
  fra_fig2 = go.Figure()
  fra_fig2.add_trace(go.Scatter(x = fra_data1["players"], y = fra_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  fra_fig2.add_trace(go.Scatter(x = fra_data1["players"], y = fra_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  fra_fig1.update_layout(showlegend=False)

  fra_mid_bar = px.bar(x = "players",y = "ratings", data_frame = fra_data2, color = "position")
  fra_mid_bar.update_layout(showlegend=False)
  fra_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = fra_data2, color = "position",orientation='h')
  fra_mid_h_bar.update_layout(showlegend=False)
  fra_mid_line = px.line(x = "players",y = "interceptions", data_frame = fra_data2, color = "position",markers=True)
  fra_mid_line.update_layout(showlegend=False)
  fra_mid_fig = go.Figure()
  fra_mid_fig.add_trace(go.Scatter(x = fra_data2["players"], y = fra_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  fra_mid_fig.add_trace(go.Scatter(x = fra_data2["players"], y = fra_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  fra_mid_fig.update_layout(showlegend=False)
  fra_mid_fig1 = go.Figure()
  fra_mid_fig1.add_trace(go.Bar(x = fra_data2["players"], y = fra_data2["dribbles completed"], name = "dribbles completed"))
  fra_mid_fig1.add_trace(go.Bar(x = fra_data2["players"], y = fra_data2["dribbles attempt"], name = "dribbles attempted"))
  fra_mid_fig1.update_layout(showlegend=False)
  fra_mid_fig2 = go.Figure()
  fra_mid_fig2.add_trace(go.Scatter(x = fra_data2["players"], y = fra_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  fra_mid_fig2.add_trace(go.Scatter(x = fra_data2["players"], y = fra_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  fra_mid_fig2.update_layout(showlegend=False)

  fra_def_bar = px.bar(x = "players",y = "ratings", data_frame = fra_data3, color = "position")
  fra_def_bar.update_layout(showlegend=False)
  fra_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = fra_data3, color = "position",orientation='h')
  fra_def_h_bar.update_layout(showlegend=False)
  fra_def_line = px.line(x = "players",y = "interceptions", data_frame = fra_data3, color = "position",markers=True)
  fra_def_line.update_layout(showlegend=False)
  fra_def_fig = go.Figure()
  fra_def_fig.add_trace(go.Scatter(x = fra_data3["players"], y = fra_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  fra_def_fig.add_trace(go.Scatter(x = fra_data3["players"], y = fra_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  fra_def_fig.update_layout(showlegend=False)
  fra_def_fig1 = go.Figure()
  fra_def_fig1.add_trace(go.Bar(x = fra_data3["players"], y = fra_data3["clearances"], name = "clearances"))
  fra_def_fig1.add_trace(go.Bar(x = fra_data3["players"], y = fra_data3["blocks"], name = "blocks"))
  fra_def_fig1.update_layout(showlegend=False)
  fra_def_fig2 = go.Figure()
  fra_def_fig2.add_trace(go.Scatter(x = fra_data3["players"], y = fra_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  fra_def_fig2.add_trace(go.Scatter(x = fra_data3["players"], y = fra_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  fra_def_fig2.update_layout(showlegend=False)






  ger_att_bar = px.bar(x = "players",y = "ratings", data_frame = ger_data1, color = "position")
  ger_att_bar.update_layout(showlegend=False)
  ger_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = ger_data1, color = "position",orientation='h')
  ger_att_h_bar.update_layout(showlegend=False)
  ger_att_line = px.line(x = "players",y = "assist", data_frame = ger_data1, color = "position",markers=True)
  ger_att_line.update_layout(showlegend=False)
  ger_fig = go.Figure()
  ger_fig.add_trace(go.Scatter(x = ger_data1["players"], y = ger_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  ger_fig.add_trace(go.Scatter(x = ger_data1["players"], y = ger_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  ger_fig.update_layout(showlegend=False)
  ger_fig1 = go.Figure()
  ger_fig1.add_trace(go.Bar(x = ger_data1["players"], y = ger_data1["dribbles completed"], name = "dribbles completed"))
  ger_fig1.add_trace(go.Bar(x = ger_data1["players"], y = ger_data1["dribbles attempt"], name = "dribbles attempted"))
  ger_fig1.update_layout(showlegend=False)
  ger_fig2 = go.Figure()
  ger_fig2.add_trace(go.Scatter(x = ger_data1["players"], y = ger_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  ger_fig2.add_trace(go.Scatter(x = ger_data1["players"], y = ger_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  ger_fig1.update_layout(showlegend=False)

  ger_mid_bar = px.bar(x = "players",y = "ratings", data_frame = ger_data2, color = "position")
  ger_mid_bar.update_layout(showlegend=False)
  ger_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = ger_data2, color = "position",orientation='h')
  ger_mid_h_bar.update_layout(showlegend=False)
  ger_mid_line = px.line(x = "players",y = "interceptions", data_frame = ger_data2, color = "position",markers=True)
  ger_mid_line.update_layout(showlegend=False)
  ger_mid_fig = go.Figure()
  ger_mid_fig.add_trace(go.Scatter(x = ger_data2["players"], y = ger_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  ger_mid_fig.add_trace(go.Scatter(x = ger_data2["players"], y = ger_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  ger_mid_fig.update_layout(showlegend=False)
  ger_mid_fig1 = go.Figure()
  ger_mid_fig1.add_trace(go.Bar(x = ger_data2["players"], y = ger_data2["dribbles completed"], name = "dribbles completed"))
  ger_mid_fig1.add_trace(go.Bar(x = ger_data2["players"], y = ger_data2["dribbles attempt"], name = "dribbles attempted"))
  ger_mid_fig1.update_layout(showlegend=False)
  ger_mid_fig2 = go.Figure()
  ger_mid_fig2.add_trace(go.Scatter(x = ger_data2["players"], y = ger_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  ger_mid_fig2.add_trace(go.Scatter(x = ger_data2["players"], y = ger_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  ger_mid_fig2.update_layout(showlegend=False)

  ger_def_bar = px.bar(x = "players",y = "ratings", data_frame = ger_data3, color = "position")
  ger_def_bar.update_layout(showlegend=False)
  ger_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = ger_data3, color = "position",orientation='h')
  ger_def_h_bar.update_layout(showlegend=False)
  ger_def_line = px.line(x = "players",y = "interceptions", data_frame = ger_data3, color = "position",markers=True)
  ger_def_line.update_layout(showlegend=False)
  ger_def_fig = go.Figure()
  ger_def_fig.add_trace(go.Scatter(x = ger_data3["players"], y = ger_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  ger_def_fig.add_trace(go.Scatter(x = ger_data3["players"], y = ger_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  ger_def_fig.update_layout(showlegend=False)
  ger_def_fig1 = go.Figure()
  ger_def_fig1.add_trace(go.Bar(x = ger_data3["players"], y = ger_data3["clearances"], name = "clearances"))
  ger_def_fig1.add_trace(go.Bar(x = ger_data3["players"], y = ger_data3["blocks"], name = "blocks"))
  ger_def_fig1.update_layout(showlegend=False)
  ger_def_fig2 = go.Figure()
  ger_def_fig2.add_trace(go.Scatter(x = ger_data3["players"], y = ger_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  ger_def_fig2.add_trace(go.Scatter(x = ger_data3["players"], y = ger_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  ger_def_fig2.update_layout(showlegend=False)





  eng_att_bar = px.bar(x = "players",y = "ratings", data_frame = eng_data1, color = "position")
  eng_att_bar.update_layout(showlegend=False)
  eng_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = eng_data1, color = "position",orientation='h')
  eng_att_h_bar.update_layout(showlegend=False)
  eng_att_line = px.line(x = "players",y = "assist", data_frame = eng_data1, color = "position",markers=True)
  eng_att_line.update_layout(showlegend=False)
  eng_fig = go.Figure()
  eng_fig.add_trace(go.Scatter(x = eng_data1["players"], y = eng_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  eng_fig.add_trace(go.Scatter(x = eng_data1["players"], y = eng_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  eng_fig.update_layout(showlegend=False)
  eng_fig1 = go.Figure()
  eng_fig1.add_trace(go.Bar(x = eng_data1["players"], y = eng_data1["dribbles completed"], name = "dribbles completed"))
  eng_fig1.add_trace(go.Bar(x = eng_data1["players"], y = eng_data1["dribbles attempt"], name = "dribbles attempted"))
  eng_fig1.update_layout(showlegend=False)
  eng_fig2 = go.Figure()
  eng_fig2.add_trace(go.Scatter(x = eng_data1["players"], y = eng_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  eng_fig2.add_trace(go.Scatter(x = eng_data1["players"], y = eng_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  eng_fig1.update_layout(showlegend=False)

  eng_mid_bar = px.bar(x = "players",y = "ratings", data_frame = eng_data2, color = "position")
  eng_mid_bar.update_layout(showlegend=False)
  eng_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = eng_data2, color = "position",orientation='h')
  eng_mid_h_bar.update_layout(showlegend=False)
  eng_mid_line = px.line(x = "players",y = "interceptions", data_frame = eng_data2, color = "position",markers=True)
  eng_mid_line.update_layout(showlegend=False)
  eng_mid_fig = go.Figure()
  eng_mid_fig.add_trace(go.Scatter(x = eng_data2["players"], y = eng_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  eng_mid_fig.add_trace(go.Scatter(x = eng_data2["players"], y = eng_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  eng_mid_fig.update_layout(showlegend=False)
  eng_mid_fig1 = go.Figure()
  eng_mid_fig1.add_trace(go.Bar(x = eng_data2["players"], y = eng_data2["dribbles completed"], name = "dribbles completed"))
  eng_mid_fig1.add_trace(go.Bar(x = eng_data2["players"], y = eng_data2["dribbles attempt"], name = "dribbles attempted"))
  eng_mid_fig1.update_layout(showlegend=False)
  eng_mid_fig2 = go.Figure()
  eng_mid_fig2.add_trace(go.Scatter(x = eng_data2["players"], y = eng_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  eng_mid_fig2.add_trace(go.Scatter(x = eng_data2["players"], y = eng_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  eng_mid_fig2.update_layout(showlegend=False)

  eng_def_bar = px.bar(x = "players",y = "ratings", data_frame = eng_data3, color = "position")
  eng_def_bar.update_layout(showlegend=False)
  eng_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = eng_data3, color = "position",orientation='h')
  eng_def_h_bar.update_layout(showlegend=False)
  eng_def_line = px.line(x = "players",y = "interceptions", data_frame = eng_data3, color = "position",markers=True)
  eng_def_line.update_layout(showlegend=False)
  eng_def_fig = go.Figure()
  eng_def_fig.add_trace(go.Scatter(x = eng_data3["players"], y = eng_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  eng_def_fig.add_trace(go.Scatter(x = eng_data3["players"], y = eng_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  eng_def_fig.update_layout(showlegend=False)
  eng_def_fig1 = go.Figure()
  eng_def_fig1.add_trace(go.Bar(x = eng_data3["players"], y = eng_data3["clearances"], name = "clearances"))
  eng_def_fig1.add_trace(go.Bar(x = eng_data3["players"], y = eng_data3["blocks"], name = "blocks"))
  eng_def_fig1.update_layout(showlegend=False)
  eng_def_fig2 = go.Figure()
  eng_def_fig2.add_trace(go.Scatter(x = eng_data3["players"], y = eng_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  eng_def_fig2.add_trace(go.Scatter(x = eng_data3["players"], y = eng_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  eng_def_fig2.update_layout(showlegend=False)





  mor_att_bar = px.bar(x = "players",y = "ratings", data_frame = mor_data1, color = "position")
  mor_att_bar.update_layout(showlegend=False)
  mor_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = mor_data1, color = "position",orientation='h')
  mor_att_h_bar.update_layout(showlegend=False)
  mor_att_line = px.line(x = "players",y = "assist", data_frame = mor_data1, color = "position",markers=True)
  mor_att_line.update_layout(showlegend=False)
  mor_fig = go.Figure()
  mor_fig.add_trace(go.Scatter(x = mor_data1["players"], y = mor_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  mor_fig.add_trace(go.Scatter(x = mor_data1["players"], y = mor_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  mor_fig.update_layout(showlegend=False)
  mor_fig1 = go.Figure()
  mor_fig1.add_trace(go.Bar(x = mor_data1["players"], y = mor_data1["dribbles completed"], name = "dribbles completed"))
  mor_fig1.add_trace(go.Bar(x = mor_data1["players"], y = mor_data1["dribbles attempt"], name = "dribbles attempted"))
  mor_fig1.update_layout(showlegend=False)
  mor_fig2 = go.Figure()
  mor_fig2.add_trace(go.Scatter(x = mor_data1["players"], y = mor_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  mor_fig2.add_trace(go.Scatter(x = mor_data1["players"], y = mor_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  mor_fig1.update_layout(showlegend=False)

  mor_mid_bar = px.bar(x = "players",y = "ratings", data_frame = mor_data2, color = "position")
  mor_mid_bar.update_layout(showlegend=False)
  mor_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = mor_data2, color = "position",orientation='h')
  mor_mid_h_bar.update_layout(showlegend=False)
  mor_mid_line = px.line(x = "players",y = "interceptions", data_frame = mor_data2, color = "position",markers=True)
  mor_mid_line.update_layout(showlegend=False)
  mor_mid_fig = go.Figure()
  mor_mid_fig.add_trace(go.Scatter(x = mor_data2["players"], y = mor_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  mor_mid_fig.add_trace(go.Scatter(x = mor_data2["players"], y = mor_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  mor_mid_fig.update_layout(showlegend=False)
  mor_mid_fig1 = go.Figure()
  mor_mid_fig1.add_trace(go.Bar(x = mor_data2["players"], y = mor_data2["dribbles completed"], name = "dribbles completed"))
  mor_mid_fig1.add_trace(go.Bar(x = mor_data2["players"], y = mor_data2["dribbles attempt"], name = "dribbles attempted"))
  mor_mid_fig1.update_layout(showlegend=False)
  mor_mid_fig2 = go.Figure()
  mor_mid_fig2.add_trace(go.Scatter(x = mor_data2["players"], y = mor_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  mor_mid_fig2.add_trace(go.Scatter(x = mor_data2["players"], y = mor_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  mor_mid_fig2.update_layout(showlegend=False)

  mor_def_bar = px.bar(x = "players",y = "ratings", data_frame = mor_data3, color = "position")
  mor_def_bar.update_layout(showlegend=False)
  mor_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = mor_data3, color = "position",orientation='h')
  mor_def_h_bar.update_layout(showlegend=False)
  mor_def_line = px.line(x = "players",y = "interceptions", data_frame = mor_data3, color = "position",markers=True)
  mor_def_line.update_layout(showlegend=False)
  mor_def_fig = go.Figure()
  mor_def_fig.add_trace(go.Scatter(x = mor_data3["players"], y = mor_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  mor_def_fig.add_trace(go.Scatter(x = mor_data3["players"], y = mor_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  mor_def_fig.update_layout(showlegend=False)
  mor_def_fig1 = go.Figure()
  mor_def_fig1.add_trace(go.Bar(x = mor_data3["players"], y = mor_data3["clearances"], name = "clearances"))
  mor_def_fig1.add_trace(go.Bar(x = mor_data3["players"], y = mor_data3["blocks"], name = "blocks"))
  mor_def_fig1.update_layout(showlegend=False)
  mor_def_fig2 = go.Figure()
  mor_def_fig2.add_trace(go.Scatter(x = mor_data3["players"], y = mor_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  mor_def_fig2.add_trace(go.Scatter(x = mor_data3["players"], y = mor_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  mor_def_fig2.update_layout(showlegend=False)






  prt_att_bar = px.bar(x = "players",y = "ratings", data_frame = prt_data1, color = "position")
  prt_att_bar.update_layout(showlegend=False)
  prt_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = prt_data1, color = "position",orientation='h')
  prt_att_h_bar.update_layout(showlegend=False)
  prt_att_line = px.line(x = "players",y = "assist", data_frame = prt_data1, color = "position",markers=True)
  prt_att_line.update_layout(showlegend=False)
  prt_fig = go.Figure()
  prt_fig.add_trace(go.Scatter(x = prt_data1["players"], y = prt_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  prt_fig.add_trace(go.Scatter(x = prt_data1["players"], y = prt_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  prt_fig.update_layout(showlegend=False)
  prt_fig1 = go.Figure()
  prt_fig1.add_trace(go.Bar(x = prt_data1["players"], y = prt_data1["dribbles completed"], name = "dribbles completed"))
  prt_fig1.add_trace(go.Bar(x = prt_data1["players"], y = prt_data1["dribbles attempt"], name = "dribbles attempted"))
  prt_fig1.update_layout(showlegend=False)
  prt_fig2 = go.Figure()
  prt_fig2.add_trace(go.Scatter(x = prt_data1["players"], y = prt_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  prt_fig2.add_trace(go.Scatter(x = prt_data1["players"], y = prt_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  prt_fig1.update_layout(showlegend=False)

  prt_mid_bar = px.bar(x = "players",y = "ratings", data_frame = prt_data2, color = "position")
  prt_mid_bar.update_layout(showlegend=False)
  prt_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = prt_data2, color = "position",orientation='h')
  prt_mid_h_bar.update_layout(showlegend=False)
  prt_mid_line = px.line(x = "players",y = "interceptions", data_frame = prt_data2, color = "position",markers=True)
  prt_mid_line.update_layout(showlegend=False)
  prt_mid_fig = go.Figure()
  prt_mid_fig.add_trace(go.Scatter(x = prt_data2["players"], y = prt_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  prt_mid_fig.add_trace(go.Scatter(x = prt_data2["players"], y = prt_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  prt_mid_fig.update_layout(showlegend=False)
  prt_mid_fig1 = go.Figure()
  prt_mid_fig1.add_trace(go.Bar(x = prt_data2["players"], y = prt_data2["dribbles completed"], name = "dribbles completed"))
  prt_mid_fig1.add_trace(go.Bar(x = prt_data2["players"], y = prt_data2["dribbles attempt"], name = "dribbles attempted"))
  prt_mid_fig1.update_layout(showlegend=False)
  prt_mid_fig2 = go.Figure()
  prt_mid_fig2.add_trace(go.Scatter(x = prt_data2["players"], y = prt_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  prt_mid_fig2.add_trace(go.Scatter(x = prt_data2["players"], y = prt_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  prt_mid_fig2.update_layout(showlegend=False)

  prt_def_bar = px.bar(x = "players",y = "ratings", data_frame = prt_data3, color = "position")
  prt_def_bar.update_layout(showlegend=False)
  prt_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = prt_data3, color = "position",orientation='h')
  prt_def_h_bar.update_layout(showlegend=False)
  prt_def_line = px.line(x = "players",y = "interceptions", data_frame = prt_data3, color = "position",markers=True)
  prt_def_line.update_layout(showlegend=False)
  prt_def_fig = go.Figure()
  prt_def_fig.add_trace(go.Scatter(x = prt_data3["players"], y = prt_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  prt_def_fig.add_trace(go.Scatter(x = prt_data3["players"], y = prt_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  prt_def_fig.update_layout(showlegend=False)
  prt_def_fig1 = go.Figure()
  prt_def_fig1.add_trace(go.Bar(x = prt_data3["players"], y = prt_data3["clearances"], name = "clearances"))
  prt_def_fig1.add_trace(go.Bar(x = prt_data3["players"], y = prt_data3["blocks"], name = "blocks"))
  prt_def_fig1.update_layout(showlegend=False)
  prt_def_fig2 = go.Figure()
  prt_def_fig2.add_trace(go.Scatter(x = prt_data3["players"], y = prt_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  prt_def_fig2.add_trace(go.Scatter(x = prt_data3["players"], y = prt_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  prt_def_fig2.update_layout(showlegend=False)







  sen_att_bar = px.bar(x = "players",y = "ratings", data_frame = sen_data1, color = "position")
  sen_att_bar.update_layout(showlegend=False)
  sen_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = sen_data1, color = "position",orientation='h')
  sen_att_h_bar.update_layout(showlegend=False)
  sen_att_line = px.line(x = "players",y = "assist", data_frame = sen_data1, color = "position",markers=True)
  sen_att_line.update_layout(showlegend=False)
  sen_fig = go.Figure()
  sen_fig.add_trace(go.Scatter(x = sen_data1["players"], y = sen_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  sen_fig.add_trace(go.Scatter(x = sen_data1["players"], y = sen_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  sen_fig.update_layout(showlegend=False)
  sen_fig1 = go.Figure()
  sen_fig1.add_trace(go.Bar(x = sen_data1["players"], y = sen_data1["dribbles completed"], name = "dribbles completed"))
  sen_fig1.add_trace(go.Bar(x = sen_data1["players"], y = sen_data1["dribbles attempt"], name = "dribbles attempted"))
  sen_fig1.update_layout(showlegend=False)
  sen_fig2 = go.Figure()
  sen_fig2.add_trace(go.Scatter(x = sen_data1["players"], y = sen_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  sen_fig2.add_trace(go.Scatter(x = sen_data1["players"], y = sen_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  sen_fig1.update_layout(showlegend=False)

  sen_mid_bar = px.bar(x = "players",y = "ratings", data_frame = sen_data2, color = "position")
  sen_mid_bar.update_layout(showlegend=False)
  sen_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = sen_data2, color = "position",orientation='h')
  sen_mid_h_bar.update_layout(showlegend=False)
  sen_mid_line = px.line(x = "players",y = "interceptions", data_frame = sen_data2, color = "position",markers=True)
  sen_mid_line.update_layout(showlegend=False)
  sen_mid_fig = go.Figure()
  sen_mid_fig.add_trace(go.Scatter(x = sen_data2["players"], y = sen_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  sen_mid_fig.add_trace(go.Scatter(x = sen_data2["players"], y = sen_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  sen_mid_fig.update_layout(showlegend=False)
  sen_mid_fig1 = go.Figure()
  sen_mid_fig1.add_trace(go.Bar(x = sen_data2["players"], y = sen_data2["dribbles completed"], name = "dribbles completed"))
  sen_mid_fig1.add_trace(go.Bar(x = sen_data2["players"], y = sen_data2["dribbles attempt"], name = "dribbles attempted"))
  sen_mid_fig1.update_layout(showlegend=False)
  sen_mid_fig2 = go.Figure()
  sen_mid_fig2.add_trace(go.Scatter(x = sen_data2["players"], y = sen_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  sen_mid_fig2.add_trace(go.Scatter(x = sen_data2["players"], y = sen_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  sen_mid_fig2.update_layout(showlegend=False)

  sen_def_bar = px.bar(x = "players",y = "ratings", data_frame = sen_data3, color = "position")
  sen_def_bar.update_layout(showlegend=False)
  sen_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = sen_data3, color = "position",orientation='h')
  sen_def_h_bar.update_layout(showlegend=False)
  sen_def_line = px.line(x = "players",y = "interceptions", data_frame = sen_data3, color = "position",markers=True)
  sen_def_line.update_layout(showlegend=False)
  sen_def_fig = go.Figure()
  sen_def_fig.add_trace(go.Scatter(x = sen_data3["players"], y = sen_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  sen_def_fig.add_trace(go.Scatter(x = sen_data3["players"], y = sen_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  sen_def_fig.update_layout(showlegend=False)
  sen_def_fig1 = go.Figure()
  sen_def_fig1.add_trace(go.Bar(x = sen_data3["players"], y = sen_data3["clearances"], name = "clearances"))
  sen_def_fig1.add_trace(go.Bar(x = sen_data3["players"], y = sen_data3["blocks"], name = "blocks"))
  sen_def_fig1.update_layout(showlegend=False)
  sen_def_fig2 = go.Figure()
  sen_def_fig2.add_trace(go.Scatter(x = sen_data3["players"], y = sen_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  sen_def_fig2.add_trace(go.Scatter(x = sen_data3["players"], y = sen_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  sen_def_fig2.update_layout(showlegend=False)







  uru_att_bar = px.bar(x = "players",y = "ratings", data_frame = uru_data1, color = "position")
  uru_att_bar.update_layout(showlegend=False)
  uru_att_h_bar = px.bar(y = "players",x = "goals scored", data_frame = uru_data1, color = "position",orientation='h')
  uru_att_h_bar.update_layout(showlegend=False)
  uru_att_line = px.line(x = "players",y = "assist", data_frame = uru_data1, color = "position",markers=True)
  uru_att_line.update_layout(showlegend=False)
  uru_fig = go.Figure()
  uru_fig.add_trace(go.Scatter(x = uru_data1["players"], y = uru_data1["shots on target"], name = "shots on target", fill='tozeroy'))
  uru_fig.add_trace(go.Scatter(x = uru_data1["players"], y = uru_data1["shots attempted"], name = "shots attempted", fill='tozeroy'))
  uru_fig.update_layout(showlegend=False)
  uru_fig1 = go.Figure()
  uru_fig1.add_trace(go.Bar(x = uru_data1["players"], y = uru_data1["dribbles completed"], name = "dribbles completed"))
  uru_fig1.add_trace(go.Bar(x = uru_data1["players"], y = uru_data1["dribbles attempt"], name = "dribbles attempted"))
  uru_fig1.update_layout(showlegend=False)
  uru_fig2 = go.Figure()
  uru_fig2.add_trace(go.Scatter(x = uru_data1["players"], y = uru_data1["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  uru_fig2.add_trace(go.Scatter(x = uru_data1["players"], y = uru_data1["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  uru_fig1.update_layout(showlegend=False)

  uru_mid_bar = px.bar(x = "players",y = "ratings", data_frame = uru_data2, color = "position")
  uru_mid_bar.update_layout(showlegend=False)
  uru_mid_h_bar = px.bar(y = "players",x = "tackles", data_frame = uru_data2, color = "position",orientation='h')
  uru_mid_h_bar.update_layout(showlegend=False)
  uru_mid_line = px.line(x = "players",y = "interceptions", data_frame = uru_data2, color = "position",markers=True)
  uru_mid_line.update_layout(showlegend=False)
  uru_mid_fig = go.Figure()
  uru_mid_fig.add_trace(go.Scatter(x = uru_data2["players"], y = uru_data2['long balls'], name = "long balls attempted", fill='tozeroy'))
  uru_mid_fig.add_trace(go.Scatter(x = uru_data2["players"], y = uru_data2['long balls completed'], name = "long balls completed", fill='tozeroy'))
  uru_mid_fig.update_layout(showlegend=False)
  uru_mid_fig1 = go.Figure()
  uru_mid_fig1.add_trace(go.Bar(x = uru_data2["players"], y = uru_data2["dribbles completed"], name = "dribbles completed"))
  uru_mid_fig1.add_trace(go.Bar(x = uru_data2["players"], y = uru_data2["dribbles attempt"], name = "dribbles attempted"))
  uru_mid_fig1.update_layout(showlegend=False)
  uru_mid_fig2 = go.Figure()
  uru_mid_fig2.add_trace(go.Scatter(x = uru_data2["players"], y = uru_data2["key passes"], name = "key passes",line=dict(color='royalblue', width=4)))
  uru_mid_fig2.add_trace(go.Scatter(x = uru_data2["players"], y = uru_data2["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  uru_mid_fig2.update_layout(showlegend=False)

  uru_def_bar = px.bar(x = "players",y = "ratings", data_frame = uru_data3, color = "position")
  uru_def_bar.update_layout(showlegend=False)
  uru_def_h_bar = px.bar(y = "players",x = "tackles", data_frame = uru_data3, color = "position",orientation='h')
  uru_def_h_bar.update_layout(showlegend=False)
  uru_def_line = px.line(x = "players",y = "interceptions", data_frame = uru_data3, color = "position",markers=True)
  uru_def_line.update_layout(showlegend=False)
  uru_def_fig = go.Figure()
  uru_def_fig.add_trace(go.Scatter(x = uru_data3["players"], y = uru_data3['long balls'], name = "long balls attempted", fill='tozeroy'))
  uru_def_fig.add_trace(go.Scatter(x = uru_data3["players"], y = uru_data3['long balls completed'], name = "long balls completed", fill='tozeroy'))
  uru_def_fig.update_layout(showlegend=False)
  uru_def_fig1 = go.Figure()
  uru_def_fig1.add_trace(go.Bar(x = uru_data3["players"], y = uru_data3["clearances"], name = "clearances"))
  uru_def_fig1.add_trace(go.Bar(x = uru_data3["players"], y = uru_data3["blocks"], name = "blocks"))
  uru_def_fig1.update_layout(showlegend=False)
  uru_def_fig2 = go.Figure()
  uru_def_fig2.add_trace(go.Scatter(x = uru_data3["players"], y = uru_data3["take-ons conceeded"], name = "take-ons conceeded",line=dict(color='royalblue', width=4)))
  uru_def_fig2.add_trace(go.Scatter(x = uru_data3["players"], y = uru_data3["duels won"], name = "duels won",line=dict(color='firebrick', width=4)))
  uru_def_fig2.update_layout(showlegend=False)







  st.markdown("""
        <style>
        /* Style the selectbox label */
        .stSelectbox label {
            color: #FFFFFF !important;
            font-size: 18px !important;
            font-weight: bold !important;
        }
        
        /* Style the selectbox container*/
        div[data-baseweb="select"] > div {
            background-color: #008000 !important;
          
        }
                    
        /* Target the select widget container */
        .stSelectbox div[data-baseweb="select"] {
            background-color: #008000 !important;
            border-radius: 10px !important;
            border: 2px solid #4CAF50 !important;
        }            
        
        /* Style the selected value */
        .stSelectbox div[data-baseweb="select"] div {
            font-weight: bold !important;
            font-size: 16px !important;
        }
        
        /* Style dropdown menu items */
        div[role="listbox"] div {
            background-color: #e8f5e9 !important;
            color: #1B5E20 !important;
            font-size: 14px !important;
        }
        
        /* The actual list item Streamlit renders */
    li[role="option"]:hover {
        background-color: #008000 !important;
        color: white !important;
    }
        

        </style>
    """, unsafe_allow_html=True)

  drop1 = st.selectbox(label="Teams",options=["Spain","Argentina","Belgium","Brazil","Colombia","Croatia","Netherlands","France","Germany","England","Morocco","Portugal","Uruguay","Senegal"])
  if drop1 == "Spain":
    st.markdown("""
<div style="font-size: 64px; color: #d81005; font-weight: bold">
    SPAIN
</div>
""", unsafe_allow_html=True)
    






    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      st.markdown("""
<style>
    /* Style for the dataframe */
    .dataframe td:first-child, .dataframe th:first-child {
        background-color: #FFE4B5 !important;
    }
    .dataframe td:nth-child(2), .dataframe th:nth-child(2) {
        background-color: #E6F3FF !important;
    }
    .dataframe td:nth-child(3), .dataframe th:nth-child(3) {
        background-color: #FFE4B5 !important;
    }
    .dataframe td:nth-child(4), .dataframe th:nth-child(4) {
        background-color: #E6F3FF !important;
    }
</style>
""", unsafe_allow_html=True)

# Display the dataframe
      esp_datax1 = esp_datax.drop(["players.1","position.1"],axis=1)
      st.dataframe(esp_datax1, use_container_width=True, height=1050)
      #esp_datax
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
      
      if drop2 == "Attack":
        with col12:
          st.subheader("ratings")
          esp_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_att_bar,use_container_width=False)
          st.subheader("goals")
          esp_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_att_h_bar,use_container_width=False)
          st.subheader("assists")
          esp_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_att_line,use_container_width=False)
        with col13:
          st.subheader("shots")
          esp_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_fig,use_container_width=False)
          st.subheader("dribbles")
          esp_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_fig1,use_container_width=False)
          st.subheader("key passes and duels")
          esp_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_fig2,use_container_width=False)
  


      if drop2 == "Midfield":
        with col12:
          st.subheader("ratings")
          esp_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_mid_bar,use_container_width=False)
          st.subheader("tackles")
          esp_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_mid_h_bar,use_container_width=False)
          st.subheader("interceptions")
          esp_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_mid_line,use_container_width=False)
    
        with col13:
          st.subheader("long balls")
          esp_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_mid_fig,use_container_width=False)
          st.subheader("dribbles")
          esp_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_mid_fig1,use_container_width=False)
          st.subheader("key passes and duels")
          esp_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_mid_fig2,use_container_width=False)
    
  


      if drop2 == "Defence":
        with col12:
          st.subheader("ratings")
          esp_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_def_bar,use_container_width=False)
          st.subheader("tackles")
          esp_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_def_h_bar,use_container_width=False)
          st.subheader("interceptions")
          esp_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_def_line,use_container_width=False)
        
        with col13:
          st.subheader("long balls")
          esp_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_def_fig,use_container_width=False)
          st.subheader("clears and blocks")
          esp_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_def_fig1,use_container_width=False)
          st.subheader("take-ons conceed and duels")
          esp_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_def_fig2,use_container_width=False)
  

    
  if drop1 == "Argentina":
    st.markdown("""
<div style="font-size: 64px; color: #4d89e2; font-weight: bold">
    ARGENTINA
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      #arg_datax1 = arg_datax.drop(["players.1","position.1"],axis=1)
      st.dataframe(arg_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
      if drop2 == "Attack":
          with col12:
              st.subheader("ratings")
              arg_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_att_bar,use_container_width=False)
              st.subheader("goals")
              arg_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_att_h_bar,use_container_width=False)
              st.subheader("assists")
              arg_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_att_line,use_container_width=False)
          with col13:
              st.subheader("shots")
              arg_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_fig,use_container_width=False)
              st.subheader("dribbles")
              arg_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              arg_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_fig2,use_container_width=False)


      if drop2 == "Midfield":
          with col12:
              st.subheader("ratings")
              arg_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_mid_bar,use_container_width=False)
              st.subheader("tackles")
              arg_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_mid_h_bar,use_container_width=False)
              st.subheader("interceptions")
              arg_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_mid_line,use_container_width=False)

          with col13:
              st.subheader("long balls")
              arg_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_mid_fig,use_container_width=False)
              st.subheader("dribbles")
              arg_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_mid_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              arg_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_mid_fig2,use_container_width=False)


      if drop2 == "Defence":
          with col12:
              st.subheader("ratings")
              arg_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_def_bar,use_container_width=False)
              st.subheader("tackles")
              arg_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_def_h_bar,use_container_width=False)
              st.subheader("interceptions")
              arg_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_def_line,use_container_width=False)
          
          with col13:
              st.subheader("long balls")
              arg_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_def_fig,use_container_width=False)
              st.subheader("clears and blocks")
              arg_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_def_fig1,use_container_width=False)
              st.subheader("take-ons conceed and duels")
              arg_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(arg_def_fig2,use_container_width=False)
    

  if drop1 == "Belgium":
    st.markdown("""
<div style="font-size: 64px; color: #d81005; font-weight: bold">
    BELGIUM
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      st.dataframe(bel_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
      if drop2 == "Attack":
          with col12:
              st.subheader("ratings")
              bel_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_att_bar,use_container_width=False)
              st.subheader("goals")
              bel_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_att_h_bar,use_container_width=False)
              st.subheader("assists")
              bel_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_att_line,use_container_width=False)
          with col13:
              st.subheader("shots")
              bel_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_fig,use_container_width=False)
              st.subheader("dribbles")
              bel_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              bel_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_fig2,use_container_width=False)


      if drop2 == "Midfield":
          with col12:
              st.subheader("ratings")
              bel_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_mid_bar,use_container_width=False)
              st.subheader("tackles")
              bel_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_mid_h_bar,use_container_width=False)
              st.subheader("interceptions")
              bel_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_mid_line,use_container_width=False)

          with col13:
              st.subheader("long balls")
              bel_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_mid_fig,use_container_width=False)
              st.subheader("dribbles")
              bel_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_mid_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              bel_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_mid_fig2,use_container_width=False)


      if drop2 == "Defence":
          with col12:
              st.subheader("ratings")
              bel_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_def_bar,use_container_width=False)
              st.subheader("tackles")
              bel_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_def_h_bar,use_container_width=False)
              st.subheader("interceptions")
              bel_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_def_line,use_container_width=False)
          
          with col13:
              st.subheader("long balls")
              bel_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_def_fig,use_container_width=False)
              st.subheader("clears and blocks")
              bel_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_def_fig1,use_container_width=False)
              st.subheader("take-ons conceed and duels")
              bel_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bel_def_fig2,use_container_width=False)
      

  if drop1 == "Brazil":
    st.markdown("""
<div style="font-size: 64px; color: #f9ff49; font-weight: bold">
    BRAZIL
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      
      st.dataframe(bra_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
      if drop2 == "Attack":
          with col12:
              st.subheader("ratings")
              bra_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_att_bar,use_container_width=False)
              st.subheader("goals")
              bra_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_att_h_bar,use_container_width=False)
              st.subheader("assists")
              bra_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_att_line,use_container_width=False)
          with col13:
              st.subheader("shots")
              bra_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_fig,use_container_width=False)
              st.subheader("dribbles")
              bra_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              bra_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_fig2,use_container_width=False)


      if drop2 == "Midfield":
          with col12:
              st.subheader("ratings")
              bra_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_mid_bar,use_container_width=False)
              st.subheader("tackles")
              bra_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_mid_h_bar,use_container_width=False)
              st.subheader("interceptions")
              bra_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_mid_line,use_container_width=False)

          with col13:
              st.subheader("long balls")
              bra_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_mid_fig,use_container_width=False)
              st.subheader("dribbles")
              bra_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_mid_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              bra_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_mid_fig2,use_container_width=False)


      if drop2 == "Defence":
          with col12:
              st.subheader("ratings")
              bra_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_def_bar,use_container_width=False)
              st.subheader("tackles")
              bra_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_def_h_bar,use_container_width=False)
              st.subheader("interceptions")
              bra_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_def_line,use_container_width=False)
          
          with col13:
              st.subheader("long balls")
              bra_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_def_fig,use_container_width=False)
              st.subheader("clears and blocks")
              bra_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_def_fig1,use_container_width=False)
              st.subheader("take-ons conceed and duels")
              bra_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(bra_def_fig2,use_container_width=False)

  if drop1 == "Colombia":
    st.markdown("""
<div style="font-size: 64px; color: #af37ff; font-weight: bold">
    COLOMBIA
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      
      st.dataframe(col_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
      if drop2 == "Attack":
          with col12:
              st.subheader("ratings")
              uru_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_att_bar,use_container_width=False)
              st.subheader("goals")
              uru_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_att_h_bar,use_container_width=False)
              st.subheader("assists")
              uru_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_att_line,use_container_width=False)
          with col13:
              st.subheader("shots")
              uru_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_fig,use_container_width=False)
              st.subheader("dribbles")
              uru_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              uru_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_fig2,use_container_width=False)


      if drop2 == "Midfield":
          with col12:
              st.subheader("ratings")
              uru_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_mid_bar,use_container_width=False)
              st.subheader("tackles")
              uru_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_mid_h_bar,use_container_width=False)
              st.subheader("interceptions")
              uru_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_mid_line,use_container_width=False)
          
          with col13:
              st.subheader("long balls")
              uru_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_mid_fig,use_container_width=False)
              st.subheader("dribbles")
              uru_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_mid_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              uru_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_mid_fig2,use_container_width=False)


      if drop2 == "Defence":
          with col12:
              st.subheader("ratings")
              uru_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_def_bar,use_container_width=False)
              st.subheader("tackles")
              uru_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_def_h_bar,use_container_width=False)
              st.subheader("interceptions")
              uru_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_def_line,use_container_width=False)
              
          with col13:
              st.subheader("long balls")
              uru_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_def_fig,use_container_width=False)
              st.subheader("clears and blocks")
              uru_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_def_fig1,use_container_width=False)
              st.subheader("take-ons conceed and duels")
              uru_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(uru_def_fig2,use_container_width=False)

  if drop1 == "Croatia":
    st.markdown("""
<div style="font-size: 64px; color: #ffcbcb; font-weight: bold">
    CROATIA
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      
      st.dataframe(cro_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
    if drop2 == "Attack":
        with col12:
            st.subheader("ratings")
            cro_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_att_bar,use_container_width=False)
            st.subheader("goals")
            cro_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_att_h_bar,use_container_width=False)
            st.subheader("assists")
            cro_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_att_line,use_container_width=False)
        with col13:
            st.subheader("shots")
            cro_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_fig,use_container_width=False)
            st.subheader("dribbles")
            cro_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_fig1,use_container_width=False)
            st.subheader("key passes and duels")
            cro_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_fig2,use_container_width=False)


    if drop2 == "Midfield":
        with col12:
            st.subheader("ratings")
            cro_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_mid_bar,use_container_width=False)
            st.subheader("tackles")
            cro_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_mid_h_bar,use_container_width=False)
            st.subheader("interceptions")
            cro_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_mid_line,use_container_width=False)

        with col13:
            st.subheader("long balls")
            cro_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_mid_fig,use_container_width=False)
            st.subheader("dribbles")
            cro_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_mid_fig1,use_container_width=False)
            st.subheader("key passes and duels")
            cro_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_mid_fig2,use_container_width=False)


    if drop2 == "Defence":
        with col12:
            st.subheader("ratings")
            cro_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_def_bar,use_container_width=False)
            st.subheader("tackles")
            cro_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_def_h_bar,use_container_width=False)
            st.subheader("interceptions")
            cro_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_def_line,use_container_width=False)
        
        with col13:
            st.subheader("long balls")
            cro_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_def_fig,use_container_width=False)
            st.subheader("clears and blocks")
            cro_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_def_fig1,use_container_width=False)
            st.subheader("take-ons conceed and duels")
            cro_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(cro_def_fig2,use_container_width=False)


  if drop1 == "Netherlands":
    st.markdown("""
<div style="font-size: 64px; color: #fd7f00; font-weight: bold">
    NETHERLANDS
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      
      st.dataframe(ned_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
      if drop2 == "Attack":
          with col12:
              st.subheader("ratings")
              ned_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_att_bar,use_container_width=False)
              st.subheader("goals")
              ned_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_att_h_bar,use_container_width=False)
              st.subheader("assists")
              ned_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_att_line,use_container_width=False)
          with col13:
              st.subheader("shots")
              ned_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_fig,use_container_width=False)
              st.subheader("dribbles")
              ned_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              ned_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_fig2,use_container_width=False)


      if drop2 == "Midfield":
          with col12:
              st.subheader("ratings")
              ned_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_mid_bar,use_container_width=False)
              st.subheader("tackles")
              ned_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_mid_h_bar,use_container_width=False)
              st.subheader("interceptions")
              ned_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_mid_line,use_container_width=False)

          with col13:
              st.subheader("long balls")
              ned_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_mid_fig,use_container_width=False)
              st.subheader("dribbles")
              ned_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_mid_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              ned_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_mid_fig2,use_container_width=False)


      if drop2 == "Defence":
          with col12:
              st.subheader("ratings")
              ned_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_def_bar,use_container_width=False)
              st.subheader("tackles")
              ned_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_def_h_bar,use_container_width=False)
              st.subheader("interceptions")
              ned_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_def_line,use_container_width=False)
          
          with col13:
              st.subheader("long balls")
              ned_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_def_fig,use_container_width=False)
              st.subheader("clears and blocks")
              ned_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_def_fig1,use_container_width=False)
              st.subheader("take-ons conceed and duels")
              ned_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ned_def_fig2,use_container_width=False)

  if drop1 == "France":
    st.markdown("""
<div style="font-size: 64px; color: #2414ff; font-weight: bold">
    FRANCE
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      
      st.dataframe(fra_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
      if drop2 == "Attack":
          with col12:
              st.subheader("ratings")
              fra_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_att_bar,use_container_width=False)
              st.subheader("goals")
              fra_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_att_h_bar,use_container_width=False)
              st.subheader("assists")
              fra_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_att_line,use_container_width=False)
          with col13:
              st.subheader("shots")
              fra_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_fig,use_container_width=False)
              st.subheader("dribbles")
              fra_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              fra_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_fig2,use_container_width=False)


      if drop2 == "Midfield":
          with col12:
              st.subheader("ratings")
              fra_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_mid_bar,use_container_width=False)
              st.subheader("tackles")
              fra_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_mid_h_bar,use_container_width=False)
              st.subheader("interceptions")
              fra_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_mid_line,use_container_width=False)

          with col13:
              st.subheader("long balls")
              fra_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_mid_fig,use_container_width=False)
              st.subheader("dribbles")
              fra_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_mid_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              fra_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_mid_fig2,use_container_width=False)


      if drop2 == "Defence":
          with col12:
              st.subheader("ratings")
              fra_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_def_bar,use_container_width=False)
              st.subheader("tackles")
              fra_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_def_h_bar,use_container_width=False)
              st.subheader("interceptions")
              fra_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_def_line,use_container_width=False)
          
          with col13:
              st.subheader("long balls")
              fra_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_def_fig,use_container_width=False)
              st.subheader("clears and blocks")
              fra_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_def_fig1,use_container_width=False)
              st.subheader("take-ons conceed and duels")
              fra_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(fra_def_fig2,use_container_width=False)

  if drop1 == "Germany":
    st.markdown("""
<div style="font-size: 64px; color: #ffffff; font-weight: bold">
    GERMANY
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      
      st.dataframe(ger_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
      
      if drop2 == "Attack":
          with col12:
              st.subheader("ratings")
              ger_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_att_bar,use_container_width=False)
              st.subheader("goals")
              ger_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_att_h_bar,use_container_width=False)
              st.subheader("assists")
              ger_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_att_line,use_container_width=False)
          with col13:
              st.subheader("shots")
              ger_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_fig,use_container_width=False)
              st.subheader("dribbles")
              ger_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              ger_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_fig2,use_container_width=False)


      if drop2 == "Midfield":
          with col12:
              st.subheader("ratings")
              ger_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_mid_bar,use_container_width=False)
              st.subheader("tackles")
              ger_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_mid_h_bar,use_container_width=False)
              st.subheader("interceptions")
              ger_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_mid_line,use_container_width=False)

          with col13:
              st.subheader("long balls")
              ger_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_mid_fig,use_container_width=False)
              st.subheader("dribbles")
              ger_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_mid_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              ger_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_mid_fig2,use_container_width=False)


      if drop2 == "Defence":
          with col12:
              st.subheader("ratings")
              ger_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_def_bar,use_container_width=False)
              st.subheader("tackles")
              ger_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_def_h_bar,use_container_width=False)
              st.subheader("interceptions")
              ger_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_def_line,use_container_width=False)
          
          with col13:
              st.subheader("long balls")
              ger_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_def_fig,use_container_width=False)
              st.subheader("clears and blocks")
              ger_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_def_fig1,use_container_width=False)
              st.subheader("take-ons conceed and duels")
              ger_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(ger_def_fig2,use_container_width=False)

  if drop1 == "England":
    st.markdown("""
<div style="font-size: 64px; color: #ffffff; font-weight: bold">
    ENGLAND
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      
      st.dataframe(eng_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
    
      if drop2 == "Attack":
          with col12:
              st.subheader("ratings")
              eng_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_att_bar,use_container_width=False)
              st.subheader("goals")
              eng_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_att_h_bar,use_container_width=False)
              st.subheader("assists")
              eng_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_att_line,use_container_width=False)
          with col13:
              st.subheader("shots")
              eng_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_fig,use_container_width=False)
              st.subheader("dribbles")
              eng_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              eng_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_fig2,use_container_width=False)


      if drop2 == "Midfield":
          with col12:
              st.subheader("ratings")
              eng_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_mid_bar,use_container_width=False)
              st.subheader("tackles")
              eng_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_mid_h_bar,use_container_width=False)
              st.subheader("interceptions")
              eng_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_mid_line,use_container_width=False)

          with col13:
              st.subheader("long balls")
              eng_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_mid_fig,use_container_width=False)
              st.subheader("dribbles")
              eng_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_mid_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              eng_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_mid_fig2,use_container_width=False)


      if drop2 == "Defence":
          with col12:
              st.subheader("ratings")
              eng_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_def_bar,use_container_width=False)
              st.subheader("tackles")
              eng_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_def_h_bar,use_container_width=False)
              st.subheader("interceptions")
              eng_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_def_line,use_container_width=False)
          
          with col13:
              st.subheader("long balls")
              eng_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_def_fig,use_container_width=False)
              st.subheader("clears and blocks")
              eng_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_def_fig1,use_container_width=False)
              st.subheader("take-ons conceed and duels")
              eng_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(eng_def_fig2,use_container_width=False)

  if drop1 == "Morocco":
    st.markdown("""
<div style="font-size: 64px; color: #d81005; font-weight: bold">
    MOROCCO
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      
      st.dataframe(mor_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
      
      if drop2 == "Attack":
          with col12:
              st.subheader("ratings")
              mor_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_att_bar,use_container_width=False)
              st.subheader("goals")
              mor_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_att_h_bar,use_container_width=False)
              st.subheader("assists")
              mor_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_att_line,use_container_width=False)
          with col13:
              st.subheader("shots")
              mor_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_fig,use_container_width=False)
              st.subheader("dribbles")
              mor_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              mor_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_fig2,use_container_width=False)

      if drop2 == "Midfield":
          with col12:
              st.subheader("ratings")
              mor_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_mid_bar,use_container_width=False)
              st.subheader("tackles")
              mor_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_mid_h_bar,use_container_width=False)
              st.subheader("interceptions")
              mor_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_mid_line,use_container_width=False)

          with col13:
              st.subheader("long balls")
              mor_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_mid_fig,use_container_width=False)
              st.subheader("dribbles")
              mor_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_mid_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              mor_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_mid_fig2,use_container_width=False)

      if drop2 == "Defence":
          with col12:
              st.subheader("ratings")
              mor_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_def_bar,use_container_width=False)
              st.subheader("tackles")
              mor_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_def_h_bar,use_container_width=False)
              st.subheader("interceptions")
              mor_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_def_line,use_container_width=False)
          
          with col13:
              st.subheader("long balls")
              mor_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_def_fig,use_container_width=False)
              st.subheader("clears and blocks")
              mor_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_def_fig1,use_container_width=False)
              st.subheader("take-ons conceed and duels")
              mor_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(mor_def_fig2,use_container_width=False)

  if drop1 == "Portugal":
    st.markdown("""
<div style="font-size: 64px; color: #a70000; font-weight: bold">
    PORTUGAL
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      
      st.dataframe(prt_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
      
      if drop2 == "Attack":
          with col12:
              st.subheader("ratings")
              prt_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_att_bar,use_container_width=False)
              st.subheader("goals")
              prt_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_att_h_bar,use_container_width=False)
              st.subheader("assists")
              prt_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_att_line,use_container_width=False)
          with col13:
              st.subheader("shots")
              prt_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_fig,use_container_width=False)
              st.subheader("dribbles")
              prt_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              prt_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_fig2,use_container_width=False)


      if drop2 == "Midfield":
          with col12:
              st.subheader("ratings")
              prt_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_mid_bar,use_container_width=False)
              st.subheader("tackles")
              prt_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_mid_h_bar,use_container_width=False)
              st.subheader("interceptions")
              prt_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_mid_line,use_container_width=False)

          with col13:
              st.subheader("long balls")
              prt_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_mid_fig,use_container_width=False)
              st.subheader("dribbles")
              prt_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_mid_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              prt_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_mid_fig2,use_container_width=False)


      if drop2 == "Defence":
          with col12:
              st.subheader("ratings")
              prt_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_def_bar,use_container_width=False)
              st.subheader("tackles")
              prt_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_def_h_bar,use_container_width=False)
              st.subheader("interceptions")
              prt_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_def_line,use_container_width=False)
          
          with col13:
              st.subheader("long balls")
              prt_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_def_fig,use_container_width=False)
              st.subheader("clears and blocks")
              prt_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_def_fig1,use_container_width=False)
              st.subheader("take-ons conceed and duels")
              prt_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(prt_def_fig2,use_container_width=False)


  if drop1 == "Senegal":
    st.markdown("""
<div style="font-size: 64px; color: #00ce78; font-weight: bold">
    SENEGAL
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      
      st.dataframe(sen_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)
      if drop2 == "Attack":
          with col12:
              st.subheader("ratings")
              sen_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_att_bar,use_container_width=False)
              st.subheader("goals")
              sen_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_att_h_bar,use_container_width=False)
              st.subheader("assists")
              sen_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_att_line,use_container_width=False)
          with col13:
              st.subheader("shots")
              sen_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_fig,use_container_width=False)
              st.subheader("dribbles")
              sen_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              sen_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_fig2,use_container_width=False)


      if drop2 == "Midfield":
          with col12:
              st.subheader("ratings")
              sen_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_mid_bar,use_container_width=False)
              st.subheader("tackles")
              sen_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_mid_h_bar,use_container_width=False)
              st.subheader("interceptions")
              sen_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_mid_line,use_container_width=False)

          with col13:
              st.subheader("long balls")
              sen_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_mid_fig,use_container_width=False)
              st.subheader("dribbles")
              sen_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_mid_fig1,use_container_width=False)
              st.subheader("key passes and duels")
              sen_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_mid_fig2,use_container_width=False)


      if drop2 == "Defence":
          with col12:
              st.subheader("ratings")
              sen_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_def_bar,use_container_width=False)
              st.subheader("tackles")
              sen_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_def_h_bar,use_container_width=False)
              st.subheader("interceptions")
              sen_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_def_line,use_container_width=False)
          
          with col13:
              st.subheader("long balls")
              sen_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_def_fig,use_container_width=False)
              st.subheader("clears and blocks")
              sen_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_def_fig1,use_container_width=False)
              st.subheader("take-ons conceed and duels")
              sen_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
              st.plotly_chart(sen_def_fig2,use_container_width=False)

  if drop1 == "Uruguay":
    st.markdown("""
<div style="font-size: 64px; color: #0599d8; font-weight: bold">
    URUGUAY
</div>
""", unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
      st.subheader("Average Squad")
      st.write("    ")
      
      st.dataframe(uru_datax, use_container_width=True, height=1050)
    with col11:
      st.subheader("Average stats per match")
      st.write("    ")
      drop2 = st.selectbox(label="Trait",options=["Attack","Midfield","Defence"])
      col12,col13 = st.columns(2)

      if drop2 == "Attack":
          with col12:
            st.subheader("ratings")
            uru_att_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(uru_att_bar,use_container_width=False)
            st.subheader("goals")
            uru_att_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(uru_att_h_bar,use_container_width=False)
            st.subheader("assists")
            uru_att_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(uru_att_line,use_container_width=False)
          with col13:
            st.subheader("shots")
            uru_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(uru_fig,use_container_width=False)
            st.subheader("dribbles")
            uru_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(uru_fig1,use_container_width=False)
            st.subheader("key passes and duels")
            uru_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(uru_fig2,use_container_width=False)
  


      if drop2 == "Midfield":
        with col12:
          st.subheader("ratings")
          uru_mid_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_mid_bar,use_container_width=False)
          st.subheader("tackles")
          uru_mid_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_mid_h_bar,use_container_width=False)
          st.subheader("interceptions")
          uru_mid_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_mid_line,use_container_width=False)
    
        with col13:
          st.subheader("long balls")
          uru_mid_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_mid_fig,use_container_width=False)
          st.subheader("dribbles")
          uru_mid_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_mid_fig1,use_container_width=False)
          st.subheader("key passes and duels")
          uru_mid_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_mid_fig2,use_container_width=False)
    
  


      if drop2 == "Defence":
        with col12:
          st.subheader("ratings")
          uru_def_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_def_bar,use_container_width=False)
          st.subheader("tackles")
          uru_def_h_bar.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_def_h_bar,use_container_width=False)
          st.subheader("interceptions")
          uru_def_line.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_def_line,use_container_width=False)
        
        with col13:
          st.subheader("long balls")
          uru_def_fig.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_def_fig,use_container_width=False)
          st.subheader("clears and blocks")
          uru_def_fig1.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_def_fig1,use_container_width=False)
          st.subheader("take-ons conceed and duels")
          uru_def_fig2.update_layout(height=250,width=450,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_def_fig2,use_container_width=False)
  

elif selected == "PREDICTIONS":
  
  spain_pred = pd.read_csv("data/spain_prediction_final_data.csv")
  argentina_pred = pd.read_csv("data/argentina_prediction_final_data.csv")
  france_pred = pd.read_csv("data/france_prediction_final_data.csv")
  belgium_pred = pd.read_csv("data/belgium_prediction_final_data.csv")
  brazil_pred = pd.read_csv("data/brazil_prediction_final_data.csv")
  colombia_pred = pd.read_csv("data/colombia_prediction_final_data.csv")
  croatia_pred = pd.read_csv("data/croatia_prediction_final_data.csv")
  netherlands_pred = pd.read_csv("data/netherlands_prediction_final_data.csv")
  germany_pred = pd.read_csv("data/germany_prediction_final_data.csv")
  england_pred = pd.read_csv("data/england_prediction_final_data.csv")
  morocco_pred = pd.read_csv("data/morocco_prediction_final_data.csv")
  portugal_pred = pd.read_csv("data/portugal_prediction_final_data.csv")
  uruguay_pred = pd.read_csv("data/uruguay_prediction_final_data.csv")
  senegal_pred = pd.read_csv("data/senegal_prediction_final_data.csv")
  st.markdown("""
        <style>
        /* Style the selectbox label */
        .stSelectbox label {
            color: #FFFFFF !important;
            font-size: 18px !important;
            font-weight: bold !important;
        }
        
        /* Style the selectbox container*/
        div[data-baseweb="select"] > div {
            background-color: #008000 !important;
          
        }
                    
        /* Target the select widget container */
        .stSelectbox div[data-baseweb="select"] {
            background-color: #008000 !important;
            border-radius: 10px !important;
            border: 2px solid #4CAF50 !important;
        }            
        
        /* Style the selected value */
        .stSelectbox div[data-baseweb="select"] div {
            font-weight: bold !important;
            font-size: 16px !important;
        }
        
        /* Style dropdown menu items */
        div[role="listbox"] div {
            background-color: #e8f5e9 !important;
            color: #1B5E20 !important;
            font-size: 14px !important;
        }
        
        /* The actual list item Streamlit renders */
    li[role="option"]:hover {
        background-color: #008000 !important;
        color: white !important;
    }
        

        </style>
    """, unsafe_allow_html=True)
  drop2 = st.selectbox(label="Teams",options=["Spain","Argentina","Belgium","Brazil","Colombia","Croatia","Netherlands","France","Germany","England","Morocco","Portugal","Uruguay","Senegal"])
  if drop2 == "Spain":
    st.markdown("""
<div style="font-size: 64px; color: #d81005; font-weight: bold">
    SPAIN
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      spain_pred1 = spain_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(spain_pred1, use_container_width=True, height=500) 
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = spain_pred,color_discrete_sequence=['red'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          esp_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = spain_pred,color_discrete_sequence=['red'])
          st.subheader("Elo difference")
          esp_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          esp_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = spain_pred,color_discrete_sequence=['red'])
          esp_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(esp_f1_line,use_container_width=False)
    
  if drop2 == "Argentina":
    
    st.markdown("""
<div style="font-size: 64px; color: #4d89e2; font-weight: bold">
    ARGENTINA
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      argentina_pred1 = argentina_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(argentina_pred1, use_container_width=True, height=500)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = argentina_pred,color_discrete_sequence=['#4d89e2'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          arg_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = argentina_pred,color_discrete_sequence=['#4d89e2'])
          st.subheader("Elo difference")
          arg_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(arg_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          arg_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = argentina_pred,color_discrete_sequence=['#4d89e2'])
          arg_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(arg_f1_line,use_container_width=False)

  if drop2 == "Belgium":
    
    st.markdown("""
<div style="font-size: 64px; color: #d81005; font-weight: bold">
    BELGIUM
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      belgium_pred1 = belgium_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(belgium_pred, use_container_width=True, height=500)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = belgium_pred,color_discrete_sequence=['#d81005'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          bel_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = belgium_pred,color_discrete_sequence=['#d81005'])
          st.subheader("Elo difference")
          bel_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(bel_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          bel_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = belgium_pred,color_discrete_sequence=['#d81005'])
          bel_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(bel_f1_line,use_container_width=False)

  if drop2 == "Brazil":
    
    st.markdown("""
<div style="font-size: 64px; color: #f9ff49; font-weight: bold">
    BRAZIL
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      brazil_pred1 = brazil_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(brazil_pred, use_container_width=True, height=500)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = belgium_pred,color_discrete_sequence=['#f9ff49'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          bra_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = belgium_pred,color_discrete_sequence=['#f9ff49'])
          st.subheader("Elo difference")
          bra_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(bra_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          bra_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = belgium_pred,color_discrete_sequence=['#f9ff49'])
          bra_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(bra_f1_line,use_container_width=False)

  if drop2 == "Colombia":
    
    st.markdown("""
<div style="font-size: 64px; color: #af37ff; font-weight: bold">
    COLOMBIA
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      colombia_pred1 = colombia_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(colombia_pred, use_container_width=True, height=500)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = colombia_pred,color_discrete_sequence=['#af37ff'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          col_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = colombia_pred,color_discrete_sequence=['#af37ff'])
          st.subheader("Elo difference")
          col_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(col_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          col_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = colombia_pred,color_discrete_sequence=['#af37ff'])
          col_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(col_f1_line,use_container_width=False)

  if drop2 == "Croatia":
    st.markdown("""
<div style="font-size: 64px; color: #ffcbcb; font-weight: bold">
    CROATIA
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      croatia_pred1 = croatia_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(croatia_pred, use_container_width=True, height=500)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = croatia_pred,color_discrete_sequence=['#ffcbcb'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          cro_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = croatia_pred,color_discrete_sequence=['#ffcbcb'])
          st.subheader("Elo difference")
          cro_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(cro_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          cro_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = croatia_pred,color_discrete_sequence=['#ffcbcb'])
          cro_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(cro_f1_line,use_container_width=False)


  if drop2 == "Netherlands":
    st.markdown("""
<div style="font-size: 64px; color: #fd7f00; font-weight: bold">
    NETHERLANDS
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      netherlands_pred1 = netherlands_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(netherlands_pred, use_container_width=True, height=500)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = netherlands_pred,color_discrete_sequence=['#fd7f00'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          ned_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = netherlands_pred,color_discrete_sequence=['#fd7f00'])
          st.subheader("Elo difference")
          ned_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(ned_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          ned_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = netherlands_pred,color_discrete_sequence=['#fd7f00'])
          ned_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(ned_f1_line,use_container_width=False) 


  if drop2 == "France":
    
    st.markdown("""
<div style="font-size: 64px; color: #2414ff; font-weight: bold">
    FRANCE
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      france_pred1 = france_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(france_pred, use_container_width=True, height=500)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = france_pred,color_discrete_sequence=['#2414ff'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          fra_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = france_pred,color_discrete_sequence=['#2414ff'])
          st.subheader("Elo difference")
          fra_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(fra_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          fra_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = france_pred,color_discrete_sequence=['#2414ff'])
          fra_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(fra_f1_line,use_container_width=False)

  if drop2 == "Germany":
    
    st.markdown("""
<div style="font-size: 64px; color: #ffffff; font-weight: bold">
    GERMANY
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      germany_pred1 = germany_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(germany_pred, use_container_width=True, height=500)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = germany_pred,color_discrete_sequence=['#ffffff'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False) 
      col30,col31 = st.columns(2)
      with col30:
          ger_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = germany_pred,color_discrete_sequence=['#ffffff'])
          st.subheader("Elo difference")
          ger_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(ger_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          ger_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = germany_pred,color_discrete_sequence=['#ffffff'])
          ger_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(ger_f1_line,use_container_width=False)

  if drop2 == "England":
    
    st.markdown("""
<div style="font-size: 64px; color: #ffffff; font-weight: bold">
    ENGLAND
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      england_pred1 = england_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(england_pred, use_container_width=True, height=600)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = england_pred,color_discrete_sequence=['#f0f0f0'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          eng_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = england_pred,color_discrete_sequence=['#f0f0f0'])
          st.subheader("Elo difference")
          eng_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(eng_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          eng_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = england_pred,color_discrete_sequence=['#f0f0f0'])
          eng_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(eng_f1_line,use_container_width=False)

  if drop2 == "Morocco":
    
    st.markdown("""
<div style="font-size: 64px; color: #d81005; font-weight: bold">
    MOROCCO
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      morocco_pred1 = morocco_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(morocco_pred, use_container_width=True, height=500)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = morocco_pred,color_discrete_sequence=['#d81005'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          mor_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = morocco_pred,color_discrete_sequence=['#d81005'])
          st.subheader("Elo difference")
          mor_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(mor_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          mor_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = morocco_pred,color_discrete_sequence=['#d81005'])
          mor_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(mor_f1_line,use_container_width=False)
    

  if drop2 == "Portugal":

    st.markdown("""
<div style="font-size: 64px; color: #a70000; font-weight: bold">
    PORTUGAL
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      portugal_pred1 = portugal_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(portugal_pred, use_container_width=True, height=500)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = portugal_pred,color_discrete_sequence=['#a70000'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          prt_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = portugal_pred,color_discrete_sequence=['#a70000'])
          st.subheader("Elo difference")
          prt_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(prt_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          prt_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = portugal_pred,color_discrete_sequence=['#a70000'])
          prt_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(prt_f1_line,use_container_width=False)


  if drop2 == "Senegal":

    st.markdown("""
<div style="font-size: 64px; color: #00ce78; font-weight: bold">
    SENEGAL
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      senegal_pred1 = senegal_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(senegal_pred, use_container_width=True, height=500)
    with col20:
      st.subheader("Winning probalities in %")

      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = senegal_pred,color_discrete_sequence=['#00ce78'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          sen_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = senegal_pred,color_discrete_sequence=['#00ce78'])
          st.subheader("Elo difference")
          sen_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(sen_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          sen_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = senegal_pred,color_discrete_sequence=['#00ce78'])
          sen_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(sen_f1_line,use_container_width=False)

  if drop2 == "Uruguay":
    st.markdown("""
<div style="font-size: 64px; color: #0599d8; font-weight: bold">
    URUGUAY
</div>
""", unsafe_allow_html=True)
    col19,col20 = st.columns(2)
    with col19:
      st.subheader("H2H data")
      uruguay_pred1 = uruguay_pred.drop(["Result","Predicted_Result","Second Result"],axis=1)
      st.dataframe(uruguay_pred, use_container_width=True, height=600)
    with col20:
      st.subheader("Winning probalities in %")
      f1 = px.area(x = "Countries",y = "Win Probability in %",data_frame = uruguay_pred,color_discrete_sequence=['#0599d8'])
      f1.update_layout(height=250,margin=dict(t=20, b=0, l=0, r=0))
      st.plotly_chart(f1,use_container_width=False)
      col30,col31 = st.columns(2)
      with col30:
          uru_f1_bar = px.bar(x = "Countries",y = "Elo_diff",data_frame = uruguay_pred,color_discrete_sequence=['#0599d8'])
          st.subheader("Elo difference")
          uru_f1_bar.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_f1_bar,use_container_width=False)
      with col31:
          st.subheader("Composite Score")
          uru_f1_line = px.line(x = "Countries",y = "Composite_Score",data_frame = uruguay_pred,color_discrete_sequence=['#0599d8'])
          uru_f1_line.update_layout(height=250,width=600,margin=dict(t=20, b=0, l=0, r=0))
          st.plotly_chart(uru_f1_line,use_container_width=False)
