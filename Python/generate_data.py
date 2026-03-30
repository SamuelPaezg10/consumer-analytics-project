import pandas as pd
import numpy as np
import os

np.random.seed(42)

n = 5000

df = pd.DataFrame({
    "customer_id": np.random.randint(1, 1000, n),
    "product": np.random.choice(["A", "B", "C", "D"], n),
    "units": np.random.poisson(3, n),
    "price": np.random.uniform(5, 50, n),
    "date": pd.to_datetime("2024-01-01") + pd.to_timedelta(np.random.randint(0, 365, n), unit="D")
})

df["sales"] = df["units"] * df["price"]

# Outliers
outliers_index = np.random.choice(df.index, 10)
df.loc[outliers_index, "units"] = df.loc[outliers_index, "units"] * 50

# 🔥 Crear carpeta automáticamente
os.makedirs("../Data", exist_ok=True)

df.to_csv("Data/consumer_data.csv", index=False)

print("Dataset generado correctamente")

print(os.getcwd())