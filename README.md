# Vaishnabot

Vaishnabot is a telegram bot to notify and provide information about Vaishnavism and its events.

### About

The bot is currently deployed to Heroku and you can test him at https://t.me/VaishnavismNotifyBot. All the data is stored in
a postgresql database, also inside Heroku app.

It currently has support for the following commands:

```
/start (default one)
/help (display the list of available commands)
/ekadasi (get a pdf document with the ekadasi dates)
/iskcon_events (get a pdf document with the iskcon events)
```

### Todo 

This application started as a hobby to learn how to code a bot for telegram using python but I'd like to make it bigger
and add more features:

- [ ] Remider for events, 24/12 hrs before they start.
- [ ] Add more important events
- [ ] Improve the pdf layout for the events (currently using basic bootstrap)
- [ ] Send a message every day at a given hour about information of something interesting (avatars, gita, etc, ...)


## Links

[Vaishnavism events](https://www.drikpanchang.com/) 
