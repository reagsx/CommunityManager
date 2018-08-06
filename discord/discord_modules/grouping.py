import asyncio
import json
import discord
from discord import channel
from discord.ext import commands

class grouping:
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role('Officer')
    @commands.command(pass_context = True)
    async def groups(self, ctx, pa_groups: int = 2):
        #Load Group Names from JSON and convert into a list
        with open("/home/chris/Community_Manager/settings/discord_settings.json") as cfg:
            settings = json.load(cfg)

        if pa_groups > 10:
            return await self.bot.say("Try a number less than 10 for PA groups.")

        pa_list = []

        groups        = settings["settings"]["groups"]
        list_of_group_names = [x for x in groups.split(",")]

        group_dict = {'group_list':[],}
        member_role_dict = {}
        pa_groups_dict = {}

        def get_channels():
            ''' Searches for all Voice Channels in server and returns a list of voice channels'''
            voice_channel_list = []
            for server in self.bot.servers:
                for channel in server.channels:
                    if channel.type == discord.ChannelType.voice:
                        if channel.name != 'AFK':
                            voice_channel_list.append(channel)
            return voice_channel_list

        def build_group_helper(name, role_list):
            '''The function will add a name to group dictionary in the first group
               that matches a corresponding role.

               name (str): name of discord member
               role_list (list): list of roles
               '''
            if "member" in role_list:
                if "pa" in role_list:
                    pa_list.append(name)
                for group in list_of_group_names:
                    if group.lower() in role_list:
                        return group_dict[group].append(name)
                return group_dict['group_list'].append(name)

        def build_dict(group_names):
            for group in group_names:
                if group not in group_dict:
                    group_dict[group] = []

        def build_group_dict(channel_list):
            build_dict(list_of_group_names)
            for channel in channel_list:
                members = channel.voice_members
                for member in members:
                    member_role_dict[member.display_name] = [x.name.lower() for x in member.roles]
            for key in member_role_dict:
                build_group_helper(key, member_role_dict.get(key))


        def build_groups():
            players = group_dict.pop('group_list')
            total_players = len(players)
            number_of_groups = (total_players//5) + 1

            print("Total Groups: " + str(number_of_groups))

            for group_number in range(number_of_groups):
                group_dict['Group ' + str(group_number+1)] = []
                for x in range(5):
                    try:
                        group_dict['Group ' + str(group_number+1)].append(players.pop())
                    except Exception:
                        print('Out of Players')
                        break

        def pa_group():
            for i in range(pa_groups):
                pa_groups_dict['PA Group ' + str(i+1)] = []

            while len(pa_list) > 0:
                for x in range(pa_groups):
                    if len(pa_list) > 0:
                        pa_groups_dict['PA Group ' + str(x+1)].append(pa_list.pop())


        def format_groups():
            build_group_dict(get_channels())
            build_groups()
            pa_group()
            return "\n\n".join("**{}:** {}".format(key,', '.join(value)) for (key,value) in group_dict.items())\
            + '\n\n\n\n__**PA Groups**__\n\n' + "\n\n".join("**{}:** {}".format(key, ', '.join(value)) for (key,value) in pa_groups_dict.items())
            


        embed = discord.Embed(title = "Group setup for all members in Discord",
                              description = format_groups(),
                              color=discord.Color.blue())

        return await self.bot.say(embed = embed)

def setup(bot):
    bot.add_cog(grouping(bot))
