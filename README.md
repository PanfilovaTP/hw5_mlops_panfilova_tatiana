# HW5 MLOps Panfilova Tatiana

## Цель проекта

Цель проекта — собрать минимальный воспроизводимый MLOps-контур для учебного эксперимента:

- код версионируется через Git;
- данные и артефакты версионируются через DVC;
- обучение оформлено как DVC-пайплайн;
- параметры и метрики логируются в MLflow;
- подготовлена конфигурация Feature Store.

## Структура проекта

```text
.
├── data/
│   ├── raw/
│   │   └── data.csv.dvc
│   └── processed/
├── postgres_repo/
│   └── feature_repo/
│       └── feature_store.yaml
├── src/
│   ├── prepare.py
│   └── train.py
├── dvc.yaml
├── params.yaml
├── requirements.txt
└── HW5_MLOps_Panfilova_Tatiana.ipynb
```

## Как запустить

```после клонирования/скачивания репозитория

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
dvc pull
dvc repro

mlflow ui --backend-store-uri sqlite:///mlflow.db
```

MLflow UI будет доступен по адресу:

```text
http://127.0.0.1:5000
```

## Краткое описание пайплайна

В проекте реализован DVC-пайплайн из двух стадий:

1. `prepare` — читает исходные данные, выполняет базовую обработку, делит данные на train/test и сохраняет результат в `data/processed/`.
2. `train` — обучает модель `LogisticRegression`, сохраняет модель в `model.pkl` и логирует параметры и метрики в MLflow.

Параметры эксперимента вынесены в `params.yaml`.

## Где смотреть MLflow

После запуска команды:

```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

откройте в браузере:

```text
http://127.0.0.1:5000
```

В MLflow отображаются параметры модели, метрика `accuracy` и артефакт `model.pkl`.

## Feature Store

В проекте используется Feast. Конфигурация находится в файле:

```text
postgres_repo/feature_repo/feature_store.yaml
```

В конфигурации используется PostgreSQL для `registry`, `online_store` и `offline_store`.

Для локального запуска PostgreSQL можно использовать Docker:

```powershell
docker run --name feast-postgres -e POSTGRES_USER=tuser -e POSTGRES_PASSWORD=12345 -e POSTGRES_DB=mydb -p 5433:5432 -d postgres:16
```

Запуск Feast UI:

```powershell
feast -c postgres_repo/feature_repo ui --host 127.0.0.1 --port 8889
```

Feast UI будет доступен по адресу:

```text
http://127.0.0.1:8889
```

## Схема ML-системы для размытия лиц

Схема ML-системы для размытия лиц на видео приведена в ноутбуке:

```text
HW5_MLOps_Panfilova_Tatiana.ipynb
```

В схеме показаны основные этапы: загрузка видео, разбиение на кадры, параллельная обработка, детекция лиц, размытие найденных областей, сборка итогового видео и сохранение результата.
