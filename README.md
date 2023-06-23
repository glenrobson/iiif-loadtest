# iiif-loadtest
A program to run load testing on a IIIF server. This can be useful to check the scalability of your infrastructure can be run against a single image server or at a proxy for multiple image servers. There are various tests in [locustfile.py](imagesrv/locustfile.py) that will mimic a real user using a image server including requesting thumbnails and zooming around an image.  

To use the load tester you will need to supply a list of URLs to the locust test runner. A complete example is aviliable in [iiif-reference.txt](data/iiif-reference.txt) but an extract is below:

```
/api/image/2.0/example/reference/0a469c27256eda739d43124cc448a3ba-1_frontcover/info.json
/api/image/2.1/example/reference/0a469c27256eda739d43124cc448a3ba-1_frontcover/info.json
/api/image/3.0/example/reference/0a469c27256eda739d43124cc448a3ba-1_frontcover/info.json
/api/image/2.0/example/reference/0a469c27256eda739d43124cc448a3ba-2_insidefrontcover/info.json
/api/image/2.1/example/reference/0a469c27256eda739d43124cc448a3ba-2_insidefrontcover/info.json
/api/image/3.0/example/reference/0a469c27256eda739d43124cc448a3ba-2_insidefrontcover/info.json
```

You can see above the loadtest will work with both v2 and v3 images. To run the loadtest you can run the following passing in the image server host using -H parameter:

```
locust -f imagesrv/locustfile.py --url-list data/iiif-reference.txt -H https://iiif.io
```

This will start the locust web server at [http://0.0.0.0:8089/](http://0.0.0.0:8089/) where you can enter the number of threads and start the test. You can also run the tests from the command line by running: 

```
locust -f imagesrv/locustfile.py -t 1m --only-summary -u 10 --headless --url-list data/iiif-reference.txt -H https://iiif.io 
```

Where:
 * -f is the location of the locustfile
 * -t is the time to run the tests
 * --only-summary to print the summary at the end
 * -u 10 run with 10 users
 * --headless don't run the Web interface
 * --url-list location of the data file containing a list of info.json URLs (without the host)

For a full list of command line options see the [Locust Command line documentation](https://docs.locust.io/en/stable/configuration.html)

## Other scripts

Python URL check will look through a datafile and check that all of the info.json files return 200 and are valid JSON. This is useful to run before running the tests to check the URLs are working OK:

```
python urlCheck.py https://iiif.io data/iiif-reference.txt 

404: /api/image/2.0/example/reference/329817fc8a251a01c393f517d8a17d87-.metadata.json.swo/info.json

404: /api/image/2.1/example/reference/329817fc8a251a01c393f517d8a17d87-.metadata.json.swo/info.json
```