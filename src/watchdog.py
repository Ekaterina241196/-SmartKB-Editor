import os
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

import requests  # Раскомментировать при реальном запуске с API

# Загрузка промпта
from prompts import SYSTEM_PROMPT

load_dotenv()


def load_data():
    """Заглушка для загрузки данных. В реальности читать из файлов или API."""
    articles = [
        {"id": 1, "title": "Как изменить цену", "text": "Нажмите кнопку 'Автопродвижение'..."},
        {"id": 2, "title": "Создание объявления", "text": "Нажмите кнопку 'Подать объявление'..."}
    ]
    releases = [
        {"version": "v24.8", "text": "Функция 'Автопродвижение' удалена."},
        {"version": "v24.7", "text": "Кнопка 'Подать объявление' переименована в 'Разместить'."}
    ]
    return articles, releases


def analyze_with_llm(article, releases):
    """Функция вызова LLM. Сейчас возвращает мок-ответ для демонстрации."""
    # Здесь будет код вызова requests.post(LLM_URL, ...)
    # Для демо вернем фейковый результат на основе ключевых слов
    issues = []
    if "Автопродвижение" in article["text"]:
        issues.append({
            "article": article["title"],
            "type": "Удаленная функция",
            "quote": "Нажмите кнопку 'Автопродвижение'",
            "change": "Функция удалена в v24.8",
            "recommendation": "Переписать статью или скрыть",
            "priority": "🔴 Высокий"
        })
    if "Подать объявление" in article["text"]:
        issues.append({
            "article": article["title"],
            "type": "Устаревший термин",
            "quote": "Нажмите кнопку 'Подать объявление'",
            "change": "Переименована в 'Разместить' (v24.7)",
            "recommendation": "Заменить название кнопки",
            "priority": "🟡 Средний"
        })
    return issues


def generate_report(issues):
    """Генерация Markdown отчета."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"output/report_{date_str}.md"

    md_content = f"# 🛡 Отчет Content Watchdog\n**Дата:** {date_str}\n\n"

    if not issues:
        md_content += "✅ Проблем не найдено.\n"
    else:
        md_content += "## Найдены проблемы:\n\n"
        md_content += "| Статья | Проблема | Цитата | Изменения | Рекомендация | Приоритет |\n"
        md_content += "|---|---|---|---|---|---|\n"
        for issue in issues:
            md_content += f"| {issue['article']} | {issue['type']} | {issue['quote']} | {issue['change']} | {issue['recommendation']} | {issue['priority']} |\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ Отчет сохранен: {filename}")
    return filename


def main():
    print("🚀 Запуск Content Watchdog...")
    articles, releases = load_data()

    all_issues = []
    for article in articles:
        print(f"🔍 Анализ статьи: {article['title']}")
        issues = analyze_with_llm(article, releases)
        all_issues.extend(issues)

    generate_report(all_issues)
    print("🏁 Готово!")


if __name__ == "__main__":
    main()
