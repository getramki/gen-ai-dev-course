from mcp import Server
import asyncio
import logging
import json
from typing import Dict, Optional
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create weather server
server = Server("weather-server")

# Mock weather data for demonstration
WEATHER_DATA = {
    "new york": {"temp": 22, "condition": "Sunny", "humidity": 65, "wind": 8},
    "london": {"temp": 15, "condition": "Cloudy", "humidity": 78, "wind": 12},
    "tokyo": {"temp": 28, "condition": "Partly Cloudy", "humidity": 72, "wind": 6},
    "sydney": {"temp": 25, "condition": "Rainy", "humidity": 85, "wind": 15},
    "paris": {"temp": 18, "condition": "Overcast", "humidity": 70, "wind": 10},
    "mumbai": {"temp": 32, "condition": "Hot", "humidity": 80, "wind": 5},
    "toronto": {"temp": 12, "condition": "Snow", "humidity": 60, "wind": 20}
}

@server.tool()
async def get_weather(location: str) -> Dict:
    """Get current weather information for a location"""
    try:
        location_key = location.lower().strip()
        
        if location_key in WEATHER_DATA:
            weather = WEATHER_DATA[location_key].copy()
            weather["location"] = location.title()
            weather["timestamp"] = "2024-01-15 10:00:00"
            
            logger.info(f"Retrieved weather for {location}")
            return weather
        else:
            # Generate random weather for unknown locations
            weather = {
                "location": location.title(),
                "temp": random.randint(10, 35),
                "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]),
                "humidity": random.randint(40, 90),
                "wind": random.randint(5, 25),
                "timestamp": "2024-01-15 10:00:00",
                "note": "Simulated data for unknown location"
            }
            
            logger.info(f"Generated simulated weather for {location}")
            return weather
            
    except Exception as e:
        logger.error(f"Error getting weather for {location}: {e}")
        raise ValueError(f"Failed to get weather data: {str(e)}")

@server.tool()
async def get_forecast(location: str, days: Optional[int] = 3) -> Dict:
    """Get weather forecast for multiple days"""
    try:
        if days < 1 or days > 7:
            raise ValueError("Forecast days must be between 1 and 7")
        
        location_key = location.lower().strip()
        base_weather = WEATHER_DATA.get(location_key, {
            "temp": 20, "condition": "Variable", "humidity": 65, "wind": 10
        })
        
        forecast = {
            "location": location.title(),
            "days": days,
            "forecast": []
        }
        
        conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Overcast"]
        
        for day in range(days):
            day_weather = {
                "day": day + 1,
                "date": f"2024-01-{15 + day}",
                "temp_high": base_weather["temp"] + random.randint(-5, 5),
                "temp_low": base_weather["temp"] - random.randint(5, 10),
                "condition": random.choice(conditions),
                "humidity": base_weather["humidity"] + random.randint(-10, 10),
                "wind": base_weather["wind"] + random.randint(-5, 5)
            }
            forecast["forecast"].append(day_weather)
        
        logger.info(f"Generated {days}-day forecast for {location}")
        return forecast
        
    except Exception as e:
        logger.error(f"Error getting forecast for {location}: {e}")
        raise ValueError(f"Failed to get forecast: {str(e)}")

@server.tool()
async def compare_weather(location1: str, location2: str) -> Dict:
    """Compare weather between two locations"""
    try:
        weather1 = await get_weather(location1)
        weather2 = await get_weather(location2)
        
        comparison = {
            "location1": weather1,
            "location2": weather2,
            "comparison": {
                "temperature_diff": weather1["temp"] - weather2["temp"],
                "warmer_location": location1 if weather1["temp"] > weather2["temp"] else location2,
                "humidity_diff": weather1["humidity"] - weather2["humidity"],
                "wind_diff": weather1["wind"] - weather2["wind"]
            }
        }
        
        logger.info(f"Compared weather between {location1} and {location2}")
        return comparison
        
    except Exception as e:
        logger.error(f"Error comparing weather: {e}")
        raise ValueError(f"Failed to compare weather: {str(e)}")

@server.tool()
async def weather_alert(location: str, condition: str) -> str:
    """Check if current weather matches alert condition"""
    try:
        weather = await get_weather(location)
        current_condition = weather["condition"].lower()
        alert_condition = condition.lower()
        
        if alert_condition in current_condition:
            message = f"⚠️ WEATHER ALERT: {condition} conditions detected in {location}!"
        else:
            message = f"✅ No {condition} alert for {location}. Current condition: {weather['condition']}"
        
        logger.info(f"Weather alert check for {location}: {condition}")
        return message
        
    except Exception as e:
        logger.error(f"Error checking weather alert: {e}")
        raise ValueError(f"Failed to check weather alert: {str(e)}")

async def main():
    """Run the weather MCP server"""
    logger.info("Starting Weather MCP Server...")
    
    print("🌤️ Weather MCP Server is ready!")
    print("\nAvailable tools:")
    for tool in server.tools:
        print(f"  - {tool.name}: {tool.description}")
    
    print("\nExample usage:")
    print("  await get_weather('New York')")
    print("  await get_forecast('London', 5)")
    print("  await compare_weather('Tokyo', 'Sydney')")
    print("  await weather_alert('Mumbai', 'hot')")
    
    # Keep server running
    print("\nServer is running... Press Ctrl+C to stop")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Weather server stopped!")

if __name__ == "__main__":
    asyncio.run(main())