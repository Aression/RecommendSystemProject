# Development!
# ART0189

from AppStartDataBase import CUser, CMovie, CCustomUser, CMovieTag

# Other data-write operations are not recommandable.
# Most data-read operation need be implemented manually.

DebugDBOp = True


def MIdToIMDBId(MID):
    Query = {"MID": MID}
    Result = CMovie.find_one(Query)
    IntIMDBId = int(Result["IMDBID"])
    Temp = IntIMDBId
    TargetStr = ""
    while Temp < 1000000:
        TargetStr += "0"
        Temp *= 10
    return TargetStr + str(IntIMDBId)


def InsertUser(UserId, UserPassword, UserPreferenceMap, UserRecommandMap):
    UserObject = {"UID": UserId, "UPwd": str(UserPassword), "UPref": UserPreferenceMap, "URec": UserRecommandMap}
    Result = CUser.insert_one(UserObject)
    if DebugDBOp and not Result.acknowledged:
        raise Exception("Invalid user insert!", UserObject)
    return Result.acknowledged


def UpdateUserRecommand(UserId, NewUserRecommandList):
    Query = {"UID": UserId}
    Result = CUser.find_one(Query)
    Result["URec"] = NewUserRecommandList
    Result = CUser.update_one(Query, {"$set": Result})
    if DebugDBOp and not Result.acknowledged:
        raise Exception("Invalid user update!", Result)
    return bool(Result.modified_count == 1)


def RemoveUser(Query):
    Result = CUser.delete_one(Query)
    return Result


def InsertMovie(MovieId, MovieLatUpdateTime, MovieAvgRating, MovieRatingCnt, IMDBId):
    MovieObject = {"MID": MovieId, "MLastUpdate": MovieLatUpdateTime, "MAvgRating": MovieAvgRating,
                   "MRatingCnt": MovieRatingCnt, "IMDBID": IMDBId}
    Result = CMovie.insert_one(MovieObject)
    if DebugDBOp and not Result.acknowledged:
        raise Exception("Invalid user insert!", MovieObject)
    return Result.acknowledged


def InsertCustomUser(CustomUserId):
    CustomUserObject = {"CUID": CustomUserId, "MatchedUID": -1}
    Result = CCustomUser.insert_one(CustomUserObject)
    if DebugDBOp and not Result.acknowledged:
        raise Exception("Invalid custom user insert!", CustomUserObject)
    return Result.acknowledged


def UpdateCustomUser(CustomUserId, CustomTags):
    Query = {"CUID": CustomUserId}
    Result = CCustomUser.find_one(Query)
    Result["MatchedUID"] = MatchExistedUser(CustomTags)
    Result = CCustomUser.update_one(Query, {"$set": Result})
    if DebugDBOp and not Result.acknowledged:
        raise Exception("Invalid custom user update!", Result)
    return Result.acknowledged


def InsertMovieTag(MovieId, TagList):
    MovieTagObject = {"MID": MovieId, "Tags": TagList}
    Result = CMovieTag.insert_one(MovieTagObject)
    if DebugDBOp and not Result.acknowledged:
        raise Exception("Invalid user insert!", MovieTagObject)
    return Result.acknowledged


def MatchExistedUser(CustomTags):
    ConstMinRating = 4.0

    for i in range(1, 100):
        ExistedUserTag = []

        Query = {"UID": i}
        Result = CUser.find_one(Query)
        for j in Result["UPref"]:
            if j["UPrefRating"] >= ConstMinRating:
                SecQuery = {"MID": j["UPrefMID"]}
                SecResult = CMovieTag.find_one(SecQuery)
                ExistedUserTag += SecResult["Tags"]

        bAllMatched = True
        for k in CustomTags:
            if not k in ExistedUserTag:
                bAllMatched = False
                break
        if bAllMatched:
            return i

    raise Exception("Can not find suitable user to match!")
