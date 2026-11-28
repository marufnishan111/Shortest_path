places = ["Main Gate","Academic Building","Library","Cafeteria","Auditorium","Admin Building","Medical Center","Dormitory","Mosque","Student Center","Lab Building","Playground"]

roads = {
    "Main Gate": {
        "Academic Building": [0.4, 0],
        "Admin Building": [0.3, 0]
    },
    "Academic Building": {
        "Main Gate": [0.4, 0],
        "Library": [0.2, 1],
        "Cafeteria": [0.3, 0],
        "Auditorium": [0.5, 0]
    },
    "Library": {
        "Academic Building": [0.2, 1],
        "Cafeteria": [0.2, 1],
        "Medical Center": [0.4, 0],
        "Lab Building": [0.3, 0]
    },
    "Cafeteria": {
        "Academic Building": [0.3, 0],
        "Library": [0.2, 1],
        "Dormitory": [0.5, 0],
        "Student Center": [0.3, 0]
    },
    "Auditorium": {
        "Academic Building": [0.5, 0],
        "Admin Building": [0.3, 0],
        "Dormitory": [0.4, 0],
        "Playground": [0.5, 0]
    },
    "Admin Building": {
        "Main Gate": [0.3, 0],
        "Auditorium": [0.3, 0],
        "Medical Center": [0.5, 0],
        "Mosque": [0.3, 0]
    },
    "Medical Center": {
        "Library": [0.4, 1],
        "Admin Building": [0.5, 0],
        "Dormitory": [0.3, 0],
        "Lab Building": [0.4, 0]
    },
    "Dormitory": {
        "Cafeteria": [0.5, 0],
        "Auditorium": [0.4, 0],
        "Medical Center": [0.3, 0],
        "Playground": [0.4, 0],
        "Mosque": [0.3, 0]
    },
    "Mosque": {
        "Admin Building": [0.3, 0],
        "Dormitory": [0.3, 0],
        "Student Center": [0.4, 0]
    },
    "Student Center": {
        "Cafeteria": [0.3, 0],
        "Mosque": [0.4, 0],
        "Lab Building": [0.3, 0]
    },
    "Lab Building": {
        "Library": [0.3, 1],
        "Medical Center": [0.4, 0],
        "Student Center": [0.3, 0],
        "Playground": [0.5, 0]
    },
    "Playground": {
        "Auditorium": [0.5, 1],
        "Dormitory": [0.4, 0],
        "Lab Building": [0.5, 0]
    }
}
def dijkstra(start, end, avoid_traffic=False):
    distance = {}
    previous = {}
    visited = []
    for place in places:
        distance[place] = float("inf")

    distance[start] = 0

    while len(visited) < len(places):
        current = None
        for place in places:
            if place not in visited:
                if current is None or distance[place] < distance[current]:
                    current = place

        if current is None or distance[current] == float("inf"):
            break

        visited.append(current)
        if current == end:
            break

        for neighbor in roads[current]:
            road_distance = roads[current][neighbor][0]
            traffic = roads[current][neighbor][1]

            if avoid_traffic and traffic == 1:
                continue

            if neighbor not in visited:
                new_distance = distance[current] + road_distance
                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    previous[neighbor] = current

    path = []
    current = end

    while current in previous:
        path.append(current)
        current = previous[current]

    if current == start:
        path.append(start)
    else:
        return None, float("inf")
    path.reverse()
    return path, distance[end]





def show_route(title, path, distance):

    print("\n======", title, "======")

    print("Path:", " -> ".join(path))
    print("Distance:", round(distance, 2), "km")

    walking_time = (distance / 5) * 60
    rickshaw_time = (distance / 12) * 60
    fare = distance * 15

    print("Walking Time:", round(walking_time), "minutes")
    print("Rickshaw Time:", round(rickshaw_time), "minutes")
    print("Rickshaw Fare:", round(fare), "Taka")

print("===== University Campus Route System =====")

print("\nAvailable Places:")
for place in places:
    print("-", place)

start = input("\nEnter starting place: ").strip().lower()
end = input("Enter destination: ").strip().lower()

place_names = {}

for place in places:
    place_names[place.lower()] = place

if start not in place_names or end not in place_names:
    print("Invalid place!")

else:
    start = place_names[start]
    end = place_names[end]
    if start == end:
        print("Starting place and destination are same!")
    else:
        best_path, best_distance = dijkstra(start, end)
        if best_path is None:
            print("No route found!")
        else:
            show_route("BEST ROUTE", best_path, best_distance)
            if has_traffic(best_path):

                print("\nTraffic found on Best Route!")
                print("Searching Alternative Route...")

                alt_path, alt_distance = dijkstra(start, end, avoid_traffic=True)
                if alt_path is not None:
                    show_route("ALTERNATIVE ROUTE",alt_path,alt_distance)
                else:
                    print("No alternative route available!")
            else:
                print("\nNo traffic on Best Route.")
                print("Only one route is needed.")
