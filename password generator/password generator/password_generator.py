for i in range (10):
    import random
    lower_case = "abcdefghijklmnopqrstuvwxyz"
    upper_case = "ABCDEFGHIGKLMNOPQRSTUVWXYZ"
    number = "0123456789"
    symbols = "!@#$%^&*"

    use_for = lower_case + upper_case + number + symbols
    length_for_pass = 70

    password = "".join(random.sample(use_for, length_for_pass))

    print(password)
