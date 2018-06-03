0. docker-compose exec landingnet sh
1. python manage.py add_product Demo
2. cd demo
3. sh symbols.sh demo.sym
4. sh crash.sh demo.dmp
5. psql -h postgresql -U landingnet landingnetdb -f dump_all.sql