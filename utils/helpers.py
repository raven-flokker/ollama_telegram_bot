import random


def random_greeting():
    responses = [
        "Мяу. Ты что, просто мяукал? 🐾",
        "Мяу. Я сплю. Не мешай. 🐾",
        "Мяу. А ты чем занимаешься? 🤔",
        "Мяу. Я не обязан отвечать. 🤡",
        "Мяу. Я котик гений. А ты кто? 🐾🤖"
    ]
    return random.choice(responses)
