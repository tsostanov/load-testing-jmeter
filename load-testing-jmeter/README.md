# Load Testing with Apache JMeter

Учебный проект по нагрузочному и стресс-тестированию веб-сервиса с помощью **Apache JMeter** и последующему анализу результатов в **Python**.

Проект показывает полный мини-пайплайн:

- подготовка JMeter test plan для load testing и stress testing;
- настройка виртуальных пользователей, ramp-up, duration и target throughput;
- запуск HTTP-сценариев из CLI;
- сохранение результатов в `.jtl`;
- анализ `response time`, `throughput`, `error rate`, HTTP 500/503;
- построение графиков по результатам тестирования.

> Все реальные адреса, токены и пользовательские параметры заменены на демо-значения. Репозиторий безопасен для публичной публикации.

## Стек

- Apache JMeter
- Python 3
- pandas
- matplotlib
- HTTP / REST basics
- Linux / CLI

## Структура проекта

```text
.
├── jmeter/
│   ├── load-test.jmx          # нагрузочное тестирование
│   └── stress-test.jmx        # стресс-тестирование
├── scripts/
│   └── analyze_jtl.py         # анализ JTL/CSV результатов
├── results/
│   ├── sample/                # обезличенные примеры результатов
│   └── analysis/              # выходные отчёты и графики
├── docs/
│   └── methodology.md         # краткая методика тестирования
├── requirements.txt
└── README.md
```

## Быстрый старт

Установить зависимости для анализа результатов:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Построить сводку и графики по sample-результатам:

```bash
python scripts/analyze_jtl.py results/sample/stress_503_sample.csv --out results/analysis
```

После выполнения появятся:

```text
results/analysis/summary.csv
results/analysis/response_time_over_time.png
results/analysis/throughput_over_time.png
results/analysis/response_codes.png
```

## Запуск JMeter из CLI

Пример нагрузочного теста:

```bash
jmeter -n \
  -t jmeter/load-test.jmx \
  -l results/raw/load_config3.jtl \
  -Jhost=example.com \
  -Jport=8080 \
  -Jtoken=DEMO_TOKEN \
  -Juser=DEMO_USER \
  -Jconfig=3 \
  -Jusers=13 \
  -Jramp_up=13 \
  -Jduration=120 \
  -Jthroughput=260
```

Пример стресс-теста:

```bash
jmeter -n \
  -t jmeter/stress-test.jmx \
  -l results/raw/stress_260.jtl \
  -Jhost=example.com \
  -Jport=8080 \
  -Jtoken=DEMO_TOKEN \
  -Juser=DEMO_USER \
  -Jconfig=3 \
  -Jusers=260 \
  -Jramp_up=15 \
  -Jduration=90 \
  -Jthroughput=10000
```

Для Windows можно использовать `jmeter.bat` вместо `jmeter`.

## Что анализируется

Скрипт `scripts/analyze_jtl.py` считает:

- количество запросов;
- среднее, минимальное и максимальное время ответа;
- p90 / p95 / p99 latency;
- процент ошибок;
- throughput;
- распределение HTTP-кодов ответа.

## Пример результата

В sample-данных есть сценарий стресс-тестирования, где при повышенной нагрузке появляются ответы **HTTP 503 Service Unavailable**. Это показывает момент, когда сервис перестаёт стабильно обрабатывать входящие запросы.

## Как это можно описать в резюме

```text
Load Testing Project — JMeter, Python, HTTP, Linux
Проект по нагрузочному и стресс-тестированию веб-сервиса: JMeter test plans, запуск из CLI, анализ JTL-результатов, графики response time/throughput/error rate и исследование HTTP 500/503.
```
