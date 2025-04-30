from line_info import LineInfo

line = LineInfo("osaka_metro\\midosuji_line.yaml")
station = line.get_station("M16")

print(station.name["zh-TW"])  # Higashi-Mikuni
print(station.previous_station)  # ['M11', 2.0, 150]
