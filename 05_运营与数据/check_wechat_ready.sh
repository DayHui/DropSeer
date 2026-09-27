#!/usr/bin/env bash
# 微信接口就绪自检（不产生任何副作用：只调 /cgi-bin/token，不建草稿、不发消息）
# 用法： bash 05_运营与数据/check_wechat_ready.sh
#
# 读取本机 .env.secret（不入库），输出 access_token 获取结果并翻译常见错误码。

set -u
# 脚本位于 <项目根>/05_运营与数据/，故项目根 = 脚本目录的上一级
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SCRIPT_DIR/.." || exit 1
ENV_FILE=".env.secret"

# 微信同一时刻只保留一个有效 access_token：本脚本自己取一次，就会顶掉 wenyan 缓存的 token，
# 导致紧接着 publish 报 40001。故脚本收尾时清掉 wenyan 的 token 缓存，强制它下次重新获取。
purge_wenyan_token() {
  local f="$APPDATA/wenyan-md/token.json"
  [ -f "$f" ] || f="/c/Users/17783/AppData/Roaming/wenyan-md/token.json"
  if [ -f "$f" ]; then
    rm -f "$f" && echo "（已清除 wenyan 的 token 缓存，避免下次 publish 报 40001）"
  fi
}

if [ ! -f "$ENV_FILE" ]; then
  echo "[FAIL] 找不到 $ENV_FILE（应含 WECHAT_APP_ID / WECHAT_APP_SECRET）"
  exit 1
fi

APP_ID=$(grep '^WECHAT_APP_ID=' "$ENV_FILE" | cut -d= -f2- | tr -d '\r')
APP_SECRET=$(grep '^WECHAT_APP_SECRET=' "$ENV_FILE" | cut -d= -f2- | tr -d '\r')

echo "AppID  : ${APP_ID:0:6}…（${#APP_ID} 字符）"
echo "Secret : ${#APP_SECRET} 字符"
echo "出口 IP: $(curl -s --max-time 15 https://api.ipify.org 2>/dev/null || echo '查询失败')"
echo "---- 请求 access_token ----"

RESP=$(curl -s --max-time 25 "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${APP_ID}&secret=${APP_SECRET}")

if echo "$RESP" | grep -q '"access_token"'; then
  echo "[1/2 OK] 凭证与白名单均已就绪，access_token 获取成功（不打印 token 本身）"
  TOKEN=$(echo "$RESP" | sed -n 's/.*"access_token":"\([^"]*\)".*/\1/p')
  echo "---- 探测草稿箱接口权限（只读 draft/count，不创建任何内容）----"
  RESP2=$(curl -s --max-time 25 "https://api.weixin.qq.com/cgi-bin/draft/count?access_token=${TOKEN}")
  echo "原始返回：$RESP2"
  if echo "$RESP2" | grep -q '"total_count"'; then
    echo "[2/2 OK] 草稿箱接口可用 → 可以直接推草稿箱（手册 §二 路径 A）"
    purge_wenyan_token
    exit 0
  fi
  CODE2=$(echo "$RESP2" | sed -n 's/.*"errcode":\([0-9-]*\).*/\1/p')
  case "$CODE2" in
    48001) echo "[2/2 FAIL] 48001 接口未授权 → 该账号无草稿箱接口权限（未认证常见），改走 §二 路径 B（render + 手动粘贴）" ;;
    45009) echo "[2/2 WARN] 45009 接口调用频率超限，稍后再试" ;;
    40001) echo "[2/2 FAIL] 40001 token 无效（可能被别处刷新覆盖），重跑本脚本即可" ;;
    *)     echo "[2/2 ?] 未识别返回，把原始返回贴给项目助手" ;;
  esac
  purge_wenyan_token
  exit 1
fi

echo "原始返回：$RESP"
CODE=$(echo "$RESP" | sed -n 's/.*"errcode":\([0-9-]*\).*/\1/p')
echo "---- 错误码解读 ----"
case "$CODE" in
  40164)
    IP=$(echo "$RESP" | sed -n 's/.*invalid ip \([0-9.]*\).*/\1/p')
    echo "  40164 IP 不在白名单"
    echo "  >>> 要加进白名单的地址：${IP:-见上方原始返回}"
    echo "      路径：公众号后台 → 设置与开发 → 基本配置 → IP 白名单"
    ;;
  40125) echo "  40125 AppSecret 无效 → 回开发者平台重置一次，重新填 .env.secret" ;;
  40013) echo "  40013 AppID 无效 → 核对 AppID 是否抄错" ;;
  48001) echo "  48001 接口未授权 → 账号类型无此权限（未认证订阅号常见），改用 render 复制粘贴路径" ;;
  *)     echo "  未识别，请把原始返回贴给项目助手" ;;
esac
exit 1
