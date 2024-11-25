@echo on
chcp 65001 > nul

REM ログファイルの設定
set LOG_FILE=log.txt
echo > %LOG_FILE%

REM バッチファイルのパスを取得（バッチファイルがあるディレクトリ）
set BIN_DIR=%~dp0
set PROJECT_ROOT=%BIN_DIR%..\..
echo バッチファイルのパス: %BIN_DIR% >> %LOG_FILE%


REM requirements.txt のパスを固定
set REQUIREMENTS_FILE=%BIN_DIR%requirements.txt
if not exist "%REQUIREMENTS_FILE%" (
    echo ERROR: requirements.txt が見つかりませんでした。 >> %LOG_FILE%
    exit /b 1


REM 仮想環境の作成（初回のみ）
if not exist "%VENV_DIR%" (
    echo Creating virtual environment... >> %LOG_FILE%
    python -m venv "%VENV_DIR%" >> %LOG_FILE% 2>&1
    if errorlevel 1 (
        echo ERROR: 仮想環境の作成に失敗しました。 >> %LOG_FILE%
        exit /b 1
    )
) else (
    echo 仮想環境が既に存在します。 >> %LOG_FILE%
)

REM 仮想環境を有効化
call "%VENV_DIR%\Scripts\activate"


if not exist "%VENV_DIR%\Scripts\activate" (
    echo ERROR: 仮想環境の有効化スクリプトが見つかりませんでした。 >> %LOG_FILE%
    exit /b 1
)
call "%VENV_DIR%\Scripts\activate"


REM requirements.txt のインストール（初回のみ）
set INSTALL_FLAG=%BIN_DIR%requirements_installed.flag
if not exist "%INSTALL_FLAG%" (
    echo Installing requirements from %REQUIREMENTS_FILE% >> %LOG_FILE%
    pip install --upgrade pip >> %LOG_FILE% 2>&1
    pip install -r "%REQUIREMENTS_FILE%" >> %LOG_FILE% 2>&1
    if errorlevel 1 (
        echo ERROR: requirements.txt のインストールに失敗しました。 >> %LOG_FILE%
        exit /b 1
    )
    type nul > "%INSTALL_FLAG%"
) else (
    echo Requirements already installed. Skipping installation. >> %LOG_FILE%
)


REM Flow.py を検索
for /r "%PROJECT_ROOT%" %%f in (Flow.py) do (
    set MAIN_FILE=%%f
    goto :found_main
)
:found_main

REM 仮想環境のディレクトリ
set VENV_DIR=%BIN_DIR%venv

REM 仮想環境を作成（初回のみ）
if not exist "%VENV_DIR%" (
    echo Creating virtual environment... >> %LOG_FILE%
    python -m venv "%VENV_DIR%" >> %LOG_FILE% 2>&1
    if errorlevel 1 (
        echo ERROR: 仮想環境の作成に失敗しました。 >> %LOG_FILE%
        exit /b 1
    )
) else (
    echo 仮想環境が既に存在します。 >> %LOG_FILE%
)

REM 仮想環境を有効化
call "%VENV_DIR%\Scripts\activate"

REM requirements.txt のインストール（初回のみ）
if defined REQUIREMENTS_FILE (
    set INSTALL_FLAG=%BIN_DIR%requirements_installed.flag
    if not exist "%INSTALL_FLAG%" (
        echo Installing requirements from %REQUIREMENTS_FILE% >> %LOG_FILE%
        pip install --upgrade pip >> %LOG_FILE% 2>&1
        pip install -r "%REQUIREMENTS_FILE%" >> %LOG_FILE% 2>&1
        if errorlevel 1 (
            echo ERROR: requirements.txt のインストールに失敗しました。 >> %LOG_FILE%
            exit /b 1
        )
        echo Installation complete. Creating flag file. >> %LOG_FILE%
        type nul > "%INSTALL_FLAG%"
    ) else (
        echo Requirements already installed. Skipping installation. >> %LOG_FILE%
    )
) else (
    echo ERROR: requirements.txt が見つかりませんでした。 >> %LOG_FILE%
    exit /b 1
)

REM main.py の実行
if defined MAIN_FILE (
    echo Running main.py from %MAIN_FILE%... >> %LOG_FILE%
    python "%MAIN_FILE%" >> %LOG_FILE% 2>&1
    if errorlevel 1 (
        echo ERROR: main.py の実行中にエラーが発生しました。 >> %LOG_FILE%
        exit /b 1
    )
) else (
    echo ERROR: main.py が見つかりませんでした。 >> %LOG_FILE%
    exit /b 1
)

REM 仮想環境を無効化
deactivate

REM 正常終了メッセージ
echo バッチファイルの実行が完了しました。 >> %LOG_FILE%
pause
