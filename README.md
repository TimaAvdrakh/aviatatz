# aviatatz
Тестовое задание в компанию Aviata/Chocotravel на позицию jun3

# Download
git clone https://github.com/TimaAvdrakh/aviatatz


### Installing requirements
pip3 install -req.txt

### Enabling RabbitMQ
sudo systemctl enable rabbitmq-server

### Celery worker info
celery -A aviata worker -l info

### Celery beat
celery -A aviata beat -l info
