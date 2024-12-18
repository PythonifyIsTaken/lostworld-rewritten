import discord

am = discord.AllowedMentions.none()

async def ban(message):
    user_id = message.content.split()[1]
    reason = " ".join(message.content.split()[2:])
    if not "@" in user_id:
        user_id = int(user_id)
    else:
        user_id = int(user_id[2:-1])
    if not message.author.guild_permissions.ban_members:
        await message.channel.send('You do not have permission to ban members.')
    banned_user = message.guild.get_member(user_id)
    await banned_user.ban(delete_message_days=0, reason=str(reason))
    await message.channel.send(f'Banned <@{user_id}> for `{str(reason)}`.', allowed_mentions=am)


async def unban(message):
    if not message.author.guild_permissions.ban_members:
        await message.channel.send('You do not have permission to unban members.')
        return
    content = message.content.split()
    if len(content) < 2:
        await message.channel.send('Please provide a user ID or mention to unban.')
        return
    user_id = content[1]
    reason = ' '.join(content[2:]) if len(content) > 2 else 'No reason provided'
    if "@" in user_id:
        user_id = int(user_id[2:-1])
    else:
        user_id = int(user_id)
    banned_users = [entry async for entry in message.guild.bans()]

    user = next((ban_entry.user for ban_entry in banned_users if ban_entry.user.id == user_id), None)
    if user is None:
        await message.channel.send('<@{user_id}> is not banned.', allowed_mentions=am)
        return
    await message.guild.unban(user, reason=reason)
    await message.channel.send(f'Unbanned <@{user_id}>  for `{reason}`.', allowed_mentions=am)



async def add_role(message):
    user_id = message.content.split()[1]
    role_id = message.content.split()[2]

    if "@" in user_id:
        user_id = int(user_id[2:-1])
    else:
        user_id = int(user_id)

    if "@" in role_id:
        role_id = int(role_id[3:-1])
    else:
        role_id = int(role_id)

    if not message.author.guild_permissions.manage_roles:
        await message.channel.send('You do not have permission to add roles.')
        return

    role = message.guild.get_role(role_id)

    member = await message.guild.fetch_member(user_id)
    if role:
        await member.add_roles(role)
        await message.channel.send(f'Added role <@&{role_id}> to <@{user_id}>', allowed_mentions=am)
    else:
        await message.channel.send(f'Could not find a role with the id {role_id}.', allowed_mentions=am)

async def remove_role(message):
    user_id = message.content.split()[1]
    role_id = message.content.split()[2]

    if "@" in user_id:
        user_id = int(user_id[2:-1])
    else:
        user_id = int(user_id)

    if "@" in role_id:
        role_id = int(role_id[3:-1])
    else:
        role_id = int(role_id)

    if not message.author.guild_permissions.manage_roles:
        await message.channel.send('You do not have permission to remove roles.')
        return

    role = message.guild.get_role(role_id)

    member = await message.guild.fetch_member(user_id)
    if role:
        await member.remove_roles(role)
        await message.channel.send(f'Removed role <@&{role_id}> from <@{user_id}>.', allowed_mentions=am)
    else:
        await message.channel.send(f'Could not find a role with the id {role_id}.', allowed_mentions=am)
