from chargebeecli.Configuration import Configuration


def main():
    pass


def process(profile_name, profile_data):
    configuration = Configuration.Instance()
    configuration.update_section(profile_name, profile_data)



if __name__ == '__main__':
    main()
