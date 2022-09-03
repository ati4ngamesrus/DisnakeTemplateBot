import disnake as discord
from disnake.ext import commands

token = "YOUR BOT TOKEN" 
bot = commands.Bot(command_prefix='/') 
bot.remove_command('help') 


@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="slash commands"))
	print('Bot is working!')


@bot.slash_command(description="Clear up to 1000 messages")
async def clear( ctx, amount:int = None):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.message.add_reaction("<:NO:934789609932611594>")
        Embed = discord.Embed(title='<:NO:934789609932611594>|Error!', description = 'You do not have the required rights :(', color=discord.Color.red())
        await ctx.response.send_message(embed = Embed)
        return
    if not amount:
        Embed = discord.Embed(title='<:NO:934789609932611594>|Error!', description = 'No number of messages specified :(', color=0x30d5c8)
        await ctx.response.send_message(embed = Embed)
        return
    if amount<1 or amount > 1000:
        Embed = discord.Embed(title='<:NO:934789609932611594>|Error!', description ='Maximum 1000,Minimum 1', color=discord.Color.red())
        await ctx.response.send_message(embed=Embed)
        return
    else:
        x = await ctx.channel.purge(limit=amount)
        Embed = discord.Embed(title='Cleared', description =f'Cleared {len(x)} messages from {amount} specified,enjoy :)', color=discord.Color.green())
        await ctx.response.send_message(embed=Embed)


@bot.slash_command(description="Play pop it, why not?")
async def popit(ctx):
 		cpage = discord.Embed(
 			title = 'Pop-it!',
 			description = f'''
 ||:red_square:||||:red_square:||||:red_square:||||:red_square:||||:red_square:||||:red_square:||
 ||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||
 ||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||
 ||:green_square:||||:green_square:||||:green_square:||||:green_square:||||:green_square:||||:green_square:||
 ||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||
 ||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||''', 
		color=discord.Color.blue()
 	)
 	await ctx.send(embed=cpage)
 	

@bot.slash_command(description="Say text")
async def echo(ctx, message=None):
    await ctx.send(message)

@bot.slash_command(description="Run code in Python environment. Only available to the bot developer")
async def eval(ctx, *, code):
    if ctx.author.id in [PASTE YOUR ID HERE]:
        pending_embed = discord.Embed(title = 'Hello! 👋', description = 'Code executing, please wait.....', color = discord.Colour.from_rgb(255, 255, 0))
        message = await ctx.send(embed = pending_embed)
        success_embed = discord.Embed(title = 'Succes! 🐍', color = discord.Colour.from_rgb(0, 255, 0))
        code = clean_code(code)
        local_variables = {
            "discord": discord,
            "cache": cache,
            "db": db,
            "commands": commands,
            "client": bot,
            "bot": bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }
        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )
                obj = await local_variables["func"]()
                result = stdout.getvalue()
                success_embed.add_field(name = 'Executed code:', value = f'```py\n{code}\n```', inline = False)
                what_returned = None
                if obj != None:
                    if isinstance(obj, int) == True:
                        if obj == True:
                            what_returned = 'Boolean value'
                        elif obj == False:
                            what_returned = 'Boolean value'
                        else:
                            what_returned = 'Integer'
                    elif isinstance(obj, str) == True:
                        what_returned = 'Line'
                    elif isinstance(obj, float) == True:
                        what_returned = 'Fractional number'
                    elif isinstance(obj, list) == True:
                        what_returned = 'List'
                    elif isinstance(obj, tuple) == True:
                        what_returned = 'Immutable list'
                    elif isinstance(obj, set) == True:
                        what_returned = 'Unique list'
                    else:
                        what_returned = 'Unrecognized data type....'
                    success_embed.add_field(name = 'Data type:', value = f'```\n{what_returned}\n```', inline = False)
                    success_embed.add_field(name = 'Returned:', value = f'```\n{obj}\n```', inline = False)
                else:
                    pass
                if result:
                    success_embed.add_field(name = 'Execution result:', value = f'```py\nConsole:\n\n{result}\n```', inline = False)
                else:
                    pass
                await message.edit(embed = success_embed)
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))
            fail_embed = discord.Embed(title = 'Error!', color = discord.Colour.from_rgb(255, 0, 0))
            fail_embed.add_field(name = 'Executed code:', value = f'```py\n{code}\n```', inline = False)
            fail_embed.add_field(name = 'Error:', value = f'```py\n{e}\n```', inline = False)
    else:
        fail_embed = discord.Embed(title = 'Error!', color = discord.Colour.from_rgb(255, 0, 0))
        fail_embed.add_field(name = 'Execute code:', value = f'```py\nThe code is hidden for security purposes\n```', inline = False)
        fail_embed.add_field(name = 'Error:', value = f'```\nYou must have the following permissions to run this command:Bot developer\n```', inline = False)

bot.run(token)	
