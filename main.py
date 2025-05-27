from mcp.server.fastmcp import FastMCP
import sys
sys.path.append(".")  # Ensure current directory is in sys.path for local imports

import requests

mcp = FastMCP("Weather Service")  # Instantiate FastMCP to use its decorators

def fetch_weather_from_claude(location):
    """
    Fetch weather data from Claude desktop API for the given location.
    """
    try:
        # Adjust the URL/port/path as per your Claude desktop API
        response = requests.get(f"http://localhost:5001/weather", params={"location": location}, timeout=5)
        response.raise_for_status()
        data = response.json()
        # Expected keys: temperature, humidity, condition
        return {
            "temperature": data.get("temperature", "N/A"),
            "humidity": data.get("humidity", "N/A"),
            "condition": data.get("condition", "N/A")
        }
    except Exception as e:
        return {
            "temperature": "N/A",
            "humidity": "N/A",
            "condition": f"Error fetching data: {e}"
        }

@mcp.tool()
def get_weather(location: str):
    """
    Get the current weather for a given location.
    """
    weather = fetch_weather_from_claude(location)
    return {
        f"Weather in {location}": {
            "Temperature": weather["temperature"],
            "Humidity": weather["humidity"],
            "Condition": weather["condition"]
        }
    }

@mcp.resource("weather://{location}")
def get_weather_resource(location: str):
    """
    Provide weather data as a resource.
    """
    weather = fetch_weather_from_claude(location)
    return {
        f"Weather data for {location}": {
            "Temperature": weather["temperature"],
            "Humidity": weather["humidity"],
            "Condition": weather["condition"]
        }
    }

@mcp.prompt()
def get_weather_report(location: str):
    """
    Create a prompt for the user to get a weather report.
    """
    weather = fetch_weather_from_claude(location)
    return (
        f"Weather report for {location}:\n"
        f"- Temperature: {weather['temperature']}\n"
        f"- Humidity: {weather['humidity']}\n"
        f"- Condition: {weather['condition']}"
    )

if __name__ == "__main__":
    mcp.run(transport="sse", port=3001)
