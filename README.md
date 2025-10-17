**20251017 基本操作をコマンドで実行する機能を実装しました。AU取得、統計情報の表示、分析グラフの表示などは全てshell.py実行後に表示されるプロンプトにコマンドを入力して実行できます。**

**20250906　データベースの構成を変更しました。一度main_table及びAU_tableを削除して、再度実行してください**

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

https://www.docker.com/ja-jp/products/docker-desktop/からDockerDesktop をインストールする。

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

1. 下記のサイトからPostgreSQLのインストーラをダウンロードする。 https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
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

https://database-client.com/が提供する拡張機能PostgreSQLをインストールしておくとよい。

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
- done
    - 撮影した動画のうち、表情分析が実行済みのものを格納するためのディレクトリ
- output
    - 表情分析の出力結果（CSVファイル）を格納するためのディレクトリ
- result
    - グラフなど、CSVを分析した結果を格納するためのディレクトリ
- modules
    - 分析を行う各種スクリプトファイルを格納するためのディレクトリ
- commands **（20251017追加）**
    - 各種操作をコマンドラインで実行するためのスクリプトファイルを格納するためのディレクトリ

## 実行手順 **（20251017変更）**

1. 分析したい顔動画をInputディレクトリに格納
    1. 複数の動画を一斉に分析することが可能
    2. 10秒以上の動画である必要がある
2. shell.pyを実行
    1.プロンプト（>）が表示される。
    2. OpenFaceによる表情分析、AU統計分析、データベース登録を一括で実行するにはAUAnalyzeコマンドを実行
        1. 撮影者と日付を聞かれるので入力する（日付はyyyymmddHHMMss型）
        2. 動画撮影アプリでエクスポートした全記録データを用いたいので、今後自動化する
    3. Inputの動画を完了済みディレクトリdoneに移すには、moveコマンドを実行

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
