import requests
def getrep(token="",id=""):
    discordrep = requests.get("https://discordrep.com/api/v3/rep/"+ id, headers={"Authorization":token})
