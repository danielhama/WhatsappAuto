def convert_to_float(num) -> float:
    if type(num) == int:
        return num
    else:
        num = num.replace(',', '.')
        num = float(num)
        return num
