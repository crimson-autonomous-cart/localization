# Read input data from the provided format
with open('data1.txt', 'r') as file:
    input_data = file.readlines()

# Parse input data and extract latitude and longitude
output_data = ""
for line in input_data:
    parts = line.split()
    lat = float(parts[1]) * 1e-7
    lon = float(parts[3]) * 1e-7
    output_data += f"Latitude: {lat} Long: {lon}\n"

# Write output data to a text file
with open('output_data1.txt', 'w') as file:
    file.write(output_data)

print("Output data has been written to output_data.txt")
