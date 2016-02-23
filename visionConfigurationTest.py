import VisionConfiguration


def test():
    config = VisionConfiguration.VisionConfiguration("settings.conf")
    config.set_two_low(200)
    config.set_three_high(180)
    config.set_one_low(219)
    config.set_two_high(250)
    config.set_three_high(253)
    config.set_one_high(255)
    config.set_kernel_close_size(3)
    config.set_kernel_open_size(2)
    config.set_should_open(True)
    config.set_should_close(False)
    config.save()


if __name__ == "__main__":
    test()
