## Steps to run the Agent assist chat application


1. Run `setup.sh` in your terminal (local or SageMaker Studio) which installs the dependencies listed in the `requirements.txt` file using pip, and some additional system dependencies only needed if you are serving the app from within SageMaker Studio. run the following command in your local terminal:
```bash
$ ./setup.sh
```

2. Run `run.sh` in the terminal with an argument `-e` providing the value as `local` or `sagemaker` depending on where you are running the application:

```bash
$  run.sh -e sagemaker
```

3. Click on URL shown in the output on the terminal. It opens the chat app in a new browser tab

4. Upload the sample transcript present in the `streamlit` folder with name `bank-call-centre-transcript.txt` to the chat interface.

5. Use the prompts provided in the `prompts.txt` to talk the Agent Assist chatbot.

