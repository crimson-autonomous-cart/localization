"""
Script to visualize route using GPS latitude and longitutude.

Usage:
    python3 gpsMap.py <dataFile.txt>
"""
import cv2
import numpy as np
import sys

# Check that correct number of arguments were passed in
if len(sys.argv) != 2:
    print("Usage: python3 gpsMap.py <dataFile.txt")
    sys.exit(0)

# Read data points from file
data_points = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        lat, lon, header = map(float, line.split()[1::2])
        data_points.append((lat, lon))

# Find minimum and maximum latitude and longitude
min_lat = min(data_points, key=lambda x: x[0])[0]
max_lat = max(data_points, key=lambda x: x[0])[0]
min_lon = min(data_points, key=lambda x: x[1])[1]
max_lon = max(data_points, key=lambda x: x[1])[1]

# Scale the coordinates to fit in an image
scale = 1000  # Adjust this scale factor according to your preference
scaled_points = [(int(scale * (lon - min_lon) / (max_lon - min_lon)), int(scale * (max_lat - lat) / (max_lat - min_lat))) for lat, lon in data_points]

# Create an image with white background
image = np.ones((scale, scale, 3), np.uint8) * 255

# Plot the data points
for point in scaled_points:
    cv2.circle(image, point, 3, (0, 0, 0), -1)

# Display the image
cv2.imshow('Data Points', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
