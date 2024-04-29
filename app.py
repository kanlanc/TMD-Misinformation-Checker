import streamlit as st
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import anthropic

# Function to send text to Claude API for summarization and translation
def summarize_and_translate(text):

    # Replace with your actual API key  
    api_key = "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"

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Is this true?"
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
    admin_boundaries.plot(column="value", cmap="RdYlGn", linewidth=0.8, edgecolor="0.8", ax=ax)

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
    
    if st.button("Submit"):
        if text:
            # Summarize and translate text using Claude API
            summary = summarize_and_translate(text)
            
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

if __name__ == "__main__":
    main()


