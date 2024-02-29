# Weather Worldwide

## Introduction
Weather Worldwide is an innovative weather forecasting application built using Streamlit, providing users with real-time weather data across a broad selection of global locations. It integrates OpenWeatherMap for weather data, Vertex AI for advanced data processing, and DeepL for multilingual support, offering a user-friendly interface for accessing accurate weather forecasts.

## Features
- **Global Weather Forecasts**: Access real-time weather data for cities across various countries.
- **Multilingual Support**: Translate weather information into multiple languages using DeepL.
- **Custom Weather Details**: Users can select specific weather details they are interested in, such as temperature, humidity, cloud cover, precipitation, and wind speed/direction.
- **Interactive UI**: Streamlit-powered interface for an engaging user experience.
- **Model Selection**: Choose between different models (Text Bison, Gemini Pro) for processing weather data.
- **Error Handling**: Graceful error handling for issues like API connectivity problems, providing a smooth user experience.


##Set Up API Keys and Credentials**
    - Obtain and set up API keys for OpenWeatherMap and DeepL.
    - Set the Google Cloud credentials by placing the `key.json` file in your project directory and referencing it in the environment variable `GOOGLE_APPLICATION_CREDENTIALS`.
    - Update `PROJECT_ID`, `REGION`, and `BUCKET_URI` with your Google Cloud configurations for Vertex AI.


## Usage
- Use the sidebar to select a country and city, choose the language for the weather forecast, and select the weather details you wish to view.
- Click the "Give me the Weather details!" button to retrieve and display the weather forecast.
- Optionally, change the underlying model used for processing the weather data via the sidebar.

## Technologies Used
- **Streamlit**: For creating the interactive web application.
- **OpenWeatherMap API**: For fetching real-time weather data.
- **Vertex AI**: For advanced data processing using machine learning models.
- **DeepL API**: For translating the weather data into different languages.
- **Google Cloud**: For cloud services and infrastructure.

## Acknowledgments
- OpenWeatherMap for providing the weather data API.
- DeepL for the translation services.


