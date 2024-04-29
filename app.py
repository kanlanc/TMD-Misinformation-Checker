import streamlit as st
import requests
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import anthropic
from matplotlib.colors import ListedColormap


memory_chat = {}


# Function to send text to Claude API for summarization and translation
def summarize_and_translate(text, memory_chat):

    # Replace with your actual API key  
    api_key = "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"

    client = anthropic.Anthropic(api_key=api_key)


    if text in memory_chat:
        return memory_chat[text]

    print(memory_chat)

    message = client.messages.create(
        model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Your gonna act as a fake news aggregator model. Without any extra unnecessary wording, Your just a mockup and randomly gonna decide if your gonna reply with the website or say this piece of text is true. I am gonna be sending you a piece of text and your meant to respond with "+ "Yes, this is true and can be found at the restoftheworld.com" + "website."
                        },
                        {
                            "type": "text",
                            "text": text
                        }
                    ],
                }
            ],
    )
    print(message.content)

    


    return message.content[0].text

# Function to visualize India map with states highlighted based on threshold
def visualize_india_map(data):
    admin_boundaries = gpd.read_file("india_states.shp")
    print(admin_boundaries.info())

    # Access the geometry column
    geometries = admin_boundaries.geometry

    # Access the attribute columns
    attributes = admin_boundaries.drop('geometry', axis=1)

    # Create a plot
    fig, ax = plt.subplots(figsize=(10, 10))

    # Merge the admin_boundaries GeoDataFrame with the data
    admin_boundaries["value"] = admin_boundaries["ST_NM"].map(data)

    # Plot the admin_boundaries with the color based on the "value" column
    # admin_boundaries.plot(column="value", cmap="RdYlGn", linewidth=0.8, edgecolor="0.8", ax=ax)
    bins = [0, 10,16, admin_boundaries["value"].max()]
    labels = ["Low", "Medium", "High"]
    admin_boundaries["value_cat"] = pd.cut(admin_boundaries["value"], bins=bins, labels=labels)

    # Define a custom colormap with three colors
    colors = ["green", "yellow", "red"]
    cmap = ListedColormap(colors)

    # Plot the admin_boundaries with the color based on the "value_cat" column
    admin_boundaries.plot(column="value_cat", cmap=cmap, linewidth=0.8, edgecolor="0.8", ax=ax)
    # Iterate over each geometry and add its name as a label
    for idx, row in admin_boundaries.iterrows():
        centroid = row.geometry.centroid
        name = row['ST_NM']
        ax.annotate(text=name, xy=(centroid.x, centroid.y), ha='center', va='center', fontsize=6, color="black")

    # Remove the axis
    plt.axis("off")

    # Display the plot using Streamlit
    st.pyplot(fig)
# Streamlit app
def main():
    st.title("Text Summarization and India Map Visualization")
    
    # Text input
    text = st.text_area("Enter the text to summarize and translate")
    
    
    if st.button("Is this news true?"):
        if text and text not in memory_chat:
            # Summarize and translate text using Claude API
            summary = summarize_and_translate(text,memory_chat)

            memory_chat[text] = summary
            
            # Display the summary
            st.subheader("Summary")
            st.write(summary)
        else:
            st.warning("Please enter both text and API key.")
    
    # India map visualization
    st.subheader("India Map Visualization")
    data = {
  "Andaman and Nicobar Islands": 7,
  "Andhra Pradesh": 9,
  "Arunachal Pradesh": 3,
  "Assam": 11,
  "Bihar": 12,
  "Chandigarh": 2,
  "Chhattisgarh": 8,
  "Dadra and Nagar Haveli and Daman and Diu": 1,
  "Delhi": 16,
  "Goa": 5,
  "Gujarat": 14,
  "Haryana": 13,
  "Himachal Pradesh": 6,
  "Jammu and Kashmir": 7,
  "Jharkhand": 9,
  "Karnataka": 10,
  "Kerala": 12,
  "Ladakh": 2,
  "Lakshadweep": 1,
  "Madhya Pradesh": 6,
  "Maharashtra": 18,
  "Manipur": 4,
  "Meghalaya": 3,
  "Mizoram": 2,
  "Nagaland": 3,
  "Odisha": 11,
  "Puducherry": 2,
  "Punjab": 10,
  "Rajasthan": 20,
  "Sikkim": 1,
  "Tamil Nadu": 15,
  "Telangana": 8,
  "Tripura": 4,
  "Uttar Pradesh": 25,
  "Uttarakhand": 5,
  "West Bengal": 8
}
    visualize_india_map(data)

    memory = []

if __name__ == "__main__":
    main()


