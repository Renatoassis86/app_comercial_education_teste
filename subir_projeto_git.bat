@echo off
echo Iniciando push para o GitHub...

cd /d C:\Users\renato\Desktop\repositorio_comerciacve\paideia_app

git init
git remote set-url origin https://github.com/Renatoassis86/app_comercial_education.git
git add .
git commit -m "Atualização do projeto Paideia App"
git pull origin main --rebase
git push origin main

echo Operação concluída com sucesso!
pause
