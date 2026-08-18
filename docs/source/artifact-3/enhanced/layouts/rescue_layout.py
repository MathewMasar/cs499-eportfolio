# ============================================================
# RESCUE DASHBOARD LAYOUT
# ============================================================
# Defines the operational rescue dashboard used to filter
# animals by rescue program, display matching records, and
# provide chart and map containers for callback output.

from dash import dcc, html, dash_table
import pandas as pd


def create_rescue_layout(animals):

    # Load the initial set of shelter records.
    records = animals.read({
        "animal_type": {"$exists": True}
    })

    df = pd.DataFrame.from_records(records)

    # Remove fields that should not be displayed directly.
    if "_id" in df.columns:
        df.drop(columns=["_id"], inplace=True)

    if "location" in df.columns:
        df.drop(columns=["location"], inplace=True)

    # Convert date/time values to display-safe strings.
    date_columns = [
        "date_of_birth",
        "datetime",
        "monthyear"
    ]

    for column in date_columns:
        if column in df.columns:
            df[column] = df[column].astype(str)

    return html.Div([

        # ----------------------------------------------------
        # RESCUE PROGRAM FILTERS
        # ----------------------------------------------------
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "padding": "10px 20px"
            },
            children=[

                dcc.RadioItems(
                    id="filter-type",

                    options=[
                        {
                            "label": "Water Rescue",
                            "value": "water"
                        },
                        {
                            "label": "Mountain / Wilderness",
                            "value": "mountain"
                        },
                        {
                            "label": "Disaster / Tracking",
                            "value": "disaster"
                        },
                        {
                            "label": "Default / Reset",
                            "value": "reset"
                        }
                    ],

                    value="reset",
                    inline=True,

                    labelStyle={
                        "marginRight": "30px"
                    }
                ),

                html.Div(
                    id="result-count",
                    children=f"Total Results: {len(df)}",
                    style={
                        "fontWeight": "bold"
                    }
                )
            ]
        ),

        html.Hr(),

        # ----------------------------------------------------
        # ANIMAL DATA TABLE
        # ----------------------------------------------------
        dash_table.DataTable(
            id="datatable-id",

            columns=[
                {
                    "name": column,
                    "id": column,
                    "deletable": False,
                    "selectable": True
                }
                for column in df.columns
            ],

            data=df.to_dict("records"),

            filter_action="native",
            sort_action="native",
            sort_mode="multi",

            page_action="native",
            page_current=0,
            page_size=10,

            row_selectable="single",
            selected_rows=[0],

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
        ),

        html.Br(),
        html.Hr(),

        # ----------------------------------------------------
        # VISUALIZATION AND MAP
        # ----------------------------------------------------
        html.Div(
            style={
                "display": "flex",
                "gap": "20px"
            },
            children=[

                html.Div(
                    id="graph-id",
                    style={
                        "width": "50%"
                    }
                ),

                html.Div(
                    id="map-id",
                    style={
                        "width": "50%"
                    }
                )
            ]
        )
    ])