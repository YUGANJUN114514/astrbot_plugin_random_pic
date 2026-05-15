from astrbot.api import AstrBotConfig
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import random
import httpx
import json

@register("random_pic", "YUGANJUN114514", "从指定api获取随机图片", "1.0.0")
class RandomPicPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        """插件异步初始化方法"""
        logger.info("random_pic插件已加载")

    def _ensure_https(self, api: str) -> str:
        """确保API地址以https://或http://开头"""
        if not api.startswith(("https://", "http://")):
            logger.info(f"API地址格式异常，正在尝试修正: {api}")
            return "https://" + api
        return api

    def _parse_image_url(self, rejson: dict) -> str:
        """从API返回的JSON字典中解析图片URL"""
        # 尝试常见的图片API返回格式
        try:
            return rejson["data"][0]["url"]
        except (KeyError, TypeError, IndexError):
            pass
        try:
            return rejson["data"][0]["urls"]
        except (KeyError, TypeError, IndexError):
            pass
        try:
            return rejson["data"]["link"]
        except (KeyError, TypeError, IndexError):
            pass
        raise KeyError("无法匹配已知的图片地址格式")

    async def _fetch_and_send_image(self, event: AstrMessageEvent, api: str):
        """请求API并发送图片，处理各种异常与重定向"""
        api = self._ensure_https(api)
        logger.info(f"正在请求API: {api}")
        
        try:
            response = httpx.get(api, timeout=10.0)
            strjson = response.text
            
            # 安全替换JSON中的布尔值，避免影响字符串内容
            strjson = strjson.replace(": true", ": True").replace(":false", ":False")
            rejson = json.loads(strjson)
            
            logger.info(f"API返回数据为字典: {rejson}")
            url = self._parse_image_url(rejson)
            logger.info(f"成功解析图片地址: {url}")
            yield event.image_result(url)
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"JSON解析或图片地址提取失败: {e}，尝试直接作为图片链接发送")
            try:
                yield event.image_result(api)
            except Exception:
                logger.warning("直接发送失败，尝试跟随重定向获取真实图片地址")
                try:
                    r = httpx.get(api, follow_redirects=True, timeout=10.0)
                    logger.info(f"已重定向到网址: {r.url}")
                    yield event.image_result(str(r.url))
                except Exception as redirect_err:
                    logger.error(f"图片获取最终失败: {redirect_err}")
                    yield event.plain_result("图片获取失败")
        except Exception as e:
            logger.error(f"请求API时发生未知错误: {e}")
            yield event.plain_result("图片获取失败")

    @filter.command_group("图图配置")
    @filter.permission_type(filter.PermissionType.ADMIN)
    async def 图图配置(self, event: AstrMessageEvent):
        """配置指令入口"""
        yield event.plain_result("请输入正确的指令格式: 图图配置 最大数量/api/白名单")

    @filter.command("图图")
    async def 图图(self, event: AstrMessageEvent):     
        """随机从API列表中获取一张图片"""
        apilist = self.config["api"]
        apidict = apilist[0]
        apiname = random.choice(list(apidict.keys()))
        api = apidict[apiname]
        
        logger.info(f"已随机选取API [{apiname}]: {api}")
        async for result in self._fetch_and_send_image(event, api):
            yield result

    @filter.command_group("图图测试")
    async def 图图测试(self, event: AstrMessageEvent):
        """测试指令入口"""
        yield event.plain_result("请输入正确的指令格式: 图图测试 指定 api名称")

    @图图测试.command("指定")
    async def 指定(self, event: AstrMessageEvent, eapi: str = None):
        """测试指定的API"""
        apilist = self.config["api"]
        apidict = apilist[0]
        
        if eapi not in apidict:
            yield event.plain_result(f"无法获取指定api名称 {eapi} 所对应的api")
            return
            
        api = apidict[eapi]
        logger.info(f"已指定API [{eapi}]: {api}")
        async for result in self._fetch_and_send_image(event, api):
            yield result

    @filter.command("多图图")
    async def 多图图(self, event: AstrMessageEvent, number: int, eapi: str = "manyacg"):
        """一次获取多张图片，需白名单权限"""
        wh_list = self.config["wh_list"]
        user_id = event.get_sender_id()
        maxnum = self.config["max_num"]
        
        logger.info(f"用户 {user_id} 正在尝试使用多图图命令")
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
        apidict = apilist[0]
        if eapi not in apidict:
            yield event.plain_result(f"无法获取指定api名称 {eapi} 所对应的api")
            return
            
        api = apidict[eapi]
        logger.info(f"正在获取{number}张图片，API: {api}")
        
        for _ in range(number):
            async for result in self._fetch_and_send_image(event, api):
                yield result
            
    @图图配置.command("白名单")
    async def 白名单(self, event: AstrMessageEvent, mode: str = None, user_id: str = None):
        """管理多图图命令的白名单"""
        wh_list = self.config["wh_list"]
        if mode == "list":
            yield event.plain_result(f"当前白名单用户ID列表为: {wh_list}")
        elif mode == "add":
            if user_id:
                if str(user_id) not in wh_list:
                    wh_list.append(str(user_id))
                    self.config["wh_list"] = wh_list
                    self.config.save_config()
                    logger.info(f"已将用户ID {user_id} 添加至白名单")
                    yield event.plain_result(f"已将用户ID {user_id} 添加至白名单")
                else:
                    yield event.plain_result(f"用户ID: {user_id} 已在白名单中")
            else:
                yield event.plain_result("请输入用户ID")
        elif mode == "remove":
            if user_id:
                if str(user_id) in wh_list:
                    wh_list.remove(str(user_id))
                    self.config["wh_list"] = wh_list
                    self.config.save_config()
                    logger.info(f"已将用户ID {user_id} 从白名单中移除")
                    yield event.plain_result(f"已将用户ID {user_id} 从白名单中移除")
                else:
                    yield event.plain_result(f"用户ID: {user_id} 不在白名单中")       
            else:
                yield event.plain_result("请输入用户ID")
        elif mode == "help":
            yield event.plain_result("白名单指令格式:\n图图配置 白名单 add 用户ID\n图图配置 白名单 remove 用户ID\n图图配置 白名单 list")     
        else:
            yield event.plain_result("无效的模式，请使用add、remove、list或help")

    @图图配置.command("最大数量")
    async def 最大数量(self, event: AstrMessageEvent, number: int = None):
        """设置多图图最大获取数量"""
        if number is None or number < 1:
            yield event.plain_result("每次获取的最大图片数量不能少于1张哦~")
            return
        self.config["max_num"] = number
        self.config.save_config()
        logger.info(f"已将最大图片数量设置为 {number}")
        yield event.plain_result(f"已将每次获取的最大图片数量设置为{number}张")

    @图图配置.command("api")
    async def api(self, event: AstrMessageEvent, mode: str = None, apiname: str = None, api: str = None):
        """管理随机图片API列表"""
        if mode == "add":
            if apiname and api:
                if apiname not in self.config["api"][0]:
                    self.config["api"][0][apiname] = api
                    self.config.save_config()
                    logger.info(f"已添加api: {api}, 名称: {apiname}")
                    yield event.plain_result(f"已添加api: {api}, 名称: {apiname}")
                else:
                    yield event.plain_result(f"api名称: {apiname} 已在列表中")
            else:
                yield event.plain_result("请输入api名称和api地址")
        elif mode == "remove":
            if apiname:
                if apiname in self.config["api"][0]:
                    del self.config["api"][0][apiname]
                    self.config.save_config()
                    logger.info(f"已移除api名称: {apiname}")
                    yield event.plain_result(f"已移除api名称: {apiname}")
                else:
                    yield event.plain_result(f"api名称: {apiname} 不在列表中，请使用list查看api字典")
            else:
                yield event.plain_result("请输入api名称")
        elif mode == "list":
            yield event.plain_result(f"当前api字典为: {self.config['api']}")
        elif mode == "help":
            yield event.plain_result("api指令格式:\n图图配置 api add api名称 api\n图图配置 api remove api名称\n图图配置 api list")
        else:
            yield event.plain_result("无效的模式，请使用add、remove、list或help")

    async def terminate(self):
        """插件销毁方法"""
        logger.info("random_pic插件已被卸载")
