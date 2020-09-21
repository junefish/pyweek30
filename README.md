# pyweek30
Team Bung for Pyweek 30 competition


## install

### setup (for development)
```bash
# First - Fork to your repo
git clone # your repo

python --version
# 3.8.x 
python -m install pipenv

cd pyweek30
mkdir .venv
python -m pipenv install
```
### run sample
```
python -m pipenv run sample
```


Regarding the files i added
1. unzip maps and put in same folder as others, its a map represented by .txt
2. saple.py 
-its sample game using the engine i made today 
- i suggest watching it last
3. ray_cast.py
- dont touch it works
- u dont need to read it for now
4. pyweek_engine.py
- READ this file pls I left a ton of comments there
- some additional usefull comments below
- [
- u can edit collisions in collisions class (ignore __init__ method thats in the class),
- movement is done in collisions(),
- ignore class Ray_cast_block for now,
- dir_movement is movement but saved in another variable(but a little different, u can ignore),
- last func load_objects() defines what object each symbol in map represents
- ]


- thats it, after 4 just look at sample.py
