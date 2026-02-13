def save_csv_with_spaces(df, filename):
    df.to_csv(filename, index=False)
    with open(filename, "r") as f:
        data = f.read()
    data = data.replace(",", ", ")
    with open(filename, "w") as f:
        f.write(data)