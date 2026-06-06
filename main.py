import time

import httpx

import astrbot.api.message_components as Comp
from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.message_components import Image, Node
from astrbot.api.star import Context, Star, register

api = "https://manyacg.top/setu"
r18_api = "https://manyacg.top/sese"


class ImageError(Exception):
    pass


@register("random_pic", "YUGANJUN114514", "从指定api获取随机图片", "1.0.0")
class RandomPicPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        logger.info("random_pic插件已被加载")

    @filter.command_group("图图配置")
    @filter.permission_type(filter.PermissionType.ADMIN)
    async def 图图配置(self, event: AstrMessageEvent):
        """插件配置入口"""
        pass

    @filter.command("图图", alias={"tutu", "pic"})
    async def 图图(self, event: AstrMessageEvent, cr18: str = None):
        """获取单张图片"""
        R18_gr_mode = self.config["R18_gr_mode"]
        R18mode = self.config["R18"]
        logger.info(f"全局R18模式为{R18mode}")
        if cr18 != None:
            if (
                cr18 == "r18:on"
                or cr18 == "r18：on"
                or cr18 == "on"
                or cr18 == "R18:on"
                or cr18 == "R18：on"
                or cr18 == "ON"
            ):
                cr18 = True
            elif (
                cr18 == "r18:off"
                or cr18 == "r18：off"
                or cr18 == "off"
                or cr18 == "R18:off"
                or cr18 == "R18：off"
                or cr18 == "OFF"
            ):
                cr18 = False
            else:
                yield event.plain_result(
                    "无效的cr18参数喵!将按照off处理喵,请使用on或off"
                )
                cr18 = False
        else:
            cr18 = R18mode
        if R18mode == False:
            if cr18 == True:
                yield event.plain_result("当前全局R18模式为关闭状态喵")
            for i in range(1, 4):
                try:
                    r = await httpx.AsyncClient().get(api, follow_redirects=True)
                    if await self.get_kv_data(str(r.url), default=None) == None:
                        await self.put_kv_data(str(r.url), "")
                        logger.info(f"已将图片{r.url}添加至已请求列表")
                        yield event.image_result(str(r.url))
                        break
                    else:
                        logger.info("获取到重复图片")
                        raise ImageError("获取到重复图片")
                except Exception as e:
                    logger.warning(f"获取图片失败,错误信息为{e},正在进行第{i}次重试")
                    if i == 3:
                        logger.error(f"获取图片失败:{e}")
                        yield event.plain_result(f"获取图片失败喵:(\n{e}")
        else:
            if len(R18_gr_mode) == 0 and cr18 == True:
                logger.info("未设置群组r18模式,按照True处理")
                for i in range(1, 4):
                    try:
                        r = await httpx.AsyncClient().get(
                            r18_api, follow_redirects=True
                        )
                        if await self.get_kv_data(str(r.url), default=None) == None:
                            await self.put_kv_data(str(r.url), "")
                            logger.info(f"已将图片{r.url}添加至已请求列表")
                            yield event.image_result(str(r.url))
                            break
                        else:
                            logger.info("获取到重复图片")
                            raise ImageError("获取到重复图片")
                    except Exception as e:
                        logger.warning(
                            f"获取图片失败,错误信息为{e},正在进行第{i}次重试"
                        )
                        if i == 3:
                            logger.error(f"获取图片失败:{e}")
                            yield event.plain_result(f"获取图片失败喵:(\n{e}")
            elif len(R18_gr_mode) == 0 and cr18 == False:
                logger.info("未设置群组r18模式,但用户选择False,按照False处理")
                for i in range(1, 4):
                    try:
                        r = await httpx.AsyncClient().get(api, follow_redirects=True)
                        if await self.get_kv_data(str(r.url), default=None) == None:
                            await self.put_kv_data(str(r.url), "")
                            logger.info(f"已将图片{r.url}添加至已请求列表")
                            yield event.image_result(str(r.url))
                            break
                        else:
                            logger.info("获取到重复图片")
                            raise ImageError("获取到重复图片")
                    except Exception as e:
                        logger.warning(
                            f"获取图片失败,错误信息为{e},正在进行第{i}次重试"
                        )
                        if i == 3:
                            logger.error(f"获取图片失败:{e}")
                            yield event.plain_result(f"获取图片失败喵:(\n{e}")
            elif R18_gr_mode and cr18 == True:
                if event.get_group_id() in R18_gr_mode and cr18 == True:
                    logger.info(f"群{event.get_group_id()}的R18模式为True")
                    for i in range(1, 4):
                        try:
                            r = await httpx.AsyncClient().get(
                                r18_api, follow_redirects=True
                            )
                            if await self.get_kv_data(str(r.url), default=None) == None:
                                await self.put_kv_data(str(r.url), "")
                                logger.info(f"已将图片{r.url}添加至已请求列表")
                                yield event.image_result(str(r.url))
                                break
                            else:
                                logger.info("获取到重复图片")
                                raise ImageError("获取到重复图片")
                        except Exception as e:
                            logger.warning(
                                f"获取图片失败,错误信息为{e},正在进行第{i}次重试"
                            )
                            if i == 3:
                                logger.error(f"获取图片失败:{e}")
                                yield event.plain_result(f"获取图片失败喵:(\n{e}")
                elif event.get_group_id() in R18_gr_mode and cr18 == False:
                    logger.info(
                        f"群{event.get_group_id()}的R18模式为True,但用户选择False,按照False处理"
                    )
                    for i in range(1, 4):
                        try:
                            r = await httpx.AsyncClient().get(
                                api, follow_redirects=True
                            )
                            if await self.get_kv_data(str(r.url), default=None) == None:
                                await self.put_kv_data(str(r.url), "")
                                logger.info(f"已将图片{r.url}添加至已请求列表")
                                yield event.image_result(str(r.url))
                                break
                            else:
                                logger.info("获取到重复图片")
                                raise ImageError("获取到重复图片")
                        except Exception as e:
                            logger.warning(
                                f"获取图片失败,错误信息为{e},正在进行第{i}次重试"
                            )
                            if i == 3:
                                logger.error(f"获取图片失败:{e}")
                                yield event.plain_result(f"获取图片失败喵:(\n{e}")
                elif event.get_group_id() not in R18_gr_mode and cr18 == False:
                    if cr18 == True:
                        yield event.plain_result(
                            "当前群组r18模式为False喵!将使用False模式获取图片喵"
                        )
                    logger.info(f"群{event.get_group_id()}的R18模式为False")
                    for i in range(1, 4):
                        try:
                            r = await httpx.AsyncClient().get(
                                api, follow_redirects=True
                            )
                            if await self.get_kv_data(str(r.url), default=None) == None:
                                await self.put_kv_data(str(r.url), "")
                                logger.info(f"已将图片{r.url}添加至已请求列表")
                                yield event.image_result(str(r.url))
                                break
                            else:
                                logger.info("获取到重复图片")
                                raise ImageError("获取到重复图片")
                        except Exception as e:
                            logger.warning(
                                f"获取图片失败,错误信息为{e},正在进行第{i}次重试"
                            )
                            if i == 3:
                                logger.error(f"获取图片失败:{e}")
                                yield event.plain_result(f"获取图片失败喵:(\n{e}")

    @filter.command("多图图", alias={"duotutu", "manypic"})
    async def 多图图(self, event: AstrMessageEvent, number: int, cr18: str = None):
        """获取多张图片"""
        wh_list = self.config["wh_list"]
        logger.info(f"已获取白名单:{wh_list}")
        user_id = event.get_sender_id()
        maxnum = self.config["max_num"]
        R18_gr_mode = self.config["R18_gr_mode"]
        many_gr_list = self.config["many_gr_list"]
        R18mode = self.config["R18"]
        err = 0
        warn = 0
        urls = []
        logger.info(f"用户ID为{user_id}的用户正在尝试使用多图图命令")
        if cr18 != None:
            if (
                cr18 == "r18:on"
                or cr18 == "r18：on"
                or cr18 == "on"
                or cr18 == "R18:on"
                or cr18 == "R18：on"
                or cr18 == "ON"
            ):
                cr18 = True
                logger.info(f"用户ID为{user_id}的用户在多图图命令中临时开启了R18模式")
            elif (
                cr18 == "r18:off"
                or cr18 == "r18：off"
                or cr18 == "off"
                or cr18 == "R18:off"
                or cr18 == "R18：off"
                or cr18 == "OFF"
            ):
                cr18 = False
                logger.info(f"用户ID为{user_id}的用户在多图图命令中临时关闭了R18模式")
            else:
                yield event.plain_result(
                    "无效的cr18参数喵!将按照off处理喵,请使用on或off"
                )
                cr18 = False
        else:
            cr18 = R18mode
        if wh_list:
            if user_id not in wh_list:
                yield event.plain_result("抱歉,您没有权限使用多图图命令喵")
                logger.info(f"用户ID为{user_id}的用户没有权限使用多图图命令")
                return
        if many_gr_list:
            if str(event.get_group_id()) not in many_gr_list:
                yield event.plain_result("抱歉,当前群组没有权限使用多图图命令喵")
                return
        if number < 1:
            yield event.plain_result("一次获取的图片数量不能少于1张喵")
            return
        if number > maxnum:
            yield event.plain_result(f"一次获取的图片数量不能超过{maxnum}张喵")
            return
        if event.get_platform_name() == "aiocqhttp":
            logger.info(
                f"用户ID为{user_id}的用户正在获取{number}张图片,全局R18模式为{R18mode}"
            )
            if R18mode == False:
                if cr18 == True:
                    yield event.plain_result(
                        "全局r18模式为False,将使用False模式获取图片喵"
                    )
                yield event.plain_result(
                    f"正在获取{number}张图片,R18模式为False喵,大约需要{2 * number}秒喵"
                )
                start_time = time.time()
                for i in range(number):
                    for j in range(1, 4):
                        try:
                            r = await httpx.AsyncClient().get(
                                api, follow_redirects=True
                            )
                            if await self.get_kv_data(str(r.url), default=None) == None:
                                await self.put_kv_data(str(r.url), "")
                                logger.info(
                                    f"已将图片{r.url}添加至已请求列表\n\t{i + 1}/{number}"
                                )
                                urls.append(str(r.url))
                                if i == number - 1:
                                    end_time = time.time()
                                    chain = [
                                        Node(
                                            uin=3180515954,
                                            name="BOT",
                                            content=[
                                                Image.fromURL(urls[len(urls) - i - 1])
                                                for i in range(len(urls))
                                            ],
                                        ),
                                        Comp.At(qq=event.get_sender_id()),
                                        Comp.Plain(
                                            f"出来了喵!\n获取url用时{int(end_time - start_time)}秒喵\n出现了{warn}次警告和{err}次错误喵"
                                        ),
                                    ]
                                    yield event.chain_result(chain)
                                    end_time = time.time()
                                    logger.info(
                                        f"获取{number}张图片完成,总用时{end_time - start_time}秒,出现了{warn}次警告和{err}次错误"
                                    )
                            else:
                                logger.info("获取到重复图片")
                                raise ImageError("获取到重复图片")
                            break
                        except Exception as e:
                            logger.warning(
                                f"获取图片失败,错误信息为{e},正在进行第{j}次重试"
                            )
                            warn += 1
                            if j == 3:
                                err += 1
                                logger.error(f"获取图片失败:{e}")
                                yield event.plain_result(f"获取图片失败喵:(\n{e}")
            else:
                if len(R18_gr_mode) == 0 and cr18 == True:
                    logger.info(
                        "未设置群组r18模式,且用户选择的r18模式为True,按照True处理"
                    )
                    yield event.plain_result(
                        f"正在获取{number}张图片,R18模式为True喵,大约需要{2 * number}秒喵"
                    )
                    start_time = time.time()
                    for i in range(0, number):
                        for j in range(1, 4):
                            try:
                                r = await httpx.AsyncClient().get(
                                    r18_api, follow_redirects=True
                                )
                                if (
                                    await self.get_kv_data(str(r.url), default=None)
                                    == None
                                ):
                                    await self.put_kv_data(str(r.url), "")
                                    logger.info(
                                        f"已将图片{str(r.url)}添加至已请求列表\n\t{i + 1}/{number}"
                                    )
                                    urls.append(str(r.url))
                                    if i == number - 1:
                                        end_time = time.time()
                                        chain = [
                                            Node(
                                                uin=3180515954,
                                                name="BOT",
                                                content=[
                                                    Image.fromURL(
                                                        urls[len(urls) - i - 1]
                                                    )
                                                    for i in range(len(urls))
                                                ],
                                            ),
                                            Comp.At(qq=event.get_sender_id()),
                                            Comp.Plain(
                                                f"出来了喵!\n获取url用时{int(end_time - start_time)}秒喵\n出现了{warn}次警告和{err}次错误喵"
                                            ),
                                        ]
                                        yield event.chain_result(chain)
                                        end_time = time.time()
                                        logger.info(
                                            f"获取{number}张图片完成,总用时{end_time - start_time}秒,出现了{warn}次警告和{err}次错误"
                                        )
                                else:
                                    logger.info("获取到重复图片")
                                    raise ImageError("获取到重复图片")
                                break
                            except Exception as e:
                                logger.warning(
                                    f"获取图片失败,错误信息为{e},正在进行第{j}次重试"
                                )
                                warn += 1
                                if j == 3:
                                    err += 1
                                    logger.error(f"获取图片失败:{e}")
                                    yield event.plain_result(f"获取图片失败喵:(\n{e}")
                elif len(R18_gr_mode) == 0 and cr18 == False:
                    logger.info(
                        "未设置群组r18模式,但用户选择的r18模式为False,按照False处理"
                    )
                    yield event.plain_result(
                        f"正在获取{number}张图片,R18模式为False喵,大约需要{2 * number}秒喵"
                    )
                    start_time = time.time()
                    for i in range(0, number):
                        for j in range(1, 4):
                            try:
                                r = await httpx.AsyncClient().get(
                                    api, follow_redirects=True
                                )
                                if (
                                    await self.get_kv_data(str(r.url), default=None)
                                    == None
                                ):
                                    await self.put_kv_data(str(r.url), "")
                                    logger.info(
                                        f"已将图片{str(r.url)}添加至已请求列表\n\t{i + 1}/{number}"
                                    )
                                    urls.append(str(r.url))
                                    if i == number - 1:
                                        end_time = time.time()
                                        chain = [
                                            Node(
                                                uin=3180515954,
                                                name="BOT",
                                                content=[
                                                    Image.fromURL(
                                                        urls[len(urls) - i - 1]
                                                    )
                                                    for i in range(len(urls))
                                                ],
                                            ),
                                            Comp.At(qq=event.get_sender_id()),
                                            Comp.Plain(
                                                f"出来了喵!\n获取url用时{int(end_time - start_time)}秒喵\n出现了{warn}次警告和{err}次错误喵"
                                            ),
                                        ]
                                        yield event.chain_result(chain)
                                        end_time = time.time()
                                        logger.info(
                                            f"获取{number}张图片完成,总用时{end_time - start_time}秒,出现了{warn}次警告和{err}次错误"
                                        )
                                else:
                                    logger.info("获取到重复图片")
                                    raise ImageError("获取到重复图片")
                                break
                            except Exception as e:
                                logger.warning(
                                    f"获取图片失败,错误信息为{e},正在进行第{j}次重试"
                                )
                                warn += 1
                                if j == 3:
                                    err += 1
                                    logger.error(f"获取图片失败:{e}")
                                    yield event.plain_result(f"获取图片失败喵:(\n{e}")
                elif R18_gr_mode:
                    if event.get_group_id() in R18_gr_mode and cr18 == True:
                        logger.info(f"群{event.get_group_id()}的R18模式为True")
                        yield event.plain_result(
                            f"正在获取{number}张图片,R18模式为True喵,大约需要{2 * number}秒喵"
                        )
                        start_time = time.time()
                        for i in range(0, number):
                            for j in range(1, 4):
                                try:
                                    r = await httpx.AsyncClient().get(
                                        r18_api, follow_redirects=True
                                    )
                                    if (
                                        await self.get_kv_data(str(r.url), default=None)
                                        == None
                                    ):
                                        await self.put_kv_data(str(r.url), "")
                                        logger.info(
                                            f"已将图片{str(r.url)}添加至已请求列表\n\t{i + 1}/{number}"
                                        )
                                        urls.append(str(r.url))
                                        if i == number - 1:
                                            end_time = time.time()
                                            chain = [
                                                Node(
                                                    uin=3180515954,
                                                    name="BOT",
                                                    content=[
                                                        Image.fromURL(
                                                            urls[len(urls) - i - 1]
                                                        )
                                                        for i in range(len(urls))
                                                    ],
                                                ),
                                                Comp.At(qq=event.get_sender_id()),
                                                Comp.Plain(
                                                    f"出来了喵!\n获取url用时{int(end_time - start_time)}秒喵\n出现了{warn}次警告和{err}次错误喵"
                                                ),
                                            ]
                                            yield event.chain_result(chain)
                                            end_time = time.time()
                                            logger.info(
                                                f"获取{number}张图片完成,总用时{end_time - start_time}秒,出现了{warn}次警告和{err}次错误"
                                            )
                                    else:
                                        logger.info("获取到重复图片")
                                        raise ImageError("获取到重复图片")
                                    break
                                except Exception as e:
                                    logger.warning(
                                        f"获取图片失败,错误信息为{e},正在进行第{j}次重试"
                                    )
                                    warn += 1
                                    if j == 3:
                                        err += 1
                                        logger.error(f"获取图片失败:{e}")
                                        yield event.plain_result(
                                            f"获取图片失败喵:(\n{e}"
                                        )
                    elif event.get_group_id() in R18_gr_mode and cr18 == False:
                        logger.info(f"群{event.get_group_id()}的R18模式为True")
                        yield event.plain_result(
                            f"正在获取{number}张图片,R18模式为False喵,大约需要{2 * number}秒喵"
                        )
                        start_time = time.time()
                        for i in range(0, number):
                            for j in range(1, 4):
                                try:
                                    r = await httpx.AsyncClient().get(
                                        api, follow_redirects=True
                                    )
                                    if (
                                        await self.get_kv_data(str(r.url), default=None)
                                        == None
                                    ):
                                        await self.put_kv_data(str(r.url), "")
                                        logger.info(
                                            f"已将图片{str(r.url)}添加至已请求列表\n\t{i + 1}/{number}"
                                        )
                                        urls.append(str(r.url))
                                        if i == number - 1:
                                            end_time = time.time()
                                            chain = [
                                                Node(
                                                    uin=3180515954,
                                                    name="BOT",
                                                    content=[
                                                        Image.fromURL(
                                                            urls[len(urls) - i - 1]
                                                        )
                                                        for i in range(len(urls))
                                                    ],
                                                ),
                                                Comp.At(qq=event.get_sender_id()),
                                                Comp.Plain(
                                                    f"出来了喵!\n获取url用时{int(end_time - start_time)}秒喵\n出现了{warn}次警告和{err}次错误喵"
                                                ),
                                            ]
                                            yield event.chain_result(chain)
                                            end_time = time.time()
                                            logger.info(
                                                f"获取{number}张图片完成,总用时{end_time - start_time}秒,出现了{warn}次警告和{err}次错误"
                                            )
                                    else:
                                        logger.info("获取到重复图片")
                                        raise ImageError("获取到重复图片")
                                    break
                                except Exception as e:
                                    logger.warning(
                                        f"获取图片失败,错误信息为{e},正在进行第{j}次重试"
                                    )
                                    warn += 1
                                    if j == 3:
                                        err += 1
                                        logger.error(f"获取图片失败:{e}")
                                        yield event.plain_result(
                                            f"获取图片失败喵:(\n{e}"
                                        )
                    elif event.get_group_id() not in R18_gr_mode:
                        if cr18 == True:
                            yield event.plain_result(
                                "当前群组r18模式为False喵!将使用False模式获取图片喵"
                            )
                        logger.info(f"群{event.get_group_id()}的R18模式为False")
                        yield event.plain_result(
                            f"正在获取{number}张图片,R18模式为False喵,大约需要{2 * number}秒喵"
                        )
                        start_time = time.time()
                        for i in range(0, number):
                            for j in range(1, 4):
                                try:
                                    r = await httpx.AsyncClient().get(
                                        api, follow_redirects=True
                                    )
                                    if (
                                        await self.get_kv_data(str(r.url), default=None)
                                        == None
                                    ):
                                        await self.put_kv_data(str(r.url), "")
                                        logger.info(
                                            f"已将图片{str(r.url)}添加至已请求列表\n\t{i + 1}/{number}"
                                        )
                                        urls.append(str(r.url))
                                        if i == number - 1:
                                            end_time = time.time()
                                            chain = [
                                                Node(
                                                    uin=3180515954,
                                                    name="BOT",
                                                    content=[
                                                        Image.fromURL(
                                                            urls[len(urls) - i - 1]
                                                        )
                                                        for i in range(len(urls))
                                                    ],
                                                ),
                                                Comp.At(qq=event.get_sender_id()),
                                                Comp.Plain(
                                                    f"出来了喵!\n获取url用时{int(end_time - start_time)}秒喵\n出现了{warn}次警告和{err}次错误喵"
                                                ),
                                            ]
                                            yield event.chain_result(chain)
                                            end_time = time.time()
                                            logger.info(
                                                f"获取{number}张图片完成,总用时{end_time - start_time}秒,出现了{warn}次警告和{err}次错误"
                                            )
                                    else:
                                        logger.info("获取到重复图片")
                                        raise ImageError("获取到重复图片")
                                    break
                                except Exception as e:
                                    logger.warning(
                                        f"获取图片失败,错误信息为{e},正在进行第{j}次重试"
                                    )
                                    warn += 1
                                    if j == 3:
                                        err += 1
                                        logger.error(f"获取图片失败:{e}")
                                        yield event.plain_result(
                                            f"获取图片失败喵:(\n{e}"
                                        )
        else:
            logger.warning(
                f"用户ID为{user_id}的用户正在尝试使用多图图命令,但当前平台{event.get_platform_id()}不支持多图图命令"
            )
            yield event.plain_result(
                "抱歉,当前平台不支持多图图命令喵,敬请期待后续更新喵"
            )

    @图图配置.command("用户白名单")
    async def 用户白名单(
        self, event: AstrMessageEvent, mode: str = None, user_id: str = None
    ):
        """设置可以使用多图图命令的用户白名单"""
        wh_list = self.config["wh_list"]
        logger.info(f"已获取白名单:{wh_list}")
        if mode == "list":
            yield event.plain_result(f"当前白名单用户ID列表为:{wh_list}")
        elif mode == "add":
            if user_id != None:
                if str(user_id) not in wh_list:
                    wh_list.append(str(user_id))
                    self.config["wh_list"] = wh_list
                    self.config.save_config()
                    yield event.plain_result(f"已将用户ID{user_id}添加至白名单")
                    logger.info(f"已将用户ID:{user_id}添加至白名单")
                else:
                    yield event.plain_result(f"用户ID:{user_id}已在白名单中")
            else:
                yield event.plain_result("请输入用户ID")
        elif mode == "remove":
            if user_id != None:
                if str(user_id) in wh_list:
                    wh_list.remove(str(user_id))
                    self.config["wh_list"] = wh_list
                    self.config.save_config()
                    yield event.plain_result(f"已将用户ID:{user_id}从白名单中移除")
                    logger.info(f"已将用户ID:{user_id}从白名单中移除")
                else:
                    yield event.plain_result(f"用户ID:{user_id}不在白名单中")
            else:
                yield event.plain_result("请输入用户ID")
        elif mode == "help":
            yield event.plain_result(
                "白名单指令格式:\n图图配置 白名单 add 用户ID\n图图配置 白名单 remove 用户ID\n图图配置 白名单 list"
            )
        else:
            yield event.plain_result("无效的模式,请使用add、remove,list或help")

    @图图配置.command("群组白名单")
    async def 群组白名单(
        self, event: AstrMessageEvent, mode: str = None, group_id: str = None
    ):
        """设置可以使用多图图命令的群组白名单"""
        many_gr_list = self.config["many_gr_list"]
        logger.info(f"已获取群组多图图白名单:{many_gr_list}")
        if mode == "list":
            yield event.plain_result(f"多图图白名单为:{many_gr_list}")
        elif mode == "add":
            if group_id != None:
                if str(group_id) not in many_gr_list:
                    many_gr_list.append(str(group_id))
                    self.config.save_config()
                    yield event.plain_result(
                        f"已将群组ID:{group_id}添加至群组多图图白名单"
                    )
                else:
                    yield event.plain_result(f"群组ID:{group_id}已在群组多图图白名单中")
            else:
                yield event.plain_result("请输入群组ID")
        elif mode == "remove":
            if group_id != None:
                if str(group_id) in many_gr_list:
                    many_gr_list.remove(str(group_id))
                    self.config.save_config()
                    yield event.plain_result(
                        f"已将群组ID:{group_id}从群组多图图白名单中移除"
                    )
                    logger.info(f"已将群组ID:{group_id}从群组多图图白名单中移除")
                else:
                    yield event.plain_result(f"群组ID:{group_id}不在群组多图图白名单中")
            else:
                yield event.plain_result("请输入群组ID")
        elif mode == "help":
            yield event.plain_result(
                "群组多图图白名单指令格式:\n图图配置 群组多图图白名单 add 群组ID\n图圖配置 群組多圖圖白名單 remove 群組ID\n圖圖配置 群組多圖圖白名單 list"
            )
        else:
            yield event.plain_result("无效的模式,请使用add、remove,list或help")

    @图图配置.command("群组r18")
    async def 群组r18(
        self, event: AstrMessageEvent, mode: str = None, group_id: str = None
    ):
        """设置哪些群可以使用r18功能"""
        if mode == "add":
            if group_id != None:
                if str(group_id) in self.config["R18_gr_mode"]:
                    yield event.plain_result(f"群组ID:{group_id}已经在群组r18白名单中")
                else:
                    R18_gr_mode = self.config["R18_gr_mode"]
                    R18_gr_mode.append(str(group_id))
                    self.config.save_config()
                    yield event.plain_result(f"已将群组ID:{group_id}添加到列表中")
            else:
                yield event.plain_result("请输入群组ID")
        elif mode == "remove":
            if group_id != None:
                if str(group_id) not in self.config["R18_gr_mode"]:
                    yield event.plain_result(f"群组ID:{group_id}未在列表中")
                else:
                    R18_gr_mode = self.config["R18_gr_mode"]
                    R18_gr_mode.remove(str(group_id))
                    self.config.save_config()
                    yield event.plain_result(f"已将群组ID:{group_id}从列表中移除")
            else:
                yield event.plain_result("请输入群组ID")
        elif mode == "list":
            yield event.plain_result(f"当前群组r18配置为{self.config['R18_gr_mode']}")
        elif mode == "help":
            yield event.plain_result(
                "群组r18设置语法:\n/图图配置 群组r18设置 add 群组ID 模式(Ture/False)\n/图图配置 群组r18设置 remove 群组ID\n/图图配置 群组r18设置 list"
            )
        else:
            yield event.plain_result(
                "语法错误,请输入/图图配置 群组r18设置 help查看帮助"
            )

    @图图配置.command("最大数量")
    async def 最大数量(self, event: AstrMessageEvent, number: int = None):
        """设置多图图指令的最大数量"""
        if number == None:
            yield event.plain_result(
                f"当前每次获取的最大图片数量为{self.config['max_num']}"
            )
            return
        if number < 1:
            yield event.plain_result("每次获取的最大图片数量不能少于1张哦~")
            return
        self.config["max_num"] = number
        self.config.save_config()
        yield event.plain_result(f"已将每次获取的最大图片数量设置为{number}张")

    @图图配置.command("r18")
    async def r18(self, event: AstrMessageEvent, mode: str = None):
        """设置全局r18模式"""
        if mode == "on":
            self.config["R18"] = True
            self.config.save_config()
            yield event.plain_result("已开启R18模式")
            logger.info("已开启R18模式")
        elif mode == "off":
            self.config["R18"] = False
            self.config.save_config()
            yield event.plain_result("已关闭R18模式")
            logger.info("已关闭R18模式")
        elif mode == "list":
            R18mode = self.config["R18"]
            yield event.plain_result(f"当前R18模式为{R18mode}")
        elif mode == "help":
            yield event.plain_result(
                "R18指令格式:\n图图配置 R18 on\n图图配置 R18 off\n图图配置 R18 list\n图图配置 R18 help"
            )
        else:
            yield event.plain_result("无效的模式,请使用on或off")

    async def terminate(self):
        logger.info("random_pic插件已被卸载")
