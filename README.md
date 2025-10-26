- **20251026**
    - **データベースの構成を変更しました。一度main_table及びAU_tableを削除して、再度実行してください。**
    - **機械学習用データセットを生成する機能を実装しました。動画分析後、コマンドdatasetを実行することでCSVファイルを生成します。**
- **20251017**
    - **基本操作をコマンドで実行する機能を実装しました。AU取得、統計情報の表示、分析グラフの表示などは全てshell.py実行後に表示されるプロンプトにコマンドを入力して実行できます。**
- **20250906**
    - **データベースの構成を変更しました。一度main_table及びAU_tableを削除して、再度実行してください。**

# 概要（20251026追加）

このリポジトリは、疲労分析システムで使用される機械学習用データセットを生成するプログラムである。専用のAndroidアプリ（FatigueFaceCapture）で記録したデータを指定のディレクトリに格納しコマンドを実行することで、データセットを作成することができる。また、顔動画の分析結果を表示するデータ可視化のコマンドも実装されている。

# プログラム説明

## データベース

## 撮影動画の読み込み（20251026変更）

動画撮影アプリFatigueFaceCaptureを用いて撮影した動画を分析しデータセットに追加する前段階として、以下の操作を行う。

1. 分析したい顔動画をInputディレクトリに格納
    1. 複数の動画を一斉に分析することが可能
    2. 10秒以上の動画である必要がある
2. FatigueFaceCaptureの「開発者モード」をタップし出力されたJsonファイルを、本リポジトリのjsonディレクトリに格納する。

## 各種コマンド（20251026変更）

顔動画分析やデータ可視化、データセットの作成などは全てコマンドを通して実行する。commandsディレクトリにあるshell.pyを実行するとプロンプトが立ち上がる。

- AUAnalyze
    - Inputディレクトリにある動画とjsonディレクトリにあるJSONファイルを解析し、以下の処理を行う
        - 顔動画の分析：AUなど各種時系列データを取得し、outputディレクトリにCSVファイルが出力される
        - AU時系列データ分析：トレンドノイズ分離、基本統計量（平均、分散）、ピーク点検出を行う
        - DB登録：AU時系列データ分析の結果や、FatigueFaceCaptureにて記録したユーザ情報、主観疲労度など、データセット生成に必要な全てのデータをデータセットに保存する
    - コマンドオプション
        - なし
- dataset
    - データベースに保存されているデータから、機械学習用データセットを生成する
    - 出力形式はCSV
    - コマンドオプション
        - `-s`(必須): 出力期間の開始日の指定（yyyymmdd形式）
        - `-e`(必須): 出力期間の終了日の指定（yyyymmdd形式）
        - `-person`(必須): 出力対象のユーザを指定（複数指定可能、カンマで区切る）
- move
    - Inputディレクトリ内のすべての動画及びjsonディレクトリ内の全てのJSONファイルを、doneディレクトリに移動する
    - 分析が未実行でも実行可能であるため注意。
- trend
    - AU時系列データを大きな変動（トレンド）と揺らぎ（ノイズ）に分離したグラフを出力する
    - コマンドオプション
        - `-date(必須)`: 日付
        - `-person(必須)`: 撮影者
        - `-au`: AU番号
        - `-all`(フラグ): 全てのAUを表示する。`-au` オプションの指定は不要
- peaks
    - AU時系列データからピーク点を検出し赤い点で表示する
    - コマンドオプション
        - -`date`(必須): 日付
        - `-person`(必須): 撮影者
        - `-au`: AU番号
        - `-all`(フラグ): 全てのAUを表示する。`-au` オプションの指定は不要
- stats
    - 各種AU時系列データの基本統計量をログで表示する。
    - コマンドオプション
        - `-date`(必須): 日付
        - `-person`(必須): 撮影者
        - `-au`: AU番号
        - `-all`(フラグ): 全てのAUを表示する。`-au` オプションの指定は不要
- EOF
    - コマンド インタープリタを終了する

# 導入手順

## Venv導入

本プロジェクトでは仮想環境Venvを使用する。以下のコマンドを実行し仮想環境を構築、アクティベートする。

```powershell
python -m venv .venv
```

```powershell
.venv/scripts/activate
```

requirements.txtには本プロジェクトで使用するパッケージの一覧が記載されている。以下のコマンドを実行し、それらをすべてインストールする。

```powershell
pip install -r requirements.txt
```

## Configファイルの作成

環境依存の設定をConfigに追加する。

1. config_sample.ps1をコピペし、同じ場所に新規ファイルconfig.ps1を作成
2. modulesディレクトリにあるdb_config_sample.pyをコピペし、同じ場所に新規ファイルdb_config.pyを作成

config.ps1はOpenFaceセットアップ後に、db_config.pyはSQL導入後に設定を記述する。

## OpenFace導入

表情分析にはOpenFaceを使用する。環境構築にはDockerを使用する。DockerはLinux上でのみ動作するので、Windowsなら事前にWSLをインストールする。

### Docker Desktopの導入

[https://www.docker.com/ja-jp/products/docker-desktop/](https://www.docker.com/ja-jp/products/docker-desktop/)  からDockerDesktopをインストールする。

次にDockerでopenfaceをインストールする。Powershellで以下のコマンドを実行

```bash
docker run -it --rm algebr/openface:latest

```

Dockerデスクトップを開き、コンテナIDとコンテナ名を確認。config.ps1に記述する。

```powershell
$ContainerName = "your_openface_docker_container_name"
$ContainerID = "your_openface_docker_container_id"

```

## SQL導入

1. [https://www.enterprisedb.com/downloads/postgres-postgresql-downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)からPostgreSQLのインストーラをダウンロードする。
 
2. 手順に沿ってインストールする。
    1. 基本的に選択肢はデフォルトのまま
    2. 終了後に起動するStackBuildeは閉じてよい（最後のページのチェックを外せば起動しない）
3. 環境変数のPathにインストールしたPostgreSQLのbinディレクトリのパスを追加
4. `psql —-version` を実行し、インストールしたPostgreSQLのバージョンが表示されれば成功
    1. 反映が遅い場合はターミナルの再起動などを行う。

### 登録情報の設定

環境依存であるProstgreSQLのユーザ名、パスワード、ホスト名をdb_config.pyに記述する。

```python
user_name = "your_user_name"
password = "your_password"
host_name = "localhost"

```

### 拡張機能の導入

[https://database-client.com/](https://database-client.com/)   が提供する拡張機能PostgreSQLをインストールしておくといい
[](https://database-client.com/%E3%81%8C%E6%8F%90%E4%BE%9B%E3%81%99%E3%82%8B%E6%8B%A1%E5%BC%B5%E6%A9%9F%E8%83%BDPostgreSQL%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%97%E3%81%A6%E3%81%8A%E3%81%8F%E3%81%A8%E3%82%88%E3%81%84%E3%80%82)

### データベースの作成

ターミナルで以下を実行する

```powershell
psql -U postgres

```

`postgres` はスーパーユーザ名。パスワードが要求されるので、セットアップ時に設定したものを入力する。

これでデータベースに接続でき、psqlのプロンプト`postgres=#` が表示される。

以下のコマンドを実行し、本プロジェクトで使用するデータベースを作成する。

```powershell
CREATE DATABASE facehealthdb

```

`facehealthdb` はデータベース名。

# プログラム説明

### ディレクトリ構成

- input
    - 撮影した動画のうち、表情分析が未実行のものを格納するためのディレクトリ
- json**（20251026変更）**
    - FatigueFaceCaptureのエクスポート機能で出力されたJSONファイルを格納するディレクトリ
- done
    - 撮影した動画のうち、表情分析が実行済みのものを格納するためのディレクトリ
    - 動画はmovie、JSONはjsonディレクトリに格納される
- output
    - 表情分析の出力結果（CSVファイル）を格納するためのディレクトリ
- result**（20251026変更）**
    - グラフや機械学習用データセットなど、CSVを分析した結果を格納するためのディレクトリ
- modules
    - 分析を行う各種スクリプトファイルを格納するためのディレクトリ
- commands **（20251017追加）**
    - 各種操作をコマンドラインで実行するためのスクリプトファイルを格納するためのディレクトリ

# 開発手順

mainブランチへ直接コミットすることはできない。ブランチを切って作業を行う。

- feature/○○
    - 機能追加など
- Hotfix/〇〇
    - 細かい修正、バグ修正

mainブランチへのプルリクエストは承認が必要

## Issue

修正、機能追加などを依頼するときはIssueを利用する。

Issueを投稿するとチケット番号が発行される。コミットメッセージやプルリクエストのタイトル・Discriptionにチケット番号（半角＃と数字）を含めることで、画像のようにIssueと作業内容を紐づけることができる。作業が完了したらIssueを閉じる。
<img width="893" height="587" alt="Image" src="https://github.com/user-attachments/assets/4faa8b72-ac0a-4712-af6a-9ea9da7363c2" />
