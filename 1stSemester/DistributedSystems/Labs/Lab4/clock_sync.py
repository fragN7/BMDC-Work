from datetime import datetime

# Function to calculate the offset between two clocks
def calculate_offset(local_time, received_time):
    return (received_time - local_time) // 2

# Function to synchronize the clock with the server with Cristian's algorithm concept
def synchronize_clock(server_time):
    local_time = datetime.now()
    offset = calculate_offset(local_time, server_time)
    return local_time + offset

# Example usage
server_time = datetime.strptime(input("Enter the server time in format yyyy-mm-dd HH:MM:SS: "), '%Y-%m-%d %H:%M:%S')
synchronized_time = synchronize_clock(server_time)
print("The synchronized time is:", synchronized_time)
