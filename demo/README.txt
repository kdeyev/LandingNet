0. docker-compose exec landingnet sh
1. cd demo
2. sh symbols.sh demo.sym
3. sh crash.sh demo.dmp
4. psql -h postgresql -U landingnet landingnetdb -f dump_all.sql