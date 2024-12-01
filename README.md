NOTE: if this doesn't work, you need to add your own client-id and bearer token. You could do it with the --client-id and --authorization command line arguments, or just change the default client_id and auth lines.

You get your client-id and access tokens here: https://twitchtokengenerator.com/

![C7278D90-628E-43E0-83F3-DE43ED46AAE2](https://github.com/bshang165-2/dl-twitch/assets/138236136/e155c0e2-9c57-43ec-b95b-b2fbc0d3dc96)



    else:
        #auth = 'Bearer 34o73hb40ag2g50sz38wjgyb1rjpmw'
        auth = 'Bearer kkm7qh0sgokps8vgt4xtwk32994x9r'
    if client_id:
        client_id = client_id
    else:
        #client_id = '43zeiffzo1vaceatiyp58fzbynqhlq'
        client_id = 'gp762nuuoqcoxypju8c569th9wz7q5'

---

Pre-requisites: python(3), selenium, and Google Chrome (or for testing or whatever works with chromedriver) + chromedriver

https://chromedriver.chromium.org/downloads (use wget rather than curl -O or whatever... same i think..... wget is a wrapper and a parser....)

also yt-dlp (use pip install or brew install or apt install or choco or rpm or whatever) and ffmpeg (same) if you want to download videos. can't include ffmpeg in requirements.txt unless i write it PURELY in python or cpython.. :(((( 


---

Usage: python (or python3) dl_twitch.py user_name1 user_name2 etc.

Video of sample usage: https://www.youtube.com/watch?v=SelWmJm2Stg

---

6/23/2023 UPDATE: I think they actually broke their own API to stop the gathering of gambling streamers and their content. I don't see any bugs in my code, but there's always the possibility. Right now their API ignores the game_id parameter for get streams so it just gets everyone. Right now I'll display a temporary archive of mostly-illegal casino streamers promoting their own referral links at the very least, but I plan to get their whole data for "larger" streamers anyways: https://www.dropbox.com/sh/luy0xux3xalp2k8/AABSzu2rWqJT0mHdzEkxoOAja?dl=0

---

Illegal gambling streamers specific usage:

Specific usage: python dl_twitch.py --games casino -NV (grabs metadata and screenshots for all the casino and poker streamers, including slots, blackjack, etc)

Specific usage 2: python dl_twitch.py --games casino (also downloads videos in 480p for all casino and poker streamers)

Experimental: sh gamblers_autorun.sh (this shouldn't crash your filesystem compared to autorun.sh because there's only 100-200 gambling streams on Twitch at once, but it's still experimental)

Sample Dropbox links displaying gambling stream screenshots: 

1) https://www.dropbox.com/sh/9fsnvn7auwiijo5/AADgknLY1NJM_iHRHZyUJLuUa?dl=0

2) https://www.dropbox.com/sh/jx76dse4ex4z9xp/AABB2D-D0FgTAf7250oTpvaoa?dl=0

---

Arguments: python dl_twitch.py --games (to get specific games that string match) -NV (no videos to downlaod) -TS (get top streamers information) --pages (specify how many pages * 100 streamers you want to download; replaces the -TS flag) -NS (no screenshots) -STAFF (get Twitch staff data)

Additional arguments: python dl_twitch.py -h

Experimental: sh autorun.sh (this may crash filesystem after grabbing screenshots and running for a long time; may need to append screenshots together to not crash)


---

To detect illegal gambling streamers static algorithms may be sufficient, but the idea is to start designing a general purpose algorithm that detects dangerous or illegal activities on the Internet. The possibilities of how to do this is endless, and I don't think adding random layers to all the raw data will work well. I think you need much more targeted design principles, but I think you definitely can train useful models with proper design.

- Possible Federal violation 1: 18 U.S. Code § 1084 - Transmission of wagering information; penalties
https://www.law.cornell.edu/uscode/text/18/1084

- Possible Federal violation 2: 18 U.S. Code § 1955 - Prohibition of illegal gambling businesses
https://www.law.cornell.edu/uscode/text/18/1955

- Possible Federal violation 3: 18 U.S. Code § 1956 - Laundering of monetary instruments
https://www.law.cornell.edu/uscode/text/18/1956

- Possible Federal violation 4 (Twitch overall in a nutshell): 18 U.S. Code § 1343 - Fraud by wire, radio, or television
https://www.law.cornell.edu/uscode/text/18/1343

---

20 headless chrome demo usage: https://www.youtube.com/watch?v=fvvegqhXbLg

download all vidoes 15 thraeds at a time: https://www.youtube.com/watch?v=S5harHGAutY

getting all metadata (use the -TS flag): https://www.youtube.com/watch?v=le5WDC6v10w
