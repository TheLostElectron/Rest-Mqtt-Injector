# Rest-Mqtt-Injector
 Webhooks are an easy to implement way for servers across the internet to notify each other of events, and trigger action. Because of this, many services will integrate with a webhook in some way, from GitHub on pushes, to IFTTT on tweets from your favourite user. Unfortunately a lot of hobbyist developers are without a way to receive webhooks on their creations reliably. While there are a couple services on the internet to forward REST requests over mqtt, most require authentication headers in the incoming web request. From my experience, a lot of the services I used that used webhooks, did not support custom headers, which once again posed a problem for getting it on homebuilt creations. 
 
 That was the birth of this idea. A bare-bones script to take random, unauthenticated webhooks, and forward them over mqtt. This allowed me to finally get my computer to be able to scream on command from Google Assistant, through the simple path of *Google Assistant->IFTTT->Outgoing Webhooks->Incoming Webhooks->This Script->MQTT Broker->Python MQTT Client*
 
 --- 
  ### Installation
  Installation is quite simple.
  - Clone this repository with `git clone https://github.com/TheLostElectron/Rest-Mqtt-Injector`
  - Enter the directory with `cd Rest-Mqtt-Injector`
  - Run the script with `python3 webToMqtt.py`

 ---

  ### Security
 In the current version, there is no security whatsoever. Anyone can edit, or add to your configuration simply by knowing where it is hosted. I will be addressing this in the future, but it works for now. The passwords used for mqtt are incredibly easy to access given access to the script itself, although it is a little bit  more difficult to get them from the web interface. 
  ### Future
 In the future, I'm hoping to make a full site for this. A site with a decent user interface, authentication, some form of security, and scalable.

