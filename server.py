#import necessary dependencies
import discord
import os
import json
import datetime
from discord.ext import commands, tasks
from random import *
import sys

#initialize token and client
TOKEN = os.environ["INSERT_TOKEN_HERE"]
client = commands.Bot(command_prefix="wurf ", case_insensitive=True)

#useful functions
def saveToFile(filename, data):
    obj = json.dumps(data, indent=4)
    with open(filename, 'w') as outfile:
        outfile.write(obj)

def readFromFile(filename):
    with open(filename, "r") as infile:
        obj = json.load(infile)
    return obj

def haveFile(name, folder):
    for i in os.listdir(folder):
        fileName = i.split(".")[0]
        if name == fileName:
            return True
        else:
            pass
    return False


def sortCrumbs(array):
    return array[1]



#####################
#Custom Status, startup
#####################
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"wurf help | in {len(client.guilds)} servers"))

@client.event
async def on_guild_join(guild):
    print(f"Bot was added to a new server called {guild}! Bot is now in {len(client.guilds)} guilds!")
    owner = guild.owner
    await owner.send(f"Hello, my name is **Bread Dog**, a fat bot jam-packed with functionality. \nI was recently added to your server {guild}. The bot has the following: \nA moderation system that can: Kick, Warn, Mute, Ban \nA utility system for flipping coins, and other commonly needed functions \nAnd a fun economy system ^^ \nNot sure what to do? Simply type `wurf help`!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"wurf help | in {len(client.guilds)} servers"))



#####################
#Commands
#####################


#Custom help command
class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=0xff4500, description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

#Utility Category
class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(
        help="Shows the ping/latency of the bot in miliseconds.",
        brief="Shows ping."
    )
    async def ping(self, ctx):
        if round(client.latency * 1000) <= 50:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(client.latency *1000)}** milliseconds!", color=0x44ff44)
        elif round(client.latency * 1000) <= 100:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(client.latency *1000)}** milliseconds!", color=0xffd000)
        elif round(client.latency * 1000) <= 200:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(client.latency *1000)}** milliseconds!", color=0xff6600)
        else:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(client.latency *1000)}** milliseconds!", color=0x990000)
        await ctx.send(embed=embed)

    @commands.command(
        help="Flip a coin!",
        brief="Flip a coin!"
    )
    async def flip(self, ctx):
        if randint(1, 2) == 1:
            embed=discord.Embed(title="Heads!", description="**You flipped a heads!**", color=0x33ff33)
            await ctx.channel.send(embed=embed)
        else:
            embed=discord.Embed(title="Tails!", description="**You flipped a tails!**", color=0xff3333)
            await ctx.channel.send(embed=embed)
    
    @commands.command(
        help="Displays your user ID.",
        brief="Displays your user ID."
    )
    async def findUserId(self, ctx, user:discord.Member=None):
        if not(user):
            user = ctx.message.author
        await ctx.channel.send(f"The user ID for {user} is: {user.id}")
    

    @commands.command(
        help="Get the ID of your guild/server.",
        brief="Get the Id of your guild."
    )
    async def guildId(self, ctx):
        await ctx.channel.send(f"{ctx.message.guild.id}")
    

    @commands.command(
        help="See how many servers/guilds this bot is in!",
        brief="See how many servers this bot is in!",
        aliases=["botGuilds", "botGuildCount", "botServerCount"]
    )
    async def botServers(self, ctx):
        embed = discord.Embed(title="Bot's server count:", description=f"Bread Dog is currently in **{len(client.guilds)}** guilds!")
        await ctx.channel.send(embed=embed)





#Extra Category
class Extra(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(
        help="Link for inviting this bot.",
        brief="Link for inviting this bot."
    )
    async def invite(self, message):
        embed=discord.Embed(title="Invite Bread Dog!", description="You can invite our bot here:\nhttps://discord.com/api/oauth2/authorize?client_id=745366103706042521&permissions=8&scope=bot", color=0xffff33)
        await message.channel.send(embed=embed)

    @commands.command(
        help="Wanna join our discord server? Run this command and click on the link!",
        brief="Dispalys link to our official server.",
    )
    async def join(self, message):
        embed=discord.Embed(title="Join Our Official Server!", description="Join our Official Discord Server here:\nhttps://discord.gg/A62QpsZ", color=0xffff33)
        await message.channel.send(embed=embed)

    @commands.command(
        help="Greets you back with a Hello followed by your username.",
        brief="Greetings!"
    )
    async def hello(self, message):
        await message.channel.send(f"Hello, {message.author}!")
    
    @commands.command(
        help="Greets you with a happy wurf!",
        brief="Wurf Wurf Wurf!"
    )
    async def wurf(self, message):
        await message.channel.send("Wurf Wurf Wurf!")
    

    @commands.command(
        help="Look at the code for this bot on GitHub! Please don't try to copy our bot, you can make parodies, but no direct copies. Thank you!",
        brief="Check out our code! All rights reserved.",
        aliases=["source", "sourceCode", "gitHub"]
    )
    async def code(self, ctx):
        await ctx.channel.send(f"{ctx.message.author}, the code for this bot can be found here:\nhttps://github.com/CheetSheatOverlode/breaddog\nAll rights reserved. You can take the code to make a parody of our bot, but you may not directly copy it.")




#Moderation Category
class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.has_permissions(kick_members=True)
    @commands.command(
        help="Kicks members from your server. They can still come back",
        brief="Kicks members from server.",
        aliases=["softban"]
    )
    async def kick(self, ctx, member: discord.Member=None, *, reason="None specified"):
        if not(member):
            await ctx.channel.send(f"{ctx.message.author} yo you gotta tell me someone to kick right?")
            return
        a = ctx.guild.roles
        a.reverse()
        print(a)
        for r in a:
            if r not in member.roles:
                if r in ctx.message.author.roles:
                    try:
                        channel = await member.create_dm()
                        await channel.send(
                            f'{member.name}, you were kicked from the server by {ctx.message.author}.'
                            f' | Reason: %s. You may contact them to appeal or get reinvited.' % reason
                        )
                    except:
                        pass
                    await member.kick(reason=reason)
                    l = []
                    l.append("%s has been kicked by %s" % (member, ctx.message.author))
                    l.append("Action: Kick")
                    l.append("Member kicked: %s" % member)
                    l.append("Moderator responsible: %s" % ctx.message.author)
                    l.append("Reason: %s" % reason)
                    m = l[1:]
                    embed = discord.Embed(title="{}".format(l[0]),
                                        description="{}".format('\n'.join(m)))
                    await ctx.channel.send(embed=embed)
    
    @commands.has_permissions(ban_members=True)
    @commands.command(
        help="Ban hammer go bam. User is now banned. They can't come back.",
        brief="Bans someone from your server."
    )
    async def ban(self, ctx, member: discord.Member = None, *, reason="None Specified"):
        if not(member):
            await ctx.channel.send(f"{ctx.message.author} yo you gotta tell me someone to kick right?")
            return
        a = ctx.guild.roles
        a.reverse()
        for r in a:
            if r in member.roles:
                if r not in ctx.message.author.roles:
                    try:
                        channel = await member.create_dm()
                        await channel.send(
                            f'{member.name}, you were banned from the server by {ctx.message.author}.'
                            f' | Reason: %s. You may contact them to appeal or get reinvited.' % reason
                        )
                    except:
                        pass
                    await member.ban(reason=reason)
                    l = []
                    l.append("%s has been banned by %s" % (member, ctx.message.author))
                    l.append("Action: Ban")
                    l.append("Member banned: %s" % member)
                    l.append("Moderator responsible: %s" % ctx.message.author)
                    l.append("Reason: %s" % reason)
                    m = l[1:]
                    embed = discord.Embed(title="{}".format(l[0]),
                                        description="{}".format('\n'.join(m)))
                    await ctx.channel.send(embed=embed)
                    break
    

    @commands.command(
        help="Pardon someone from a ban.",
        brief="Unban someone.",
        aliases=["pardon"]
    )
    async def unban(self, ctx, *, member=None):
        if not(member):
            await ctx.channel.send("Don't know what you're thinking, you gotta tell me someone to unban.")
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
    
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            try:
                await ctx.guild.unban(user)
                await ctx.send(f"{user} has been unbanned sucessfully")
            except:
                await ctx.channel.send(f"{ctx.message.author}: Can't do that.")
            return

    @commands.command(
        help="Makes it so that toxic people can't talk. You must have a role called Muted in your server. Change its permissions so that it 'Send Messages' is off. It must be the highest role for somebody in order to mute them.",
        brief="Mute toxic people."
    )
    async def mute(self, ctx, member: discord.Member=None):
        if member.id == ctx.message.author.id:
            await ctx.channel.send(f"{ctx.message.author} WHAAAAT you want to mute yourself?")
            return
        if not(member):
            await ctx.channel.send("Sure thing. But next time tell me who to mute, alright?")
            return
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        user = member
        await user.add_roles(role)
        embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff0000)
        await ctx.channel.send(embed=embed)


    @commands.command(
        help="Warn a user. Note that this doesn't do anything excpet DM them.",
        brief="Warn a user that they're about to get butt-banned."
    )
    async def warn(self, ctx, member:discord.Member=None, *, reason=None):
        await ctx.channel.send("%s has been warned by %s. Reason: %s" % (member, ctx.message.author, reason))
        channel = await member.create_dm()
        await channel.send(
            f'{member.name}, you were warned by {ctx.message.author}.\nReason: {reason}'
        )





#Economy Category
class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        help="Set up your account, and money.",
        brief="Set up your account, and money."
    )
    async def setup(self, ctx):
        hasAccount = haveFile(str(ctx.message.author.id), "Users")
        if not(hasAccount):
            userData = {
                "name":str(ctx.message.author).split("#")[0],
                "discriminator":str(ctx.message.author).split("#")[1],
                "crumbs":1000,
                "timeBeg":(2020, 1, 1, 1, 1, 1),
                "timeDaily":(2020, 1, 1),
                "timeWeekly":(2020, 1, 1),
                "timeWork":(2020, 1, 1, 1, 1, 1),
                "timeRob":(2020, 1, 1, 1, 1, 1),
                "dailyStreak":0,
                "job":None,
                "inventory":{},
                "pets":{},
                "notifications":{}
            }
            saveToFile("Users/" + str(ctx.message.author.id) + ".json", userData)
            await ctx.channel.send(f"Set {ctx.message.author} up with 1000 bread crumbs!")
        else:
            await ctx.channel.send(f"{ctx.message.author}, don't try to cheat me! You already have an account! Use the other currency commands, like a normal person!")
    

    @commands.command(
        help="Check your bread crumbs balance",
        brief="Check your balance!",
        aliases=["bal", "amount", "crumbs"]
    )
    async def balance(self, ctx, member:discord.Member=None):
        try:
            userId = member.id
        except:
            userId = ctx.message.author.id
        if not(member):
            member = ctx.message.author
            userId = ctx.message.author.id
        if haveFile(str(userId), "Users"):
            userData = readFromFile("Users/" + str(userId) + ".json")
            balance = userData["crumbs"]
            await ctx.channel.send(f"{member}'s balance:\n{balance} bread crumbs.")
        else:
            if member == ctx.message.author:
                await ctx.channel.send(f"{member}, you don't have a balance yet. You can get one by doing `wurf setup`.")
            else:
                await ctx.channel.send(f"{member} doesn't have a balance in Bread Dog!")
            
    

    @commands.command(
        help="Hungry? Beg for some bread crumbs!",
        brief="Beg for some bread crumbs."
    )
    async def beg(self, ctx):
        userId = ctx.message.author.id
        if haveFile(str(userId), "Users"):
            userData = readFromFile("Users/" + str(ctx.message.author.id) + ".json")
            today = datetime.datetime.today()
            now = (int(today.year), int(today.month), int(today.day), int(today.hour), int(today.minute), int(today.second))
            lastBeg = datetime.datetime(userData["timeBeg"][0], userData["timeBeg"][1], userData["timeBeg"][2], userData["timeBeg"][3], userData["timeBeg"][4], userData["timeBeg"][5])
            if ((datetime.datetime(int(today.year), int(today.month), int(today.day), int(today.hour), int(today.minute), int(today.second)) - lastBeg).seconds / 60) > 5:
                amount = randint(0, 200)
                userData["crumbs"] += amount
                await ctx.channel.send(f"{ctx.message.author} begged in the streets and earned **{amount}** crumbs.")
                userData["timeBeg"] = now
                saveToFile("Users/" + str(ctx.message.author.id) + ".json", userData)
            else:
                await ctx.channel.send(f"{ctx.message.author}, you already begged in the last 5 minutes. Wait a bit.")
        else:
            await ctx.channel.send(f"{ctx.message.author}, you don't have a balance yet. Get one by doing `wurf setup`.")
    

    @commands.command(
        help="Get your daily dose of bread crumbs!",
        brief="Get your daily bread crumbs!"
    )
    async def daily(self, ctx):
        userId = ctx.message.author.id
        if haveFile(str(userId), "Users"):
            userData = readFromFile("Users/" + str(ctx.message.author.id) + ".json")
            my_date = datetime.date.today()
            year, week, day = my_date.isocalendar()
            now = [year, week, day]
            lastDaily = [userData["timeDaily"][0], userData["timeDaily"][1], userData["timeDaily"][2]]
            streak = userData["dailyStreak"]
            if (now[1]*7 + now[2]) > (lastDaily[1]*7 + lastDaily[2]):
                amount = 1000 + (streak * 100)
                userData["crumbs"] += amount
                await ctx.channel.send(f"{ctx.message.author} got their daily 1000 crumbs. They also got {streak * 100} crumbs as a reward for a {streak} daily streak. The daily resets every day at 12 AM EST.")
                if (now[1]*7 + now[2]) - (lastDaily[1]*7 + lastDaily[2]) <= 1:
                    userData["dailyStreak"] += 1
                else:
                    userData["dailyStreak"] = 0
                userData["timeDaily"] = now
                saveToFile("Users/" + str(ctx.message.author.id) + ".json", userData)
            else:
                await ctx.channel.send(f"{ctx.message.author}, you already got your daily. You can get one every day at 12 AM EST.")
                return
        else:
            await ctx.channel.send(f"{ctx.message.author}, you don't have a balance yet. Get one by doing `wurf setup`.")
        

    @commands.command(
        help="Get your weekly dose of bread crumbs!",
        brief="Get your weekly bread crumbs!"
    )
    async def weekly(self, ctx):
        userId = ctx.message.author.id
        if haveFile(str(userId), "Users"):
            userData = readFromFile("Users/" + str(ctx.message.author.id) + ".json")
            my_date = datetime.date.today()
            year, week, day = my_date.isocalendar()
            now = [year, week, day]
            lastWeekly = [userData["timeWeekly"][0], userData["timeWeekly"][1], userData["timeWeekly"][2]]
            if now[1] > lastWeekly[1]:
                amount = 5000
                userData["crumbs"] += amount
                await ctx.channel.send(f"{ctx.message.author} got their weekly 5000 crumbs. It resets every Sunday at midnight, EST.")
                userData["timeWeekly"] = now
                saveToFile("Users/" + str(ctx.message.author.id) + ".json", userData)
            else:
                await ctx.channel.send(f"{ctx.message.author}, you already got your weekly. It resets every Sunday at midnight, EST.")
        else:
            await ctx.channel.send(f"{ctx.message.author}, you don't have a balance yet. Get one by doing `wurf setup`.")
    

    @commands.command(
        help="Bet some crumbs to earn more, or lose.",
        brief="Bet some crumbs.",
        aliases=["gamble"]
    )
    async def bet(self, ctx, amount:int):
        userId = ctx.message.author.id
        if haveFile(str(userId), "Users"):
            if not(amount):
                await ctx.channel.send(f"{ctx.message.author}, tell me what to bet! Don't make me pick for you!")
                return
            elif amount < 1:
                await ctx.channel.send(f"{ctx.message.author} quit wasting my time. I gotta spend my energy handling REAL requests. Hmmmph.")
                return
            userData = readFromFile("Users/" + str(ctx.message.author.id) + ".json")
            if userData["crumbs"] >= amount:
                if randint(0, 1) == 1:
                    await ctx.channel.send(f"{ctx.message.author}, you won **{amount}** crumbs! NICE.")
                    userData["crumbs"] += amount
                    saveToFile("Users/" + str(ctx.message.author.id) + ".json", userData)
                else:
                    await ctx.channel.send(f"{ctx.message.author}, you lost **{amount}** crumbs. Haha sucks to be you.")
                    userData["crumbs"] -= amount
                    saveToFile("Users/" + str(ctx.message.author.id) + ".json", userData)
            else:
                await ctx.channel.send(f"{ctx.message.author}: Can't you do the math? You can't afford that bet. Go back to preschool smh.")
        else:
            await ctx.channel.send(f"{ctx.message.author}, you don't have a balance yet. Get one by doing `wurf setup`.")
    

    @commands.command(
        help="Attempt to rob someone.",
        brief="Attempt to rob someone.",
        aliases=["steal"]
    )
    async def rob(self, ctx, target:discord.Member=None):
        userId = ctx.message.author.id
        if not(target):
            await ctx.channel.send(f"{ctx.message.author} you gotta mention someone to rob, right?")
            return
        targetId = target.id
        if str(targetId) == "699659941572640788":
            await ctx.channel.send(f"Trying to rob the devs, {ctx.message.author}? Seriously? They work their butts off to bring you this good game, and this is how you repay them? By robbing them? Screw off.")
            return
        elif targetId == userId:
            await ctx.channel.send(f"{ctx.message.author} WHAAAAT you want to rob yourself?")
            return
        if haveFile(str(userId), "Users"):
            if haveFile(str(targetId), "Users"):
                userData = readFromFile("Users/" + str(userId) + ".json")
                targetData = readFromFile("Users/" + str(targetId) + ".json")
                if userData["crumbs"] >= 500:
                    if targetData["crumbs"] >= 500:
                        if "timeRob" not in userData:
                            userData["timeRob"] = (2020, 1, 1, 1, 1, 1)
                        today = datetime.datetime.today()
                        now = (int(today.year), int(today.month), int(today.day), int(today.hour), int(today.minute), int(today.second))
                        lastRob = datetime.datetime(userData["timeRob"][0], userData["timeRob"][1], userData["timeRob"][2], userData["timeRob"][3], userData["timeRob"][4], userData["timeRob"][5])
                        if not ((datetime.datetime(int(today.year), int(today.month), int(today.day), int(today.hour), int(today.minute), int(today.second)) - lastRob).seconds / 60) > 5:
                            await ctx.channel.send(f"{ctx.message.author}, you already robbed someone in the last five minutes. Take a break, or you're gonna get busted.")
                            return
                        if randint(1, 10) >= 3:
                            percent = randrange(20, 50)
                            amount = int(targetData["crumbs"] * percent * 0.01)
                            targetData["crumbs"] -= amount
                            userData["crumbs"] += amount
                            userData["timeRob"] = now
                            targetData["notifications"][str(datetime.datetime.now())] = f"{ctx.message.author} stole {amount} crumbs from you in {ctx.message.guild}!"
                            saveToFile("Users/" + str(userId) + ".json", userData)
                            saveToFile("Users/" + str(targetId) + ".json", targetData)
                            await ctx.channel.send(f"{ctx.message.author} stole {amount} bread crumbs from {target}. HAHAHAHAHAHAHAHA")
                        else:
                            if userData["crumbs"] < 1000:
                                userData["crumbs"] = 0
                                userData["job"] = None
                                targetData["notifications"][str(datetime.datetime.now())] = f"{ctx.message.author} tried to steal crumbs from you in {ctx.message.guild}, but failed!"
                                saveToFile("Users/" + str(userId) + ".json", userData)
                                saveToFile("Users/" + str(targetId) + ".json", targetData)
                                await ctx.channel.send(f"{ctx.message.author} tried to rob {target}, but got busted by the cops.\nThey couldn't pay the bribe of 1000 bread crumbs, so they got shot and died. They lost all their money and their job.")
                            else:
                                userData["crumbs"] *= 0.5
                                userData["crumbs"] = int(userData["crumbs"])
                                userData["job"] = None
                                targetData["notifications"][str(datetime.datetime.now())] = f"{ctx.message.author} tried to steal crumbs from you in {ctx.message.guild}, but failed!"
                                saveToFile("Users/" + str(userId) + ".json", userData)
                                saveToFile("Users/" + str(targetId) + ".json", targetData)
                                await ctx.channel.send(f"{ctx.message.author} tried to rob {target}, but got busted by the cops.\nThey had to pay the bribe to get out of jail. They lost half their money and their job.")
                    else:
                        await ctx.channel.send(f"{ctx.message.author}, your target {target} does not have 500 crumbs. Not worth it.")
                else:
                    await ctx.channel.send(f"{ctx.message.author}, you don't have enough crumbs. You need at least 500 crumbs to rob someone.")
            else:
                await ctx.channel.send(f"{ctx.message.author}, your target {target} doesn't have a balance yet. Hence, you won't get any money.")
        else:
            await ctx.channel.send(f"{ctx.message.author}, you don't have a balance yet. Get one by doing `wurf setup`.")
    

    @commands.command(
        help="Display notifications in the currency system.",
        brief="Display notifications.",
        aliases=["notifs"]
    )
    async def notifications(self, ctx):
        userId = ctx.message.author.id
        if haveFile(str(userId), "Users"):
            userData = readFromFile("Users/" + str(userId) + ".json")
            notifs = userData["notifications"]
            notification = {}
            for i in list(sorted(notifs.keys(), reverse=True)):
                notification[i] = notifs[i]
            length = len(notification)
            for i in list(sorted(notifs.keys(), reverse=True))[-(length-10):]:
                notification.pop(i)
            msg = []
            for i in notification.keys():
                msg.append(i+"\n"+notification[i])
            mesg = "\n".join(msg)
            if notifs == {}:
                mesg = "None"
            await ctx.channel.send(f"{ctx.message.author}'s notifications:\n{mesg}")
        else:
            await ctx.channel.send(f"{ctx.message.author}, you don't have a balance yet. Get one by doing `wurf setup`.")
    

    @commands.command(
        help="Share some crumbs with another user to be nice!",
        brief="Give some crumbs to another user!",
        aliases=["share"]
    )
    async def give(self, ctx, target:discord.Member=None, amount:int=None):
        if not(target):
            await ctx.channel.send(f"{ctx.message.author} sure thing, but tell me someone to share with, ok? Don't make me keep the money for myself.")
            return
        elif not(amount):
            await ctx.channel.send(f"{ctx.message.author} ok but how much am I supposed to send? Grrrr people these days.")
            return
        elif amount < 1:
            await ctx.channel.send(f"{ctx.message.author} what? You tryna break or cheat me? Hmmmph.")
            return
        userId = ctx.message.author.id
        targetId = target.id
        if userId == targetId:
            await ctx.channel.send(f"{ctx.message.author} Yo you can't give yourself coins ok that's called cheating stop it")
            return
        if haveFile(str(userId), "Users"):
            if haveFile(str(targetId), "Users"):
                userData = readFromFile("Users/" + str(userId) + ".json")
                targetData = readFromFile("Users/" + str(targetId) + ".json")
                if userData["crumbs"] < amount:
                    await ctx.channel.send(f"{ctx.message.author} Can't you do the math? You don't have enough crumbs. Hence, you can't send that many.")
                    return
                else:
                    if randint(1, 5) == 1:
                        percent = randrange(25, 75)
                        userData["crumbs"] -= amount
                        newAmount = int(amount*(100-percent)/100)
                        targetData["crumbs"] += newAmount
                        targetData["notifications"][str(datetime.datetime.now())] = f"{ctx.message.author} tried to send you {amount} crumbs in {ctx.message.guild}, but the shipment was attacked by pirates on the way, and only {newAmount} crumbs got to you!"
                        saveToFile("Users/" + str(userId) + ".json", userData)
                        saveToFile("Users/" + str(targetId) + ".json", targetData)
                        await ctx.channel.send(f"{ctx.message.author} tried to send {target} {amount} crumbs in {ctx.message.guild}, but the shipment was attacked by pirates on the way, and only {newAmount} crumbs got through!")
                    else:
                        userData["crumbs"] -= amount
                        targetData["crumbs"] += amount
                        targetData["notifications"][str(datetime.datetime.now())] = f"{ctx.message.author} sent you {amount} crumbs in {ctx.message.guild}!"
                        saveToFile("Users/" + str(userId) + ".json", userData)
                        saveToFile("Users/" + str(targetId) + ".json", targetData)
                        await ctx.channel.send(f"{ctx.message.author} successfully sent {target} {amount} crumbs!")
            else:
                await ctx.channel.send(f"{ctx.message.author}, the person you're trying to give crumbs to doesn't have an account. Hence, they probably won't use it.")
        else:
            await ctx.channel.send(f"{ctx.message.author}, you don't have a balance yet. Get one by doing `wurf setup`.")
    

    @commands.command(
        help="Look for a job!",
        brief="Look for a job!"
    )
    async def apply(self, ctx, job:str=None):
        jobs = [
            ("Janitor", 100, 1000),
            ("Cashier", 200, 2500),
            ("Chef", 250, 5000),
            ("Teacher", 500, 10000),
            ("Librarian", 1000, 20000),
            ("Nurse", 1500, 50000),
            ("Doctor", 2000, 100000),
            ("Bread Dog Developer", 20000, 100000000)
        ]
        userId = ctx.message.author.id
        if haveFile(str(userId), "Users"):
            userData = readFromFile("Users/" + str(userId) + ".json")
            if not(job):
                msg = []
                for j in jobs:
                    msg.append(str(j[0])+":\n"+"Salary = "+str(j[1])+"\n"+"Application Price = "+str(j[2])+"\n")
                message = "\n".join(msg) + "\nApply for a job by doing `wurf apply <job>`."
                final = discord.Embed(title="The current jobs are:", description=message, color=0xffaaff)
                await ctx.channel.send(embed=final)
            else:
                hasJob = False
                for i in jobs:
                    if i[0] == job.capitalize():
                        hasJob = True
                        jobIndex = jobs.index(i)
                if hasJob:
                    if userData["crumbs"] >= jobs[jobIndex][2]:
                        userData["crumbs"] -= jobs[jobIndex][2]
                        userData["job"] = jobs[jobIndex][0]
                        saveToFile("Users/" + str(userId) + ".json", userData)
                        await ctx.channel.send(f"{ctx.message.author} is now working as a **{jobs[jobIndex][0]}**!")
                    else:
                        await ctx.channel.send(f"{ctx.message.author}, can't you do the math? You can't afford to apply for that job!")
                else:
                    await ctx.channel.send(f"{ctx.message.author}, that is not a valid job. Check the list my doing `wurf apply`.")
        else:
            await ctx.channel.send(f"{ctx.message.author}, you don't have a balance yet. Get one by doing `wurf setup`")
        

    @commands.command(
        help="Work for some bread crumbs!",
        brief="Work for some bread crumbs."
    )
    async def work(self, ctx):
        jobs = [
            ("Janitor", 100, 1000),
            ("Cashier", 200, 2500),
            ("Chef", 250, 5000),
            ("Teacher", 500, 10000),
            ("Librarian", 1000, 20000),
            ("Nurse", 1500, 50000),
            ("Doctor", 2000, 100000),
            ("Bread Dog Developer", 20000, 100000000)
        ]
        userId = ctx.message.author.id
        if haveFile(str(userId), "Users"):
            userData = readFromFile("Users/" + str(userId) + ".json")
            if userData["job"]:
                for i in jobs:
                    if i[0] == userData["job"]:
                        jobIndex = jobs.index(i)
                today = datetime.datetime.today()
                now = (int(today.year), int(today.month), int(today.day), int(today.hour), int(today.minute), int(today.second))
                lastWork = datetime.datetime(userData["timeWork"][0], userData["timeWork"][1], userData["timeWork"][2], userData["timeWork"][3], userData["timeWork"][4], userData["timeWork"][5])
                if ((datetime.datetime(int(today.year), int(today.month), int(today.day), int(today.hour), int(today.minute), int(today.second)) - lastWork).total_seconds() / 3600) >= 1:
                    userData["crumbs"] += jobs[jobIndex][1]
                    userData["timeWork"] = now
                    saveToFile("Users/" + str(userId) + ".json", userData)
                    await ctx.channel.send(f"{ctx.message.author} worked for a **{jobs[jobIndex][0]}** for an hour, and earned **{jobs[jobIndex][1]}** coins.")
                else:
                    await ctx.channel.send(f"{ctx.message.author}, you already worked this hour.")
            else:
                await ctx.channel.send(f"{ctx.message.author}, you don't have a job yet. Get one by doing `wurf apply`")
        else:
            await ctx.channel.send(f"{ctx.message.author}, you don't have a balance yet. Get one by doing `wurf setup`")


    @commands.command(
        help="Check out what we have in the store! Buy some stuff!",
        brief="Check out the store!",
        aliases=["store", "market"]
    )
    async def shop(self, ctx):
        shopDict = {
            "Food":10,
            "Bread_Loaf":20,
            "Corgi_Plush":50,
            "Beer":1000,
            "Phone":5000,
            "Bitcoin":10000,
        }
        lis = [f"{key} - {shopDict[key]}" for key in shopDict.keys()]
        lineBreak = "\n"
        await ctx.channel.send(f"Bread Dog store: \n{lineBreak.join(lis)}")
    

    @commands.command(
        help="Buy something from the store!",
        brief="Buy something form the store!",
        aliases=["purchase"]
    )
    async def buy(self, ctx, item:str=None, amount:int=1):
        shopDict = {
            "Food":10,
            "Bread_Loaf":20,
            "Corgi_Plush":50,
            "Beer":1000,
            "Phone":5000,
            "Bitcoin":10000,
        }
        userId = ctx.message.author.id
        if amount < 1:
            await ctx.channel.send(f"{ctx.message.author} yo stop wasting my time if you want to sell ur stuff then sell ur stuff don't buy negative")
            return
        if haveFile(str(userId), "Users"):
            if item:
                if item in shopDict.keys():
                    userData = readFromFile("Users/" + str(userId) + ".json")
                    if userData["crumbs"] >= shopDict[item]*amount:
                        if item in userData["inventory"].keys():
                            userData["crumbs"] -= shopDict[item]*amount
                            userData["inventory"][item] += amount
                        else:
                            userData["crumbs"] -= shopDict[item]*amount
                            userData["inventory"][item] = 0
                            userData["inventory"][item] += amount
                        saveToFile("Users/" + str(userId) + ".json", userData)
                        await ctx.channel.send(f"{ctx.message.author} successfully purchased {amount} {item}")
                    else:
                        await ctx.channel.send(f"{ctx.message.author} broke kid get out you can't even afford what you're trying to buy ok")
                else:
                    await ctx.channel.send(f"{ctx.message.author}, that item isnt' in the shop. Make sure you capitalized everything.")
            else:
                await ctx.channel.send(f"{ctx.message.author}, ok but what are you going to buy?")
        else:
            await ctx.channel.send(f"{ctx.message.author}, you don't have a Bread Dog account yet. You can get one by typing `wurf setup`.")
    

    @commands.command(
        help="Check out your inventory!",
        brief="Check out your inventory!",
        aliases=["inv", "backpack"]
    )
    async def inventory(self, ctx):
        userId = ctx.message.author.id
        if haveFile(str(userId), "Users"):
            userData = readFromFile("Users/" + str(userId) + ".json")
            inv = userData["inventory"]
            invList = [f"{key} - {inv[key]}" for key in inv.keys()]
            invList.sort()
            lineBreak="\n"
            if not(inv):
                invList = ["Inventory is Empty!"]
            await ctx.channel.send(f"{ctx.message.author}'s inventory: \n{lineBreak.join(invList)}")
        else:
            await ctx.channel.send(f"{ctx.message.author}, you don't have a Bread Dog account yet. You can get one by typing `wurf setup`.")


"""
    @commands.command(
        help="Sell stuff from you're inventory",
        brief="Sell stuff for profit",
        aliases=["pawn"]
    )
    async def sell(self, ctx, item:str=None, amount:int=1):
"""


client.help_command = MyHelpCommand()
client.add_cog(Utility(client))
client.add_cog(Extra(client))
client.add_cog(Moderation(client))
client.add_cog(Economy(client))
client.run(TOKEN)
