import streamlit as st
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import anthropic

# Function to send text to Claude API for summarization and translation
def summarize_and_translate(text, api_key):

    # Replace with your actual API key  
    api_key = "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"

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Summarize the text to one point"
                        }
                    ],
                }
            ],
    )
    print(message)
    return message

# Function to visualize India map with states highlighted based on threshold
def visualize_india_map(data):
    india_map = gpd.read_file("india_states.shp")
    india_map["color"] = india_map["STATE_NAME"].map(data)
    india_map.plot(column="color", cmap="RdYlGn", linewidth=0.8, edgecolor="0.8", figsize=(10, 10))
    plt.axis("off")
    st.pyplot(plt)

# Streamlit app
def main():
    st.title("Text Summarization and India Map Visualization")
    
    # Text input
    text = st.text_area("Enter the text to summarize and translate")
    
    if st.button("Submit"):
        if text:
            # Summarize and translate text using Claude API
            summary = summarize_and_translate(text, api_key)
            
            # Display the summary
            st.subheader("Summary")
            st.write(summary)
        else:
            st.warning("Please enter both text and API key.")
    
    # India map visualization
    st.subheader("India Map Visualization")
    data = {
        "Uttar Pradesh": 25,
        "Maharashtra": 18,
        "Bihar": 12,
        "West Bengal": 8,
        "Madhya Pradesh": 6,
        "Tamil Nadu": 15,
        "Rajasthan": 20,
        "Karnataka": 10,
        "Gujarat": 14,
        "Andhra Pradesh": 9
    }
    visualize_india_map(data)

if __name__ == "__main__":
    main()


