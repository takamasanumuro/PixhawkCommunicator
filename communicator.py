#The purpose of this script is to extract Mavlink data being streamed from Ardupilot and sending it to an endpoint on the server.
#It uses MAVSDK-Python to connect to the drone and extract the data via event callbacks.
#Check the MAVSDK-Python documentation to see what other data can be extracted from the drone.
#Check the server API to see which endpoints are available to send data to.

#The shebang line is used to tell the system what interpreter to use to run this script.
#It can fix issues with the script not running properly or importing the wrong packages.
#!/usr/bin/env python3

from mavsdk import System # Package that allows us to connect to the drone and extract data
import asyncio # Package that allows us to run multiple tasks at once
import requests # Package that allows us to send HTTP requests to the server

#Initialize the connection to the drone and start listening for data
async def run():
    # Init the drone
    print("Init the drone")
    drone = System()
    print("Waiting for drone to connect...")
    #Mavproxy must be running and streaming data to the given port first
    #Pay attention whether UDP or TCP is being used
    await drone.connect(system_address="udp://:14550") 
    print("Connected to drone!")

    # Start the tasks. Uncomment the ones you want to use
    #asyncio.ensure_future(print_battery(drone))
    #asyncio.ensure_future(print_telemetry_info(drone))
    asyncio.ensure_future(print_gps_info(drone))

async def print_gps_info(drone):
    #Subscribe to telemetry position
    async for position in drone.telemetry.position():
        print(f"Position: {position.latitude_deg} {position.longitude_deg} {position.relative_altitude_m}")
        #Send request to server
        #!TODO:Make the web request asynchronous to not block the main thread
        #The URL depends if the server is running locally or on a remote device
        url = "http://localhost:5000/api/marker"
        payload = {"latitude": position.latitude_deg, "longitude": position.longitude_deg, "altitude": position.relative_altitude_m}
        headers = {"Content-Type": "application/json"} 
        try:
            response = requests.request("POST", url, headers=headers, json=payload)
            print(response.text)
        except:
            print("Error")

async def print_battery(drone):
    async for battery in drone.telemetry.battery():
        print(f"Battery: {battery.remaining_percent}")

async def print_telemetry_info(drone):

    async for health in drone.telemetry.health():
        print(f"Health info: {health}")

##########################################################


#Boilerplate code to initialize the script using asyncio
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    run_task = asyncio.ensure_future(run())
    loop.run_forever()
    