title: Install and run a large language model on your laptop
slug: llm-laptop-ollama
summary: Run machine learning models, such as large language models, on consumer-grade computers using the Ollama project
date: 2023-12-18
modified: 2023-12-18
category: Machine Learning
<!-- status: Published -->


One way to experiment with the large language models that are creating so much excitement is to use a hosted solution like *[Replicate](https://replicate.com/)*, which lets you host your own instances of many open-source models. Or, you can use the proprietary AI services offered by cloud services like *[OpenAI](https://openai.com/product)*/*[Azure](https://azure.microsoft.com/en-us/solutions/ai)*, *[Google AI](https://ai.google/build)*, or *[Amazon AWS](https://aws.amazon.com/machine-learning/ai-services/)*.

However, it is also interesting to experiment with ways to run open-source machine learning models on your own hardware, like your laptop computer. 

Currently, the easiest-to-use tool that enables users to run machine learning models on their personal computers is *[ollama.ai](https://ollama.ai/)*. Some other available tools are *[h2oGPT](https://github.com/h2oai/h2ogpt)*, *[GPT4All](https://gpt4all.io/index.html)*, and *[LLM](https://llm.datasette.io/en/stable/)*.

This post will describe how to install Ollama on your local PC and use it to run open-source models.

## Ollama

[Ollama](https://github.com/jmorganca/ollama) acts like a package manager for machine learning models. It runs locally and makes it easy to download and try different models. It is simple to experiment with because it can be [installed in a container](https://ollama.ai/blog/ollama-is-now-available-as-an-official-docker-image) on your Linux PC.

Ollama has very low hardware requirements. You do not need a GPU, although a GPU helps greatly with performance. You can find models in the [Ollama repository](https://ollama.ai/library) that require less than 16 GB of memory to use. As always, more powerful hardware allows you to run more powerful models.

Ollama enables you to keep multiple models available on your local PC. You can use Ollama to add, copy, and delete models. You can also import your own custom models into Ollama and then use Ollama's command-line interface to manage and run them.

## Installing Ollama

You may install Ollama on a Linux PC a couple of different ways. I prefer to use the Ollama container, available in the DockerHub container registry. Use the following Docker command to download the container and run it.

```text
$ docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

This pulls the Ollama image from the Docker Hub repository and starts it.

## Using Ollama

A running Ollama model can be accessed several ways: 

* Using Ollama's prompt-based interface,
* Using a REST API
* Using Python LLM frameworks, such as *[LangChain](https://python.langchain.com/docs/integrations/providers/ollama)* or *[LlamaIndex](https://docs.llamaindex.ai/en/stable/getting_started/installation.html)*.










Running Open Source LLMs Locally Using Ollama: A Step-by-Step Guide
https://medium.com/@kbdhunga/running-open-source-llms-locally-using-ollama-a-step-by-step-guide-cf2ab62c817a

 



https://python.langchain.com/docs/guides/local_llms




https://ollama.ai/blog/ollama-is-now-available-as-an-official-docker-image

My T480 has no graphics card so use CPU-only



Use 7b llama model because it needs only 16 GB memory

```
$ docker exec -it ollama ollama run mistral:7b
```

4.1 GB file download

```
pulling manifest 
pulling c70fa74a8e81... 100%                         
pulling e6836092461f... 100%                        
pulling 1128f85489e0... 100%                          
pulling 70ded05e7c58... 100%                        
verifying sha256 digest 
writing manifest 
removing any unused layers 
success 
>>> Send a message (/? for help)
```

At the >>> prompt, ask your questuions

```
>>> How fast can a moose run?
A moose is one of the largest species of deer in the world and they are 
known for their swift running abilities. On average, a moose can run at 
speeds between 35 to 40 miles per hour (56 to 64 kilometers per hour) over 
short distances. However, they typically do not maintain this speed for 
long periods due to their large size and the energy required for such 
quick movements. Moose are also excellent swimmers and can easily cover 
several hundred yards in a lake or river.
```

Fairly slow (try to compare with ChatGPT online)

```
>>> write a short story about a boy and his dog
 Title: The Unbreakable Bond

Once upon a time in the quaint little town of Meadowbrook, lived a young 
boy named Timmy. Timmy was an ordinary boy with an extraordinary companion 
- his loyal and faithful dog, Max. Max was a beautiful Golden Retriever 
with a heart as golden as his coat. They shared an unbreakable bond that 
brought joy and comfort to each other's lives.

Timmy and Max were inseparable. Every morning, they would wake up together,
Max wagging his tail excitedly at the first sign of sunlight, while Timmy 
smiled at the sight of his beloved friend. They spent their days exploring 
the vast meadows surrounding Meadowbrook, playing fetch by the tranquil 
creek, and basking in the warmth of the sun together.

One autumn afternoon, as they frolicked in the golden leaves, a sudden hush
fell upon the land. Dark clouds gathered on the horizon, foretelling an 
impending storm. Timmy looked worriedly at Max, who seemed unusually 
restless. The winds began to howl, and raindrops started pelting down. 
Realizing that they needed to seek shelter, they hurried towards their cozy
cabin by the woods.

As they reached the doorstep, a loud crack echoed through the forest, 
followed by a series of thunderous roars. A giant oak tree had fallen on 
the cabin, leaving Timmy and Max trapped outside in the storm. The boy was 
petrified as he clung onto Max, who nuzzled against him, trying to offer 
what little comfort he could.

The hours passed slowly as they huddled together under a tree, waiting for 
the storm to subside. Timmy's fears subsided as he felt the warmth of Max's
presence and the reassuring beat of his heart. The dog remained steadfast, 
refusing to leave his boy's side even in the face of danger.

When dawn finally broke, they emerged from their hiding place to find that 
the storm had passed. The townspeople were amazed at how the two had 
survived the calamity, and everyone marveled at the bond between Timmy and 
Max. Their tale spread far and wide, inspiring awe and admiration in all 
who heard it.

From then on, their bond grew even stronger, proving that love knows no 
bounds, not even the fury of nature itself. And so, they continued their 
days filled with joy, adventure, and most importantly, their unbreakable 
bond.

>>> Send a message (/? for help)
```

So, mistral works well.

Context? Ask it to revisit the story

```
>>> rewrite the story with a cat
 Title: The Purrfect Companion

Once upon a time in the quaint little town of Meadowbrook, lived a young 
boy named Timmy. Timmy was an ordinary boy with an extraordinary companion 
- his loyal and wise cat, Whiskers. Whiskers was a beautiful Siamese with 
piercing blue eyes and a coat as soft as silk. They shared an unbreakable 
bond that brought joy and comfort to each other's lives.

Timmy and Whiskers were inseparable. Every morning, they would wake up 
together, Whiskers purring softly at the first sign of sunlight, while 
Timmy smiled at the sight of his cherished friend. They spent their days 
exploring the quiet corners of Meadowbrook, curling up by the fireplace 
during chilly afternoons, and sharing whispered secrets in the stillness of
the night.

One winter evening, as they settled down for a cozy nap by the hearth, the 
winds began to howl outside, foretelling an impending blizzard. Timmy 
looked nervously at Whiskers, who seemed unusually restless. The snow 
started falling heavily, blanketing the town in white. Realizing that they 
needed to find shelter before the storm worsened, they braved the elements 
and set out towards their cottage by the lake.

As they reached the doorstep, a sudden gust of wind knocked it open, 
revealing a tree branch teetering precariously above them. Timmy froze in 
fear as he realized that the branch was about to fall on them. Whiskers, 
sensing his boy's terror, leapt into action. He scratched and meowed 
fiercely at the branch until it finally gave way. The tree limb crashed 
harmlessly away from them, leaving Timmy amazed and grateful for his brave 
companion.

They managed to reach their cottage just in time, huddling together by the 
fireplace as the blizzard raged outside. Whiskers kept watch over Timmy, 
never leaving his side even for a moment. The boy's fears subsided as he 
felt the warmth of his cat's presence and the gentle purring that resonated
through the cabin.

When morning dawned, they emerged from their refuge to find that the storm 
had passed. The townspeople marveled at how Timmy and Whiskers had survived
the blizzard, and everyone was in awe of the bond between the boy and his 
cat. Their tale spread far and wide, inspiring admiration and wonder in all
who heard it.

From then on, their bond grew even stronger, proving that love knows no 
bounds, not even the harshest winter storms. And so, they continued their 
days filled with warmth, companionship, and most importantly, their 
unbreakable bond.

>>> Send a message (/? for help)
```

```
>>> That was great. No rewrite it so it is half as long.
 Title: The Unbreakable Bond (Short)

In the tranquil town of Meadowbrook lived a boy named Timmy and his 
extraordinary cat, Whiskers. Their bond was unbreakable as they spent their
days exploring and sharing secrets. During a winter storm, Timmy and 
Whiskers huddled together for safety. With Whiskers' brave actions, they 
survived and the town marveled at their unbreakable bond.

>>> Send a message (/? for help)
```

So, not exactly accurate because it was 1/8 as long instead of 1/2 as long, but still an impressive result running on an 8-year old laptop with no GPU


Try code:

```
>>> Write a python function that implements the min max algorithm
```

The output is:

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



Use the API. In another terminal window:

```
$ curl -X POST http://localhost:11434/api/generate -d '{
  "model": "mistral:7b",
  "prompt":"What color is the sky?"
 }'
```

Output is provided in small chunks. I show a portion of the total output below.

```
{"model":"mistral:7b","created_at":"2023-12-14T20:29:38.176298946Z","response":" The","done":false}
{"model":"mistral:7b","created_at":"2023-12-14T20:29:38.488782789Z","response":" color","done":false}
{"model":"mistral:7b","created_at":"2023-12-14T20:29:38.822915843Z","response":" of","done":false}
{"model":"mistral:7b","created_at":"2023-12-14T20:29:39.139350724Z","response":" the","done":false}
{"model":"mistral:7b","created_at":"2023-12-14T20:29:39.456925434Z","response":" sky","done":false}
{"model":"mistral:7b","created_at":"2023-12-14T20:29:39.777533809Z","response":" can","done":false}
{"model":"mistral:7b","created_at":"2023-12-14T20:29:40.095794941Z","response":" vary","done":false}
{"model":"mistral:7b","created_at":"2023-12-14T20:29:40.409452609Z","response":" depending","done":false}
{"model":"mistral:7b","created_at":"2023-12-14T20:29:40.737500539Z","response":" on","done":false}
{"model":"mistral:7b","created_at":"2023-12-14T20:29:41.051624152Z","response":" the","done":false}
{"model":"mistral:7b","created_at":"2023-12-14T20:29:41.369585894Z","response":" time","done":false}
...
...
{"model":"mistral:7b","created_at":"2023-12-14T20:30:19.391460176Z","response":"","done":true,"context":[733,16289,28793,28705,1824,3181,349,272,7212,28804,733,28748,16289,28793,415,3181,302,272,7212,541,11204,10085,356,272,727,302,1370,304,28446,27552,294,4331,28723,6213,264,3081,1370,28725,272,7212,8045,298,347,264,6833,5045,3181,2940,298,272,21635,302,22950,486,272,13789,28723,1794,4376,24035,304,4376,673,28725,272,7212,541,4249,264,2819,302,9304,2490,2760,28713,28725,12937,28713,28725,442,5897,28725,304,3276,2815,390,272,4376,28742,28713,408,748,460,25028,1059,680,302,272,8599,28742,28713,13789,28723,1794,2125,28725,272,7212,349,6741,2687,28725,562,378,541,506,7448,28725,272,11375,28725,304,799,9645,374,505,9401,9141,10085,356,15912,4331,28723],"total_duration":45452942787,"prompt_eval_count":15,"prompt_eval_duration":4544940000,"eval_count":119,"eval_duration":40902512000}
```

To make the output human readable, parse it with the `jq` command. Also, use the `curl` command's`-s` option to silence the progress status bar:

```
$ curl -s -X POST http://localhost:11434/api/generate -d '{
    "model": "mistral:7b", 
    "prompt":"What color is the ocean?"
  }' \
  | jq -j .response
```

Now each chunk that was returned in the JSON *response* field is parsed out and joined into one readable paragraph: 


```
 The color of the ocean can vary depending on its depth, location, and the presence of suspended
 particles or organisms. In general, the open ocean, particularly in clear weather conditions, 
 appears shades of blue or green due to the absorption and scattering of sunlight by water 
 molecules and dissolved substances. However, shallow waters near coastlines may appear 
 turquoise, green, or other colors depending on their depth, sediment content, and water 
 clarity. Additionally, the ocean's surface color can change due to weather conditions, such as 
 overcast skies or strong waves, which can affect the amount of sunlight reflected or absorbed.
```

Good for text but some work required to get usable code format from API:

```
$ curl -s -X POST http://localhost:11434/api/generate -d '{
    "model": "mistral:7b", 
    "prompt":"Write a python function that implements the min max algorithm"
    }' | jq -j .response
```

Here is the response, whcih includes some explanation and a cose sample:

    Here is an example of how to implement the MinMax algorithm for a two-player zero-sum game using Python. In this example, I will assume that you are implementing this algorithm for a simple 2x2 game. Please note that this is just one way of implementing MinMax and there might be other variations depending on the specific use case.

    ```python
    def minmax(board, depth, maximizing_player):
        if depth == 0 or check_if_game_over(board):
            return evaluate_score(board)

        if maximizing_player:
            best = float('-inf')
            for move in possible_moves(board):
                score = minmax(make_move(board, move), depth - 1, False)
                best = max(best, score)
            return best
        else:
            best = float('inf')
            for move in possible_moves(board):
                score = minmax(make_move(board, move), depth - 1, True)
                best = min(best, score)
            return best

    def check_if_game_over(board):
        # Check for a win or a draw here.
        # This function should return a boolean value indicating if the game is over.
        pass

    def evaluate_score(board):
        # Evaluate the score of the board based on some given criteria.
        # In a simple 2x2 game, this could be just returning 1 for a win and -1 for a loss.
        pass

    def possible_moves(board):
        # Return a list of valid moves for the current player.
        pass

    def make_move(board, move):
        # Make a move on the board and return the updated board.
        pass
    ```

    This code defines a `minmax()` function that recursively calls itself with alternating players to find the best possible move based on the Maximizing (Max) or Minimizing (Min) strategy. The `check_if_game_over()`, `evaluate_score()`, `possible_moves()`, and `make_move()` functions are placeholders for your specific game logic, such as checking if the game is over, evaluating the score of a board state, finding valid moves, and making a move on the board.


    https://huggingface.co/






