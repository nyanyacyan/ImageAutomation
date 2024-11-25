@echo on
chcp 65001 > nul
set PYTHONIOENCODING=utf-8

REM デバッグ: 開始メッセージ
echo スクリプトを開始します。

REM ログファイルの設定
set LOG_FILE=log.txt
echo > %LOG_FILE%

REM バッチファイルのパスを取得（バッチファイルがあるディレクトリ）
set BIN_DIR=%~dp0
echo BIN_DIR: %BIN_DIR%

set PROJECT_ROOT=%BIN_DIR%..\..
echo PROJECT_ROOT: %PROJECT_ROOT%

set VENV_DIR=%BIN_DIR%venv
echo VENV_DIR: %VENV_DIR%

REM requirements.txt のパスを設定
set REQUIREMENTS_FILE=%PROJECT_ROOT%\installer\bin\requirements.txt
if not exist "%REQUIREMENTS_FILE%" (
    echo ERROR: requirements.txt が見つかりません。
    exit /b 1
)
echo REQUIREMENTS_FILE: %REQUIREMENTS_FILE%

REM 仮想環境の作成（初回のみ）
if not exist "%VENV_DIR%" (
    echo 仮想環境を作成します...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ERROR: 仮想環境の作成に失敗しました。
        exit /b 1
    )
) else (
    echo 仮想環境が既に存在します。
)

REM 仮想環境の有効化
if not exist "%VENV_DIR%\Scripts\activate" (
    echo ERROR: 仮想環境の有効化スクリプトが見つかりませんでした。
    exit /b 1
)
call "%VENV_DIR%\Scripts\activate"
echo 仮想環境が有効化されました。

REM requirements.txt のインストール（初回のみ）
set INSTALL_FLAG=%BIN_DIR%requirements_installed.flag
if not exist "%INSTALL_FLAG%" (
    echo requirements.txt をインストールします...
    pip install --upgrade pip
    pip install -r "%REQUIREMENTS_FILE%"
    if errorlevel 1 (
        echo ERROR: requirements.txt のインストールに失敗しました。
        exit /b 1
    )
    echo > "%INSTALL_FLAG%"
) else (
    echo requirements.txt は既にインストール済みです。
)

REM main.py の検索
for /r "%PROJECT_ROOT%\installer\src" %%f in (main.py) do (
    set MAIN_FILE=%%f
    goto :found_main
)
:found_main
if not defined MAIN_FILE (
    echo ERROR: main.py が見つかりませんでした。
    exit /b 1
)
echo MAIN_FILE: %MAIN_FILE%

REM main.py の実行
echo main.py を実行します...
python "%MAIN_FILE%"
if errorlevel 1 (
    echo ERROR: main.py の実行中にエラーが発生しました。
    exit /b 1
)

REM 仮想環境を無効化
deactivate
echo 仮想環境を無効化しました。

REM 完了メッセージ
echo スクリプトの実行が完了しました。
pause
