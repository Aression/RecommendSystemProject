from .ResponsorHeader import *

ThisUserAccount = -1
UseCustomUser = False

route_base = Blueprint('', __name__)


# 不考虑自定义用户的再次登录，这样就不用走数据库了
@route_base.route('/login', methods=["GET", "POST"])
def Login():
    req = request.values
    InUserId = req["user_account"]
    InUserPassword = req["user_password"]
    RespCode = 406
    if 0 < int(InUserId) < 60001 and InUserPassword == str(123456):
        RespCode = 200

        global ThisUserAccount, UseCustomUser
        ThisUserAccount = InUserId
        UseCustomUser = False

    resp = {'code': RespCode}
    return jsonify(resp)


# 只考虑注册不考虑自定义用户的再次登录
@route_base.route('/register', methods=["GET", "POST"])
def RegisterCustomUser():
    req = request.values
    InUserAcc = req["user_account"]
    # InUserPassword=req["user_password"]

    InsertCustomUser(InUserAcc)

    global ThisUserAccount, UseCustomUser
    ThisUserAccount = InUserAcc
    UseCustomUser = True

    resp = {'code': 200}
    return jsonify(resp)


@route_base.route('/choose', methods=["GET", "POST"])
def ApplyCustomTags():
    req = request.values
    InCustomTags = req["taglist"]

    global ThisUserAccount, UseCustomUser
    UseCustomUser = True
    ThisUserAccount = "114514"
    if not UseCustomUser:
        raise Exception("Choose tag when use existed user!")
    UpdateCustomUser(ThisUserAccount, json.loads(InCustomTags))

    resp = {'code': 200}
    return jsonify(resp)


@route_base.route('/home', methods=["GET"])
def ShowRecommendation():
    global ThisUserAccount, UseCustomUser
    MappedUserId = ThisUserAccount
    if UseCustomUser:
        Query = {"CUID": ThisUserAccount}
        Result = CCustomUser.find_one(Query)
        MappedUserId = Result["MatchedUID"]

    Query = {"UID": MappedUserId}
    Result = CUser.find_one(Query)
    RecommendPairs = Result["URec"]
    RecommendList = []
    for i in range(15):
        IMDBQueryResult = RequestBaseInfoById(MIdToIMDBId(RecommendPairs[i]["MID"]))
        RecommendList.append({"movie_imgae": IMDBQueryResult["image"], "movie_title": IMDBQueryResult["title"],
                              "movie_id ": RecommendPairs[i]["MID"]})

    resp = {'code': 200, "recommendmovies": RecommendList}
    return jsonify(resp)


@route_base.route('/showMovies', methods=["GET", "POST"])
def ShowDetails():
    req = request.values
    IMDBId = MIdToIMDBId(req["movie_id"])
    IMDBQueryResult = RequestDetailInfoById(IMDBId)

    Query = {"MID": req["movie_id"]}
    Result = CMovie.find_one(Query)
    resp = \
        {
            'code': 200,
            "movie_cover": IMDBQueryResult["image"],
            "movie_name": IMDBQueryResult["fullTitle"],
            "movie_rating": Result["MAvgRating"],
            "movie_tag": IMDBQueryResult["genres"],
            "movie_introduction": IMDBQueryResult["plot"],
            "movie_date": IMDBQueryResult["releaseDate"],
            "movie_language": "English"
        }
    return jsonify(resp)
