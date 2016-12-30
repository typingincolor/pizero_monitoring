import unirest


def get_sensu_status(url, username, password):
    response = unirest.get(url, auth=(username, password))

    warning = 0
    critical = 0

    for check in response.body:
        if check['check']['handle'] == 1:
            if check['check']['status'] == 1:
                warning += 1
            if check['check']['status'] == 2:
                critical += 1

    return warning, critical
