#!/bin/bash
set -e

DATA_DIR="/home/support/data_for_api"
PPS_DB="/home/protei/Protei-PPS/Server/data/data.sqlite"
MKD_JSON="/home/protei/Protei-MKD/MKD/profiles/registrations.db"
LOG_FILE="$DATA_DIR/script.log"

# Создаем лог-файл, если его нет
mkdir -p "$DATA_DIR"
touch "$LOG_FILE"

# Перенаправляем весь вывод в лог и терминал
exec > >(tee -a "$LOG_FILE") 2>&1

function init_setup {
    echo "🔧 Инициализация..."
    mkdir -p "$DATA_DIR"
    echo "📦 Копирование базы данных с ППС..."
    cp "$PPS_DB" "$DATA_DIR/phones.sqlite"
    echo "📦 Копирование json с МКД..."
    cp "$MKD_JSON" "$DATA_DIR/reg_from_mkd.json"
    echo "🚀 Запуск скрипта sqlite_driver.py..."
    python3 sqlite_driver.py
    echo "✅ Инициализация завершена."
}

function add_new_users {
    echo "➕ Добавление новых абонентов..."
    cp "$PPS_DB" "$DATA_DIR/phones.sqlite"
    cp "$MKD_JSON" "$DATA_DIR/reg_from_mkd.json"
    python3 sqlite_driver.py
    echo "✅ Абоненты добавлены."
}

function update_ips {
    echo "🌐 Обновление IP адресов..."
    cp "$MKD_JSON" "$DATA_DIR/reg_from_mkd.json"
    python3 json_update.py
    echo "✅ IP адреса обновлены."
}

echo "============================"
echo "📅 $(date '+%Y-%m-%d %H:%M:%S') — запуск скрипта"
echo "Выберите действие:"
echo "1. 🔧 Инициализация (первая выгрузка данных)"
echo "2. ➕ Добавить новых пользователей"
echo "3. 🌐 Обновить IP адреса"
read -p "Введите номер действия (1/2/3): " choice

case "$choice" in
    1) init_setup ;;
    2) add_new_users ;;
    3) update_ips ;;
    *) echo "❌ Неверный выбор. Завершение."; exit 1 ;;
esac

echo "📦 Все действия завершены. Лог: $LOG_FILE"
