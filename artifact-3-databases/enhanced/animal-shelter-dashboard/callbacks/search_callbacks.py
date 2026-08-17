# ============================================================
# SEARCH DASHBOARD CALLBACKS
# ============================================================
# Contains callback logic for the animal search dashboard,
# including dynamic breed options and multi-criteria searching.

from dash import Input, Output, State, ctx
import pandas as pd


def register_search_callbacks(app, animals):

    # ========================================================
    # BREED FILTER CALLBACK
    # ========================================================
    # Updates the available breed options whenever the selected
    # animal type changes.

    @app.callback(
        [
            Output("search-breed", "options"),
            Output("search-breed", "value"),
            Output("search-breed", "disabled"),
            Output("search-breed", "placeholder")
        ],
        Input("search-animal-type", "value")
    )
    def update_breed_options(animal_type):

        # No animal type selected, so breed selection remains
        # disabled until an animal type is chosen.
        if not animal_type:
            return (
                [],
                None,
                True,
                "Select Animal Type First"
            )

        # Retrieve breeds belonging to the selected animal type.
        breeds = animals.get_breeds_by_animal_type(
            animal_type
        )

        options = [
            {
                "label": breed,
                "value": breed
            }
            for breed in breeds
        ]

        return (
            options,
            None,
            False,
            "Any Breed"
        )


    # ========================================================
    # SEARCH CALLBACK
    # ========================================================
    # Uses the enhanced AnimalRepository search method to return
    # animal records matching the selected search criteria.

    @app.callback(
        [
            Output("search-results-table", "data"),
            Output("search-results-table", "columns"),
            Output("search-result-count", "children")
        ],
        [
            Input("search-button", "n_clicks"),
            Input("search-reset-button", "n_clicks")
        ],
        [
            State("search-animal-type", "value"),
            State("search-breed", "value"),
            State("search-outcome-type", "value"),
            State("search-min-age", "value"),
            State("search-max-age", "value")
        ],
        prevent_initial_call=True
    )
    def search_dashboard(
            search_clicks,
            reset_clicks,
            animal_type,
            breed,
            outcome_type,
            min_age,
            max_age):

        trigger = ctx.triggered_id

        # ----------------------------------------------------
        # RESET SEARCH
        # --------------------------------------------------------
        # Clears the current search results when Reset is used.
        if trigger == "search-reset-button":
            return (
                [],
                [],
                "Search reset."
            )

        # ----------------------------------------------------
        # VALIDATE AGE INPUT
        # --------------------------------------------------------
        # Age fields use text input to avoid browser-generated
        # number spinner controls. Convert entered values into
        # numbers before sending them to the repository.

        try:
            min_age = (
                float(min_age)
                if min_age not in (None, "")
                else None
            )

            max_age = (
                float(max_age)
                if max_age not in (None, "")
                else None
            )

        except (ValueError, TypeError):
            return (
                [],
                [],
                "Age values must be numeric."
            )

        # Age values cannot be negative.
        if min_age is not None and min_age < 0:
            return (
                [],
                [],
                "Minimum age cannot be negative."
            )

        if max_age is not None and max_age < 0:
            return (
                [],
                [],
                "Maximum age cannot be negative."
            )

        # Minimum age cannot exceed maximum age.
        if (
            min_age is not None
            and max_age is not None
            and min_age > max_age
        ):
            return (
                [],
                [],
                "Minimum age cannot be greater than maximum age."
            )

        # ----------------------------------------------------
        # EXECUTE SEARCH
        # --------------------------------------------------------
        # Send the selected search criteria to the enhanced
        # AnimalRepository search method.

        results = animals.search_animals(
            animal_type=animal_type,
            breed=breed,
            outcome_type=outcome_type,
            min_age_weeks=min_age,
            max_age_weeks=max_age
        )

        result_df = pd.DataFrame.from_records(
            results
        )

        # ----------------------------------------------------
        # HANDLE NO RESULTS
        # --------------------------------------------------------

        if result_df.empty:
            return (
                [],
                [],
                "No matching animals found."
            )

        # ----------------------------------------------------
        # PREPARE RESULTS FOR DISPLAY
        # --------------------------------------------------------

        # MongoDB internal IDs are not displayed.
        if "_id" in result_df.columns:
            result_df.drop(
                columns=["_id"],
                inplace=True
            )

        # GeoJSON data is retained in MongoDB for geospatial
        # operations but should not display directly.
        if "location" in result_df.columns:
            result_df.drop(
                columns=["location"],
                inplace=True
            )

        # Convert MongoDB date fields into display-safe strings.
        date_columns = [
            "date_of_birth",
            "datetime",
            "monthyear"
        ]

        for column in date_columns:
            if column in result_df.columns:
                result_df[column] = (
                    result_df[column].astype(str)
                )

        # Convert the DataFrame into records for the Dash table.
        data = result_df.to_dict("records")

        # Dynamically create table columns based on the fields
        # returned by the database search.
        columns = [
            {
                "name": column,
                "id": column
            }
            for column in result_df.columns
        ]

        # ----------------------------------------------------
        # RETURN SEARCH RESULTS
        # --------------------------------------------------------

        return (
            data,
            columns,
            f"Search Results: {len(data)}"
        )