# aifactory-alpha

Alpha version of `aifactory` module

## Install via `pip`

```
pip install aifactory-alpha
```

## Submit the result

```
aifactory-submit --user_email user0@aifactory.page 
                 --task_id 3000 
                 --file answer.csv
                 # --log_dir ./log
                 # --auth_url auth.aifactory.solutions
                 # --submit_url submit.aifactory.solutions
                 
aifactory-submit --file ./sample_data/sample_answer.csv 
                 --debug True # debug mode has default dummy user information
                              # You can still change argument on debug mode to make an error
```
