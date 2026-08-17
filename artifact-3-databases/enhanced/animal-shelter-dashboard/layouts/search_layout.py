# ============================================================
# SEARCH DASHBOARD LAYOUT
# ============================================================
# Defines the interactive animal search interface. Search logic
# is handled separately in the search callback module.

from dash import dcc, html, dash_table


def create_search_layout():

    return html.Div(
        style={
            "padding": "20px"
        },
        children=[

            html.H2(
                "Animal Search",
                style={
                    "textAlign": "center"
                }
            ),

            html.P(
                "Search shelter records by animal type, breed, "
                "outcome, and age range.",
                style={
                    "textAlign": "center"
                }
            ),

            html.Hr(),

            # ------------------------------------------------
            # SEARCH FILTER CONTROLS
            # ------------------------------------------------
            html.Div(
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "gap": "20px",
                    "justifyContent": "center",
                    "alignItems": "end"
                },
                children=[

                    # Animal Type
                    html.Div([
                        html.Label("Animal Type"),

                        dcc.Dropdown(
                            id="search-animal-type",

                            options=[
                                {
                                    "label": "Dog",
                                    "value": "Dog"
                                },
                                {
                                    "label": "Cat",
                                    "value": "Cat"
                                },
                                {
                                    "label": "Bird",
                                    "value": "Bird"
                                },
                                {
                                    "label": "Other",
                                    "value": "Other"
                                }
                            ],

                            placeholder="Any Type",
                            clearable=True,

                            style={
                                "width": "180px"
                            }
                        )
                    ]),

                    # Breed
                    html.Div([
                        html.Label("Breed"),

                        dcc.Dropdown(
                            id="search-breed",
                            options=[],
                            placeholder="Select Animal Type First",
                            clearable=True,
                            disabled=True,

                            style={
                                "width": "260px"
                            }
                        )
                    ]),

                    # Outcome Type
                    html.Div([
                        html.Label("Outcome Type"),

                        dcc.Dropdown(
                            id="search-outcome-type",

                            options=[
                                {
                                    "label": "Adoption",
                                    "value": "Adoption"
                                },
                                {
                                    "label": "Transfer",
                                    "value": "Transfer"
                                },
                                {
                                    "label": "Return to Owner",
                                    "value": "Return to Owner"
                                },
                                {
                                    "label": "Euthanasia",
                                    "value": "Euthanasia"
                                }
                            ],

                            placeholder="Any Outcome",
                            clearable=True,

                            style={
                                "width": "200px"
                            }
                        )
                    ]),

                    # Minimum Age
                    html.Div([
                        html.Label("Minimum Age (Weeks)"),

                        dcc.Input(
                            id="search-min-age",
                            type="text",
                            placeholder="Minimum",
                            style={
                                "width": "150px",
                                "height": "36px"
                            }
                        )
                    ]),

                    # Maximum Age
                    html.Div([
                        html.Label("Maximum Age (Weeks)"),

                        dcc.Input(
                            id="search-max-age",
                            type="text",
                            placeholder="Maximum",
                            style={
                                "width": "150px",
                                "height": "36px"
                            }
                        )
                    ]),
                ]
            ),

            html.Br(),

            # ------------------------------------------------
            # SEARCH BUTTONS
            # ------------------------------------------------
            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "gap": "15px"
                },
                children=[

                    html.Button(
                        "Search",
                        id="search-button",
                        n_clicks=0
                    ),

                    html.Button(
                        "Reset",
                        id="search-reset-button",
                        n_clicks=0
                    )
                ]
            ),

            html.Br(),

            html.Div(
                id="search-result-count",
                style={
                    "textAlign": "center",
                    "fontWeight": "bold"
                }
            ),

            html.Hr(),

            # ------------------------------------------------
            # SEARCH RESULTS TABLE
            # ------------------------------------------------
            dash_table.DataTable(
                id="search-results-table",

                data=[],

                filter_action="native",
                sort_action="native",
                sort_mode="multi",

                page_action="native",
                page_current=0,
                page_size=10,

                style_table={
                    "overflowX": "auto"
                },

                style_cell={
                    "textAlign": "left",
                    "padding": "8px",
                    "minWidth": "100px",
                    "maxWidth": "250px",
                    "whiteSpace": "normal"
                }
            )
        ]
    )