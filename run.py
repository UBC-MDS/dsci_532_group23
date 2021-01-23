import src.dashboard.app as dba

app = dba.make_app()
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)