# gw2-gemstore-miner

Shoddy python script for finding out what the gemstore schedule is until next patch, ready-for-reddit formatted.

But hey, it worked well enough for me. Still better than spending half an hour finding the items manually.

Before you start:
* make sure your WIN_USER is correct.

Flow:
* Before patch (or after), go to your windows %tmp% folder and clean up your gw2 folders. 
  Only really needed if you have multiple of those folders, like when you use LaunchBuddy for multiboxing.
* After patch, launch the game and open gem store window and let it load. 
  This downloads the gem store stuff to your temp folder.
* Go to your %tmp% folder, copy the GW2 folder name and put it in FOLDER_NAME
* Put the patch day's date into TODAY, the hours are before patch time so no need to touch that.
* Run it
* You'll get list of stuff and no picture links. Look at the list and take the new items out and put them into new_names
* Run again, now you get pic links too
* Next patch tends to be on Tuesday after the furthest item, 
  eg last item is on Friday, then patch on Tuesday after that,
  or last item is on Tuesday, then patch is on same day