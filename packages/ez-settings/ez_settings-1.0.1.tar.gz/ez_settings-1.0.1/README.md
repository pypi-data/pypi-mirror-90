# 🌴 EZ Settings

EZ Settings is a very simple, lightweight settings module that makes it easy to get and set settings for your application. It's all stored in a JSON file, so any value you want to store has to be able to be serialized in a JSON file.

### Initializing

```python
from ez_settings.ez_settings import EZSettings

settings = EZSettings("/home/applications/my_app/settings.json")
```

### Setting values

I like to make simple classes to store setting names, just because it makes it easier to autocomplete when writing code. You can also just pass in a normal string in the `set` and `get` functions.

```python
from ez_settings.ez_settings import EZSettings
class Settings:
    NAME =            "name"
    POSITION =        "position"
    SUPERBOWL_WINS =  "superbowl_wins"
    TEAMS  =          "teams"
    ACTIVE  =         "active"

settings = EZSettings("/home/applications/my_app/settings.json")

settings.set(Settings.NAME, "Tom Brady")
settings.set(Settings.SUPERBOWL_WINS, 5)

```

### Getting values

```python
from ez_settings.ez_settings import EZSettings
class Settings:
    NAME =            "name"
    POSITION =        "position"
    SUPERBOWL_WINS =  "superbowl_wins"
    TEAMS  =          "teams"
    ACTIVE  =         "active"

settings = EZSettings("/home/applications/my_app/settings.json")

championships = settings.get(Settings.SUPERBOWL_WINS)

```

### List values

You can append or pop items if the value of your setting is a list

```python
from ez_settings.ez_settings import EZSettings
class Settings:
    NAME =            "name"
    POSITION =        "position"
    SUPERBOWL_WINS =  "superbowl_wins"
    TEAMS  =          "teams"
    ACTIVE  =         "active"

settings = EZSettings("/home/applications/my_app/settings.json")

# set a list value
settings.set(Settings.TEAMS, ["New England"])

# add to the list value
settings.append(Settings.TEAMS, "Tampa Bay")

# remove from the list values
settings.pop(Settings.TEAMS, "New England")

```

### Deleting a single setting

```python
from ez_settings.ez_settings import EZSettings
class Settings:
    NAME =            "name"
    POSITION =        "position"
    SUPERBOWL_WINS =  "superbowl_wins"
    TEAMS  =          "teams"
    ACTIVE  =         "active"

settings = EZSettings("/home/applications/my_app/settings.json")
settings.remove(Settings.POSITION)
```

### Wiping all settings

```python
from ez_settings.ez_settings import EZSettings

settings = EZSettings("/home/applications/my_app/settings.json")
settings.reset()
```
### Checking if a setting exists

```python
from ez_settings.ez_settings import EZSettings

settings = EZSettings("/home/applications/my_app/settings.json")
settings.exists("Injuries")
```
