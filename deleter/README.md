A simple Discord chat deleter<br>

### Config

Configure `config.json` file.

### Get requirements

1. Open `https://discordapp.com/` in your browser
2. Login and enable developer mode on your Discord account

### How to get authorization token in Chrome

1. Press `f12` key on your keyboard
2. Click `Network` tab then `XHR`
3. Refresh page using `f5` key on your keyboard
4. Under `Name` tab click the `science` then `Headers`
5. Scroll through `Headers` until you find `authorization` then copy that into `config.json`

### How to get channel id in Chrome

1. Select the channel you wish to get the channel id of
2. Within the URL bar you should see something similar to: `https://discordapp.com/channels/@me/098765432109876543`
3. `098765432109876543` would be the channel id

### Admin user

If the channel is a server and user has admin privs

### Install requirements

```shell
$> pip install requirements.txt
```

### Run

```shell
$> python deleter.py
```
