# ============================================================
# RESCUE DASHBOARD CALLBACKS
# ============================================================
# Contains callback logic for the operational rescue dashboard,
# including rescue-program filtering, visualization updates,
# and selected-animal map display.

from dash import Input, Output, dcc, html

import dash_leaflet as dl
import plotly.express as px
import pandas as pd


def register_rescue_callbacks(app, animals):

    # ========================================================
    # RESCUE PROGRAM FILTER CALLBACK
    # ========================================================
    # Updates the animal table and result count whenever a
    # rescue program filter is selected.

    @app.callback(
        [
            Output("datatable-id", "data"),
            Output("result-count", "children")
        ],
        Input("filter-type", "value")
    )
    def update_dashboard(filter_type):

        # ----------------------------------------------------
        # BUILD FILTER QUERY
        # ----------------------------------------------------

        if filter_type == "reset":
            query = {
                "animal_type": {"$exists": True}
            }

        elif filter_type == "water":
            query = {
                "animal_type": "Dog",
                "breed": {
                    "$in": [
                        "Labrador Retriever Mix",
                        "Chesapeake Bay Retriever",
                        "Newfoundland"
                    ]
                },
                "sex_upon_outcome": "Intact Female",
                "age_upon_outcome_in_weeks": {
                    "$gte": 26,
                    "$lte": 156
                }
            }

        elif filter_type == "mountain":
            query = {
                "animal_type": "Dog",
                "breed": {
                    "$in": [
                        "German Shepherd",
                        "Alaskan Malamute",
                        "Old English Sheepdog",
                        "Siberian Husky",
                        "Rottweiler"
                    ]
                },
                "sex_upon_outcome": "Intact Male",
                "age_upon_outcome_in_weeks": {
                    "$gte": 26,
                    "$lte": 156
                }
            }

        elif filter_type == "disaster":
            query = {
                "animal_type": "Dog",
                "breed": {
                    "$in": [
                        "Doberman Pinscher",
                        "German Shepherd",
                        "Golden Retriever",
                        "Bloodhound",
                        "Rottweiler"
                    ]
                },
                "sex_upon_outcome": "Intact Male",
                "age_upon_outcome_in_weeks": {
                    "$gte": 20,
                    "$lte": 300
                }
            }

        else:
            query = {
                "animal_type": {"$exists": True}
            }

        # ----------------------------------------------------
        # RETRIEVE AND PREPARE DATA
        # ----------------------------------------------------

        results = animals.read(query)

        filtered_df = pd.DataFrame.from_records(results)

        if "_id" in filtered_df.columns:
            filtered_df.drop(
                columns=["_id"],
                inplace=True
            )

        if "location" in filtered_df.columns:
            filtered_df.drop(
                columns=["location"],
                inplace=True
            )

        date_columns = [
            "date_of_birth",
            "datetime",
            "monthyear"
        ]

        for column in date_columns:
            if column in filtered_df.columns:
                filtered_df[column] = (
                    filtered_df[column].astype(str)
                )

        data = filtered_df.to_dict("records")

        return data, f"Total Results: {len(data)}"


    # ========================================================
    # RESCUE PROGRAM GRAPH CALLBACK
    # ========================================================
    # Displays rescue candidate distribution in the default
    # view and breed distribution for a selected program.

    @app.callback(
        Output("graph-id", "children"),
        [
            Input("datatable-id", "derived_virtual_data"),
            Input("filter-type", "value")
        ]
    )
    def update_graph(view_data, filter_type):

        if not view_data:
            return html.Div(
                "No data available for visualization."
            )

        filtered_df = pd.DataFrame.from_records(view_data)

        # ----------------------------------------------------
        # DEFAULT RESCUE DISTRIBUTION
        # ----------------------------------------------------

        if filter_type == "reset":

            water_query = {
                "animal_type": "Dog",
                "breed": {
                    "$in": [
                        "Labrador Retriever Mix",
                        "Chesapeake Bay Retriever",
                        "Newfoundland"
                    ]
                },
                "sex_upon_outcome": "Intact Female",
                "age_upon_outcome_in_weeks": {
                    "$gte": 26,
                    "$lte": 156
                }
            }

            mountain_query = {
                "animal_type": "Dog",
                "breed": {
                    "$in": [
                        "German Shepherd",
                        "Alaskan Malamute",
                        "Old English Sheepdog",
                        "Siberian Husky",
                        "Rottweiler"
                    ]
                },
                "sex_upon_outcome": "Intact Male",
                "age_upon_outcome_in_weeks": {
                    "$gte": 26,
                    "$lte": 156
                }
            }

            disaster_query = {
                "animal_type": "Dog",
                "breed": {
                    "$in": [
                        "Doberman Pinscher",
                        "German Shepherd",
                        "Golden Retriever",
                        "Bloodhound",
                        "Rottweiler"
                    ]
                },
                "sex_upon_outcome": "Intact Male",
                "age_upon_outcome_in_weeks": {
                    "$gte": 20,
                    "$lte": 300
                }
            }

            rescue_summary = pd.DataFrame({
                "Rescue Program": [
                    "Water Rescue",
                    "Mountain / Wilderness",
                    "Disaster / Tracking"
                ],
                "Candidates": [
                    len(animals.read(water_query)),
                    len(animals.read(mountain_query)),
                    len(animals.read(disaster_query))
                ]
            })

            figure = px.pie(
                rescue_summary,
                names="Rescue Program",
                values="Candidates",
                title="Rescue Candidate Distribution"
            )

        # ----------------------------------------------------
        # FILTERED BREED DISTRIBUTION
        # ----------------------------------------------------

        else:

            program_names = {
                "water": "Water Rescue",
                "mountain": "Mountain / Wilderness",
                "disaster": "Disaster / Tracking"
            }

            program_name = program_names.get(
                filter_type,
                "Selected Rescue Program"
            )

            figure = px.pie(
                filtered_df,
                names="breed",
                title=f"Breed Distribution: {program_name}"
            )

        return dcc.Graph(
            figure=figure
        )


    # ========================================================
    # MAP CALLBACK
    # ========================================================
    # Updates the map based on the currently selected animal
    # record in the rescue dashboard table.

    @app.callback(
        Output("map-id", "children"),
        [
            Input(
                "datatable-id",
                "derived_virtual_data"
            ),
            Input(
                "datatable-id",
                "derived_virtual_selected_rows"
            )
        ]
    )
    def update_map(view_data, selected_rows):

        if not view_data:
            return html.Div(
                "No location data available."
            )

        filtered_df = pd.DataFrame.from_records(
            view_data
        )

        if filtered_df.empty:
            return html.Div(
                "No location data available."
            )

        # Default to the first visible record.
        if not selected_rows:
            row_index = 0
        else:
            row_index = selected_rows[0]

        # Protect against invalid selection after filtering.
        if row_index >= len(filtered_df):
            row_index = 0

        selected_record = filtered_df.iloc[row_index]

        latitude = selected_record.get("location_lat")
        longitude = selected_record.get("location_long")

        if pd.isna(latitude) or pd.isna(longitude):
            return html.Div(
                "Selected animal does not contain "
                "valid location data."
            )

        return dl.Map(
            style={
                "width": "100%",
                "height": "500px"
            },

            center=[
                latitude,
                longitude
            ],

            zoom=10,

            children=[

                dl.TileLayer(),

                dl.Marker(
                    position=[
                        latitude,
                        longitude
                    ],

                    children=[

                        dl.Tooltip(
                            selected_record.get(
                                "breed",
                                "Unknown Breed"
                            )
                        ),

                        dl.Popup([

                            html.B("Animal Record"),

                            html.Br(),

                            html.Span(
                                f"Animal ID: "
                                f"{selected_record.get('animal_id', 'N/A')}"
                            ),

                            html.Br(),

                            html.Span(
                                f"Name: "
                                f"{selected_record.get('name') or 'N/A'}"
                            ),

                            html.Br(),

                            html.Span(
                                f"Type: "
                                f"{selected_record.get('animal_type', 'N/A')}"
                            ),

                            html.Br(),

                            html.Span(
                                f"Breed: "
                                f"{selected_record.get('breed', 'N/A')}"
                            ),

                            html.Br(),

                            html.Span(
                                f"Outcome: "
                                f"{selected_record.get('outcome_type', 'N/A')}"
                            ),

                            html.Br(),

                            html.Span(
                                f"Sex: "
                                f"{selected_record.get('sex_upon_outcome', 'N/A')}"
                            ),

                            html.Br(),

                            html.Span(
                                f"Age: "
                                f"{selected_record.get('age_upon_outcome', 'N/A')}"
                            )
                        ])
                    ]
                )
            ]
        )