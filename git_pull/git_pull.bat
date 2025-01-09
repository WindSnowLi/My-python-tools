@echo off
setlocal

rem 检查是否提供了路径参数
if "%~1"=="" (
    echo 请提供一个路径作为参数
    exit /b 1
)

rem 获取输入的路径
set "root_dir=%~1"

rem 检查路径是否存在
if not exist "%root_dir%" (
    echo 路径不存在: %root_dir%
    exit /b 1
)

rem 遍历根目录下的所有文件夹
for /d %%d in ("%root_dir%\*") do (
    if exist "%%d\.git" (
        echo 正在执行 git pull: %%d
        pushd "%%d"
        git pull
        popd
    )
)

endlocal