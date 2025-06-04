import datetime
import json
from zoneinfo import ZoneInfo
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from google.adk.agents import Agent
from google.adk.tools import google_search  # Built-in tool import
from google.adk.tools.agent_tool import AgentTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Data structures for enhanced functionality
@dataclass
class WeatherAlert:
    type: str
    severity: str
    description: str
    expires: str

@dataclass
class CityInfo:
    name: str
    country: str
    timezone: str
    population: int
    coordinates: tuple
    currency: str
    language: str

# Extended city database with comprehensive information
CITY_DATABASE = {
    "new york": CityInfo(
        name="New York", country="United States", timezone="America/New_York",
        population=8336817, coordinates=(40.7128, -74.0060),
        currency="USD", language="English"
    ),
    "london": CityInfo(
        name="London", country="United Kingdom", timezone="Europe/London",
        population=9648110, coordinates=(51.5074, -0.1278),
        currency="GBP", language="English"
    ),
    "tokyo": CityInfo(
        name="Tokyo", country="Japan", timezone="Asia/Tokyo",
        population=13960000, coordinates=(35.6762, 139.6503),
        currency="JPY", language="Japanese"
    ),
    "lagos": CityInfo(
        name="Lagos", country="Nigeria", timezone="Africa/Lagos",
        population=15388000, coordinates=(6.5244, 3.3792),
        currency="NGN", language="English"
    ),
    "paris": CityInfo(
        name="Paris", country="France", timezone="Europe/Paris",
        population=2165423, coordinates=(48.8566, 2.3522),
        currency="EUR", language="French"
    ),
    "dubai": CityInfo(
        name="Dubai", country="UAE", timezone="Asia/Dubai",
        population=3331420, coordinates=(25.2048, 55.2708),
        currency="AED", language="Arabic"
    ),
    "sydney": CityInfo(
        name="Sydney", country="Australia", timezone="Australia/Sydney",
        population=5312163, coordinates=(-33.8688, 151.2093),
        currency="AUD", language="English"
    ),
    "mumbai": CityInfo(
        name="Mumbai", country="India", timezone="Asia/Kolkata",
        population=20411274, coordinates=(19.0760, 72.8777),
        currency="INR", language="Hindi/English"
    )
}

# Enhanced weather data with more details
WEATHER_DATA = {
    "new york": {
        "condition": "sunny", "temperature_c": 25, "temperature_f": 77,
        "humidity": 60, "wind_speed": 15, "wind_direction": "SW",
        "pressure": 1013.2, "visibility": 10, "uv_index": 6,
        "air_quality": "Good", "feels_like_c": 27, "feels_like_f": 81,
        "alerts": []
    },
    "london": {
        "condition": "cloudy", "temperature_c": 18, "temperature_f": 64,
        "humidity": 75, "wind_speed": 10, "wind_direction": "W",
        "pressure": 1008.5, "visibility": 8, "uv_index": 3,
        "air_quality": "Moderate", "feels_like_c": 16, "feels_like_f": 61,
        "alerts": []
    },
    "tokyo": {
        "condition": "partly cloudy", "temperature_c": 28, "temperature_f": 82,
        "humidity": 65, "wind_speed": 8, "wind_direction": "E",
        "pressure": 1015.1, "visibility": 12, "uv_index": 7,
        "air_quality": "Good", "feels_like_c": 31, "feels_like_f": 88,
        "alerts": []
    },
    "lagos": {
        "condition": "thunderstorms", "temperature_c": 26, "temperature_f": 79,
        "humidity": 94, "wind_speed": 5, "wind_direction": "W",
        "pressure": 1009.8, "visibility": 5, "uv_index": 4,
        "air_quality": "Moderate", "feels_like_c": 28, "feels_like_f": 83,
        "alerts": [{"type": "Thunderstorm", "severity": "moderate", "description": "Scattered thunderstorms expected", "expires": "2025-06-03T20:00:00"}]
    },
    "paris": {
        "condition": "rainy", "temperature_c": 16, "temperature_f": 61,
        "humidity": 80, "wind_speed": 20, "wind_direction": "NW",
        "pressure": 1005.2, "visibility": 6, "uv_index": 2,
        "air_quality": "Good", "feels_like_c": 14, "feels_like_f": 57,
        "alerts": []
    }
}

def get_weather(city: str, detailed: bool = False) -> dict:
    """Retrieves comprehensive weather information for a specified city.
    
    Args:
        city (str): The name of the city
        detailed (bool): Whether to include detailed weather metrics
    
    Returns:
        dict: Weather information with status
    """
    city_lower = city.lower().strip()
    
    if city_lower in WEATHER_DATA:
        weather = WEATHER_DATA[city_lower]
        
        # Basic weather report
        report = (
            f"🌤️ Weather in {city.title()}: {weather['condition'].title()}\n"
            f"🌡️ Temperature: {weather['temperature_c']}°C ({weather['temperature_f']}°F)\n"
            f"🤔 Feels like: {weather['feels_like_c']}°C ({weather['feels_like_f']}°F)\n"
            f"💧 Humidity: {weather['humidity']}%\n"
            f"💨 Wind: {weather['wind_speed']} km/h {weather['wind_direction']}"
        )
        
        if detailed:
            report += (
                f"\n📊 Pressure: {weather['pressure']} hPa\n"
                f"👁️ Visibility: {weather['visibility']} km\n"
                f"☀️ UV Index: {weather['uv_index']}\n"
                f"🏭 Air Quality: {weather['air_quality']}"
            )
        
        # Add weather alerts if any
        if weather['alerts']:
            report += "\n\n⚠️ Weather Alerts:"
            for alert in weather['alerts']:
                report += f"\n• {alert['type']} ({alert['severity']}): {alert['description']}"
        
        return {
            "status": "success",
            "report": report,
            "raw_data": weather if detailed else None
        }
    else:
        available_cities = ", ".join([city.title() for city in WEATHER_DATA.keys()])
        return {
            "status": "error",
            "error_message": f"Weather data for '{city}' not available. Try: {available_cities}. Or I can search the web for it."
        }

def get_current_time(city: str, format_type: str = "standard") -> dict:
    """Returns current time in various formats for a city.
    
    Args:
        city (str): City name
        format_type (str): "standard", "business", "iso", or "relative"
    
    Returns:
        dict: Time information
    """
    city_lower = city.lower().strip()
    
    if city_lower not in CITY_DATABASE:
        available_cities = ", ".join([city.title() for city in CITY_DATABASE.keys()])
        return {
            "status": "error",
            "error_message": f"Time zone data for '{city}' not available. Try: {available_cities}. Or I can search the web for it."
        }
    
    try:
        city_info = CITY_DATABASE[city_lower]
        tz = ZoneInfo(city_info.timezone)
        now = datetime.datetime.now(tz)
        
        formats = {
            "standard": now.strftime("%A, %B %d, %Y at %I:%M:%S %p %Z"),
            "business": now.strftime("%Y-%m-%d %H:%M %Z"),
            "iso": now.isoformat(),
            "relative": f"{now.strftime('%I:%M %p')} (UTC{now.strftime('%z')})"
        }
        
        formatted_time = formats.get(format_type, formats["standard"])
        
        return {
            "status": "success",
            "report": f"🕐 Current time in {city.title()}: {formatted_time}",
            "timestamp": now.isoformat(),
            "timezone": city_info.timezone,
            "utc_offset": now.strftime('%z')
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error getting time for {city}: {str(e)}"
        }

def get_city_info(city: str) -> dict:
    """Get comprehensive information about a city.
    
    Args:
        city (str): City name
        
    Returns:
        dict: City information
    """
    city_lower = city.lower().strip()
    
    if city_lower not in CITY_DATABASE:
        available_cities = ", ".join([city.title() for city in CITY_DATABASE.keys()])
        return {
            "status": "error",
            "error_message": f"City information for '{city}' not available. Try: {available_cities}. Or I can search the web for it."
        }
    
    city_info = CITY_DATABASE[city_lower]
    
    report = (
        f"🏙️ {city_info.name}, {city_info.country}\n"
        f"👥 Population: {city_info.population:,}\n"
        f"🗺️ Coordinates: {city_info.coordinates[0]:.4f}, {city_info.coordinates[1]:.4f}\n"
        f"💰 Currency: {city_info.currency}\n"
        f"🗣️ Language: {city_info.language}\n"
        f"🕐 Timezone: {city_info.timezone}"
    )
    
    return {
        "status": "success",
        "report": report,
        "city_data": city_info.__dict__
    }

def compare_cities(city1: str, city2: str, comparison_type: str = "weather") -> dict:
    """Compare two cities based on weather, time, or general info.
    
    Args:
        city1, city2 (str): Cities to compare
        comparison_type (str): "weather", "time", or "info"
        
    Returns:
        dict: Comparison results
    """
    if comparison_type == "weather":
        weather1 = get_weather(city1)
        weather2 = get_weather(city2)
        
        if weather1["status"] == "error" or weather2["status"] == "error":
            if city1.lower().strip() not in WEATHER_DATA or city2.lower().strip() not in WEATHER_DATA:
                 return {
                    "status": "error",
                    "error_message": f"Weather data missing for one or both cities. I can try a web search for current weather if you'd like."
                }
            return {
                "status": "error",
                "error_message": "Cannot compare - one or both cities have no weather data"
            }
        
        w1 = WEATHER_DATA[city1.lower()]
        w2 = WEATHER_DATA[city2.lower()]
        
        temp_diff = w1["temperature_c"] - w2["temperature_c"]
        humidity_diff = w1["humidity"] - w2["humidity"]
        
        report = (
            f"🌍 Weather Comparison: {city1.title()} vs {city2.title()}\n\n"
            f"{city1.title()}: {w1['temperature_c']}°C, {w1['condition']}\n"
            f"{city2.title()}: {w2['temperature_c']}°C, {w2['condition']}\n\n"
            f"🌡️ Temperature difference: {abs(temp_diff):.1f}°C "
            f"({'warmer' if temp_diff > 0 else 'cooler'} in {city1.title() if temp_diff > 0 else city2.title()})\n"
            f"💧 Humidity difference: {abs(humidity_diff)}% "
            f"({'higher' if humidity_diff > 0 else 'lower'} in {city1.title() if humidity_diff > 0 else city2.title()})"
        )
        
        return {"status": "success", "report": report}
    
    elif comparison_type == "time":
        time1 = get_current_time(city1)
        time2 = get_current_time(city2)
        
        if time1["status"] == "error" or time2["status"] == "error":
            if city1.lower().strip() not in CITY_DATABASE or city2.lower().strip() not in CITY_DATABASE:
                return {
                    "status": "error",
                    "error_message": "Timezone data unavailable for one or both cities in my database. I can search the web for current times."
                }
            return {
                "status": "error", 
                "error_message": "Cannot compare - timezone data unavailable for one or both cities"
            }
        
        # Calculate time difference
        tz1 = ZoneInfo(CITY_DATABASE[city1.lower()].timezone)
        tz2 = ZoneInfo(CITY_DATABASE[city2.lower()].timezone)
        now1 = datetime.datetime.now(tz1)
        now2 = datetime.datetime.now(tz2)
        
        diff = (now1.utcoffset() - now2.utcoffset()).total_seconds() / 3600
        
        report = (
            f"🕐 Time Comparison: {city1.title()} vs {city2.title()}\n\n"
            f"{city1.title()}: {now1.strftime('%I:%M %p %Z')}\n"
            f"{city2.title()}: {now2.strftime('%I:%M %p %Z')}\n\n"
            f"⏰ Time difference: {abs(diff):.0f} hours "
            f"({city1.title() if diff > 0 else city2.title()} is ahead)"
        )
        
        return {"status": "success", "report": report}
    
    else:
        info1 = get_city_info(city1)
        info2 = get_city_info(city2)
        if info1["status"] == "error" or info2["status"] == "error":
            return {
                "status": "error",
                "error_message": f"City info missing for comparison. I can try searching the web for {city1} or {city2} if they are not in my database."
            }
        return {
            "status": "error",
            "error_message": "Invalid comparison type or not fully implemented for 'info'. Use 'weather' or 'time', or I can search for general info on both."
        }

def get_weather_forecast(city: str, days: int = 3) -> dict:
    """Get weather forecast for upcoming days (mock implementation).
    
    Args:
        city (str): City name
        days (int): Number of days to forecast (1-7)
        
    Returns:
        dict: Forecast information
    """
    city_lower = city.lower().strip()
    
    if city_lower not in WEATHER_DATA:
        return {
            "status": "error",
            "error_message": f"Weather forecast data for '{city}' not available in my database. I can try to search the web for it."
        }
    
    if days < 1 or days > 7:
        return {
            "status": "error",
            "error_message": "Forecast days must be between 1 and 7"
        }
    
    # Mock forecast data
    base_weather = WEATHER_DATA[city_lower]
    forecast_conditions = ["sunny", "partly cloudy", "cloudy", "rainy", "thunderstorms"]
    
    report = f"📅 {days}-Day Weather Forecast for {city.title()}:\n\n"
    
    for i in range(days):
        date = datetime.date.today() + datetime.timedelta(days=i+1)
        temp_variation = (-2 + i) if i < 3 else (1 - i)
        temp_c = base_weather["temperature_c"] + temp_variation
        temp_f = int(temp_c * 9/5 + 32)
        condition = forecast_conditions[i % len(forecast_conditions)]
        
        report += f"📆 {date.strftime('%A, %B %d')}: {condition.title()}, {temp_c}°C ({temp_f}°F)\n"
    
    return {
        "status": "success",
        "report": report,
        "forecast_days": days
    }

def search_cities_in_database(query: str) -> dict:
    """Search for cities matching a query within the internal database.
    
    Args:
        query (str): Search term (city name, country, or partial match)
        
    Returns:
        dict: Matching cities
    """
    query_lower = query.lower().strip()
    matches = []
    
    for city_key, city_info in CITY_DATABASE.items():
        if (query_lower in city_info.name.lower() or 
            query_lower in city_info.country.lower() or
            query_lower in city_key):
            matches.append({
                "name": city_info.name,
                "country": city_info.country,
                "population": city_info.population
            })
    
    if matches:
        report = f"🔍 Found {len(matches)} cities in my database matching '{query}':\n\n"
        for match in matches:
            report += f"• {match['name']}, {match['country']} (Pop: {match['population']:,})\n"
        
        return {
            "status": "success",
            "report": report,
            "matches": matches,
            "count": len(matches)
        }
    else:
        return {
            "status": "error",
            "error_message": f"No cities found in my database matching '{query}'. I can perform a web search if you'd like."
        }

def get_travel_info(origin: str, destination: str) -> dict:
    """Get basic travel information between two cities.
    
    Args:
        origin, destination (str): Origin and destination cities
        
    Returns:
        dict: Travel information
    """
    origin_lower = origin.lower().strip()
    dest_lower = destination.lower().strip()
    
    if origin_lower not in CITY_DATABASE or dest_lower not in CITY_DATABASE:
        return {
            "status": "error",
            "error_message": "Travel info requires both cities to be in our database. I can try a web search for information about these cities."
        }
    
    origin_info = CITY_DATABASE[origin_lower]
    dest_info = CITY_DATABASE[dest_lower]
    
    # Calculate approximate distance (simplified)
    import math
    
    lat1, lon1 = math.radians(origin_info.coordinates[0]), math.radians(origin_info.coordinates[1])
    lat2, lon2 = math.radians(dest_info.coordinates[0]), math.radians(dest_info.coordinates[1])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    distance_km = 6371 * c  # Earth's radius in km
    
    # Time zone difference
    origin_tz = ZoneInfo(origin_info.timezone)
    dest_tz = ZoneInfo(dest_info.timezone)
    now_origin = datetime.datetime.now(origin_tz)
    now_dest = datetime.datetime.now(dest_tz)
    
    time_diff = (now_dest.utcoffset() - now_origin.utcoffset()).total_seconds() / 3600
    
    report = (
        f"✈️ Travel Info: {origin.title()} → {dest.title()}\n\n"
        f"📏 Distance: ~{distance_km:.0f} km ({distance_km*0.621371:.0f} miles)\n"
        f"🕐 Time difference: {abs(time_diff):.0f} hours "
        f"({'ahead' if time_diff > 0 else 'behind'} in {dest.title()})\n"
        f"💱 Currency: {origin_info.currency} → {dest_info.currency}\n"
        f"🗣️ Language: {origin_info.language} → {dest_info.language}"
    )
    
    return {
        "status": "success",
        "report": report,
        "distance_km": round(distance_km),
        "time_difference_hours": time_diff
    }

# Create separate agents for different functionalities

# 1. Custom functions agent (handles database operations)
custom_functions_agent = Agent(
    name="city_functions_agent",
    model="gemini-2.0-flash",
    description="Handles city database operations like weather, time, and city info",
    instruction=(
        "You handle city database operations. Use the available functions to provide "
        "weather, time, city information, comparisons, forecasts, and travel info. "
        "If data is not available in the database, inform the user that web search is needed."
    ),
    tools=[
        get_weather, get_current_time, get_city_info, compare_cities,
        get_weather_forecast, search_cities_in_database, get_travel_info
    ]
)

# 2. Google search agent (handles web searches)
search_agent = Agent(
    name="web_search_agent",
    model="gemini-2.0-flash",
    description="Handles web searches for information not in the database",
    instruction=(
        "You are a web search specialist. Use Google Search to find information "
        "about cities, weather, or any other queries when the data is not available "
        "in the internal database. Provide comprehensive and accurate information."
    ),
    tools=[google_search]
)

# 3. Root agent that coordinates between the two
root_agent = Agent(
    name="comprehensive_city_agent",
    model="gemini-2.0-flash",
    description=(
        "A comprehensive city information agent that provides weather, time, city information, "
        "comparisons, forecasts, travel insights, and can search the web for broader queries."
    ),
    instruction=(
        "You are an advanced city information assistant with the following capabilities:\n\n"
        "🌤️ WEATHER: Provide current weather with detailed metrics, alerts, and forecasts.\n"
        "🕐 TIME: Show current time in multiple formats across different timezones.\n"
        "🏙️ CITY INFO: Share comprehensive city data.\n"
        "🔄 COMPARISONS: Compare cities by weather or time.\n"
        "📅 FORECASTS: Provide weather forecasts.\n"
        "✈️ TRAVEL: Calculate distances and provide travel-related information.\n"
        "🔍 DATABASE SEARCH: Find cities matching user queries within the internal database.\n"
        "🌍 WEB SEARCH: For any information not found in the internal database, or for general knowledge questions.\n\n"
        "WORKFLOW:\n"
        "1. First, try to use the city_functions_agent for database operations\n"
        "2. If the information is not available in the database, use the web_search_agent\n"
        "3. Always be informative, friendly, and use emojis to make responses engaging\n"
        "4. Provide practical insights for comparisons and travel info\n\n"
        "Always prioritize using the database first, then web search as a fallback."
    ),
    tools=[
        AgentTool(agent=custom_functions_agent),
        AgentTool(agent=search_agent)
    ]
)

# Setup for running the agent
APP_NAME = "comprehensive_city_app"
USER_ID = "user123"
SESSION_ID = "session1"

def setup_and_run_agent():
    """Setup and return a runner for the agent."""
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name=APP_NAME, 
        user_id=USER_ID, 
        session_id=SESSION_ID
    )
    
    runner = Runner(
        agent=root_agent, 
        app_name=APP_NAME, 
        session_service=session_service
    )
    
    return runner, session_service

def call_agent(runner, query):
    """Call the agent with a query."""
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    
    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response:", final_response)
            return final_response

# Comprehensive testing suite
if __name__ == "__main__":
    print("🧪 Testing Comprehensive City Agent\n")
    
    # Setup the agent
    runner, session_service = setup_and_run_agent()
    
    # Test 1: Weather in database
    print("1. Detailed Weather Test (Lagos - in DB):")
    call_agent(runner, "What's the detailed weather in Lagos?")
    print("\n" + "="*50 + "\n")

    # Test 2: Weather not in database (should use web search)
    print("2. Weather Test (Berlin - not in DB, should use web search):")
    call_agent(runner, "What's the weather in Berlin?")
    print("\n" + "="*50 + "\n")
    
    # Test 3: City comparison
    print("3. City Comparison Test (New York vs Tokyo - weather):")
    call_agent(runner, "Compare the weather in New York and Tokyo.")
    print("\n" + "="*50 + "\n")
    
    # Test 4: Travel info
    print("4. Travel Information Test (London to Lagos):")
    call_agent(runner, "Tell me about travel from London to Lagos.")
    print("\n" + "="*50 + "\n")
    
    # Test 5: Forecast
    print("5. Weather Forecast Test (Paris, 5 days):")
    call_agent(runner, "What's the 5-day forecast for Paris?")
    print("\n" + "="*50 + "\n")
    
    # Test 6: Database search
    print("6. City Database Search Test:")
    call_agent(runner, "Search your database for cities in the United States.")
    print("\n" + "="*50 + "\n")

    # Test 7: General knowledge (should use web search)
    print("7. General Knowledge Test (should use Google Search):")
    call_agent(runner, "What is the tallest building in Dubai?")
    print("\n" + "="*50 + "\n")

    # Test 8: Unknown city weather (should use web search)
    print("8. Weather for unknown city (should use Google Search):")
    call_agent(runner, "What's the weather like in Addis Ababa?")
    print("\n" + "="*50 + "\n")