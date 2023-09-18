# songLLM
Turn your promts to beautifully created songs. <br/>
## Instructions
Firstly, download all the files locally, using `git clone https://github.com/ishan121028/songLLM.git`<br/>
Use this command in the directory to download all the requirements of the system `pip install -r requirements.txt`<br/>
Then initialize the submodule by this command `git submodule init` <br/>
Also use this command to update the submodules from the remote `git submodule update --force --recursive --init --remote`<br/>
Change the directory to `minGPT/` and run the command <br/>
`pip install -e .` <br/>
Now we are good to go with training and serving our model.


### For training

For further training the data over the dataset, use this command <br/>
`python train.py --fp 'dataset/spotify_millsongdata.csv' --lr learning rate` <br/>
This would start training from the last checkpoint and would keep saving the model weights as well as configurations into the out/SongData directory. <br/>

***Note:*** For now have kept `out/SongData` directory as static.

### For serving

For serving the model, we have to run the server using following command: <br/>
`python -m uvicorn server:app --reload` <br/>
This would run a server locally on the IP address `127.0.0.1` and port number `8000`, the endpoint is `/generatetext` <br/>
We can post a request to this server in this format: `{"text": "Enter Your Prompt Here", "max_length": "Enter the maximum length of your reply here"}` <br/>
The output message is `{"generated_text":"This is the generated text."}`<br/>

We can use these commands to curl (Windows): <br/>
`set json={"text": "Type your prompt here!", "max_length": 1000}` <br/>
`curl -i -X POST -H "Content-Type: application/json" -d "%json:"=\"%" http://127.0.0.1:8000/generatetext` <br/>

### Multithreading 

* Stress Testing the server: For stress testing, we can use this command, <br/> `python stress_test.py --url http://127.0.0.1:8000/generatetext --threads 10 --requests 10 --max_length 500` 
* Normal Inference: For normal inference from our model, we can use this command <br/> `python normal_inference.py --url http://127.0.0.1:8000/generatetext --messages "prompt1" "prompt2" "prompt3" "for" "prompt4" "prompt5" "prompt6" --max_length 500`
* Multi Threaded Inference: For multi threases inference from our model, we can use this command <br/> `python multi_inference.py --url http://127.0.0.1:8000/generatetext --messages "prompt1" "prompt2" "prompt3" "prompt4" "prompt5" "prompt6" --max_length 500`




