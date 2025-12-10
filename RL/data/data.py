import pandas as pd
import numpy as np

def generate_data(nbre_ligne, nbre_col):
    """
    Générer un DataFrame de loyers : Pour nombre_col et nombre_ligne
    f(x) = Y
    x = surface de la maison
    Y = Loyer de la maison
    """
    data = {}
    for i in range(nbre_col):
        surface = np.random.uniform(20, 200, nbre_ligne)
        loyer = surface * np.random.uniform(8, 15) + np.random.normal(0, 100, nbre_ligne)
        data[f'surface_{i+1}'] = surface
        data[f'loyer_{i+1}'] = loyer
    df = pd.DataFrame(data)
    # Save to CSV
    df.to_csv('data/Loyers.csv', index=False)
    return df