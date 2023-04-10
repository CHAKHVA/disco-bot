import discord
from discord.ext import commands
from discord.utils import get
import os
import pafy

import sys
sys.path.append('.')

from extra.helper import Helper


FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class Disco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def volume(self, ctx, volume: int):
        '''Changes the player's volume'''

        if ctx.voice_client is None:
            return await ctx.send('Not connected to a voice channel.')

        ctx.voice_client.source.volume = volume / 100
        await ctx.send('Changed volume to {}%'.format(volume))
    
    @commands.command()
    async def join(self, ctx, *, channel_name=None):
        channel = get(ctx.guild.voice_channels, name=channel_name)
        print(channel)
        if channel and channel_name:
            voice_channel = channel
        elif not channel and channel_name:
            return await ctx.send("There is no voice channel with given name")
        else:
            if not ctx.author.voice:
                return await ctx.send("You aren't in a voice channel and channel name is not given")
            else:
                voice_channel = ctx.author.voice.channel
        print(voice_channel)
        if ctx.voice_client:
            await ctx.voice_client.move_to(voice_channel)
        else:
            await voice_channel.connect()

        await ctx.send(f'Joined {voice_channel}')
    
    @commands.command(aliases=['disconnect'])
    async def leave(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        print(voice)
        print(voice.is_connected())
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f'The bot has left {voice.channel}')
        else:
            await ctx.send("Don't think I am in a voice channel")

    @commands.command()
    async def play(self, ctx, *, url):
        if not Helper.validate(url):
            url = Helper.get_url(url)
            audio = pafy.new(url)
            best = audio.getbestaudio()
            url = best.url
            
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(source=url, executable=os.path.join('..', 'ffmpeg', 'ffmpeg'), **FFMPEG_OPTS))
        print('End1')
        voice.source = discord.PCMVolumeTransformer(voice.source)
        print('End2')
        voice.source.volume = 0.07
        print('End3')
    
    @commands.command()
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print('Music paused')
            voice.pause()
            await ctx.send('Music paused')
        else:
            print('Music not playing failed pause')
            await ctx.send('Music not playing failed pause')

    @commands.command()
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print('Resumed music')
            voice.resume()
            await ctx.send('Resumed music')
        else:
            print('Music is not paused')
            await ctx.send('Music is not paused')
    
    @commands.command()
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print('Music stopped')
            voice.stop()
            await ctx.send('Music stopped')
        else:
            print('No music playing failed to stop')
            await ctx.send('No music playing failed to stop')

async def setup(bot):
    await bot.add_cog(Disco(bot))