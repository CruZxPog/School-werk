def keer_om(woord):
    new_word = ""
    for letter in woord[::-1]:
        new_word += letter
    return new_word

print(keer_om("Python"))