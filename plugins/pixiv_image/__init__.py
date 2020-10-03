# coding=utf-8
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from jieba import posseg
import apscheduler, nonebot,os
from .source import mkdir, add_order, pic_send,pic_order_update_all, delete, pic_reload,IMAGE_PATH,IMAGR_DATA_PATH,ARTIST_DATA_PATH,listdir

mkdir(IMAGE_PATH)
mkdir(ARTIST_DATA_PATH)
mkdir(IMAGR_DATA_PATH)
cwd=os.getcwd()


@on_natural_language(keywords={'涩图', "色图", "纸片人"}, only_to_me=False)
@on_command('wallpaper_send_one', aliases=('色图', '涩图', '纸片人'))
async def _(session: CommandSession):
    msg, file_list, pic_num_remain = await pic_send(1)
    await session.send(msg)
    delete(file_list)
    if pic_num_remain < 10:
        pic_reload()

@on_natural_language(keywords={'色图三连', "涩图三连"}, only_to_me=False)
@on_command('wallpaper_send_three', aliases=('色图三连', '涩图三连'))
async def _(session: CommandSession):
    msg, file_list, pic_num_remain = await pic_send(3)
    await session.send(msg)
    delete(file_list)
    if pic_num_remain < 6:
        pic_reload()


@nonebot.scheduler.scheduled_job('cron', hour='2', minute="0")
async def _():
    await pic_order_update_all()

@on_command('wallpaper_send_all', aliases=('色图齐射', '涩图齐射'))
async def _(session: CommandSession):
    msg, file_list, pic_num_remain = await pic_send(6)
    await session.send(msg)
    delete(file_list)
    if pic_num_remain < 6:
        pic_reload()


@on_command("wallpaper_update", aliases=('更新图库'))
async def _(session: CommandSession):
    await pic_order_update_all()
    await session.send("更新成功")

@on_command("wallpaper_addorder", aliases=('添加订阅'))
async def _(session: CommandSession):
    artistsID=session.get("artistsID",prompt="请您给出要订阅的作者ID")
    await add_order(artistsID)
    await session.send("添加成功")

@on_command("wallpaper_reload", aliases=('重新装填'))
async def _(session: CommandSession):
    try:
        delete(listdir(IMAGE_PATH))
        await pic_reload()
        await session.send("装填成功")
    except:
        await session.send("装填失败")

@on_command("wallpaper_help", aliases=('帮助'))
async def _(session: CommandSession):
    msg="""
    [命令]:[效果]
    色图,涩图,纸片人:发送1张图片
    涩图三连,色图三连:发送3张图片
    添加订阅 [作者ID]:添加图片作者订阅
    重新装填:手动补充图片
    更新图库:更新作者图片信息
    """
    await session.send(msg)


