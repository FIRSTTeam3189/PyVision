import VisionConfiguration


def test():
    config = VisionConfiguration.VisionConfiguration("settings.conf")
    config.set_green_low(200)
    config.set_blue_high(180)
    config.set_red_low(219)
    config.set_green_high(250)
    config.set_blue_high(253)
    config.set_red_high(255)
    config.set_kernel_close_size(3)
    config.set_kernel_open_size(2)
    config.set_should_open(True)
    config.set_should_close(False)
    config.save()


if __name__ == "__main__":
    test()
