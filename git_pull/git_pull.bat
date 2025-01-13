@echo off
setlocal

rem ����Ƿ��ṩ��·������
if "%~1"=="" (
    echo ���ṩһ��·����Ϊ����
    exit /b 1
)

rem ��ȡ�����·��
set "root_dir=%~1"

rem ���·���Ƿ����
if not exist "%root_dir%" (
    echo ·��������: %root_dir%
    exit /b 1
)

rem ������Ŀ¼�µ������ļ���
for /d %%d in ("%root_dir%\*") do (
    if exist "%%d\.git" (
        echo ����ִ�� git pull: %%d
        pushd "%%d"
        git pull
        popd
    )
)

endlocal