title: Install and run a machine learning model on your laptop
slug: llm-laptop-ollama
summary: Discover how to run machine learning models, such as large language models, on consumer-grade computers using the Ollama project.
date: 2023-12-18
modified: 2023-12-18
category: Machine Learning
status: Published


One way to experiment with the large language models that are creating so much excitement is to use a hosted solution like *[Replicate](https://replicate.com/)*, which lets you host your own instances of many open-source models. Or, you can use the proprietary AI services offered by cloud services like *[OpenAI](https://openai.com/product)*/*[Azure](https://azure.microsoft.com/en-us/solutions/ai)*, *[Google AI](https://ai.google/build)*, or *[Amazon AWS](https://aws.amazon.com/machine-learning/ai-services/)*.

However, running open-source machine learning models on your own hardware like your laptop computer offers a unique hands-on experience. Currently, the easiest-to-use tool that enables users to run machine learning models on their personal computers is *[Ollama](https://ollama.ai/)*. Some other available tools are *[h2oGPT](https://github.com/h2oai/h2ogpt)*, *[GPT4All](https://gpt4all.io/index.html)*, and *[LLM](https://llm.datasette.io/en/stable/)*.

This post will describe how to install Ollama on your local PC and use it to run open-source models.

## Ollama

[Ollama](https://github.com/jmorganca/ollama) acts like a package manager for machine learning models. It runs locally and makes it easy to download and try different models. It is simple to experiment with because it can be [installed in a container](https://ollama.ai/blog/ollama-is-now-available-as-an-official-docker-image) on your Linux PC.

Ollama has very low hardware requirements. You do not need a GPU, although a GPU helps greatly with performance. You can find models in the [Ollama repository](https://ollama.ai/library) that require less than 16 GB of memory to use. As always, more powerful hardware allows you to run more powerful models.

Ollama enables you to keep multiple models available on your local PC. You can use Ollama to add, copy, and delete models. You can also import your own custom models into Ollama and then use Ollama's command-line interface to manage and run them.

## Installing Ollama

You may [install Ollama on a Linux PC](https://github.com/jmorganca/ollama/blob/main/docs/linux.md) a couple of different ways. I prefer to use the [Ollama container](https://hub.docker.com/r/ollama/ollama), available in the DockerHub container registry. Use the following Docker command to download the container and run it.

```text
$ docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

I am using an old Thinkpad T480 that has no GPU, so the procedure shown above runs a container that uses only the CPU. To use a GPU, see the [Ollama Docker image instructions](https://hub.docker.com/r/ollama/ollama).

Docker pulls the Ollama image from the Docker Hub repository and starts it. The models, which can be very large files, will be stored in a Docker volume named *ollama*:

```text
$ docker volume list
DRIVER    VOLUME NAME
local     ollama
```

## Using Ollama

A running Ollama model can be used several ways:

* Using a REST API, via the [Python *requests* library](https://requests.readthedocs.io/en/latest/), or the Linux *[curl](https://curl.se/)* command.
* Using Ollama's command-line interface.
* Using LLM frameworks, such as *[Lang](https://python.langchain.com/docs/integrations/providers/ollama)[Chain](https://python.langchain.com/docs/guides/local_llms)* or *[LlamaIndex](https://docs.llamaindex.ai/en/stable/getting_started/installation.html)*.

### Getting models

To use Ollama machine learning models, you *pull* a model you want to use and then *run* it. Go to the [Ollama repository](https://ollama.ai/library) to find models that will run on your hardware. In my case, because I am running an old laptop with a 6th-Gen Intel i5 and only 16 GB of memory, I will look for models designed to run on CPU-only with less than 16 GB of RAM.

Typically, models trained with 7 billion parameters or less are good candidates to run on a laptop computer without a dedicated GPU. When you click on a model in the Ollama repository, you will see an overview of its information, which includes how many parameters are in each version of the model and how much memory is needed to run each of them. Then, click on the *Tags* tab, next to the *Overview* tab, to see the tags that identify each version of the model. 

Click on the tag you wish to use. The next page will show you some more information about the model and will usually show you some instructions about how to use the model.

### Ollama REST API

I chose to use the [*orca-mini:3b* model](https://ollama.ai/library/orca-mini), which was created by Microsoft researchers and is [based](https://huggingface.co/papers/2306.02707) on the open-source Llama2 model. It is designed to be a small model that cam deliver performance similar to larger models.

I wrote a simple Python script to access Ollama's REST API. 

```python
import requests
import json

url = "http://localhost:11434/api/generate"

data = {
    "model": "orca-mini:3b",
    "system": "Answer using 10 words or less.",
    "prompt": "Tell me why the sky is blue."
}

response = requests.post(url, json=data)
print(response.text)
```

I saved the script as *orca.py* and ran it. This resulted in an error because the model was not yet downloaded. 

```text
$ python3 orca.py 
{"error":"model 'orca-mini:3b' not found, try pulling it first"}
```

Use the API's [*pull* endpoint](https://github.com/jmorganca/ollama/blob/main/docs/api.md#pull-a-model) to download the model. I wrote another Python script to pull the model I wanted:

```python
import requests

url = "http://localhost:11434/api/pull"

data = {
    "name": "orca-mini:3b"
}

response = requests.post(url, json=data)
print(response.text)
```

I saved this script as *pull.py* and ran it. The console displays a large amount of responses as Ollama downloads the model. The output below shows the end of the operation:

```text
python3 pull.py
...
...
{"status":"pulling fd52b10ee3ee","digest":"sha256:fd52b10ee3ee9d753b9ed07a6f764ef2d83628fde5daf39a3d84b86752902182","total":455}
{"status":"pulling fd52b10ee3ee","digest":"sha256:fd52b10ee3ee9d753b9ed07a6f764ef2d83628fde5daf39a3d84b86752902182","total":455,"completed":455}
{"status":"verifying sha256 digest"}
{"status":"writing manifest"}
{"status":"removing any unused layers"}
{"status":"success"}
```

Now, I ran the original *orca.py* script to run the Orca model. Remember that script included a *[system prompt](https://huggingface.co/blog/llama2#how-to-prompt-llama-2)* that requested that the model behave in a certain way and a *[user prompt]()*, that asked the model why the sky is blue.

```text
$ python3 orca.py
{"model":"orca-mini:3b","created_at":"2023-12-16T20:37:18.66622562Z","response":" Sky","done":false}
{"model":"orca-mini:3b","created_at":"2023-12-16T20:37:18.843828069Z","response":" is","done":false}
{"model":"orca-mini:3b","created_at":"2023-12-16T20:37:18.975351886Z","response":" blue","done":false}
{"model":"orca-mini:3b","created_at":"2023-12-16T20:37:19.104637855Z","response":".","done":false}
{"model":"orca-mini:3b","created_at":"2023-12-16T20:37:19.234764526Z","response":"","done":true,"context":[31822,13,8458,31922,3244,31871,13,3838,397,363,7421,8825,342,5243,10389,5164,828,31843,9530,362,988,362,365,473,31843,13,13,8458,31922,9779,31871,13,10568,281,1535,661,31822,31853,31852,2665,31844,1831,515,674,3465,322,266,7661,31843,13,13,8458,31922,13166,31871,13,8296,322,4842,31843],"total_duration":7058888990,"prompt_eval_count":57,"prompt_eval_duration":6662088000,"eval_count":4,"eval_duration":390769000}
```

The model returns JSON responses and each response contains one word, or part of a word.
I add some code to the *orca.py* script to parse the response tokens from the json and join it into a readable paragraph:

```python
import requests
import json

url = "http://localhost:11434/api/generate"

data = {
    "model": "orca-mini:3b",
    "system": "Answer using 10 words or less.",
    "prompt": "Tell me why the sky is blue."
}

response = requests.post(url, json=data)
data = response.text.splitlines()
response_list = [json.loads(line)['response'] for line in data]

print(''.join(response_list))
```

Running the program multiple time produces results that are different, but that relate to the original prompt.

```text
$ python3 orca.py
 Blue.
$ python3 orca.py
 I'm sorry, but as an AI language model, I cannot see the sky.
$ python3 orca.py
 Blue.
$ python3 orca.py
 The color of the sky changes depending on the time of day and weather conditions.
```

Performance is OK. It takes about 5 to 10 seconds for each response to be completed.

#### Using *curl* with the Ollama REST API

If you don't want to write Python scripts to access the REST API, you can use the *curl* command. Pipe the output into the *jq* command to parse the responses from the JSON output and join them together into a readable paragraph:

```text
$ curl -s -X POST http://localhost:11434/api/generate -d '{
    "model": "orca-mini:3b", 
    "prompt":"What color is the ocean?"
  }' \
  | jq -j .response
```

In this case, I did not include a system prompt, which is optional. The model responds correctly:

```text
 The ocean appears to be a deep blue color, often referred to as 
 dark navy or indigo.
```


### Ollama command-line interface

Ollama also offers a command-line interface. I will test another model to demonstrate the Ollama CLI. I used the *mistral:7b* model because it needs less than 16GB of memory. Use Docker to send the ollama commands to the container:

```text
$ docker exec -it ollama ollama pull mistral:7b
```

Then run the model:

```text
$ docker exec -it ollama ollama run mistral:7b
```

The model's CLI prompt appears:

```text
>>> Send a message (/? for help)
```

At the `>>>` prompt, ask your questions:

```text
>>> How fast can a moose run?
A moose is one of the largest species of deer in the world and they are 
known for their swift running abilities. On average, a moose can run at 
speeds between 35 to 40 miles per hour (56 to 64 kilometers per hour) over 
short distances. However, they typically do not maintain this speed for 
long periods due to their large size and the energy required for such 
quick movements. Moose are also excellent swimmers and can easily cover 
several hundred yards in a lake or river.
```

The performance on my laptop was fairly slow, because I am running a larger model. It tool over 30 seconds to return a result.

Different models seems to offer different feature. For example. the *mistral* model seems to remember the context of your previous prompts. For example, I asked it to tell me a short story about a boy and his dog. *Mistral* produced a decent story. Then, I asked *msitral* to reqrite the story except replace the dog with a cat. It seemed top remember the plot of the previous story and wrote a very similar story featuring a very loyal cat. 

The base *mistral* model also seems to do a good job writing code, and there are specific models that are fine-tuned to write code, like *[codellama](https://ollama.ai/library/codellama)*

For example, I asked *mistral* to write a Python function:

```text
>>> Write a python function that implements the min max algorithm
```

The output was:

    Title: MinMax Algorithm Function (Python)

    ```python
    def minmax(board, depth, maximizing_player):
        if terminate_game(board):  # Check for game termination
            return util.calculate_utility(board)

        if maximizing_player:
            best_score = float('-inf')
            for move in possible_moves(board):
                score = minmax(board.copy(), depth + 1, False)
                best_score = max(best_score, score)
                board.make_move(move)
            return best_score

        else:
            best_score = float('inf')
            for move in possible_moves(board):
                score = minmax(board.copy(), depth + 1, True)
                best_score = min(best_score, score)
                board.make_move(move)
            return best_score
    ```

    In this implementation, the `minmax()` function is used to evaluate the 
    maximum and minimum scores for a given game state (represented by the 
    `board` parameter). The `depth` variable denotes the current depth in the 
    search tree, while `maximizing_player` is a boolean flag indicating whether
    the maximizing player's turn is being considered.

    The function uses recursion to explore the game tree, alternating between 
    maximizing and minimizing scores at each level. When evaluating maximum 
    scores (during maximizing_player = True), it searches for the best possible
    score by considering all possible moves and selecting the one with the 
    highest utility value. Similarly, during minimizing scores 
    (maximizing_player = False), it searches for the worst possible score by 
    considering all possible moves and selecting the one with the lowest 
    utility value.

    The `terminate_game()`, `util.calculate_utility()`, `possible_moves()`, and
    `board.copy()` functions are assumed to be implemented separately and 
    provide functionality to check for game termination, calculate the utility 
    of a given board state, generate possible moves for a given board state, 
    and create a copy of the current board state, respectively.

This seemed to be a satisfactory result. *Mistral* also tried to explain the code to the user.

### Managing models using the Ollama CLI

To manage a model, use the *ollama* CLI commands, which are preceded by a forward slash. You can see all available commands using the `/?` command. 

To exit the model prompt, run the `/bye` command:

```text
>>> \bye
```

Depending on the model, you may have more CLI commands available to you. For example, you could set the system prompt, tell the model to remember its previous responses, configure output formats, and more. 

### Stopping Ollama

When you are done using Ollama, stop the Ollama container:

```text
$ docker stop ollama
```

You can start it again when you need to use it.

## Conclusion

Running AI models locally is an educational journey, offering deeper insights and more [configuration options](https://huggingface.co/blog/llama2#how-to-prompt-llama-2) than cloud-based solutions. It's especially beneficial for those with powerful hardware, enabling experimentation without relying on third-party services.






