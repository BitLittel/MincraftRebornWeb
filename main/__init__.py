from flask import Flask


main = Flask(__name__)
main.config.from_object('config')


from main import views
