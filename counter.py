import pymongo
from timecontrol import TimeControl

def process_file(filepath, database):
    with open(filepath, "r") as f:
        player1 = None
        player2 = None
        variant = None
        tc = None
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith("[White "):
                player1 = line.split("\"")[1].lower()
            elif line.startswith("[Black "):
                player2 = line.split("\"")[1].lower()
            elif line.startswith("[Variant "):
                variant = line.split("\"")[1]
            elif line.startswith("[TimeControl "):
                tc = TimeControl(line.split("\"")[1])
            elif not line.startswith("["):
                if player1 is None or player2 is None or variant is None or tc is None:
                    raise Exception("bug")
                update_player(player1, tc.score, database, variant)
                update_player(player2, tc.score, database, variant)

def update_player(uid, score, database, variant):
    if database[variant].find_one({ "_id": uid}) is None:
        database[variant].insert_one({ "_id": uid, "score": 0 })
    database[variant].update({ "_id": uid}, { "$inc": { "score": score }})

if __name__ == "__main__":
    database = pymongo.MongoClient()["vascores"]
    filepaths = input("File paths, comma-separated: ").split(",")
    for fp in filepaths:
        process_file(fp, database)
            