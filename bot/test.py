from helpers.beautify import beautify_events



def test():
    print("this is a test")
    events = [
    {
                "name": "Pausha Putrada Ekadashi",
                        "date": "January 6, 2020, Monday",
                            },
        {
                    "name": "Shattila Ekadashi",
                            "date": "Ferbuary 6, 2020, Monday",
                                },
            {
                        "name": "Pausha Putrada Ekadashi",
                                "date": "April 20, 2020, Monday",
                                    },
    ]
    beautify_events({"events": events, "year": 2020, "month": "October" }, kind="ekadasi_events")
