from chargebeecli.Configuration import Configuration
from chargebeecli.util.printer import custom_print
from chargebeecli.util.url_validator import is_valid_url


def main():
    pass


def process(profile_name, profile_data):
    configuration = Configuration.Instance()
    if is_valid_url(profile_data['account']):
        configuration.update_section(profile_name, profile_data)
        custom_print("profile configured properly")
    else:
        custom_print(profile_data['account'] + " :url is not valid")
        exit()


if __name__ == '__main__':
    main()
