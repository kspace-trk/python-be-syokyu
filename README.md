# Python Backend Railway
Python バックエンド 初級編

## 環境構築
Python Railway の問題を解くために必要な下記ツールのインストール方法と環境構築の手順を解説します。
- Python 3.12
- Docker
- Visual Studio Code
- Git

上記のうち、Visual Studio Code と Git についてのインストール方法は、
[Railway 準備編](https://techbowl.notion.site/Railway-ceba695d5014460e9733c2a46318cdec) をご確認いただき、挑戦の準備をしてください。

その他リポジトリの更新の仕方や、トラブルシューティングについても上記の Railway 準備編にございます。
何かあった際は、まずそちらを確認しましょう。

Python や Docker のセットアップについては、実際にStationに取り組みながら実施していきます。

※以下セットアップテキストへのリンクは実際のStationの中で対応する手順です。<br>
そのため、こちらのリンクは見直す方向けのリンクである事をご留意ください。
- Pythonセットアップ
  - [Windows](./docs/instructions/00_install_python/install_python_windows.md)
  - [MacOS](./docs/instructions/00_install_python/install_python_mac.md)
- Dockerセットアップ
  - [Windows](./docs/instructions/10_install_docker/install_docker_windows.md)
  - [MacOS](./docs/instructions/10_install_docker/install_docker_mac.md)

## このRailwayについて
このRailwayで扱う技術要素やカバーする範囲、利用する開発環境について説明します。

### 扱う技術要素
Python 製 Web アプリケーションフレームワークである FastAPI を使用した WebAPI の開発。

<details>
<summary>FastAPIについて</summary>
FastAPI は Python 言語を使用した、Web アプリケーション向けのフレームワークです。

2018年12月に最初のリリースが行われ、2021年頃から大きくシェアを伸ばし、2023年には Python の Web アプリケーションフレームワークで Django や Flask に次ぐフレームワークに成長しています。

Java 開発者向けの統合開発環境として知名度の高い IntelliJ IDEA などを開発している JetBrains 社の開発者のエコシステムに関するレポートでは、FastAPI の使用率が 25% に増加している事を報告しており、 Django の 40% や Flask の 38% には及ばないものの、過去数年で大きく利用率を伸ばしてきている存在として、注目されています。

FastAPI は容易に WebAPI が開発でき、少ないコードの記述で実装できることや効率的な処理を実現するための仕組み、開発している API を UI 上で確認するための仕組みなど WebAPI の開発を支援する仕組みが標準で組み込まれています。
</details>

### カバーする範囲
今回は実際に動くものを作ってみるという点にフォーカスし、カバーする範囲を以下の通り決めています。

**【凡例】✅:  カバー / ❌: 今回のRailwayでは取り扱わない点**
- ✅ FastAPI を利用した WebAPI ( REST API ) の基本的な開発
- ✅ アプリケーションからリレーショナルデータベースへの連携 ( CRUD 処理 )
- ✅ SwaggerUI を用いた API のお試し実行
- ❎ データベースのテーブル設計
- ❌ SQLAlchemy や Alembic など FastAPI 以外のパッケージ導入
- ❌ REST API の設計
- ❌ 開発環境の構築方法
- ❌ FastAPI のより発展的な利用方法
- ❌ テストコードの実装方法

### 開発環境
![](./docs/images/dev_environment_overview.drawio.png)
- この Railway で使用する開発環境は Docker の仮想環境をアプリケーションの実行環境としています。（環境構築が再現性高くスピーディにおこえる事を目的としている）
- アプリケーション本体用の Docker コンテナである App コンテナ、アプリケーションと連携させるデータベース用のコンテナである DB コンテナの 2 つが、連携して Docker 環境内で稼働する形となります。

#### 言語・バージョン
- Python 3.12

#### 使用ライブラリ
- フレームワーク
    - [FastAPI](https://fastapi.tiangolo.com/ja/) 0.136.3（`fastapi-debug-toolbar` 互換のため 0.137 未満に固定）
    - 開発サーバーは `fastapi dev` を使用
- O/Rマッパー
    - [SQLAlchemy](https://www.sqlalchemy.org/)
- マイグレーションツール
    - [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- テスティングフレームワーク
    - [Pytest](https://docs.pytest.org/en/stable/)
- リンター/フォーマッター
    - [Ruff](https://docs.astral.sh/ruff/)

## 主に使用している VSCode 拡張機能
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

## プロジェクト構造
```
.
├── .techtrain
│   └── TechTrain合格判定用ディレクトリ(触れない)
├── .vscode
│   └── VSコードのワークスペースの設定ファイルが置かれる。(このリポジトリでは、推奨拡張機能の構成ファイルのみ管理しています。)
├── README.md
├── alembic.ini
├── app
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   └── models
│       ├── __init__.py
│       └── (SQLAlchemyのためのモデル定義群)
├── docker-compose.yml
├── docs
│   └── (READMEから参照するドキュメント類)
├── infra
│   └── docker
│       └── (Docker Compose環境に必要なファイル群)
├── migration
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── (DBマイグレーションファイル)
├── pyproject.toml
├── test-outputs
│   └── (TechTrain合格判定用テスト結果レポートファイル格納先)
└── tests
    └── (合格判定用テストコード群)
```
