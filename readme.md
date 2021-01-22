## Description
This is a simple REST service which is used to query csv data (in thi example - vulnerabilities) stored in s3 bucket.
This api supports pagination and sorting based on any column defined in a csv file for a specific host.
## Example of usage
* `/{host}/vulnerabilities` - get first ten records sorted by `risk_score` (default pagination and sorting) for `{host}`;
* `/{host}/vulnerabilities?start_from=20&size=5` - get five records starting from 20th record (sorted by `risk_score`);
* `/{host}/vulnerabilities?order_by=vulnerability&order=asc` - get ten records sorted by vulnerability with ascending order;

#### Example of response:
```json
{
    "order": "asc",
    "order_by": "vulnerability",
    "total": 33,
    "start_from": 0,
    "size": 10,
    "results": [
        "Apache OpenOffice < 4.1.8 Arbitrary Code Execution",
        "Apache Struts2 Remote Command Execution",
        "Bind Shell Backdoor Detection",
        "Docker remote API detection",
        "Exposure of Application source code, config files and credentials",
        "Exposure of Application source code, config files and credentials",
        "File Content Disclosure /etc/passwd",
        "File Content Disclosure /etc/passwd",
        "Google Chrome < 87.0.4280.66 Multiple Vulnerabilities",
        "Google Chrome < 87.0.4280.88 Multiple Vulnerabilities"
    ]
}
```

## Local environment
#### Requirements:
* Python 3.5+;
* pip;
* nodejs 14+ (for serverless framework);
* npm  
* docker; 
* docker-compose;
* aws account (for deployment);

#### Getting started:
* install nodejs packages: `npm install`;
* install python packages: `pip install -r requirements.txt`;
* start minio container: `docker-compose up -d`;
* start serverless offline: `sls offline start`;

At this point everything should be set up. The Api should be available at localhost:3000. 
For example: http://localhost:3000/local/197.227.236.56/vulnerabilities

## Tests
Run pytest: `python -m pytest`

## Deployment

* Create s3 bucket and upload a csv file to it;
* set bucket name and file name in .env.{stage} file;
* run `sls deploy -s {stage}`
