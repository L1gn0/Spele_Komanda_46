def validate_length(value):
    try:
        n = int(value)
    except ValueError:
        return False, "Garumam jābūt veselam skaitlim 15–25."

    if not (15 <= n <= 25):
        return False, "Garumam jābūt diapazonā 15–25."

    return True, n