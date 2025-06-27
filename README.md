# zaim-csv-download

Zaim に自動ログインし、指定した期間の CSV データをダウンロードします

## 必要な環境

このスクリプトを実行する前に、以下の環境が整っていることを確認してください。

- **Python 3.6 以上**: Python がシステムにインストールされている必要があります。
- **Zaim アカウント**: 有効な Zaim アカウントと、必要な認証情報が必要です。
- **環境変数**: 以下の環境変数を設定してください。
  - `ZAIM_ID`: Zaim アカウントの ID(メールアドレス)。
  - `ZAIM_PASSWORD`: Zaim アカウントのパスワード。

## セットアップ

1.  **Python のインストール**: Python がインストールされていない場合は、[python.org](https://www.python.org/downloads/) からダウンロードしてインストールしてください。
2.  **依存関係のインストール**: ターミナルを開き、以下のコマンドを実行してください。

    ```bash
    pip install -r requirements.txt
    ```

3.  **環境変数の設定**: `ZAIM_ID` と `ZAIM_PASSWORD` の環境変数を設定してください。ターミナルまたはシステムの環境設定で設定できます。

    - **Linux/macOS**:

      ```bash
      export ZAIM_ID="あなたのZaimID@example.com"
      export ZAIM_PASSWORD="あなたのZaimパスワード"
      ```

    - **Windows**:

      ```powershell
      $env:ZAIM_ID="あなたのZaimID@example.com"
      $env:ZAIM_PASSWORD="あなたのZaimパスワード"
      ```

## 使い方

スクリプトを実行するには、以下のコマンドを使用します。

```bash
python download.py <開始年> <開始月> <開始日> <終了年> <終了月> <終了日> [オプション]
```

### 引数

- `<開始年>`: データダウンロードを開始する年(例: 2020)。
- `<開始月>`: データダウンロードを開始する月(例: 01)。
- `<開始日>`: データダウンロードを開始する日(例: 01)。
- `<終了年>`: データダウンロードを終了する年(例: 2021)。
- `<終了月>`: データダウンロードを終了する月(例: 12)。
- `<終了日>`: データダウンロードを終了する日(例: 31)。

### オプション

- `-t, --totp`: 2 段階認証コード(有効な場合)。
- `-c, --charset`: 出力ファイルの文字コード。選択肢: `utf8`, `sjis`。デフォルト: `utf8`。
- `-o, --outputdir`: `~/Downloads` 以下の出力ディレクトリ。デフォルト: `selenium_downloads`。
- `--prompt_for_download`: ダウンロード確認のプロンプトを有効にする。
- `-v, --verbose`: デバッグ用の詳細ログを有効にする。

### 例

1. **基本的な使い方**:

   ```bash
   python download.py 2024 01 01 2024 01 31
   ```

2. **TOTP コードを使用する場合**:

   ```bash
   python download.py 2024 01 01 2024 01 31 -t 123456
   ```

3. **出力ディレクトリを指定する場合**:

   ```bash
   python download.py 2024 01 01 2024 01 31 -o zaim_data
   ```

4. **詳細ログを有効にする場合**:

   ```bash
   python download.py 2024 01 01 2024 01 31 -v
   ```

## 出力

スクリプトは、Zaim のデータを CSV ファイルとしてダウンロードし、指定された出力ディレクトリ(またはデフォルトの `~/Downloads/selenium_downloads`)に保存します。ファイル名は以下の形式で自動的に生成されます。

`zaim_data_<開始年><開始月><開始日>_<終了年><終了月><終了日>_YYYYMMDDHHMMSSmm.csv`

各項目の意味は以下の通りです。

- `YYYYMMDDHHMMSSmm` は、ダウンロードが完了した日時です。

## トラブルシューティング

- **"WebDriverException: Message: 'chromedriver' executable needs to be in PATH"**:
  - ChromeDriver が正しくインストールされ、システムの PATH にアクセス可能であることを確認してください。Selenium が自動的に処理するはずですが、手動での介入が必要になる場合があります。
- **"ValueError: Environment variables ZAIM_ID and ZAIM_PASSWORD must be set."**:
  - `ZAIM_ID` と `ZAIM_PASSWORD` の環境変数が正しく設定されていることを確認してください。
- **スクリプトがページ上の要素を見つけられない**:
  - Zaim の Web サイトのレイアウトが変更された可能性があります。ブラウザの開発者ツールを使用して要素を調査し、スクリプトを適宜更新してください。
- **ダウンロードが失敗またはタイムアウトする**:
  - インターネット接続を確認し、Zaim の Web サイトにアクセスできることを確認してください。

## 免責事項

このスクリプトは現状有姿で提供され、その使用から生じる可能性のある問題について、私は一切責任を負いません。責任を持って、ご自身の責任で使用してください。

---

This README file was generated with assistance from GitHub Copilot.
