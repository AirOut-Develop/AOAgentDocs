#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION_FILE="${ROOT_DIR}/VERSION"

if [[ ! -f "${VERSION_FILE}" ]]; then
  echo "VERSION 파일이 없습니다: ${VERSION_FILE}" >&2
  exit 1
fi

VERSION="$(tr -d '[:space:]' < "${VERSION_FILE}")"
if [[ -z "${VERSION}" ]]; then
  echo "VERSION 값이 비어 있습니다." >&2
  exit 1
fi

DIST_DIR="${ROOT_DIR}/dist"
OUT_FILE="${DIST_DIR}/AOAgentDocs_v${VERSION}.zip"
TMP_DIR="$(mktemp -d)"
PKG_DIR="${TMP_DIR}/AOAgentDocs"

mkdir -p "${DIST_DIR}"
mkdir -p "${PKG_DIR}"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

rsync -a \
  --exclude ".git/" \
  --exclude "dist/" \
  --exclude ".idea/" \
  --exclude ".omc/" \
  "${ROOT_DIR}/" "${PKG_DIR}/"

if command -v zip >/dev/null 2>&1; then
  (
    cd "${TMP_DIR}"
    zip -qr "${OUT_FILE}" "AOAgentDocs"
  )
elif command -v powershell.exe >/dev/null 2>&1; then
  WIN_TMP_DIR="$(wslpath -w "${TMP_DIR}")"
  WIN_OUT_FILE="$(wslpath -w "${OUT_FILE}")"
  powershell.exe -NoProfile -Command \
    "Compress-Archive -Path '${WIN_TMP_DIR}\\AOAgentDocs\\*' -DestinationPath '${WIN_OUT_FILE}' -Force" >/dev/null
else
  echo "zip 또는 powershell.exe를 찾을 수 없어 패키지를 생성할 수 없습니다." >&2
  exit 1
fi

echo "릴리즈 패키지 생성 완료: ${OUT_FILE}"
