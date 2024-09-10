import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Set the plotting style
plt.style.use('dark_background')


# Function to generate time series plots
def generate_time_series_plots(username, df):
    st.subheader(f"Carbon emissions over Time for {username}")

    # Ensure 'dated' column is of datetime type
    df['dated'] = pd.to_datetime(df['dated'])

    # Plot 1: Line plot of prediction values over time
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['dated'], df['prediction'], color='#DA444A', marker='o')
    ax.set_xlabel("Date")
    ax.set_ylabel("Emission Value")
    ax.set_title(f"Carbon emissions over Time for {username}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # Plot 2: Scatter plot with trend line
    st.subheader(f"Trend Line for {username}")
    fig, ax = plt.subplots(figsize=(12, 6))

    df['dated_numeric'] = (df['dated'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1d')
    sns.regplot(x='dated_numeric', y='prediction', data=df, color='#DA444A', ax=ax)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.set_xlabel("Date")
    ax.set_ylabel("Emissions")
    ax.set_title(f"Trend Line for {username}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # Plot 3: Box plot by month
    st.subheader(f"Box Plot of Emissions Values by Month for {username}")
    df['month'] = df['dated'].dt.month
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='month', y='prediction', data=df, color='#DA444A', ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Prediction Value")
    ax.set_title(f"Bar Plot of Emissions Values by Month for {username}")
    st.pyplot(fig)


# Function to plot feature contribution
def plot_feature_contribution(username, df):
    st.subheader(f"Top 5 Feature Contributions to Emissions for {username}")

    features = ['MonthlyGroceryBill', 'VehicleDailyDistanceKm', 'WasteBagWeeklyCount',
                'HowLongTVPCDailyHour', 'HowManyNewClothesMonthly', 'HowLongInternetDailyHour']

    # Calculate feature contributions
    feature_contributions = {feature: df[feature].sum() for feature in features}
    sorted_contributions = sorted(feature_contributions.items(), key=lambda x: x[1], reverse=True)[:5]
    top_features, top_values = zip(*sorted_contributions)

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(top_values, labels=top_features, autopct='%1.1f%%', startangle=90)
    ax.legend(wedges, top_features, title="Features", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title(f"Top 5 Feature Contributions to Emissions for {username}")
    ax.axis('equal')
    st.pyplot(fig)


# Function to plot categorical variable contributions
def plot_categorical_contribution(username, df):
    st.subheader(f"Categorical Variable Contributions to Emissions for {username}")

    categorical_features = ['Diet', 'HowOftenShower', 'HeatingEnergySource',
                            'Transport', 'VehicleType', 'SocialActivity',
                            'FrequencyOfTravelingWithAir', 'WasteBagSize',
                            'EnergyEfficiency', 'Recycling', 'Cooking_With']

    # Loop through each categorical feature
    for selected_feature in categorical_features:
        contributions = df.groupby(selected_feature)['prediction'].sum()
        sorted_contributions = contributions.sort_values(ascending=False)[:5]
        top_categories = sorted_contributions.index
        top_values = sorted_contributions.values

        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(top_values, labels=top_categories, autopct='%1.1f%%', startangle=90)
        ax.legend(wedges, top_categories, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        ax.set_title(f"Top 5 Category Contributions to Emission for {selected_feature} ({username})")
        ax.axis('equal')
        st.pyplot(fig)


# Streamlit App
def main():
    st.title("Carbon Emission Visualization Dashboard")

    # Upload CSV
    uploaded_file = st.sidebar.file_uploader("Upload CSV file with prediction data", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Input username
        username = st.sidebar.text_input("Enter username")

        # Check if the username exists in the CSV
        if username in df['username'].unique():
            st.write(f"Generating visualizations for {username}")
            # Sidebar for selecting the type of visualization
            vis_type = st.sidebar.selectbox("Select Visualization Type",
                                            ("Time Series Plots", "Feature Contribution", "Categorical Contribution"))

            if vis_type == "Time Series Plots":
                generate_time_series_plots(username, df)
            elif vis_type == "Feature Contribution":
                plot_feature_contribution(username, df)
            elif vis_type == "Categorical Contribution":
                plot_categorical_contribution(username, df)

        else:
            st.error(f"Username '{username}' not found in the uploaded file.")


if __name__ == '__main__':
    main()
