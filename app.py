import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# ── 1. Load and prepare data ─────────────────────────────────────────────────
df = pd.read_csv("output.csv")

# Ensure date is parsed correctly and sorted
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Aggregate total sales per day across all regions
daily_sales = df.groupby("date", as_index=False)["sales"].sum()

# ── 2. Build the line chart ───────────────────────────────────────────────────
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Daily Sales",
    labels={"date": "Date", "sales": "Total Sales ($)"},
)

# Add a vertical line marking the price increase on Jan 15, 2021
fig.add_vline(
    x="2021-01-15",
    line_dash="dash",
    line_color="red",
    annotation_text="Price Increase (Jan 15, 2021)",
    annotation_position="top left",
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Sales ($)",
    hovermode="x unified",
    template="plotly_white",
)

# ── 3. Build the Dash app ─────────────────────────────────────────────────────
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        # Header
        html.H1(
            "Soul Foods — Pink Morsel Sales Visualiser",
            style={
                "textAlign": "center",
                "fontFamily": "Arial, sans-serif",
                "color": "#2c3e50",
                "padding": "20px",
                "borderBottom": "2px solid #e74c3c",
                "marginBottom": "20px",
            },
        ),

        # Subtitle / business question
        html.P(
            "Were sales higher before or after the Pink Morsel price increase on 15 January 2021?",
            style={
                "textAlign": "center",
                "fontFamily": "Arial, sans-serif",
                "color": "#7f8c8d",
                "fontSize": "16px",
                "marginBottom": "30px",
            },
        ),

        # Line chart
        dcc.Graph(
            id="sales-line-chart",
            figure=fig,
            style={"height": "550px"},
        ),

        # Footer note
        html.P(
            "The dashed red line marks the price increase date. Sales above this line represent post-increase performance.",
            style={
                "textAlign": "center",
                "fontFamily": "Arial, sans-serif",
                "color": "#95a5a6",
                "fontSize": "13px",
                "marginTop": "10px",
            },
        ),
    ],
    style={"maxWidth": "1100px", "margin": "0 auto", "padding": "20px"},
)

# ── 4. Run the app ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)