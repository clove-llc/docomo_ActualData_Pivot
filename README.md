# excel-table-transposer

Excel の「横持ちテーブル（1 行に日付が横に並んでいる形式）」を  
「縦持ちテーブル（イベント情報 + 日付 + 日付実績）」に変換するためのスクリプトです。

---

## ディレクトリ構成

リポジトリ直下は以下のような構成を想定しています。

```text
excel-table-transposer/
  ├ .venv/              # 仮想環境（任意）
  ├ input_files/        # 入力用 Excel を置くフォルダ
  ├ output_files/       # 変換結果の Excel が出力されるフォルダ
  ├ .gitignore
  ├ README.md
  ├ requirements.txt
  └ transform_excel.py  # 実行スクリプト
````

---

## 初回セットアップ手順

1. **リポジトリをクローン**
```bash
git clone <このリポジトリのURL>
cd excel-table-transposer
```

2. **仮想環境の作成（任意）**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows の場合: .venv\Scripts\activate
```

3. **ライブラリのインストール**
```bash
pip install -r requirements.txt
```

4. **フォルダの準備**

まだ無い場合は、`input_files` と `output_files` を作成します。
```bash
mkdir -p input_files output_files
```

---

## 使い方

1. **入力ファイルを配置**

変換したい Excel ファイル（例: `docomo.xlsx`）を`input_files` フォルダの中に置きます。
```text
input_files/
  └ docomo_2025-11.xlsx   ← ここに置く
```

2. **スクリプトを実行**

プロジェクトのルートディレクトリ（`transform_excel.py` がある場所）で実行します。
```bash
python transform_excel.py
```

3. **実行時の入力（対話式）**

実行すると、以下のようにコマンドラインから順に質問されます。

   1. **入力ファイル名**

      ```text
      input_files内にあるファイル名を入力してください（例: input.xlsx）:
      ```

      → 例: `docomo_2025-11.xlsx`

      ※ `input_files/` のパスは自動で付くので、ファイル名だけ入力してください。

   2. **シート名**

      ```text
      シート名を入力してください:
      ```

      → 例: `11月会場別実績`

      （Excel で下に表示されるシート名そのままを入力します）

   3. **出力ファイル名**

      ```text
      出力ファイル名を入力してください（例: output.xlsx）:
      ```

      → 例: `docomo_2025-11_long.xlsx`

      出力先は `output_files/` 配下になります。

4. **出力の確認**

   正常に終了すると、`output_files/` に指定したファイル名で出力されます。

   ```text
   output_files/
     └ docomo_2025-11_long.xlsx
   ```

   コマンドラインには次のように表示されます。

   ```text
   フォーマット完了: ./output_files/docomo_2025-11_long.xlsx
   ```

---

## スクリプトの処理内容

`transform_excel.py` は、ざっくり以下の流れで処理します。

```python
import pandas as pd

def main():
    input_file_name = input("input_files内にあるファイル名を入力してください（例: input.xlsx）: ")
    input_file_path = "./input_files/" + input_file_name.strip()
    sheet_name = input("シート名を入力してください: ")

    # Excelファイルを読み込む
    df = pd.read_excel(
        input_file_path,
        sheet_name=sheet_name,
        header=5,      # ← Excel 上の 6 行目をヘッダーとして扱う設定（必要に応じて変更）
        usecols="B:BG" # ← B〜BG列だけを使用
    )

    # 不要な上部行を削除する場合の例（今はコメントアウト）
    # rows_to_drop = range(1, 50)
    # df = df.drop(index=rows_to_drop, errors="ignore")

    key_cols = df.columns[0:13]   # No〜実施日数（イベント情報列）
    date_cols = df.columns[13:]   # 日付列全部

    # 横持ち → 縦持ち
    df_long = df.melt(
        id_vars=key_cols,
        value_vars=date_cols,
        var_name="日付",        # 元の列名（例: 24日(金)）
        value_name="日付実績"   # セルの中身（例: @）
    )

    # イベント情報でソート
    df_long = df_long.sort_values(by=list(key_cols)).reset_index(drop=True)

    output_file_name = input("出力ファイル名を入力してください（例: output.xlsx）: ")
    output_path = "./output_files/" + output_file_name

    df_long.to_excel(output_path, index=False)
    print("フォーマット完了:", output_path)

if __name__ == "__main__":
    main()
```

### 前提としているフォーマット

* **ヘッダー行**: Excel 上の 6 行目（Python では `header=5` として指定）
* **使用する列**: B〜BG 列（`usecols="B:BG"`）
* **キー列（イベント情報）**: 先頭から 13 列分（`df.columns[0:13]`）
* **日付列**: 14 列目以降（`df.columns[13:]`）

### 出力される列

出力ファイルは、

* 元のイベント情報（No, 実施月, …, 実施日数）
* `日付` 列
* `日付実績` 列

という構成になります。

---

## カスタマイズのポイント

### 1. ヘッダー行が違う場合

ヘッダー行の位置がファイルによって違う場合は、以下を変更してください。

```python
df = pd.read_excel(
    input_file_path,
    sheet_name=sheet_name,
    header=5,      # ← ここを変更（Excel 上のヘッダー行 - 1）
    usecols="B:BG"
)
```

例）Excel の 4 行目がヘッダーなら `header=3` にする。

### 2. 使用する列の範囲が違う場合

列範囲が B〜BG 以外の場合は `usecols` を変更します。

```python
usecols="C:AZ"
```

のように指定可能です。

### 3. キー列・日付列の範囲が違う場合

イベント情報の列数が変わる場合は、ここを調整してください。

```python
key_cols = df.columns[0:13]   # 0〜12列目
date_cols = df.columns[13:]   # 13列目以降
```

---
