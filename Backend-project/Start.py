from AppStartDataBase import *
from Responsor.Responsors import *
from DataBase.Constructor import DBConstructor as DBC

App.register_blueprint(route_base, url_prefix="/")

# launch
# launch databse local debug
if __name__ == '__main__':
    # DBC.ConstructRecommend()

    App.run(host='0.0.0.0', port=8082, debug=True)
