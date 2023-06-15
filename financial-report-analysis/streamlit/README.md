## Prerequisites - Configuration

* Ensure you update the credentials needed to access AWS OpenSearch indices in the `config.yml`

* Run `chmod +x` for `cleanup.sh`, `run.sh` and `setup.sh`. Install the dependencies listed in the `requirements.txt` file using pip, you can run the following command in your local terminal:
```bash
$ chmod +x setup.sh
$ chmod +x cleanup.sh
$ chmod +x run.sh
```

* Execute the `setup.sh` which will install all the required dependencies
```bash
$ ./setup.sh
```

* Run the Streamlit application by executing the `run.sh`:

```bash
$ ./run.sh
```

the output will provide the streamlit app url which looks something like this:
https://{domain_id}.studio.{region}.sagemaker.aws/jupyter/default/proxy/8501/


* Click on the URL and it will open new tab in the browser where the application will be loaded: http://localhost:8501.


