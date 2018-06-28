import json

class Interpret(object):
  """
  Interpret is the result of calling interpret() on a Text object. It simply
  encapsulates the user's intent and any entities that may have been detected
  in the utterance.

  Example:
    t = Text("what is the weather in los angeles")
    i = t.interpret()
    # get the user's intent
    print(i.intent)   # weather
    # get the entities in the query
    print(i.entites)  # { 'location': 'los angeles' }
  """
  def __init__(self, interpretation):
    """ Construct an interpret object from the API response """
    self.text = interpretation["text"]
    self.intent = interpretation["intent"]
    self.entities = interpretation["entities"]
    self.raw = interpretation

  def __repr__(self):
    return json.dumps(self.raw, indent=2)
  
  def context_dict(self):
    return self.raw