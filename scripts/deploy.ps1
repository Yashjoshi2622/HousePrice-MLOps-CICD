docker stop houseprice-api 2>$null
docker rm houseprice-api 2>$null
docker build -t houseprice-mlops .
docker run -d -p 8000:8000 --name houseprice-api houseprice-mlops
