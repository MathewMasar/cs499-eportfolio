# ============================================================
# ADMIN / REPORTING DASHBOARD CALLBACKS
# ============================================================
# Contains callback logic for administrative reporting,
# including adoption summaries, outcome distributions,
# animal-type metrics, breed metrics, and age-group metrics.

from dash import Input, Output, dcc, html
import plotly.express as px
import pandas as pd


def register_admin_callbacks(app, reports):

    # ========================================================
    # ADMIN REPORTING CALLBACK
    # ========================================================
    # Loads shelter-wide reporting data when the Admin /
    # Reporting dashboard is displayed or refreshed.

    @app.callback(
        [
            Output("admin-summary-cards", "children"),
            Output("admin-outcome-chart", "children"),
            Output("admin-type-chart", "children"),
            Output("admin-breed-chart", "children"),
            Output("admin-age-chart", "children")
        ],
        Input("admin-refresh-button", "n_clicks")
    )
    def update_admin_dashboard(n_clicks):

        # ----------------------------------------------------
        # OVERALL ADOPTION SUMMARY
        # ----------------------------------------------------

        summary = reports.get_adoption_summary()

        total_animals = summary.get(
            "total_animals",
            0
        )

        total_adoptions = summary.get(
            "total_adoptions",
            0
        )

        adoption_rate = summary.get(
            "adoption_rate",
            0
        )

        summary_cards = html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "gap": "25px",
                "flexWrap": "wrap"
            },
            children=[

                html.Div(
                    style={
                        "padding": "20px",
                        "border": "1px solid #ccc",
                        "borderRadius": "8px",
                        "minWidth": "180px",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3("Total Animals"),
                        html.H2(f"{total_animals:,}")
                    ]
                ),

                html.Div(
                    style={
                        "padding": "20px",
                        "border": "1px solid #ccc",
                        "borderRadius": "8px",
                        "minWidth": "180px",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3("Total Adoptions"),
                        html.H2(f"{total_adoptions:,}")
                    ]
                ),

                html.Div(
                    style={
                        "padding": "20px",
                        "border": "1px solid #ccc",
                        "borderRadius": "8px",
                        "minWidth": "180px",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3("Adoption Rate"),
                        html.H2(f"{adoption_rate:.2f}%")
                    ]
                )
            ]
        )

        # ----------------------------------------------------
        # OUTCOME DISTRIBUTION
        # ----------------------------------------------------

        outcome_results = (
            reports.get_outcome_distribution()
        )

        outcome_df = pd.DataFrame.from_records(
            outcome_results
        )

        if outcome_df.empty:
            outcome_chart = html.Div(
                "No outcome reporting data available."
            )
        else:
            outcome_figure = px.pie(
                outcome_df,
                names="outcome_type",
                values="count",
                title="Shelter Outcome Distribution"
            )

            outcome_chart = dcc.Graph(
                figure=outcome_figure
            )

        # ----------------------------------------------------
        # ADOPTION BY ANIMAL TYPE
        # ----------------------------------------------------

        type_results = (
            reports.get_adoption_stats_by_animal_type()
        )

        type_df = pd.DataFrame.from_records(
            type_results
        )

        if type_df.empty:
            type_chart = html.Div(
                "No animal type reporting data available."
            )
        else:
            type_figure = px.bar(
                type_df,
                x="animal_type",
                y="adoption_rate",
                text="adoption_rate",
                title="Adoption Rate by Animal Type",
                labels={
                    "animal_type": "Animal Type",
                    "adoption_rate": "Adoption Rate (%)"
                }
            )

            type_chart = dcc.Graph(
                figure=type_figure
            )

        # ----------------------------------------------------
        # ADOPTION BY BREED
        # ----------------------------------------------------

        breed_results = (
            reports.get_adoption_stats_by_breed(10)
        )

        breed_df = pd.DataFrame.from_records(
            breed_results
        )

        if breed_df.empty:
            breed_chart = html.Div(
                "No breed reporting data available."
            )
        else:
            breed_figure = px.bar(
                breed_df,
                x="breed",
                y="adoption_rate",
                text="adoption_rate",

                hover_data={
                    "adoptions": True,
                    "total": True,
                    "adoption_rate": ":.2f"
                },

                title="Adoption Rate Among Top 10 Most-Adopted Breeds",

                labels={
                    "breed": "Breed",
                    "adoption_rate": "Adoption Rate (%)",
                    "adoptions": "Total Adopted",
                    "total": "Total Records"
                }
            )

            breed_chart = dcc.Graph(
                figure=breed_figure
            )

        # ----------------------------------------------------
        # ADOPTION BY AGE GROUP
        # ----------------------------------------------------

        age_results = (
            reports.get_adoption_stats_by_age_group()
        )

        age_df = pd.DataFrame.from_records(
            age_results
        )

        if age_df.empty:
            age_chart = html.Div(
                "No age-group reporting data available."
            )
        else:
            age_figure = px.bar(
                age_df,
                x="age_group",
                y="adoption_rate",
                text="adoption_rate",
                title="Adoption Rate by Age Group",
                labels={
                    "age_group": "Age Group",
                    "adoption_rate": "Adoption Rate (%)"
                }
            )

            age_chart = dcc.Graph(
                figure=age_figure
            )

        return (
            summary_cards,
            outcome_chart,
            type_chart,
            breed_chart,
            age_chart
        )