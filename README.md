# lab 6 Контейнеризация Django-приложения с Docker

Козел Максим Владимирович
С9121-10.05.01ммзи


### 1. Клонирование репозитория
```bash
git clone https://github.com/eternalsunset671/data_generator.git
```

### 2. Создание файла конфигурации для production на основе текущих переменных окружения
```bash
cp .env .env.prod
```

### 3. Копирование файла с начальными данными в директорию Django-приложения
```bash
cp data.json webtech_lab1/data.json
```

### 4. Сборка Docker-образов и запуск всех сервисов приложения в фоновом режиме

```bash
docker-compose up -d --build
```


### Вывод команды docker-compose ps
![alt text](lab_images/image.png)


### Вывод команды docker images (размеры образов)
![alt text](lab_images/image-1.png)

### Вывод docker-compose up
![alt text](lab_images/image-2.png)


### Работающее приложение в браузере
![alt text](lab_images/image-3.png)

### Админ панель Django
![alt text](lab_images/image-4.png)