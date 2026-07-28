#!/bin/bash
# ============================================================
#  一键部署到 GitHub Pages 用户页
#  用法：  bash deploy.sh <你的GitHub用户名>
#  例如：  bash deploy.sh xueyizhang1998
#
#  这个脚本会：改 _config.yml 里的站点地址 → git 初始化 → 提交
#             → 关联远端 → 询问后推送
#  推送前会停下来问你一次，不会偷偷传东西上去。
# ============================================================
set -euo pipefail
cd "$(dirname "$0")"

echo "==> 目录：$(pwd)"
[ -f _config.yml ] && [ -f index.html ] || { echo "错误：当前目录不像站点根目录（缺 _config.yml 或 index.html）"; exit 1; }

# ---------- 1. 环境检查 ----------
command -v git >/dev/null 2>&1 || { echo "错误：没装 git。装 Xcode 命令行工具即可： xcode-select --install"; exit 1; }

GIT_NAME="$(git config --get user.name  || true)"
GIT_MAIL="$(git config --get user.email || true)"
if [ -z "$GIT_NAME" ] || [ -z "$GIT_MAIL" ]; then
  echo "==> git 还没设置提交身份。稍后 git init 之后，只在这个仓库内设置（不动全局配置）。"
  NEED_IDENTITY=1
else
  echo "==> git 身份：$GIT_NAME <$GIT_MAIL>"
  NEED_IDENTITY=0
fi

# ---------- 2. 取 GitHub 用户名 ----------
USER_NAME="${1:-}"
if [ -z "$USER_NAME" ]; then
  echo
  echo "需要你的 GitHub 用户名（大小写照抄你 GitHub 上显示的）。"
  read -r -p "GitHub 用户名: " USER_NAME
fi
[ -n "$USER_NAME" ] || { echo "错误：用户名不能为空"; exit 1; }

REPO="${USER_NAME}.github.io"
# 域名不区分大小写，GitHub 实际提供服务的是全小写地址，站点 url 用小写才是规范形式
USER_LC="$(printf '%s' "$USER_NAME" | tr '[:upper:]' '[:lower:]')"
SITE_URL="https://${USER_LC}.github.io"
echo "==> 仓库名将是：$REPO"
echo "==> 站点地址将是：$SITE_URL"

# ---------- 3. 未填内容提醒（只警告，不阻断）----------
echo
echo "==> 检查还没填的内容："
WARN=0
grep -q 'github: *""' _data/profile.yml 2>/dev/null && { echo "    ! profile.yml 的 github 链接还是空的（侧栏不会显示图标）"; WARN=1; }
grep -q 'cv: *""'     _data/profile.yml 2>/dev/null && { echo "    ! profile.yml 的 cv 还是空的（没有 CV 按钮）"; WARN=1; }
grep -q 'period: *""' _data/projects.yml 2>/dev/null && { echo "    ! projects.yml 的项目起止年份还是空的"; WARN=1; }
[ "$WARN" = "0" ] && echo "    都填好了。"
echo "    （这些不影响上线，之后改完再推一次即可）"

# ---------- 4. 写入站点地址 ----------
echo
echo "==> 更新 _config.yml 的 url"
sed -i.bak "s|^url:.*$|url: \"${SITE_URL}\"|" _config.yml
rm -f _config.yml.bak
grep -n "^url:" _config.yml

# ---------- 5. git 初始化并提交 ----------
echo
if [ -d .git ]; then
  echo "==> 已有 git 仓库，跳过 init"
else
  echo "==> git init"
  git init -q
fi

# 只在本仓库内设置提交身份，不碰全局配置
if [ "$NEED_IDENTITY" = "1" ]; then
  echo
  echo "需要提交身份（只写进这个仓库的 .git/config，不影响你机器上其他项目）。"
  read -r -p "  姓名（如 Xueyi Zhang）: " ID_NAME
  read -r -p "  邮箱（如 xueyi.zhang@nus.edu.sg）: " ID_MAIL
  [ -n "$ID_NAME" ] && [ -n "$ID_MAIL" ] || { echo "错误：姓名和邮箱都不能为空"; exit 1; }
  git config user.name  "$ID_NAME"
  git config user.email "$ID_MAIL"
  echo "==> 已设置（仅本仓库）：$(git config --get user.name) <$(git config --get user.email)>"
fi

git add -A
if git diff --cached --quiet 2>/dev/null; then
  echo "==> 没有新变更需要提交"
else
  git commit -q -m "Academic homepage: bilingual Jekyll site" && echo "==> 已提交"
fi

git branch -M main
echo "==> 当前分支：$(git rev-parse --abbrev-ref HEAD)"

# ---------- 6. 关联远端 ----------
REMOTE_URL="https://github.com/${USER_NAME}/${REPO}.git"
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE_URL"
  echo "==> 已更新 origin"
else
  git remote add origin "$REMOTE_URL"
  echo "==> 已添加 origin"
fi
echo "==> origin = $(git remote get-url origin)"

# ---------- 7. 推送前确认 ----------
cat <<EOF

------------------------------------------------------------
下一步会执行： git push -u origin main

推送前请确认你已经在 GitHub 上建好了空仓库：
  仓库名必须正好是   ${REPO}
  建的时候不要勾选 README / .gitignore / license（保持空仓库）
  建仓库地址： https://github.com/new
------------------------------------------------------------
EOF
read -r -p "现在推送吗？(y/N) " ANS
case "$ANS" in
  y|Y|yes|YES)
    echo "==> 推送中……（可能会弹出 GitHub 登录/授权）"
    git push -u origin main
    cat <<EOF

==> 推送完成。最后一步要手动在网页上点：

  1. 打开  https://github.com/${USER_NAME}/${REPO}/settings/pages
  2. Source 选  "Deploy from a branch"
  3. Branch 选  main  ，目录选  / (root)  ，点 Save
  4. 等 1-2 分钟，打开  ${SITE_URL}

之后想改内容：改 _data/ 里的 yml，然后
    git add -A && git commit -m "update" && git push
EOF
    ;;
  *)
    echo "==> 没有推送。准备好之后自己跑： git push -u origin main"
    ;;
esac
