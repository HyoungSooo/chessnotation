import pyspark as spark
import pandas as pd
import chess.pgn
import numpy as np
from api.models import NotataionVersion, ChessELO, ChessNotation
from .utils import is_unique_avg

class Processor:

    def __init__(self, fpath) -> None:
        self.df = pd.DataFrame()

        name = self.parse_data_to_csv(fpath)
        self.msg = self.store_data(name)


    def parse_data_to_csv(self, fpath):
        
        value = open(fpath, 'r')

        game = chess.pgn.read_game(value)

        while game != None:
          if not self.df.empty:
            df = pd.DataFrame(list(game.headers.values())+ [game.mainline_moves()]).T
            df.columns = list(game.headers.keys()) + ['mainline']
            self.df = pd.concat([self.df, df], ignore_index= True)
          else:
            self.df = pd.DataFrame(list(game.headers.values()) + [game.mainline_moves()]).T
            self.df.columns = list(game.headers.keys()) + ['mainline']

          game = chess.pgn.read_game(value)
        
        try:
          NotataionVersion.objects.last()
          name = NotataionVersion.objects.create()
          self.df.to_csv(f'api\\dist\\data\\notation-v{name.id}.csv')
        except:
          name = NotataionVersion.objects.create()
          self.df.to_csv(f'api\\dist\\data\\notation-v{name.id}.csv')


        return f'notation-v{name.id}'
    
    def store_data(self, fname):
        data = pd.read_csv(f'api\\dist\\data\\{fname}.csv')
        
        success = 0
        error = 0

        for index, row in data.iterrows():
            try:
              avg = (((row['BlackElo'] + row['WhiteElo']) // 2) // 100) * 100
              elo = is_unique_avg(avg)

              notation = ChessNotation(avg=elo, white=row["White"], black=row["Black"], site=row["Site"], 
                                mainline=row["mainline"], opening=row["Opening"], event=row["Event"], 
                                result=row["Result"])
              notation.save()

              success += 1
            except:
              error += 1
        return f'success : {success}, fail : {error}'

