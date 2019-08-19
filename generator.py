from lib.application import ApplicationFactory


def run():
    app = ApplicationFactory.make()
    app.run()


if __name__ == "__main__":
    run()
