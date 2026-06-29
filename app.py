import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# ── 1. Load and prepare data ──────────────────────────────────────────────────
df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# ── 2. Build the Dash app ─────────────────────────────────────────────────────
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "background": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
        "fontFamily": "'Segoe UI', Arial, sans-serif",
        "padding": "30px 20px",
    },
    children=[

        # ── Header card ───────────────────────────────────────────────────────
        html.Div(
            style={
                "textAlign": "center",
                "marginBottom": "30px",
            },
            children=[
                html.H1(
                    "🍬 Soul Foods Sales Visualiser",
                    style={
                        "color": "#ffffff",
                        "fontSize": "2.6rem",
                        "fontWeight": "700",
                        "letterSpacing": "1px",
                        "margin": "0 0 8px 0",
                        "textShadow": "0 2px 10px rgba(0,0,0,0.4)",
                    },
                ),
                html.P(
                    "Pink Morsel Regional Sales — Were sales higher before or after the price increase on 15 Jan 2021?",
                    style={
                        "color": "#a0aec0",
                        "fontSize": "1rem",
                        "margin": "0",
                    },
                ),
            ],
        ),

        # ── Main content card ─────────────────────────────────────────────────
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "background": "rgba(255, 255, 255, 0.05)",
                "borderRadius": "20px",
                "padding": "30px",
                "boxShadow": "0 8px 32px rgba(0, 0, 0, 0.4)",
                "backdropFilter": "blur(10px)",
                "border": "1px solid rgba(255, 255, 255, 0.1)",
            },
            children=[

                # ── Region filter label ───────────────────────────────────────
                html.P(
                    "Filter by Region",
                    style={
                        "color": "#e2e8f0",
                        "fontWeight": "600",
                        "fontSize": "0.9rem",
                        "textTransform": "uppercase",
                        "letterSpacing": "1.5px",
                        "marginBottom": "12px",
                    },
                ),

                # ── Radio buttons ─────────────────────────────────────────────
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "center",
                        "marginBottom": "28px",
                    },
                    children=[
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": " All",   "value": "all"},
                                {"label": " North", "value": "north"},
                                {"label": " East",  "value": "east"},
                                {"label": " South", "value": "south"},
                                {"label": " West",  "value": "west"},
                            ],
                            value="all",
                            inline=True,
                            inputStyle={
                                "marginRight": "6px",
                                "accentColor": "#e74c3c",
                                "cursor": "pointer",
                            },
                            labelStyle={
                                "color": "#e2e8f0",
                                "fontSize": "1rem",
                                "fontWeight": "500",
                                "marginRight": "28px",
                                "cursor": "pointer",
                                "padding": "8px 16px",
                                "borderRadius": "50px",
                                "border": "1px solid rgba(255,255,255,0.15)",
                                "background": "rgba(255,255,255,0.05)",
                                "transition": "all 0.2s ease",
                            },
                        ),
                    ],
                ),

                # ── Line chart ────────────────────────────────────────────────
                dcc.Graph(
                    id="sales-line-chart",
                    style={"height": "500px"},
                    config={"displayModeBar": False},
                ),

                # ── Divider ───────────────────────────────────────────────────
                html.Hr(
                    style={
                        "border": "none",
                        "borderTop": "1px solid rgba(255,255,255,0.1)",
                        "margin": "24px 0 16px",
                    }
                ),

                # ── Footer note ───────────────────────────────────────────────
                html.P(
                    "📍 The dashed red line marks the Pink Morsel price increase on 15 January 2021.",
                    style={
                        "color": "#718096",
                        "fontSize": "0.85rem",
                        "textAlign": "center",
                        "margin": "0",
                    },
                ),
            ],
        ),
    ],
)

# ── 3. Callback: update chart on region selection ─────────────────────────────
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(selected_region):
    # Filter data
    if selected_region == "all":
        filtered = df.groupby("date", as_index=False)["sales"].sum()
        region_label = "All Regions"
    else:
        filtered = (
            df[df["region"] == selected_region]
            .groupby("date", as_index=False)["sales"]
            .sum()
        )
        region_label = selected_region.capitalize()

    # Build figure
    fig = px.line(
        filtered,
        x="date",
        y="sales",
        labels={"date": "Date", "sales": "Total Sales ($)"},
    )

    # Style the line
    fig.update_traces(
        line=dict(color="#e74c3c", width=2.5),
        mode="lines",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales: $%{y:,.2f}<extra></extra>",
    )

    # Price increase marker
    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_color="rgba(255, 200, 0, 0.8)",
        line_width=2,
        annotation_text="Price Increase ↑",
        annotation_font_color="rgba(255, 200, 0, 0.9)",
        annotation_font_size=12,
        annotation_position="top left",
    )

    # Dark theme layout
    fig.update_layout(
        title=dict(
            text=f"Daily Pink Morsel Sales — {region_label}",
            font=dict(color="#e2e8f0", size=16),
            x=0.5,
            xanchor="center",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(color="#a0aec0"),
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.07)",
            linecolor="rgba(255,255,255,0.1)",
            tickfont=dict(color="#a0aec0"),
            title_font=dict(color="#e2e8f0"),
        ),
        yaxis=dict(
            title="Total Sales ($)",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.07)",
            linecolor="rgba(255,255,255,0.1)",
            tickfont=dict(color="#a0aec0"),
            title_font=dict(color="#e2e8f0"),
            tickprefix="$",
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#1a1a2e",
            bordercolor="#e74c3c",
            font_color="#ffffff",
        ),
        margin=dict(l=60, r=30, t=60, b=60),
    )

    return fig


# ── 4. Run ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)