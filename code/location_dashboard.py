import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure page layout
st.set_page_config(layout="wide")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Load and cache parking ticket data."""
    return pd.read_csv(path)

@st.cache_data
def filter_by_location(df: pd.DataFrame, location: str) -> pd.DataFrame:
    """Cache filtered dataframe for a given location."""
    return df[df['location'] == location]

def plot_bar(data: pd.DataFrame, x: str, y: str, title: str) -> plt.Figure:
    """Create a bar plot of summed values by category."""
    fig, ax = plt.subplots()
    sns.barplot(data=data, x=x, y=y, estimator=sum, ax=ax)
    ax.set_title(title)
    return fig


def main():
    # Load data once
    df = load_data('./cache/tickets_in_top_locations.csv')

    st.title('Top Locations for Parking Tickets within Syracuse')
    st.caption(
        'This dashboard shows the parking tickets issued in locations with $1,000+'
        ' in total violation amounts.'
    )

    # Location selector
    location = st.selectbox('Select a location:', df['location'].unique())
    if not location:
        return

    # Filter data
    filtered_df = filter_by_location(df, location)

    # Layout: metrics and plots
    col1, col2 = st.columns(2)

    with col1:
        st.metric('Total tickets issued', filtered_df.shape[0])
        fig1 = plot_bar(
            filtered_df,
            x='hourofday',
            y='count',
            title='Tickets Issued by Hour of Day'
        )
        st.pyplot(fig1)

    with col2:
        total_amount = filtered_df['amount'].sum()
        st.metric('Total amount', f"${total_amount:,.2f}")
        fig2 = plot_bar(
            filtered_df,
            x='dayofweek',
            y='count',
            title='Tickets Issued by Day of Week'
        )
        st.pyplot(fig2)

    # Map of ticket locations
    st.map(filtered_df[['lat', 'lon']])


if __name__ == '__main__':
    main()
