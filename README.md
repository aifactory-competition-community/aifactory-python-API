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

## To-do
 - [ ] 언노운 에러 -> 패키지 업데이트하라고 알려주기
 - [ ] 윈도우에서도 되는지 확인해보기
 - [ ] 다른 플랫폼에서도 constants 공유할 수 있게 하기


### ASCII Arts Reference
> https://wepplication.github.io/tools/asciiArtGen/
