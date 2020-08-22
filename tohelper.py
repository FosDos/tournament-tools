import challonge
import datetime

class chal_driver(object):
  '''
  Initialization function

  PARAMETERS:
    String user - username of the challonge account
    String key - API key of the challonge account
    String sub - subdomain of the challonge account, defaults to blank

  RETURNS:
    None

  '''
  def __init__(self, user = "", key = "", sub = ''):
    self.user = user
    self.key = key
    self.sub = sub
    self.brackets = []
    challonge.set_credentials(self.user, self.key)




  '''
  authenticate function, returns false if username or key is incorrect

  PARAMTERS:
    None
  RETURNS:
    boolean auth - True if connection works, False if not

  '''

  def authenticate(self):
    try:
      index = challonge.tournaments.index()
    except:
      return False
    return True


  '''
  get_recent function, returns the ids of the last tournaments you ran

  PARAMTERS:
    int amount - integer representing the amount of tournaments you want
  RETURNS:
    int[] return_ids - a list with the ids of the most recent tournaments

  '''
  def get_recent(self, amount):
    index = challonge.tournaments.index()
    return_ids = []
    for iterator in range(amount):
      to_ret = index[len(index)-(1+iterator)]
      return_ids.append(to_ret["id"])
    return return_ids


  '''
  get game id function returns the numerical code for the game id played in a tournament

  PARAMETERS:
    int t_id - a tournaments id number

  RETURNS:
    int return_id - a int that is the game id of the searched bracket

  '''
  def get_game_id(self, t_id):
    data = challonge.tournaments.show(t_id)

    return data["game_id"]


  '''
  get_last function, returns the id of the last tournament you ran

  PARAMTERS:
    None
  RETURNS:
    int del_id - int representing the id of a tournament

  '''


  def get_last(self):
    index = challonge.tournaments.index()
    to_del = index[len(index)-1]
    del_id = to_del["id"]
    return del_id
    '''
    get_name function, returns the name of a tournament

    PARAMETERS:
      int t_id - a tournaments id number

    RETURNS:
      String name - a string containing the requested name

    '''
  def get_name(self, t_id):
    name = challonge.tournaments.show(t_id)["url"]
    return name
  '''
  create_bracket function, creates a bracket and returns its ID

  PARAMETERS:
    String name - string to be set as the tournament name
    String game - the game being played in that tournament
    String style - the type of bracket that is being run

  RETURNS:
    int

  '''
  def create_bracket( self, name, game, style= "double elimination"):

    today_date = str(datetime.datetime.now()).split()[0].replace('-','_')
    split_date = today_date.split('_')
    today_date = split_date[1] + "_" + split_date[2] + "_" + split_date[0]
    if (self.sub == ''):
      url = game + "_" + name.replace(' ', '_') +"_" +  today_date
    else:
      url = game + "_" + today_date
    today_date = today_date.replace('_', '/')
    if(game == "Smash4"):
      badfix = "Smash 4"
      name = name + " " + badfix + " " + today_date
    else:
      name = name + " " + game + " " + today_date
    gameid = 0
    if (game == "Smash4"):
      gameid = 20988
    if (game == "PM"):
      gameid = 597
    if (game == "Melee"):
      gameid = 394

    created = challonge.tournaments.create(name, url, style, subdomain= self.sub, game_id = gameid)
    t_id = created["id"]
    return t_id


  '''
  bulk delete function, deletes a certain number of tournaments
  PARAMETERS:
    int[] t_ids - a list of tournament ids to delete

  RETURNS:
    None

  '''
  def bulk_delete(self, t_ids):
    for item in range(len(t_ids)):
      challonge.tournaments.destroy(t_ids[item])


  '''
  delete function, deletes a tournament

  PARAMETERS:
    int t_id - a tournaments id number

  RETURNS:
    None

  '''
  def delete(self, t_id):
    challonge.tournaments.destroy(t_id)


  '''
  add function, adds a participant to a tournament

  PARAMETERS:
    int t_id - a tournaments id number
    String name - a participants name

  RETURNS:
    None

  '''
  def add(self, t_id, name):
    challonge.participants.create(t_id, name)


  '''
  remove function, removes a participant from a bracket

  PARAMETERS:
    int t_id - a tournaments id number
    int p_id - a participants id
  RETURNS:
    None

  '''
  def remove(self, t_id, name):
    challonge.participants.destroy(t_id, p_id)
  '''
  get_curr_matchlist - returns the matches that are currently available

  PARAMETERS:
    int t_id - a tournaments id number

  RETURNS:
    String[] toReturn - a string list containing available match ID's

  '''
  def get_curr_matchlist(self, t_id):
    toReturn = []
    for item in challonge.matches.index(t_id):
      if item["player1_id"] != None:
        if item["player2_id"] != None:
          toReturn.append(item["id"])
    return toReturn
  '''
  start function

  PARAMETERS:
    int t_id - a tournaments id number

  RETURNS:
    None

  '''
  def start(self, t_id):
    challonge.tournaments.start(t_id)


  '''
  encode function, encodes a bracket by hiding its entrants names

  PARAMETERS:
    int t_id - a tournaments id number

  RETURNS:
    dict toReturn - a dictionary object with the structure {id : name}
  '''
  def encode(self, t_id):
    toReturn = {}
    data = challonge.participants.index(t_id)
    for item in data:
      toReturn[item["id"]] = item["display_name_with_invitation_email_address"]
    for item in data:
      edit_name = str(item["seed"]) + "#NotMyPanel"
      challonge.participants.update(t_id,item["id"], name = edit_name)
    return toReturn
  '''
  decode function, decodes function encoded by the encode function

  PARAMETERS:
    int t_id - a tournaments id number
    dict key - a dictionary created by the encode function as a key

  RETURNS:
    None

  '''
  def decode(self, t_id, key):
    to_decode = challonge.participants.index(t_id)
    for item in key:
      challonge.participants.update(t_id, item, name = key[item] )
  '''
  get_entrants function, returns a list of the entrants in a tournament

  PARAMETERS:
    int t_id - a tournaments id number

  RETURNS:
    String[] toReturn - a string[] containing all the partcipant names

  '''
  def get_entrants(self, t_id):
    entrant_data = challonge.participants.index(t_id)
    toReturn = []
    for x in entrant_data:
      toReturn.append(x["display_name_with_invitation_email_address"])
    for iterator in range(len(toReturn)):
      toReturn[iterator] = toReturn[iterator].encode('ascii', 'ignore')
    return toReturn
  '''
  report_match function, reports a match score and winner

  PARAMETERS:
    int t_id - a tournaments id number
    int match_id - matches id number
    String score - a string containing the score (0-1,2-0, etc)

  RETURNS:
    None

  '''
  def report_match(self, t_id, match_id, score):
    match = challonge.matches.show(t_id, match_id)
    t_score = score.split('-')
    if (int(t_score[0]) > int(t_score[1])):
      winner = match["player1_id"]
    elif (int(t_score[0]) < int(t_score[1])):
      winner = match["player2_id"]
    challonge.matches.update(t_id, match_id,scores_csv = score, winner_id = winner )
