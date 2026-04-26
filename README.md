# HW5 MLOps Panfilova Tatiana

## Цель проекта

Собрать минимальный воспроизводимый MLOps-контур для учебного эксперимента:

- код версионируется через Git;
- данные и артефакты версионируются через DVC;
- обучение оформлено как DVC-пайплайн из стадий `prepare` и `train`;
- параметры, метрики и артефакты эксперимента логируются в MLflow;
- для задания по Feature Store подготовлен `feature_store.yaml` на основе шаблона `postgres`.

## Структура проекта

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── feature_repo/
│   └── feature_store.yaml
├── models/
├── reports/
├── src/
│   ├── prepare.py
│   └── train.py
├── dvc.yaml
├── params.yaml
├── requirements.txt
└── HW5_MLOps_Panfilova_Tatiana.ipynb
```

## Как запустить

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
dvc pull
dvc repro
mlflow ui --backend-store-uri ./mlruns
```

Команды проверялись в PowerShell на Windows. В `dvc.yaml` стадии запускаются через локальный интерпретатор `.venv\Scripts\python`.

MLflow UI по умолчанию будет доступен по адресу `http://127.0.0.1:5000`.

Если на Windows DVC выдаст ошибку доступа к `C:\ProgramData\iterative`, перед запуском можно один раз выполнить:

```powershell
$env:DVC_NO_ANALYTICS='1'
$env:DVC_GLOBAL_CONFIG_DIR="$PWD\\.dvc_global"
$env:DVC_SYSTEM_CONFIG_DIR="$PWD\\.dvc_system"
$env:DVC_SITE_CACHE_DIR="$PWD\\.dvc_site_cache"
```

## Краткое описание пайплайна

1. Сырые данные `data/raw/data.csv` добавлены в DVC, а не в Git.
2. Стадия `prepare` читает исходный CSV, удаляет дубликаты и пропуски, делит выборку на `train/test` и сохраняет результат в `data/processed/`.
3. Стадия `train` обучает `RandomForestClassifier`, сохраняет модель в `models/model.pkl`, метрики в `reports/metrics.json` и график матрицы ошибок в `reports/confusion_matrix.png`.
4. Во время обучения MLflow логирует параметры, метрики и артефакты.

## Где смотреть UI MLflow

После выполнения команды:

```powershell
mlflow ui --backend-store-uri ./mlruns
```

откройте в браузере:

```text
http://127.0.0.1:5000
```

## Feature Store

Для шага 3 в проект добавлен файл [`feature_repo/feature_store.yaml`](feature_repo/feature_store.yaml), настроенный по образцу `feast init ... --template postgres`.

В конфигурации используются:

- PostgreSQL как `registry`;
- PostgreSQL как `offline_store`;
- PostgreSQL как `online_store`.

Локальная проверка конфигурации выполнялась командами:

```powershell
python -m yamllint feature_repo/feature_store.yaml
feast -c feature_repo configuration
```

## Ограничения Colab по сравнению с Marimo

Краткий вывод для ноутбука:

- в Colab легко нарушить порядок выполнения ячеек, из-за чего состояние среды становится неявным;
- зависимости и временные файлы живут только в рамках сессии, поэтому DevOps-часть воспроизводить сложнее;
- `.ipynb` хуже подходит для code review и git diff;
- `marimo` удобнее для оформления воспроизводимого `.py`-файла с явными зависимостями между ячейками.

## Готовность ML-системы к production

Текущий проект является учебным прототипом и частично готов к переносу в production:

- уже есть контроль версий кода, данных, параметров и результатов обучения;
- есть разбиение пайплайна на этапы и логирование экспериментов;
- есть заготовка Feature Store.

Для полноценного production-развертывания пока не хватает:

- автоматических тестов;
- CI/CD;
- контейнеризации;
- мониторинга качества данных и модели;
- управления секретами;
- отдельного сервиса инференса и схемы отката модели.

## Схема ML-системы для заблюривания лиц

Для шага 5 схема описана в ноутбуке `HW5_MLOps_Panfilova_Tatiana.ipynb`. В ней выделены следующие блоки:

- источник видео;
- покадровая обработка;
- детекция лиц;
- модуль размытия найденных областей;
- сборка итогового видео;
- сохранение и выдача результата пользователю.

## Примечание по DVC remote

Для удобства проверки домашнего задания remote настроен как локальное хранилище `dvc_storage` внутри репозитория. Это позволяет выполнить `dvc pull` сразу после клонирования проекта без дополнительной настройки внешнего облачного хранилища.
