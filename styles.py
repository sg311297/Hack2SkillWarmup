"""
CSS styling for the Monsoon Preparedness Application.
Contains all custom CSS classes and theme definitions.
"""

GLOBAL_STYLES = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Nunito:wght@400;600;700&display=swap');
    :root {
        color-scheme: light;
        font-family: 'Inter', 'Nunito', sans-serif;
        background: #f8fafc;
    }
    html, body {
        background: #f8fafc;
    }
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #eef4fb 100%);
        color: #0f172a;
    }
"""

CARD_STYLES = """
    .hero-panel,
    .glass-card,
    .sidebar-card,
    .result-card,
    .loading-card,
    .report-card {
        border-radius: 22px;
        background: rgba(255,255,255,0.86);
        box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
        border: 1px solid rgba(255,255,255,0.72);
        backdrop-filter: blur(18px);
        padding: 10px;
    }
"""

HERO_STYLES = """
    .hero-panel {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(37,99,235,0.95), rgba(20,184,166,0.9));
        color: #ffffff;
        border: none;
    }
    .hero-panel::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top left, rgba(255,255,255,0.22), transparent 24%),
                    radial-gradient(circle at bottom right, rgba(255,255,255,0.16), transparent 18%);
        pointer-events: none;
    }
    .hero-content {
        position: relative;
        z-index: 1;
    }
    .hero-title {
        font-size: clamp(2.55rem, 2.35vw, 3.75rem);
        line-height: 1.02;
        margin: 0;
        letter-spacing: -0.05em;
        font-weight: 800;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.92;
        max-width: 760px;
        margin-top: 14px;
        line-height: 1.75;
    }
    .hero-pill-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 16px;
        margin-top: 28px;
    }
    .hero-pill {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 18px;
        border-radius: 18px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.18);
        color: #ffffff;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .hero-pill span {
        font-size: 1.35rem;
    }
"""

METRIC_STYLES = """
    .metric-card {
        border-radius: 22px;
        border: 1px solid rgba(15,23,42,0.08);
        padding: 24px;
        background: #ffffff;
        box-shadow: 0 18px 40px rgba(15,23,42,0.06);
        min-height: 140px;
    }
    .metric-card h4 {
        margin: 0 0 12px;
        font-size: 0.95rem;
        color: #475569;
        font-weight: 600;
    }
    .metric-card p {
        margin: 0;
        font-size: 1.85rem;
        font-weight: 700;
        color: #0f172a;
    }
"""

SIDEBAR_STYLES = """
    .sidebar-panel {
        border-radius: 24px;
        padding: 22px;
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(15,23,42,0.06);
        box-shadow: 0 24px 50px rgba(15,23,42,0.08);
        margin-bottom: 18px;
    }
    .sidebar-brand {
        display: flex;
        gap: 14px;
        align-items: center;
        margin-bottom: 20px;
    }
    .sidebar-brand .brand-icon {
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        border-radius: 14px;
        background: linear-gradient(135deg, #2563eb, #14b8a6);
        color: white;
        font-size: 1.15rem;
    }
    .sidebar-brand h2 {
        margin: 0;
        font-size: 1.05rem;
        line-height: 1.2;
        color: #0f172a;
    }
    .sidebar-link {
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none;
        color: #0f172a;
        padding: 12px 14px;
        border-radius: 16px;
        margin-bottom: 8px;
        transition: all 180ms ease;
        border: 1px solid transparent;
        font-size: 0.98rem;
        background: rgba(15,23,42,0.02);
    }
    .sidebar-link:hover {
        transform: translateX(4px);
        border-color: rgba(37,99,235,0.18);
        background: rgba(37,99,235,0.06);
    }
    .sidebar-divider {
        height: 1px;
        background: rgba(15,23,42,0.08);
        margin: 18px 0;
    }
"""

RESULT_STYLES = """
    .glass-card h3,
    .result-card h3,
    .loading-card h3 {
        margin-top: 0;
        margin-bottom: 12px;
        font-size: 1.25rem;
    }
    .result-grid {
        display: grid;
        gap: 20px;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    }
    .result-card {
        position: relative;
        overflow: hidden;
    }
    .result-card .card-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 14px;
        margin-bottom: 14px;
        font-size: 1.25rem;
    }
"""

BADGE_STYLES = """
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 700;
    }
    .badge-success { background: rgba(34,197,94,0.12); color: #166534; }
    .badge-warning { background: rgba(245,158,11,0.12); color: #92400e; }
    .badge-danger { background: rgba(239,68,68,0.12); color: #991b1b; }
"""

LOADING_STYLES = """
    .loading-card {
        display: grid;
        grid-template-columns: 1fr;
        gap: 18px;
        align-items: center;
        text-align: center;
    }
    .loading-dots {
        display: inline-flex;
        gap: 8px;
        justify-content: center;
    }
    .loading-dots span {
        width: 12px;
        height: 12px;
        border-radius: 999px;
        background: #2563eb;
        animation: bounce 1.15s infinite ease-in-out;
    }
    .loading-dots span:nth-child(2) { animation-delay: 0.15s; }
    .loading-dots span:nth-child(3) { animation-delay: 0.3s; }
    @keyframes bounce {
        0%, 80%, 100% { transform: translateY(0); opacity: 0.55; }
        40% { transform: translateY(-10px); opacity: 1; }
    }
"""

BUTTON_STYLES = """
    .primary-gradient-button > button {
        border-radius: 18px;
        padding: 14px 28px;
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        background: linear-gradient(135deg, #2563eb, #14b8a6);
        border: none;
        box-shadow: 0 20px 40px rgba(37,99,235,0.18);
        transition: transform 180ms ease, box-shadow 180ms ease;
    }
    .primary-gradient-button > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 26px 50px rgba(37,99,235,0.22);
    }
    .primary-gradient-button > button:focus {
        outline: none;
        box-shadow: 0 0 0 4px rgba(37,99,235,0.18);
    }
"""

FOOTER_STYLES = """
    .footer-bar {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 12px;
        padding: 16px 20px;
        margin-top: 42px;
        border-top: 1px solid rgba(15,23,42,0.08);
        color: #475569;
        font-size: 0.93rem;
    }
    .footer-bar strong { color: #0f172a; }
"""

UTILITY_STYLES = """
    .section-divider {
        height: 1px;
        background: rgba(15,23,42,0.08);
        margin: 28px 0;
    }
    .report-card {
        border-radius: 20px;
        padding: 22px;
        background: rgba(255,255,255,0.94);
        border: 1px solid rgba(15,23,42,0.06);
        box-shadow: 0 18px 35px rgba(15,23,42,0.06);
    }
    .section-heading {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 18px;
    }
    .section-heading h2 {
        margin: 0;
        font-size: 1.5rem;
    }
    .section-heading p {
        margin: 0;
        color: #64748b;
        font-size: 0.95rem;
    }
    .stCheckbox label {
        font-weight: 600;
    }
    .stCheckbox input:checked + label {
        color: #15803d;
    }
"""

# Combine all styles
ALL_STYLES = f"""
<style>
{GLOBAL_STYLES}
{CARD_STYLES}
{HERO_STYLES}
{METRIC_STYLES}
{SIDEBAR_STYLES}
{RESULT_STYLES}
{BADGE_STYLES}
{LOADING_STYLES}
{BUTTON_STYLES}
{FOOTER_STYLES}
{UTILITY_STYLES}
</style>
"""
