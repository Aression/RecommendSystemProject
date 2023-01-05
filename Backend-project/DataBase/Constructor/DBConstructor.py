# Development!
# ART0189

from ..DBHelper import DBFunctionLibrary as DBFL
import pandas as pd

filepath = "Backend-project\\DataBase\\Constructor\\Data"


def ConstructAll():
    # ConstructUser()
    # ConstructRemove()
    # ConstructMovie()
    # ConstructMovieTags()
    pass

def ConstructRecommend():
    filename = 'D:\GITHUB-DESKTOP\RecommendSystemProject\Backend-project\DataBase\Constructor\Data\handeled_recommend.csv'
    data = pd.read_csv(f'{filename}')
    for index, row in data.iterrows():
        DBFL.UpdateUserRecommand(row['userIdInt'], eval(row['recommendations']))
        print(f'{index}th user recommend complete')


# Construct users from ratings{userId,movieId,rating,timestamp}
def ConstructUser():
    LastId = 1
    PreferMovies = []

    filename = "ratings.csv"
    data = pd.read_csv("{}\\{}".format(filepath, filename))
    for index, RowData in data.iterrows():
        if LastId != RowData['userId']:
            DBFL.InsertUser(LastId, 123456, PreferMovies, [])

            LastId = RowData['userId']
            PreferMovies = []
        PreferMovies.append({"UPrefMID": RowData["movieId"], "UPrefRating": RowData["rating"]})


def ConstructRemove():
    for i in range(60001, 283228):
        Query = {"UID": i}
        DBFL.RemoveUser(Query)


# MovieObject={"MID":MovieId,"MLastUpdate":MovieLatUpdateTime,"MAvgRating":MovieAvgRating,"MRatingCnt":MovieRatingCnt,"IMDBID":IMDBId}
# links{movieId,imdbId,tmdbId}
# ratings{userId,movieId,rating,timestamp}
def ConstructMovie():
    Movies = {}

    filename = "links.csv"
    data = pd.read_csv("{}\\{}".format(filepath, filename))
    for index, RowData in data.iterrows():
        Movies[str(int(RowData["movieId"]))] = {"MLastUpdate": -1, "MAvgRating": 0, "MRatingCnt": 0,
                                                "IMDBID": RowData["imdbId"]}

    filename = "ratings.csv"
    data = pd.read_csv("{}\\{}".format(filepath, filename))
    for index, RowData in data.iterrows():
        ThisIndex = str(int(RowData["movieId"]))
        TempMovie = Movies[ThisIndex]
        if (RowData["timestamp"] > TempMovie["MLastUpdate"]):
            TempMovie["MLastUpdate"] = RowData["timestamp"]
        TempMovie["MAvgRating"] += RowData["rating"]
        TempMovie["MRatingCnt"] += 1
        Movies[ThisIndex] = TempMovie

    for Key, Value in Movies.items():
        if (Value["MAvgRating"] != 0):
            Value["MAvgRating"] /= Value["MRatingCnt"]
        DBFL.InsertMovie(Key, Value["MLastUpdate"], Value["MAvgRating"], Value["MRatingCnt"], Value["IMDBID"])


# movies{movieId,title,genres}
def ConstructMovieTags():
    filename = "movies.csv"
    data = pd.read_csv("{}\\{}".format(filepath, filename))
    for index, RowData in data.iterrows():
        TagList = (str(RowData["genres"])).split("|")
        DBFL.InsertMovieTag(RowData["movieId"], TagList)
