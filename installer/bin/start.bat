@echo off
REM バッチファイルのパスを取得
set BIN_DIR=%~dp0
set PROJECT_ROOT=%BIN_DIR%..\..

REM requirements.txt をバッチファイルの基準位置から検索
for /r "%PROJECT_ROOT%" %%f in (requirements.txt) do (
    set REQUIREMENTS_FILE=%%f
    goto :found_requirements
)
:found_requirements

REM main.py をバッチファイルの基準位置から検索
for /r "%PROJECT_ROOT%" %%f in (main.py) do (
    set MAIN_FILE=%%f
    goto :found_main
)
:found_main

REM 仮想環境を作成（初回のみ）
if not exist "%BIN_DIR%venv" (
    echo Creating virtual environment...
    python -m venv "%BIN_DIR%venv"
)

REM 仮想環境を有効化
call "%BIN_DIR%venv\Scripts\activate"

REM requirements.txt のインストール（初回のみ）
if defined REQUIREMENTS_FILE (
    set INSTALL_FLAG=%BIN_DIR%requirements_installed.flag
    if not exist "%INSTALL_FLAG%" (
        echo Installing requirements from %REQUIREMENTS_FILE%...
        pip install --upgrade pip
        pip install -r "%REQUIREMENTS_FILE%"
        echo Installation complete. Creating flag file.
        type nul > "%INSTALL_FLAG%"
    ) else (
        echo Requirements already installed. Skipping installation.
    )
) else (
    echo ERROR: requirements.txt not found! Ensure it exists in the project directory.
    exit /b 1
)

REM main.py の実行
if defined MAIN_FILE (
    echo Running main.py from %MAIN_FILE%...
    python "%MAIN_FILE%"
) else (
    echo ERROR: main.py not found! Ensure it exists in the project directory.
    exit /b 1
)

REM 仮想環境を無効化
deactivate
