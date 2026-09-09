#!/usr/bin/envpython3
#-*-coding:utf-8-*-

"""
02_英语学习系统
knowledge_image.py
======================================================================

功能：
根据英语学习文章生成ONE张配套知识图片。

核心规则：
1.一篇文章只生成一张图片
2.根据文章标题+正文决定画面内容
3.图片中加入文章原始英文标题
4.视觉风格：
-1970s–1990s日本复古动画电影感
-手绘赛璐珞动画质感
-复古背景绘画
-电影感构图
-温暖、诗意、怀旧
-细腻胶片颗粒
5.不直接模仿具体艺术家的名字
6.图片中除了文章英文标题，不允许出现其他文字
7.使用AgnesImageAPI
8.模型：
agnes-image-2.5-flash
9.输出：
2K/16:9
实际输出约为2624×1472
10.Agnes返回URL后立即下载并落盘
11.单张图片失败自动重试
12.图片失败不影响文章、试卷、音频等其他系统
13.APIKey从环境变量AGNES_API_KEY获取

======================================================================
"""

importargparse
importjson
importos
importre
importsys
importtime
frompathlibimportPath
fromurllib.errorimportHTTPError,URLError
fromurllib.requestimportRequest,urlopen


#======================================================================
#路径
#======================================================================

SCRIPT_DIR=Path(__file__).resolve().parent
SYSTEM_DIR=SCRIPT_DIR.parent

CONFIG_PATH=SYSTEM_DIR/"config"/"config.json"
OUTPUT_DIR=SYSTEM_DIR/"output"


#======================================================================
#Agnes图片参数
#======================================================================

DEFAULT_AGNES_IMAGE_MODEL="agnes-image-2.5-flash"

DEFAULT_IMAGE_SIZE="2K"
DEFAULT_IMAGE_RATIO="16:9"

MAX_RETRIES=5
RETRY_BASE_SECONDS=5

IMAGE_FILENAME="文章配图.png"


#======================================================================
#日志
#======================================================================

deflog(message:str):
print(message,flush=True)


#======================================================================
#配置
#======================================================================

defload_config()->dict:
ifnotCONFIG_PATH.exists():
raiseFileNotFoundError(
f"找不到配置文件：{CONFIG_PATH}"
)

withCONFIG_PATH.open(
"r",
encoding="utf-8"
)asf:
returnjson.load(f)


defget_required_env(name:str)->str:
value=os.getenv(name,"").strip()

ifnotvalue:
raiseRuntimeError(
f"环境变量{name}未设置或为空。"
)

returnvalue


#======================================================================
#Markdown清理
#======================================================================

defclean_text(text:str)->str:

ifnottext:
return""

#删除代码块
text=re.sub(
r"```.*?```",
"",
text,
flags=re.DOTALL
)

#删除Markdown图片
text=re.sub(
r"!\[[^\]]*\]\([^)]+\)",
"",
text
)

#Markdown链接只保留文字
text=re.sub(
r"\[([^\]]+)\]\([^)]+\)",
r"\1",
text
)

#删除Markdown标题符号
text=re.sub(
r"^\s*#+\s*",
"",
text,
flags=re.MULTILINE
)

#删除HTML
text=re.sub(
r"<[^>]+>",
"",
text
)

#压缩空白
text=re.sub(
r"\s+",
"",
text
)

returntext.strip()


#======================================================================
#提取标题和正文
#======================================================================

defextract_title_and_body(markdown_text:str):

lines=markdown_text.splitlines()

title=""

#------------------------------------------------------------------
#1.Markdown标题
#------------------------------------------------------------------

forlineinlines:

stripped=line.strip()

match=re.match(
r"^#{1,6}\s+(.+?)\s*$",
stripped
)

ifmatch:

title=clean_text(
match.group(1)
)

break

#------------------------------------------------------------------
#2.Title:
#------------------------------------------------------------------

ifnottitle:

forlineinlines:

stripped=line.strip()

match=re.match(
r"^(?:Title|TITLE|title)\s*[:：]\s*(.+)$",
stripped
)

ifmatch:

title=clean_text(
match.group(1)
)

break

#------------------------------------------------------------------
#3.中文标题：
#------------------------------------------------------------------

ifnottitle:

forlineinlines:

stripped=line.strip()

match=re.match(
r"^标题\s*[:：]\s*(.+)$",
stripped
)

ifmatch:

title=clean_text(
match.group(1)
)

break

#------------------------------------------------------------------
#4.第一行非空文本
#------------------------------------------------------------------

ifnottitle:

forlineinlines:

stripped=clean_text(line)

ifstripped:

title=stripped

break

#------------------------------------------------------------------
#正文
#------------------------------------------------------------------

body_lines=[]

forlineinlines:

stripped=line.strip()

ifnotstripped:
continue

cleaned=clean_text(stripped)

ifnotcleaned:
continue

#跳过标题
iftitleandcleaned==title:
continue

#跳过Title:
ifre.match(
r"^(?:Title|TITLE|title|标题)\s*[:：]",
cleaned
):
continue

body_lines.append(cleaned)

body=clean_text(
"\n".join(body_lines)
)

returntitle,body


#======================================================================
#自动寻找文章
#======================================================================

deffind_article_file(run_date:str)->Path:

date_dir=OUTPUT_DIR/run_date

ifnotdate_dir.exists():

raiseFileNotFoundError(
f"找不到当天输出目录：{date_dir}"
)

candidates=[]

#------------------------------------------------------------------
#优先搜索文章目录
#------------------------------------------------------------------

article_dirs=[

date_dir/"文章",

date_dir/"英语文章",

date_dir/"article",

date_dir/"articles",

]

fordirectoryinarticle_dirs:

ifdirectory.exists():

candidates.extend(
sorted(
directory.glob("*.md")
)
)

#------------------------------------------------------------------
#如果没找到，则搜索当天所有Markdown
#------------------------------------------------------------------

ifnotcandidates:

candidates=sorted(

p

forpindate_dir.rglob("*.md")

if"配图"notinstr(p)

)

ifnotcandidates:

raiseFileNotFoundError(
f"在{date_dir}中没有找到Markdown文章。"
)

#------------------------------------------------------------------
#优先文章类文件
#------------------------------------------------------------------

priority=[]

forpathincandidates:

name=path.stem.lower()

if(
"article"inname
or"english"inname
or"文章"inname
):

priority.append(path)

ifpriority:

returnpriority[0]

returncandidates[0]


#======================================================================
#图片Prompt
#======================================================================

defbuild_image_prompt(
title:str,
body:str
)->str:

#防止正文过长
body_for_prompt=body[:12000]

prompt=f"""
CreateONEcinematiceditorialillustrationbasedonthe
followingEnglishlearningarticle.

============================================================
ARTICLETITLE
============================================================

{title}

============================================================
ARTICLECONTENT
============================================================

{body_for_prompt}

============================================================
MAINREQUIREMENT
============================================================

Firstunderstandthearticle.

ThencreateONEspecific,meaningfulvisualscenethat
communicatesthecentralsubject,situation,people,
environment,action,andemotionalatmosphereofthearticle.

TheimagemustNOTbeagenericstockillustration.

Thevisualscenemustclearlyfeelconnectedtothearticle.

Ifthearticledescribespeople,showappropriatepeople
andnaturalinteraction.

Ifitdescribesaplace,maketheenvironmentimportant.

Ifitdescribeseducation,work,technology,nature,travel,
society,family,relationships,history,dailylife,oranother
topic,visuallycommunicatethattopicthroughacoherent
cinematicscene.

============================================================
VISUALSTYLE
============================================================

Japaneseretroanimatedfeature-filmaestheticinspiredby
thevisuallanguageofthe1970s,1980s,andearly1990s.

Traditionalhand-drawncelanimationfeeling.

Hand-paintedbackgrounds.

Classicpaintedanimationbackgrounds.

Subtleanalogfilmgrain.

Slightlysoftenededges.

Naturalhand-drawnlinequality.

Warmatmosphericlighting.

Poeticcinematiccomposition.

Nostalgiclate-Showaandearly-Heiseimood.

Beautifulenvironmentalstorytelling.

Naturalhumanexpressions.

Believableanatomy.

Detailedenvironments.

Quietemotionalatmosphere.

Asenseofwonder,warmth,youth,memory,andeverydaylife.

Useslightlymutedvintagecolors.

Avoidmodernglossydigital-artappearance.

Avoidphotorealism.

Avoid3D-renderedappearance.

Thefinalimageshouldfeellikeacarefullypaintedframe
fromaclassicJapaneseanimatedfeaturefilm.

============================================================
COMPOSITION
============================================================

16:9widescreencinematiccomposition.

Strongforeground,middleground,andbackground.

Clearfocalsubject.

Naturaldepth.

Elegantvisualbalance.

LeavesufficientcleannegativespacefortheEnglish
articletitle.

Thearticletitleshouldfeellikepartofabeautiful
vintageanimated-filmposter.

Theartworkremainstheprimaryvisualelement.

============================================================
ARTICLETITLEINIMAGE
============================================================

TheONLYintentionalreadabletextintheimagemustbe:

"{title}"

RenderthetitleEXACTLYasprovided.

DoNOT:

-translateit
-rewriteit
-shortenit
-abbreviateit
-replaceit
-paraphraseit
-misspellit
-inventanothertitle

UseelegantvintagecinematicEnglishtypography.

Thetitleshouldbehighlyreadable.

Placeitnaturallyinthenegativespaceofthecomposition.

Userestrained,tastefultypography.

============================================================
TEXTRESTRICTIONS
============================================================

AbsolutelyNOotherreadabletext.

Nosubtitles.

Nocaptions.

Nodialogue.

Nospeechbubbles.

NoadditionalEnglishwords.

NoChinesetext.

NoJapanesetext.

Nologos.

Nobrandnames.

Nowatermarks.

Nosignatures.

Norandomletters.

Nofakenewspapertext.

Nofakesignswithreadablewriting.

TheONLYreadabletextis:

"{title}"

============================================================
FINALIMAGE
============================================================

Onefinishedimage.

Cinematic.

Hand-painted.

Nostalgic.

Elegant.

Emotionallymeaningful.

Visuallyconnectedtothearticle.

16:9widescreen.

Highdetail.

RetroJapaneseanimationatmosphere.
"""

returnprompt.strip()


#======================================================================
#AgnesAPI请求
#======================================================================

defagnes_generate_image(
api_key:str,
base_url:str,
model:str,
prompt:str,
):
"""
调用AgnesImageAPI。

请求：

POST/images/generations

参数：

model
prompt
n
size=2K
ratio=16:9
extra_body.response_format=url
"""

url=(
base_url.rstrip("/")
+"/images/generations"
)

payload={

"model":model,

"prompt":prompt,

"n":1,

"size":DEFAULT_IMAGE_SIZE,

"ratio":DEFAULT_IMAGE_RATIO,

"extra_body":{

"response_format":"url"

},

}

data=json.dumps(
payload,
ensure_ascii=False
).encode("utf-8")

request=Request(

url,

data=data,

method="POST",

headers={

"Authorization":
f"Bearer{api_key}",

"Content-Type":
"application/json",

"Accept":
"application/json",

},

)

log("")
log("CallingAgnesImageAPI...")
log(f"Endpoint:{url}")
log(f"Model:{model}")
log(f"Size:{DEFAULT_IMAGE_SIZE}")
log(f"Ratio:{DEFAULT_IMAGE_RATIO}")

withurlopen(
request,
timeout=600
)asresponse:

raw=response.read()

result=json.loads(
raw.decode("utf-8")
)

#------------------------------------------------------------------
#API基本检查
#------------------------------------------------------------------

ifnotisinstance(result,dict):

raiseRuntimeError(
f"Agnes返回格式异常：{result}"
)

data_list=result.get("data")

ifnotdata_list:

raiseRuntimeError(
f"Agnes没有返回图片：{result}"
)

item=data_list[0]

#------------------------------------------------------------------
#URL
#------------------------------------------------------------------

image_url=item.get("url")

ifimage_url:

return{
"type":"url",
"value":image_url,
}

#------------------------------------------------------------------
#Base64备用
#------------------------------------------------------------------

b64_json=item.get("b64_json")

ifb64_json:

return{
"type":"base64",
"value":b64_json,
}

raiseRuntimeError(
f"Agnes返回中没有url或b64_json：{result}"
)


#======================================================================
#下载图片
#======================================================================

defdownload_image(
image_url:str
)->bytes:

log("")
log("Downloadinggeneratedimage...")

request=Request(

image_url,

headers={

"User-Agent":
"748686-English-Learning-System"

},

)

withurlopen(
request,
timeout=600
)asresponse:

image_bytes=response.read()

ifnotimage_bytes:

raiseRuntimeError(
"下载到的图片为空。"
)

returnimage_bytes


#======================================================================
#Base64解码
#======================================================================

defdecode_base64_image(
b64_data:str
)->bytes:

importbase64

image_bytes=base64.b64decode(
b64_data
)

ifnotimage_bytes:

raiseRuntimeError(
"Base64图片为空。"
)

returnimage_bytes


#======================================================================
#安全保存
#======================================================================

defsave_image(
image_bytes:bytes,
output_path:Path
):

output_path.parent.mkdir(
parents=True,
exist_ok=True
)

#--------------------------------------------------------------
#临时文件
#--------------------------------------------------------------

temp_path=output_path.with_suffix(
".tmp"
)

withtemp_path.open(
"wb"
)asf:

f.write(image_bytes)

f.flush()

os.fsync(
f.fileno()
)

#--------------------------------------------------------------
#原子替换
#--------------------------------------------------------------

temp_path.replace(
output_path
)


#======================================================================
#生成图片
#======================================================================

defgenerate_image(
run_date:str,
article_path:Path,
config:dict,
):

#------------------------------------------------------------------
#读取文章
#------------------------------------------------------------------

markdown=article_path.read_text(
encoding="utf-8"
)

title,body=extract_title_and_body(
markdown
)

ifnottitle:

raiseRuntimeError(
"无法从文章中提取英文标题。"
)

ifnotbody:

raiseRuntimeError(
"文章正文为空。"
)

#------------------------------------------------------------------
#日志
#------------------------------------------------------------------

log("")
log("="*72)
log("748686·02_英语学习系统")
log("KNOWLEDGEIMAGE")
log("="*72)

log(f"DATE:{run_date}")
log(f"ARTICLE:{article_path}")
log(f"TITLE:{title}")

log("="*72)

#------------------------------------------------------------------
#Agnes配置
#------------------------------------------------------------------

agnes_config=config.get(
"agnes",
{}
)

base_url=(
agnes_config
.get(
"base_url",
"https://api.agnes-ai.cn/v1"
)
.strip()
)

#------------------------------------------------------------------
#图片模型
#
#这里明确使用：
#agnes-image-2.5-flash
#
#不使用文字模型agnes-3.0-flash
#------------------------------------------------------------------

model=(
agnes_config
.get(
"image_model",
DEFAULT_AGNES_IMAGE_MODEL
)
.strip()
)

ifnotmodel:

model=DEFAULT_AGNES_IMAGE_MODEL

#------------------------------------------------------------------
#APIKey环境变量名称
#------------------------------------------------------------------

api_key_env=(
agnes_config
.get(
"api_key_env",
"AGNES_API_KEY"
)
.strip()
)

api_key=get_required_env(
api_key_env
)

#------------------------------------------------------------------
#输出
#------------------------------------------------------------------

image_dir=(
OUTPUT_DIR
/run_date
/"配图"
)

output_path=(
image_dir
/IMAGE_FILENAME
)

#------------------------------------------------------------------
#如果已经生成过
#------------------------------------------------------------------

ifoutput_path.exists():

log("")
log("✓配图已经存在")
log(f"✓{output_path}")

returnoutput_path

#------------------------------------------------------------------
#Prompt
#------------------------------------------------------------------

prompt=build_image_prompt(
title,
body
)

log("")
log("IMAGEPROMPT")
log("-"*72)
log(prompt)
log("-"*72)

#------------------------------------------------------------------
#重试
#------------------------------------------------------------------

last_error=None

forattemptinrange(
1,
MAX_RETRIES+1
):

log("")
log(
f"🖼️Agnes图片生成"
f"{attempt}/{MAX_RETRIES}"
)

try:

result=agnes_generate_image(

api_key=api_key,

base_url=base_url,

model=model,

prompt=prompt,

)

#----------------------------------------------------------
#URL
#----------------------------------------------------------

ifresult["type"]=="url":

image_bytes=download_image(
result["value"]
)

#----------------------------------------------------------
#Base64
#----------------------------------------------------------

elifresult["type"]=="base64":

image_bytes=decode_base64_image(
result["value"]
)

else:

raiseRuntimeError(
f"未知图片返回类型："
f"{result['type']}"
)

#----------------------------------------------------------
#立即保存
#----------------------------------------------------------

save_image(
image_bytes,
output_path
)

log("")
log("✓图片生成成功")
log("✓图片已经立即落盘")
log(f"✓{output_path}")

log("")
log("="*72)
log("KNOWLEDGEIMAGESUCCESS")
log("="*72)

returnoutput_path

exceptHTTPErrorase:

error_body=""

try:

error_body=(
e.read()
.decode(
"utf-8",
errors="replace"
)
)

exceptException:

pass

last_error=(
f"HTTP{e.code}:"
f"{error_body}"
)

log("")
log("❌AgnesAPI请求失败")
log(last_error)

exceptURLErrorase:

last_error=(
f"网络错误：{e}"
)

log("")
log("❌图片下载/网络错误")
log(last_error)

exceptExceptionase:

last_error=(
f"{type(e).__name__}:{e}"
)

log("")
log("❌图片生成失败")
log(last_error)

#--------------------------------------------------------------
#重试
#--------------------------------------------------------------

ifattempt<MAX_RETRIES:

wait_seconds=(
RETRY_BASE_SECONDS
*attempt
)

log(
f"⏳{wait_seconds}秒后重试..."
)

time.sleep(
wait_seconds
)

#------------------------------------------------------------------
#全部失败
#------------------------------------------------------------------

raiseRuntimeError(
"Agnes图片生成最终失败。\n"
f"最后错误：{last_error}"
)


#======================================================================
#MAIN
#======================================================================

defmain():

parser=argparse.ArgumentParser(

description=(
"02_英语学习系统："
"使用AgnesImage2.5Flash"
"生成一张英语文章配图"
)

)

parser.add_argument(

"--date",

required=True,

help=(
"文章日期，例如：2026-09-09"
)

)

parser.add_argument(

"--article",

required=False,

default="",

help=(
"可选：直接指定文章Markdown文件"
)

)

args=parser.parse_args()

run_date=args.date.strip()

#------------------------------------------------------------------
#日期格式
#------------------------------------------------------------------

ifnotre.fullmatch(
r"\d{4}-\d{2}-\d{2}",
run_date
):

raiseValueError(
f"日期格式错误：{run_date}"
)

#------------------------------------------------------------------
#读取配置
#------------------------------------------------------------------

config=load_config()

#------------------------------------------------------------------
#找文章
#------------------------------------------------------------------

ifargs.article:

article_path=Path(
args.article
)

ifnotarticle_path.is_absolute():

article_path=(
SYSTEM_DIR
/article_path
)

article_path=(
article_path.resolve()
)

ifnotarticle_path.exists():

raiseFileNotFoundError(
f"指定文章不存在："
f"{article_path}"
)

else:

article_path=find_article_file(
run_date
)

#------------------------------------------------------------------
#生成
#------------------------------------------------------------------

output_path=generate_image(

run_date=run_date,

article_path=article_path,

config=config,

)

#------------------------------------------------------------------
#最终
#------------------------------------------------------------------

log("")
log("="*72)
log("IMAGEGENERATIONFINISHED")
log("="*72)
log(f"ARTICLE:{article_path}")
log(f"IMAGE:{output_path}")
log("="*72)

return0


#======================================================================
#程序入口
#======================================================================

if__name__=="__main__":

try:

sys.exit(
main()
)

exceptKeyboardInterrupt:

log("")
log("❌用户中断。")

sys.exit(130)

exceptExceptionase:

log("")
log("="*72)
log("KNOWLEDGEIMAGEFAILED")
log("="*72)
log(
f"❌{type(e).__name__}:{e}"
)
log("="*72)

#--------------------------------------------------------------
#图片属于附加材料。
#
#图片失败不让整个英语学习系统失败。
#--------------------------------------------------------------

sys.exit(0)
