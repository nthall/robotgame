#!/usr/bin/python
# a very simple bot that just runs to the center and stands there, and tries to clump up a bit i guess
# currently mostly useful for giving the better version something to fight against.
import rg

class Robot:
  def act(self, game):
    blob_locs = set(self.location)
   
    #suicide squad
      #explode if surrounded by enemies
 
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
