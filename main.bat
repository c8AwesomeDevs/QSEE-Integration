cd C:\Users\simeq\Developments\QSEEIntegration\QSEE-Integration
set datetimef=%date:~-4%%date:~3,2%%date:~0,2%
set std_out_log=logs\%datetimef%_std.out
set std_err_log=logs\%datetimef%_std.err
..\venv\Scripts\python.exe test.py 1>> %std_out_log% 2>> %std_err_log%
