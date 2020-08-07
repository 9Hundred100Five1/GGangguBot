import neispy
import asyncio
import discord
import datetime
import requests
import os
import sys
import pkg_resources
import time
from DiscordHelper import DiscordHelper

owner = [554114456703991808]
건의 = 738021499557904406
client = discord.Client()
helper = DiscordHelper()

@client.event
async def on_ready():
    print("로그인중")
    print(client.user.name)
    print(client.user.id)
    print("------------------")
    game = discord.Game("맛있는 급식 Eating..")
   

@client.event
async def on_message(message):

    neis = neispy.AsyncClient('e56853ad96dc4d2194472ad88a3926be')

    if message.author.bot:
        return None

    if message.content.startswith('깽구야 급식정보 '):
        try:
            msg = message.content[9:]
            scinfo = await neis.schoolInfo(SCHUL_NM=msg)
            AE = scinfo.ATPT_OFCDC_SC_CODE  # 교육청코드
            SE = scinfo.SD_SCHUL_CODE
            scmeal = await neis.mealServiceDietInfo(AE, SE)
            meal = scmeal.DDISH_NM.replace('<br/>', '\n')
            embed=discord.Embed(color=0xff00, title="깽구가 불러온 급식정보", description="``꺵구가 급식정보를 불러왔습니다. 정말 자랑스럽네요!``", timestamp=message.created_at)
            embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
            embed.add_field(name='교육청 코드', value=AE, inline=False)
            embed.add_field(name='학교 코드', value=SE, inline=False)
            embed.add_field(name='급식 정보:', value=meal, inline=True)
            await message.delete()
            await message.channel.send(embed=embed)
        except neispy.error.DataNotFound:
            await message.delete()
            await message.channel.send('해당하는 데이터가 없습니다.')
        except discord.errors.Forbidden:
            await message.channel.send('권한이 없습니다. 관리자 권한을 부여해주세요')

    if message.content == '깽구야 핑':
        ping= round(client.latency * 1000)
        if ping >= 0 and ping <= 100:
            pings = "매우좋음"
        elif ping >= 101 and ping <= 200:
            pings = "좋음" 
        elif ping >= 201 and ping <= 500:
            pings = "보통"
        elif ping >= 501 and ping <= 1000:
            pings = "나쁨"
        elif ping >= 1000:
            pings = "매우나쁨"
        embed = discord.Embed(title='🏓퐁!', colour = message.author.colour)
        embed.add_field(name = '핑', value=f'{ping}ms')
        embed.add_field(name = '상태:', value=f"{pings}")
        embed.set_thumbnail(url='https://images.emojiterra.com/google/android-10/share/1f3d3.jpg')
        await message.channel.send(embed=embed)

    if message.content.startswith("깽구야 건의 "):
            if str(message.content[7:]) == '' or str(message.content[7:]) == ' ':
                await message.channel.send("**오류 !! 오류 !! 건의사항을 입력해주세요 !! **")
            else:
                msg = message.content[7:]
                await client.get_channel(int(건의)).send(embed = discord.Embed(title=f"{message.author}님의 건의", description=msg , timestamp=message.created_at))
                await message.channel.send(f"{message.author.mention}님 ! 건의 신청이 완료되었습니다. ")
                try:
                    await message.delete()
                except discord.errors.Forbidden:
                    await message.channel.send('봇의 권한이 부족합니다. 관리자 역할을 지급해주세요.')



    if message.content == '깽구야 도와줘':
        embed=discord.Embed(color=0xff00, title="깽구의 도움 !", description="``내가 도와줄게 !``", timestamp=message.created_at)
        embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
        embed.add_field(name='깽구야 정보', value='``깽구가 자신에 대한 정보를 소개합니다.``', inline=False)
        embed.add_field(name='깽구야 급식정보 학교이름', value='``깽구가 수소문을 하면서 열심히 수집한 급식정보를 알려줍니다.``', inline=False)
        embed.add_field(name='깽구야 문의', value='``깽구봇에 대한 건의를 할수있습니다.``', inline=False)
        embed.add_field(name='깽구야 번역 번역할문장', value='``깽구가 번역을 해줍니다 !``', inline=False)
        embed.add_field(name='깽구야 핑', value='``현재 핑을 알려줍니다.``', inline=False)
        embed.add_field(name='깽구 탄신일', value='``깽구가 태어난날을 알려줍니다.``', inline=False)
        embed.add_field(name='깽구야 버전', value='``깽구봇의 버전을 알려줍니다.``', inline=False)
        await message.channel.send(embed=embed)
    
    if message.content == '깽구 탄신일':
        embed=discord.Embed(color=0xff00, title="깽구의 탄신일", description="우헤헿", timestamp=message.created_at)
        embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
        embed.add_field(name='깽구의 생일', value='**7월 27일** 은 깽구의 생일입니다 ! (선물 준비안하면 깽구가 현실갱 간다는 소문이..)', inline=False)
        await message.channel.send(embed=embed)
    
    if message.content == '깽구야 버전':
        embed=discord.Embed(color=0xff00, title="깽구의 버전", description="뾰로롱 !", timestamp=message.created_at)
        embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
        embed.add_field(name='Discord.Py 버전', value=f'`{pkg_resources.get_distribution("discord.py").version}`')
        embed.add_field(name='Python 버전', value='Python 3.8.2 64-bit')
        await message.channel.send(embed=embed)
        
    if message.content.startswith('깽구야 번역 '):
        client_id = "a6BgeA44fGPgCocW5TEX"
        client_secret = "C5PqpewyBZ"

        url = "https://openapi.naver.com/v1/papago/n2mt"

        msg = message.content[7:]
        headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
        params = {"source": "en", "target": "ko", "text": msg}
        response = requests.post(url, headers=headers, data=params)
        result = response.json()

        embed=discord.Embed(color=0xff00, title="깽구가 영차영차 번역결과를 가져왔네요 !", description="와 ! 아시는구나 !", timestamp=message.created_at)
        embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
        embed.add_field(name='결과', value=(result['message']['result']['translatedText']))
        await message.channel.send(embed=embed)

    
    if message.content.startswith("깽구야 공지 "):
        if message.author.id in owner:
            if str(message.content[7:]) == '' or str(message.content[7:]) == ' ':
                await message.channel.send("메세지를 작성하세여 !")
            try:
                msg = message.content[7:]
                oksv = 0
                embed = discord.Embed(
                    title = msg.split('&&')[0],
                    description = msg.split('&&')[1] + f"\n\n이 채널에 공지가 오기 싫다면 `봇-공지` 채널을 만들어주세요!\n[{client.user.name} 초대하기](https://discord.com/oauth2/authorize?client_id=737300288280592404&permissions=8&scope=bot)\n[팀 SB 공식 포럼](https://discord.gg/9w5DhsB)",                        colour = discord.Colour.blue(),
                    timestamp = message.created_at
                ).set_footer(icon_url=message.author.avatar_url, text=f'{message.author} - 인증됨, 원작자는 삼성해피트리입니다.' ) .set_thumbnail(url=client.user.avatar_url_as(format=None, static_format="png", size=1024))
            except IndexError:
                await message.channel.send(f"형식이 틀렸습니다. ``깽구야 공지 <제목>&&<내용>``으로 다시 시도해보세요.")
            m = await message.channel.send("아래와 같이 공지가 발신됩니다!", embed=embed)
            await m.add_reaction('✅')
            await m.add_reaction('❎')
            try:
                reaction, user = await client.wait_for('reaction_add', timeout = 20, check = lambda reaction, user: user == message.author and str(reaction.emoji) in ['✅', '❎'])
            except asyncio.TimeoutError:
                await message.channel.send('시간이 초과되었습니다.')
            else:
                if str(reaction.emoji) == "❎":
                    await message.channel.send("공지 전송이 취소되었습니다 !")
                elif str(reaction.emoji) == "✅":
                    await m.edit(content="전송중...", embed=embed)
                    for i in client.guilds:
                        arr = [0]
                        alla = False
                        flag = True
                        z = 0
                        for j in i.channels:
                            arr.append(j.id)
                            z+=1
                            if "깽구의-봇-공지" in j.name or"봇-공지" in j.name or "봇_공지" in j.name or "봇공지" in j.name or "bot_announcement" in j.name or "봇ㆍ공지" in j.name:
                                if str(j.type)=='text':
                                    try:
                                        oksv += 1
                                        await j.send(embed=embed)
                                        alla = True
                                    except:
                                        pass
                                    break
                        if alla==False:
                            try:
                                chan=i.channels[1]
                            except:
                                pass
                            if str(chan.type)=='text':
                                try:
                                    oksv += 1
                                    await chan.send(embed=embed)
                                except:
                                    pass
                    await message.channel.send(f"**`깽구 공지 전송완료 !`**\n\n{len(client.guilds)}개의 서버 중 {oksv}개의 서버에 발신 완료, {len(client.guilds) - oksv}개의 서버에 발신 실패")
                    await m.edit(content="발신이 완료되었습니다!", embed=embed)
        else:
            await message.channel.send('권한이 부족하여 메세지전송이 취소되었습니다.')

    if message.content == '깽구야 초대':
        embed=discord.Embed(color=0xff00, title="깽구봇 초대링크", description=f"[{client.user.name} 초대하기](https://discord.com/oauth2/authorize?client_id=737300288280592404&permissions=8&scope=bot)\n[팀 SB 공식 포럼](https://discord.gg/9w5DhsB)", timestamp=message.created_at)
        embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)

    if message.content == '깽구야 업타임':
        embed=discord.Embed(color=0xff00, title="깽구봇 업타임", description=f"{helper.uptime()}", timestamp=message.created_at)
        embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)




    




async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed():
        game = discord.Game("깽구야 도와줘를 통해서 명령어를 알아보세요 !")
        await client.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(10)
        game = discord.Game(f'서버:{len(client.guilds)}개/유저:{len(client.users)}명과 함께 지내는중')
        await client.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(10)
        game = discord.Game(f'핑:{round(client.latency * 1000)}ms')   
        await client.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(10)
        game = discord.Game("이 메시지는 10초 마다 바꿥니다")
        await client.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(10)
client.loop.create_task(my_background_task())


        
client.run('NzM3MzAwMjg4MjgwNTkyNDA0.Xx7WZw.3lPSS-X9edCbxG8Fv-3G7AOfdlg')
