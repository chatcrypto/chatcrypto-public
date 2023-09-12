def get_last_n_elements(arr, n):
    if len(arr) <= n:
        return arr
    else:
        return arr[-n:]