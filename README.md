# songLLM
This is a repository for the challenge by NimbleBox.ai for the internship role of a ML Engineer.\
## Instructions
Firstly, download all the files locally, using `git clone https://github.com/ishan121028/songLLM.git`\\
Use this command in the directory to download all the requirements of the system `pip install -r requirements.txt`\\
Change the directory to minGPT/ and run the command\
`pip install -e .`\
Now we are good to go with training and serving our model.


### For training

For further training the data over the dataset, use this command\
`python train.py --fp 'dataset/spotify_millsongdata.csv' --lr learning rate`\
This would start training from the last checkpoint and would keep saving the model weights as well as configurations into the out/SongData directory.\

***Note:*** For now have kept `out/SongData` directory as static.

### For serving

For serving the model, we have to run the server using following command: \
`python -m uvicorn server:app --reload`\
This would run a server locally on the IP address `127.0.0.1` and port number `8000`, the endpoint is `/generatetext`\
We can post a request to this server in this format: `{"text": "Enter Your Prompt Here", "max_length": "Enter the maximum length of your reply here"}`\
The output message is `{"generated_text":"This is the generated text."}`\

We can use these commands to curl (Windows):\
`set json={"text": "NimbleBox!", "max_length": 1000}`\
`curl -i -X POST -H "Content-Type: application/json" -d "%json:"=\"%" http://127.0.0.1:8000/generatetext`\

### Multithreading 

* Stress Testing the server: For stress testing, we can use this command,\ `python stress_test.py --url http://127.0.0.1:8000/generatetext --threads 10 --requests 10 --max_length 500`\
* Normal Inference: For normal inference from our model, we can use this command \ `python normal_inference.py --url http://127.0.0.1:8000/generatetext --messages "I" "have" "applied" "for" "NimbleBox" "Internship" --max_length 500`
* Multi Threaded Inference: For multi threases inference from our model, we can use this command \ `python multi_inference.py --url http://127.0.0.1:8000/generatetext --messages "I" "have" "applied" "for" "NimbleBox" "Internship" --max_length 500`




