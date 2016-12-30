import unirest


def rgb(minimum, maximum, value):
    mid_val = (maximum - minimum) / 2

    if value > maximum:
        value = maximum
    if value < minimum:
        value = minimum

    if value > mid_val:
        r = 255
        g = 255 * ((maximum - value) / (maximum - mid_val))
        b = 0
    else:
        g = 255
        r = 255 * ((value - minimum) / (mid_val - minimum))
        b = 0

    return r, g, b


def get_hive_status(username, password):
    login_response = unirest.post("https://api.hivehome.com/v5/login",
                                  headers={"Content-Type": "application/x-www-form-urlencoded"},
                                  params={"username": username, "password": password})

    cookie = login_response.headers['Set-Cookie']

    status_response = unirest.get("https://api.hivehome.com/v5/users/" + username + "/widgets/climate",
                                  headers={"Cookie": cookie})

    return status_response.body['active'], \
           status_response.body['currentTemperature'], \
           status_response.body['targetTemperature'], \
           status_response.body['outsideTemperature']
