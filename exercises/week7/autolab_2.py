def df_memsize(df):
    return df.memory_usage(deep=True).sum()