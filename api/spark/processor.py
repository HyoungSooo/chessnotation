import pyspark as spark
import pandas as pd
import chess.pgn
import numpy as np
from api.models import NotataionVersion, ChessELO, ChessNotation, ChessNoationCheckPoint
from .utils import is_unique_avg


class Processor:

    def __init__(self, fpath, num, checkpoint=None, name=None) -> None:
        self.df = pd.DataFrame()
        self.num = num
        self.checkpoint = checkpoint
        self.name = name
        self.msg = 'done'

        b = self.parse_data_to_csv(fpath)
        if b:
            self.msg = self.store_data()
        else:
            self.msg = 'parsing fali'

    def parse_data_to_csv(self, fpath):

        value = open(fpath, 'r')
        if self.checkpoint:
            for i in range(self.checkpoint):
                game = chess.pgn.read_game(value)

        game = chess.pgn.read_game(value)
        cnt = 0
        if game:
            while game != None:
                if cnt >= self.num:
                    break

                if not self.df.empty:
                    df = pd.DataFrame(
                        list(game.headers.values()) + [game.mainline_moves()]).T
                    df.columns = list(game.headers.keys()) + ['mainline']
                    self.df = pd.concat([self.df, df], ignore_index=True)
                else:
                    self.df = pd.DataFrame(
                        list(game.headers.values()) + [game.mainline_moves()]).T
                    self.df.columns = list(game.headers.keys()) + ['mainline']

                game = chess.pgn.read_game(value)
                cnt += 1

            try:
                data = ChessNoationCheckPoint.objects.get(
                    fname=self.name)
                print(data)
                data.checkpoint += cnt
                data.save()
                print('done', data.checkpoint)
            except:
                print('fail')
                o = ChessNoationCheckPoint.objects.create(
                    fname=self.name, checkpoint=cnt)
                o.save()
            return True
        else:
            return None

    def store_data(self):

        success = 0
        error = 0

        for index, row in self.df.iterrows():
            avg = (
                (int(row['BlackElo']) + int(row['WhiteElo']) // 2) // 100) * 100
            elo = is_unique_avg(avg)

            notation = ChessNotation.objects.create(avg=elo, white=row["White"], black=row["Black"], site=row["Site"],
                                                    mainline=row["mainline"], opening=row["Opening"], event=row["Event"],
                                                    result=row["Result"])
            notation.save()

            success += 1
            error += 1
        self.msg = f'success : {success}, fail : {error}'
        return
