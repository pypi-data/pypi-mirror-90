from chargebeecli.commands import router


def main():
    # f= Configuration.Instance()
    # values = dict({'a':'b', 'c':'d'  })
    # values = dict({'a1':'b', 'c':'d1'  })
    # f.update_section("test",values)
    # print(f.get_data())
    router.safe_entry_point()


if __name__ == '__main__':
    main()
