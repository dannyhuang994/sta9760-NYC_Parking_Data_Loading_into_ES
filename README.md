## STAT9760 - Project 1 - Part 2 Loading NYC Parking Data into ElasticSearch

#### pwd should be the file containing dockerfile and yml file


Start:

```
docker-compose up -d
```

This will start ElasticSearch and Kibana.

**ElasticSearch**: http://localhost:9200
**Kibana**: http://localhost:5601

Running python:

```
sudo docker-compose run -e APP_KEY=YOUR_APP_TOKEN -v $(pwd):/app bigdata python main.py --page_size=3 --num_pages=3 --output=result.json
```

Replace **YOUR_APP_TOKEN** with the actual token you have obtained.

In this case, you will load 3*3 = 9 data points into ElasticSearch.

--**page_size** is the number of data point per line. This is required. 

--**num_pages** is the number of lines of data you want. This is optional. When it is omitted or --num_pages=None, the program will read the data until every line from the API is exhausted.

--**output** is the name of the output file. When it is omitted, each line will be printed on the console and nothing will be loaded into ElasticSearch Server.

#### to check if you have sucessfully upload the data into ElasticSearch Server

run:

```
curl -0 http://localhost:9200/_search?pretty
```

-- this prints out a sample of your data from ElasticSearch
