def zoek_waarde(lijst, waarde):
    for i in range(len(lijst)):
        if lijst[i] == waarde:
            return i


print(zoek_waarde([10, 20, 30], 5))
