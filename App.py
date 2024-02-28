import os
from langchain_community.utilities import OpenWeatherMapAPIWrapper
import streamlit as st
import vertexai
from langchain_google_vertexai import VertexAI
from langchain import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import numpy as np

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

weather_data = weather.run("Columbus")

st.title("Weather Finder")
st.sidebar.title("Please select your interest:")
Temperature_Box = st.sidebar.checkbox(label="Temperature", value=True, disabled=True)
Humidity_Box = st.sidebar.checkbox(label="Humidity") 
Cloud_Cover_Box = st.sidebar.checkbox(label="Cloud Cover")
Percipitation_Box = st.sidebar.checkbox(label="Percipitation")
Wind_Box = st.sidebar.checkbox(label="Wind Speed/Direction")

generate_result = st.sidebar.button("Tell Me!")
if generate_result:
    #Selecting the what the user wants to see using mask
    user_wants = np.array([Temperature_Box, Humidity_Box, Cloud_Cover_Box, Percipitation_Box, Wind_Box])
    strings= np.array(["Temperature", "Humidity", "Cloud Cover", "Percipitation", "Wind Speed/Direction"])
    selected_strings = strings[user_wants]

    #Depending on what they want, we join the strings correclty to pass to LLM in a good format
    if len(selected_strings) > 2:
        output = ", ".join(selected_strings[:-1]) + " and " + selected_strings[-1] #if we have more than 2 we want to add "and" for the last
    elif len(selected_strings) == 2:
        output = " and ".join(selected_strings) #if we have only 2 we want to add "and" 
    else:
        output = selected_strings[0] # do nothing 

    prompt_template_weather = PromptTemplate(
        input_variables=['output', 'weather_data'],
        template= 'The user wants to know the {output} about the following data. Here is the data: {weather_data}. Please reply with the location name and the requested data.'
        )
        
        #Create Prompt for the LLM. Note we pass the requests in output and the weather data as a string. 
    
    chain = LLMChain(llm=llm1, prompt=prompt_template_weather) #Create our chain and print to Streamlit
    result = chain.run(output=output, weather_data=weather_data)
    st.write(result)