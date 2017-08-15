from subprocess import call


def put_command():
    assert 1 == 1
    print call(["python", "account.py"])


if __name__ == '__main__':
    put_command()