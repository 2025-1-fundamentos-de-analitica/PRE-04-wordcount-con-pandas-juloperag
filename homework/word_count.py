"""Taller evaluable"""

import glob
import os

import pandas as pd  # type: ignore


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #
    files = glob.glob(f"{input_directory}/*")
    #Se crea una lista donde se lee los archivos de texto y se crea una tabla por cada texto
    dataframes = [
        pd.read_csv(
            file,
            header=None,
            delimiter="\t",
            names=["line"],
            index_col=None,
        )
        for file in files
    ]
    #Luego se concatena 
    dataframe = pd.concat(dataframes, ignore_index=True)

    return dataframe


def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    dataframe = dataframe.copy()
    dataframe["line"] = dataframe["line"].str.lower()
    #Aqui se borrar los signos de puntuacion
    dataframe["line"] = (
        dataframe["line"]
        .str.replace(",", "")
        .str.replace(
            ".",
            "",
        )
    )
    return dataframe


def count_words(dataframe):
    """Word count"""

    dataframe = dataframe.copy()
    #Tomar cara registro y aplico split(), donde aqui para un strg separa cada palabra de las lineas
    dataframe["line"] = dataframe["line"].str.split()
    #toma cada registro y separa
    #A: {a, [c,b]}, B: {b, [c,d]}
    #0: a , c
    #0: a, b
    dataframe = dataframe.explode("line")
    dataframe = dataframe.groupby("line").size().reset_index(name="count")
    return dataframe


def save_output(dataframe, output_directory):
    """Save output to a file."""

    if os.path.exists(output_directory):
        files = glob.glob(f"{output_directory}/*")
        for file in files:
            os.remove(file)
        os.rmdir(output_directory)

    os.makedirs(output_directory)

    dataframe.to_csv(
        f"{output_directory}/part-00000",
        sep="\t",
        index=False,
        header=False,
    )


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """Create Marker"""

    with open(f"{output_directory}/_SUCCESS", "w", encoding="utf-8") as f:
        f.write("")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """Job"""
    #Carga de archivo
    dataframe = load_input(input_directory)
    #Limpieza de texto
    dataframe = clean_text(dataframe)
    dataframe = count_words(dataframe)
    save_output(dataframe, output_directory)
    create_marker(output_directory)


if __name__ == "__main__":

    run_job(
        "files/input",
        "files/output",
    )