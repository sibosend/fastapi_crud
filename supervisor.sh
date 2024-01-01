[program:fastapi_crud]
directory=/root/autodl-tmp/lili/fastapi_crud
command=bash start.sh
autostart=true
autorestart=true
startretries=1
redirect_stderr=true
stdout_logfile=/var/log/supervisor/fastapi_crud.log
environment=ASPNETCORE_ENVIRONMENT="Development"