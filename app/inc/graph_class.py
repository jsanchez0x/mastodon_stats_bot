# -*- coding: utf-8 -*-

import inc
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint


class Graph:
    def __init__(self):
        self.db_data = {}

    def prepareData(self, x_db_column, y_db_column):
        x = []
        y = []

        for row in self.db_data:
            pprint(dict(row), indent=2)
            x.append(row[x_db_column])
            y.append(row[y_db_column])

        return {"Date": x, "TotalUsers": y}

    def createGraph(self):
        print("📈 Imprimiendo gráfica...")
        data = self.prepareData('timestamp', 'total_users')

        pprint(data, indent=2)

        # Crear un DataFrame a partir de los datos
        df = pd.DataFrame(data)

        # Definir la columna 'Date' como índice
        df.set_index("Date", inplace=True)

        # Crear el gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["TotalUsers"], marker='o')

        # Añadir títulos y etiquetas
        plt.title("Mastodon users evolution")
        plt.xlabel("Date")
        plt.xticks(rotation=45)
        plt.ylabel("Total Users")
        plt.grid(True)
        plt.subplots_adjust(bottom=0.3)  # Aumentar el margen inferior

        # Guardar el gráfico como imagen
        plt.savefig("/mastodon_stats_bot/logs/grafico.png")