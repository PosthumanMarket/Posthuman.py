sudo pip3 install celery[redis]
redis-server

echo "we're good to go!"
echo "keep in mind: I'm using port 6379"
sudo celery -A qa_backend worker -l info -c 1 -P solo