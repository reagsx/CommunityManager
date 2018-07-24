import asyncio

import discord
from discord import channel
from discord.ext import commands


class grouping:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def groups(self, ctx, voice_channel_id):
        #First getting the voice channel object
        voice_channel = discord.utils.get(ctx.message.server.channels, id = voice_channel_id)
        if not voice_channel:
            return await self.bot.say("That is not a valid voice channel.")

        list_of_group_names = ['Defense','Flex 1','Flex 2']

        group_dict = {'group_list':[],}


        def build_group_helper(name, role_list):
            '''The function will add a name to group dictionary in the first group
               that matches a corresponding role.

               name (str): name of discord member
               role_list (list): list of roles
               '''

            for group in list_of_group_names:
                if group.lower() in role_list:
                    return group_dict[group].append(name)
            return group_dict['group_list'].append(name)


        def build_dict(group_names):
            for group in group_names:
                if group not in group_dict:
                    group_dict[group] = []


        def build_group_dict():
            build_dict(list_of_group_names)
            members = voice_channel.voice_members
            member_role_dict = {}

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
                    except Exception as e:
                        print('Out of Players')
                        break

        def pa_group():
            pa_list = []

            members = voice_channel.voice_members
            for m_role_check in members:
                member_role = m_role_check.roles
                if "pa" in [x.name.lower() for x in member_role]:
                    pa_list.append(m_role_check.display_name)

            half = len(pa_list)//2
            group_1 = pa_list[:half]
            group_2 = pa_list[half:]
            return "\n**Group 1: **" + ', '.join(group_1) +\
            "\n**Group 2: **" + ', '.join(group_2)

        def groups():
            build_group_dict()
            build_groups()
            return "\n\n".join("**{}:** {}".format(key,', '.join(value)) for (key,value) in group_dict.items())\
        + '\n\n__**PA Groups**__' + pa_group()


        embed = discord.Embed(title = "Group setup for all members in {}".format(voice_channel.name),
                              description = groups(),
                              color=discord.Color.blue())

        return await self.bot.say(embed = embed)

def setup(bot):
    bot.add_cog(grouping(bot))
