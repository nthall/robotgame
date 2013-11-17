#!/usr/bin/python
import operator
import rg

class Robot:
  def act(self, game):
    blob_locs = set(self.location)
   
    #if one nearby enemy, attack
    #if surrounded by enemies, suicide
    #in between, run towards center.
    adj_enemies = []
    for l in set(rg.locs_around(self.location, ['spawn', 'invalid'])).difference(blob_locs):
      if l in game.get('robots').keys():
        if game['robots'][l].get('player_id') != self.player_id:
          adj_enemies.append(game['robots'][l])
    if len(adj_enemies) >= 4:
      return ['suicide']
    elif len(adj_enemies) > 1:
      #if in center, stand and fight lowest hp enemy 
      if self.location == rg.CENTER_POINT:
        target = min(adj_enemies, key=lambda k: k['hp']) 
        return['attack', target['location']]
      else:
        return ['move', rg.toward(self.location, rg.CENTER_POINT)]
    elif len(adj_enemies) == 1:
      return ['attack', adj_enemies[0]['location']]

    #hold the center
    if self.location == rg.CENTER_POINT:
      return ['guard']
    elif self.in_blob(self.location, blob_locs, game) and rg.CENTER_POINT in blob_locs:
      return ['guard']

    #don't hang around spawn points
    if 'spawn' in rg.loc_types(self.location):
      return ['move', rg.toward(self.location, rg.CENTER_POINT)]

    #if nothing better to do, move toward center.
    return ['move', rg.toward(self.location, rg.CENTER_POINT)]
    
  
  #a blob is some number of adjacent allied units
  def in_blob(self, loc, blob_locs, game):
    for l in set(rg.locs_around(loc, ['spawn', 'invalid'])).difference(blob_locs):
      if l in game.get('robots').keys():
        if game['robots'][l].get('player_id') == self.player_id:
          blob_locs.add(l)
          self.in_blob(l, blob_locs, game)
