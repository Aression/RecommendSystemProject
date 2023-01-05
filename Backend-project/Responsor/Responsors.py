from .ResponsorHeader import *
import random

# 随便选一个作为初始展示页面
randInitialDisplay = random.randint(0, 100)
ThisUserAccount = randInitialDisplay
UseCustomUser = False

route_base = Blueprint('', __name__)


@route_base.route('/login', methods=["GET", "POST"])
def Login():
    req = json.loads(request.data)
    print(f'received data:{req}')
    InUserId = req['user_account']
    InUserPassword = req['user_password']

    passwd = ReadCustomUserPwd(InUserId)
    if InUserPassword == passwd:
        # 转为该用户的登录态
        global ThisUserAccount, UseCustomUser
        ThisUserAccount = InUserId
        UseCustomUser = True
        print(f'login success, user id changed to {InUserId}')
        resp = {'code': 200}
    else:
        infomation = 'login denied, check your id or password'
        raise RuntimeError(infomation)
    return jsonify(resp)


@route_base.route('/register', methods=["GET", "POST"])
def RegisterCustomUser():
    req = json.loads(request.data)
    InUserAcc = req["user_account"]
    InUserPassword = req["user_password"]

    InsertCustomUser(InUserAcc, InUserPassword)
    print(f'register complete, current user is {InUserAcc}')
    global ThisUserAccount, UseCustomUser
    ThisUserAccount = InUserAcc
    UseCustomUser = True

    resp = {'code': 200}
    return jsonify(resp)


@route_base.route('/choose', methods=["GET", "POST"])
def ApplyCustomTags():
    req = json.loads(request.data)
    InCustomTags = req["taglist"]
    print(f'received tag preference{InCustomTags}')
    try:
        UpdateCustomUser(ThisUserAccount, InCustomTags)
    except Exception as e:
        print(e.__traceback__)
        return jsonify({'code': 500})
    return jsonify({'code': 200})


@route_base.route('/home', methods=["GET"])
def ShowRecommendation():
    global ThisUserAccount, UseCustomUser
    MappedUserId = ThisUserAccount
    print(f'when /home is called, current global user is {ThisUserAccount}')
    if UseCustomUser:
        Query = {"CUID": ThisUserAccount}
        Result = CCustomUser.find_one(Query)
        MappedUserId = Result["MatchedUID"]

    Query = {"UID": MappedUserId}
    Result = CUser.find_one(Query)
    RecommendPairs = Result["URec"]
    RecommendList = []
    for i in range(15):
        movieId = list(RecommendPairs[i].keys())[0]
        IMDBQueryResult = RequestBaseInfoById(MIdToIMDBId(movieId))
        print(IMDBQueryResult)
        RecommendList.append({"movie_imgae": IMDBQueryResult["Poster"], "movie_title": IMDBQueryResult["Title"],
                              "movie_id": movieId})
    print(RecommendList)
    resp = {'code': 200, "recommendmovies": RecommendList}
    return jsonify(resp)


@route_base.route('/showMovies', methods=["GET", "POST"])
def ShowDetails():
    req = json.loads(request.data)
    print(f'received : {req}')
    movieid = req["movie_id"]

    IMDBId = MIdToIMDBId(movieid)
    IMDBQueryResult = RequestDetailInfoById(IMDBId)

    Query = {"MID": req["movie_id"]}
    Result = CMovie.find_one(Query)
    localRating = round(Result['MAvgRating'], 2)
    resp = \
        {
            'code': 200,
            "movie_cover": IMDBQueryResult["Poster"],
            "movie_name": IMDBQueryResult["Title"],
            "movie_rating": localRating,
            "movie_tag": list(IMDBQueryResult["Genre"].split(',')),
            "movie_introduction": IMDBQueryResult["Plot"],
            "movie_date": IMDBQueryResult["Released"],
            "movie_language": IMDBQueryResult["Language"],
            'movie_director': IMDBQueryResult['Director'],
            'movie_country': IMDBQueryResult['Country'],
            'movie_length': IMDBQueryResult['Runtime']
        }
    print(IMDBQueryResult)
    print(resp)
    return jsonify(resp)
