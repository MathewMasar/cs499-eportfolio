# ============================================================
# ADMIN / REPORTING DASHBOARD LAYOUT
# ============================================================
# Defines the administrative reporting interface used to
# display shelter-wide adoption metrics, outcome summaries,
# and database-generated reporting visualizations.

from dash import html


def create_admin_layout():

    return html.Div(
        style={
            "padding": "20px"
        },
        children=[

            # ------------------------------------------------
            # HEADER
            # ------------------------------------------------
            html.H2(
                "Admin / Reporting",
                style={
                    "textAlign": "center"
                }
            ),

            html.P(
                "View shelter-wide adoption metrics, outcome "
                "distributions, and reporting summaries.",
                style={
                    "textAlign": "center"
                }
            ),

            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "center"
                },
                children=[

                    html.Button(
                        "Refresh Reports",
                        id="admin-refresh-button",
                        n_clicks=0
                    )
                ]
            ),

            html.Hr(),

            # ------------------------------------------------
            # SUMMARY CARDS
            # ------------------------------------------------
            html.Div(
                id="admin-summary-cards"
            ),

            html.Br(),
            html.Hr(),

            # ------------------------------------------------
            # OUTCOME DISTRIBUTION
            # ------------------------------------------------
            html.Div(
                id="admin-outcome-chart"
            ),

            html.Hr(),

            # ------------------------------------------------
            # ADOPTION BY ANIMAL TYPE
            # ------------------------------------------------
            html.Div(
                id="admin-type-chart"
            ),

            html.Hr(),

            # ------------------------------------------------
            # ADOPTION BY BREED
            # ------------------------------------------------
            html.Div(
                id="admin-breed-chart"
            ),

            html.Hr(),

            # ------------------------------------------------
            # ADOPTION BY AGE GROUP
            # ------------------------------------------------
            html.Div(
                id="admin-age-chart"
            )
        ]
    )