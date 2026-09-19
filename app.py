import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Mind at Work | Mental Health in Tech",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# COLOR SYSTEM
# ============================================================
BG = "#0a0e17"
CARD = "#141a28"
BORDER = "#2d3444"
GOLD = "#d4a656"
BLUE = "#4C7FDB"
RED = "#e0575f"
GREEN = "#4fce89"
TEAL = "#4fd1c5"
PURPLE = "#9d7fd6"
TEXT = "#eef1f6"
MUTED = "#8b93a7"
DIVERGING = [RED, GOLD, GREEN]

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(f"""
<style>
.stApp {{ background-color: {BG}; color: {TEXT}; }}

.metric-card {{
    background-color: {CARD}; border: 1px solid {BORDER}; border-top: 3px solid {GOLD};
    border-radius: 10px; padding: 18px; text-align: center;
}}
.metric-label {{ color: {GOLD}; font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }}
.metric-value {{ color: #ffffff; font-size: 30px; font-weight: 800; margin-top: 4px; }}

.banner {{
    background: linear-gradient(135deg, #131a2b 0%, #1f2c47 100%);
    padding: 26px 32px; border-radius: 12px; margin-bottom: 18px;
    display: flex; align-items: center; gap: 20px;
}}

.finding-card {{
    background-color: {CARD}; border: 1px solid {BORDER}; border-left: 4px solid {GOLD};
    border-radius: 8px; padding: 14px 16px; margin-bottom: 10px; min-height: 92px;
}}
.finding-title {{ color: {GOLD}; font-weight: 700; font-size: 13.5px; }}
.finding-body {{ color: #c3c9d6; font-size: 13px; margin-top: 4px; line-height: 1.4; }}

.rec-card {{
    background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 10px;
    padding: 16px 18px; margin-bottom: 14px; display: flex; gap: 14px;
    align-items: flex-start; min-height: 150px;
}}
.rec-num {{
    background: {GOLD}; color: {BG}; font-weight: 800; font-size: 14px;
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}}
.rec-num-warn {{ background: {RED}; color: #fff; }}
.rec-title {{ color: #fff; font-weight: 700; font-size: 14.5px; margin-bottom: 4px; }}
.rec-body {{ color: #c3c9d6; font-size: 13px; line-height: 1.45; }}

.fun-card {{
    background: linear-gradient(135deg, #1a2740 0%, #24253a 100%);
    border: 1px solid {PURPLE}; border-radius: 10px; padding: 18px 22px;
}}

.filter-label {{
    color: {GOLD}; font-size: 12px; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; margin-bottom: 6px; margin-top: 4px;
}}

.stMultiSelect span[data-baseweb="tag"],
.stMultiSelect div[data-baseweb="tag"],
span[data-baseweb="tag"],
div[data-baseweb="tag"] {{
    background-color: rgba(212,166,86,0.18) !important;
    border: 1px solid {GOLD} !important;
    color: {GOLD} !important;
}}
.stMultiSelect span[data-baseweb="tag"] span,
.stMultiSelect div[data-baseweb="tag"] span,
span[data-baseweb="tag"] span,
div[data-baseweb="tag"] span {{ color: {GOLD} !important; }}
.stMultiSelect span[data-baseweb="tag"] svg,
.stMultiSelect div[data-baseweb="tag"] svg,
span[data-baseweb="tag"] svg,
div[data-baseweb="tag"] svg {{ fill: {GOLD} !important; }}

.stTabs [data-baseweb="tab-list"] {{
    gap: 4px; background-color: {CARD}; padding: 6px; border-radius: 10px;
    border: 1px solid {BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    background-color: transparent; border-radius: 8px; padding: 10px 18px;
    color: {MUTED}; font-weight: 600; font-size: 14.5px;
}}
.stTabs [aria-selected="true"] {{
    background-color: {GOLD} !important; color: {BG} !important;
}}
.stTabs [data-baseweb="tab-highlight"] {{ display: none; }}
.stTabs [data-baseweb="tab-border"] {{ display: none; }}
</style>
""", unsafe_allow_html=True)

def style_fig(fig, height=380, title=""):
    fig.update_layout(
        plot_bgcolor=CARD, paper_bgcolor=CARD, font_color=TEXT,
        title=dict(text=title, font=dict(color=GOLD, size=15)),
        height=height, margin=dict(l=10, r=10, t=50, b=10)
    )
    return fig

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/Vipsa2207/Mental-Health-In-Tech/refs/heads/main/survey.csv')

    def clean_gender(g):
        g = str(g).strip().lower()
        male_set = {'male', 'm', 'mail', 'maile', 'make', 'mal', 'male (cis)',
                    'male-ish', 'malr', 'man', 'msle', 'cis male', 'cis man',
                    'male leaning androgynous',
                    'ostensibly male, unsure what that really means',
                    'something kinda male?', 'guy (-ish) ^_^'}
        female_set = {'female', 'f', 'femail', 'femake', 'female (cis)',
                      'female (trans)', 'cis female', 'cis-female/femme',
                      'woman', 'trans woman', 'trans-female'}
        if g in male_set:
            return 'Male'
        elif g in female_set:
            return 'Female'
        else:
            return 'Other'

    df['Gender_clean'] = df['Gender'].apply(clean_gender)
    df = df[(df['Age'] >= 18) & (df['Age'] <= 75)].reset_index(drop=True)
    df['self_employed'] = df['self_employed'].fillna('No')
    df['work_interfere'] = df['work_interfere'].fillna('Not applicable')
    df['Age_group'] = pd.cut(df['Age'], bins=[17, 24, 34, 44, 54, 75],
                              labels=['18-24', '25-34', '35-44', '45-54', '55+'])
    return df

df = load_data()


@st.cache_data
def load_2016_data():
    df16 = pd.read_csv('https://raw.githubusercontent.com/Vipsa2207/Mental-Health-In-Tech/refs/heads/main/mental-heath-in-tech-2016_20161114.csv')

    col_map = {
        'Have you ever sought treatment for a mental health issue from a mental health professional?': 'treatment',
        'How many employees does your company or organization have?': 'no_employees',
        'Does your employer provide mental health benefits as part of healthcare coverage?': 'benefits',
        'Do you know the options for mental health care available under your employer-provided coverage?': 'care_options',
        'Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources provided by your employer?': 'anonymity',
        'If a mental health issue prompted you to request a medical leave from work, asking for that leave would be:': 'leave'
    }
    df16 = df16.rename(columns=col_map)
    df16 = df16[list(col_map.values())].copy()

    df16['treatment'] = df16['treatment'].map({1: 'Yes', 0: 'No'})
    df16['benefits'] = df16['benefits'].replace({"I don't know": "Don't know"})
    df16['care_options'] = df16['care_options'].replace({'I am not sure': 'Not sure'})
    df16['anonymity'] = df16['anonymity'].replace({"I don't know": "Don't know"})

    df16_benefits = df16[df16['benefits'] != 'Not eligible for coverage / N/A']

    return df16, df16_benefits

df16, df16_benefits = load_2016_data()

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("🧠 Mind at Work")

with st.sidebar.expander("▸ SEGMENT FILTERS", expanded=True):

    with st.container(border=True):
        st.markdown('<div class="filter-label">🌍 Geography</div>', unsafe_allow_html=True)
        countries = ['All'] + sorted(df['Country'].value_counts().head(15).index.tolist())
        selected_country = st.selectbox("Country", countries, label_visibility="collapsed")

    with st.container(border=True):
        st.markdown('<div class="filter-label">👤 Gender</div>', unsafe_allow_html=True)
        selected_gender = st.multiselect(
            "Gender", options=df['Gender_clean'].unique().tolist(),
            default=df['Gender_clean'].unique().tolist(), label_visibility="collapsed"
        )

    with st.container(border=True):
        st.markdown('<div class="filter-label">🎂 Age Range</div>', unsafe_allow_html=True)
        age_range = st.slider(
            "Age Range", int(df['Age'].min()), int(df['Age'].max()),
            (int(df['Age'].min()), int(df['Age'].max())), label_visibility="collapsed"
        )

    with st.container(border=True):
        st.markdown('<div class="filter-label">💼 Company Size</div>', unsafe_allow_html=True)
        size_options = ['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000']
        selected_sizes = st.multiselect(
            "Company Size", options=size_options, default=size_options, label_visibility="collapsed"
        )

    with st.container(border=True):
        st.markdown('<div class="filter-label">🔎 Quick Toggles</div>', unsafe_allow_html=True)
        family_only = st.checkbox("Family history only")
        self_emp_only = st.checkbox("Self-employed only")
        tech_only = st.checkbox("Tech companies only")

filtered_df = df.copy()
if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]
filtered_df = filtered_df[filtered_df['Gender_clean'].isin(selected_gender)]
filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]
filtered_df = filtered_df[filtered_df['no_employees'].isin(selected_sizes)]
if family_only:
    filtered_df = filtered_df[filtered_df['family_history'] == 'Yes']
if self_emp_only:
    filtered_df = filtered_df[filtered_df['self_employed'] == 'Yes']
if tech_only:
    filtered_df = filtered_df[filtered_df['tech_company'] == 'Yes']

df16_sized = df16[df16['no_employees'].isin(selected_sizes)]
df16_benefits_sized = df16_benefits[df16_benefits['no_employees'].isin(selected_sizes)]

st.sidebar.markdown(f"**Showing {len(filtered_df)} of {len(df)} respondents**")

# ============================================================
# BANNER - single bold title line, no separate subheading
# ============================================================
banner_html = f'<div class="banner"><div style="background:{GOLD}; border-radius:10px; width:64px; height:64px; display:flex; align-items:center; justify-content:center; font-size:36px; flex-shrink:0;">🧠</div><div><h1 style="margin:0; color:#ffffff; font-size:28px; line-height:1.3;">Mind at Work: A Data-Driven Look at Mental Health in the Tech Industry</h1></div></div>'
st.markdown(banner_html, unsafe_allow_html=True)

# ============================================================
# KPI ROW
# ============================================================
treatment_pct = (filtered_df['treatment'] == 'Yes').mean() * 100 if len(filtered_df) else 0
family_pct = (filtered_df['family_history'] == 'Yes').mean() * 100 if len(filtered_df) else 0
remote_pct = (filtered_df['remote_work'] == 'Yes').mean() * 100 if len(filtered_df) else 0
tech_pct = (filtered_df['tech_company'] == 'Yes').mean() * 100 if len(filtered_df) else 0

kpi_cols = st.columns(5)
kpi_data = [
    ("Respondents", f"{len(filtered_df):,}"),
    ("Sought Treatment", f"{treatment_pct:.1f}%"),
    ("Family History", f"{family_pct:.1f}%"),
    ("Works Remotely", f"{remote_pct:.1f}%"),
    ("At Tech Company", f"{tech_pct:.1f}%"),
]
for col, (label, value) in zip(kpi_cols, kpi_data):
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Overview", "📊 EDA Explorer", "🔍 Workplace Factors",
    "📈 2014 vs 2016", "💡 Recommendations", "🎯 Awareness Gap"
])

# ---------------- TAB 1: OVERVIEW ----------------
with tab1:
    left, right = st.columns([1.3, 1])

    with left:
        st.subheader("Project Summary")
        st.markdown("""
            This dashboard explores the 2014 OSMI survey on attitudes toward mental health in the tech workplace.
            After cleaning invalid age entries and standardizing 49 raw spellings of Gender, the analysis looks at
            who seeks treatment and which employer-side factors — benefits, care options, anonymity, leave policy —
            are associated with it.

            **Business Objective:** Identify which workplace factors most strongly affect employee mental health,
            and assess how many people seek treatment and how well employers support it.
        """)

    with right:
        if len(filtered_df):
            donut_df = filtered_df['treatment'].value_counts().reset_index()
            donut_df.columns = ['Treatment', 'Count']
            fig_donut = px.pie(donut_df, names='Treatment', values='Count', hole=0.6,
                                color='Treatment', color_discrete_map={'Yes': GREEN, 'No': RED})
            fig_donut.update_traces(textinfo='percent+label', textfont_size=13)
            fig_donut = style_fig(fig_donut, height=280, title='Treatment Split — Current Segment')
            fig_donut.update_layout(showlegend=False)
            st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("### Key Findings")
    f1, f2 = st.columns(2)
    with f1:
        st.markdown('<div class="finding-card"><div class="finding-title">🧬 Family History Roughly Doubles Treatment-Seeking</div><div class="finding-body">74% of people with a family history of mental illness sought treatment, vs 35% without one — the strongest single predictor in the dataset.</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="finding-card"><div class="finding-title">😨 Fear Shuts Down Disclosure</div><div class="finding-body">Willingness to tell a supervisor drops from 73% to under 10% once someone expects a negative consequence for speaking up.</div></div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="finding-card"><div class="finding-title">❓ Not Knowing Beats a Flat "No"</div><div class="finding-body">Employees unsure whether their employer offers care options seek treatment at a lower rate than employees who know the answer is "no."</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="finding-card"><div class="finding-title">🎂 Early-Career Employees Seek Help Least</div><div class="finding-body">18-24 year olds sought treatment at 45% — the lowest of any age group, rising steadily to ~71% for 55+.</div></div>', unsafe_allow_html=True)

# ---------------- TAB 2: EDA EXPLORER ----------------
with tab2:
    sub1, sub2, sub3 = st.tabs(["👤 Demographics", "🩺 Treatment Patterns", "🏢 Workplace Culture"])

    with sub1:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(filtered_df, x='Age', nbins=30, color_discrete_sequence=[BLUE])
            st.plotly_chart(style_fig(fig, title='Age Distribution'), use_container_width=True)
        with c2:
            gc = filtered_df['Gender_clean'].value_counts().reset_index()
            gc.columns = ['Gender', 'Count']
            fig = px.bar(gc, x='Gender', y='Count', color='Gender',
                         color_discrete_sequence=[BLUE, GOLD, PURPLE])
            fig.update_layout(showlegend=False)
            st.plotly_chart(style_fig(fig, title='Gender Distribution'), use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            tc = filtered_df['Country'].value_counts().head(10).reset_index()
            tc.columns = ['Country', 'Count']
            fig = px.bar(tc, x='Count', y='Country', orientation='h', color_discrete_sequence=[TEAL])
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(style_fig(fig, title='Top 10 Countries by Respondents'), use_container_width=True)
        with c4:
            sc = filtered_df['no_employees'].value_counts().reindex(size_options).dropna().reset_index()
            sc.columns = ['Company Size', 'Count']
            fig = px.bar(sc, x='Company Size', y='Count', color_discrete_sequence=[PURPLE])
            st.plotly_chart(style_fig(fig, title='Company Size Distribution'), use_container_width=True)

    with sub2:
        c1, c2 = st.columns(2)
        with c1:
            ct = pd.crosstab(filtered_df['family_history'], filtered_df['treatment'], normalize='index') * 100
            ct = ct.reset_index().melt(id_vars='family_history', var_name='Treatment', value_name='Percentage')
            fig = px.bar(ct, x='family_history', y='Percentage', color='Treatment', barmode='group',
                         color_discrete_map={'Yes': GREEN, 'No': RED})
            st.plotly_chart(style_fig(fig, title='Treatment Rate by Family History'), use_container_width=True)
        with c2:
            ag = pd.crosstab(filtered_df['Age_group'], filtered_df['treatment'], normalize='index')['Yes'] * 100
            ag = ag.reset_index()
            ag.columns = ['Age Group', 'Treatment Rate']
            fig = px.line(ag, x='Age Group', y='Treatment Rate', markers=True, color_discrete_sequence=[GOLD])
            fig.update_traces(line=dict(width=3), marker=dict(size=10))
            st.plotly_chart(style_fig(fig, title='Treatment Rate by Age Group'), use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            ct2 = pd.crosstab(filtered_df['remote_work'], filtered_df['treatment'], normalize='index')['Yes'] * 100
            ct2 = ct2.reset_index()
            ct2.columns = ['Remote Work', 'Treatment Rate']
            fig = px.bar(ct2, x='Remote Work', y='Treatment Rate', color='Remote Work',
                         color_discrete_sequence=[BLUE, TEAL])
            fig.update_layout(showlegend=False)
            st.plotly_chart(style_fig(fig, title='Treatment Rate: Remote vs On-site'), use_container_width=True)
        with c4:
            wi = filtered_df['work_interfere'].value_counts().reindex(
                ['Never', 'Rarely', 'Sometimes', 'Often', 'Not applicable']).dropna().reset_index()
            wi.columns = ['Work Interference', 'Count']
            fig = px.bar(wi, x='Work Interference', y='Count', color_discrete_sequence=[RED])
            st.plotly_chart(style_fig(fig, title='How Often Condition Interferes With Work'), use_container_width=True)

    with sub3:
        c1, c2 = st.columns(2)
        with c1:
            cow = filtered_df['coworkers'].value_counts().reindex(['No', 'Some of them', 'Yes']).reset_index()
            cow.columns = ['Response', 'Count']
            sup = filtered_df['supervisor'].value_counts().reindex(['No', 'Some of them', 'Yes']).reset_index()
            sup.columns = ['Response', 'Count']
            cow['Who'] = 'Coworkers'
            sup['Who'] = 'Supervisor'
            combined = pd.concat([cow, sup])
            fig = px.bar(combined, x='Response', y='Count', color='Who', barmode='group',
                         color_discrete_sequence=[BLUE, GOLD])
            st.plotly_chart(style_fig(fig, title='Willingness to Discuss: Coworkers vs Supervisor'), use_container_width=True)
        with c2:
            mhc = pd.crosstab(filtered_df['mental_health_consequence'], filtered_df['supervisor'], normalize='index') * 100
            mhc = mhc.reindex(['No', 'Maybe', 'Yes'])
            mhc = mhc[[c for c in ['No', 'Some of them', 'Yes'] if c in mhc.columns]].reset_index()
            mhc = mhc.melt(id_vars='mental_health_consequence', var_name='Willing to tell supervisor', value_name='Percent')
            fig = px.bar(mhc, x='mental_health_consequence', y='Percent', color='Willing to tell supervisor',
                         barmode='stack', color_discrete_sequence=[RED, GOLD, GREEN])
            st.plotly_chart(style_fig(fig, title='Fear of Consequences vs Supervisor Disclosure'), use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            lv = filtered_df['leave'].value_counts().reindex(
                ['Very easy', 'Somewhat easy', "Don't know", 'Somewhat difficult', 'Very difficult']
            ).dropna().reset_index()
            lv.columns = ['Leave Difficulty', 'Count']
            fig = px.bar(lv, x='Leave Difficulty', y='Count', color_discrete_sequence=[PURPLE])
            st.plotly_chart(style_fig(fig, title='Ease of Taking Medical Leave'), use_container_width=True)
        with c4:
            an = filtered_df['anonymity'].value_counts().reindex(["Don't know", 'No', 'Yes']).reset_index()
            an.columns = ['Anonymity Protected', 'Count']
            fig = px.pie(an, names='Anonymity Protected', values='Count', hole=0.5,
                         color='Anonymity Protected',
                         color_discrete_map={'Yes': GREEN, 'No': RED, "Don't know": GOLD})
            fig.update_traces(textinfo='percent+label')
            st.plotly_chart(style_fig(fig, title='Anonymity Protection Awareness'), use_container_width=True)

# ---------------- TAB 3: WORKPLACE FACTORS ----------------
with tab3:
    st.subheader("Workplace Policy vs. Treatment-Seeking")

    factor_options = {
        'Employer provides mental-health benefits': 'benefits',
        'Aware of care options': 'care_options',
        'Anonymity protected': 'anonymity',
        'Ease of taking mental-health leave': 'leave',
        'Wellness program discussed': 'wellness_program',
        'Employer provides seek-help resources': 'seek_help'
    }

    st.markdown("**All factors at a glance** *(share of respondents answering positively)*")
    summary_rows = []
    for label, col in factor_options.items():
        if col == 'leave':
            pct = filtered_df[col].isin(['Very easy', 'Somewhat easy']).mean() * 100 if len(filtered_df) else 0
        else:
            pct = (filtered_df[col] == 'Yes').mean() * 100 if len(filtered_df) else 0
        summary_rows.append({'Factor': label, 'Positive %': pct})
    summary_df = pd.DataFrame(summary_rows).sort_values('Positive %')

    fig_summary = px.bar(summary_df, x='Positive %', y='Factor', orientation='h',
                          color='Positive %', color_continuous_scale=DIVERGING, text_auto='.1f')
    fig_summary.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_fig(fig_summary, height=340, title='All Workplace Factors — Current Segment'), use_container_width=True)

    st.markdown("---")
    st.markdown("**Drill into one factor**")
    selected_factor_label = st.selectbox("Choose a workplace factor:", list(factor_options.keys()))
    selected_factor = factor_options[selected_factor_label]

    order_maps = {
        'benefits': ["Don't know", 'No', 'Yes'],
        'care_options': ['No', 'Not sure', 'Yes'],
        'anonymity': ["Don't know", 'No', 'Yes'],
        'leave': ['Very easy', 'Somewhat easy', "Don't know", 'Somewhat difficult', 'Very difficult'],
        'wellness_program': ["Don't know", 'No', 'Yes'],
        'seek_help': ["Don't know", 'No', 'Yes']
    }

    ct = pd.crosstab(filtered_df[selected_factor], filtered_df['treatment'], normalize='index')['Yes'] * 100
    ct = ct.reindex(order_maps[selected_factor]).dropna().reset_index()
    ct.columns = [selected_factor, 'Treatment Rate']

    fig_factor = px.bar(ct, x=selected_factor, y='Treatment Rate', color='Treatment Rate',
                         color_continuous_scale=DIVERGING, text_auto='.1f')
    fig_factor.update_layout(coloraxis_showscale=False, yaxis_title='% Who Sought Treatment')
    st.plotly_chart(style_fig(fig_factor, title=f'Treatment Rate by: {selected_factor_label}'), use_container_width=True)

    st.markdown("---")
    st.markdown("**Correlation Heatmap** — how these factors and outcomes move together")

    encode_yn = {'Yes': 1, 'No': 0, "Don't know": 0.5, 'Not sure': 0.5}
    cs = filtered_df.copy()
    cs['Treatment'] = cs['treatment'].map(encode_yn)
    cs['Family Hist.'] = cs['family_history'].map(encode_yn)
    cs['Benefits'] = cs['benefits'].map(encode_yn)
    cs['Care Options'] = cs['care_options'].map(encode_yn)
    cs['Anonymity'] = cs['anonymity'].map(encode_yn)
    cs['Seek Help'] = cs['seek_help'].map(encode_yn)
    cs['Wellness'] = cs['wellness_program'].map(encode_yn)
    cs['Remote'] = cs['remote_work'].map(encode_yn)
    cs['Tech Co.'] = cs['tech_company'].map(encode_yn)
    cs['Leave Ease'] = cs['leave'].map(
        {'Very easy': 0, 'Somewhat easy': 1, "Don't know": -1, 'Somewhat difficult': 2, 'Very difficult': 3})
    cs['Work Interfere'] = cs['work_interfere'].map(
        {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Not applicable': -1})

    corr_cols = ['Treatment', 'Family Hist.', 'Benefits', 'Care Options', 'Anonymity',
                 'Seek Help', 'Wellness', 'Remote', 'Tech Co.', 'Leave Ease', 'Work Interfere']
    corr_matrix = cs[corr_cols].corr()

    fig_heat = px.imshow(corr_matrix, text_auto='.2f', color_continuous_scale='RdBu_r',
                          zmin=-1, zmax=1, aspect='auto')
    st.plotly_chart(style_fig(fig_heat, height=520, title='Correlation Heatmap — Encoded Variables'), use_container_width=True)

# ---------------- TAB 4: 2014 VS 2016 ----------------
with tab4:
    st.subheader("2014 vs 2016: Has Anything Changed?")
    st.caption("The 2014 side reflects your current sidebar filters. The 2016 survey only shares Company Size "
               "with 2014 (it doesn't have the same Gender/Age/Country columns), so the 2016 side responds to "
               "the Company Size filter only.")

    rate_2014 = (filtered_df['treatment'] == 'Yes').mean() * 100 if len(filtered_df) else 0
    rate_2016 = (df16_sized['treatment'] == 'Yes').mean() * 100 if len(df16_sized) else 0
    delta = rate_2016 - rate_2014

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">2014 Treatment Rate</div><div class="metric-value">{rate_2014:.1f}%</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">2016 Treatment Rate</div><div class="metric-value">{rate_2016:.1f}%</div></div>', unsafe_allow_html=True)
    with c3:
        arrow = "▲" if delta >= 0 else "▼"
        color = GREEN if delta >= 0 else RED
        st.markdown(f'<div class="metric-card"><div class="metric-label">Change</div><div class="metric-value" style="color:{color};">{arrow} {abs(delta):.1f} pts</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    def compare_chart(field, title, order, use_benefits_16=False):
        src16 = df16_benefits_sized if use_benefits_16 else df16_sized
        c14 = filtered_df[field].value_counts(normalize=True).reindex(order) * 100 if len(filtered_df) else pd.Series(0, index=order)
        c16 = src16[field].value_counts(normalize=True).reindex(order) * 100 if len(src16) else pd.Series(0, index=order)
        comp = pd.DataFrame({'2014': c14, '2016': c16}).reset_index()
        comp.columns = ['Response', '2014', '2016']
        comp = comp.melt(id_vars='Response', var_name='Year', value_name='Percent')
        fig = px.bar(comp, x='Response', y='Percent', color='Year', barmode='group',
                     color_discrete_sequence=[BLUE, TEAL])
        fig.update_layout(legend=dict(orientation='h', y=-0.25))
        return style_fig(fig, height=360, title=title)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.plotly_chart(compare_chart('benefits', 'Benefits Awareness', ["Don't know", 'No', 'Yes'], use_benefits_16=True), use_container_width=True)
    with r1c2:
        st.plotly_chart(compare_chart('care_options', 'Care Options Awareness', ['No', 'Not sure', 'Yes']), use_container_width=True)

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.plotly_chart(compare_chart('anonymity', 'Anonymity Protection', ["Don't know", 'No', 'Yes']), use_container_width=True)
    with r2c2:
        c14_size = filtered_df['no_employees'].value_counts(normalize=True).reindex(size_options) * 100 if len(filtered_df) else pd.Series(0, index=size_options)
        c16_size = df16_sized['no_employees'].value_counts(normalize=True).reindex(size_options) * 100 if len(df16_sized) else pd.Series(0, index=size_options)
        comp = pd.DataFrame({'2014': c14_size, '2016': c16_size}).reset_index()
        comp.columns = ['Company Size', '2014', '2016']
        comp = comp.melt(id_vars='Company Size', var_name='Year', value_name='Percent')
        fig = px.bar(comp, x='Company Size', y='Percent', color='Year', barmode='group',
                     color_discrete_sequence=[BLUE, TEAL])
        fig.update_layout(legend=dict(orientation='h', y=-0.25))
        st.plotly_chart(style_fig(fig, height=360, title='Company Size Distribution'), use_container_width=True)

# ---------------- TAB 5: RECOMMENDATIONS ----------------
with tab5:
    st.subheader("Solution to the Business Objective")

    recs = [
        ("1", "gold", "Fix Communication First",
         "Employees who don't know what's available underperform even employees who know the answer is \"no.\" "
         "Auditing and clearly communicating existing benefits, care options, and leave policy is the "
         "lowest-cost, highest-leverage fix in this dataset."),
        ("2", "gold", "Train Supervisors on Disclosure",
         "Willingness to talk to a supervisor collapses from 73% to under 10% once someone expects a "
         "negative consequence. The fear itself — not the formal policy — is what suppresses these conversations."),
        ("3", "gold", "Target Early-Career Outreach",
         "18-24 year olds seek treatment at the lowest rate of any age group (45%). Awareness campaigns "
         "aimed at early-career employees have more room to move the needle than a generic company-wide push."),
        ("4", "warn", "Don't Over-Index on Company Size",
         "Every company-size bucket sits within a tight 44-56% treatment range, with no clean trend. "
         "Restructuring around headcount is not an efficient lever for this objective."),
        ("5", "warn", "Remote Work Isn't the Lever",
         "Remote vs on-site shows only a 3-point gap in treatment-seeking — within normal noise. "
         "Work-location policy won't move this metric on its own."),
        ("6", "warn", "Being a Tech Company Isn't Protective",
         "Tech companies show a 50% treatment rate vs 54% for non-tech — industry alone doesn't predict "
         "better support. The real drivers are cultural and informational, not sector-based."),
    ]

    for i in range(0, len(recs), 2):
        row = st.columns(2)
        for j, col in enumerate(row):
            idx = i + j
            if idx < len(recs):
                num, kind, title, body = recs[idx]
                num_class = "rec-num" if kind == "gold" else "rec-num rec-num-warn"
                with col:
                    st.markdown(f'<div class="rec-card"><div class="{num_class}">{num}</div><div><div class="rec-title">{title}</div><div class="rec-body">{body}</div></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="fun-card"><b>💬 What People Actually Said</b><br><br>The optional comments section — filled in by just 13% of respondents — echoed the same themes as the charts, unprompted. Words like <i>depression</i>, <i>anxiety</i>, and <i>bipolar</i> showed up alongside <i>employer</i>, <i>manager</i>, and <i>benefit</i> — people weren\'t just answering the survey, they were describing real workplace dynamics in their own words. That overlap between what the numbers show and what people volunteered to say makes the case for these recommendations stronger, not just statistically but personally.</div>', unsafe_allow_html=True)

# ---------------- TAB 6: AWARENESS GAP RADAR ----------------
with tab6:
    st.subheader("🎯 The Awareness Gap Radar")
    st.markdown("""
        The gold shape below shows what share of your **currently filtered segment** answered "Yes" to five
        workplace-support questions, plotted against the full dataset's baseline (dashed grey). A small,
        collapsed gold shape means most people are **unsure or unaware** — not necessarily told "no."
    """)

    awareness_fields = {
        'Benefits': 'benefits', 'Care Options': 'care_options', 'Anonymity': 'anonymity',
        'Seek-Help Resources': 'seek_help', 'Wellness Program': 'wellness_program'
    }

    def awareness_pct(data, field):
        return (data[field] == 'Yes').mean() * 100 if len(data) else 0

    filtered_scores = [awareness_pct(filtered_df, f) for f in awareness_fields.values()]
    baseline_scores = [awareness_pct(df, f) for f in awareness_fields.values()]
    categories = list(awareness_fields.keys())

    left, right = st.columns([1.4, 1])

    with left:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=baseline_scores + [baseline_scores[0]], theta=categories + [categories[0]],
            fill='none', name='Full Dataset (baseline)', line=dict(color=MUTED, dash='dash', width=2),
            hovertemplate='%{theta} — baseline: %{r:.1f}%<extra></extra>'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=filtered_scores + [filtered_scores[0]], theta=categories + [categories[0]],
            fill='toself', name='Current Segment', line=dict(color=GOLD, width=3),
            fillcolor='rgba(212,166,86,0.28)', mode='lines+markers',
            marker=dict(size=8, color=GOLD),
            hovertemplate='%{theta} — segment: %{r:.1f}%<extra></extra>'
        ))
        fig_radar.update_layout(
            polar=dict(bgcolor=CARD, radialaxis=dict(visible=True, range=[0, 100], color=MUTED, tickfont=dict(size=11)),
                       angularaxis=dict(color=TEXT, tickfont=dict(size=13))),
            paper_bgcolor=BG, font_color=TEXT, showlegend=True,
            legend=dict(orientation='h', y=-0.12), height=560,
            title=dict(text='Awareness Score by Category (% answering "Yes")', font=dict(color=GOLD, size=15)),
            hoverlabel=dict(bgcolor=CARD, font_color=TEXT, bordercolor=GOLD)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with right:
        st.markdown("**Same data, plain bar chart**")
        bar_df = pd.DataFrame({'Category': categories, 'Segment %': filtered_scores}).sort_values('Segment %')
        fig_bar = px.bar(bar_df, x='Segment %', y='Category', orientation='h',
                          color='Segment %', color_continuous_scale=DIVERGING, text_auto='.1f')
        fig_bar.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_fig(fig_bar, height=350, title='Awareness by Category — Segment'), use_container_width=True)

        awareness_score = sum(filtered_scores) / len(filtered_scores)
        st.markdown(f'<div class="metric-card"><div class="metric-label">Awareness Score (segment)</div><div class="metric-value">{awareness_score:.1f}%</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Awareness Score by Company Size** *(full dataset, for comparison)*")

    rows = []
    for size in size_options:
        subset = df[df['no_employees'] == size]
        if len(subset) > 0:
            score = sum(awareness_pct(subset, f) for f in awareness_fields.values()) / len(awareness_fields)
            rows.append({'Company Size': size, 'Awareness Score': round(score, 1)})

    size_award_df = pd.DataFrame(rows)
    fig_size = px.bar(size_award_df, x='Company Size', y='Awareness Score',
                       color='Awareness Score', color_continuous_scale=DIVERGING, text_auto='.1f')
    fig_size.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_fig(fig_size, height=340, title='Awareness Score by Company Size'), use_container_width=True)
