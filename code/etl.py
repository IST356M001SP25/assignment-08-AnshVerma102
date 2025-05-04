import pandas as pd
import streamlit as st


def top_locations(violations_df: pd.DataFrame, threshold: float = 1000) -> pd.DataFrame:
    """
    Aggregate total violation amounts by location and return those above the threshold.
    """
    summed = (
        violations_df
        .groupby('location', as_index=False)['amount']
        .sum()
    )
    top = summed[summed['amount'] >= threshold]
    return top.sort_values('amount', ascending=False).reset_index(drop=True)


def top_locations_mappable(violations_df: pd.DataFrame, threshold: float = 1000) -> pd.DataFrame:
    """
    Get top locations with total amounts >= threshold and attach latitude/longitude.
    """
    top_loc = top_locations(violations_df, threshold)
    coords = (
        violations_df[['location', 'lat', 'lon']]
        .drop_duplicates(subset=['location'])
    )
    return top_loc.merge(coords, on='location')


def tickets_in_top_locations(violations_df: pd.DataFrame, threshold: float = 1000) -> pd.DataFrame:
    """
    Return all ticket records for locations whose total amounts exceed the threshold.
    """
    top_loc = top_locations(violations_df, threshold)
    return violations_df[violations_df['location'].isin(top_loc['location'])]


def main():
    print("Running ETL job...")
    input_file = './cache/final_cuse_parking_violations.csv'
    violations_df = pd.read_csv(input_file)

    # Top locations summary
    top_df = top_locations(violations_df)
    top_df.to_csv('./cache/top_locations.csv', index=False)
    print("Wrote top locations to './cache/top_locations.csv'.")

    # Top locations with coordinates
    mappable_df = top_locations_mappable(violations_df)
    mappable_df.to_csv('./cache/top_locations_mappable.csv', index=False)
    print("Wrote mappable top locations to './cache/top_locations_mappable.csv'.")

    # All tickets in top locations
    tickets_df = tickets_in_top_locations(violations_df)
    tickets_df.to_csv('./cache/tickets_in_top_locations.csv', index=False)
    print("Wrote tickets in top locations to './cache/tickets_in_top_locations.csv'.")


if __name__ == '__main__':
    main()
