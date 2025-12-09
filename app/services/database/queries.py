from app.services.database.models.guild import Guild
from app.services.database.models.guild_settings import GuildSettings
from app.services.database.models.mod_logs import ModLogs
from app.services.database.models.feature_settings import FeatureSettings


async def get_or_create_guild(guild_id: int, name: str) -> Guild:
    guild, created = await Guild.get_or_create(
        guild_id=str(guild_id), defaults={"name": name}
    )

    await GuildSettings.get_or_create(guild=guild)
    await FeatureSettings.get_or_create(guild=guild)

    if guild.name != name:
        guild.name = name
        await guild.save()

    return guild


async def delete_guild_data(guild_id: int) -> None:
    await Guild.filter(guild_id=str(guild_id)).delete()


async def fetch_prefix(guild_id: int) -> str:
    settings = await GuildSettings.get(guild_id=str(guild_id))
    return settings.prefix


async def set_prefix(guild_id: int, new_prefix: str) -> None:
    settings = await GuildSettings.get(guild_id=str(guild_id))
    settings.prefix = new_prefix
    await settings.save()


async def insert_modlog(
    guild_id: int, target_id: int, mod_id: int, action: str, reason: str
) -> int:
    guild = await Guild.get(guild_id=str(guild_id))

    log = await ModLogs.create(
        guild=guild,
        target_id=str(target_id),
        mod_id=str(mod_id),
        action=action,
        reason=reason,
    )
    case_id = log.case_id
    return case_id


async def get_modlog_channel(guild_id: int) -> int:
    settings = await GuildSettings.get(guild_id=str(guild_id))
    return settings.modlog_channelid


async def set_modlog_channel(guild_id: int, channel_id: int) -> None:
    settings = await GuildSettings.get(guild_id=str(guild_id))
    settings.modlog_channelid = str(channel_id)
    await settings.save()


async def get_suggestion_channel(guild_id: int) -> int:
    settings = await GuildSettings.get(guild_id=str(guild_id))
    return settings.suggestion_channelid


async def set_suggestion_channel(guild_id: int, channel_id: int) -> None:
    settings = await GuildSettings.get(guild_id=str(guild_id))
    settings.suggestion_channelid = str(channel_id)
    await settings.save()


async def fetch_modlogs(guild_id: int, user_id: int) -> list:
    logs = await ModLogs.filter(
        guild_id=str(guild_id), target_id=str(user_id)
    ).order_by("case_id")
    results = []
    for log in logs:
        results.append(
            {
                "id": log.case_id,
                "guild_id": log.guild_id,
                "user_id": log.target_id,
                "moderator": log.mod_id,
                "action": log.action,
                "reason": log.reason,
                "date": log.timestamp.isoformat(),
                "resolved": log.resolved,
            }
        )
    return results


async def edit_modlogs(case_id: int, new_reason: str) -> None:
    log = await ModLogs.get(case_id=case_id)
    log.reason = new_reason
    await log.save()


async def delete_modlogs(case_id: int) -> None:
    log = await ModLogs.get(case_id=case_id)
    await log.delete()


async def fetch_warnings(guild_id: int, user_id: int) -> list:
    logs = await ModLogs.filter(
        guild_id=str(guild_id), target_id=str(user_id), action="warn"
    ).order_by("case_id")
    results = []
    for log in logs:
        results.append(
            {
                "id": log.case_id,
                "guild_id": log.guild_id,
                "user_id": log.target_id,
                "moderator": log.mod_id,
                "action": log.action,
                "reason": log.reason,
                "date": log.timestamp.isoformat(),
            }
        )
    return results


async def get_appeal_channel(guild_id: int):
    settings = await GuildSettings.get(guild_id=str(guild_id))
    return settings.appeal_channelid


async def set_appeal_channel(guild_id: int, channel_id: int):
    settings = await GuildSettings.get(guild_id=str(guild_id))
    settings.appeal_channelid = str(channel_id)
    await settings.save()


async def resolve_case(case_id: int):
    logs = await ModLogs.get(case_id=case_id)
    logs.resolved = True
    await logs.save()
