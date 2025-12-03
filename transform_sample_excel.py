import pandas as pd

def main():
    file_path = "./docomo.xlsx"
    sheet_name = "11月会場別実績"

     # Excelファイルを読み込む
     # 対象範囲: B〜BG列、4行目以降
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        header=3,
        usecols="B:BG"
    )

    # 2行目 - 50行目は空白行なので削除(一旦ハードコーディング)
    rows_to_drop = range(1, 50)
    df = df.drop(index=rows_to_drop, errors="ignore")

    key_cols = df.columns[0:13]   # No〜実施日数
    date_cols = df.columns[13:]   # 日付列全部

    df_long = df.melt(
        id_vars=key_cols,
        value_vars=date_cols,
        var_name="日付",        # 元の列名（24日(金) など）が入る
        value_name="日付実績"   # セルの中身（@ など）が入る
    )

    # イベント情報別にソートする
    df_long = df_long.sort_values(by=list(key_cols)).reset_index(drop=True)

    output_path = "./output_縦持ち.xlsx"

    df_long.to_excel(output_path, index=False)

    print("フォーマット完了:", output_path)

if __name__ == "__main__":
    main()
