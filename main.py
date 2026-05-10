from astrbot.api import AstrBotConfig
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp
import random
import httpx
import aiocqhttp
import json

@register("random_pic", "YUGANJUN114514", "从指定api获取随机图片", "1.0.0")
class RandomPicPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        print(self.config)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        logger.info("random_pic插件已被加载")

    @filter.command_group("图图配置")
    @filter.permission_type(filter.PermissionType.ADMIN)
    async def 图图配置(self, event: AstrMessageEvent):
        yield event.plain_result("请输入正确的指令格式:图图配置,最大数量,api")

    @filter.command_group("图图")
    async def 图图(self, event: AstrMessageEvent):
        apilist = self.config["api"]
        logger.info(f"已获取api列表:{apilist}")
        number = random.randint(0,len(self.config["api"])-1)
        logger.info(f"已生成随机数:{number}")
        api = apilist[number]
        if not api.startswith(("https://", "http://")):
            logger.info(f"api语法异常,正在尝试修正...")
            api = "https://" + api
        else:
            logger.info(f"api语法正常")
        logger.info(f"已随机获取api:{api}")
        #TODO 需要添加多种api的适配
        try:
            yield event.image_result(api)
        except aiocqhttp.exceptions.ActionFailed as e:
            logger.error(f"获取图片时发生错误: {e}")
            logger.info("正在尝试重定向...")
            try:
                r = httpx.get(api, follow_redirects=True)
                logger.info(f"已重定向到网址{r.url}")
                yield event.image_result(str(r.url))
            except Exception as e:
                logger.error(f"重定向失败: {e}")
                yield event.plain_result("抱歉，获取图片失败了呢~")

    @图图.command("指定")
    async def 指定(self, event:AstrMessageEvent, eapi: str):
        apilist = self.config["api"]
        logger.info(f"已获取api列表:{apilist}")
        index_eapi = apilist.index(eapi)
        logger.info(f"索引位置为{index_eapi}")
        api = apilist[index_eapi]
        if not api.startswith(("https://", "http://")):
            logger.info(f"api语法异常,正在尝试修正...")
            api = "https://" + api
        else:
            logger.info(f"api语法正常")
        logger.info(f"已获取api:{api}")
        #TODO 需要添加多种api的适配:)
        try:
            yield event.image_result(api)
        except aiocqhttp.exceptions.ActionFailed as e:
            logger.error(f"获取图片时发生错误: {e}")
            logger.info("正在尝试重定向...")
            r = httpx.get(api, follow_redirects=True)
            logger.info(f"已重定向到网址{r.url}")
            yield event.image_result(str(r.url))
        except Exception as e:
            logger.error(f"重定向失败: {e}")
            yield event.plain_result("抱歉，获取图片失败了呢~")

    @filter.command("多图图")
    async def 多图图(self, event:AstrMessageEvent, number: int, api: str = "manyacg.top/setu"):
        wh_list = self.config["wh_list"]
        logger.info(f"已获取白名单:{wh_list}")
        user_id = event.get_sender_id()
        maxnum = self.config["max_num"]
        logger.info(f"用户ID为{user_id}的用户正在尝试使用多图图命令")
        if user_id not in wh_list:
            yield event.plain_result("抱歉，您没有权限使用多图图命令哦~")
            return
        if number < 1:
            yield event.plain_result("一次获取的图片数量不能少于1张哦~")
            return
        if number > maxnum:
            yield event.plain_result(f"一次获取的图片数量不能超过{maxnum}张哦~")
            return
        apilist = self.config["api"]
        logger.info(f"已获取api列表:{apilist}")
        if api != "manyacg.top/setu":
            logger.info(f"已获取自定义api:{api}")
            index_api = apilist.index(api)
            logger.info(f"索引位置为{index_api}")
            api = apilist[index_api]
        if not api.startswith(("https://", "http://")):
            logger.info(f"api语法异常,正在尝试修正...")
            api = "https://" + api
        else:
            logger.info(f"api语法正常")
        logger.info(f"已获取api:{api}")
        logger.info(f"正在获取{number}张图片,api为{api}")
        for i in range(number):
            try:
                yield event.image_result(api)
                yield event.plain_result(f"已获取第{i+1}张图片")
                if i == number - 1:
                    yield event.plain_result("获取图片完成")
            except aiocqhttp.exceptions.ActionFailed as e:
                logger.error(f"获取图片时发生错误: {e}")
                logger.info("正在尝试重定向...")
                r = httpx.get(api, follow_redirects=True)
                logger.info(f"已重定向到网址{r.url}")
                yield event.image_result(str(r.url))
            except Exception as e:
                logger.error(f"重定向失败: {e}")
                yield event.plain_result("抱歉，获取图片失败了呢~")
                return
            
    @图图配置.command("白名单")
    async def 白名单(self, event:AstrMessageEvent, mode: str = None, user_id: str = None):
        wh_list = self.config["wh_list"]
        logger.info(f"已获取白名单:{wh_list}")
        if mode == "list":
            yield event.plain_result(f"当前白名单用户ID列表为:{wh_list}")
        elif mode == "add":
            if str(user_id) not in wh_list:
                wh_list.append(str(user_id))
                self.config["wh_list"] = wh_list
                self.config.save_config()
                yield event.plain_result(f"已将用户ID{user_id}添加至白名单")

            else:
                yield event.plain_result(f"用户ID:{user_id}已在白名单中")
        elif mode == "remove":
            if str(user_id) in wh_list:
                wh_list.remove(str(user_id))
                self.config["wh_list"] = wh_list
                self.config.save_config()
                yield event.plain_result(f"已将用户ID:{user_id}从白名单中移除")

            else:
                yield event.plain_result(f"用户ID:{user_id}不在白名单中")       
        elif mode == "help":
            yield event.plain_result("白名单指令格式:\n图图配置 白名单 add 用户ID\n图图配置 白名单 remove 用户ID\n图图配置 白名单 list")     
        else:
            yield event.plain_result("无效的模式,请使用add、remove,list或help")

    @图图配置.command("最大数量")
    async def 最大数量(self, event:AstrMessageEvent, number: int = None):
        if number < 1:
            yield event.plain_result("每次获取的最大图片数量不能少于1张哦~")
            return
        self.config["max_num"] = number
        self.config.save_config()
        yield event.plain_result(f"已将每次获取的最大图片数量设置为{number}张")


    @图图配置.command("api")
    async def api(self, event:AstrMessageEvent, mode: str = None, api:str = None):
        if mode == "add":
            if api not in self.config["api"]:
                self.config["api"].append(api)
                self.config.save_config()
                yield event.plain_result(f"已添加api:{api}")

            else:
                yield event.plain_result(f"api:{api}已在列表中")
        elif mode == "remove":
            if api in self.config["api"]:
                self.config["api"].remove(api)
                self.config.save_config()
                yield event.plain_result(f"已移除api{api}")

            else:
                yield event.plain_result(f"api:{api}不在列表中")
        elif mode == "list":
            yield event.plain_result(f"当前api列表为:{self.config['api']}")
        elif mode == "help":
            yield event.plain_result("api指令格式:\n图图配置 api add api地址\n图图配置 api remove api地址\n图图配置 api list")
        else:
            yield event.plain_result("无效的模式,请使用add、remove、list或help")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        logger.info("random_pic插件已被卸载")
