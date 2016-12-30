import unirest


def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b


def get_hive_status(username, password):
    login_response=unirest.post("https://api.hivehome.com/v5/login",
                 headers={"Content-Type": "application/x-www-form-urlencoded" },
                 params={"username": username, "password": password})

    cookie = login_response.headers['Set-Cookie']

    status_response=unirest.get("https://api.hivehome.com/v5/users/" + username + "/widgets/climate",
                                headers={"Cookie": cookie})

    return status_response.body['active'], \
           status_response.body['currentTemperature'], \
           status_response.body['targetTemperature']
