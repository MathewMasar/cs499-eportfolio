# ============================================================
# GRAZIOSO SALVARE DASHBOARD
# ============================================================
# Application entry point for the enhanced CS-499 database
# artifact. This file creates the shared database services,
# configures the Dash application, and loads each dashboard view.

from dash import Dash, dcc, html, Input, Output

from database import DatabaseConnection
from animal_repository import AnimalRepository
from reporting_service import ReportingService

from layouts.rescue_layout import create_rescue_layout
from layouts.search_layout import create_search_layout
from layouts.admin_layout import create_admin_layout

from callbacks.rescue_callbacks import register_rescue_callbacks
from callbacks.search_callbacks import register_search_callbacks
from callbacks.admin_callbacks import register_admin_callbacks

# ============================================================
# DATABASE SERVICES
# ============================================================

database = DatabaseConnection()

animals = AnimalRepository(database)

reports = ReportingService(database)


# ============================================================
# DASH APPLICATION
# ============================================================

app = Dash(
    __name__,
    suppress_callback_exceptions=True
)

# Register Rescue Dashboard callbacks.
register_rescue_callbacks(
    app,
    animals
)

# Register Search Dashboard callbacks
register_search_callbacks(
    app,
    animals
)

# Register Admin Dashboard callbacks
register_admin_callbacks(
    app,
    reports
)
# ============================================================
# APPLICATION LAYOUT
# ============================================================

app.layout = html.Div([

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------
    html.Div(
        style={
            "textAlign": "center",
            "padding": "25px"
        },
        children=[

            html.H1(
                "Grazioso Salvare Dashboard",
                style={"margin": "0"}
            ),

            html.H2(
                "Animal Shelter Management and Reporting",
                style={"margin": "5px"}
            ),

            html.H3(
                "Enhanced CS-499 Database Artifact",
                style={"margin": "5px"}
            ),

            html.P(
                "Mathew Masar",
                style={"margin": "5px"}
            )
        ]
    ),

    html.Hr(),

    # --------------------------------------------------------
    # DASHBOARD NAVIGATION
    # --------------------------------------------------------
    dcc.Tabs(
        id="dashboard-tabs",
        value="rescue",
        children=[

            dcc.Tab(
                label="Rescue Dashboard",
                value="rescue"
            ),

            dcc.Tab(
                label="Search Dashboard",
                value="search"
            ),

            dcc.Tab(
                label="Admin / Reporting",
                value="admin"
            )
        ]
    ),

    html.Div(
        id="tab-content"
    )
])


# ============================================================
# TAB NAVIGATION CALLBACK
# ============================================================

@app.callback(
    Output("tab-content", "children"),
    Input("dashboard-tabs", "value")
)
def render_tab(tab):

    if tab == "rescue":
        return create_rescue_layout(animals)

    if tab == "search":
        return create_search_layout()

    if tab == "admin":
        return create_admin_layout()

    return html.Div(
        "Unable to load dashboard."
    )


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    print(
        "Database connected:",
        database.health_check()
    )

    app.run(debug=False)