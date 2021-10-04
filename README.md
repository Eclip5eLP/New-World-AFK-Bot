# New World AFK Bot

## Info

This Bot will open your chat and type things into your group or consul chat to avoid being kicked.<br/>(Make sure you are a consul or in a group)<br/>
This should be very hard to detect in contrast to other bots that just walk into a corner.<br/>

## How to use

Run ```python core.py``` in your terminal.<br/>
If you are on windows you can also just execute the ```run.bat``` file.<br/>
<br/>

## Settings

```
{
    "msgList": ["Yes", "No", "lol"],
    "waitTime": 120
}
```
<br/>

```msgList``` - Specifies the words or phrases the bot will type into chat.<br/>
```waitTime``` - Specifies the time until a new message will be sent (in seconds).


# Fishing Bot

## Info

Will start fishing once you press F3 to take out the fishing rod.<br/>

## How to use

Run ```python core.py``` in your terminal.<br/>
If you are on windows you can also just execute the ```run.bat``` file.<br/>
<br/>

## Settings

```
{
    "bait": "NULL",
    "reelTime": 1.8,
    "repairCycle": 20
    "hotkeys": ["ctrl", "f11"]
}
```
<br/>

```bait``` - Use the specified bait for catching. (Currently not implemented)<br/>
```reelTime``` - Duration for which the reel will be held down (in seconds).<br/>
```repairCycle``` - Fishing cycles completed until trying to repair the fishing rod.<br/>
```hotkeys``` - 1 = Pause Key, 2 = Quit Key.<br/>
