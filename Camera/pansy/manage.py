from apps import create_app

app = create_app()


if __name__ == "__main__":
    app.run()
    # app.run(debug=True, host="0.0.0.0", port=<포트번호>)
