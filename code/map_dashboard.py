import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import geopandas as gpd

# Configure page layout
st.set_page_config(layout="wide")

# Map display constants
CUSE = (43.0481, -76.1474)  # Center of map (latitude, longitude)
ZOOM = 14                   # Initial zoom level
VMIN = 1000                 # Minimum value for color scale
VMAX = 5000                 # Maximum value for color scale

@st.cache_data
def load_ticket_data(path: str) -> pd.DataFrame:
    """Load and cache top locations with coordinates and amounts."""
    return pd.read_csv(path)


def create_ticket_map(
    df: pd.DataFrame,
    center: tuple,
    zoom_start: int,
    vmin: float,
    vmax: float
) -> folium.Map:
    """Generate a Folium map with ticket locations colored by amount."""
    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.lon, df.lat),
        crs='EPSG:4326'
    )
    # Initialize map
    m = folium.Map(location=center, zoom_start=zoom_start)
    # Add choropleth-style points
    gdf.explore(
        column='amount',
        map=m,
        cmap='magma',
        vmin=vmin,
        vmax=vmax,
        legend=True,
        legend_name='Total Violation Amount',
        marker_type='circle',
        marker_kwds={'radius': 10, 'fill': True}
    )
    return m


def main():
    st.title('Top Locations for Parking Tickets within Syracuse')
    st.caption(
        'This dashboard visualizes locations with $1,000+ in total parking '
        'violation amounts on an interactive map.'
    )

    # Load data
    df = load_ticket_data('./cache/top_locations_mappable.csv')

    # Render map
    folium_map = create_ticket_map(df, CUSE, ZOOM, VMIN, VMAX)
    sf.folium_static(folium_map, width=800, height=600)


if __name__ == '__main__':
    main()
