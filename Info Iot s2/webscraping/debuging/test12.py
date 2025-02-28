def grootste_waarde(lijst):
    grootste = 0
    for getal in lijst:
        if getal > grootste:
            grootste = getal
    return grootste

print(grootste_waarde([-10, -20, -30]))  # Verwachte output: -10