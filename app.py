import requests
import streamlit as st
import plotly.express as px
import pandas as pd
import altair as alt


# Location coordinates
locations = {
    'Kota Surabaya': {'latitude': -7.25, 'longitude': 112.75},
    'Kab. Sidoarjo': {'latitude': -7.4418, 'longitude': 112.6010},
    'Kab. Bojonegoro': {'latitude': -7.1414, 'longitude': 112.5253},
    'Kota Mojokerto': {'latitude': -7.4703, 'longitude': 112.4473},
    'Kab. Lamongan': {'latitude': -6.4412, 'longitude': 112.3991},
    'Kota Pekalongan': {'latitude': -6.8793, 'longitude': 109.6748},
    'Kab. Pekalongan': {'latitude': -6.9545, 'longitude': 109.6884},
    'Kota Tegal': {'latitude': -6.8793, 'longitude': 109.6748},
    'Kota Bandung': {'latitude': -6.9175, 'longitude': 107.6191},
    'Kota Medan': {'latitude': 3.5952, 'longitude': 98.6722}
}

# Streamlit app layout
st.title("Weather Forecast 💧 dex pump v0.1")

# Location selection
selected_location = st.selectbox("Select Location", list(locations.keys()))
latitude = locations[selected_location]['latitude']
longitude = locations[selected_location]['longitude']

# URL for Open-Meteo API
url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

# Send request to API
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Display location based on coordinates
    st.write(f"Location: {selected_location} (Latitude {latitude}, Longitude {longitude})")

    # Current weather data
    current_weather = data.get("current_weather", {})
    if current_weather:
        # Safely get values and cast to float
        temperature = float(current_weather.get("temperature", 0))
        humidity = float(current_weather.get("relative_humidity_2m", 0))
        wind_speed = float(current_weather.get("windspeed", 0))
        
        st.write(f"Current Weather:")
        st.write(f"  Temperature: {temperature}°C")
        st.write(f"  Humidity: {humidity}%")
        st.write(f"  Wind Speed: {wind_speed} km/h")

        # Weather prediction based on the parameters
        forecast = "Unknown"
        potential_impact = "No prediction available"

        if temperature > 30 and humidity > 80:
            forecast = "Thunderstorm"
            potential_impact = "High risk of lightning and strong winds."
        elif temperature > 30 and wind_speed > 20:
            forecast = "Clear with strong winds"
            potential_impact = "Dangerous winds may occur."
        elif humidity > 80 and wind_speed < 5:
            forecast = "Rain"
            potential_impact = "Heavy rainfall expected."
        elif temperature > 25 and humidity < 80:
            forecast = "Partly Cloudy"
            potential_impact = "Mild conditions, good weather."
        else:
            forecast = "Cloudy"
            potential_impact = "No significant weather events expected."

        st.write(f"Forecast: {forecast}")
        st.write(f"Potential Impact: {potential_impact}")

    # Hourly weather forecast
    hourly_data = data.get("hourly", {})
    if hourly_data:
        times = hourly_data["time"]
        temperatures = hourly_data["temperature_2m"]
        humidities = hourly_data["relative_humidity_2m"]
        wind_speeds = hourly_data["wind_speed_10m"]

        # Create plots with Plotly Express
        temp_fig = px.line(x=times, y=temperatures, labels={'x': 'Time', 'y': 'Temperature (°C)'}, title='Temperature over Time')
        st.plotly_chart(temp_fig)

        humidity_fig = px.line(x=times, y=humidities, labels={'x': 'Time', 'y': 'Humidity (%)'}, title='Humidity over Time')
        st.plotly_chart(humidity_fig)

        wind_fig = px.line(x=times, y=wind_speeds, labels={'x': 'Time', 'y': 'Wind Speed (km/h)'}, title='Wind Speed over Time')
        st.plotly_chart(wind_fig)
        # Create two columns layout
    # Hourly weather forecast
    hourly_data = data.get("hourly", {})
    if hourly_data:
        times = hourly_data["time"]
        temperatures = hourly_data["temperature_2m"]
        humidities = hourly_data["relative_humidity_2m"]
        wind_speeds = hourly_data["wind_speed_10m"]

        # Calculate average values
        avg_temperature = sum(temperatures) / len(temperatures)
        avg_humidity = sum(humidities) / len(humidities)
        avg_wind_speed = sum(wind_speeds) / len(wind_speeds)

        # Donut Chart Function
        def make_donut(input_response, input_unit, input_color):
            if input_color == 'blue':
                chart_color = ['#29b5e8', '#155F7A']
            if input_color == 'green':
                chart_color = ['#27AE60', '#12783D']
            if input_color == 'orange':
                chart_color = ['#F39C12', '#875A12']
            if input_color == 'red':
                chart_color = ['#E74C3C', '#781F16']

            source = pd.DataFrame({
                "Topic": ['', input_unit],
                "% value": [100-input_response, input_response]
            })
            source_bg = pd.DataFrame({
                "Topic": ['', input_unit],
                "% value": [100, 0]
            })

            plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
                theta="% value",
                color= alt.Color("Topic:N",
                                scale=alt.Scale(
                                    domain=[input_unit, ''],
                                    range=chart_color),
                                legend=None),
            ).properties(width=300, height=300)

            # Display only the value inside the donut with larger font size
            text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(
                text=alt.value(f'{input_response:.1f} {input_unit}'))
            plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
                theta="% value",
                color= alt.Color("Topic:N",
                                scale=alt.Scale(
                                    domain=[input_unit, ''],
                                    range=chart_color),
                                legend=None),
            ).properties(width=300, height=300)
            return plot_bg + plot + text

        # Display donut charts with average values
        st.subheader("Weather Data Donut Charts")

        # Temperature Donut Chart
        st.write("Average Temperature")
        st.altair_chart(make_donut(avg_temperature, '°C', 'blue'), use_container_width=True)

        # Humidity Donut Chart
        st.write("Average Humidity")
        st.altair_chart(make_donut(avg_humidity, '%', 'green'), use_container_width=True)

        # Wind Speed Donut Chart
        st.write("Average Wind Speed")
        st.altair_chart(make_donut(avg_wind_speed, 'km/h', 'orange'), use_container_width=True)


else:
    st.write(f"Failed to fetch data from API. Status code: {response.status_code}")
