import requests
import json
from decouple import config


def create_session():
	s = requests.Session()
	s.headers.update({
		"Accept-Language": "es-ES,es;q=0.9",
    	"Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    	"X-Riot-Token": config("R_Token")
	})

	return s


def main(user = "MrMewtwo02"):
	champions = requests.get("https://ddragon.leagueoflegends.com/cdn/13.12.1/data/es_ES/champion.json").json()
	sess = create_session()
	url = config("URL")
	current_season = "1632294000"

	get_id = sess.get(f"{url}/lol/summoner/v4/summoners/by-name/{user}").json()

	response = sess.get(f"{url}/lol/league/v4/entries/by-summoner/{get_id['id']}").json()

	rango = {	
		"Ranked_FLEX_SR" : f"{response[0]['tier']} {response[0]['rank']}",
		"Ranked_SOLO_5X5" : f"{response[1]['tier']} {response[1]['rank']}"
	}

	winrate = {
		"Ranked_FLEX_SR" : round(response[0]['wins'] * 100 / (response[0]['wins'] + response[0]['losses'])),
		"Ranked_SOLO_5X5" : round(response[1]['wins'] * 100 / (response[1]['wins'] + response[1]['losses']))
	}

	#main

	#get player first mastery champion, i guess thats main now?
	response = sess.get(f"{url}/lol/champion-mastery/v4/champion-masteries/by-puuid/{get_id['puuid']}").json()[0]


	for i in champions["data"]:
		if champions["data"][i]["key"] == str(response["championId"]):
			main = (champions["data"][i]["id"])
			break

	return f"User {user}:\nMain: {main}\nRank:\nFlex - {rango['Ranked_FLEX_SR']}\nSolo - {rango['Ranked_SOLO_5X5']}\nWinrate:\nFlex - {winrate['Ranked_FLEX_SR']}%\nSolo - {winrate['Ranked_SOLO_5X5']}%"


if __name__ == '__main__':

	main()

