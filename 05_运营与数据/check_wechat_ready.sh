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
  echo "[OK] 凭证与白名单均已就绪，access_token 获取成功（不打印 token 本身）"
  exit 0
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
