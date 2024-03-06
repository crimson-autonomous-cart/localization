from geopy import distance
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Read coordinates from the file
def read_coordinates(filename):
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("Latitude:") and "Long:" in line:
                parts = line.split()
                latitude = float(parts[1])
                longitude = float(parts[3])
                yield latitude, longitude

# Setting Min/Max Longitude & Latitude by Hardaway Hall
min_lat = 33.212196
max_lat = 33.214260
min_lon = -87.545644
max_lon = -87.543037

# Define the boundary square
boundary_square = {
    'min_lat': min_lat,
    'max_lat': max_lat,
    'min_lon': min_lon,
    'max_lon': max_lon
}
# Calculate midpoints
mid_lat = (boundary_square['min_lat'] + boundary_square['max_lat']) / 2
mid_lon = (boundary_square['min_lon'] + boundary_square['max_lon']) / 2

# Define quadrants
quadrants = {
    'NW': {'min_lat': mid_lat, 'max_lat': boundary_square['max_lat'], 'min_lon': boundary_square['min_lon'], 'max_lon': mid_lon},
    'NE': {'min_lat': mid_lat, 'max_lat': boundary_square['max_lat'], 'min_lon': mid_lon, 'max_lon': boundary_square['max_lon']},
    'SW': {'min_lat': boundary_square['min_lat'], 'max_lat': mid_lat, 'min_lon': boundary_square['min_lon'], 'max_lon': mid_lon},
    'SE': {'min_lat': boundary_square['min_lat'], 'max_lat': mid_lat, 'min_lon': mid_lon, 'max_lon': boundary_square['max_lon']}
}

# Assign track coordinates to quadrants ('NW':[], 'NE':[], etc..)
quadrant_tracks = {quadrant: [] for quadrant in quadrants}

# Read track coordinates from the file and assign them to quadrants
with open("output_data1.txt", "r") as file:
    for line in file:
        if line.startswith("Latitude:") and "Long:" in line:
            parts = line.split()
            latitude = float(parts[1])
            longitude = float(parts[3])
            # Determine which quadrant the coordinate belongs to
            for quadrant, boundary in quadrants.items():
                if boundary['min_lat'] <= latitude <= boundary['max_lat'] and boundary['min_lon'] <= longitude <= boundary['max_lon']:
                    quadrant_tracks[quadrant].append((latitude, longitude))
                    break  # No need to check other quadrants

# Print the number of coordinates in each quadrant (for verification)
for quadrant, tracks in quadrant_tracks.items():
    print(f"Quadrant {quadrant}: {len(tracks)} coordinates")


# Function to check if robot is on track within a certain tolerance
def is_on_track(lat, lon, tolerance=2):
    # Determine the quadrant based on the robot's location
    for quadrant, bounds in quadrants.items():
        #print("CHECKING ROBOT IN QUADRANT: ", quadrant)
        if bounds['min_lat'] <= lat <= bounds['max_lat'] and bounds['min_lon'] <= lon <= bounds['max_lon']:
            #print("KART IS IN '" + quadrant + "' QUADRANT!")
            # The robot's location is within this quadrant
            # Check the track coordinates in this quadrant
            for track_lat, track_lon in quadrant_tracks[quadrant]:
                dist_meters = distance.distance((lat, lon), (track_lat, track_lon)).m
                if dist_meters <= tolerance:
                    return True
            break  # No need to check other quadrants if the robot is found in one
    return False

# Read robot coordinates from the file
robot_coordinates = list(read_coordinates("robots_coordinates.txt"))  # Read all coordinates

# Checks if the Kart is on or off Track
for robot_lat, robot_lon in robot_coordinates:
    if is_on_track(robot_lat, robot_lon):
        print("Kart is on track.")
    else:
        print("Kart is off track.")

#------------------------------------- Plots Kart Movement on Track -----------------------------------------------------------------------------

# Define function to plot quadrants, data points, and robot location with zooming
def plot_quadrants_and_robot_zoom(quadrants, quadrant_tracks, robot_location, ax=None):
    if ax is None:
        fig, ax = plt.subplots()

    # Plot boundary square
    ax.plot([boundary_square['min_lon'], boundary_square['max_lon'], boundary_square['max_lon'], boundary_square['min_lon'], boundary_square['min_lon']],
             [boundary_square['min_lat'], boundary_square['min_lat'], boundary_square['max_lat'], boundary_square['max_lat'], boundary_square['min_lat']],
             color='blue', label='Boundary Square')

    # Plot quadrants
    for quadrant, bounds in quadrants.items():
        ax.plot([bounds['min_lon'], bounds['max_lon'], bounds['max_lon'], bounds['min_lon'], bounds['min_lon']],
                 [bounds['min_lat'], bounds['min_lat'], bounds['max_lat'], bounds['max_lat'], bounds['min_lat']],
                 label=quadrant)

    # Plot data points
    for quadrant, tracks in quadrant_tracks.items():
        for lat, lon in tracks:
            ax.scatter(lon, lat, color='red', label=f'Data in {quadrant}')

    # Plot robot location
    ax.scatter(robot_location['lon'], robot_location['lat'], color='green', label='Robot Location')

    # Get minimum and maximum latitude and longitude values of the entire boundary square
    min_lat = boundary_square['min_lat']
    max_lat = boundary_square['max_lat']
    min_lon = boundary_square['min_lon']
    max_lon = boundary_square['max_lon']

    # Set plot limits with padding
    padding = 0.0005  # Adjust as needed
    ax.set_xlim(min_lon - padding, max_lon + padding)

    # Calculate aspect ratio based on the boundaries of the entire boundary square
    aspect_ratio = (max_lon - min_lon) / (max_lat - min_lat)

    # Set y-axis limits based on the aspect ratio
    y_center = (max_lat + min_lat) / 2
    y_range = (max_lon - min_lon) / aspect_ratio / 2
    ax.set_ylim(y_center - y_range, y_center + y_range)

    # Set plot labels and legend
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Boundary Square with Quadrants, Data Points, and Robot Location')
    ax.legend()

    # Set aspect ratio
    ax.set_aspect(aspect_ratio)

    # Return the axis
    return ax

def plot_quadrants_and_robot_zoom(quadrants, quadrant_tracks, robot_location, ax=None):
    if ax is None:
        fig, ax = plt.subplots()

    # Read the image file
    background_image = plt.imread("background.png")

    # Define the extent of the image (adjust as needed)
    extent = [boundary_square['min_lon'], boundary_square['max_lon'], boundary_square['min_lat'], boundary_square['max_lat']]

    # Display the background image
    ax.imshow(background_image, extent=extent, aspect='auto')

    # Plot boundary square
    ax.plot([boundary_square['min_lon'], boundary_square['max_lon'], boundary_square['max_lon'], boundary_square['min_lon'], boundary_square['min_lon']],
             [boundary_square['min_lat'], boundary_square['min_lat'], boundary_square['max_lat'], boundary_square['max_lat'], boundary_square['min_lat']],
             color='blue', label='Boundary Square')

    # Plot quadrants
    for quadrant, bounds in quadrants.items():
        ax.plot([bounds['min_lon'], bounds['max_lon'], bounds['max_lon'], bounds['min_lon'], bounds['min_lon']],
                 [bounds['min_lat'], bounds['min_lat'], bounds['max_lat'], bounds['max_lat'], bounds['min_lat']],
                 label=quadrant)

    # Plot data points
    for quadrant, tracks in quadrant_tracks.items():
        for lat, lon in tracks:
            ax.scatter(lon, lat, color='red', label=f'Data in {quadrant}')

    # Plot robot location
    ax.scatter(robot_location['lon'], robot_location['lat'], color='green', label='Robot Location')

    # Get minimum and maximum latitude and longitude values of the entire boundary square
    min_lat = boundary_square['min_lat']
    max_lat = boundary_square['max_lat']
    min_lon = boundary_square['min_lon']
    max_lon = boundary_square['max_lon']

    # Set plot limits with padding
    padding = 0.001  # Adjust as needed
    ax.set_xlim(min_lon - padding, max_lon + padding)

    # Calculate aspect ratio based on the boundaries of the entire boundary square
    aspect_ratio = (max_lon - min_lon) / (max_lat - min_lat)

    # Set y-axis limits based on the aspect ratio
    y_center = (max_lat + min_lat) / 2
    y_range = (max_lon - min_lon) / aspect_ratio / 2
    ax.set_ylim(y_center - y_range, y_center + y_range)

    # Set plot labels and legend
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Boundary Square with Quadrants, Data Points, and Robot Location')

    # Set aspect ratio
    ax.set_aspect(aspect_ratio)

    # Return the axis
    return ax


# Function to update the plot with new robot location
def update_plot_with_new_location(frame):
    try:
        # Read next coordinates from the file
        lat, lon = next(coordinates)
        robot_location['lat'] = lat
        robot_location['lon'] = lon

        # Clear the existing plot
        ax.clear()

        # Plot quadrants, data points, and robot location with zooming
        plot_quadrants_and_robot_zoom(quadrants, quadrant_tracks, robot_location, ax)
    except StopIteration:
        # Stop animation when coordinates are exhausted
        ani.event_source.stop()

# Create initial plot
fig, ax = plt.subplots()

# Initialize robot location
robot_location = {'lat': None, 'lon': None}

# Create animation
coordinates = read_coordinates("robots_coordinates.txt")  # Replace with your file name
ani = FuncAnimation(fig, update_plot_with_new_location, frames=None, interval=1000)

# Show the plot
plt.title("Kart Location Animation")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
