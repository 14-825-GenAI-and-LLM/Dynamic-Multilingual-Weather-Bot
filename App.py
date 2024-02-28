import os
from langchain_community.utilities import OpenWeatherMapAPIWrapper
import streamlit as st
import vertexai
from langchain_google_vertexai import VertexAI
from langchain import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import numpy as np
import requests

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="key.json" # place the key JSON file in the same folder as your notebook
PROJECT_ID = "gen-ai-llm-14825" # use your project id 
REGION = "us-central1"  #
BUCKET_URI = f"gs://gen-ai-llm-bucket"  # create your own bucket

vertexai.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_URI)

llm1 = VertexAI(
    model_name="text-bison@001",
    max_output_tokens=256,
    temperature=0.5,
    top_p=0.8,
    top_k=40,
    verbose=True,
)

llm2 = VertexAI(
    model_name="gemini-pro",
    max_output_tokens=256,
    temperature=0.5,
    top_p=0.8,
    top_k=40,
    verbose=True,
)

os.environ["OPENWEATHERMAP_API_KEY"] = '5708941459d96133b31f54f2f15bd9aa'

weather = OpenWeatherMapAPIWrapper()

#weather_data = weather.run("Columbus")
st.title("Weather Worldwide")
st.image('weather_logo.png')

###############
# Sidebar for Country selection
countries_and_cities = {
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Pittsburgh', 'Use this to test errors from API :)'],
    'Canada': ['Toronto', 'Vancouver', 'Montreal'],
    'UK': ['London', 'Manchester', 'Birmingham']
}

st.sidebar.title("Please select your location:")
country = st.sidebar.selectbox('Select a country:', list(countries_and_cities.keys()))
cities = countries_and_cities[country]
city = st.sidebar.selectbox('Select a city:', cities)
###############
#Select Weather Boxes
st.sidebar.title("Please select your weather interest:")
Temperature_Box = st.sidebar.checkbox(label="Temperature (Required)", value=True, disabled=True)
Humidity_Box = st.sidebar.checkbox(label="Humidity") 
Cloud_Cover_Box = st.sidebar.checkbox(label="Cloud Cover")
Precipitation_Box = st.sidebar.checkbox(label="Precipitation")
Wind_Box = st.sidebar.checkbox(label="Wind Speed/Direction")
##############
#Select Model
st.sidebar.title("Change the model (optional):")
LLM_choice = st.sidebar.selectbox("Model choice:", ["Text Bison", "Gemini Pro"])


#The following runs after the user selects their desired info. By default, they will get the Temp in New York, USA (prepopulated)
generate_result = st.sidebar.button("Tell Me!")
if generate_result:
    weather_data = None

    #Send API call based on selected country/city. If the try doesn't work with the API, send error message to user
    try:
        weather_data = weather.run(f"{city},{country}")
    # Process weather_data
    except Exception as e:
        st.error(f"\u26A0 An error occurred with the weather API: \"{e}\"  \n\nWe apologize for the inconvenience!  \nPlease try again later.")

    #If an exception was triggered above then weather_data will still be none and this won't run
    if weather_data:
        st.write(f"Getting weather for {city}, {country}.")
    
        # Parse what the user wants to see using mask
        user_wants = np.array([Temperature_Box, Humidity_Box, Cloud_Cover_Box, Precipitation_Box, Wind_Box])
        strings= np.array(["Temperature", "Humidity", "Cloud Cover", "Precipitation", "Wind Speed/Direction"])
        selected_strings = strings[user_wants]

        #Depending on what they want, we join the strings correctly to pass to LLM in a coherent sentence
        if len(selected_strings) > 2:
            output = ", ".join(selected_strings[:-1]) + " and " + selected_strings[-1] #if we have more than 2 we want to add "and" for the last
        elif len(selected_strings) == 2:
            output = " and ".join(selected_strings) #if we have only 2 we want to add "and" 
        else:
            output = selected_strings[0] # do nothing 

        #Provided the sentence from above, we pass it to the prompt template 
        prompt_template_weather = PromptTemplate(
            input_variables=['output', 'weather_data'],
            template= 'The user wants to know the {output} from the following: {weather_data}. This data is in metric units. Please reply with the location name and the requested data.'
            )
            
        
        #Now we access our chain
        if LLM_choice =="Text Bison":
            llm=llm1
        else:
            llm=llm2

        chain = LLMChain(llm=llm, prompt=prompt_template_weather) #Create our chain and print to Streamlit
        result = chain.run(output=output, weather_data=weather_data)
        st.write(result)