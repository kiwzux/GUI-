@echo off
title Скрипт компиляции стека
color 0A
echo ========================================
echo   КОМПИЛЯЦИЯ ВСЕХ БИБЛИОТЕК СТЕКА
echo ========================================
echo.

REM --- Компиляция C ---
echo [1/3] Компиляция C библиотеки...
gcc -shared -o stack.dll stack_lib.c
if %errorlevel% equ 0 (
    echo     ✓ Готово: stack.dll
) else (
    echo     ✗ Ошибка компиляции C
)

echo.

REM --- Компиляция C++ ---
echo [2/3] Компиляция C++ библиотеки...
g++ -shared -o stack_cpp.dll stack_cpp.cpp
if %errorlevel% equ 0 (
    echo     ✓ Готово: stack_cpp.dll
) else (
    echo     ✗ Ошибка компиляции C++
)

echo.

REM --- Компиляция Pascal ---
echo [3/3] Компиляция Pascal библиотеки...
fpc -Twin -Cu -B -Xs -o stack_pas.dll stack_pas.pas
if %errorlevel% equ 0 (
    echo     ✓ Готово: stack_pas.dll
) else (
    echo     ✗ Ошибка компиляции Pascal
)

echo.
echo ========================================
echo   ЗАВЕРШЕНО!
echo ========================================
pause