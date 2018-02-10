import discord
import asyncio
import random
import time
from collections import defaultdict


# initializing model
model_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))

def choose_word(markov):
    randval = random.random()
    cursum = 0.0
    for word in markov:
        cursum += markov[word]
        if randval < cursum:
            return word

def generate_message(model):
    message_length = random.randint(5, 15)
    model_num = 0
    message = []
    while len(message) < message_length:
        if model_num == 0:
            message.append(choose_word(model[0][()]))
            model_num += 1
        else:
            previous = message[-model_num:]
            if tuple(previous) in model[model_num]:
                message.append(choose_word(model[model_num][tuple(previous)]))
                model_num += 1
            else:
                model_num -= 1
    return " ".join(message)



client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print("LEARNING")
    for serv in client.servers:
        try:
            with open(serv.id + "messages.txt") as data:
                for message in data.readlines():
                    split = message.split()
                    for index in range(len(split)):
                        word = split[index]
                        cur = split[:index]
                        if index == 0:
                            model_dict[serv.id][0][()][word] += 1
                        else:
                            while len(cur) > 0:
                                curt = tuple(cur)
                                model_dict[serv.id][len(cur)][curt][word] += 1 
                                cur = cur[1:]                   
            for markov in model_dict[serv.id].values():
                for value in markov.values():
                    occurences = float(sum(value.values()))
                    for item in value:
                        value[item] = value[item] / occurences
        except FileNotFoundError:
            print("File not found.")
    print("LEARNED")


@client.event
async def on_message(message):
    if message.content.startswith("!msg"):
        await client.send_message(message.channel, generate_message(model_dict[message.server.id]))
    elif message.author.id != client.user.id:
        with open(message.server.id + "messages.txt", "a") as msgfile:
            msgfile.write(message.content + "\n")


client.run("YOUR KEY HERE")

