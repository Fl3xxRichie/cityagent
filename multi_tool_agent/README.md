# Comprehensive City Agent

This project implements a sophisticated AI agent capable of providing a wide range of city-related information, including weather, time, general city details, comparisons between cities, weather forecasts, and travel insights. It leverages an internal database for quick access to common queries and integrates with Google Search for broader information retrieval. Built using the Google Agent Development Kit (ADK), this agent demonstrates a multi-tool approach to information synthesis.

## Features

*   **🌤️ Current Weather:** Get detailed weather conditions, temperature (Celsius/Fahrenheit), humidity, wind speed, pressure, visibility, UV index, air quality, and real-time alerts for supported cities.
*   **🕐 Current Time:** Retrieve the current time in various formats (standard, business, ISO, relative) for cities across different timezones.
*   **🏙️ City Information:** Access comprehensive data about cities, including population, coordinates, currency, language, and timezone.
*   **🔄 City Comparisons:** Compare two cities based on their weather conditions or current time differences.
*   **📅 Weather Forecasts:** Obtain multi-day weather forecasts for supported cities.
*   **✈️ Travel Information:** Get basic travel insights between two cities, including approximate distance and time zone differences.
*   **🔍 Internal Database Search:** Efficiently search for cities within the agent's predefined database.
*   **🌍 Web Search Integration:** Utilizes Google Search as a fallback mechanism to answer queries not covered by the internal database, ensuring comprehensive information retrieval.

## Setup

Follow these steps to set up and run the Comprehensive City Agent on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### 1. Clone the Repository (if applicable)

If you haven't already, clone this repository to your local machine:

```bash
git clone [repository_url]
cd multi_tool_agent
```
*(Note: Replace `[repository_url]` with the actual URL of your repository.)*

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies and avoid conflicts with other Python projects.

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

*   **On macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```
*   **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```

### 4. Install Dependencies

Once the virtual environment is active, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

The agent requires a Google API Key for web search functionality.

1.  Create a `.env` file in the `multi_tool_agent/` directory (if it doesn't already exist).
2.  Add your Google API Key to this file:

    ```
    GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
    GOOGLE_GENAI_USE_VERTEXAI=FALSE
    ```
    Replace `YOUR_GOOGLE_API_KEY` with your actual Google API Key. You can obtain one from the Google Cloud Console or Google AI Studio.

## Usage

To run the agent and interact with it, you have a few options:

*   **Run the Agent Development UI:**
    ```bash
    adk web
    ```
    This will launch a local web interface where you can interact with and test your agent.

*   **Run the Agent Directly:**
    ```bash
    adk run agent
    ```
    This command executes the agent directly.

The `agent.py` script also includes a comprehensive testing suite that demonstrates various queries and the agent's capabilities. You can modify the `if __name__ == "__main__":` block in `agent.py` to add your own queries.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
