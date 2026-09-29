#!/usr/bin/env python3
"""
Publish the v1.19.1 Zenodo deposit (zip + metadata) and mint a DOI.

Zero third-party dependencies (Python standard library only). Run this ON A
MACHINE WITH INTERNET ACCESS TO zenodo.org (the sandbox cannot reach Zenodo).

Usage:
    # Windows PowerShell
    $env:ZENODO_TOKEN = "your_personal_access_token"
    python publish_zenodo.py

    # Linux/macOS
    export ZENODO_TOKEN="your_personal_access_token"
    python publish_zenodo.py

The token is read ONLY from the ZENODO_TOKEN environment variable. It is never
printed, logged, or written to disk. If your network needs a proxy, set
HTTPS_PROXY / HTTP_PROXY as usual; the script picks them up automatically.
"""
import os
import sys
import json
import urllib.request
import urllib.error

ZENODO_API = "https://zenodo.org/api"
ZIP_NAME = "sepsis-immunoparalysis-hub-v1.19.1.zip"
HERE = os.path.dirname(os.path.abspath(__file__))


def get_token():
    t = os.environ.get("ZENODO_TOKEN")
    if not t:
        sys.exit("ERROR: set the ZENODO_TOKEN environment variable first "
                 "(it was NOT provided in any file).")
    return t


def make_opener():
    proxies = {}
    for k in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        if os.environ.get(k):
            proxies["http"] = os.environ[k]
            proxies["https"] = os.environ[k]
            break
    handlers = []
    if proxies:
        handlers.append(urllib.request.ProxyHandler(proxies))
    return urllib.request.build_opener(*handlers)


OPENER = None


def api(method, url, token, data=None, raw_body=None, content_type=None):
    """Call Zenodo API. Tries Bearer auth first, falls back to ?access_token=."""
    def do(req_url, headers, body):
        try:
            with OPENER.open(req_url, timeout=180) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            return -1, str(e)

    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        raw = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif raw_body is not None:
        raw = raw_body
        if content_type:
            headers["Content-Type"] = content_type
    else:
        raw = None

    status, body = do(urllib.request.Request(url, data=raw, method=method,
                                             headers=headers), headers, raw)
    if status in (401, 403) and "access_token=" not in url:
        sep = "&" if "?" in url else "?"
        status, body = do(
            urllib.request.Request(url + sep + "access_token=" + token,
                                  data=raw, method=method, headers={}), {}, raw)
    return status, body


def main():
    global OPENER
    token = get_token()
    OPENER = make_opener()

    zip_path = os.path.join(HERE, ZIP_NAME)
    meta_path = os.path.join(HERE, "zenodo_metadata.json")
    if not os.path.exists(zip_path):
        sys.exit(f"ERROR: {zip_path} not found.")
    if not os.path.exists(meta_path):
        sys.exit(f"ERROR: {meta_path} not found.")

    # 1) create an empty deposition
    status, body = api("POST", f"{ZENODO_API}/deposit/depositions", token, data={})
    if status != 201:
        sys.exit(f"ERROR creating deposition: HTTP {status}\n{body[:800]}")
    dep = json.loads(body)
    dep_id = dep["id"]
    print(f"[1/4] deposition created  id={dep_id}")

    # 2) upload the archive
    with open(zip_path, "rb") as f:
        filedata = f.read()
    status, body = api(
        "PUT",
        f"{ZENODO_API}/deposit/depositions/{dep_id}/files/{ZIP_NAME}",
        token, raw_body=filedata, content_type="application/octet-stream")
    if status not in (200, 201):
        sys.exit(f"ERROR uploading file: HTTP {status}\n{body[:800]}")
    print(f"[2/4] file uploaded  {ZIP_NAME} ({len(filedata):,} bytes)")

    # 3) set metadata
    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)
    status, body = api("PUT", f"{ZENODO_API}/deposit/depositions/{dep_id}",
                       token, data=meta)
    if status != 200:
        sys.exit(f"ERROR setting metadata: HTTP {status}\n{body[:800]}")
    print("[3/4] metadata set")

    # 4) publish -> mints the DOI
    status, body = api(
        "POST",
        f"{ZENODO_API}/deposit/depositions/{dep_id}/actions/publish",
        token, data={})
    if status != 202:
        sys.exit(f"ERROR publishing: HTTP {status}\n{body[:800]}")
    pub = json.loads(body)
    print("[4/4] PUBLISHED")
    print("  DOI         :", pub.get("doi"))
    print("  Concept DOI :", pub.get("conceptdoi"))
    rec = pub.get("record_url") or (pub.get("links", {}) or {}).get("record")
    print("  Record URL  :", rec)
    print("\nNext: paste this DOI into manuscript Data availability, CITATION.cff,")
    print("Reporting_Summary, SUBMISSION_MANIFEST.md and Data_Availability_Statement.txt.")


if __name__ == "__main__":
    main()
