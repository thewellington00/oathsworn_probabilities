import numpy as np
import pandas as pd


def generate_pdf_and_ccdf(data):
    index = np.arange(0, np.max(data) + 1)
    values = np.arange(0, np.max(data) + 2)  # +2 to include the last value in the histogram
    pdf = np.histogram(data, bins=values, density=True)[0]
    ccdf = 1 - np.cumsum(pdf) + pdf  # plus pdf to make the logic "greater than or equal to"
    return pd.DataFrame(index=index, data={'pdf': pdf, 'ccdf': ccdf})
