from app import app


def run():
    app.run(debug=True, host='0.0.0.0', port='5101')


if __name__ == '__main__':
    run()